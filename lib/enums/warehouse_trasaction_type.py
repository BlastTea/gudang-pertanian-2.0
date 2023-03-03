from enum import Enum
from typing_extensions import Self


class WarehouseTransactionType(Enum):
    IN = 'in'
    OUT = 'out'

    @classmethod
    def fromValue(cls, value: str) -> Self:
        if value == 'in':
            return cls.IN
        elif value == 'out':
            return cls.OUT
        else:
            raise ValueError(f'Unknown {value}')
