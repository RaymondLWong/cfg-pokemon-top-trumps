import pprint as pp
import random
from typing import List, TypeVar

import questionary
from enum import Enum
from questionary import Choice

from Card import Entry, Pokemon, create_pokemon
from Generations import get_random_pokemon, get_available_generations, get_static_pokemon_count_for_generation, \
    get_poke_id
from Utils import create_choice, green, red, yellow, blue, purple
from prompt_toolkit.styles import Style

T = TypeVar('T')


class BattleResult(Enum):
    win = 1
    draw = 0
    lose = -1


class Turn(Enum):
    user = 1,
    opponent = 2


Player = Turn


class CoinToss(Enum):
    heads = 1,
    tails = 0


class GameMode(Enum):
    single_match = 1,
    traditional = 2,  # winner keeps cards, draws ensue extra round, continues until s player has all cards
    deplete = 3,  # stop when card limit reached
    vs_player = 4


def compare(a: T, b: T) -> BattleResult:
    if a > b:
        return BattleResult.win
    elif a == b:
        return BattleResult.draw
    else:
        return BattleResult.lose


def validate_card_limit(limit: str) -> bool:
    try:
        int(limit)
        return True
    except ValueError:
        print(f'Please enter a valid number between 1 and {limit}')
        return False


class Game:
    custom_styling = Style([
        ('highlighted', 'fg:cyan'),
        ('pointer', 'bold')
    ])

    generation: int

    battle_count = 0
    wins = 0
    draws = 0
    loses = 0

    deck: List[int] = []
    player_cards: List[Pokemon] = []
    opponent_cards: List[Pokemon] = []

    def __init__(self):
        game_mode = self.prompt_game_mode()

        if game_mode == GameMode.single_match:
            self.start_single_match()
        elif game_mode == GameMode.traditional:
            self.start_traditional()
        elif game_mode == GameMode.deplete:
            self.start_deplete_game_mode()
        else:
            self.start_versus_player()

    def prompt_game_mode(self) -> GameMode:
        return questionary.select(
            message=f'Choose a game mode:',
            choices=[
                Choice(title='Single Match', value=GameMode.single_match),
                Choice(title='Traditional', value=GameMode.traditional),
                Choice(title='Deplete', value=GameMode.deplete),
                Choice(title='Versus Player', value=GameMode.vs_player)
            ],
            style=self.custom_styling,
            qmark='🕹'
        ).ask()

    def start_single_match(self):
        self.generation = self.prompt_user_for_generation()
        self.create_deck()
        user_wants_to_battle = True
        first_battle = True
        while user_wants_to_battle:
            self.commence_battle(first_battle=first_battle)
            first_battle = False
            user_wants_to_battle = self.prompt_continue()
        self.show_final_score()

    def start_traditional(self):
        pass

    def start_deplete_game_mode(self):
        self.generation = self.prompt_user_for_generation()
        self.create_deck()
        card_limit = self.prompt_max_cards_win_condition(self.generation)
        turn_player = self.choose_turn_player(CoinToss.heads)
        previous_battle_result = None
        while self.battle_count < card_limit:
            if previous_battle_result == BattleResult.lose:
                turn_player = self.change_turns(turn_player)
            previous_battle_result = self.commence_battle(turn_player)
        self.announce_match_winner_for_deplete()
        self.show_final_score()

    def start_versus_player(self):
        pass

    def change_turns(self, current_turn_player: Turn) -> Turn:
        return Turn.opponent if current_turn_player == Turn.user else Turn.user

    def prompt_card_limit(self, gen: int) -> int:
        max_cards = get_static_pokemon_count_for_generation(gen)
        user_choice = questionary.text(
            message=f'Enter a card limit (1-{max_cards}):',
            style=self.custom_styling,
            qmark='🃏',
            validate=validate_card_limit
        ).ask()
        return int(user_choice) or max_cards

    def prompt_max_cards_win_condition(self, gen: int) -> int or None:
        enforce_limit = questionary.confirm(
            message=f'Set a card limit?',
            style=self.custom_styling,
            qmark='🧢'
        ).ask()
        return self.prompt_card_limit(gen) if enforce_limit else  get_static_pokemon_count_for_generation(gen)

    def create_deck(self):
        pokemon_in_generation = get_static_pokemon_count_for_generation(self.generation)
        offset = get_poke_id(self.generation, 1)
        self.deck = list(range(offset, offset + pokemon_in_generation))

    def draw_from_deck(self) -> Pokemon:
        poke_id = random.choice(self.deck)
        self.deck.remove(poke_id)
        pokemon = create_pokemon(poke_id)
        return pokemon

    def move_card(self, card: Pokemon, player_to_take_from: Player):
        if player_to_take_from == Player.user:
            self.opponent_cards.append(card)
            self.player_cards.remove(card)
        else:
            self.player_cards.append(card)
            self.opponent_cards.remove(card)

    def choose_turn_player(self, user_choice: CoinToss) -> Turn:
        print('Tossing coin... ', end='')
        coin_toss: CoinToss = random.choice([CoinToss.heads, CoinToss.tails])
        if user_choice:
            turn_player = Turn.user if coin_toss == user_choice else Turn.opponent
        else:
            turn_player = Turn.user if coin_toss == CoinToss.heads else Turn.opponent
        coin_toss_str = 'HEADS' if coin_toss == CoinToss.heads else 'TAILS'
        print('{}! '.format(yellow(coin_toss_str)), end='')
        if turn_player == Turn.user:
            print('{} go first!'.format(green('YOU')))
        else:
            print('Your {} goes first!'.format(yellow(red('OPPONENT'))))
        return turn_player

    def prompt_continue(self) -> bool:
        win_rate = 100 * (self.wins / self.battle_count)
        stats = '{:.2f}% win rate, {} total battles'.format(win_rate, self.battle_count)
        return questionary.select(
            message=f'Battle again? ({stats})',
            choices=[
                Choice(title='Yes', value=True),
                Choice(title='No', value=False)
            ],
            style=self.custom_styling,
            qmark='👊'
        ).ask()

    def show_final_score(self):
        win_count = green(f'{self.wins} wins')
        lose_count = red(f'{self.loses} loses')
        draw_count = yellow(f'{self.draws} draws')
        total = blue(f'{self.battle_count} total')
        print('=' * 50)
        print(f'Your score: {win_count}, {lose_count}, {draw_count} ({total})')
        print('=' * 50)

    def commence_battle(
            self,
            turn_player: Turn = None,
            first_battle: bool = None
    ) -> BattleResult:
        if first_battle or not turn_player:
            turn_player = self.choose_turn_player(CoinToss.heads)

        # choose pokemon for user and opponent
        user_pokemon = self.draw_from_deck()
        self.player_cards.append(user_pokemon)
        print(f'You drew {blue(user_pokemon.name)}!')
        # pp.pprint(user_pokemon)
        enemy_pokemon = self.draw_from_deck()
        self.opponent_cards.append(enemy_pokemon)

        if turn_player == Turn.user:
            turn_player_chosen_stat = self.prompt_user_for_stat(user_pokemon)
        else:
            # pp.pprint(enemy_pokemon)
            turn_player_chosen_stat = self.choose_stat_for_opponent(enemy_pokemon)

        self.announce_chosen_stat(turn_player, turn_player_chosen_stat)

        result = self.do_battle(turn_player_chosen_stat, user_pokemon, enemy_pokemon)
        # TODO: if draw, pick another card
        return result

    def prompt_user_for_stat(self, user_pokemon: Pokemon) -> Entry:
        choices = list(map(lambda stat: create_choice(stat), user_pokemon.get_available_battle_stats(False)))
        return questionary.select(
            message=f'Choose a stat from {user_pokemon.name} to compete with:',
            choices=choices,
            style=self.custom_styling,
            qmark='💪'
        ).ask()

    def choose_stat_for_opponent(self, opponent_pokemon: Pokemon) -> Entry:
        available_stats = opponent_pokemon.get_available_battle_stats(True)
        random_stat = random.choice(available_stats)
        return opponent_pokemon[random_stat]

    def get_turn_player_str(self, turn_player: Turn) -> str:
        if turn_player == Turn.user:
            return green('YOU')
        else:
            return 'Your {}'.format(red('OPPONENT'))

    def announce_chosen_stat(self, turn_player: Turn, stat: Entry):
        announce_turn_player = self.get_turn_player_str(turn_player)
        print('{} chose {}!'.format(announce_turn_player, yellow(stat.name)))

    def do_battle(self, stat_choice: Entry, user_pokemon: Pokemon, enemy_pokemon: Pokemon) -> BattleResult:
        self.battle_count += 1
        stat_name = stat_choice.name
        user_pokemon_stat = user_pokemon[stat_name].value
        enemy_pokemon_stat = enemy_pokemon[stat_name].value

        result = compare(user_pokemon_stat, enemy_pokemon_stat)
        if result == BattleResult.draw:
            self.draws += 1
            user_pokemon = blue(user_pokemon.name),
            enemy_pokemon = red(enemy_pokemon.name),
            stat_name = yellow(stat_name),
            stat_value = yellow(user_pokemon_stat)
            summary = f"{yellow('DRAW')}! "\
                      f"Your {user_pokemon} and your opponent's {enemy_pokemon} both have {stat_value} {stat_name}"
        else:
            if result == BattleResult.win:
                self.wins += 1
                self.move_card(enemy_pokemon, Player.opponent)

                winner = 'Your'
                wining_pokemon = blue(user_pokemon.name)
                wining_stat = yellow(user_pokemon_stat)
                loser = 'enemy'
                loser_pokemon = red(enemy_pokemon.name)
                losing_stat = yellow(enemy_pokemon_stat)
            else:
                self.loses += 1
                self.move_card(user_pokemon, Player.user)
                winner = 'Enemy'
                wining_pokemon = red(enemy_pokemon.name)
                wining_stat = yellow(enemy_pokemon_stat)
                loser = 'your'
                loser_pokemon = blue(user_pokemon.name)
                losing_stat = yellow(user_pokemon_stat)
            coloured_stat_name = yellow(stat_name)
            summary = f"{winner} {wining_pokemon}'s {wining_stat} {coloured_stat_name} beats "\
                      f"{loser} {loser_pokemon}'s {losing_stat} {coloured_stat_name}! "
        print(summary)
        return result

    def announce_match_winner(self, result: BattleResult):
        print('=' * 50)
        player_card_count = purple(len(self.player_cards))
        opponent_card_count = purple(len(self.opponent_cards))
        print(f'You accumulated {player_card_count} cards and your opponent amassed {opponent_card_count} cards.')
        if result == BattleResult.win:
            print('You {} the match!'.format(green('WIN')))
        elif result == BattleResult.lose:
            print('You {} the match!'.format(red('LOSE')))
        else:
            print('The match ends in a {}!'.format(yellow('DRAW')))

    def announce_match_winner_for_deplete(self):
        match_result = compare(len(self.player_cards), len(self.opponent_cards))
        self.announce_match_winner(match_result)

    def prompt_user_for_generation(self) -> int:
        return questionary.select(
            message='Choose a generation to pick Pokemon from:',
            choices=get_available_generations(),
            style=self.custom_styling,
            qmark='⭐'
        ).ask()


new_game = Game()
