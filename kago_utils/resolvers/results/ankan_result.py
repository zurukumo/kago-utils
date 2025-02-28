from kago_utils.actions import Ankan
from kago_utils.player import Player


class AnkanResult:
    player: Player
    action: Ankan

    def __init__(self, player: Player, action: Ankan) -> None:
        self.player = player
        self.action = action
