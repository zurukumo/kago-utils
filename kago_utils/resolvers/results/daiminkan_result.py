from kago_utils.actions import Daiminkan
from kago_utils.player import Player


class DaiminkanResult:
    player: Player
    action: Daiminkan

    def __init__(self, player: Player, action: Daiminkan) -> None:
        self.player = player
        self.action = action
