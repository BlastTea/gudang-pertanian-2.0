KEY_LAST_ITEM_ID = 'last_item_id'
KEY_LAST_RACK_ID = 'last_rack_id'
KEY_LAST_ITEM_RACK_ID = 'last_item_rack_id'
KEY_LAST_WAREHOUSE_TRANSACTION_ID = 'last_warehouse_transaction_id'
KEY_LAST_TRANSACTION_ID = 'last_transaction_id'
KEY_LAST_ITEM_TRANSACTION_ID = 'last_item_transaction_id'

PATH_ITEM = './databases/items.csv'
PATH_RACK = './databases/racks.csv'
PATH_ITEM_RACK = './databases/item_racks.csv'
PATH_WAREHOUSE_TRANSACTION = './databases/warehouse_transactions.csv'
PATH_TRANSACTION = './databases/transactions.csv'
PATH_ITEM_TRANSACTION = './databases/item_transactions.csv'

# Item
COLUMN_ITEM_ID = 'item_id'
COLUMN_ITEM_NAME = 'name'
COLUMN_ITEM_TYPE = 'type'
COLUMN_ITEM_STATUS = 'status'
COLUMN_ITEM_PRICE = 'price'
COLUMN_ITEM_EXPIRED_DAY = 'expired_day'

# Rack
COLUMN_RACK_ID = 'rack_id'
COLUMN_RACK_NAME = 'name'
COLUMN_RACK_TYPE = 'type'
COLUMN_RACK_STATUS = 'status'

# Item Rack
COLUMN_ITEM_RACK_ID = 'item_rack_id'
# COLUMN_ITEM_ID
# COLUMN_RACK_ID
COLUMN_ITEM_RACK_STOCK = 'stock'
COLUMN_ITEM_RACK_DATE = 'date'

# Warehouse Transaction
COLUMN_WAREHOUSE_TRANSACTION_ID = 'warehouse_transaction_id'
# COLUMN_ITEM_ID
# COLUMN_RACK_ID
COLUMN_WAREHOUSE_TRANSACTION_SENDER_NAME = 'sender_name'
COLUMN_WAREHOUSE_TRANSACTION_TYPE = 'type'
COLUMN_WAREHOUSE_TRANSACTION_AMOUNT = 'amount'
COLUMN_WAREHOUSE_TRANSACTION_DATE = 'date'

# Transaction
COLUMN_TRANSACTION_ID = 'transaction_id'
COLUMN_TRANSACTION_NAME = 'name'
COLUMN_TRANSACTION_STATUS = 'status'
COLUMN_TRANSACTION_DATE = 'date'
COLUMN_TRANSACTION_PAY = 'pay'

# Item Transaction
COLUMN_ITEM_TRANSACTION_ID = 'item_transaction_id'
# COLUMN_TRANSACTION_ID
# COLUMN_ITEM_ID
COLUMN_ITEM_TRANSACTION_AMOUNT = 'amount'

DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'
