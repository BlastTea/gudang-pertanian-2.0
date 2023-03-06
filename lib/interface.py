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
        actual_length = 1
        column_lengths = [0] * len(values[0])

        for value in values:
            for j, key in enumerate(value):
                value_len = len(f'{value[key]}')
                column_lengths[j] = max(
                    [column_lengths[j], value_len, len(key)])

        for column_length in column_lengths:
            actual_length += column_length + 1

        # if WIDTH > actual_length:
        #     rest_width = WIDTH - actual_length
        #     while rest_width > 0:
        #         each_width = rest_width // len(column_lengths)

        #         if each_width == 0:
        #             each_width = 1

        #         for i in range(len(column_lengths)):
        #             column_lengths[i] += each_width
        #             rest_width -= each_width
        #             if rest_width <= 0:
        #                 break

        if WIDTH > actual_length and flex:
            for i in range(len(column_lengths)):
                column_lengths[i] = WIDTH // len(column_lengths) - 1
                if i == len(column_lengths) - 1:
                    column_lengths[i] -= 1

        # header
        out = '+'
        for i in column_lengths:
            out += '-' * i + '+'
        print(out)

        out = '|'
        for i, key in enumerate(values[0]):
            out += key.center(column_lengths[i]) + '|'
        print(out)

        out = '+'
        for i in column_lengths:
            out += '-' * i + '+'
        print(out)
