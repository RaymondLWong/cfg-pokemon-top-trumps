import pprint as pp
from random import randrange
from typing import List

import questionary
from enum import Enum
from questionary import Choice

from Card import Entry, Pokemon
from Generations import get_random_pokemon, get_available_generations
from Utils import create_choice, green, red, yellow, blue
from prompt_toolkit.styles import Style


class BattleResult(Enum):
    win = 1
    draw = 0
    lose = -1


class Turn(Enum):
    user = 1,
    opponent = 2


class CoinToss(Enum):
    heads = 1,
    tails = 0


class GameMode(Enum):
    single_match = 1,
    versus_bot = 2


class EntryNotFoundError(RuntimeError):
    pass


def get_entry(entry_name: str, pokemon: Pokemon) -> Entry:
    if isinstance(pokemon[entry_name], Entry):
        return pokemon[entry_name]
    elif isinstance(pokemon['stats'][entry_name], Entry):
        return pokemon['stats'][entry_name]
    else:
        raise EntryNotFoundError()


class Game:
    custom_styling = Style([
        ('highlighted', 'fg:cyan'),
        ('pointer', 'bold')
    ])

    battles = 0
    wins = 0
    draws = 0
    loses = 0

    def __init__(self):
        self.generation = self.prompt_user_for_generation()

        user_wants_to_battle = True
        while user_wants_to_battle:
            self.commence_battle()
            user_wants_to_battle = self.prompt_continue()
        self.show_score()

    def get_turn_player_str(self, turn_player: Turn) -> str:
        if turn_player == Turn.user:
            return green('YOU')
        else:
            return 'Your {}'.format(red('OPPONENT'))

    def choose_turn_player(self, user_choice: CoinToss) -> Turn:
        print('Tossing coin... ', end='')
        coin_toss: CoinToss = randrange(0, 1)
        if user_choice:
            turn_player = Turn.user if coin_toss == user_choice else Turn.opponent
        else:
            turn_player = Turn.user if coin_toss == CoinToss.heads else Turn.opponent
        coin_toss_str = 'HEADS' if coin_toss == CoinToss.heads else 'TAILS'
        print('{}! {} goes first!'.format(yellow(coin_toss_str), self.get_turn_player_str(turn_player)))
        return turn_player

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
        win_count = green(f'{self.wins} wins')
        lose_count = red(f'{self.loses} loses')
        draw_count = yellow(f'{self.draws} draws')
        total = blue(f'{self.battles} total')
        print(f'Your score: {win_count}, {lose_count}, {draw_count} ({total})')

    def commence_battle(self):
        # choose pokemon for user and opponent
        user_pokemon = get_random_pokemon(self.generation)
        print(f'You drew {blue(user_pokemon.name)}!')
        # pp.pprint(user_pokemon)
        enemy_pokemon = get_random_pokemon(self.generation)

        turn_player = self.choose_turn_player(CoinToss.heads)

        if turn_player == Turn.user:
            turn_player_chosen_stat = self.prompt_user_for_stat(user_pokemon)
        else:
            # pp.pprint(enemy_pokemon)
            turn_player_chosen_stat = self.choose_stat_for_opponent(enemy_pokemon)

        self.announce_chosen_stat(turn_player, turn_player_chosen_stat)

        result = self.do_battle(turn_player_chosen_stat, user_pokemon, enemy_pokemon)
        self.declare_winner(result)

    def get_stats_from_pokemon(self, pokemon: Pokemon) -> List[Choice]:
        choices = [
            create_choice(pokemon.poke_id),
            create_choice(pokemon.height),
            create_choice(pokemon.weight)
        ]
        for stat in pokemon.stats.values():
            choices.append(create_choice(stat))
        return choices

    def prompt_user_for_stat(self, user_pokemon: Pokemon) -> Entry:
        return questionary.select(
            message=f'Choose a stat from {user_pokemon.name} to compete with:',
            choices=self.get_stats_from_pokemon(user_pokemon),
            style=self.custom_styling,
            qmark='💪'
        ).ask()

    def choose_stat_for_opponent(self, opponent_pokemon: Pokemon) -> Entry:
        random_number = randrange(1, opponent_pokemon.option_count)
        random_stat = opponent_pokemon.get_available_battle_stats().__getitem__(random_number)
        return get_entry(random_stat, opponent_pokemon)

    def announce_chosen_stat(self, turn_player: Turn, stat: Entry):
        announce_turn_player = self.get_turn_player_str(turn_player)
        print('{} chose {}!'.format(announce_turn_player, yellow(stat.name)))

    def do_battle(self, stat_choice: Entry, user_pokemon: Pokemon, enemy_pokemon: Pokemon) -> BattleResult:
        self.battles += 1
        user_pokemon_stat = get_entry(stat_choice.name, user_pokemon).value
        enemy_pokemon_stat = get_entry(stat_choice.name, enemy_pokemon).value

        summary = 'Your {} has {} {}. Enemy {} has {} {}...'.format(
            blue(user_pokemon.name),
            yellow(user_pokemon_stat),
            yellow(stat_choice.name),
            red(enemy_pokemon.name),
            yellow(enemy_pokemon_stat),
            yellow(stat_choice.name)
        )
        print(summary)

        if user_pokemon_stat > enemy_pokemon_stat:
            return BattleResult.win
        elif user_pokemon_stat == enemy_pokemon_stat:
            return BattleResult.draw
        else:
            return BattleResult.lose

    def declare_winner(self, result: BattleResult):
        if result == BattleResult.win:
            self.wins += 1
            print('You {}!'.format(green('WIN')))
        elif result == BattleResult.lose:
            self.loses += 1
            print('You {}!'.format(red('LOSE')))
        else:
            self.draws += 1
            print('You {}!'.format(yellow('DRAW')))

    def prompt_user_for_generation(self) -> int:
        return questionary.select(
            message='Choose a generation to pick Pokemon from:',
            choices=get_available_generations(),
            style=self.custom_styling,
            qmark='⭐'
        ).ask()


new_game = Game()
