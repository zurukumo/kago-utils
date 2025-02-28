from kago_utils.actions import Pon
from kago_utils.player import Player


class PonResult:
    player: Player
    action: Pon

    def __init__(self, player: Player, action: Pon) -> None:
        self.player = player
        self.action = action
