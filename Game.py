import pprint as pp
import random
from enum import Enum

from colorama import Fore, Style
from Card import get_static_generation_counts, get_random_pokemon, Entry, Stats, Pokemon


class BattleResult(Enum):
    WIN = 1
    DRAW = 0
    LOSE = -1


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
        self.user_pokemon = get_random_pokemon(generation)
        print(f'You drew {highlight(self.user_pokemon.name)}!')
        pp.pprint(self.user_pokemon)
        (name, entry) = self.prompt_user_for_stat()
        stat_highlighted = highlight(name, Fore.YELLOW)
        print(f'You choose {stat_highlighted} with a value of {highlight(entry.value, Fore.YELLOW)}')
        enemy_pokemon = get_random_pokemon(generation)
        pp.pprint(enemy_pokemon)
        enemy_option = random.randrange(1, enemy_pokemon.option_count)
        enemy_stat = find_entry(enemy_option, vars(enemy_pokemon))[1]
        print(f'Enemy {highlight(enemy_pokemon.name, Fore.RED)} has a {stat_highlighted} of {highlight(enemy_stat, Fore.YELLOW)}')
        result = self.battle(entry.shortcut, enemy_pokemon)
        self.declare_winner(result)

    def prompt_user_for_stat(self) -> (str, Entry):
        valid_number = False
        while not valid_number:
            max_options = self.user_pokemon.option_count
            number = input(f'Choose a stat by pressing the corresponding number key (1-{max_options}): ')
            try:
                option = int(number)
                valid_number = True
                return find_entry(option, vars(self.user_pokemon))
            except ValueError:
                print(f'Invalid number {number}, please try again.')

    def battle(self, choice: int, enemy_pokemon: Pokemon) -> BattleResult:
        user_pokemon_stat = find_entry(choice, vars(self.user_pokemon))[1].value
        enemy_pokemon_stat = find_entry(choice, vars(enemy_pokemon))[1].value

        if user_pokemon_stat > enemy_pokemon_stat:
            return BattleResult.WIN
        elif user_pokemon_stat == enemy_pokemon_stat:
            return BattleResult.DRAW
        else:
            return BattleResult.LOSE

    @staticmethod
    def declare_winner(result: BattleResult):
        if result == BattleResult.WIN:
            print(f"You {highlight('WIN', Fore.GREEN)}!")
        elif result == BattleResult.LOSE:
            print(f"You {highlight('LOSE', Fore.RED)}!")
        else:
            print(f"You {highlight('DRAW', Fore.YELLOW)}!")


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
