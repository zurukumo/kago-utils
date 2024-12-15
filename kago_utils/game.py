from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from kago_utils.hai import Hai

if TYPE_CHECKING:
    from kago_utils.player import Player


class Game:
    players: list[Player]

    kyoku: int
    honba: int
    kyoutaku: int

    teban: int
    last_teban: int | None
    last_dahai: Hai | None

    yama: list[Hai]

    __slots__ = ("players", "kyoku", "honba", "kyoutaku", "teban", "last_teban", "last_dahai", "yama")

    def __init__(self) -> None:
        self.players = []

    def add_player(self, player: Player) -> None:
        player.game = self
        player.zaseki = len(self.players)
        self.players.append(player)

    def find_player_by_zaseki(self, zaseki: int) -> Player:
        return self.players[zaseki]

    @property
    def bakaze(self) -> Literal["東", "南", "西", "北"]:
        match self.kyoku // 4:
            case 0:
                return "東"
            case 1:
                return "南"
            case 2:
                return "西"
            case 3:
                return "北"

        raise Exception()
