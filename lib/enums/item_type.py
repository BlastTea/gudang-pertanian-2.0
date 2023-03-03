from enum import Enum
from typing_extensions import Self


class ItemType(Enum):
    FRUIT = 'fruit'

    VEGETABLE = 'vegetable'

    FRUIT_VEGETABLE = 'fruit vegetable'

    @classmethod
    def fromValue(cls, value: str) -> Self:
        if value == 'fruit':
            return cls.FRUIT
        elif value == 'vegetable':
            return cls.VEGETABLE
        elif value == 'fruit vegetable':
            return cls.FRUIT_VEGETABLE
        else:
            raise ValueError(f'Unknown {value}')
