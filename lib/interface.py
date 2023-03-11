import os
from typing import Any

from constants import *
from enums import *
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
    def print_table(
        values: list[dict[str, Any]],
        flex=True,
        alignments: dict[str, TextAlign] | list[TextAlign] = None,
        fits: dict[str, Fit] | list[Fit] = None,
        default_alignment: TextAlign = TextAlign.CENTER,
        default_fit: Fit = Fit.EXPAND
    ):
        if isinstance(alignments, list) and len(values[0]) != len(alignments):
            raise AssertionError(
                'Length of alignments must be the same as values')
        if isinstance(fits, list) and len(values[0]) != len(fits):
            raise AssertionError('Length of fits must be the same as values')

        actual_length = 1
        column_lengths: list[dict[str, Any]] = [
            {
                'min_width': 0,
                'width': 0,
                'alignment': default_alignment,
                'fit': default_fit
            }
        ] * len(values[0])

        for value in values:
            for i, key in enumerate(value):
                width = max([column_lengths[i]['width'], len(
                    f'{value[key]}'), len(key)])
                column_lengths[i] = {
                    'min_width': width,
                    'width': width,
                    'alignment': default_alignment,
                    'fit': default_fit
                }

        for i, column_length in enumerate(column_lengths):
            column_lengths[i]['min_width'] += 2
            column_lengths[i]['width'] += 2

            if isinstance(alignments, list):
                column_lengths[i]['alignment'] = alignments[i]
            if isinstance(alignments, dict):
                if alignments is not None:
                    if alignments.get(list(values[0].keys())[i]):
                        column_lengths[i]['alignment'] = alignments[list(values[0].keys())[
                            i]]

            if isinstance(fits, list):
                column_lengths[i]['fit'] = fits[i]
            if isinstance(fits, dict):
                if fits is not None:
                    if fits.get(list(values[0].keys())[i]):
                        column_lengths[i]['fit'] = fits[list(
                            values[0].keys())[i]]

            actual_length += column_length['width'] + 1

        if WIDTH > actual_length and flex:
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
                    new_column_lengths[i] = (WIDTH) // (len(column_lengths) - total_of_tight_column)

                    if new_column_lengths[i] <= column_lengths[i]['width']:
                        diff = column_lengths[i]['width'] - \
                            new_column_lengths[i]
                        new_column_lengths[i] += diff
                        actual_diff += diff
                        total_of_vast_column -= 1
                actual_length += new_column_lengths[i] + 1

            actual_diff += total_of_vast_column

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
