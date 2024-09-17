import os
import pickle
from typing import TypeVar

from kago_utils.hai import Hai, Hai34Counter, Hai34List, Hai34String

H = TypeVar('H', Hai34Counter, Hai34List, Hai34String)


class Shanten:
    suuhai_patterns: dict[tuple[tuple[int, ...], int], int] | None = None
    zihai_patterns: dict[tuple[tuple[int, ...], int], int] | None = None

    @classmethod
    def load_patterns(cls) -> None:
        if cls.suuhai_patterns is None or cls.zihai_patterns is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            suuhai_patterns_path = os.path.join(current_dir, 'data/suuhai_shanten.pickle')
            zihai_patterns_path = os.path.join(current_dir, 'data/zihai_shanten.pickle')

            with open(suuhai_patterns_path, 'rb') as f:
                cls.suuhai_patterns = pickle.load(f)
            with open(zihai_patterns_path, 'rb') as f:
                cls.zihai_patterns = pickle.load(f)

    @staticmethod
    def calculate_shanten(jun_tehai: Hai) -> int:
        shantens = (
            Shanten.calculate_shanten_for_regular(jun_tehai),
            Shanten.calculate_shanten_for_chiitoitsu(jun_tehai),
            Shanten.calculate_shanten_for_kokushimusou(jun_tehai)
        )
        return min(shanten for shanten in shantens if shanten is not None)

    @classmethod
    def calculate_shanten_for_regular(cls, jun_tehai: Hai) -> int:
        cls.load_patterns()
        if cls.suuhai_patterns is None or cls.zihai_patterns is None:
            raise RuntimeError('Patterns are not loaded')

        jun_tehai = jun_tehai.to_hai34_counter()

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
                        m = cls.suuhai_patterns[(manzu, n_manzu + (2 if jantou_suit == 0 else 0))]
                        p = cls.suuhai_patterns[(pinzu, n_pinzu + (2 if jantou_suit == 1 else 0))]
                        s = cls.suuhai_patterns[(souzu, n_souzu + (2 if jantou_suit == 2 else 0))]
                        z = cls.zihai_patterns[(zihai, n_zihai + (2 if jantou_suit == 3 else 0))]
                        min_shanten = min(min_shanten, m + p + s + z - 1)

        return min_shanten

    @staticmethod
    def calculate_shanten_for_chiitoitsu(jun_tehai: Hai) -> int | None:
        jun_tehai = jun_tehai.to_hai34_counter()

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

    @staticmethod
    def calculate_shanten_for_kokushimusou(jun_tehai: Hai) -> int | None:
        jun_tehai = jun_tehai.to_hai34_counter()

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

    @staticmethod
    def calculate_yuukouhai(jun_tehai: H) -> H:
        current_shanten = Shanten.calculate_shanten(jun_tehai)
        jun_tehai_counter = jun_tehai.to_hai34_counter()

        yuukouhai = []
        for i in range(34):
            if jun_tehai_counter.data[i] >= 4:
                continue
            jun_tehai_counter.data[i] += 1
            if Shanten.calculate_shanten(jun_tehai_counter) < current_shanten:
                yuukouhai.append(i)
            jun_tehai_counter.data[i] -= 1

        return jun_tehai.__class__.from_hai34(Hai34List(yuukouhai))
