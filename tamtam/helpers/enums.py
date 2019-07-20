from enum import Enum


class MetaEnum(Enum):
    @classmethod
    def has(cls, item):
        return any((item == var.value) or (item == var) for var in cls)
