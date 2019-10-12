"""This file contains message-related models"""
import typing

from pydantic import BaseModel

from .messages_enums import LinkTypes
from .chat import ChatType
from .attachments import (
    VideoAttachment,
    AudioAttachment,
    FileAttachment,
    ImageAttachment,
    InlineKeyboardAttachment,
    LocationAttachment,
    StickerAttachment
)


AnyAttachment = typing.Union[
    VideoAttachment,
    AudioAttachment,
    FileAttachment,
    ImageAttachment,
    InlineKeyboardAttachment,
    LocationAttachment,
    StickerAttachment,
]


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

    attachments: AnyAttachment = []
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
    def __init__(
        self, text: str, attachments: list, link: NewMessageLink, notify: bool = False
    ):
        super().__init__(**locals())
    """purpose of adding __init__ - make pycharm more helpful"""

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


class EditMessageConfig(BaseModel):
    chat_id: int = None
    """..."""

    message_ids: typing.List[int] = None
    """..."""

    from_: int = None
    """..."""

    to: int = None
    """..."""

    count: int = None
    """..."""

