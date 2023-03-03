from enum import Enum
from typing_extensions import Self


class RackType(Enum):
    DISPLAY = 'display'

    STORAGE = 'storage'

    @classmethod
    def fromValue(cls, value: str) -> Self:
        if value == 'display':
            return cls.DISPLAY
        elif value == 'storage':
            return cls.STORAGE
        else:
            raise ValueError(f'Unknown {value}')
