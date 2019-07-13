"""This file contains models with updates.py"""

from enum import Enum

from pydantic import BaseModel

from .messages import Message
from ..helpers.vars import Var


class Callback:
    timestamp: int
    """todo"""

    callback_id: int
    """todo"""


class Update(BaseModel):
    update_type: str
    """todo"""

    timestamp: str
    """todo"""

    message: Message = None
    """todo"""


class UpdatesEnum(Enum):
    # TODO PRIORITY 9 FROM 11
    message_created: str = Var()
    """message_created update"""

    chat_title_changed: str = Var()
    """chat_title_changed update"""
