import typing

from .base import BaseModel


class ImagePayload(BaseModel):
    url: str = None
    """url"""

    token: str = None
    """..."""

    photos: typing.Dict[str, dict] = None
    """..."""

    def __init__(self, url: str, token: str, *, photos: dict):
        super().__init__(url=url, token=token, photos=photos)


class BaseAttachment(BaseModel):
    type: str
    payload: BaseModel


class ImageAttachment(BaseAttachment):
    type = "image"
    """..."""

    payload: ImagePayload
    """..."""


class _TokenAttachment(BaseAttachment):
    payload: typing.Dict[str, str]
    """payload(token.str)"""


class VideoAttachment(_TokenAttachment):
    type = "video"
    """video"""


class AudioAttachment(_TokenAttachment):
    type = "audio"
    """audio"""


class FileAttachment(_TokenAttachment):
    type = "file"
    """file"""


class StickerAttachment(_TokenAttachment):
    """NOTE: instead of token key you should use code for stickers"""

    type = "sticker"


class ContactPayload(BaseAttachment):
    type = "contact"

    name: str = None
    """contact name"""

    contactId: int = None
    """contact identifier"""

    vcfInfo: str = None
    """Full information about contact in VCF format"""

    vcfPhone: str = None
    """Contact phone in VCF format"""


class LocationAttachment(BaseAttachment):
    type = "location"
    """location"""

    latitude: float
    """lat"""

    longitude: float
    """lon"""


# =========================================================================
# KEYBOARDS REGION START
# =========================================================================


class _BaseButton(BaseModel):
    type: str
    """type"""

    text: str
    """visible text of button. 128 max size char-array"""


class CallbackButton(_BaseButton):
    type = "callback"

    payload: str
    """payload of button"""

    intent: str = "default"
    """Default: "default" Enum:"positive" "negative" "default"
       Intent of button. Affects clients representation"""

    def __init__(self, text: str, payload: str, intent: str = "default"):
        super().__init__(text=text, payload=payload, intent=intent)


class LinkButton(_BaseButton):
    type = "link"

    url: str
    """url"""

    def __init__(self, url: str):
        super().__init__(url=url)


class RequestContactButton(_BaseButton):
    type = "request_contact"


class RequestLocationButton(_BaseButton):
    type = "request_geo_location"

    quick: bool = False
    """Default: false
       If true, sends location without asking user's confirmation"""

    def __init__(self, quick: bool = False):
        super().__init__(quick=quick)
