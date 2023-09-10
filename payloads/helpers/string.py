import string
from random import choice, randint


def random_string(length_minimum, length_maximum, characters=string.ascii_letters):
    return ''.join(choice(characters) for _ in range(randint(length_minimum, length_maximum)))


def unique_random_string_set(set_size, length_minimum, length_maximum, characters=string.ascii_letters):
    unqiue_strings = set()
    while len(unqiue_strings) < set_size:
        unqiue_strings.add(random_string(length_minimum=length_minimum,
                                         length_maximum=length_maximum,
                                         characters=characters))
    return list(unqiue_strings)

