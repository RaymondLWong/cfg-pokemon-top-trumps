import random
import pprint as pp
from typing import List

import questionary
from enum import Enum
from colorama import Fore
from questionary import Choice

from Card import Entry, Stats, Pokemon
from Generations import get_random_pokemon, get_available_generations
from Utils import highlight, create_choice
from prompt_toolkit.styles import Style


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
    custom_styling = Style([
        ('highlighted', 'fg:cyan'),
        ('pointer', 'bold')
    ])

    def __init__(self):
        self.generation = self.prompt_user_for_generation()
        self.battles = 0
        self.wins = 0
        self.draws = 0
        self.loses = 0

        user_wants_to_battle = True
        while user_wants_to_battle:
            self.commence_battle()
            user_wants_to_battle = self.prompt_continue()
        self.show_score()

    def prompt_continue(self) -> bool:
        return questionary.select(
            message='Battle again?',
            choices=[
                Choice(title='Yes', value=True),
                Choice(title='No', value=False)
            ],
            style=self.custom_styling,
            qmark='→'
        ).ask()

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
        user_chosen_pokemon_stat = self.prompt_user_for_stat(user_pokemon)
        stat_highlighted = highlight(user_chosen_pokemon_stat.name, Fore.YELLOW)
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

    def get_stats_from_pokemon(self, pokemon: Pokemon) -> List[Choice]:
        choices = [
            create_choice(pokemon.poke_id),
            create_choice(pokemon.height),
            create_choice(pokemon.weight)
        ]
        for stat in vars(pokemon.stats).values():
            choices.append(create_choice(stat))
        return choices

    def prompt_user_for_stat(self, user_pokemon: Pokemon) -> Entry:
        return questionary.select(
            message=f'Choose a stat from {user_pokemon.name} to compete with:',
            choices=self.get_stats_from_pokemon(user_pokemon),
            style=self.custom_styling,
            qmark='💪'
        ).ask()

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

    def prompt_user_for_generation(self) -> int:
        return questionary.select(
            message='Choose a generation to pick Pokemon from:',
            choices=get_available_generations(),
            style=self.custom_styling,
            qmark='⭐'
        ).ask()


new_game = Game()
