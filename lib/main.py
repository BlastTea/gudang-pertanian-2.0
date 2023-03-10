from enums import *
from interface import *

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
print('len:', len(
    '+----------------------------------------+----------------+----------------+'))
Interface.print_table(
    [
        {'value': 'Hello World asdfasdfasdfasdfasdfasdfff',
            'key': 'hahahaha', 'a': 'a'},
        # {'value': 'Hello World', 'key': 'hahahaha', 'a': 'a'},
        {'value': 'Haha', 'key': 'apa', 'a': 'a'}
    ],
    True
)
