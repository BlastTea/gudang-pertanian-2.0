import re

from models.item import Item

global_items: list[Item] = []


def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def get_fields(obj) -> list[str]:
    return [attr for attr in obj.__dict__ if not callable(getattr(obj, attr))]