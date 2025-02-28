from kago_utils.actions import Kakan
from kago_utils.player import Player


class KakanResult:
    player: Player
    action: Kakan

    def __init__(self, player: Player, action: Kakan) -> None:
        self.player = player
        self.action = action
