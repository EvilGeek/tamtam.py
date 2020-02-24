import typing

import ujson
from pydantic import BaseModel

from .types.attachments import BaseAttachment

if typing.TYPE_CHECKING:
    from .types.attachments import _BaseButton as BaseButton


class ButtonPayload(BaseModel):
    buttons: typing.List[typing.List["BaseButton"]]


class _Row:
    def __init__(self, size: int = None):
        if size <= 0:
            raise ValueError("Row can not have 0 or negative width.")

        self.size: int = size
        self.__row: typing.List["BaseButton"] = []

    def add(self, button: "BaseButton"):
        if self.size is not None and len(self.__row) == self.size:
            raise ValueError(f"Size of Row exceed, it expected to be {self.size!s}.")

        self.__row.append(button)

    def flush(self):
        self.__row.clear()


class ButtonsArray:
    """
    Helper for building button markups
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
        json = {"type": self.type, "payload": {"buttons": []}}

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
