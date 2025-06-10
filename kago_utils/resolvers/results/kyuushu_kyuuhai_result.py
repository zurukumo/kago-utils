from kago_utils.actions import KyuushuKyuuhai
from kago_utils.player import Player


class KyuushuKyuuhaiResult:
    player: Player
    action: KyuushuKyuuhai

    def __init__(self, player: Player, action: KyuushuKyuuhai):
        self.player = player
        self.action = action
