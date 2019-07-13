import typing

from pydantic import BaseModel

from .chat_enums import ChatStatus, ChatType


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

    participants: list = None  # noqa todo
    """Participants in chat with time of last activity. Can be null when you request list of chats.
     [Visible for chat admins only]"""

    is_public: bool
    """Is current chat publicly available. Always false for dialogs"""

    link: str = None
    """Link on chat if it is public"""

    description: str = None
    """Chat description"""


class Chats(BaseModel):
    chats: typing.List[Chat]
    """List of requested chats"""

    marker: int = None
    """Reference to the next page of requested chats"""
