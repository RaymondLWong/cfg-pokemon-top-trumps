import atexit
import sys

from src.gameplay.game import Game

game_instance = None

try:
    game_instance = Game()
except KeyboardInterrupt:
    sys.exit(0)


@atexit.register
def save_and_exit():
    print('saving...')
    game_instance.store.sync_and_close()
    if game_instance.battle_count > 0:
        game_instance.announce_match_winner()
