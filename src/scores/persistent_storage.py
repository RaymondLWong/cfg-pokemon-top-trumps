import shelve
from typing import Union
from src.scores.high_scores import ScoreboardType, Score, Scoreboard, get_scoreboard_name, Scoreboards


class Settings:
    player_name: str


SettingsStore = Union[Settings, shelve.DbfilenameShelf]
ScoreboardStore = Union[Scoreboards, shelve.DbfilenameShelf]


class Store:
    settings: SettingsStore = shelve.open('settings', writeback=True)
    high_scores: ScoreboardStore = shelve.open('scoreboards', writeback=True)

    def __init__(self):
        if 'player_name' not in self.settings:
            self.settings['player_name'] = 'unknown'

    def player_name_set(self) -> bool:
        return self.settings['player_name'] != 'unknown'

    def submit_score(self, scoreboard_type: ScoreboardType, pvp: bool, score: Score) -> bool:
        scoreboard_name = get_scoreboard_name(scoreboard_type, pvp)
        if scoreboard_name in self.high_scores:
            scoreboard = self.high_scores.get(scoreboard_name)
        else:
            scoreboard = Scoreboard(scoreboard_type)
            self.high_scores[scoreboard_name] = scoreboard
        new_score = scoreboard.add_score(score)
        self.sync()
        return new_score

    def get_scoreboard(self, scoreboard_type: ScoreboardType, pvp: bool) -> Scoreboard:
        scoreboard_name = get_scoreboard_name(scoreboard_type, pvp)
        return self.high_scores[scoreboard_name]

    def sync(self):
        self.high_scores.sync()
        self.settings.sync()

    def sync_and_close(self):
        self.high_scores.close()
        self.settings.close()

    def set_player_name(self, player_name: str):
        self.settings['player_name'] = player_name
