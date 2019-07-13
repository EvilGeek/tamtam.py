import asyncio
import typing
import logging
import re

from ..helpers.ctx import ContextInstanceMixin
from ..types.updates import UpdatesEnum


logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


# NOQA:
def message_handler_fl_conf(
    regexp: str, from_users: typing.List[int], commands: typing.List[str]
):
    # create adequate filters config
    fl_stack = []

    if regexp:
        fl_stack.append(lambda update: re.compile(regexp).match(update.body.text))

    if from_users:
        fl_stack.append(lambda update: update.sender.user_id in from_users)

    if commands:
        fl_stack.append(
            lambda update: update.body.text.startswith("/")
            and update.body.text[1:] in commands
        )

    return fl_stack


class Handler:
    stack = []

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
                        loop.create_task(handler(update))
                        break
                else:
                    loop.create_task(handler(update))
                    break

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

        # todo
        self.message_handlers = Handler()

    async def process_events(self, events: list) -> typing.NoReturn:
        """

        :param events:
        :return:
        """
        for event in events:
            if event.update_type == UpdatesEnum.message_created:
                await self.message_handlers.notify(event.message)

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

    def register_new_message_handler(
        self,
        handler,
        *filters,
        match: str = None,
        from_users: typing.List[int] = None,
        commands: typing.List[str] = None,
    ):
        """

        :param handler:
        :param filters:
        :param match:
        :param from_users:
        :param commands:
        :return:
        """
        conf_filters = message_handler_fl_conf(
            match, from_users, commands
        )  # todo change
        self.message_handlers.register(handler, *filters, *conf_filters)

    def message_handler(
        self,
        *filters,
        match: str = None,
        from_users: typing.List[int] = None,
        commands: typing.List[str] = None,
    ):
        """

        :param filters:
        :param match:
        :param from_users:
        :param commands:
        :return:
        """

        def decor(handler):
            self.register_new_message_handler(
                handler, *filters, match=match, from_users=from_users, commands=commands
            )
            return handler

        return decor
