from ..helpers.enums import MetaEnum


class ChatType(MetaEnum):
    dialog = "dialog"
    chat = "chat"
    channel = "channel"


class ChatStatus(MetaEnum):
    active = "active"
    """active: api is active member of chat"""

    removed = "removed"
    """removed: api was kicked"""

    left = "left"
    """left: api intentionally left chat"""

    closed = "closed"
    """closed: chat was closed"""

    suspended = "suspended"
    """..."""
