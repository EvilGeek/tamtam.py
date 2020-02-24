import asyncio
import inspect
import logging
import typing
from functools import wraps

from ..api.bot import Bot
from ..helpers.ctx import ContextInstanceMixin
from ..helpers.vars import Var
from ..types.updates import ChatAnyAction, Update, UpdatesEnum
from .event_manager import ChatEvent
from .filters import MessageFilters
from .server import run_app

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()

# some handler-types
RAW = Var()
UNHANDLED = Var()
CHAT_ANY_ACTION = Var()


class Handler:
    def __init__(self):
        self.stack = []
        self.cache = {}
        self.max_cache_size = 16384  # 128 ^ 2
        self.use_cache = True

    def register(self, handler: typing.Callable[[Update], typing.NoReturn], *filters):
        """
        Filters should return positive value
        :param handler: async function
        :param filters: callable async or sync functions
        """
        async_filters = []
        sync_filters = []

        for fl in filters:
            if inspect.iscoroutinefunction(fl):
                async_filters.append(fl)
            else:
                sync_filters.append(fl)

        self.stack.append((handler, sync_filters, async_filters))

    async def run_filters(
        self,
        update: Update,
        filters: typing.List[typing.Callable],
        *,
        is_async: bool = False,
    ):
        if self.use_cache:
            if self.cache.__sizeof__() > self.max_cache_size:
                self.cache = {}

            cache = self.cache

            for fl in filters:
                if fl not in cache:
                    if is_async:
                        cache[fl] = await fl(update)
                    else:
                        cache[fl] = fl(update)
                if not cache[fl]:
                    break
            else:
                return True
            return False

        else:
            if is_async:
                return all(await fl(update) for fl in filters)
            else:
                return all(fl(update) for fl in filters)

    async def notify(self, update):
        """

        :param update:
        :return:
        """

        for handler, filters, coro_filters in self.stack or ():
            if coro_filters and filters:
                if not await self.run_filters(
                    update, filters
                ) or not await self.run_filters(update, coro_filters, is_async=True):
                    break
                else:
                    return loop.create_task(handler(update))

            elif coro_filters:
                if await self.run_filters(update, coro_filters, is_async=True):
                    return loop.create_task(handler(update))
            elif filters:
                if await self.run_filters(update, filters):
                    return loop.create_task(handler(update))
            else:
                return loop.create_task(handler(update))

    @property
    def all(self) -> typing.List[str]:
        return [f"{func.__name__}, {filters}" for func, filters in self.stack]


class Dispatcher(ContextInstanceMixin):
    def __init__(self, bot: Bot = None):
        """
        Dispatcher class
        :param bot: ..api.bot::Bot
        """
        self.bot = bot or Bot.current(no_error=False)

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
            CHAT_ANY_ACTION: Handler(),
            UNHANDLED: Handler(),
            RAW: Handler(),
        }

        self.OnChatEvent = ChatEvent(self)

        self.bot_polling = True
        self.use_polling = self.bot_polling
        self.use_webhook = not self.bot_polling

    @property
    def registered_handlers(self) -> typing.List[typing.List[str]]:
        return [handler.all for handler in self.__handlers]

    async def process_events(self, events: typing.List[Update]) -> typing.NoReturn:
        """

        :param events:
        :return:
        """
        for event in events:
            model = event.make_update_model()

            if not await self.__handlers[event.type].notify(model):

                if isinstance(model, ChatAnyAction):
                    await self.__handlers[CHAT_ANY_ACTION].notify(model)

                else:
                    await self.__handlers[UNHANDLED].notify(model)

            await self.__handlers[RAW].notify(event)

    async def poll(
        self,
        lim: int = 100,
        timeout: int = 30,
        marker: typing.Optional[int] = None,
        update_types: typing.Optional[str] = None,
        sleep_on_exc: float = 3.3,
        sleep_after_call: float = 0.01,
        skip_updates: bool = False,
    ):
        """

        :param lim:
        :param timeout:
        :param marker:
        :param update_types:
        :param sleep_on_exc:
        :param sleep_after_call:
        :param skip_updates: Skip pending updates
        :return:
        """

        while self.use_polling:
            try:
                events, marker = await self.bot.get_updates(
                    lim, timeout, marker, update_types, skip_updates
                )
            except (Exception,) as err:  # noqa
                logger.exception(f"Error {err!r} while getting new events")
                await asyncio.sleep(sleep_on_exc)
                continue

            if events:
                marker += 1
                loop.create_task(self.process_events(events))

            await asyncio.sleep(sleep_after_call)

    def listen(self, *, host: str = None, port: int = None, path: str = None, app=None):
        """
        Listen to hooks from TT
        :param host: your host
        :param port: your port
        :param path: your path
        :param app: app[Optional]
        :return:
        """
        run_app(dispatcher=self, host=host, path=path, port=port, app=app)

    def register_new_handler(self, handler, update_type, *filters):
        fls = []
        for fl in filters:
            if isinstance(fl, MessageFilters):
                for inner_fl in fl.stack:
                    fls.append(inner_fl)
            elif isinstance(fl, typing.Callable):
                fls.append(fl)

        self.__handlers[update_type].register(handler, *fls)

    def message_handler(self, *filters):
        @wraps
        def decor(handler):
            self.register_new_handler(handler, UpdatesEnum.message_created, *filters)
            return handler

        return decor

    def bot_started(self, *filters):
        @wraps
        def decor(handler):
            self.register_new_handler(handler, UpdatesEnum.bot_started, *filters)
            return handler

        return decor

    def raw_handler(self):
        @wraps
        def decor(handler):
            self.register_new_handler(handler, RAW)
            return handler

        return decor


__all__ = ["Dispatcher"]
