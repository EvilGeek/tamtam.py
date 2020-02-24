from typing import Union

from pydantic import BaseModel as _PydanticBaseModel


class BaseModel(_PydanticBaseModel):
    __default_method__: Union[str] = None
    """current method being called for this model on await"""

    __use_custom_call__: bool = False
    """use custom passed parameters"""

    async def call(self, *args, **kwargs):
        """
        Call bot.(self.__default_method__)((*args, **kwargs) or (self[MODEL]))
        :param args: self.__default_method__ arguments
        :param kwargs: self.__default_method__ keyword arguments
        :return: anything
        """
        from ..api import bot

        bot_ = bot.Bot.current(False)
        method = getattr(bot_, self.__default_method__)

        if self.__use_custom_call__:
            return await method(*args, **kwargs)
        else:
            return await method(self)

    def __await__(self):
        return self.call().__await__()
