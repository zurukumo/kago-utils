import gzip
import os
import pickle
import unittest

from kago_utils.game import Game
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.huuro import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.player import Player
from kago_utils.zaichi import Zaichi


# This function simplifies the representation of huuro.
# In Tenhou, the structure of huuro is randomized, likely to prevent reading of opponents' player.
# Therefore, we need to simplify the structure for testing purposes.
# For example, if hais 0, 1, and 4 are in player, and the upper player discards hai 8,
# the player can form a Chii using 0, 4, 8 or 1, 4, 8. The specific arrangement is random.
# So, when comparing Tenhou’s game records in tests, we need to convert sequences like 0, 4, 8 or 1, 4, 8
# into a standardized format, such as kuro1m|kuro2m|kuro3m, for accurate comparison.
def simplify_huuro(huuro: Chii | Pon | Kakan | Daiminkan | Ankan) -> str:
    return "|".join([hai.long_name for hai in huuro.hais])


def player_factory():
    game = Game()
    for i in range(4):
        game.players.append(Player(id=str(i)))
    return game.players[0]


class TestPlayerInit(unittest.TestCase):
    def test_init(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list(list(range(14)))


class TestPlayerChii(unittest.TestCase):
    def test_chii(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list([4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52])
        chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))
        player.chii(chii)

        self.assertIn(chii, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52]))


class TestPlayerPon(unittest.TestCase):
    def test_pon(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list([0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24])
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)
        player.pon(pon)

        self.assertIn(pon, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24]))


class TestPlayerKakan(unittest.TestCase):
    def test_kakan(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list([3, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24])
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(2), added=Hai(3), from_who=Zaichi.KAMICHA)
        player.huuros = [pon]
        player.kakan(kakan)

        self.assertIn(kakan, player.huuros)
        self.assertNotIn(pon, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24]))


class TestPlayerDaiminkan(unittest.TestCase):
    def test_daiminkan(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list([0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
        daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(3), from_who=Zaichi.KAMICHA)
        player.daiminkan(daiminkan)

        self.assertIn(daiminkan, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 6, 8, 9, 10, 12, 13, 14, 16]))


class TestPlayerAnkan(unittest.TestCase):
    def test_ankan(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list([0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
        ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
        player.ankan(ankan)

        self.assertIn(ankan, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 6, 8, 9, 10, 12, 13, 14, 16]))


class TestPlayerIsMenzen(unittest.TestCase):
    def test_is_menzen_without_huuros(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list(list(range(14)))
        self.assertTrue(player.is_menzen)

    def test_is_menzen_with_chii(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))]
        self.assertFalse(player.is_menzen)

    def test_is_menzen_with_pon(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)]
        self.assertFalse(player.is_menzen)

    def test_is_menzen_with_kakan(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        ]
        self.assertFalse(player.is_menzen)

    def test_is_menzen_with_daiminkan(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)]
        self.assertFalse(player.is_menzen)

    def test_is_menzen_with_ankan(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))]
        self.assertTrue(player.is_menzen)

    def test_is_menzen_with_ankan_and_chii(self):
        player = player_factory()
        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [
            Ankan(hais=HaiGroup.from_list([0, 1, 2, 3])),
            Chii(hais=HaiGroup.from_list([4, 8, 12]), stolen=Hai(4)),
        ]
        self.assertFalse(player.is_menzen)


class TestPlayerListChiiCandidates(unittest.TestCase):
    def test_list_chii_candidates(self):
        player = player_factory()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/player/chii.pickle.gz")
        with gzip.open(filepath, "rb") as f:
            test_cases = pickle.load(f)

        for test_case in test_cases:
            juntehai = HaiGroup.from_list(test_case["juntehai"])
            hais = HaiGroup.from_list(test_case["hais"])
            stolen = Hai(test_case["stolen"])

            player.juntehai = juntehai
            candidates = map(simplify_huuro, player.list_chii_candidates(stolen=stolen))
            expected = simplify_huuro(Chii(hais=hais, stolen=stolen))

            self.assertIn(expected, candidates)


class TestPlayerListPonCandidates(unittest.TestCase):
    def test_list_pon_candidates(self):
        player = player_factory()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/player/pon.pickle.gz")
        with gzip.open(filepath, "rb") as f:
            test_cases = pickle.load(f)

        for test_case in test_cases:
            juntehai = HaiGroup.from_list(test_case["juntehai"])
            hais = HaiGroup.from_list(test_case["hais"])
            stolen = Hai(test_case["stolen"])
            from_who = Zaichi(test_case["from_who"])

            player.juntehai = juntehai
            candidates = map(simplify_huuro, player.list_pon_candidates(stolen=stolen, from_who=from_who))
            expected = simplify_huuro(Pon(hais=hais, stolen=stolen, from_who=from_who))

            self.assertIn(expected, candidates)


class TestPlayerListDaiminkanCandidates(unittest.TestCase):
    def test_list_daiminkan_candidates(self):
        player = player_factory()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/player/daiminkan.pickle.gz")
        with gzip.open(filepath, "rb") as f:
            test_cases = pickle.load(f)

        for test_case in test_cases:
            juntehai = HaiGroup.from_list(test_case["juntehai"])
            hais = HaiGroup.from_list(test_case["hais"])
            stolen = Hai(test_case["stolen"])
            from_who = Zaichi(test_case["from_who"])

            player.juntehai = juntehai
            candidates = map(simplify_huuro, player.list_daiminkan_candidates(stolen=stolen, from_who=from_who))
            expected = simplify_huuro(Daiminkan(hais=hais, stolen=stolen, from_who=from_who))

            self.assertIn(expected, candidates)


class TestPlayerListKakanCandidates(unittest.TestCase):
    def test_list_kakan_candidates(self):
        player = player_factory()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/player/kakan.pickle.gz")
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

            player.juntehai = juntehai
            player.huuros = huuros
            candidates = map(simplify_huuro, player.list_kakan_candidates(added=added))
            expected = simplify_huuro(Kakan(hais=hais, stolen=stolen, added=added, from_who=from_who))

            self.assertIn(expected, candidates)


class TestPlayerListAnkanCandidates(unittest.TestCase):
    def test_list_ankan_candidates(self):
        player = player_factory()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/player/ankan.pickle.gz")
        with gzip.open(filepath, "rb") as f:
            test_cases = pickle.load(f)

        for test_case in test_cases:
            juntehai = HaiGroup.from_list(test_case["juntehai"])
            hais = HaiGroup.from_list(test_case["hais"])

            player.juntehai = juntehai
            candidates = map(simplify_huuro, player.list_ankan_candidates())
            expected = simplify_huuro(Ankan(hais=hais))

            self.assertIn(expected, candidates)
