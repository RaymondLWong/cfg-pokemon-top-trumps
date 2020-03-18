from enum import auto, IntEnum
from typing import TypedDict

from src.gameplay.game import GameMode

DEFAULT_PORT = 8765


class PayloadType(IntEnum):
    challenge_request = auto()
    player_move = auto()
    sync_score = auto()
    end_game = auto()


class WebocketRequest:
    request_type: PayloadType
    payload: dict


class ChallengeRequest(WebocketRequest):
    request_type = PayloadType.challenge_request
    payload: GameMode


class PlayerAction(TypedDict):
    player_id: int


class CardStat(TypedDict, PlayerAction):
    card_stat: str


class PlayerMove(WebocketRequest):
    request_type = PayloadType.player_move
    payload: CardStat


class PlayerScore(TypedDict, PlayerAction):
    score: int


class SyncScore(WebocketRequest):
    request_type = PayloadType.sync_score
    payload: PlayerScore


class EndGame(WebocketRequest):
    request_type = PayloadType.end_game
    payload: PlayerAction


class ServerRequest(
    WebocketRequest,
    ChallengeRequest,
    PlayerMove,
    SyncScore,
    EndGame
):
    pass
