"""
API EXCEPTIONS

    https://dev.tamtam.chat/#section/About/HTTP-response-codes

200 — successful operation
400 — invalid request
401 — authentication error
404 — resource not found
405 — method is not allowed
429 — the number of requests is exceeded
503 — service unavailable
"""


class BaseWrapperError(Exception):
    """
    Base API-Wrapper exception, use to handle all tamtam.py requests related stuff
    """

    message: dict = ""
    """Message of error"""

    info = "Wrapper error occurred"

    def __init__(self, message: dict = None):
        self.message = message or {}

    def __repr__(self):
        return f"{self.info}: " + str(self.message)

    __str__ = __repr__


class JsonParsingError(BaseWrapperError):
    """
    Error occurred while parsing server-response json
    """

    info = "Error while parsing server response json"
