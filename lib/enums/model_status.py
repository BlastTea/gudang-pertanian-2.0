from enum import Enum
from typing_extensions import Self


class ModelStatus(Enum):
    ACTIVE = 'active'

    NOT_ACTIVE = 'not active'

    @classmethod
    def fromValue(cls, value: str) -> Self:
        if value == 'active':
            return cls.ACTIVE
        elif value == 'not active':
            return cls.NOT_ACTIVE
        else:
            raise ValueError(f'Unknown {value}')
