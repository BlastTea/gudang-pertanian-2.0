from abc import ABC, abstractmethod
from enum import Enum, EnumMeta
from six import with_metaclass
from typing_extensions import Self


class ABCEnumMeta(EnumMeta, ABC):
    pass


class ModelEnum(Enum):
    def fromvalue(cls, value):
        pass

    def translate(self) -> str:
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

    def translate(self) -> str:
        if self == self.ACTIVE:
            return 'Aktif'
        elif self == self.NOT_ACTIVE:
            return 'Tidak Aktif'
        else:
            raise ValueError(f'Unknown {self}')


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

    def translate(self) -> str:
        if self == self.FRUIT:
            return 'Buah'
        elif self == self.VEGETABLE:
            return 'Sayur'
        elif self == self.FRUIT_VEGETABLE:
            return 'Buah Sayur'
        else:
            raise ValueError(f'Unknown {self}')


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

    def translate(self) -> str:
        if self == self.DISPLAY:
            return 'Tampilan'
        elif self == self.STORAGE:
            return 'Penyimpanan'
        else:
            raise ValueError(f'Unknown {self}')


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

    def translate(self) -> str:
        if self == self.IN:
            return 'Masuk'
        elif self == self.OUT:
            return 'Keluar'
        else:
            raise ValueError(f'Unknown {self}')


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

    def translate(self) -> str:
        if self == self.UNPAID:
            return 'Belum Dibayar'
        elif self == self.PAID:
            return 'Dibayar'
        else:
            raise ValueError(f'Unknown {self}')
