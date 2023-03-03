from constants.constants import *
from datetime import datetime
from enums.rack_type import RackType
from enums.model_status import ModelStatus
from enums.item_type import ItemType
from models.item import Item;
from models.item_rack import ItemRack
from models.model import Model
from models.rack import Rack
from services.db_helper import DbHelper
from utils.utils import *

# with open(ITEMS_PATH) as file:
#     for i, value in enumerate(csv.DictReader(file)):
#         print(f'{i} : {value}')
#         # global_items.append(Item.from_list(row))

a = ItemRack
newInstance = a()
for field in get_fields(newInstance):
    print(f'is subclass of Model ({field}) : {type(getattr(newInstance, field))}')



# for value in DbHelper().read(ItemRack):
#     print(f'I Have {value.item.name} inside {value.rack.name} with value of {value.stock}')

# ItemRack()

# Item()

# DbHelper().create(ItemRack(item=Item(id=1), rack=Rack(id=1), date=datetime.now(), stock=10))

# DbHelper().create(Rack('Rak 1', RackType.STORAGE, ModelStatus.ACTIVE))