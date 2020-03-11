import shelve
from src.scores.high_scores import ScoreboardType, Score, Scoreboard, get_scoreboard_name


class Store:
    filename = 'scoreboards'
    store = shelve.open(filename, writeback=True)

    def submit_score(self, scoreboard_type: ScoreboardType, pvp: bool, score: Score) -> bool:
        scoreboard_name = get_scoreboard_name(scoreboard_type, pvp)
        if scoreboard_name in self.store:
            scoreboard = self.store.get(scoreboard_name)
        else:
            scoreboard = Scoreboard(scoreboard_type)
        return scoreboard.add_score(score)

    def get_scoreboard(self, scoreboard_type: ScoreboardType, pvp: bool) -> Scoreboard:
        scoreboard_name = get_scoreboard_name(scoreboard_type, pvp)
        return self.store[scoreboard_name]

    def sync(self):
        if self.store:
            self.store.close()
