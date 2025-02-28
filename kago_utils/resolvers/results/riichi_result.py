from kago_utils.actions import Riichi
from kago_utils.player import Player


class RiichiResult:
    player: Player
    action: Riichi

    def __init__(self, player: Player, action: Riichi) -> None:
        self.player = player
        self.action = action
