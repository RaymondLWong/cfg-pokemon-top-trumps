from enum import Enum
from typing import List


class ScoreboardType(Enum):
    single_match = 'single_match',
    traditional = 'traditional',
    deplete = 'deplete',


class Score:
    def __init__(self, player_name: str, score: int):
        self.player_name = player_name
        self.score = score


class Scoreboard:
    def __init__(
            self,
            name: ScoreboardType,
            scores: List[Score] = [],
            max_entries: int = 10,
            pvp: bool = False
    ):
        self.name = '{}{}'.format(name, '_pvp' if pvp else '')
        self.scores = scores
        self.max_entries = max_entries

    def add_score(self, score: Score):
        self.scores.append(score)
        self.scores.sort(
            key=lambda entry: entry.score,
            reverse=True  # highest score at top
        )
        self.scores = self.scores[:self.max_entries]
