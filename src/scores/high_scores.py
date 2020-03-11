from enum import Enum
from typing import List


class StrEnum(str, Enum):
    pass


class ScoreboardType(StrEnum):
    single_match = 'single_match',
    traditional = 'traditional',
    deplete = 'deplete'

    def __str__(self):
        return str(self.value)


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
        self.name = get_scoreboard_name(name, pvp)
        self.scores = scores
        self.max_entries = max_entries

    def add_score(self, score: Score) -> bool:
        """Returns True if score is placed onto scoreboard"""
        self.scores.append(score)
        self.scores.sort(
            key=lambda entry: entry.score,
            reverse=True  # highest score at top
        )
        self.scores = self.scores[:self.max_entries]
        return score.player_name in [entry.player_name for entry in self.scores]


def get_scoreboard_name(scoreboard_type: ScoreboardType, pvp: bool) -> str:
    return '{}{}'.format(scoreboard_type.value, '_pvp' if pvp else '')
