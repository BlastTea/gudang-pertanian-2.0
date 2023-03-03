from constants.constants import *
from enums.rack_type import RackType
from enums.model_status import ModelStatus
from models.model import Model


class Rack(Model):
    def __init__(
        self,
        id: int = None,
        name: str = None,
        type: RackType = None,
        status: ModelStatus = None,
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.type = type
        self.status = status

    @classmethod
    def from_map(cls, map: dict):
        return cls(
            int(map[COLUMN_RACK_ID]),
            map[COLUMN_RACK_NAME],
            RackType.fromValue(map[COLUMN_RACK_TYPE]),
            ModelStatus.fromValue(map[COLUMN_RACK_STATUS]),
        )

    def to_map(self) -> dict:
        return {
            COLUMN_RACK_ID: self.id,
            COLUMN_RACK_NAME: self.name,
            COLUMN_RACK_TYPE: self.type.value,
            COLUMN_RACK_STATUS: self.status.value,
        }

    @staticmethod
    def field_names() -> list[str]:
        return [
            COLUMN_RACK_ID,
            COLUMN_RACK_NAME,
            COLUMN_RACK_TYPE,
            COLUMN_RACK_STATUS,
        ]

    @staticmethod
    def column_id() -> str:
        return COLUMN_RACK_ID
    
    @staticmethod
    def column_status() -> str | None:
        return COLUMN_RACK_STATUS

    @staticmethod
    def database_path() -> str:
        return PATH_RACK

    @staticmethod
    def key_last_id() -> str:
        return KEY_LAST_RACK_ID
