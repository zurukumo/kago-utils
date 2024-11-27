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

    last_teban: int | None
    last_tsumo: Hai | None
    last_dahai: Hai | None

    pc: int

    __slots__ = (
        "players",
        "kyoku",
        "honba",
        "kyoutaku",
        "last_teban",
        "last_tsumo",
        "last_dahai",
        "pc",
    )

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
        match self.kyoku % 4:
            case 0:
                return "東"
            case 1:
                return "南"
            case 2:
                return "西"
            case 3:
                return "北"

        raise Exception()
