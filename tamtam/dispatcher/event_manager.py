from functools import wraps

from ..types.updates import UpdatesEnum


class ChatEvent:
    def __init__(self, dp):
        self.dp = dp

    def any(self, *filters):
        @wraps
        def decor(handler):
            self.dp.register_new_handler(handler, "CHAT_ACTION_ANY", *filters)
            return handler

        return decor

    def bot_added(self, *filters):
        @wraps
        def decor(handler):
            self.dp.register_new_handler(handler, UpdatesEnum.bot_added, *filters)
            return handler

        return decor

    def bot_removed(self, *filters):
        @wraps
        def decor(handler):
            self.dp.register_new_handler(handler, UpdatesEnum.bot_removed, *filters)
            return handler

        return decor

    def user_added(self, *filters):
        @wraps
        def decor(handler):
            self.dp.register_new_handler(handler, UpdatesEnum.user_added, *filters)
            return handler

        return decor

    def user_removed(self, *filters):
        @wraps
        def decor(handler):
            self.dp.register_new_handler(handler, UpdatesEnum.user_removed, *filters)
            return handler

        return decor

    def title_changed(self, *filters):
        @wraps
        def decor(handler):
            self.dp.register_new_handler(
                handler, UpdatesEnum.chat_title_changed, *filters
            )
            return handler

        return decor
