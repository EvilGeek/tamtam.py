"""This file contains message-related models"""
from pydantic import BaseModel

from .messages_enums import LinkTypes
from .chat import ChatType
from ..api import bot


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


class Message(BaseModel):
    sender: Sender = None
    """todo"""

    recipient: Recipient
    """todo"""

    timestamp: int
    """todo"""

    link: MessageLink = None
    """todo"""

    body: MessageItself
    """todo"""

    stat: Stats = None
    """todo"""

    async def respond(
        self,
        text: str,
        attachments: list = None,
        link: NewMessageLink = None,
        to: int = None,
    ) -> "Message":
        """

        :param text: Text of answer
        :param attachments: list of attachments
        :param link: NewMessageLink
        :param to: receiver
        :return: Message
        """

        bot_ = bot.Bot.current()
        assert bot_, "Bot was never initialized"

        return await bot_.send_message(
            NewMessage(text=text, attachments=attachments or [], link=link),
            user_id=to or self.sender.user_id,
            chat_id=self.recipient.chat_id,
        )

    async def reply(self, text: str, attachments: list = None) -> "Message":
        """
        Reply to peer
        :param text: text of message
        :param attachments: list of attachments
        :return: Message object
        """

        link = NewMessageLink(type=LinkTypes.reply.value, mid=self.body.mid)

        return await self.respond(text, attachments, link)

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
