import math

from constants import *
from copy import copy
from enums import *
from models import *
from typing import Any, Type
from utils import *


class TableSettings:
    def __init__(
        self,
        flex: bool = True,
        alignments: dict[str, TextAlign] | list[TextAlign] = None,
        fits: dict[str, Fit] | list[Fit] = None,
        alignment: TextAlign = TextAlign.CENTER,
        fit: Fit = Fit.EXPAND,
        on_empty_value: str = 'Tabel masih kosong!',
        is_hide_column: bool = False,
    ):
        self.flex = flex
        self.alignments = alignments
        self.fits = fits
        self.alignment = alignment
        self.fit = fit
        self.on_empty_value = on_empty_value
        self.is_hide_column = is_hide_column

    def copywith(
        self,
        flex: bool = None,
        alignments: dict[str, TextAlign] | list[TextAlign] = None,
        fits: dict[str, Fit] | list[Fit] = None,
        alignment: TextAlign = None,
        fit: Fit = None,
        on_empty_value: str = None,
        is_hide_column: bool = None,
    ):
        self.flex = flex if flex is not None else self.flex
        self.alignments = alignments if alignments is not None else self.alignments
        self.fits = fits if fits is not None else self.fits
        self.alignment = alignment if alignment is not None else self.alignment
        self.fit = fit if fit is not None else self.fit
        self.on_empty_value = on_empty_value if on_empty_value is not None else self.on_empty_value
        self.is_hide_column = is_hide_column if is_hide_column is not None else self.is_hide_column
        return copy(self)


TABLE_SETTING = TableSettings(
    fits={'No': Fit.TIGHT},
    alignment=TextAlign.RIGHT,
)


class InputFieldData:
    def __init__(
        self,
        field: str,
        t: Type[int | float | str | datetime | ModelEnum],
        default=None,
        is_required: bool = False,
        ignore_default_enum_text=False,
    ):
        assert t is int or t is float or t is str or t is datetime or issubclass(
            t, ModelEnum)
        assert default is None or (default is not None and t is type(default))

        self.field = field
        self.t = t
        self.default = default
        self.is_required = is_required
        self.ignore_default_enum_text = ignore_default_enum_text


class InputFieldDataNumber(InputFieldData):
    def __init__(
            self,
            field: str,
            start: int | float = float('-inf'),
            end: int | float = float('inf'),
            default=None,
            is_required: bool = False
    ):
        super().__init__(field, int, default, is_required)
        self.start = start
        self.end = end


class InputFieldDataResult(InputFieldData):
    def __init__(
            self,
            field: str,
            t: Type[int | float | str | datetime | ModelEnum],
            result: int | float | str | datetime | ModelEnum | None,
            is_required: bool = False
    ):
        assert t is type(result)
        super().__init__(field, t, is_required=is_required)
        self.result = result

    @classmethod
    def addresult(cls, updatedata: InputFieldData, result: int | float | str | datetime | ModelEnum | None):
        return cls(updatedata.field, updatedata.t, result, updatedata.is_required)


class Interface:
    @staticmethod
    def title_cover():
        print('+', '-' * (WIDTH - 2), '+', sep='')

    @staticmethod
    def title(title: str, with_bottom_cover: bool = True):
        Interface.title_cover()
        print('|', title.center(WIDTH - 2), '|', sep='')
        if with_bottom_cover:
            Interface.title_cover()

    @staticmethod
    def footer(
        index_length: int = None,
        with_top_cover: bool = True,
        prefix: str = '0',
        suffix: str = 'Kembali'
    ):
        index_length = index_length if index_length is not None else len(
            prefix)
        back_length = WIDTH - 6 - index_length
        if with_top_cover:
            Interface.title_cover()
        print('| ', f'{prefix}'.center(index_length), ' | ', suffix.ljust(
            back_length), '|', sep='')
        Interface.title_cover()

    @staticmethod
    def get_number(t: Type[int | float], prompt: str = 'Pilihan Anda', value: str = None, can_go_back: bool = False):
        user_input = 0
        try:
            if value is not None:
                user_input = t(value)
            else:
                user_input = input(f'{prompt} : ').strip()
                if user_input == '<' and can_go_back:
                    return ReturnType.BACK
                user_input = t(user_input)
        except ValueError:
            input('Angka tidak valid!')
            return ReturnType.ERROR
        else:
            return user_input

    @staticmethod
    def get_str(prompt: str = 'Pilihan Anda', empty_str_message: str = 'Pilihan tidak boleh kosong!', ignore_empty_str=False):
        user_input = ''
        while user_input == '':
            user_input = input(f'{prompt} : ').strip()
            if ignore_empty_str:
                return user_input
            if user_input == '':
                input(empty_str_message)
        return user_input

    @staticmethod
    def get_datetime(prompt: str = 'Tanggal', value: str = None):
        user_input = ''
        try:
            if value is not None:
                user_input = datetime.strptime(value, DATETIME_FORMAT)
            else:
                print('format: day-month-year Hour:Minute:Second')
                print('- untuk tanggal sekarang')
                user_input = input(f'{prompt} : ').strip()
                if user_input == '-':
                    return datetime.now()
                if user_input == '<':
                    return ReturnType.BACK
                user_input = datetime.strptime(user_input, DATETIME_FORMAT)
        except:
            input('Format tanggal tidak valid!')
            return ReturnType.ERROR
        else:
            return user_input

    @staticmethod
    def get_capped_input(
        start: int | float,
        end: int | float = float('inf'),
        prompt: str = 'Pilihan Anda',
        out_of_bound_message: str = 'Pilihan tidak ada!',
        can_be_skipped: bool = False
    ):
        user_input = ''
        if can_be_skipped:
            user_input = Interface.get_str(prompt)
            if user_input == '-':
                return ReturnType.SKIP
            if user_input == '<':
                return ReturnType.BACK

            user_input = Interface.get_number(type(start), prompt, user_input)
        else:
            user_input = Interface.get_number(type(start), prompt)

        if user_input is ReturnType.BACK or user_input is ReturnType.ERROR:
            return user_input

        if start <= user_input <= end:
            return user_input
        else:
            input(out_of_bound_message)
            return ReturnType.ERROR

    @staticmethod
    def get_choice(
        *choices: str,
        start: int | float = None,
        end: int | float = None,
        title: str = None,
        back: str = 'Kembali',
        prompt: str = 'Pilihan Anda',
        not_found_message: str = 'Pilihan tidak ada!',
        is_clear: bool = True,
        with_top_cover: bool = False,
        with_back_top_cover=True,
        index_length: int = None
    ):
        if is_clear:
            clrscr()
        if title is not None:
            Interface.title(title)
        elif with_top_cover:
            Interface.title_cover()

        index_length = len(
            f'{len(choices)}') if index_length is None else index_length
        for i, choice in enumerate(choices):
            choice_length = WIDTH - 6 - index_length

            print('| ', f'{i + 1}'.center(index_length), ' | ',
                  choice.ljust(choice_length), '|', sep='')
        else:
            Interface.footer(
                index_length,
                with_back_top_cover,
                suffix=back,
            )

        return Interface.get_capped_input(0 if start is None else start, len(choices) if end is None else end, prompt, not_found_message)

    @staticmethod
    def print_table(
        values: list[dict[str, Any]],
        setting: TableSettings = TABLE_SETTING,
        title: str = None
    ):

        if title is not None:
            Interface.title(title, len(values) == 0)

        if len(values) == 0:
            print('|' + ' ' * (WIDTH - 2) + '|')
            print('| ' + setting.on_empty_value.center(WIDTH - 4) + ' |')
            print('|' + ' ' * (WIDTH - 2) + '|')
            return

        contain_metadata = values[0].get('metadata') is not None
        values_length = (len(values[0]) - (1 if contain_metadata else 0))

        if isinstance(setting.alignments, list) and values_length != len(setting.alignments):
            raise AssertionError(
                'Length of alignments must be the same as values')
        if isinstance(setting.fits, list) and values_length != len(setting.fits):
            raise AssertionError('Length of fits must be the same as values')

        actual_length = 1
        column_lengths: list[dict[str, Any]] = [
            {
                'min_width': 0,
                'width': 0,
                'alignment': setting.alignment,
                'fit': setting.fit
            }
        ] * values_length

        for value in values:
            for i, key in enumerate(value):
                if key is 'metadata':
                    continue
                width = max([column_lengths[i]['width'], len(
                    f'{value[key]}'), len(key)])
                column_lengths[i] = {
                    'min_width': width,
                    'width': width,
                    'alignment': setting.alignment,
                    'fit': setting.fit
                }

        for i, column_length in enumerate(column_lengths):
            column_lengths[i]['min_width'] += 2
            column_lengths[i]['width'] += 2

            if isinstance(setting.alignments, list):
                column_lengths[i]['alignment'] = setting.alignments[i]
            if isinstance(setting.alignments, dict):
                if setting.alignments is not None:
                    if setting.alignments.get(list(values[0].keys())[i]):
                        column_lengths[i]['alignment'] = setting.alignments[list(values[0].keys())[
                            i]]

            if isinstance(setting.fits, list):
                column_lengths[i]['fit'] = setting.fits[i]
            if isinstance(setting.fits, dict):
                if setting.fits is not None:
                    if setting.fits.get(list(values[0].keys())[i]):
                        column_lengths[i]['fit'] = setting.fits[list(
                            values[0].keys())[i]]

            actual_length += column_length['width'] + 1

        if WIDTH > actual_length and setting.flex:
            total_of_vast_column = len(column_lengths)
            new_column_lengths: list[int] = [0] * values_length

            tight_fits = [
                fit for fit in column_lengths if fit['fit'] == Fit.TIGHT]
            total_of_tight_column = len(tight_fits)
            total_of_tight_width = total_of_tight_column

            actual_length = 1
            actual_diff = 1 if total_of_tight_column > 1 and total_of_tight_column % 2 == 0 else 0

            for i in tight_fits:
                total_of_tight_width += i['width']

            actual_diff += total_of_tight_width

            for i, column_length in enumerate(column_lengths):

                if column_lengths[i]['fit'] == Fit.TIGHT:
                    new_column_lengths[i] = column_lengths[i]['width']
                    total_of_vast_column -= 1
                else:
                    new_column_lengths[i] = WIDTH // (
                        len(column_lengths) - total_of_tight_column)

                    if new_column_lengths[i] <= column_lengths[i]['width']:
                        diff = column_lengths[i]['width'] - \
                            new_column_lengths[i]
                        new_column_lengths[i] += diff
                        actual_diff += diff
                        total_of_vast_column -= 1
                actual_length += new_column_lengths[i] + 1

            actual_diff += total_of_vast_column
            if total_of_tight_column > 0:
                for i in [a for i, a in enumerate(new_column_lengths) if column_lengths[i]['width'] == column_lengths[i]['min_width'] and column_lengths[i]['fit'] == Fit.EXPAND]:
                    actual_diff += i - \
                        WIDTH // (len(column_lengths) - total_of_tight_column)
            else:
                actual_diff = actual_length - WIDTH

            diff_mod = actual_diff % total_of_vast_column
            for i in range(len(new_column_lengths)):
                each_width = actual_diff // total_of_vast_column

                if new_column_lengths[i] > column_lengths[i]['min_width'] and actual_length > WIDTH:
                    new_column_lengths[i] -= each_width
                    actual_length -= each_width
                    if new_column_lengths[i] > column_lengths[i]['min_width']:
                        diff_width = diff_mod // total_of_vast_column
                        if diff_width == 0 and diff_mod > 0:
                            new_column_lengths[i] -= 1
                            actual_length -= 1
                            diff_mod -= 1
                        else:
                            new_column_lengths[i] -= diff_width
                            actual_length -= diff_width

                column_lengths[i]['width'] = new_column_lengths[i]

        if not setting.is_hide_column:
            # column
            out = '+'
            for column_length in column_lengths:
                out += '-' * column_length['width'] + '+'
            print(out)

            out = '|'
            for i, key in enumerate(values[0]):
                if key is 'metadata':
                    continue
                out += key.center(column_lengths[i]['width']) + '|'
            print(out)

        out = '+'
        for column_length in column_lengths:
            out += '-' * column_length['width'] + '+'
        print(out)

        # body
        for i in values:
            out = '|'
            for j, key in enumerate(i):
                if key is 'metadata':
                    continue
                if column_lengths[j]['alignment'] == TextAlign.LEFT:
                    out += f' {i[key]}'.ljust(column_lengths[j]['width']) + '|'
                elif column_lengths[j]['alignment'] == TextAlign.CENTER:
                    out += f'{i[key]}'.center(column_lengths[j]['width']) + '|'
                else:
                    out += f'{i[key]} '.rjust(column_lengths[j]['width']) + '|'
            print(out)

        out = '+'
        for column_length in column_lengths:
            out += '-' * column_length['width'] + '+'
        print(out)

    @staticmethod
    def input_field(
        data: list[InputFieldData],
        table: list[dict[str, Any]] = None,
        setting: TableSettings = TABLE_SETTING,
        title: str = None
    ):
        input_results: list[InputFieldDataResult] = []
        contain_required_field = False

        for input_field_data in data:
            contain_required_field = input_field_data.is_required and not contain_required_field

        is_not_going_back = True
        while is_not_going_back:
            try:
                clrscr()
                if title is not None:
                    Interface.title(title, False)

                if table is not None:
                    Interface.print_table(table, setting)

                if contain_required_field:
                    print('|', '* wajib (tidak bisa dilewati)'.ljust(WIDTH - 4), '|')
                else:
                    print('|', '- untuk melewati'.ljust(WIDTH - 4), '|')
                print('|', '< untuk batal'.ljust(WIDTH - 4), '|')
                Interface.title_cover()

                for i, input_field_data in enumerate(data):
                    if i > 0:
                        print()

                    if len(input_results) == i + 1 and input_results[i].result is not None:
                        print(input_field_data.field, ':',
                              input_results[i].result)
                        continue

                    if isinstance(input_field_data, InputFieldDataNumber):

                        result = Interface.get_capped_input(
                            input_field_data.start,
                            input_field_data.end,
                            input_field_data.field +
                            ('*' if input_field_data.is_required else ''),
                            input_field_data.field +
                            f' tidak boleh' +
                            (f' kurang dari {input_field_data.start}' if not math.isinf(input_field_data.start) else '') +
                            (' dan' if not math.isinf(input_field_data.start) and not math.isinf(input_field_data.end) else '') +
                            (f' lebih dari {input_field_data.end}' if not math.isinf(
                                input_field_data.end) else ''),
                            not input_field_data.is_required
                        )

                        if result is ReturnType.BACK:
                            return result
                        if result is ReturnType.SKIP:
                            result = input_field_data.default
                        elif result is ReturnType.ERROR:
                            raise

                        input_results.append(
                            InputFieldDataResult.addresult(
                                input_field_data,
                                result
                            )
                        )
                    elif issubclass(input_field_data.t, datetime):
                        result = ''
                        while result == '':
                            result = Interface.get_datetime(
                                input_field_data.field + ('*' if input_field_data.is_required else ''))

                            if result is ReturnType.BACK:
                                return result
                            elif result is ReturnType.ERROR:
                                raise

                        input_results.append(
                            InputFieldDataResult.addresult(
                                input_field_data,
                                result,
                            )
                        )
                    else:
                        if issubclass(input_field_data.t, ModelEnum):
                            Interface.print_table(
                                [{'Tipe': value.translate() + (' (Default)' if input_field_data.default.translate() == value.translate() and not input_field_data.ignore_default_enum_text else ''), 'Deskripsi': value.description()}
                                 for key, value in input_field_data.t.__members__.items()],
                                TableSettings(
                                    alignments=[
                                        TextAlign.LEFT,
                                        TextAlign.RIGHT,
                                    ]
                                )
                            )

                        result = '-'
                        while result is '-':
                            result = Interface.get_str(
                                input_field_data.field + ('*' if input_field_data.is_required else ''), input_field_data.field + ' tidak boleh kosong!', True)

                            if result == '':
                                raise
                            elif result is '<':
                                return ReturnType.BACK
                            elif result is '-' and input_field_data.is_required is not True:
                                result = input_field_data.default
                            elif result is '-' and input_field_data.is_required:
                                input(input_field_data.field +
                                      ' tidak bisa dilewati karena wajib!')
                                raise
                            elif issubclass(input_field_data.t, ModelEnum):
                                try:
                                    result = input_field_data.t.fromindonesianvalue(
                                        result.lower())
                                except:
                                    input('Tipe tidak valid!')
                                    raise

                        input_results.append(
                            InputFieldDataResult.addresult(
                                input_field_data,
                                result
                            )
                        )

                    if i == len(data) - 1:
                        is_not_going_back = False
            except:
                pass

        return input_results

    @staticmethod
    def search_table(
        table: list[dict[str, Any]],
        setting: TableSettings = TABLE_SETTING,
        title: str = None,
        prompt: str = 'Cari',
        not_found_message: str = 'Data tidak ditemukan!'
    ):
        default_on_empty_value = setting.on_empty_value
        query = None
        while True:
            clrscr()
            filtered_data: list[dict[str, Any]] = []
            added_numbers = []
            if query is not None:
                splitted_querys = [new_query.strip().lower()
                                   for new_query in query.split(',')]
                for data in table:
                    qualified = [False] * len(data)
                    for i, value in enumerate(data.values()):
                        value_str = str(value).lower()
                        for query_str in splitted_querys:
                            qualified[i] = query_str in value_str
                            if qualified[i]:
                                break
                    if len([qual for qual in qualified if qual]) >= len(splitted_querys) and data['No'] not in added_numbers:
                        filtered_data.append(data)
                        added_numbers.append(data['No'])

            if query is not None and len(filtered_data) == 0:
                setting.on_empty_value = not_found_message
            else:
                setting.on_empty_value = default_on_empty_value

            Interface.print_table(
                filtered_data if query is not None else table,
                setting,
                title
            )

            if query is not None:
                Interface.footer(
                    with_top_cover=len(filtered_data) == 0 or len(table) == 0,
                    prefix='hasil dari',
                    suffix=query
                )
            Interface.footer(
                with_top_cover=False,
            )

            query = Interface.get_str(prompt, ignore_empty_str=True)
            if query == '0':
                break
            yield filtered_data

    @staticmethod
    def search_single_table(
        data: list[dict[str, Any]],
        setting: TableSettings = TABLE_SETTING,
        title: str = None,
        prompt: str = 'No',
        not_found_message: str = 'No tidak ditemukan!',
    ):
        number = ''
        while number == '':
            clrscr()
            Interface.print_table(
                data,
                setting,
                title
            )

            number = Interface.get_choice(
                start=0,
                end=len(data),
                prompt=prompt,
                not_found_message=not_found_message,
                is_clear=False,
                with_back_top_cover=False
            )
            if number is ReturnType.SKIP or number is ReturnType.BACK or number is ReturnType.ERROR:
                number = ''
            elif number == 0:
                return ReturnType.BACK
            else:
                break
        return number

    @staticmethod
    def delete_row(
        table: list[dict[str, Any]] = None,
        setting: TableSettings = TABLE_SETTING,
        title: str = None,
        prompt: str = 'Hapus?'
    ):
        answer = ['y', 'yes', 'n', 'no']
        result = ''
        while result not in answer:
            clrscr()
            if title is not None:
                Interface.title(title, False)

            if table is not None:
                Interface.print_table(table, setting)

            result = Interface.get_str(
                prompt + ' (y/n)', 'Tidak boleh kosong!').lower()

            if result not in answer:
                input('Input tidak valid!')
        return result is 'y' or result is 'yes'
