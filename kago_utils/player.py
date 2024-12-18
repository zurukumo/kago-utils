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
    ten: int

    juntehai: HaiGroup
    huuros: list[Chii | Pon | Kakan | Daiminkan | Ankan]
    last_tsumo: Hai | None
    last_dahai: Hai | None
    is_riichi_completed: bool
    is_right_after_riichi_called: bool
    is_right_after_chii_called: bool
    is_right_after_pon_called: bool

    __slots__ = (
        "id",
        "game",
        "zaseki",
        "ten",
        "juntehai",
        "huuros",
        "last_tsumo",
        "last_dahai",
        "is_riichi_completed",
        "is_right_after_riichi_called",
        "is_right_after_chii_called",
        "is_right_after_pon_called",
    )

    def __init__(self, id: str) -> None:
        self.id = id
        self.reset()

    def reset(self) -> None:
        self.juntehai = HaiGroup([])
        self.huuros = []
        self.last_tsumo = None
        self.last_dahai = None
        self.is_riichi_completed = False
        self.is_right_after_riichi_called = False
        self.is_right_after_chii_called = False
        self.is_right_after_pon_called = False

    def tsumo(self, hai: Hai) -> None:
        self.juntehai += hai
        self.last_tsumo = hai

    def riichi(self) -> None:
        self.is_right_after_riichi_called = True

    def dahai(self, hai: Hai) -> None:
        self.juntehai -= hai
        self.last_dahai = hai

    def chii(self, chii: Chii) -> None:
        self.huuros.append(chii)
        self.juntehai -= chii.hais - chii.stolen
        self.is_right_after_chii_called = True

    def pon(self, pon: Pon) -> None:
        self.huuros.append(pon)
        self.juntehai -= pon.hais - pon.stolen
        self.is_right_after_pon_called = True

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

    def list_riichi_candidates(self) -> bool:
        # Not menzen
        if not self.is_menzen:
            return False

        # Riichi completed
        if self.is_riichi_completed:
            return False

        # Right after calling riichi
        if self.is_right_after_riichi_called:
            return False

        # Not enough ten
        if self.ten < 1000:
            return False

        # Not enough yama
        if len(self.game.yama) < 4:
            return False

        # Not tenpai
        if Shanten(self.juntehai).shanten > 0:
            return False

        return True

    def list_dahai_candidates(self) -> HaiGroup:
        # Riichi completed
        if self.is_riichi_completed:
            if self.last_tsumo is None:
                raise Exception()

            return HaiGroup([self.last_tsumo])

        # Right after calling riichi
        elif self.is_right_after_riichi_called:
            candidates = HaiGroup([])
            for hai in self.juntehai:
                new_juntehai = self.juntehai - hai
                if Shanten(new_juntehai).shanten == 0:
                    candidates += hai
            return candidates

        # Right after calling chii or pon
        elif self.is_right_after_chii_called or self.is_right_after_pon_called:
            last_huuro = self.huuros[-1]
            if not isinstance(last_huuro, (Chii, Pon)):
                raise Exception()

            candidates = HaiGroup([])
            for hai in self.juntehai:
                if hai not in last_huuro.kuikae_hais:
                    candidates += hai
            return candidates

        else:
            return self.juntehai

    def list_chii_candidates(self) -> list[Chii]:
        # Not enoguh yama
        if len(self.game.yama) == 0:
            return []

        if self.game.last_dahai is None or self.game.last_teban is None:
            raise Exception()

        stolen = self.game.last_dahai

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

            chii = Chii(hais=HaiGroup([hai1, hai2, hai3]), stolen=stolen)

            # Pass if cannot dahai after chii
            kuikae_hais = self.juntehai & chii.kuikae_hais
            if len(self.juntehai) - 2 == len(kuikae_hais):
                continue

            candidates.append(chii)

        return candidates

    def list_pon_candidates(self) -> list[Pon]:
        # Not enough yama
        if len(self.game.yama) == 0:
            return []

        if self.game.last_dahai is None or self.game.last_teban is None:
            raise Exception()

        stolen = self.game.last_dahai
        from_who = self.get_zaichi_from_zaseki(self.game.last_teban)

        candidates = []
        b = []
        r = []
        # Shuffle juntehai to select b and r randomly.
        for hai in random.sample(self.juntehai, len(self.juntehai)):
            if hai.suit == stolen.suit and hai.number == stolen.number:
                if hai.color == "b":
                    b.append(hai)
                else:
                    r.append(hai)

        if len(b) >= 2:
            candidates.append(Pon(hais=HaiGroup([stolen, b[0], b[1]]), stolen=stolen, from_who=from_who))
        if len(b) >= 1 and len(r) >= 1:
            candidates.append(Pon(hais=HaiGroup([stolen, b[0], r[0]]), stolen=stolen, from_who=from_who))

        return candidates

    def list_kakan_candidates(self) -> list[Kakan]:
        # Not enough yama
        if len(self.game.yama) == 0:
            return []

        # Four kans exist
        n_kan = 0
        for player in self.game.players:
            for huuro in player.huuros:
                if isinstance(huuro, (Kakan, Daiminkan, Ankan)):
                    n_kan += 1
        if n_kan >= 4:
            return []

        candidates = []
        for huuro in self.huuros:
            if isinstance(huuro, Pon) and huuro.to_kakan().added in self.juntehai:
                candidates.append(huuro.to_kakan())

        return candidates

    def list_daiminkan_candidates(self) -> list[Daiminkan]:
        # Not enough yama
        if len(self.game.yama) == 0:
            return []

        # Four kans exist
        n_kan = 0
        for player in self.game.players:
            for huuro in player.huuros:
                if isinstance(huuro, (Kakan, Daiminkan, Ankan)):
                    n_kan += 1
        if n_kan >= 4:
            return []

        if self.game.last_dahai is None or self.game.last_teban is None:
            raise Exception()

        stolen = self.game.last_dahai
        from_who = self.get_zaichi_from_zaseki(self.game.last_teban)

        candidates = []
        hais = [hai for hai in self.juntehai if hai.suit == stolen.suit and hai.number == stolen.number]
        if len(hais) >= 3:
            candidates.append(Daiminkan(hais=HaiGroup(hais + [stolen]), stolen=stolen, from_who=from_who))

        return candidates

    def list_ankan_candidates(self) -> list[Ankan]:
        # Not enough yama
        if len(self.game.yama) == 0:
            return []

        # Four kans exist
        n_kan = 0
        for player in self.game.players:
            for huuro in player.huuros:
                if isinstance(huuro, (Kakan, Daiminkan, Ankan)):
                    n_kan += 1
        if n_kan >= 4:
            return []

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
            if huuro.hais[0].code in ("5z", "6z", "7z"):
                n_daisangen_huuro += 1
            if huuro.hais[0].code in ("1z", "2z", "3z", "4z"):
                n_daisuushii_huuro += 1

            if n_daisangen_huuro >= 3 or n_daisuushii_huuro >= 4:
                return self.find_player_by_zaichi(huuro.from_who)

        return None

    @property
    def is_menzen(self) -> bool:
        return not any(isinstance(huuro, (Chii, Pon, Kakan, Daiminkan)) for huuro in self.huuros)

    #######################
    ### Utility methods ###
    #######################

    def find_player_by_zaichi(self, zaichi: Zaichi) -> Player:
        zaseki = (self.zaseki + zaichi.value) % 4
        return self.game.find_player_by_zaseki(zaseki)

    def get_zaichi_from_zaseki(self, zaseki: int) -> Zaichi:
        return Zaichi((zaseki - self.zaseki) % 4)

    def get_zaseki_from_zaichi(self, zaichi: Zaichi) -> int:
        return (self.zaseki + zaichi.value) % 4
