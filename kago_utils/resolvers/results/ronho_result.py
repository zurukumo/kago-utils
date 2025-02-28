from kago_utils.actions import Ronho
from kago_utils.player import Player


class RonhoResult:
    actions: list[tuple[Player, Ronho]]

    def __init__(self, actions: list[tuple[Player, Ronho]]) -> None:
        self.actions = actions
