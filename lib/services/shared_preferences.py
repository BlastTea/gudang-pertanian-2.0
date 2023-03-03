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

    def get_string(self, key: str) -> str | None:
        try:
            return self.data[key]
        except:
            return None

    def set_string(self, key: str, value: str) -> bool:
        self.data[key] = value
        return self.__save__()

    def get_bool(self, key: str) -> bool | None:
        try:
            return self.data[key]
        except:
            return None

    def set_bool(self, key: str, value: bool) -> bool:
        self.data[key] = value
        return self.__save__()

    def get_int(self, key: str) -> int | None:
        try:
            return self.data[key]
        except:
            return None

    def set_int(self, key: str, value: int) -> bool:
        self.data[key] = value
        return self.__save__()

    def get_float(self, key: str) -> float | None:
        try:
            return self.data[key]
        except:
            return None

    def set_float(self, key: str, value: float) -> bool:
        self.data[key] = value
        return self.__save__()

    def get_string_list(self, key: str) -> list[str] | None:
        try:
            return self.data[key]
        except:
            return None

    def set_string_list(self, key: str, value: list[str]) -> bool:
        self.data[key] = value
        return self.__save__()
