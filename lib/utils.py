import os
import re

from models import Item

global_items: list[Item] = []


def getclassname(obj: type):
    return cameltosnake(obj.__name__)

def cameltosnake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snaketopascal(s: str) -> str:
    words = s.split('_')
    return ''.join([word.capitalize() for word in words])

def getfields(obj) -> list[str]:
    return [attr.removeprefix('_') for attr in obj.__dict__ if not callable(getattr(obj, attr))]

def clrscr():
    os_name = os.name.lower()
    if 'nt' in os_name: # Wndows
        os.system('cls')
    elif 'posix' in os_name: # Linux/Unix/MacOS
        os.system('clear')
    else:
        raise TypeError(f'{os_name} is unsupported')