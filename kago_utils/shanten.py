import gzip
import os
import pickle
from typing import cast

from kago_utils.hai import (Hai, Hai34, Hai34List, Hai34String, Hai136,
                            Hai136List)


class Shanten[T: Hai]:
    suuhai_distance_table: dict[tuple[tuple[int, ...], int], int] | None = None
    zihai_distance_table: dict[tuple[tuple[int, ...], int], int] | None = None

    __slots__ = ('jun_tehai',
                 '_shanten', '_regular_shanten', '_chiitoitsu_shanten', '_kokushimusou_shanten',
                 '_yuukouhai')

    jun_tehai: T
    _shanten: int | None
    _regular_shanten: int | None
    _chiitoitsu_shanten: int | None
    _kokushimusou_shanten: int | None
    _yuukouhai: T | None

    def __init__(self, jun_tehai: T) -> None:
        jun_tehai.validate_as_jun_tehai()

        self.jun_tehai = jun_tehai
        self._shanten = None
        self._regular_shanten = None
        self._chiitoitsu_shanten = None
        self._kokushimusou_shanten = None
        self._yuukouhai = None

    @property
    def shanten(self) -> int:
        if self._shanten is None:
            self._shanten = self.__calculate_shanten()
        return self._shanten

    @property
    def regular_shanten(self) -> int:
        if self._regular_shanten is None:
            self._regular_shanten = self.__calculate_regular_shanten()
        return self._regular_shanten

    @property
    def chiitoitsu_shanten(self) -> int | None:
        if self._chiitoitsu_shanten is None:
            self._chiitoitsu_shanten = self.__calculate_chiitoitsu_shanten()
        return self._chiitoitsu_shanten

    @property
    def kokushimusou_shanten(self) -> int | None:
        if self._kokushimusou_shanten is None:
            self._kokushimusou_shanten = self.__calculate_kokushimusou_shanten()
        return self._kokushimusou_shanten

    @property
    def yuukouhai(self) -> T:
        if self._yuukouhai is None:
            self._yuukouhai = self.__calculate_yuukouhai()
        return self._yuukouhai

    @classmethod
    def load_patterns(cls) -> None:
        if cls.suuhai_distance_table is None or cls.zihai_distance_table is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            suuhai_distance_table_path = os.path.join(current_dir, 'data/suuhai_distance_table.pickle.gz')
            zihai_distance_table_path = os.path.join(current_dir, 'data/zihai_distance_table.pickle.gz')

            with gzip.open(suuhai_distance_table_path, 'rb') as f:
                cls.suuhai_distance_table = pickle.load(f)
            with gzip.open(zihai_distance_table_path, 'rb') as f:
                cls.zihai_distance_table = pickle.load(f)

    def __calculate_shanten(self) -> int:
        shanten = self.regular_shanten
        if self.chiitoitsu_shanten is not None:
            shanten = min(shanten, self.chiitoitsu_shanten)
        if self.kokushimusou_shanten is not None:
            shanten = min(shanten, self.kokushimusou_shanten)
        return shanten

    def __calculate_regular_shanten(self) -> int:
        Shanten.load_patterns()
        if Shanten.suuhai_distance_table is None or Shanten.zihai_distance_table is None:
            raise RuntimeError('Patterns are not loaded')

        jun_tehai = self.jun_tehai.to_hai34_counter()

        manzu = tuple(jun_tehai.data[0:9])
        pinzu = tuple(jun_tehai.data[9:18])
        souzu = tuple(jun_tehai.data[18:27])
        zihai = tuple(jun_tehai.data[27:34])

        min_shanten = 8
        n_huuro = (14 - sum(jun_tehai.data)) // 3
        n_hai = 12 - n_huuro * 3
        for n_manzu in range(0, n_hai + 1, 3):
            for n_pinzu in range(0, n_hai + 1 - n_manzu, 3):
                for n_souzu in range(0, n_hai + 1 - n_manzu - n_pinzu, 3):
                    n_zihai = n_hai - n_manzu - n_pinzu - n_souzu
                    for jantou_suit in range(4):
                        m = Shanten.suuhai_distance_table[(manzu, n_manzu + (2 if jantou_suit == 0 else 0))]
                        p = Shanten.suuhai_distance_table[(pinzu, n_pinzu + (2 if jantou_suit == 1 else 0))]
                        s = Shanten.suuhai_distance_table[(souzu, n_souzu + (2 if jantou_suit == 2 else 0))]
                        z = Shanten.zihai_distance_table[(zihai, n_zihai + (2 if jantou_suit == 3 else 0))]
                        min_shanten = min(min_shanten, m + p + s + z - 1)

        return min_shanten

    def __calculate_chiitoitsu_shanten(self) -> int | None:
        jun_tehai = self.jun_tehai.to_hai34_counter()

        if not 13 <= sum(jun_tehai.data) <= 14:
            return None

        n_toitsu = 0
        n_unique_hai = 0

        for i in range(34):
            if jun_tehai.data[i] >= 2:
                n_toitsu += 1
            if jun_tehai.data[i] >= 1:
                n_unique_hai += 1

        return 6 - n_toitsu + (7 - n_unique_hai if n_unique_hai < 7 else 0)

    def __calculate_kokushimusou_shanten(self) -> int | None:
        jun_tehai = self.jun_tehai.to_hai34_counter()

        if not 13 <= sum(jun_tehai.data) <= 14:
            return None

        n_yaochu_hai = 0
        has_toitsu = False
        yaochu_hai = Hai34String('19m19p19s1234567z').to_hai34_list()

        for i in yaochu_hai.data:
            if jun_tehai.data[i] >= 1:
                n_yaochu_hai += 1
            if jun_tehai.data[i] >= 2:
                has_toitsu = True

        return 13 - n_yaochu_hai - (1 if has_toitsu else 0)

    def __calculate_yuukouhai(self) -> T:
        if sum(self.jun_tehai.to_hai34_counter().data) % 3 != 1:
            raise ValueError(
                f"Invalid data: the total count of hais should be 3n+1. Data: {self.jun_tehai.__repr__()}")

        if isinstance(self.jun_tehai, Hai34):
            return self.__calculate_yuukouhai_for_hai34()
        elif isinstance(self.jun_tehai, Hai136):
            return self.__calculate_yuukouhai_for_hai136()

        raise TypeError(f"jun_tehai should be Hai34 or Hai136, but {self.jun_tehai.__class__.__name__}")

    def __calculate_yuukouhai_for_hai34(self) -> T:
        if not isinstance(self.jun_tehai, Hai34):
            raise ValueError(f"Invalid data: {self.jun_tehai.__repr__()}")

        current_shanten = self.shanten
        jun_tehai_counter = self.jun_tehai.to_hai34_counter()

        yuukouhai = []
        for i in range(34):
            if jun_tehai_counter.data[i] >= 4:
                continue
            jun_tehai_counter.data[i] += 1
            if Shanten(jun_tehai_counter).shanten < current_shanten:
                yuukouhai.append(i)
            jun_tehai_counter.data[i] -= 1

        return cast(T, self.jun_tehai.__class__.from_hai34(Hai34List(yuukouhai)))

    def __calculate_yuukouhai_for_hai136(self) -> T:
        if not isinstance(self.jun_tehai, Hai136):
            raise ValueError(f"Invalid data: {self.jun_tehai.__repr__()}")

        current_shanten = self.shanten
        jun_tehai34_counter = self.jun_tehai.to_hai34_counter()
        jun_tehai136_counter = self.jun_tehai.to_hai136_counter()

        yuukouhai = []
        for i in range(34):
            if jun_tehai34_counter.data[i] >= 4:
                continue
            jun_tehai34_counter.data[i] += 1
            if Shanten(jun_tehai34_counter).shanten < current_shanten:
                for j in range(4):
                    if jun_tehai136_counter.data[i * 4 + j] == 0:
                        yuukouhai.append(i * 4 + j)
            jun_tehai34_counter.data[i] -= 1

        return cast(T, self.jun_tehai.__class__.from_hai136(Hai136List(yuukouhai)))
