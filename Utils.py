from colorama import Fore, Style
from questionary import Choice

from Card import Entry


def highlight(string: str, colour: Fore = Fore.CYAN) -> str:
    return f'{colour}{string}{Style.RESET_ALL}'


def red(string: str) -> str:
    return highlight(string, Fore.RED)


def green(string: str) -> str:
    return highlight(string, Fore.GREEN)


def blue(string: str) -> str:
    return highlight(string, Fore.CYAN)


def yellow(string: str) -> str:
    return highlight(string, Fore.YELLOW)


def create_choice(entry: Entry) -> Choice:
    aligned_title = '{:<17} {:<3}'.format(entry.name, str(entry.value))
    return Choice(title=aligned_title, value=entry)
