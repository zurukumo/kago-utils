import random
from itertools import product

from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.huuro import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.zaichi import Zaichi


class Tehai:
    juntehai: HaiGroup
    huuros: list[Chii | Pon | Kakan | Daiminkan | Ankan]
    last_tsumo: Hai | None
    last_dahai: Hai | None

    __slots__ = ("juntehai", "huuros", "last_tsumo", "last_dahai")

    def __init__(self, juntehai: HaiGroup, huuros: list[Chii | Pon | Kakan | Daiminkan | Ankan] = []):
        self.juntehai = juntehai
        self.huuros = huuros

    @classmethod
    def validate_juntehai(cls, juntehai: HaiGroup) -> None:
        if any(not 0 <= v <= 1 for v in juntehai.to_counter()):
            raise ValueError(f"Invalid data: the count of each hai should be between 0 and 1. Data: {juntehai}")
        if len(juntehai) > 14:
            raise ValueError(f"Invalid data: the total count of hais should be 14 or less. Data: {juntehai}")
        if len(juntehai) % 3 == 0:
            raise ValueError(f"Invalid data: the total count of hais should be 3n+1 or 3n+2. Data: {juntehai}")

    def tsumo(self, hai: Hai) -> None:
        self.juntehai += hai
        self.last_tsumo = hai

    def dahai(self, hai: Hai) -> None:
        self.juntehai -= hai
        self.last_dahai = hai

    @property
    def is_menzen(self) -> bool:
        return not any(isinstance(huuro, (Chii, Pon, Kakan, Daiminkan)) for huuro in self.huuros)

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
