"""This file contains user-related models"""

import typing

from .base import BaseModel


class BotCommand(BaseModel):
    name: str
    """[ 1 .. 64 ] characters Command name"""

    description: str
    """[ 1 .. 128 ] characters Nullable Optional command description"""


class BotPhotos(BaseModel):
    url: str = None
    """Any external image URL you want to attach"""

    token: str
    """Token of any existing attachment photos"""

    photos: typing.Any = None
    """not-disc."""


class User(BaseModel):
    user_id: int
    """Users identifier"""

    name: str
    """Users visible name"""

    username: str = None
    """Unique public user name. Can be null if user is not accessible or it is not set"""

    avatar_url: str = None
    """URL of avatar"""

    full_avatar_url: str = None
    """URL of avatar of a bigger size"""

    commands: typing.List[BotCommand] = None
    """<= 32 items Commands supported by api"""

    description: str = None
    """<= 16000 characters Bot description"""


class SetInfo(BaseModel):
    name: str = None
    """name string optional Users visible name"""

    username: str = None
    """username	string  Nullable Unique public user name. Can be null if user is not accessible or it is not set"""

    commands: typing.List[BotCommand] = None
    """commands optional Array of object (BotCommand) <= 32 items Nullable
    Commands supported by api"""

    description: str = None
    """description optional string <= 16000 characters Nullable Bot description"""

    photo: str = None
    """todo"""

    __default_method__ = "set_me"
