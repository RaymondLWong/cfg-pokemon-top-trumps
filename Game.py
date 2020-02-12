import random
import pprint as pp
from PyInquirer import prompt, print_json
from enum import Enum
from colorama import Fore
from Card import Entry, Stats, Pokemon
from Generations import get_random_pokemon, get_available_generations
from Utils import highlight


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


class Game:
    def __init__(self):
        self.generation = prompt_user_for_generation()
        self.battles = 0
        self.wins = 0
        self.draws = 0
        self.loses = 0

        user_wants_to_battle = True
        while user_wants_to_battle:
            self.commence_battle()
            user_wants_to_battle = self.prompt_continue()
        self.show_score()

    def prompt_continue(self):
        battle_again = input(f'Do you want to battle again? (y/n) ')
        return battle_again != 'n'

    def show_score(self):
        win_count = highlight(f'{self.wins} wins', Fore.GREEN)
        lose_count = highlight(f'{self.loses} loses', Fore.RED)
        draw_count = highlight(f'{self.draws} draws', Fore.YELLOW)
        total = highlight(f'{self.battles} total', Fore.CYAN)
        print(f'Your score: {win_count}, {lose_count}, {draw_count} ({total})')

    def commence_battle(self):
        user_pokemon = get_random_pokemon(self.generation)
        print(f'You drew {highlight(user_pokemon.name)}!')
        pp.pprint(user_pokemon)
        (stat_name, user_chosen_pokemon_stat) = self.prompt_user_for_stat(user_pokemon)
        stat_highlighted = highlight(stat_name, Fore.YELLOW)
        announce_user_stat = 'You choose {} with a value of {}'.format(
            stat_highlighted,
            highlight(user_chosen_pokemon_stat.value, Fore.YELLOW)
        )
        print(announce_user_stat)
        enemy_pokemon = get_random_pokemon(self.generation)
        pp.pprint(enemy_pokemon)
        # FIXME: should only pick enemy stat when it's their turn
        enemy_option = random.randrange(1, enemy_pokemon.option_count)
        enemy_stat = find_entry(enemy_option, vars(enemy_pokemon))[1]
        announce_enemy_stat = 'Enemy {} has a {} of {}'.format(
            highlight(enemy_pokemon.name, Fore.RED),
            stat_highlighted,
            highlight(enemy_stat, Fore.YELLOW)
        )
        print(announce_enemy_stat)
        result = self.do_battle(user_chosen_pokemon_stat.shortcut, user_pokemon, enemy_pokemon)
        self.declare_winner(result)

    def prompt_user_for_stat(self, user_pokemon: Pokemon) -> (str, Entry):
        valid_number = False
        while not valid_number:
            max_options = user_pokemon.option_count
            number = input(f'Choose a stat by pressing the corresponding number key (1-{max_options}): ')
            try:
                option = int(number)
                valid_number = True
                return find_entry(option, vars(user_pokemon))
            except ValueError:
                print(f'Invalid number {number}, please try again.')

    def do_battle(self, choice: int, user_pokemon: Pokemon, enemy_pokemon: Pokemon) -> BattleResult:
        self.battles += 1
        user_pokemon_stat = find_entry(choice, vars(user_pokemon))[1].value
        enemy_pokemon_stat = find_entry(choice, vars(enemy_pokemon))[1].value

        if user_pokemon_stat > enemy_pokemon_stat:
            return BattleResult.WIN
        elif user_pokemon_stat == enemy_pokemon_stat:
            return BattleResult.DRAW
        else:
            return BattleResult.LOSE

    def declare_winner(self, result: BattleResult):
        if result == BattleResult.WIN:
            self.wins += 1
            print('You {}!'.format(highlight('WIN', Fore.GREEN)))
        elif result == BattleResult.LOSE:
            self.loses += 1
            print('You {}!'.format(highlight('LOSE', Fore.RED)))
        else:
            self.draws += 1
            print('You {}!'.format(highlight('DRAW', Fore.YELLOW)))


def prompt_user_for_generation() -> int:
    questions = [
        {
            'type': 'list',
            'name': 'user_chosen_generation',
            'message': 'Choose a generation to pick Pokemon from:',
            'choices': get_available_generations()
        }
    ]
    user_picked_gen = prompt(questions)
    print_json(user_picked_gen)

    return 1


new_game = Game()
