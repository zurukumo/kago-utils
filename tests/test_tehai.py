import gzip
import os
import pickle
import unittest

from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.huuro import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.tehai import Tehai
from kago_utils.zaichi import Zaichi


# This function simplifies the representation of huuro.
# In Tenhou, the structure of huuro is randomized, likely to prevent reading of opponents' tehai.
# Therefore, we need to simplify the structure for testing purposes.
# For example, if hais 0, 1, and 4 are in tehai, and the upper player discards hai 8,
# the player can form a Chii using 0, 4, 8 or 1, 4, 8. The specific arrangement is random.
# So, when comparing Tenhou’s game records in tests, we need to convert sequences like 0, 4, 8 or 1, 4, 8
# into a standardized format, such as kuro1m|kuro2m|kuro3m, for accurate comparison.
def simplify_huuro(huuro: Chii | Pon | Kakan | Daiminkan | Ankan) -> str:
    return "|".join([hai.long_name for hai in huuro.hais])


class TestTehaiInit(unittest.TestCase):
    def test_init_as_juntehai(self):
        hai_group = HaiGroup.from_list(list(range(14)))
        Tehai(juntehai=hai_group)

    def test_init_with_juntehai_whose_length_is_not_invalid(self):
        hai_group = HaiGroup.from_list(list(range(3)))
        with self.assertRaises(ValueError):
            Tehai(juntehai=hai_group)

    def test_init_with_juntehai_whose_length_is_too_long(self):
        hai_group = HaiGroup.from_list(list(range(15)))
        with self.assertRaises(ValueError):
            Tehai(juntehai=hai_group)

    def test_init_with_juntehai_which_has_same_hai(self):
        hai_group = HaiGroup.from_list(list(range(12)) + [12] * 2)
        with self.assertRaises(ValueError):
            Tehai(juntehai=hai_group)


class TestTehaiListChiiCandidates(unittest.TestCase):
    def test_list_chii_candidates(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/tehai/chii.pickle.gz")
        with gzip.open(filepath, "rb") as f:
            test_cases = pickle.load(f)

        for test_case in test_cases:
            juntehai = HaiGroup.from_list(test_case["juntehai"])
            hais = HaiGroup.from_list(test_case["hais"])
            stolen = Hai(test_case["stolen"])

            tehai = Tehai(juntehai)
            candidates = map(simplify_huuro, tehai.list_chii_candidates(stolen=stolen))
            expected = simplify_huuro(Chii(hais=hais, stolen=stolen))

            self.assertIn(expected, candidates)


class TestTehaiListPonCandidates(unittest.TestCase):
    def test_list_pon_candidates(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/tehai/pon.pickle.gz")
        with gzip.open(filepath, "rb") as f:
            test_cases = pickle.load(f)

        for test_case in test_cases:
            juntehai = HaiGroup.from_list(test_case["juntehai"])
            hais = HaiGroup.from_list(test_case["hais"])
            stolen = Hai(test_case["stolen"])
            from_who = Zaichi(test_case["from_who"])

            tehai = Tehai(juntehai)
            candidates = map(simplify_huuro, tehai.list_pon_candidates(stolen=stolen, from_who=from_who))
            expected = simplify_huuro(Pon(hais=hais, stolen=stolen, from_who=from_who))

            self.assertIn(expected, candidates)


class TestTehaiListDaiminkanCandidates(unittest.TestCase):
    def test_list_daiminkan_candidates(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/tehai/daiminkan.pickle.gz")
        with gzip.open(filepath, "rb") as f:
            test_cases = pickle.load(f)

        for test_case in test_cases:
            juntehai = HaiGroup.from_list(test_case["juntehai"])
            hais = HaiGroup.from_list(test_case["hais"])
            stolen = Hai(test_case["stolen"])
            from_who = Zaichi(test_case["from_who"])

            tehai = Tehai(juntehai)
            candidates = map(simplify_huuro, tehai.list_daiminkan_candidates(stolen=stolen, from_who=from_who))
            expected = simplify_huuro(Daiminkan(hais=hais, stolen=stolen, from_who=from_who))

            self.assertIn(expected, candidates)


class TestTehaiListKakanCandidates(unittest.TestCase):
    def test_list_kakan_candidates(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/tehai/kakan.pickle.gz")
        with gzip.open(filepath, "rb") as f:
            test_cases = pickle.load(f)

        for test_case in test_cases:
            juntehai = HaiGroup.from_list(test_case["juntehai"])
            hais = HaiGroup.from_list(test_case["hais"])
            stolen = Hai(test_case["stolen"])
            added = Hai(test_case["added"])
            from_who = Zaichi(test_case["from_who"])

            huuros = []
            for pon in test_case["pons"]:
                pon_hais = HaiGroup.from_list(pon["hais"])
                pon_stolen = Hai(pon["stolen"])
                pon_from_who = Zaichi(pon["from_who"])
                huuros.append(Pon(hais=pon_hais, stolen=pon_stolen, from_who=pon_from_who))

            tehai = Tehai(juntehai, huuros)
            candidates = map(simplify_huuro, tehai.list_kakan_candidates(added=added))
            expected = simplify_huuro(Kakan(hais=hais, stolen=stolen, added=added, from_who=from_who))

            self.assertIn(expected, candidates)


class TestTehaiListAnkanCandidates(unittest.TestCase):
    def test_list_ankan_candidates(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/tehai/ankan.pickle.gz")
        with gzip.open(filepath, "rb") as f:
            test_cases = pickle.load(f)

        for test_case in test_cases:
            juntehai = HaiGroup.from_list(test_case["juntehai"])
            hais = HaiGroup.from_list(test_case["hais"])

            tehai = Tehai(juntehai)
            candidates = map(simplify_huuro, tehai.list_ankan_candidates())
            expected = simplify_huuro(Ankan(hais=hais))

            self.assertIn(expected, candidates)
