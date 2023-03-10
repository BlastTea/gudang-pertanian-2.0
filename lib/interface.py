import os
from typing import Any

from constants import *
from typing_extensions import Self
from utils import *


class Interface:
    @staticmethod
    def get_choice(*choices: str, title: str = None, back: str = None) -> int:
        while True:
            clrscr()
            if title is not None:
                print('+', '-' * (WIDTH - 2), '+', sep='')
                print('|', title.center(WIDTH - 2), '|', sep='')
                print('+', '-' * (WIDTH - 2), '+', sep='')

            index_length = len(f'{len(choices)}')
            for i, choice in enumerate(choices):
                choice_length = WIDTH - 4 - index_length

                print('| ', f'{i + 1}'.center(index_length), ' | ',
                      choice.ljust(choice_length)[:choice_length - index_length], '|', sep='')
            else:
                if back is None:
                    back = 'Kembali'
                back_length = WIDTH - 4 - index_length
                print('+', '-' * (WIDTH - 2), '+', sep='')
                print('| ', f'0'.center(index_length), ' | ', back.ljust(
                    back_length)[:back_length - index_length], '|', sep='')
                print('+', '-' * (WIDTH - 2), '+', sep='')

            user_input = 0
            try:
                user_input = int(input('Pilihan Anda : '))
            except ValueError:
                input('Masukkan angka yang benar!')
                continue
            else:
                if 0 <= user_input <= len(choices):
                    return user_input
                else:
                    input('Pilihan tidak ada!')
                    continue

    @staticmethod
    def print_table(values: list[dict[str, Any]], flex=True):
        actual_length = 0
        column_lengths: list[dict[str, int]] = [
            {'min_width': 0, 'width': 0}] * len(values[0])

        for value in values:
            for i, key in enumerate(value):
                width = max([column_lengths[i]['width'], len(
                    f'{value[key]}'), len(key)])
                column_lengths[i] = {'min_width': width, 'width': width}

        for column_length in column_lengths:
            actual_length += column_length['width'] + 2

        if WIDTH > actual_length and flex:
            actual_length = 0
            total_of_vast_column = len(column_lengths)
            actual_diff = 0
            new_column_lengths: list[int] = [0] * len(values[0])

            for i, column_length in enumerate(column_lengths):
                new_column_lengths[i] = WIDTH // len(column_lengths) - 1

                if new_column_lengths[i] < column_lengths[i]['width']:
                    diff = column_lengths[i]['width'] - \
                        new_column_lengths[i]
                    new_column_lengths[i] += diff
                    actual_diff += diff + \
                        (2 if column_lengths[i]['min_width']
                         == new_column_lengths[i] else 0)
                    total_of_vast_column -= 1

                # if i == len(column_lengths) - 1 and new_column_lengths[i] > column_lengths[i]['width']:
                #     new_column_lengths[i] -= 1

            def divide_equally(actual_length: int):
                for i in range(len(new_column_lengths)):
                    diff_mod = actual_diff % total_of_vast_column
                    each_width = actual_diff // total_of_vast_column

                    if new_column_lengths[i] > column_lengths[i]['min_width']:
                        new_column_lengths[i] -= each_width
                        if new_column_lengths[i] > column_lengths[i]['min_width']:
                            new_column_lengths[i] -= diff_mod // total_of_vast_column

                    column_lengths[i]['width'] = new_column_lengths[i] + \
                        (2 if column_lengths[i]['width']
                         == new_column_lengths[i] else 0)
                    actual_length += column_lengths[i]['width']

            divide_equally(actual_length)

            if actual_length % 2 == 0:
                actual_diff = 2
            else:
                actual_diff = 1

            divide_equally(actual_length)

        # header
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

        for i in values:
            out = '|'
            for j, key in enumerate(i):
                out += f'{i[key]}'.center(column_lengths[j]['width']) + '|'
            print(out)

        out = '+'
        for column_length in column_lengths:
            out += '-' * column_length['width'] + '+'
        print(out)
