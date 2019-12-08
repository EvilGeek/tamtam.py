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


class ChatAction(MetaEnum):
    typing_on = TYPING_ON = "typing_on"
    """typing on"""

    sending_photo = SENDING_PHOTO = "sending_photo"
    """sending a photo"""

    sending_video = SENDING_VIDEO = "sending_video"
    """sending a video"""

    sending_audio = SENDING_AUDIO = "sending_audio"
    """sending and audio"""

    mark_seen = MARK_SEEN = "mark_seen"
    """mark as seen"""
