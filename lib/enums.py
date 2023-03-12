from enum import Enum


class TextAlign(Enum):
    LEFT = 0

    CENTER = 1

    RIGHT = 2


class Fit(Enum):
    EXPAND = 0

    TIGHT = 1


class ReturnType(Enum):
    SKIP = 0

    BACK = 1

    OK = 2

    ERROR = 3


class ModelEnum(Enum):
    def fromvalue(cls, value):
        pass

    def fromindonesianvalue(cls, value):
        pass

    def translate(self):
        pass


class ModelStatus(ModelEnum):
    ACTIVE = 'active'

    NOT_ACTIVE = 'not active'

    @classmethod
    def fromvalue(cls, value: str):
        if value == 'active':
            return cls.ACTIVE
        elif value == 'not active':
            return cls.NOT_ACTIVE
        else:
            raise ValueError(f'Unknown {value}')

    def fromindonesianvalue(cls, value):
        if value == 'aktif':
            return cls.ACTIVE
        elif value == 'tidak aktif':
            return cls.NOT_ACTIVE
        else:
            raise ValueError(f'Unknown {value}')

    def translate(self):
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
    def fromvalue(cls, value: str):
        if value == 'fruit':
            return cls.FRUIT
        elif value == 'vegetable':
            return cls.VEGETABLE
        elif value == 'fruit vegetable':
            return cls.FRUIT_VEGETABLE
        else:
            raise ValueError(f'Unknown {value}')

    def fromindonesianvalue(cls, value):
        if value == 'buah':
            return cls.FRUIT
        elif value == 'sayur':
            return cls.VEGETABLE
        elif value == 'buah sayur':
            return cls.FRUIT_VEGETABLE
        else:
            return ValueError(f'Unknown {value}')

    def translate(self):
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
    def fromvalue(cls, value: str):
        if value == 'display':
            return cls.DISPLAY
        elif value == 'storage':
            return cls.STORAGE
        else:
            raise ValueError(f'Unknown {value}')

    def fromindonesianvalue(cls, value):
        if value == 'tampilan':
            return cls.DISPLAY
        elif value == 'penyimpanan':
            return cls.STORAGE
        else:
            raise ValueError(f'Unknown {value}')

    def translate(self):
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
    def fromvalue(cls, value: str):
        if value == 'in':
            return cls.IN
        elif value == 'out':
            return cls.OUT
        else:
            raise ValueError(f'Unknown {value}')

    def fromindonesianvalue(cls, value):
        if value == 'masuk':
            return cls.IN
        elif value == 'keluar':
            return cls.OUT
        else:
            raise ValueError(f'Unknown {value}')

    def translate(self):
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

    def fromindonesianvalue(cls, value):
        if value == 'belum dibayar':
            return cls.UNPAID
        elif value == 'dibayar':
            return cls.PAID
        else:
            raise ValueError(f'Unknown {value}')

    def translate(self):
        if self == self.UNPAID:
            return 'Belum Dibayar'
        elif self == self.PAID:
            return 'Dibayar'
        else:
            raise ValueError(f'Unknown {self}')
