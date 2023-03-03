from constants.constants import *
from enums.item_type import ItemType
from enums.model_status import ModelStatus
from models.model import Model


class Item(Model):
    def __init__(
        self,
        id: int = None,
        name: str = None,
        type: ItemType = None,
        status: ModelStatus = None,
        price: int = None,
        expired_day: int = None,
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.type = type
        self.status = status
        self.price = price
        self.expired_day = expired_day

    @classmethod
    def from_map(cls, map: dict):
        return cls(
            int(map[COLUMN_ITEM_ID]),
            map[COLUMN_ITEM_NAME],
            ItemType.fromValue(map[COLUMN_ITEM_TYPE]),
            ModelStatus.fromValue(map[COLUMN_ITEM_STATUS]),
            int(map[COLUMN_ITEM_PRICE]),
            int(map[COLUMN_ITEM_EXPIRED_DAY]),
        )

    def to_map(self) -> dict:
        return {
            COLUMN_ITEM_ID: self.id,
            COLUMN_ITEM_NAME: self.name,
            COLUMN_ITEM_TYPE: self.type.value,
            COLUMN_ITEM_STATUS: self.status.value,
            COLUMN_ITEM_PRICE: self.price,
            COLUMN_ITEM_EXPIRED_DAY: self.expired_day,
        }

    @staticmethod
    def field_names() -> list[str]:
        return [
            COLUMN_ITEM_ID,
            COLUMN_ITEM_NAME,
            COLUMN_ITEM_TYPE,
            COLUMN_ITEM_STATUS,
            COLUMN_ITEM_PRICE,
            COLUMN_ITEM_EXPIRED_DAY,
        ]
    
    @staticmethod
    def column_id() -> str:
        return COLUMN_ITEM_ID
    
    @staticmethod
    def column_status() -> str | None:
        return COLUMN_ITEM_STATUS

    @staticmethod
    def database_path() -> str:
        return PATH_ITEM

    @staticmethod
    def key_last_id() -> str:
        return KEY_LAST_ITEM_ID
