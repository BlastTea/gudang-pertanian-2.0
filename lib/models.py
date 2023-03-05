from abc import ABC
from datetime import datetime
from enums import *


class Model(ABC):
    def __init__(self):
        self._id = 0
        self._status = ModelStatus.ACTIVE

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: ModelStatus):
        self._status = value


class Item(Model):
    def __init__(
        self,
        id: int = 0,
        status: ModelStatus = ModelStatus.ACTIVE,
        name: str = '',
        type: ItemType = ItemType.FRUIT,
        price: int = 0,
        expired_day: int = 0,
    ):
        super().__init__()
        self.id = id
        self.status = status
        self.name = name
        self.type = type
        self.price = price
        self.expired_day = expired_day


class Rack(Model):
    def __init__(
        self,
        id: int = 0,
        status: ModelStatus = ModelStatus.ACTIVE,
        name: str = '',
        type: RackType = RackType.DISPLAY,
    ):
        super().__init__()
        self.id = id
        self.status = status
        self.name = name
        self.type = type


class ItemRack(Model):
    def __init__(
        self,
        id: int = 0,
        status: ModelStatus = ModelStatus.ACTIVE,
        item: Item = Item(),
        rack: Rack = Rack(),
        stock: int = 0,
        date: datetime = datetime.now(),
    ):
        super().__init__()
        self.id = id
        self.status = status
        self.item = item
        self.rack = rack
        self.stock = stock
        self.date = date


class WarehouseTransaction(Model):
    def __init__(
        self,
        id: int = 0,
        status: ModelStatus = ModelStatus.ACTIVE,
        item: Item = Item(),
        rack: Rack = Rack(),
        sender_name: str = '',
        type: WarehouseTransactionType = None,
        amount: int = 0,
        date: datetime = datetime.now(),
    ):
        super().__init__()
        self.id = id
        self.status = status
        self.item = item
        self.rack = rack
        self.sender_name = sender_name
        self.type = type
        self.amount = amount
        self.date = date


class Transaction(Model):
    def __init__(
        self,
        id: int = 0,
        status: ModelStatus = ModelStatus.ACTIVE,
        name: str = '',
        transaction_status: TransactionStatus = TransactionStatus.UNPAID,
        date: datetime = datetime.now(),
        pay: int = 0,
    ):
        super().__init__()
        self.id = id
        self.status = status
        self.name = name
        self.transaction_status = transaction_status
        self.date = date
        self.pay = pay


class ItemTransaction(Model):
    def __init__(
        self,
        id: int = 0,
        status: ModelStatus = ModelStatus.ACTIVE,
        transaction: Transaction = Transaction(),
        item: Item = Item(),
        amount: int = 0,
    ):
        super().__init__()
        self.id = id
        self.status = status
        self.transaction = transaction,
        self.item = item
        self.amount = amount
