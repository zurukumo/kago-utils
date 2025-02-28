from kago_utils.actions import Chii
from kago_utils.player import Player


class ChiiResult:
    player: Player
    action: Chii

    def __init__(self, player: Player, action: Chii) -> None:
        self.player = player
        self.action = action
