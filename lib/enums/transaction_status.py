from enum import Enum
from typing_extensions import Self


class TransactionStatus(Enum):
    UNPAID = 'unpaid'
    PAID = 'paid'

    @classmethod
    def fromValue(cls, value: str):
        if value == 'unpaid':
            return cls.UNPAID
        elif value == 'paid':
            return cls.PAID
        else:
            raise ValueError(f'Unknown {value}')
