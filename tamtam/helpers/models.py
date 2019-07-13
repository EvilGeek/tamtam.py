# to-use

import pydantic


class BaseModel(pydantic.BaseModel):
    """Base API model"""

    ...


class BaseHandler(type):
    """Base Dispatcher handler"""

    def __init_subclass__(mcs, **kwargs):
        ...
