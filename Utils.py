from colorama import Fore, Style
from questionary import Choice
from Card import Entry

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
