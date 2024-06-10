import os
import random


def random_bytes(length_minimum, length_maximum):
    length = random.randint(length_minimum, length_maximum)
    return os.urandom(length)
