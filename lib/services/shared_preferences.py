import json
from typing_extensions import Self


class SharedPreferences:
    __instance = None

    def __new__(cls: type[Self]) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        try:
            with open('shared_preferences.json') as file:
                self.data = json.load(file)
        except:
            with open('shared_preferences.json', 'w') as filee:
                filee.write(json.dumps({}))

    def __save__(self) -> bool:
        try:
            with open('shared_preferences.json', 'w') as file:
                file.write(json.dumps(self.data))
        except:
            return False
        else:
            return True

    @staticmethod
    def get_string(key: str) -> str | None:
        instance = SharedPreferences()
        try:
            return instance.data[key]
        except:
            return None

    @staticmethod
    def set_string(key: str, value: str) -> bool:
        instance = SharedPreferences()
        instance.data[key] = value
        return instance.__save__()

    @staticmethod
    def get_bool(key: str) -> bool | None:
        instance = SharedPreferences()
        try:
            return instance.data[key]
        except:
            return None

    @staticmethod
    def set_bool(key: str, value: bool) -> bool:
        instance = SharedPreferences()
        instance.data[key] = value
        return instance.__save__()

    @staticmethod
    def get_int(key: str) -> int | None:
        instance = SharedPreferences()
        try:
            return instance.data[key]
        except:
            return None

    @staticmethod
    def set_int(key: str, value: int) -> bool:
        instance = SharedPreferences()
        instance.data[key] = value
        return instance.__save__()

    @staticmethod
    def get_float(key: str) -> float | None:
        instance = SharedPreferences()
        try:
            return instance.data[key]
        except:
            return None

    @staticmethod
    def set_float(key: str, value: float) -> bool:
        instance = SharedPreferences()
        instance.data[key] = value
        return instance.__save__()

    @staticmethod
    def get_string_list(key: str) -> list[str] | None:
        instance = SharedPreferences()
        try:
            return instance.data[key]
        except:
            return None

    @staticmethod
    def set_string_list(key: str, value: list[str]) -> bool:
        instance = SharedPreferences()
        instance.data[key] = value
        return instance.__save__()
