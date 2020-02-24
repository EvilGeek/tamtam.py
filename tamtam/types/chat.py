import datetime
import typing

from .base import BaseModel
from .chat_enums import ChatAction, ChatStatus, ChatType
from .user import User


class Icon(BaseModel):
    url: str
    """url to image source"""


class Chat(BaseModel):
    chat_id: int
    """Chats identifier"""

    type: ChatType
    """Type of chat"""

    status: ChatStatus
    """Chat status"""

    title: str = None
    """Visible title of chat. Can be null for dialogs"""

    icon: Icon = None
    """Icon of chat"""

    last_event_time: int
    """Time of last event occurred in chat"""

    participants_count: int
    """Number of people in chat. Always 2 for dialog chat type"""

    owner_id: int = None
    """Identifier of chat owner.
    [Visible only for chat admins]"""

    participants: list = None
    """Participants in chat with time of last activity. Can be null when you request list of chats.
     [Visible for chat admins only]"""

    is_public: bool
    """Is current chat publicly available. Always false for dialogs"""

    link: str = None
    """Link on chat if it is public"""

    description: str = None
    """Chat description"""

    dialog_with_user: User = None
    """todo"""

    messages_count: int = None
    """Messages count in chat. Only for group chats and channels. Not available for dialogs"""

    chat_message_id: str = None
    """Identifier of message that contains chat button initialized chat"""

    async def get_members(
        self, users_ids: typing.List[int] = None, count: int = 20, marker: int = None
    ):
        self.__default_method__ = "get_members"
        return await self.call(
            self.chat_id, users_ids=users_ids, count=count, marker=marker
        )

    async def get_admins(self):
        self.__default_method__ = "get_admins"
        return await self.call(self.chat_id)

    async def leave(self):
        self.__default_method__ = "leave_chat"
        return await self.call(self.chat_id)

    async def membership(self):
        self.__default_method__ = "get_membership"
        return await self.call(self.chat_id)

    async def action(self, action: ChatAction):
        self.__default_method__ = "action"
        return await self.call(self.chat_id, action=action)

    async def add_members(self, used_ids: typing.List[int]):
        self.__default_method__ = "add_members"
        return await self.call(self.chat_id, used_ids)

    async def remove_member(self, user_id: int):
        self.__default_method__ = "remove_member"
        return await self.call(self.chat_id, user_id)

    async def get_messages(
        self,
        messages_ids: typing.Optional[typing.List[int]] = None,
        from_date: typing.Optional[datetime.datetime] = None,
        to_date: typing.Optional[datetime.datetime] = None,
        lim: int = None,
    ):
        self.__default_method__ = "get_messages"
        return await self.call(
            self.chat_id,
            messages_ids=messages_ids,
            from_date=from_date,
            to_date=to_date,
            lim=lim,
        )

    async def edit(self, edit_chat: "EditChatInfo"):
        self.__default_method__ = "edit_chat"
        return await self.call(self.chat_id, edit_chat)

    __use_custom_call__ = True


class Chats(BaseModel):
    chats: typing.List[Chat]
    """List of requested chats"""

    marker: int = None
    """Reference to the next page of requested chats"""


class IconSetter(BaseModel):
    url: str = None
    token: str = None
    photos: typing.Dict[str, typing.Dict[str, str]] = None


class EditChatInfo(BaseModel):
    title: str
    icon: Icon


class Membership(User):
    last_access_time: int
    """..."""

    is_owner: bool
    """..."""

    is_admin: bool
    """..."""

    join_time: int
    """..."""

    permissions: typing.Optional[typing.List[str]]
    """Items Enum:"read_all_messages" "add_remove_members" "add_admins" "change_chat_info" "pin_message" "write"
       Permissions in chat if member is admin. null otherwise"""


class Members(BaseModel):
    members: typing.List[Membership]
    """..."""

    marker: typing.Optional[int] = None
    """..."""

    count: typing.Optional[int] = None
    """..."""


class Admins(Members):
    members: typing.List[Membership]
    """..."""

    marker: int
    """..."""
