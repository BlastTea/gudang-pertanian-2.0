import csv

from copy import deepcopy
from constants.constants import *
from enums.model_status import ModelStatus
from models.item import Item
from models.model import Model
from models.rack import Rack
from services.shared_preferences import SharedPreferences
from typing_extensions import Self
from typing import Type, TypeVar
from utils.utils import *

T = TypeVar('T', bound=Model)


class DbHelper:
    __instance = None

    def __new__(cls: type[Self]) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init_file(self, t: T):
        try:
            with open(t.database_path()):
                pass
        except:
            with open(t.database_path(), 'w'):
                pass

    def __read(self, t: T) -> list[dict[str, str]]:
        self.__init_file(t)
        with open(t.database_path()) as file:
            return list(csv.DictReader(file))

    def __write(self, t: T, path: str, values: list[dict[str, any]], fieldnames: list[str]):
        self.__init_file(t)

        with open(path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()

            for row in values:
                writer.writerow(row)

    def create(self, value: Model):
        if not isinstance(value, Model):
            raise ValueError('value must be a subclass of Model')

        last_id = SharedPreferences().get_int(value.key_last_id())
        if last_id == None:
            last_id = 0
        last_id += 1
        SharedPreferences().set_int(value.key_last_id(), last_id)

        value.id = last_id

        item_dicts = self.__read(type(value))
        item_dicts.append(value.to_map())

        self.__write(type(value), value.database_path(),
                     item_dicts, value.field_names())

    def read(self, t: Type[T]) -> list[T]:
        if not issubclass(t, Model):
            raise ValueError('t must be a subclass of Model')
        
        print(f'fields : {get_fields(t)}')

        relation: dict[str, list[dict[str, str]]] = {}
        if t.relation() != None:
            for key, value in t.relation().items():
                relation[key] = self.__read(value)

        models = []

        modelDicts = self.__read(t)
        for row in modelDicts:
            if t.relation() != None:
                for key, value in t.relation().items():
                    for values in relation[key]:
                        if values[value.column_id()] == row[value.column_id()]:
                            row[key] = values

            models.append(t.from_map(row))

        return models

    def update(self, value: Model):
        if not isinstance(value, Model):
            raise ValueError('value must be a subclass of Model')

        modelDicts = self.__read(type(value))

        for row in modelDicts:
            if row[value.column_id()] == value.id:
                row = value
                break

        self.__write(type(value), value.database_path(),
                     modelDicts, value.field_names())

    def delete(self, value: Model):
        if isinstance(value, Model):
            raise ValueError('value must be a subclass of Model')
        if value.column_status() == None:
            raise ValueError("value doesn't have status column")

        modelDicts = self.__read(type(value))

        for row in modelDicts:
            if row[value.column_id()] == value.id:
                row[value.column_status()] = ModelStatus.NOT_ACTIVE.value
                break

        self.__write(type(value), value.database_path(),
                     modelDicts, value.field_names())
