import typing
import asyncio
import re

loop = asyncio.get_event_loop()

CallableFilter = typing.Callable[[typing.Any], typing.Callable[[typing.Any], typing.Union[None, bool]]]


class MessageFilters:
    """
    Next methods should be in class
    """
    def __init__(self, *, startswith: str = None, match: str = None, commands: typing.List[str] = None):
        self.stack = list(filter(lambda x: x, [
            self.startswith(startswith) if startswith else None,
            self.commands(commands) if commands else None,
            self.match(match) if match else None,
        ]))

    @staticmethod
    def startswith(prefix) -> CallableFilter:
        return lambda update: update.body.text.startswith(prefix) if isinstance(update.body.text, str) else None

    @staticmethod
    def commands(*commands) -> CallableFilter:
        return lambda update: update.body.text.startswith("/") and update.body.text[1:] in commands

    @staticmethod
    def match(expression: str) -> CallableFilter:
        return lambda update: re.compile(expression).match(update.body.text)

    @staticmethod
    def text(text: str) -> CallableFilter:
        return lambda update: update.body.text == text
