from __future__ import annotations

import random
from itertools import product
from typing import Literal

from kago_utils.game import Game
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.huuro import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.shanten import Shanten
from kago_utils.zaichi import Zaichi


class Player:
    id: str
    game: Game
    zaseki: int

    juntehai: HaiGroup
    huuros: list[Chii | Pon | Kakan | Daiminkan | Ankan]
    last_tsumo: Hai | None
    last_dahai: Hai | None

    __slots__ = (
        "id",
        "game",
        "zaseki",
        "juntehai",
        "huuros",
        "last_tsumo",
        "last_dahai",
    )

    def __init__(self, id: str) -> None:
        self.id = id
        self.reset()

    def reset(self) -> None:
        self.juntehai = HaiGroup([])
        self.huuros = []

    def tsumo(self, hai: Hai) -> None:
        self.juntehai += hai
        self.last_tsumo = hai

    def dahai(self, hai: Hai) -> None:
        self.juntehai -= hai
        self.last_dahai = hai

    def chii(self, chii: Chii) -> None:
        self.huuros.append(chii)
        self.juntehai -= chii.hais - chii.stolen

    def pon(self, pon: Pon) -> None:
        self.huuros.append(pon)
        self.juntehai -= pon.hais - pon.stolen

    def kakan(self, kakan: Kakan) -> None:
        for i, huuro in enumerate(self.huuros):
            if isinstance(huuro, Pon) and huuro.can_become_kakan(kakan):
                self.huuros[i] = kakan
                self.juntehai -= kakan.added
                return

        raise ValueError(f"Invalid data: there is no pon that can become given kakan. Data: {kakan}")

    def daiminkan(self, daiminkan: Daiminkan) -> None:
        self.huuros.append(daiminkan)
        self.juntehai -= daiminkan.hais - daiminkan.stolen

    def ankan(self, ankan: Ankan) -> None:
        self.huuros.append(ankan)
        self.juntehai -= ankan.hais

    def list_chii_candidates(self, stolen: Hai) -> list[Chii]:
        prev2: dict[str, Hai | None] = {"b": None, "r": None}
        prev1: dict[str, Hai | None] = {"b": None, "r": None}
        next1: dict[str, Hai | None] = {"b": None, "r": None}
        next2: dict[str, Hai | None] = {"b": None, "r": None}
        # Shuffle juntehai to select prev2, prev1, next1, and next2 randomly.
        for hai in random.sample(self.juntehai, len(self.juntehai)):
            if hai.suit == "z" or hai.suit != stolen.suit:
                continue

            if hai.number == stolen.number - 2:
                prev2[hai.color] = hai
            if hai.number == stolen.number - 1:
                prev1[hai.color] = hai
            if hai.number == stolen.number + 1:
                next1[hai.color] = hai
            if hai.number == stolen.number + 2:
                next2[hai.color] = hai

        candidates = []
        pattern1 = list(product(prev2.values(), prev1.values(), [stolen]))
        pattern2 = list(product(prev1.values(), [stolen], next1.values()))
        pattern3 = list(product([stolen], next1.values(), next2.values()))
        for hai1, hai2, hai3 in pattern1 + pattern2 + pattern3:
            if hai1 is None or hai2 is None or hai3 is None:
                continue
            candidates.append(Chii(hais=HaiGroup([hai1, hai2, hai3]), stolen=stolen))

        return candidates

    def list_pon_candidates(self, stolen: Hai, from_who: Zaichi) -> list[Pon]:
        candidates = []
        b = []
        r = []
        # Shuffle juntehai to select b and r randomly.
        for hai in random.sample(self.juntehai, len(self.juntehai)):
            if hai.name == stolen.name:
                if hai.color == "b":
                    b.append(hai)
                else:
                    r.append(hai)

        if len(b) >= 2:
            candidates.append(Pon(hais=HaiGroup([stolen, b[0], b[1]]), stolen=stolen, from_who=from_who))
        if len(b) >= 1 and len(r) >= 1:
            candidates.append(Pon(hais=HaiGroup([stolen, b[0], r[0]]), stolen=stolen, from_who=from_who))

        return candidates

    def list_kakan_candidates(self, added: Hai) -> list[Kakan]:
        candidates = []
        for huuro in self.huuros:
            if isinstance(huuro, Pon) and huuro.hais[0].name == added.name:
                candidates.append(huuro.to_kakan())

        return candidates

    def list_daiminkan_candidates(self, stolen: Hai, from_who: Zaichi) -> list[Daiminkan]:
        candidates = []
        hais = [hai for hai in self.juntehai if hai.name == stolen.name]
        if len(hais) >= 3:
            candidates.append(Daiminkan(hais=HaiGroup(hais + [stolen]), stolen=stolen, from_who=from_who))

        return candidates

    def list_ankan_candidates(self) -> list[Ankan]:
        candidates = []
        counter = self.juntehai.to_counter34()
        for i in range(34):
            if counter[i] >= 4:
                base_id = i * 4
                candidates.append(Ankan(hais=HaiGroup.from_list([base_id, base_id + 1, base_id + 2, base_id + 3])))

        return candidates

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
        n_daisuushii_huuro = 0
        n_daisangen_huuro = 0
        for huuro in self.huuros:
            if huuro.hais[0].name in ("5z", "6z", "7z"):
                n_daisangen_huuro += 1
            if huuro.hais[0].name in ("1z", "2z", "3z", "4z"):
                n_daisuushii_huuro += 1

            if n_daisangen_huuro >= 3 or n_daisuushii_huuro >= 4:
                return self.find_player_by_zaichi(huuro.from_who)

        return None

    @property
    def is_menzen(self) -> bool:
        return not any(isinstance(huuro, (Chii, Pon, Kakan, Daiminkan)) for huuro in self.huuros)

    # Utils
    def find_player_by_zaichi(self, zaichi: Zaichi) -> Player:
        zaseki = (self.zaseki + zaichi.value) % 4
        return self.game.find_player_by_zaseki(zaseki)
