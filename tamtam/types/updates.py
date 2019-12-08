"""This file contains models with updates.py"""
import typing

from pydantic import BaseModel

from ..api import bot

from .messages import (
    Sender,
    Recipient,
    MessageLink,
    MessageItself,
    NewMessage,
    NewMessageLink,
    Stats,
    LinkTypes,
)  # NOQA
from .user import User
from ..helpers.vars import Var
from ..helpers.enums import MetaEnum


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

    url: str

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

        bot_ = bot.Bot.current()
        assert bot_, "Bot was never initialized"

        return await bot_.send_message(
            NewMessage(text=text, attachments=attachments or [], link=link, notify=notify),
            user_id=to or self.sender.user_id,
            chat_id=self.recipient.chat_id,
        )

    async def reply(self, text: str, attachments: list = None, notify: bool = False) -> "Message":
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
        bot_ = bot.Bot.current()
        assert bot_, "Bot was never initialized"

        return await bot_.delete_message(self.body.mid)


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

    payload: str = None
    """button payload"""

    user: User
    """user clicked button"""

    message: Message = None
    """original message containing inline keyboard"""

    async def answer(self, notification: str):
        bot_ = bot.Bot.current()
        assert bot_, "Bot was never initialized"

        await bot_.answer_callback_query(
            self.callback_id, notification=notification
        )


class MessageRemoved(BaseModel):
    timestamp: int
    """unix-time event occurred"""

    message_id: str
    """identifier of removed message"""


class MessageEdited(BaseModel):
    timestamp: int
    """unix-time event occurred"""

    message: Message
    """edited message"""


class ChatAnyAction(BaseModel):
    timestamp: int
    """unix-time action occurred"""

    chat_id: int
    """chat identifier"""

    user: User
    """user experienced action"""

    # noqa defined abv
    inviter_id: int = None
    admin_id: int = None
    title: int = None

    async def respond(
        self, text: str, attachments: list = None, link: NewMessageLink = None
    ):

        bot_ = bot.Bot.current()
        assert bot_, "Bot was never initialized"

        return await bot_.send_message(
            NewMessage(text=text, attachments=attachments or [], link=link),
            chat_id=self.chat_id,
            user_id=self.user.user_id,
        )


class BotAdded(ChatAnyAction):
    ...


class BotRemoved(ChatAnyAction):
    ...


class BotStarted(ChatAnyAction):
    ...


class UserAdded(ChatAnyAction):
    inviter_id: int
    """User who added user to chat"""


class UserRemoved(ChatAnyAction):
    admin_id: int
    """Administrator who removed user from chat"""


class ChatTitleChanged(ChatAnyAction):
    title: str
    """New title"""


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

        self.body: dict = body

    def make_update_model(self):
        if self.type in self.conf:
            model = self.conf[self.type](timestamp=self.timestamp, **self.body)
            if hasattr(model, "original"):
                return model.original
            return model

        raise NotImplemented(
            f"update_type={self.type!s} is not implemented in tamtam.py"
        )
