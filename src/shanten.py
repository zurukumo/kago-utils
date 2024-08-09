import itertools
import os
import pickle

from src.hai import Hai34, Hai34List, Hai34String


class Shanten:
    suuhai_patterns: dict = None
    zihai_patterns: dict = None

    @classmethod
    def load_patterns(cls):
        if cls.suuhai_patterns is None or cls.zihai_patterns is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            suuhai_patterns_path = os.path.join(current_dir, '../data/suuhai_patterns.pickle')
            zihai_patterns_path = os.path.join(current_dir, '../data/zihai_patterns.pickle')

            with open(suuhai_patterns_path, 'rb') as f:
                cls.suuhai_patterns = pickle.load(f)
            with open(zihai_patterns_path, 'rb') as f:
                cls.zihai_patterns = pickle.load(f)

    @staticmethod
    def calculate_shanten(jun_tehai: Hai34, n_huuro: int):
        shantens = (
            Shanten.calculate_shanten_for_regular(jun_tehai, n_huuro),
            Shanten.calculate_shanten_for_chiitoitsu(jun_tehai),
            Shanten.calculate_shanten_for_kokushimusou(jun_tehai)
        )
        return min(shanten for shanten in shantens if shanten is not None)

    @staticmethod
    def calculate_shanten_for_regular(jun_tehai: Hai34, n_huuro: int):
        jun_tehai = jun_tehai.to_hai34_counter()

        shanten = Shanten.__calculate_tmp_shanten_for_regular(jun_tehai, n_huuro)

        # waiting for 5th hai is not allowed
        if shanten == 0 and sum(jun_tehai.data) % 3 == 1:
            for i in range(34):
                if jun_tehai.data[i] == 4:
                    continue

                if Shanten.__calculate_tmp_shanten_for_regular(jun_tehai + Hai34List([i]), n_huuro) == -1:
                    return 0

            return 1

        return shanten

    @classmethod
    def __calculate_tmp_shanten_for_regular(cls, jun_tehai: Hai34, n_huuro: int):
        cls.load_patterns()

        jun_tehai = jun_tehai.to_hai34_counter()

        m_patterns = cls.suuhai_patterns.get(tuple(jun_tehai.data[0:9]))
        p_patterns = cls.suuhai_patterns.get(tuple(jun_tehai.data[9:18]))
        s_patterns = cls.suuhai_patterns.get(tuple(jun_tehai.data[18:27]))
        z_patterns = cls.zihai_patterns.get(tuple(jun_tehai.data[27:34]))

        min_shanten = 8
        for m, p, s, z in itertools.product(m_patterns, p_patterns, s_patterns, z_patterns):
            n_mentsu = m[0] + p[0] + s[0] + z[0] + n_huuro
            n_pre_mentsu = m[1] + p[1] + s[1] + z[1]
            has_toitsu = m[2] or p[2] or s[2] or z[2]

            # if having toitsu, use it as janto and adjust n_pre_mentsu
            if has_toitsu:
                n_pre_mentsu -= 1

            # adjust n_pre_mentsu when mentsu over
            if n_mentsu + n_pre_mentsu > 4:
                n_pre_mentsu = 4 - n_mentsu

            shanten = 8 - n_mentsu * 2 - n_pre_mentsu - (1 if has_toitsu else 0)
            min_shanten = min(min_shanten, shanten)

        return min_shanten

    @staticmethod
    def calculate_shanten_for_chiitoitsu(jun_tehai: Hai34):
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
    def calculate_shanten_for_kokushimusou(jun_tehai: Hai34):
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
    def check_waiting_for_5th_hai(jun_tehai: Hai34, n_huuro: int):
        jun_tehai = jun_tehai.to_hai34_counter()
