import random
from string import ascii_letters
from .config import BLOCKS

ALPHABET = list(ascii_letters)
ALPHABET_NUMBERS = ALPHABET + [str(i) for i in range(10)]

def random_string(length: int, char_set=ALPHABET) -> str:
    return "".join([random.choice(char_set) for _ in range(length)])


def generate_variable_name(varname: str) -> str:
    return random_string(1) + "_".join([random_string(19, char_set=ALPHABET_NUMBERS), varname])

def get_game_object_class(name) -> str:
    for block_name in BLOCKS:
        if name.startswith(block_name):
            return block_name.title()
