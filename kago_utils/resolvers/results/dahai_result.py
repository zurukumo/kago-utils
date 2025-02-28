from kago_utils.actions import Dahai
from kago_utils.player import Player


class DahaiResult:
    player: Player
    action: Dahai

    def __init__(self, player: Player, action: Dahai) -> None:
        self.player = player
        self.action = action
