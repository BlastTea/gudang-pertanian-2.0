import csv

from constants import *
from enums import ModelStatus
from models import *
from services.shared_preferences import SharedPreferences
from typing_extensions import Self
from typing import Type, TypeVar
from utils import *

T = TypeVar('T', bound=Model)


class DbHelper:
    __instance = None

    def __new__(cls: type[Self]) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __getdatabasepath__(self, t: type):
        return f'./databases/{getclassname(t)}s_test.csv'

    def __init_file__(self, t: T):
        try:
            with open(self.__getdatabasepath__(t)):
                pass
        except:
            with open(self.__getdatabasepath__(t), 'w'):
                pass

    def __read__(self, t: T) -> list[dict[str, str]]:
        self.__init_file__(t)
        with open(self.__getdatabasepath__(t)) as file:
            return list(csv.DictReader(file))

    def __write__(self, t: T, values: list[dict[str, any]]):
        self.__init_file__(t)

        with open(self.__getdatabasepath__(t), 'w', newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=self.__todict__(t()).keys())
            writer.writeheader()

            for row in values:
                writer.writerow(row)

    def __fromdict__(self, t: T, value: dict) -> T:
        instance = t()
        fields = getfields(instance)
        for i in fields:
            if issubclass(type(getattr(instance, i)), ModelEnum):
                setattr(instance, i, getattr(instance, i).fromvalue(value[i]))
            elif issubclass(type(getattr(instance, i)), Model):
                setattr(instance, i, self.__fromdict__(
                    type(getattr(instance, i)), value[i]))
            else:
                instance_type = type(getattr(instance, i))
                if instance_type is datetime:
                    setattr(instance, i, datetime.strptime(value[i], DATETIME_FORMAT))
                else:
                    setattr(instance, i, instance_type(value[i]))
        return instance

    def __todict__(self, value: Model) -> dict[str, any]:
        map = {}
        fields = getfields(value)

        for i in fields:
            if issubclass(type(getattr(value, i)), ModelEnum):
                map[i] = getattr(value, i).value
            elif issubclass(type(getattr(value, i)), Model):
                map[i+'_id'] = getattr(value, i).id
            else:
                instance_type = type(getattr(value, i))
                if instance_type is datetime:
                    map[i] = getattr(value, i).strftime(DATETIME_FORMAT)
                else:
                    map[i] = getattr(value, i)
        return map

    def create(self, value: T) -> T:
        if not isinstance(value, Model):
            raise ValueError(
                f'{type(value).__name__} must be a subclass of Model')

        model_name = getclassname(type(value))
        key_last_id = 'last_'+model_name+'_id'

        last_id = SharedPreferences().get_int(key_last_id)
        if last_id == None:
            last_id = 0
        last_id += 1
        SharedPreferences().set_int(key_last_id, last_id)

        value.id = last_id

        model_dicts = self.__read__(type(value))
        model_dicts.append(self.__todict__(value))

        self.__write__(type(value), model_dicts)
        return value

    def read(self, t: Type[T]) -> list[T]:
        if not issubclass(t, Model):
            raise ValueError(f'{t.__name__} must be a subclass of Model')

        models = []

        instance = t()

        model_changed = {}
        model_dicts = self.__read__(t)

        for i, row in enumerate(model_dicts):
            for j, key in enumerate(row):
                if key.__contains__('_id'):
                    if model_changed.get(i) is None:
                        model_changed[i] = {}
                    if model_changed.get(i).get(j) is None:
                        model_changed[i][j] = {}
                    model_changed[i][j]['pop'] = key
                    model_changed[i][j]['key'] = key.removesuffix('_id')
                    model_changed[i][j]['value'] = self.__todict__([val for val in self.read(
                        type(getattr(instance, key.removesuffix('_id')))) if val.id == int(row[key])][0])

        for i in model_changed:
            for j in model_changed[i]:
                model_dicts[i].pop(model_changed[i][j]['pop'])
                model_dicts[i][model_changed[i][j]['key']
                              ] = model_changed[i][j]['value']

        for row in model_dicts:
            models.append(self.__fromdict__(t, row))

        return models

    def update(self, value: Model):
        if not isinstance(value, Model):
            raise ValueError(
                f'{type(value).__name__} must be a subclass of Model')

        model_dicts = self.__read__(type(value))

        selected_index = 0

        for i, row in enumerate(model_dicts):
            if int(row['id']) == value.id:
                selected_index = i
                break

        model_dicts[selected_index] = self.__todict__(value)

        self.__write__(type(value), model_dicts)

    def delete(self, value: Model):
        if isinstance(value, Model):
            raise ValueError(
                f'{type(value).__name__} must be a subclass of Model')

        model_dicts = self.__read__(type(value))

        selected_index = 0

        for i, row in enumerate(model_dicts):
            if int(row['id']) == value.id:
                selected_index = i
                break

        model_dicts[selected_index]['status'] = ModelStatus.NOT_ACTIVE.value

        self.__write__(type(value), model_dicts)
