import typing

from pydantic import BaseModel
import ujson


class ImagePayload(BaseModel):
    url: str = None
    """url"""

    token: str = None
    """..."""

    photos: typing.Dict[str, dict] = None
    """..."""

    def __init__(self, url: str, token: str, *, photos: dict):
        super().__init__(**locals())


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
        super().__init__(**locals())


class LinkButton(_BaseButton):
    type = "link"

    url: str
    """url"""

    def __init__(self, url: str):
        super().__init__(**locals())


class RequestContactButton(_BaseButton):
    type = "request_contact"


class RequestLocationButton(_BaseButton):
    type = "request_geo_location"

    quick: bool = False
    """Default: false
       If true, sends location without asking user's confirmation"""

    def __init__(self, quick: bool = False):
        super().__init__(**locals())


class ButtonPayload(BaseModel):
    buttons: typing.List[typing.List[_BaseButton]]


class _Row:
    def __init__(self, size: int = None):
        if size <= 0:
            raise ValueError("Row can not have 0 or negative width.")

        self.size: int = size
        self.__row: typing.List[_BaseButton] = []

    def add(self, button: _BaseButton):
        if self.size is not None and len(self.__row) == self.size:
            raise ValueError(f"Size of Row exceed, it expected to be {self.size!s}.")

        self.__row.append(button)

    def flush(self):
        self.__row.clear()


class ButtonsArray:
    """
    Actually not a array :D

    """
    def __init__(self):
        self._rows: typing.List[_Row] = []

    def add_row(self, width: int) -> typing.Tuple[_Row, int]:
        """
        Create new row for buttons
        :param width: size of row
        :return: Row, index of row
        """
        row = _Row(width)
        self._rows.append(row)
        return row, len(self._rows) - 1

    def delete_row(self, index: int):
        del self._rows[index]

    def get_row(self, index: int):
        return self._rows[index]


class InlineKeyboardAttachment(BaseAttachment):
    type = "inline_keyboard"
    payload: ButtonPayload

    def as_json(self):
        json = {
            "type": self.type,
            "payload": {
                "buttons": []
            }
        }

        for row in self.payload:
            for button in row:
                json["payload"]["buttons"].append(button.json())

        return ujson.dumps(json)

    @classmethod
    def from_array(cls, array: ButtonsArray):
        return cls(payload={"buttons": array})

# ===========================================================================
# END REGION KEYBOARD
# ===========================================================================
