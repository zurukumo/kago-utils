from __future__ import annotations

from typing import Literal

from kago_utils.game import Game
from kago_utils.tehai import Tehai
from kago_utils.zaichi import Zaichi


class Player:
    game: Game
    tehai: Tehai
    zaseki: int

    is_riichi_completed: bool
    riichi_pc: int

    __slots__ = ("game", "tehai", "zaseki", "is_riichi_completed", "riichi_pc")

    @property
    def is_oya(self) -> bool:
        return self.zaseki == self.game.kyoku % 4

    @property
    def jikaze(self) -> Literal["東", "南", "西", "北"]:
        match (self.zaseki - self.game.kyoku) % 4:
            case 0:
                return "東"
            case 1:
                return "南"
            case 2:
                return "西"
            case 3:
                return "北"

        raise Exception()

    @property
    def pao_sekinin_player(self) -> Player | None:
        daisuushii_huuro = 0
        daisangen_huuro = 0
        for huuro in self.tehai.huuros:
            if huuro.hais[0].name in ("5z", "6z", "7z"):
                daisangen_huuro += 1
            if huuro.hais[0].name in ("1z", "2z", "3z", "4z"):
                daisuushii_huuro += 1

            if daisangen_huuro >= 3 or daisuushii_huuro >= 4:
                return self.find_player_by_zaichi(huuro.from_who)

        return None

    def find_player_by_zaichi(self, zaichi: Zaichi) -> Player:
        zaseki = (self.zaseki + zaichi.value) % 4
        return self.game.find_player_by_zaseki(zaseki)
