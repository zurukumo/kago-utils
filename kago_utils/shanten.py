from __future__ import annotations

import gzip
import os
import pickle

from kago_utils.hai_group import HaiGroup


class Shanten:
    suuhai_distance_table: dict[tuple[tuple[int, ...], int], int] | None = None
    zihai_distance_table: dict[tuple[tuple[int, ...], int], int] | None = None

    __slots__ = (
        "__juntehai",
        "__shanten",
        "__regular_shanten",
        "__chiitoitsu_shanten",
        "__kokushimusou_shanten",
        "__yuukouhai",
    )

    __juntehai: HaiGroup
    __shanten: int | None
    __regular_shanten: int | None
    __chiitoitsu_shanten: int | None
    __kokushimusou_shanten: int | None
    __yuukouhai: HaiGroup | None

    def __init__(self, juntehai: HaiGroup) -> None:
        Shanten.validate_juntehai(juntehai)

        self.__juntehai = juntehai
        self.__shanten = None
        self.__regular_shanten = None
        self.__chiitoitsu_shanten = None
        self.__kokushimusou_shanten = None
        self.__yuukouhai = None

    @classmethod
    def validate_juntehai(cls, juntehai: HaiGroup) -> None:
        if any(not 0 <= v <= 1 for v in juntehai.to_counter()):
            raise ValueError(f"Invalid data: the count of each hai should be between 0 and 1. Data: {juntehai}")
        if len(juntehai) > 14:
            raise ValueError(f"Invalid data: the total count of hais should be 14 or less. Data: {juntehai}")
        if len(juntehai) % 3 == 0:
            raise ValueError(f"Invalid data: the total count of hais should be 3n+1 or 3n+2. Data: {juntehai}")

    @property
    def shanten(self) -> int:
        if self.__shanten is None:
            self.__shanten = self.__calculate_shanten()
        return self.__shanten

    @property
    def regular_shanten(self) -> int:
        if self.__regular_shanten is None:
            self.__regular_shanten = self.__calculate__regular_shanten()
        return self.__regular_shanten

    @property
    def chiitoitsu_shanten(self) -> int | None:
        if self.__chiitoitsu_shanten is None:
            self.__chiitoitsu_shanten = self.__calculate__chiitoitsu_shanten()
        return self.__chiitoitsu_shanten

    @property
    def kokushimusou_shanten(self) -> int | None:
        if self.__kokushimusou_shanten is None:
            self.__kokushimusou_shanten = self.__calculate__kokushimusou_shanten()
        return self.__kokushimusou_shanten

    @property
    def yuukouhai(self) -> HaiGroup:
        if self.__yuukouhai is None:
            self.__yuukouhai = self.__calculate_yuukouhai()
        return self.__yuukouhai

    @classmethod
    def __load_patterns(cls) -> None:
        if cls.suuhai_distance_table is None or cls.zihai_distance_table is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            suuhai_distance_table_path = os.path.join(current_dir, "data/suuhai_distance_table.pickle.gz")
            zihai_distance_table_path = os.path.join(current_dir, "data/zihai_distance_table.pickle.gz")

            with gzip.open(suuhai_distance_table_path, "rb") as f:
                cls.suuhai_distance_table = pickle.load(f)
            with gzip.open(zihai_distance_table_path, "rb") as f:
                cls.zihai_distance_table = pickle.load(f)

    @staticmethod
    def __divide_into_four(n: int) -> list[tuple[int, int, int, int]]:
        ret = []
        for a in range(n + 1):
            for b in range(n - a + 1):
                for c in range(n - a - b + 1):
                    d = n - a - b - c
                    ret.append((a, b, c, d))
        return ret

    def __calculate_shanten(self) -> int:
        shanten = self.regular_shanten
        if self.chiitoitsu_shanten is not None:
            shanten = min(shanten, self.chiitoitsu_shanten)
        if self.kokushimusou_shanten is not None:
            shanten = min(shanten, self.kokushimusou_shanten)
        return shanten

    def __calculate__regular_shanten(self) -> int:
        Shanten.__load_patterns()
        if Shanten.suuhai_distance_table is None or Shanten.zihai_distance_table is None:
            raise RuntimeError("Patterns are not loaded")

        juntehai_counter = self.__juntehai.to_counter34()

        manzu = tuple(juntehai_counter[0:9])
        pinzu = tuple(juntehai_counter[9:18])
        souzu = tuple(juntehai_counter[18:27])
        zihai = tuple(juntehai_counter[27:34])

        min_shanten = 8
        n_menstu = sum(juntehai_counter) // 3
        for n_manzu_mentsu, n_pinzu_mentsu, n_souzu_mentsu, n_zihai_mentsu in self.__divide_into_four(n_menstu):
            for n_manzu_jantou, n_pinzu_jantou, n_souzu_jantou, n_zihai_jantou in self.__divide_into_four(1):
                n_manzu = n_manzu_mentsu * 3 + n_manzu_jantou * 2
                n_pinzu = n_pinzu_mentsu * 3 + n_pinzu_jantou * 2
                n_souzu = n_souzu_mentsu * 3 + n_souzu_jantou * 2
                n_zihai = n_zihai_mentsu * 3 + n_zihai_jantou * 2

                manzu_distance = Shanten.suuhai_distance_table[(manzu, n_manzu)]
                pinzu_distance = Shanten.suuhai_distance_table[(pinzu, n_pinzu)]
                souzu_distance = Shanten.suuhai_distance_table[(souzu, n_souzu)]
                zihai_distance = Shanten.zihai_distance_table[(zihai, n_zihai)]

                min_shanten = min(min_shanten, manzu_distance + pinzu_distance + souzu_distance + zihai_distance - 1)

        return min_shanten

    def __calculate__chiitoitsu_shanten(self) -> int | None:
        juntehai_counter = self.__juntehai.to_counter34()

        if not 13 <= sum(juntehai_counter) <= 14:
            return None

        n_toitsu = 0
        n_unique_hai = 0

        for i in range(34):
            if juntehai_counter[i] >= 2:
                n_toitsu += 1
            if juntehai_counter[i] >= 1:
                n_unique_hai += 1

        return 6 - n_toitsu + (7 - n_unique_hai if n_unique_hai < 7 else 0)

    def __calculate__kokushimusou_shanten(self) -> int | None:
        juntehai_counter = self.__juntehai.to_counter34()

        if not 13 <= sum(juntehai_counter) <= 14:
            return None

        n_yaochu_hai = 0
        has_toitsu = False
        yaochu_hai_list = HaiGroup.from_code("19m19p19s1234567z").to_list34()

        for i in yaochu_hai_list:
            if juntehai_counter[i] >= 1:
                n_yaochu_hai += 1
            if juntehai_counter[i] >= 2:
                has_toitsu = True

        return 13 - n_yaochu_hai - (1 if has_toitsu else 0)

    def __calculate_yuukouhai(self) -> HaiGroup:
        if not isinstance(self.__juntehai, HaiGroup):
            raise TypeError(f"juntehai should be HaiGroup, but {self.__juntehai.__class__.__name__}")

        if len(self.__juntehai) % 3 != 1:
            raise ValueError(
                f"Invalid data: HaiGroup's total count of hais should be 3n+1. Data: {self.__juntehai.__repr__()}"
            )

        current_shanten = self.shanten

        yuukouhai = []
        for i in range(136):
            new_juntehai = self.__juntehai + HaiGroup.from_list([i])
            try:
                new_shanten = Shanten(new_juntehai).shanten
                if new_shanten < current_shanten:
                    yuukouhai.append(i)
            except ValueError:
                pass

        return self.__juntehai.__class__.from_list(yuukouhai)
