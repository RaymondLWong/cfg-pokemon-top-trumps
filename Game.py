import pprint as pp
import random
from colorama import Fore, Style
from Card import get_static_generation_counts, get_random_pokemon, Entry, Stats


def find_entry(option: int, entries: dict) -> (str, Entry):
    for name, entry in entries.items():
        if isinstance(entry, Stats):
            return find_entry(option, vars(entry))
        elif isinstance(entry, Entry) and entry.shortcut == option:
            return name, entry


def highlight(string: str, colour: Fore = Fore.CYAN) -> str:
    return f'{colour}{string}{Style.RESET_ALL}'


class Game:
    def __init__(self):
        generation = prompt_user_for_generation()
        self.pokemon = get_random_pokemon(generation)
        print(f'You drew {highlight(self.pokemon.name)}!')
        pp.pprint(self.pokemon)
        (name, entry) = self.prompt_user_for_stat()
        print(f'You choose {highlight(name, Fore.YELLOW)} with a value of {highlight(entry.value, Fore.YELLOW)}')
        enemy_pokemon = get_random_pokemon(generation)
        pp.pprint(enemy_pokemon)
        enemy_option = random.randrange(1, enemy_pokemon.option_count)
        (enemy_stat, enemy_stat_value) = find_entry(enemy_option, vars(enemy_pokemon))
        print(f'Enemy got {highlight(enemy_pokemon.name, Fore.RED)}!')
        print(f'Enemy chose {highlight(enemy_stat, Fore.YELLOW)} with a value of {highlight(enemy_stat_value, Fore.YELLOW)}')

    def prompt_user_for_stat(self) -> (str, Entry):
        valid_number = False
        while not valid_number:
            max_options = self.pokemon.option_count
            number = input(f'Choose a stat by pressing the corresponding number key (1-{max_options}): ')
            try:
                option = int(number)
                valid_number = True
                return find_entry(option, vars(self.pokemon))
            except ValueError:
                print(f'Invalid number {number}, please try again.')


def prompt_user_for_generation() -> int:
    generation_count = len(get_static_generation_counts())
    user_picked_gen = input(f'Pick a generation between 1-{generation_count}: ')
    try:
        gen = int(user_picked_gen)
        print(f'You chose Generation {gen}!')
        if gen not in get_static_generation_counts():
            print(f'Generation {gen} is not supported. Defaulting to Gen 1.')
            gen = 1
        return gen
    except ValueError:
        print('Defaulting to Generation 1...')
        return 1


new_game = Game()
