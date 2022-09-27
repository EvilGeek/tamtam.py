"""This file contains models with updates.py"""
import typing
from typing import Optional, Union


from ..helpers.enums import MetaEnum
from ..helpers.vars import Var
from .base import BaseModel
from .messages import (LinkTypes, MessageItself, MessageLink, NewMessage,
                       NewMessageLink, Recipient, Sender, Stats)
from .user import User


class UpdatesEnum(MetaEnum):
    message_callback: str = Var()
    """message_callback"""

    message_created: str = Var()
    """message_created"""

    message_removed: str = Var()
    """message_removed"""

    message_edited: str = Var()
    """message_edited"""

    bot_added: str = Var()
    """bot_added"""

    bot_removed: str = Var()
    """bot_removed"""

    user_added: str = Var()
    """user_added"""

    user_removed: str = Var()
    """user_removed"""

    chat_title_changed: str = Var()
    """chat_title_changed"""

    bot_started: str = Var()
    """bot_started"""


class Constructor(BaseModel):
    user_id: int
    """Users identifier"""

    name: str
    """Users visible name"""

    username: str
    """Unique public user name. Can be null if user is not accessible or it is not set"""


class Message(BaseModel):
    timestamp: int
    """unix-time event occurred"""

    sender: Sender = None
    """todo"""

    recipient: Recipient
    """todo"""

    link: MessageLink = None
    """todo"""

    body: MessageItself
    """todo"""

    stat: Stats = None
    """todo"""

    url: Optional[str] = None

    constructor: typing.Optional[Constructor] = None

    user_locale: typing.Optional[str] = None

    async def respond(
        self,
        text: str,
        attachments: list = None,
        link: NewMessageLink = None,
        to: int = None,
        notify: bool = False,
    ) -> "Message":
        """

        :param text: Text of answer
        :param attachments: list of attachments
        :param link: NewMessageLink
        :param to: receiver
        :param notify:
        :return: Message
        """
        self.__default_method__ = "send_message"

        return await self.call(
            NewMessage(
                text=text, attachments=attachments or [], link=link, notify=notify
            ),
            user_id=to or self.sender.user_id,
            chat_id=self.recipient.chat_id,
        )

    async def reply(
        self, text: str, attachments: typing.Optional[list] = None, notify: bool = False
    ) -> "Message":
        """
        Reply to peer
        :param text: text of message
        :param attachments: list of attachments
        :param notify:
        :return: Message object
        """

        link = NewMessageLink(type=LinkTypes.reply.value, mid=self.body.mid)

        return await self.respond(text, attachments, link, notify=notify)

    async def forward(
        self, to: int, comment: str = None, attachments: list = None
    ) -> "Message":
        """
        Forward Message of peer to another peer
        :param to: receiver
        :param comment: comment to message you forwarding
        :param attachments: list of attachments
        :return: Message object
        """

        link = NewMessageLink(type=LinkTypes.forward.value, mid=self.body.mid)

        return await self.respond(comment, attachments, link, to)

    async def delete(self):
        self.__default_method__ = "delete_message"
        return await self.call(self.body.mid)


class _MsgUpdate(BaseModel):
    message: Message

    @property
    def original(self):
        return self.message


class Callback(BaseModel):
    timestamp: int
    """unix-time when event occurred"""

    callback_id: str
    """current keyboard identifier"""

    payload: typing.Optional[str] = None
    """button payload"""

    user: User
    """user clicked button"""

    message: Message = None
    """original message containing inline keyboard"""

    user_locale: typing.Optional[str] = None

    async def answer(self, notification: str):
        await self.call(self.callback_id, notification=notification)

    __default_method__ = "answer_callback_query"
    __use_custom_call__ = True


class MessageRemoved(BaseModel):
    timestamp: int
    """unix-time event occurred"""

    message_id: str
    """identifier of removed message"""

    user_locale: typing.Optional[str] = None


class MessageEdited(BaseModel):
    timestamp: int
    """unix-time event occurred"""

    message: Message
    """edited message"""

    user_locale: typing.Optional[str] = None


class ChatAnyAction(BaseModel):
    timestamp: int
    """unix-time action occurred"""

    chat_id: int
    """chat identifier"""

    user: User
    """user experienced action"""

    # noqa defined abv
    inviter_id: typing.Optional[int] = None
    admin_id: typing.Optional[int] = None
    title: typing.Optional[str] = None

    user_locale: typing.Optional[str] = None

    async def respond(
        self, text: str, attachments: list = None, link: NewMessageLink = None
    ):
        return await self.call(
            NewMessage(text=text, attachments=attachments or [], link=link),
            chat_id=self.chat_id,
            user_id=self.user.user_id,
        )

    __default_method__ = "send_message"
    __use_custom_call__ = True


class BotAdded(ChatAnyAction):
    user_locale: typing.Optional[str] = None


class BotRemoved(ChatAnyAction):
    user_locale: typing.Optional[str] = None


class BotStarted(ChatAnyAction):
    payload: typing.Optional[str] = None
    user_locale: typing.Optional[str] = None


class UserAdded(ChatAnyAction):
    inviter_id: int
    """User who added user to chat"""
    user_locale: typing.Optional[str] = None


class UserRemoved(ChatAnyAction):
    admin_id: int
    """Administrator who removed user from chat"""

    user_locale: typing.Optional[str] = None


class ChatTitleChanged(ChatAnyAction):
    title: str
    """New title"""

    user_locale: typing.Optional[str] = None


class Update:
    conf: typing.Dict[str, typing.Any] = {
        UpdatesEnum.message_created: _MsgUpdate,
        UpdatesEnum.message_edited: MessageEdited,
        UpdatesEnum.message_callback: Callback,
        UpdatesEnum.bot_added: BotAdded,
        UpdatesEnum.bot_removed: BotRemoved,
        UpdatesEnum.chat_title_changed: ChatTitleChanged,
        UpdatesEnum.bot_started: BotStarted,
        UpdatesEnum.message_removed: MessageRemoved,
        UpdatesEnum.user_added: UserAdded,
        UpdatesEnum.user_removed: UserRemoved,
    }

    def __init__(self, update_type: str, timestamp: int, **body):
        self.type = update_type
        self.timestamp = timestamp
        self.user_locale: typing.Optional[str] = body.pop("user_locale", None)

        self.body = body

    def make_update_model(self):
        if self.type in self.conf:
            model = self.conf[self.type](
                timestamp=self.timestamp, user_locale=self.user_locale, **self.body
            )
            if hasattr(model, "original"):
                return model.original
            return model

        raise NotImplementedError(
            f"update_type={self.type!s} is not implemented in tamtam.py"
        )
