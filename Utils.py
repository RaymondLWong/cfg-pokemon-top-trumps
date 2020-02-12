from colorama import Fore, Style
from questionary import Choice

from Card import Entry


def highlight(string: str, colour: Fore = Fore.CYAN) -> str:
    return f'{colour}{string}{Style.RESET_ALL}'


def create_choice(entry: Entry) -> Choice:
    return Choice(
        title='{} ({})'.format(entry.name, entry.value),
        value=entry
    )
