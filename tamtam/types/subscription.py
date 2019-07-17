import typing

from pydantic import BaseModel

from ..api import __wrapping_api_version__


class NewSubscriptionConfig(BaseModel):
    url: str
    """URL of HTTP(S)-endpoint of your bot. Must starts with http(s)://"""

    update_types: typing.List[str] = None
    """List of update types your bot want to receive. See Update object for a complete list of types"""

    version: str = __wrapping_api_version__
    """Version of API. Affects model representation"""


class Subscription(BaseModel):
    url: str
    """Webhook url"""

    time: int
    """Unix-time when subscription was created"""

    update_types: typing.List[str] = None
    """Update types bot subscribed for"""

    version: str = None
    r"""[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"""
