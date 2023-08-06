from enum import Enum, auto


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return [skill for skill in cls]
