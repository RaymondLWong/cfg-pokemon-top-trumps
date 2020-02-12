from colorama import Fore, Style


def highlight(string: str, colour: Fore = Fore.CYAN) -> str:
    return f'{colour}{string}{Style.RESET_ALL}'


def grass(pokemon_name: str) -> str:
    return highlight(pokemon_name, Fore.GREEN)


def fire(pokemon_name: str) -> str:
    return highlight(pokemon_name, Fore.RED)


def water(pokemon_name: str) -> str:
    return highlight(pokemon_name, Fore.CYAN)
