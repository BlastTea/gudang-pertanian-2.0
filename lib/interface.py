import math

from constants import *
from enums import *
from models import *
from typing import Any, TypeVar, Type
from utils import *


class TableSettings:
    def __init__(
        self,
        flex: bool = True,
        alignments: dict[str, TextAlign] | list[TextAlign] = None,
        fits: dict[str, Fit] | list[Fit] = None,
        default_alignment: TextAlign = TextAlign.CENTER,
        default_fit: Fit = Fit.EXPAND,
        on_empty_value: str = 'Tabel masih kosong!',
        is_hide_column: bool = False
    ):
        self.flex = flex
        self.alignments = alignments
        self.fits = fits
        self.default_alignment = default_alignment
        self.default_fit = default_fit
        self.on_empty_value = on_empty_value
        self.is_hide_column = is_hide_column


class InputFieldData:
    def __init__(
        self,
        field: str,
        t: Type[int | float | str | datetime],
        is_required: bool = False,
    ):
        assert t is int or t is float or t is str or t is datetime
        self.field = field
        self.t = t
        self.is_required = is_required


class InputFieldDataNumber(InputFieldData):
    def __init__(
            self,
            field: str,
            start: int | float = float('-inf'),
            end: int | float = float('inf'),
            is_required: bool = False
    ):
        super().__init__(field, int, is_required)
        self.start = start
        self.end = end


class InputFieldDataResult(InputFieldData):
    def __init__(
            self,
            field: str,
            t: Type[int | float | str | datetime],
            result: int | float | str | datetime | None,
            is_required: bool = False
    ):
        super().__init__(field, t, is_required)
        self.result = result

    @classmethod
    def addresult(cls, updatedata: InputFieldData, result: int | float | str | datetime | None):
        return cls(updatedata.field, updatedata.t, result, updatedata.is_required)


class Interface:
    @staticmethod
    def title(title: str):
        print('+', '-' * (WIDTH - 2), '+', sep='')
        print('|', title.center(WIDTH - 2), '|', sep='')
        print('+', '-' * (WIDTH - 2), '+', sep='')

    @staticmethod
    def get_number(t: Type[int | float], prompt: str = 'Pilihan Anda', value: str = None, is_can_go_back: bool = False):
        user_input = 0
        try:
            if value is not None:
                user_input = t(value)
            else:
                user_input = input(f'{prompt} : ').strip()
                if user_input == '<' and is_can_go_back:
                    return ReturnType.BACK
                user_input = t(user_input)
        except ValueError:
            input('Angka tidak valid!')
            return ReturnType.ERROR
        else:
            return user_input

    @staticmethod
    def get_str(prompt: str = 'Pilihan Anda', on_empty_str: str = 'Pilihan tidak boleh kosong!'):
        user_input = ''
        while user_input == '':
            user_input = input(f'{prompt} : ').strip()
            if user_input == '':
                input(on_empty_str)
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
        on_out_of_bound: str = 'Pilihan tidak ada!',
        is_can_be_skipped: bool = False
    ):
        user_input = ''
        if is_can_be_skipped:
            user_input = Interface.get_str(prompt)
            if user_input == '-':
                return ReturnType.SKIP

            user_input = Interface.get_number(type(start), prompt, user_input)
        else:
            user_input = Interface.get_number(type(start), prompt)

        if user_input is ReturnType.BACK:
            return user_input

        if start <= user_input <= end:
            return user_input
        else:
            if user_input is ReturnType.ERROR:
                input(on_out_of_bound)
            return ReturnType.ERROR

    @staticmethod
    def get_choice(
        *choices: str,
        start: int | float = None,
        end: int | float = None,
        title: str = None,
        back: str = None,
        prompt: str = 'Pilihan Anda',
        option_not_found_message: str = 'Pilihan tidak ada!',
        is_clear: bool = True,
        is_with_cover: bool = False
    ):
        if is_clear:
            clrscr()
        if title is not None:
            Interface.title(title)
        elif is_with_cover:
            print('+', '-' * (WIDTH - 2), '+', sep='')

        index_length = len(f'{len(choices)}')
        for i, choice in enumerate(choices):
            choice_length = WIDTH - 6 - index_length

            print('| ', f'{i + 1}'.center(index_length), ' | ',
                  choice.ljust(choice_length), '|', sep='')
        else:
            if back is None:
                back = 'Kembali'
            back_length = WIDTH - 6 - index_length
            print('+', '-' * (WIDTH - 2), '+', sep='')
            print('| ', f'0'.center(index_length), ' | ', back.ljust(
                back_length), '|', sep='')
            print('+', '-' * (WIDTH - 2), '+', sep='')

        return Interface.get_capped_input(0 if start is None else start, len(choices) if end is None else end, prompt, option_not_found_message)

    @staticmethod
    def print_table(
        values: list[dict[str, Any]],
        setting: TableSettings
    ):
        if len(values) == 0:
            print('|' + ' ' * (WIDTH - 2) + '|')
            print('| ' + setting.on_empty_value.center(WIDTH - 4) + ' |')
            print('|' + ' ' * (WIDTH - 2) + '|')
            return

        if isinstance(setting.alignments, list) and len(values[0]) != len(setting.alignments):
            raise AssertionError(
                'Length of alignments must be the same as values')
        if isinstance(setting.fits, list) and len(values[0]) != len(setting.fits):
            raise AssertionError('Length of fits must be the same as values')

        actual_length = 1
        column_lengths: list[dict[str, Any]] = [
            {
                'min_width': 0,
                'width': 0,
                'alignment': setting.default_alignment,
                'fit': setting.default_fit
            }
        ] * len(values[0])

        for value in values:
            for i, key in enumerate(value):
                width = max([column_lengths[i]['width'], len(
                    f'{value[key]}'), len(key)])
                column_lengths[i] = {
                    'min_width': width,
                    'width': width,
                    'alignment': setting.default_alignment,
                    'fit': setting.default_fit
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
            new_column_lengths: list[int] = [0] * len(values[0])

            tight_fits = [
                fit for fit in column_lengths if fit['fit'] == Fit.TIGHT]
            total_of_tight_column = len(tight_fits)
            total_of_tight_width = total_of_tight_column

            actual_length = 1
            actual_diff = 1 if total_of_tight_column % 2 != 0 else 0

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
            for i in [a for i, a in enumerate(new_column_lengths) if column_lengths[i]['width'] == column_lengths[i]['min_width'] and column_lengths[i]['fit'] == Fit.EXPAND]:
                actual_diff += i - \
                    WIDTH // (len(column_lengths) - total_of_tight_column)

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
    def input_field(data: list[InputFieldData], table: list[dict[str, Any]] = None, table_setting: TableSettings = TableSettings(), title: str = None):
        input_results: list[InputFieldDataResult] = []
        contain_required_field, can_be_skipped = False, False

        for input_field_data in data:
            contain_required_field = input_field_data.is_required and not contain_required_field

        can_be_skipped = len([d for d in data if d.is_required]) == 0

        is_not_going_back = True
        while is_not_going_back:
            try:
                clrscr()
                if title is not None:
                    Interface.title(title)

                if table is not None:
                    Interface.print_table(table, table_setting)

                if contain_required_field:
                    print('|', '* wajib (tidak bisa dilewati)'.ljust(WIDTH - 4), '|')
                if can_be_skipped:
                    print('|', '- untuk melewati'.ljust(WIDTH - 4), '|')
                print('|', '< untuk batal'.ljust(WIDTH - 4), '|')
                print('+', '-' * (WIDTH - 2), '+', sep='')

                for i, input_field_data in enumerate(data):
                    if isinstance(input_field_data, InputFieldDataNumber):
                        result = Interface.get_capped_input(
                            input_field_data.start,
                            input_field_data.end,
                            input_field_data.field,
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
                            result = None
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
                                input_field_data.field)

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
                        result = '-'
                        while result is '-':
                            result = Interface.get_str(
                                input_field_data.field, input_field_data.field + ' tidak boleh kosong!')

                            if result is '<':
                                return ReturnType.BACK
                            if result is '-' and input_field_data.is_required is not True:
                                result = None
                            else:
                                input(input_field_data +
                                      '  tidak bisa dilewati karena wajib!')

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
