"""This file contains message-related models"""
from pydantic import BaseModel

from .messages_enums import LinkTypes
from .chat import ChatType


class Sender(BaseModel):
    user_id: int
    """todo"""

    name: str
    """todo"""

    username: str = None
    """todo"""


class Recipient(BaseModel):
    chat_id: int = None
    """todo"""

    chat_type: ChatType
    """todo"""

    user_id: int = None
    """todo"""


class MessageItself(BaseModel):
    mid: str
    """todo"""

    seq: int
    """todo"""

    text: str = None
    """todo"""

    attachments: list = []
    """todo"""


class MessageLink(BaseModel):
    type: LinkTypes
    """todo"""

    sender: Sender
    """todo"""

    chat_id: int = None
    """todo"""

    message: MessageItself
    """todo"""


class NewMessageLink(BaseModel):
    type: LinkTypes
    """todo"""

    mid: str
    """todo"""


class NewMessage(BaseModel):
    text: str = None
    """todo"""

    attachments: list = []
    """todo"""

    link: NewMessageLink = None
    """todo"""

    notify: bool = False
    """todo"""


class Stats(BaseModel):
    views: int
    """todo"""
