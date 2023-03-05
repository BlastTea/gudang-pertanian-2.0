from abc import ABC, abstractmethod
from enum import Enum, EnumMeta
from six import with_metaclass
from typing_extensions import Self


class ABCEnumMeta(EnumMeta, ABC):
    pass


class ModelEnum(Enum):
    def fromvalue(cls, value):
        pass


class ModelStatus(ModelEnum):
    ACTIVE = 'active'

    NOT_ACTIVE = 'not active'

    @classmethod
    def fromvalue(cls, value: str) -> Self:
        if value == 'active':
            return cls.ACTIVE
        elif value == 'not active':
            return cls.NOT_ACTIVE
        else:
            raise ValueError(f'Unknown {value}')


class ItemType(ModelEnum):
    FRUIT = 'fruit'

    VEGETABLE = 'vegetable'

    FRUIT_VEGETABLE = 'fruit vegetable'

    @classmethod
    def fromvalue(cls, value: str) -> Self:
        if value == 'fruit':
            return cls.FRUIT
        elif value == 'vegetable':
            return cls.VEGETABLE
        elif value == 'fruit vegetable':
            return cls.FRUIT_VEGETABLE
        else:
            raise ValueError(f'Unknown {value}')


class RackType(ModelEnum):
    DISPLAY = 'display'

    STORAGE = 'storage'

    @classmethod
    def fromvalue(cls, value: str) -> Self:
        if value == 'display':
            return cls.DISPLAY
        elif value == 'storage':
            return cls.STORAGE
        else:
            raise ValueError(f'Unknown {value}')


class WarehouseTransactionType(ModelEnum):
    IN = 'in'

    OUT = 'out'

    @classmethod
    def fromvalue(cls, value: str) -> Self:
        if value == 'in':
            return cls.IN
        elif value == 'out':
            return cls.OUT
        else:
            raise ValueError(f'Unknown {value}')


class TransactionStatus(ModelEnum):
    UNPAID = 'unpaid'

    PAID = 'paid'

    @classmethod
    def fromvalue(cls, value: str):
        if value == 'unpaid':
            return cls.UNPAID
        elif value == 'paid':
            return cls.PAID
        else:
            raise ValueError(f'Unknown {value}')
