import sys

from src.gameplay.game import Game

game_instance = None
try:
    game_instance = Game()
except KeyboardInterrupt:
    game_instance.high_scores.sync()
    if game_instance.battle_count > 0:
        game_instance.announce_match_winner()
    sys.exit(0)
