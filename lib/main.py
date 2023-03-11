import csv

from enums import *
from interface import *
from services.db_helper import DbHelper
# items = []
# with open('./databases/items.csv') as file:
#     for i, rows in enumerate(csv.DictReader(file)):
#         # items.append([row[2], row[3], row[4], row[5]])
#         items.append({})
#         for column in rows:
#             if column == 'type':
#                 if rows[column] == 'buah':
#                     items[i]['type'] = 'fruit'
#                 else:
#                     items[i]['type'] = 'vegetable'
#             else:
#                 items[i][column] = rows[column]

# with open('./databases/items.csv', 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=[
#                    'id', 'status', 'name', 'type', 'price', 'expired_day'])
#     writer.writeheader()
#     writer.writerows(items)

Interface.get_choice(
    'Apa?',
    'Tidak',
    'Iya',
    'Hello',
    'world',
    'i',
    'dont',
    'know',
    'yet',
    'please',
    'help',
    title='Selamat Datang'
)

# print(f'hello?: {75 // 4}')

data = []

for i, item in enumerate(DbHelper.read(Item)):
    if i < 10:
        data.append(
            {
                'No': i + 1,
                'Nama': item.name,
                'Harga': item.price,
                'Expired': item.expired_day,
            }
        )
    else:
        break


Interface.print_table(
    data,
    fits={'No': Fit.TIGHT, 'Harga': Fit.TIGHT, 'Expired': Fit.TIGHT},
    default_alignment=TextAlign.RIGHT,
)
