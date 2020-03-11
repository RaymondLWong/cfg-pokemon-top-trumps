from colorama import Fore, Style
from questionary import Choice
from src.gameplay.card import Entry
import random

str_int = str or int


def highlight(string: str_int, colour: Fore = Fore.CYAN) -> str:
    return f'{colour}{string}{Style.RESET_ALL}'


def red(string: str_int) -> str:
    return highlight(string, Fore.RED)


def green(string: str_int) -> str:
    return highlight(string, Fore.GREEN)


def blue(string: str_int) -> str:
    return highlight(string, Fore.CYAN)


def yellow(string: str_int) -> str:
    return highlight(string, Fore.YELLOW)


def purple(string: str_int) -> str:
    return highlight(string, Fore.MAGENTA)


def create_choice(entry: Entry) -> Choice:
    aligned_title = '{:<17} {:<3}'.format(entry.name, str(entry.value))
    return Choice(title=aligned_title, value=entry)


def rainbow(text: str) -> str:
    bad_colours = ['BLACK', 'LIGHTBLACK_EX', 'RESET']
    colour_codes = vars(Fore)
    colours = [colour_codes[color] for color in colour_codes if color not in bad_colours]
    return ''.join([random.choice(colours) + char for char in text])

