from colorama import Fore, Style
from questionary import Choice

from Card import Entry


def highlight(string: str, colour: Fore = Fore.CYAN) -> str:
    return f'{colour}{string}{Style.RESET_ALL}'


def create_choice(entry: Entry, align=True) -> Choice:
    if align:
        aligned_title = '{:<3} {:<15}'.format(entry.name, str(entry.value))
        return Choice(title=aligned_title, value=entry)
    else:
        title = '{} ({})'.format(entry.name, str(entry.value))
        return Choice(title=title, value=entry)
