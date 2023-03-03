from abc import ABC, abstractmethod
from typing import Type
from typing_extensions import Self


class Model(ABC):

    def __init__(self):
        self._id: int = None

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        
    def relation() -> dict[str, Type[Self]] | None:
        return None

    @abstractmethod
    def from_map(map: dict):
        pass

    @abstractmethod
    def to_map(self) -> dict:
        pass

    @abstractmethod
    def field_names() -> list[str]:
        pass

    @abstractmethod
    def column_id(self) -> str:
        pass

    def column_status(self) -> str | None:
        return None

    @abstractmethod
    def database_path(self) -> str:
        pass

    @abstractmethod
    def key_last_id(self) -> str:
        pass
