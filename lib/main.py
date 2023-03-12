from enums import *
from interface import *
from models import *
from services.db_helper import DbHelper

while True:
    main_menu_choice = Interface.get_choice(
        'Barang',
        'Rak',
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

            Interface.title('Barang')
            Interface.print_table(
                data,
                TableSettings(
                    fits={'No': Fit.TIGHT},
                    default_alignment=TextAlign.RIGHT,
                    on_empty_value='Barang masih kosong!'
                )
            )

            item_choice = Interface.get_choice(
                'Edit Harga',
                is_clear=False,
                is_with_cover=len(data) == 0
            )
            if item_choice is True:
                continue

            if item_choice == 1:
                clrscr()
                Interface.title('Pilih Barang')
                Interface.print_table(
                    data,
                    TableSettings(
                        fits={'No': Fit.TIGHT},
                        default_alignment=TextAlign.RIGHT
                    )
                )

                number = -1
                try:
                    while number == -1:
                        number = Interface.get_choice(
                            start=0,
                            end=len(data),
                            prompt='No',
                            option_not_found_message='Barang tidak ditemukan!',
                            is_clear=False
                        )
                        if number is ReturnType.SKIP or number is ReturnType.BACK or number is ReturnType.ERROR:
                            number = -1
                        elif number == 0:
                            raise
                except:
                    continue

                item: Item = items[number - 1]

                result = Interface.input_field(
                    [
                        InputFieldDataNumber('Harga', 0)
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
                        True,
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

                # price = -1
                # try:
                #     while price == -1:
                #         clrscr()
                #         Interface.title('Edit Harga')
                #         Interface.print_table(
                #             [
                #                 {'Atribut': key, 'Nilai': value} for key, value in {
                #                     'No': number,
                #                     'Nama': item.name,
                #                     'Tipe': item.type.translate(),
                #                     'Harga': item.price,
                #                     'Expired': item.expired_day
                #                 }.items()
                #             ],
                #             False,
                #             alignments=[
                #                 TextAlign.LEFT,
                #                 TextAlign.RIGHT
                #             ]
                #         )
                #         Interface.updateInfo()
                #         price = Interface.get_capped_input(
                #             0,
                #             prompt='Harga',
                #             on_out_of_bound='Harga tidak boleh kurang dari 0!',
                #             is_can_be_skipped=True
                #         )
                #         if price == -2:
                #             raise
                # except:
                #     continue

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
                data.append(
                    {
                        'No': i + 1,
                        'Nama': rack.name,
                        'Tipe': rack.type.translate()
                    }
                )

            Interface.title('Rak')
            Interface.print_table(
                data,
                fits={'No': Fit.TIGHT},
                default_alignment=TextAlign.RIGHT,
                on_empty_value='Rak masih kosong!'
            )

            rack_choice = Interface.get_choice(
                'Tambah Rak', 'Edit Rak', 'Hapus Rak', is_clear=False, is_with_cover=len(data) == 0)
            if rack_choice == -1:
                continue

            if rack_choice == 1:
                name = ''
                type = ''
                while True:
                    clrscr()
                    Interface.title('Tambah Rak')
                    # Interface.updateInfo()

                    if len(name) == 0:
                        name = input('Nama* : ').strip()
                        if name == '<':
                            break
                        elif name == '-':
                            input('Nama tidak bisa dilewati karena wajib!')
                            continue
                    else:
                        print(f'Nama* : {name}')

                    if isinstance(type, str):
                        Interface.print_table(
                            [
                                {
                                    'a': 1,
                                    'b': 'Tampilan (default)',
                                    'c': 'Menunjukkan bahwa rak ini berada di tampilan depan'
                                },
                                {
                                    'a': 2,
                                    'b': 'Penyimpanan',
                                    'c': 'Menunjukkan bahwa rak ini berada di penyimpanan'
                                }
                            ],
                            alignments=[
                                TextAlign.RIGHT,
                                TextAlign.LEFT,
                                TextAlign.RIGHT
                            ],
                            is_hide_column=True
                        )
                        try:
                            type_input = input('Tipe : ').strip().lower()
                            if type_input == '1':
                                type = RackType.DISPLAY
                            elif type_input == '2':
                                type = RackType.STORAGE
                            elif type_input == '<':
                                break
                            elif type_input != '-':
                                type = RackType.fromindonesianvalue(type_input)
                            else:
                                type = RackType.DISPLAY
                        except:
                            input('Tipe tidak valid!')
                            continue
                    else:
                        print(f'Tipe : {type}')

                if len(name) != 0 and not isinstance(type, str):
                    DbHelper.create(Rack(name=name, type=type))

            elif rack_choice == 0:
                break

    elif main_menu_choice == 0:
        break
