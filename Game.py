import random
from decimal import Decimal
from typing import List, TypeVar, Callable

import questionary
from enum import Enum
from questionary import Choice

from Card import Entry, Pokemon, create_pokemon
from Generations import get_available_generations, get_static_pokemon_count_for_generation, \
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


def validate_card_limit(limit: str, min_value: int, max_value: int) -> bool:
    try:
        value = int(limit)
        return min_value <= value <= max_value
    except ValueError:
        print(f'Please enter a valid number between 2 and {limit}')
        return False


def get_separator(sep: str = None, colour_me: Callable[[str], str] = None) -> str:
    sep = sep if sep else '=' * 50
    return colour_me(sep) if colour_me else sep


def print_separator(colour_me: Callable[[str], str] = None):
    print(get_separator(colour_me=colour_me))


class Game:
    custom_styling = Style([
        ('highlighted', 'fg:cyan'),
        ('pointer', 'bold')
    ])

    game_mode: GameMode

    generation: int
    card_limit: int

    battle_count = 0
    wins = 0
    draws = 0
    loses = 0

    deck: List[int] = []
    player_cards: List[Pokemon] = []
    opponent_cards: List[Pokemon] = []

    def __init__(self):
        self.game_mode = self.prompt_game_mode()

        if self.game_mode == GameMode.single_match:
            self.start_single_match()
        elif self.game_mode == GameMode.traditional:
            self.start_traditional()
        elif self.game_mode == GameMode.deplete:
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

    def start_game(
            self,
            prompt_card_limit: bool = False
    ):
        self.generation = self.prompt_user_for_generation()
        self.create_deck()
        if prompt_card_limit:
            self.card_limit = self.prompt_max_cards_win_condition(self.generation)
            self.chop_deck(self.card_limit)
        self.announce_start()
        self.announce_instructions()

    def start_single_match(self):
        self.start_game()
        user_wants_to_battle = True
        first_battle = True
        while user_wants_to_battle:
            self.commence_battle(first_battle=first_battle)
            first_battle = False
            user_wants_to_battle = self.prompt_continue()
        self.announce_match_winner()

    # TODO: refactor as next 2 functions share lots of code
    def start_traditional(self):
        self.start_game(True)
        turn_player = self.choose_turn_player(CoinToss.heads)
        previous_battle_result = None
        while len(self.deck) != 0 and not self.has_player_obtained_all_cards():
            user_lost = turn_player == Turn.user and previous_battle_result == BattleResult.lose
            opponent_lost = turn_player == Turn.opponent and previous_battle_result == BattleResult.win
            if user_lost or opponent_lost:
                turn_player = self.change_turns(turn_player)

            if self.give_final_card(turn_player):
                break
            else:
                previous_battle_result = self.commence_battle(turn_player)
            print_separator()
        self.announce_match_winner()

    def start_deplete_game_mode(self):
        self.start_game(True)
        turn_player = self.choose_turn_player(CoinToss.heads)
        previous_battle_result = None
        while len(self.deck) > 0 and round(self.battle_count * 2) < self.card_limit:
            user_lost = turn_player == Turn.user and previous_battle_result == BattleResult.lose
            opponent_lost = turn_player == Turn.opponent and previous_battle_result == BattleResult.win

            if self.give_final_card(turn_player):
                break
            else:
                if user_lost or opponent_lost:
                    turn_player = self.change_turns(turn_player)
                previous_battle_result = self.commence_battle(turn_player)
            print_separator()
        self.announce_match_winner()

    def start_versus_player(self):
        pass

    def has_player_obtained_all_cards(self) -> bool:
        if len(self.deck) == 0:
            if len(self.player_cards) == 0 or len(self.opponent_cards) == 0:
                return True
        return False

    def give_final_card(self, turn_player: Turn) -> bool:
        # if there's one more card in the neutral deck,
        # it will just get added to the winning person's deck,
        # so start calculating winner
        if len(self.deck) == 1:
            pokemon = create_pokemon(self.deck[0])
            announcement = 'There is only one card left in the neutral deck ({}). ' \
                           'Determining winner...'.format(blue(pokemon.name))
            print(announcement)

            # add last card to current player's turn
            if turn_player == Turn.user:
                self.player_cards.append(pokemon)
            else:
                self.opponent_cards.append(pokemon)
            return True
        return False

    def chop_deck(self, new_size: int):
        if new_size:
            while len(self.deck) > new_size:
                self.deck.remove(random.choice(self.deck))

    def change_turns(self, current_turn_player: Turn) -> Turn:
        return Turn.opponent if current_turn_player == Turn.user else Turn.user

    def prompt_card_limit(self, gen: int) -> int:
        max_cards = get_static_pokemon_count_for_generation(gen)
        user_choice = questionary.text(
            message=f'Enter a card limit (2-{max_cards}):',
            style=self.custom_styling,
            qmark='🃏',
            validate=lambda user_input: validate_card_limit(user_input, 2, max_cards)
        ).ask()
        return int(user_choice) or max_cards

    def prompt_max_cards_win_condition(self, gen: int) -> int or None:
        enforce_limit = questionary.confirm(
            message=f"Set a card limit? (the default is 10% of a generation's pokemon)",
            style=self.custom_styling,
            qmark='🧢'
        ).ask()

        if enforce_limit:
            return self.prompt_card_limit(gen)
        else:
            pokemon_in_generation = get_static_pokemon_count_for_generation(gen)
            ten_percent = pokemon_in_generation / 10
            return int(ten_percent)

    def create_deck(self):
        pokemon_in_generation = get_static_pokemon_count_for_generation(self.generation)
        offset = get_poke_id(self.generation, 1)
        self.deck = list(range(offset, offset + pokemon_in_generation))

    def draw_from_deck(self, deck: List[Pokemon or int]) -> Pokemon:
        deck_to_search = self.deck if len(self.deck) > 0 else deck

        if len(deck_to_search) > 0 and isinstance(deck_to_search[0], Pokemon):
            card = random.choice(deck_to_search)
            deck_to_search.remove(card)
            return card
        else:
            poke_id = random.choice(deck_to_search)
            deck_to_search.remove(poke_id)
            pokemon = create_pokemon(poke_id)
            return pokemon

    def move_card(self, card: Pokemon, destination_pile: Player):
        if destination_pile == Player.user:
            self.player_cards.append(card)
            self.opponent_cards.remove(card)
        else:
            self.opponent_cards.append(card)
            self.player_cards.remove(card)

    def announce_start(self):
        print_separator(green)
        left_side = red('|')
        right_side = blue('|')
        title = purple('STARTING GAME...')
        print('{:<} {:^55} {:>}'.format(left_side, title, right_side))
        print_separator(yellow)

    def announce_instructions(self):
        instructions = []

        def title_me(title: str):
            instructions.append("{:^60}".format(blue(title)))

        title_me('General Instructions')
        instructions.extend([
            "- A coin flip will determine who starts the game; if it's heads, you start!",
            "- When a round starts, each player will draw one card from the deck,",
            "   starting with whomever won the last round, or the initial coin toss.",
            "- On a player's turn, they call out a stat they want to compete with.",
            "   - The turn player then announces the chosen stat and both players compare values.",
            "   - The winner then takes the loser's card (depending on the game mode).",
            "   - If there is a draw, the cards are set aside and both players draw again.",
            "   - The final winner of this 'mini-round wins ALL cards!",
            "- This repeats until there are no cards left in the neutral deck.",
            get_separator(colour_me=yellow)
        ])

        if self.game_mode == GameMode.single_match:
            title_me('Single Match Mode')
            instructions.append('- You start the game with one round; you choose when to stop!')
        elif self.game_mode == GameMode.traditional:
            title_me('Traditional Mode')
            instructions.append('- The player to obtain ALL cards wins!')
            instructions.append('- Once the neutral deck is empty, '
                                'players start using their accumulated decks.')
        elif self.game_mode == GameMode.deplete:
            title_me('Deplete Mode')
            instructions.append("- When the neutral deck is depleted, "
                                "the player with the highest number of cards wins!")
        else:
            title_me('PvP Mode')
            instructions.append("- Enter your opponent's IP address and agree on a game mode!")
        print('\n'.join(instructions))
        print_separator(yellow)

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
        win_rate = self.get_win_rate()
        stats = '{} % win rate, {} total battles'.format(win_rate, self.battle_count)
        return questionary.select(
            message=f'Battle again? ({stats})',
            choices=[
                Choice(title='Yes', value=True),
                Choice(title='No', value=False)
            ],
            style=self.custom_styling,
            qmark='👊'
        ).ask()

    def get_win_rate(self) -> str:
        win_rate = 100 * (self.wins / self.battle_count) if self.battle_count > 0 else 0
        if Decimal(win_rate) % 1 == 0:
            win_rate = int(win_rate)
        else:
            win_rate = '{:.2f}'.format(win_rate)
        return win_rate

    def show_win_rate(self):
        win_rate = self.get_win_rate()
        smiley = ':)' if int(float(win_rate)) > 70 else ':('
        win_rate = purple(win_rate)
        print('Your win rate is {} % {}'.format(win_rate, smiley))

    def show_final_score(self):
        win_count = green(f'{self.wins} wins')
        lose_count = red(f'{self.loses} loses')
        draw_count = yellow(f'{self.draws} draws')
        total = blue(f'{self.battle_count} total')
        print_separator()
        self.show_win_rate()
        print(f'Your score: {win_count}, {lose_count}, {draw_count} ({total})')
        print_separator()

    def commence_battle(
            self,
            turn_player: Turn = None,
            first_battle: bool = None
    ) -> BattleResult:
        if first_battle or not turn_player:
            turn_player = self.choose_turn_player(CoinToss.heads)

        # choose pokemon for user and opponent
        user_pokemon = self.draw_from_deck(self.player_cards)
        self.player_cards.append(user_pokemon)

        if len(self.deck) == 0:
            print('The neutral deck is empty! ', end='')

        print(f'You drew {blue(user_pokemon.name)} ', end='')

        if len(self.deck) > 0:
            print('from the neutral deck!')
        else:
            print('from your deck!')

        enemy_pokemon = self.draw_from_deck(self.opponent_cards)
        self.opponent_cards.append(enemy_pokemon)

        if turn_player == Turn.user:
            turn_player_chosen_stat = self.prompt_user_for_stat(user_pokemon)
        else:
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
            summary = "{}! Your {} and your opponent's {} both have {} {}.".format(
                yellow('DRAW'),
                blue(user_pokemon.name),
                red(enemy_pokemon.name),
                yellow(user_pokemon_stat),
                yellow(stat_name)
            )
        else:
            if result == BattleResult.win:
                self.wins += 1
                self.move_card(enemy_pokemon, Player.user)

                winner = 'Your'
                wining_pokemon = blue(user_pokemon.name)
                wining_stat = yellow(user_pokemon_stat)
                loser = 'enemy'
                loser_pokemon = red(enemy_pokemon.name)
                losing_stat = yellow(enemy_pokemon_stat)
                print('You {}! '.format(green('WIN')), end='')
            else:
                self.loses += 1
                self.move_card(user_pokemon, Player.opponent)
                winner = 'Enemy'
                wining_pokemon = red(enemy_pokemon.name)
                wining_stat = yellow(enemy_pokemon_stat)
                loser = 'your'
                loser_pokemon = blue(user_pokemon.name)
                losing_stat = yellow(user_pokemon_stat)
                print('You {}! '.format(red('LOSE')), end='')
            coloured_stat_name = yellow(stat_name)
            summary = f"{winner} {wining_pokemon}'s {wining_stat} {coloured_stat_name} beats "\
                      f"{loser} {loser_pokemon}'s {losing_stat} {coloured_stat_name}! "
        print(summary)
        if result == BattleResult.win:
            print("You get the opponent's {}!".format(red(enemy_pokemon.name)))
        elif result == BattleResult.lose:
            print('Your opponent gets your {}!'.format(blue(user_pokemon.name)))
        return result

    def announce_match_winner(self):
        if self.game_mode != GameMode.single_match:
            player_card_count = purple(len(self.player_cards))
            opponent_card_count = purple(len(self.opponent_cards))
            final_result = compare(len(self.player_cards), len(self.opponent_cards))

            print(f'You accumulated {player_card_count} cards and your opponent amassed {opponent_card_count} cards.')
            if final_result == BattleResult.win:
                print('Congratulations, you {} the match!'.format(green('WIN')))
            elif final_result == BattleResult.lose:
                print('Unfortunately, you {} the match...'.format(red('LOSE')))
            else:
                print('The match ends in a {}!'.format(yellow('DRAW')))
        self.show_final_score()

    def prompt_user_for_generation(self) -> int:
        return questionary.select(
            message='Choose a generation to pick Pokemon from:',
            choices=get_available_generations(),
            style=self.custom_styling,
            qmark='⭐'
        ).ask()


new_game = Game()
