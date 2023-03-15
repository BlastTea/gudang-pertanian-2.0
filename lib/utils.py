import os
import re

from models import Item
from typing import Callable

global_items: list[Item] = []


def getclassname(obj: type):
    return cameltosnake(obj.__name__)


def cameltosnake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def snaketopascal(s: str) -> str:
    return ''.join([word.capitalize() for word in s.split('_')])


def getfields(obj) -> list[str]:
    return [attr.removeprefix('_') for attr in obj.__dict__ if not callable(getattr(obj, attr))]


def sort_table(table: list[dict[str, object()]], on_check: Callable[[dict[str, object()]], int], sort_number: bool = True):
    length = len(table)
    for i in range(length):
        for j in range(0, length - i - 1):
            # if table[j][sort_by] > table[j + 1][sort_by]:
            if on_check(table[j]) > on_check(table[j + 1]):
                table[j], table[j + 1] = table[j + 1], table[j]
                if sort_number:
                    table[j]['No'], table[j + 1]['No'] = table[j + 1]['No'], table[j]['No']
    return table


def clrscr():
    os_name = os.name.lower()
    if 'nt' in os_name:  # Wndows
        os.system('cls')
    elif 'posix' in os_name:  # Linux/Unix/MacOS
        os.system('clear')
    else:
        raise TypeError(f'{os_name} is unsupported')
