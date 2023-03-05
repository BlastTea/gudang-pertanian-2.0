from typing import Generic, TypeVar
from constants import *
from datetime import datetime
from enums import *
from services.db_helper import DbHelper
from models import *
from utils import *
import inspect

# with open(ITEMS_PATH) as file:
#     for i, value in enumerate(csv.DictReader(file)):
#         print(f'{i} : {value}')
#         # global_items.append(Item.from_list(row))

# a = ItemRack
# newInstance = a()
# for field in get_fields(newInstance):
#     print(f'is subclass of Model ({field}) : {type(getattr(newInstance, field))}')


# for value in DbHelper().read(ItemRack):
#     print(f'I Have {value.item.name} inside {value.rack.name} with value of {value.stock}')

# ItemRack()

# Item()

# DbHelper().create(ItemRack(item=Item(id=1), rack=Rack(id=1), date=datetime.now(), stock=10))

# DbHelper().create(Rack('Rak 1', RackType.STORAGE, ModelStatus.ACTIVE))

# for name, field in inspect.getmembers(A):
#     if inspect.isfunction(field) and hasattr(field, '__field_type__'):
#         print(f'{name}: {field}: {getattr(field, "__field_type__")}')
# createdItem = DbHelper().create(Item(name='Hello there'))
# createdRack = DbHelper().create(Rack(name='Rak Hello', type=RackType.STORAGE))
# DbHelper().create(ItemRack(item=createdItem, rack=createdRack))


# itemracks = DbHelper().read(ItemRack)
# itemracks[1].status

for i in DbHelper().read(Item):
    if i.id == 23:
        print('updating id 23')
        i.status = ModelStatus.NOT_ACTIVE
        DbHelper().update(i)
    
