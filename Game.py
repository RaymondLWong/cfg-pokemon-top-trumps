import pprint as pp
from colorama import Fore, Style
from Card import get_static_generation_counts, get_random_pokemon, Entry


def highlight(string: str) -> str:
    return f'{Fore.CYAN}{string}{Style.RESET_ALL}'


class Game:
    def __init__(self):
        generation = prompt_user_for_generation()
        self.pokemon = get_random_pokemon(generation)
        print(f'You drew {highlight(self.pokemon.name.capitalize())}!')
        pp.pprint(self.pokemon)
        (name, entry) = self.prompt_user_for_stat()
        print(f'You choose {highlight(name)} with a value of {highlight(entry.value)}')

    def find_entry(self, option: int) -> (str, Entry):
        for name, entry in vars(self.pokemon).items():
            if entry.shortcut == option:
                return name, entry

    def prompt_user_for_stat(self) -> (str, Entry):
        valid_number = False
        while not valid_number:
            number = input('Choose a stat by pressing the corresponding number key: ')
            try:
                option = int(number)
                valid_number = True
                return self.find_entry(option)
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

