from copy import deepcopy
from constants.constants import *
from models.item import Item
from models.model import Model
from models.rack import Rack
from typing_extensions import Self
from typing import Type
from datetime import datetime


class ItemRack(Model):
    def __init__(
        self,
        id: int = None,
        item: Item = Item(),
        rack: Rack = Rack(),
        stock: int = None,
        date: datetime = None,
    ):
        super().__init__()
        self.id = id
        self.item = item
        self.rack = rack
        self.stock = stock
        self.date = date

    def __deepcopy__(self, memo):
        new_obj = ItemRack(
            id=deepcopy(self.id, memo),
            stock=deepcopy(self.stock, memo),
            date=deepcopy(self.date, memo),
        )
        new_obj.item = deepcopy(self.item, memo)
        new_obj.rack = deepcopy(self.rack, memo)
        return new_obj

    @classmethod
    def from_map(cls, map: dict) -> Self:
        return cls(
            map[COLUMN_ITEM_RACK_ID],
            Item.from_map(map['item']),
            Rack.from_map(map['rack']),
            map[COLUMN_ITEM_RACK_STOCK],
            datetime.strptime(map[COLUMN_ITEM_RACK_DATE], DATETIME_FORMAT),
        )

    def to_map(self) -> dict:
        return {
            COLUMN_ITEM_RACK_ID: self.id,
            COLUMN_ITEM_ID: self.item.id,
            COLUMN_RACK_ID: self.rack.id,
            COLUMN_ITEM_RACK_STOCK: self.stock,
            COLUMN_ITEM_RACK_DATE: self.date.strftime(DATETIME_FORMAT),
        }

    @staticmethod
    def field_names() -> list[str]:
        return [
            COLUMN_ITEM_RACK_ID,
            COLUMN_ITEM_ID,
            COLUMN_RACK_ID,
            COLUMN_ITEM_RACK_STOCK,
            COLUMN_ITEM_RACK_DATE,
        ]

    @staticmethod
    def column_id() -> str:
        return COLUMN_ITEM_RACK_ID

    @staticmethod
    def database_path() -> str:
        return PATH_ITEM_RACK

    @staticmethod
    def key_last_id() -> str:
        return KEY_LAST_ITEM_RACK_ID

    @staticmethod
    def relation() -> dict[str, Type[Model]] | None:
        return {
            'item': Item,
            'rack': Rack,
        }
