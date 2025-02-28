from kago_utils.actions import Tsumoho
from kago_utils.player import Player


class TsumohoResult:
    player: Player
    action: Tsumoho

    def __init__(self, player: Player, action: Tsumoho) -> None:
        self.player = player
        self.action = action
