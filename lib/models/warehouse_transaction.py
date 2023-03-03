from constants.constants import *
from datetime import datetime
from enums.warehouse_trasaction_type import WarehouseTransactionType
from models.item import Item
from models.model import Model
from models.rack import Rack
from typing_extensions import Self


class WarehouseTransaction(Model):
    def __init__(
        self,
        id: int = None,
        item: Item = None,
        rack: Rack = None,
        sender_name: str = None,
        type: WarehouseTransactionType = None,
        amount: int = None,
        date: datetime = None,
    ):
        super().__init__()
        self.id = id
        self.item = item
        self.rack = rack
        self.sender_name = sender_name
        self.type = type
        self.amount = amount
        self.date = date

    @classmethod
    def from_map(cls, map: dict) -> Self:
        return cls(
            map[COLUMN_WAREHOUSE_TRANSACTION_ID],
            Item.from_map(map['item']),
            Rack.from_map(map['rack']),
            map[COLUMN_WAREHOUSE_TRANSACTION_SENDER_NAME],
            map[COLUMN_WAREHOUSE_TRANSACTION_TYPE],
            map[COLUMN_WAREHOUSE_TRANSACTION_AMOUNT],
            datetime.strptime(map[COLUMN_WAREHOUSE_TRANSACTION_DATE], DATETIME_FORMAT),
        )
    
    def to_map(self) -> dict:
        return {
            COLUMN_WAREHOUSE_TRANSACTION_ID: self.id,
            COLUMN_ITEM_ID: self.item.id,
            COLUMN_RACK_ID: self.rack.id,
            COLUMN_WAREHOUSE_TRANSACTION_SENDER_NAME: self.sender_name,
            COLUMN_WAREHOUSE_TRANSACTION_TYPE: self.type.value,
            COLUMN_WAREHOUSE_TRANSACTION_AMOUNT: self.amount,
            COLUMN_WAREHOUSE_TRANSACTION_DATE: self.date.strftime(DATETIME_FORMAT),
        }
    
    def field_names() -> list[str]:
        return [
            COLUMN_WAREHOUSE_TRANSACTION_ID,
            COLUMN_ITEM_ID,
            COLUMN_RACK_ID,
            COLUMN_WAREHOUSE_TRANSACTION_SENDER_NAME,
            COLUMN_WAREHOUSE_TRANSACTION_TYPE,
            COLUMN_WAREHOUSE_TRANSACTION_AMOUNT,
            COLUMN_WAREHOUSE_TRANSACTION_DATE,
        ]

    @staticmethod
    def column_id(self) -> str:
        return COLUMN_WAREHOUSE_TRANSACTION_ID
    
