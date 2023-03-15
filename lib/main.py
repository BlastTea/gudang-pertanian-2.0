from enums import *
from interface import *
from models import *
from services.db_helper import DbHelper

while True:
    main_menu_choice = Interface.get_choice(
        'Barang',
        'Rak',
        'Lihat semua barang',
        'Penjualan',
        'Laporan',
        title='Gudang Pertanian 2.0',
        back='Exit'
    )
    if main_menu_choice is True:
        continue

    if main_menu_choice == 1:
        while True:
            clrscr()
            items = DbHelper.read(Item)
            data = []

            for i, item in enumerate(items):
                data.append(
                    {
                        'No': i + 1,
                        'Nama': item.name,
                        'Tipe': item.type.translate(),
                        'Harga': item.price,
                        'Expired': item.expired_day
                    }
                )

            Interface.print_table(
                data,
                TABLE_SETTING.copywith(
                    on_empty_value='Barang masih kosong!'
                ),
                'Barang'
            )

            item_choice = Interface.get_choice(
                'Cari Barang',
                'Edit Harga',
                is_clear=False,
                with_top_cover=len(data) == 0
            )
            if item_choice == 1:
                for i in Interface.search_table(
                    data,
                    TABLE_SETTING.copywith(
                        on_empty_value='Barang masih kosong!'
                    ),
                    'Cari Barang',
                    not_found_message='Barang tidak ditemukan!'
                ):
                    pass
            elif item_choice == 2:
                number = Interface.search_single_table(
                    data,
                    title='Pilih Barang',
                    not_found_message='Barang tidak ditemukan!'
                )

                if number is ReturnType.BACK:
                    continue

                item: Item = items[number - 1]

                result = Interface.input_field(
                    [
                        InputFieldDataNumber('Harga', 0, item.price)
                    ],
                    [
                        {'Atribut': key, 'Nilai': value} for key, value in {
                            'No': number,
                            'Nama': item.name,
                            'Tipe': item.type.translate(),
                            'Harga': item.price,
                            'Expired': item.expired_day
                        }.items()
                    ],
                    TableSettings(
                        alignments=[
                            TextAlign.LEFT,
                            TextAlign.RIGHT
                        ],
                        is_hide_column=True
                    ),
                    'Edit Harga'
                )
                if result is ReturnType.BACK:
                    continue

                item.price = result[0].result
                DbHelper.update(item)

            elif item_choice == 0:
                break
    elif main_menu_choice == 2:
        while True:
            clrscr()
            racks = DbHelper.read(Rack)
            data = []

            for i, rack in enumerate(racks):
                if rack.status is ModelStatus.ACTIVE:
                    data.append(
                        {
                            'No': i + 1,
                            'Nama': rack.name,
                            'Tipe': rack.type.translate()
                        }
                    )

            Interface.print_table(
                data,
                TABLE_SETTING.copywith(
                    on_empty_value='Rak masih kosong!'
                ),
                'Rak'
            )

            rack_choice = Interface.get_choice(
                'Cari Rak',
                'Tambah Rak',
                'Edit Rak',
                'Hapus Rak',
                is_clear=False,
                with_top_cover=len(data) == 0
            )

            if rack_choice == 1:
                for i in Interface.search_table(
                    data,
                    TABLE_SETTING.copywith(
                        on_empty_value='Rak masih kosong!'
                    ),
                    'Cari Rak',
                    not_found_message='Rak tidak ditemukan!'
                ):
                    pass
            if rack_choice == 2:
                result = Interface.input_field(
                    [
                        InputFieldData('Nama', str, is_required=True),
                        InputFieldData('Tipe', RackType, RackType.DISPLAY),
                    ],
                    title='Tambah Rak'
                )

                if result is not ReturnType.BACK:
                    name = result[0].result
                    type = result[1].result
                    DbHelper.create(Rack(name=name, type=type))

            elif rack_choice == 3:
                number = Interface.search_single_table(
                    data,
                    title='Pilih Rak',
                    not_found_message='Rak tidak ditemukan!'
                )

                if number is ReturnType.BACK:
                    continue

                rack: Rack = racks[number - 1]

                result = Interface.input_field(
                    [
                        InputFieldData('Nama', str, rack.name),
                        InputFieldData(
                            'Tipe',
                            RackType,
                            rack.type,
                            ignore_default_enum_text=True
                        )
                    ],
                    [
                        {'Atribut': key, 'Nilai': value} for key, value in {
                            'No': number,
                            'Nama': rack.name,
                            'Tipe': rack.type.translate()
                        }.items()
                    ],
                    TableSettings(
                        alignments=[
                            TextAlign.LEFT,
                            TextAlign.RIGHT
                        ],
                        is_hide_column=True
                    ),
                    'Edit Rak'
                )

                if result is ReturnType.BACK:
                    continue

                rack.name = result[0].result
                rack.type = result[1].result
                DbHelper.update(rack)

            elif rack_choice == 4:
                number = Interface.search_single_table(
                    data,
                    title='Pilih Rak',
                    not_found_message='Rak tidak ditemukan'
                )

                if number is ReturnType.BACK:
                    continue

                rack: Rack = racks[number - 1]

                result = Interface.delete_row(
                    [
                        {'Atribut': key, 'Nilai': value} for key, value in {
                            'No': number,
                            'Nama': rack.name,
                            'Tipe': rack.type.translate()
                        }.items()
                    ],
                    TableSettings(
                        alignments=[
                            TextAlign.LEFT,
                            TextAlign.RIGHT
                        ],
                        is_hide_column=True
                    ),
                    'Hapus Rak',
                    f'Hapus {rack.name}?'
                )

                if result:
                    DbHelper.delete(rack)

            elif rack_choice == 0:
                break

    elif main_menu_choice == 3:
        while True:
            clrscr()
            racks = DbHelper.read(Rack)
            rack_data = []

            for i, rack in enumerate(racks):
                if rack.status is ModelStatus.ACTIVE:
                    rack_data.append(
                        {
                            'No': i + 1,
                            'Nama': rack.name,
                            'Tipe': rack.type.translate()
                        }
                    )

            items = DbHelper.read(Item)
            item_data = []

            for i, item in enumerate(items):
                if item.status is ModelStatus.ACTIVE:
                    item_data.append(
                        {
                            'No': i + 1,
                            'Nama': item.name,
                            'Tipe': item.type.translate(),
                            'Harga': item.price,
                            'Expired': item.expired_day
                        }
                    )

            rack_number = Interface.search_single_table(
                rack_data,
                title='Pilih Rak',
                not_found_message='Rak tidak ditemukan'
            )

            if rack_number is ReturnType.BACK:
                break

            choosen_rack: Rack = racks[rack_number - 1]

            while True:
                clrscr()
                warehouse_transactions = DbHelper.read(WarehouseTransaction)
                warehouse_data = []

                for i, warehouse in enumerate(warehouse_transactions):
                    if warehouse.status is ModelStatus.ACTIVE and warehouse.type is WarehouseTransactionType.IN and warehouse.rack.id is choosen_rack.id:
                        remaining_time = ''
                        day, hour, minute, second = warehouse.duration()
                        if day > 0:
                            remaining_time = f'{day} Hari, {hour} Jam'
                        elif hour > 0:
                            remaining_time = f'{hour} Jam, {minute} Menit'
                        elif minute > 0:
                            remaining_time = f'{minute} Menit, {second} Detik'
                        elif second > 0:
                            remaining_time = f'{second} Detik'
                        else:
                            remaining_time = '-'

                        warehouse_transactions.append(
                            {
                                'No': i + 1,
                                'Nama': warehouse.item.name,
                                'Tipe': warehouse.item.type.translate(),
                                'Harga': warehouse.item.price,
                                'Stok': warehouse.stock,
                                'Sisa Waktu': remaining_time,
                                'metadata': {
                                    'warehouse_transaction_id': warehouse.id,
                                    'remaining_second': warehouse.duration()[3]
                                }
                            }
                        )
                Interface.print_table(
                    warehouse_data,
                    TABLE_SETTING.copywith(
                        on_empty_value='Rak masih kosong!'
                    ),
                    choosen_rack.name
                )
                item_rack_choice = Interface.get_choice(
                    'Cari Barang',
                    'Tambah Barang',
                    'Pindah Barang',
                    'Hapus Barang',
                    is_clear=False,
                    with_top_cover=len(warehouse_data) == 0
                )

                if item_rack_choice == 1:
                    for i in Interface.search_table(
                        warehouse_data,
                        title='Cari Barang',
                        not_found_message='Barang tidak ditemukan!'
                    ):
                        pass

                elif item_rack_choice == 2:
                    new_data = WarehouseTransaction()

                    item_number = Interface.search_single_table(
                        item_data,
                        title='Pilih Barang',
                        not_found_message='Barang tidak ditemukan!'
                    )

                    if item_number is ReturnType.BACK:
                        continue
                    
                    choosen_item : Item = items[item_number - 1]

                    input_result = Interface.input_field(
                        [
                            InputFieldData('Nama Pengirim', str, '-'),
                            InputFieldDataNumber('Jumlah', 1, is_required=True)
                        ],
                        [
                            {'Atribut': key, 'Nilai': value} for key, value in {
                                'No Rak': rack_number,
                                'Nama Rak': choosen_rack.name,
                                'Tipe Rak': choosen_rack.type.translate(),
                                'No Barang': item_number,
                                'Nama Barang': choosen_item.name,
                                'Tipe Barang': choosen_item.type.translate(),
                                'Harga Barang': choosen_item.price,
                                'Expired': choosen_item.expired_day,
                            }.items()
                        ],
                        title='Tambah Rak'
                    )

                    new_data.rack = choosen_rack
                    new_data.item = choosen_item
                    new_data.sender_name = input_result[0].result
                    new_data.amount = input_result[1].result
                    new_data.stock = input_result[1].result
                    DbHelper.create(new_data)

    elif main_menu_choice == 0:
        break
