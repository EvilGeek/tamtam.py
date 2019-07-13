import asyncio
import typing
import logging

from ..helpers.ctx import ContextInstanceMixin
from ..types.updates import (
    UpdatesEnum,
    Update,
    ChatAnyAction
)

from .event_manager import ChatEvent
from .filters import MessageFilters


logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


class Handler:
    def __init__(self):
        self.stack = []

    def register(self, handler: typing.Callable, *filters):
        """

        :param handler:
        :param filters:
        :return:
        """
        self.stack.append((handler, filters))

    async def notify(self, update):
        """

        :param update:
        :return:
        """

        if self.stack:
            for handler, filters in self.stack:
                if filters:
                    if all(fl(update) for fl in filters):
                        return loop.create_task(handler(update))
                else:
                    return loop.create_task(handler(update))

    @property
    def all(self) -> typing.List[str]:
        return [f"{func.__name__}, {filters}" for func, filters in self.stack]


class Dispatcher(ContextInstanceMixin):
    def __init__(self, bot):
        """

        :param bot:
        """
        self.bot = bot
        self.__polling = True

        self.set_current(self)

        self.chat_actions_handlers = Handler()

        self.__handlers = {
            UpdatesEnum.message_created: Handler(),
            UpdatesEnum.message_edited: Handler(),
            UpdatesEnum.message_callback: Handler(),
            UpdatesEnum.bot_added: Handler(),
            UpdatesEnum.bot_removed: Handler(),
            UpdatesEnum.chat_title_changed: Handler(),
            UpdatesEnum.bot_started: Handler(),
            UpdatesEnum.message_removed: Handler(),
            UpdatesEnum.user_added: Handler(),
            UpdatesEnum.user_removed: Handler(),
            "CHAT_ACTION_ANY": Handler(),
            "UNHANDLED": Handler(),
            "RAW": Handler()
        }

        self.OnChatEvents = ChatEvent(self)

    async def process_events(self, events: typing.List[Update]) -> typing.NoReturn:
        """

        :param events:
        :return:
        """
        for event in events:
            model = event.make_update_model()

            if not await self.__handlers[event.type].notify(model):

                if isinstance(model, ChatAnyAction):
                    await self.__handlers["CHAT_ACTION_ANY"].notify(model)

                else:
                    await self.__handlers["UNHANDLED"].notify(model)

            await self.__handlers["RAW"].notify(model)

    async def idle(
        self,
        lim: int = 100,
        timeout: int = 30,
        marker: typing.Optional[int] = None,
        update_types: typing.Optional[str] = None,
        sleep_on_exc: float = 3.3,
        sleep_after_call: float = 0.01,
    ):
        """

        :param lim:
        :param timeout:
        :param marker:
        :param update_types:
        :param sleep_on_exc:
        :param sleep_after_call:
        :return:
        """
        while self.__polling:
            try:
                events, marker = await self.bot.get_updates(
                    lim, timeout, marker, update_types
                )
            except:  # noqa
                logger.exception("Error while getting new events")
                await asyncio.sleep(sleep_on_exc)
                continue

            if events:
                marker += 1
                loop.create_task(self.process_events(events))

            await asyncio.sleep(sleep_after_call)

    def register_new_handler(self, handler, update_type, *filters):
        fls = []
        for fl in filters:
            if isinstance(fl, MessageFilters):
                for inner_fl in fl.stack:
                    fls.append(inner_fl)
            else:
                fls.append(fl)

        self.__handlers[update_type].register(handler, *fls)

    def message_handler(self, *filters):
        def decor(handler):
            self.register_new_handler(handler, UpdatesEnum.message_created, *filters)
            return handler

        return decor

    def bot_started(self, *filters):
        def decor(handler):
            self.register_new_handler(handler, UpdatesEnum.bot_started, *filters)
            return handler

        return decor

    def raw_handler(self):
        def decor(handler):
            self.register_new_handler(handler, "RAW")
            return handler

        return decor
