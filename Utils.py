from colorama import Fore, Style


def highlight(string: str, colour: Fore = Fore.CYAN) -> str:
    return f'{colour}{string}{Style.RESET_ALL}'
