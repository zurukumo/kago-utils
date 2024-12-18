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
    return "|".join([hai.code for hai in huuro.hais])


def game_factory():
    game = Game()
    game.yama = [Hai(i) for i in range(136)]

    for i in range(4):
        player = Player(id=str(i))
        player.ten = 25000
        game.add_player(player)

    return game


class TestPlayerInit(unittest.TestCase):
    def test_init(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))


class TestPlayerChii(unittest.TestCase):
    def test_chii(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52])
        chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))
        player.chii(chii)

        self.assertIn(chii, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52]))


class TestPlayerPon(unittest.TestCase):
    def test_pon(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24])
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)
        player.pon(pon)

        self.assertIn(pon, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24]))


class TestPlayerKakan(unittest.TestCase):
    def test_kakan(self):
        game = game_factory()
        player = game.players[0]

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
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
        daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(3), from_who=Zaichi.KAMICHA)
        player.daiminkan(daiminkan)

        self.assertIn(daiminkan, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 6, 8, 9, 10, 12, 13, 14, 16]))


class TestPlayerAnkan(unittest.TestCase):
    def test_ankan(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
        ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
        player.ankan(ankan)

        self.assertIn(ankan, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 6, 8, 9, 10, 12, 13, 14, 16]))


class TestPlayerIsMenzen(unittest.TestCase):
    def test_is_menzen_without_huuros(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        self.assertTrue(player.is_menzen)

    def test_is_menzen_with_chii(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))]
        self.assertFalse(player.is_menzen)

    def test_is_menzen_with_pon(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)]
        self.assertFalse(player.is_menzen)

    def test_is_menzen_with_kakan(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        ]
        self.assertFalse(player.is_menzen)

    def test_is_menzen_with_daiminkan(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)]
        self.assertFalse(player.is_menzen)

    def test_is_menzen_with_ankan(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))]
        self.assertTrue(player.is_menzen)

    def test_is_menzen_with_ankan_and_chii(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [
            Ankan(hais=HaiGroup.from_list([0, 1, 2, 3])),
            Chii(hais=HaiGroup.from_list([4, 8, 12]), stolen=Hai(4)),
        ]
        self.assertFalse(player.is_menzen)


class TestPlayerListRiichiCandidates(unittest.TestCase):
    def test_list_riichi_candidates(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("12346666778899m")
        self.assertEqual(player.list_riichi_candidates(), True)

    def test_list_riichi_candidates_when_not_menzen(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("123456m11p112s")

        player.huuros = []
        self.assertEqual(player.list_riichi_candidates(), True)

        player.huuros = [Chii(hais=HaiGroup.from_code("789s"), stolen=HaiGroup.from_code("789s")[0])]
        self.assertEqual(player.list_riichi_candidates(), False)

    def test_list_riichi_candidates_when_riichi_is_completed(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("123456789m11p112s")

        player.is_riichi_completed = False
        self.assertEqual(player.list_riichi_candidates(), True)

        player.is_riichi_completed = True
        self.assertEqual(player.list_riichi_candidates(), False)

    def test_list_riichi_candidates_right_after_calling_riichi(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("123456789m11p112s")

        self.assertEqual(player.list_riichi_candidates(), True)

        player.riichi()
        self.assertEqual(player.list_riichi_candidates(), False)

    def test_list_riichi_candidates_when_ten_is_not_enough(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("123456789m11p112s")

        player.ten = 1000
        self.assertEqual(player.list_riichi_candidates(), True)

        player.ten = 900
        self.assertEqual(player.list_riichi_candidates(), False)

    def test_list_riichi_candidates_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("123456789m11p112s")

        game.yama = [Hai(i) for i in range(4)]
        self.assertEqual(player.list_riichi_candidates(), True)

        game.yama = [Hai(i) for i in range(3)]
        self.assertEqual(player.list_riichi_candidates(), False)

    def test_list_riichi_candidates_when_not_tenpai(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("123456789m11p159s")

        self.assertEqual(player.list_riichi_candidates(), False)


class TestPlayerListDahaiCandidates(unittest.TestCase):
    def test_list_dahai_candidates(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("123456789m11p112s")
        self.assertEqual(player.list_dahai_candidates(), HaiGroup.from_code("123456789m11p112s"))

    def test_list_dahai_candidates_when_riichi_is_completed(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("123456789m11p112s")
        player.last_tsumo = HaiGroup.from_code("1m")[0]
        player.is_riichi_completed = True
        self.assertEqual(player.list_dahai_candidates(), HaiGroup.from_code("1m"))

    def test_list_dahai_candidates_right_after_calling_riichi(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("12346666778899m")
        player.riichi()
        self.assertEqual(player.list_dahai_candidates(), HaiGroup.from_code("14666699m"))

    def test_list_dahai_candidates_right_after_calling_chii(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("123m1112223334z")
        game.last_dahai = HaiGroup.from_code("4m")[0]
        game.last_teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)
        player.chii(player.list_chii_candidates()[0])
        self.assertEqual(player.list_dahai_candidates(), HaiGroup.from_code("1112223334z"))

    def test_list_dahai_candidates_right_after_calling_pon(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_code("555m1112223334z")
        game.last_dahai = HaiGroup.from_code("0m")[0]
        game.last_teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)
        player.pon(player.list_pon_candidates()[0])
        self.assertEqual(player.list_dahai_candidates(), HaiGroup.from_code("1112223334z"))


class TestPlayerListChiiCandidates(unittest.TestCase):
    def test_list_chii_candidates(self):
        game = game_factory()
        player = game.players[0]

        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "data/player/chii.pickle.gz")
        with gzip.open(filepath, "rb") as f:
            test_cases = pickle.load(f)

        for test_case in test_cases:
            juntehai = HaiGroup.from_list(test_case["juntehai"])
            hais = HaiGroup.from_list(test_case["hais"])
            stolen = Hai(test_case["stolen"])

            player.juntehai = juntehai
            game.last_dahai = stolen
            game.last_teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

            candidates = map(simplify_huuro, player.list_chii_candidates())
            expected = simplify_huuro(Chii(hais=hais, stolen=stolen))

            self.assertIn(expected, candidates)

    def test_list_chii_candidates_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 4, 134, 135])
        game.last_dahai = Hai(8)
        game.last_teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        game.yama = [Hai(i) for i in range(1)]
        self.assertEqual(len(player.list_chii_candidates()), 1)

        game.yama = []
        self.assertEqual(len(player.list_chii_candidates()), 0)

    def test_list_chii_candidates_when_cannot_dahai_after_chii(self):
        game = game_factory()
        player = game.players[0]

        game.last_dahai = Hai(10)
        game.last_teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player.juntehai = HaiGroup.from_list([0, 4, 8, 9, 133, 134, 135])
        self.assertEqual(len(player.list_chii_candidates()), 1)

        player.juntehai = HaiGroup.from_list([0, 4, 8, 9])
        self.assertEqual(len(player.list_chii_candidates()), 0)


class TestPlayerListPonCandidates(unittest.TestCase):
    def test_list_pon_candidates(self):
        game = game_factory()
        player = game.players[0]

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
            game.last_dahai = stolen
            game.last_teban = player.get_zaseki_from_zaichi(from_who)

            candidates = map(simplify_huuro, player.list_pon_candidates())
            expected = simplify_huuro(Pon(hais=hais, stolen=stolen, from_who=from_who))

            self.assertIn(expected, candidates)

    def test_list_pon_candidates_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 134, 135])
        game.last_dahai = Hai(2)
        game.last_teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        game.yama = [Hai(i) for i in range(1)]
        self.assertEqual(len(player.list_pon_candidates()), 1)

        game.yama = []
        self.assertEqual(len(player.list_pon_candidates()), 0)


class TestPlayerListKakanCandidates(unittest.TestCase):
    def test_list_kakan_candidates(self):
        game = game_factory()
        player = game.players[0]

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

            candidates = map(simplify_huuro, player.list_kakan_candidates())
            expected = simplify_huuro(Kakan(hais=hais, stolen=stolen, added=added, from_who=from_who))

            self.assertIn(expected, candidates)

    def test_list_kakan_candidates_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([3, 135])
        player.huuros = [Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)]

        game.yama = [Hai(i) for i in range(1)]
        self.assertEqual(len(player.list_kakan_candidates()), 1)

        game.yama = []
        self.assertEqual(len(player.list_kakan_candidates()), 0)

    def test_list_kakan_candidates_when_four_kans_exist(self):
        game = game_factory()
        player1 = game.players[0]
        player2 = game.players[1]

        player1.juntehai = HaiGroup.from_list([3, 135])
        player1.huuros = [Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)]

        player2.huuros = []
        self.assertEqual(len(player1.list_kakan_candidates()), 1)

        player2.huuros = [
            Ankan(hais=HaiGroup.from_code("1111z")),
            Ankan(hais=HaiGroup.from_code("2222z")),
            Ankan(hais=HaiGroup.from_code("3333z")),
            Ankan(hais=HaiGroup.from_code("4444z")),
        ]
        self.assertEqual(len(player1.list_kakan_candidates()), 0)


class TestPlayerListDaiminkanCandidates(unittest.TestCase):
    def test_list_daiminkan_candidates(self):
        game = game_factory()
        player = game.players[0]

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
            game.last_dahai = stolen
            game.last_teban = player.get_zaseki_from_zaichi(from_who)

            candidates = map(simplify_huuro, player.list_daiminkan_candidates())
            expected = simplify_huuro(Daiminkan(hais=hais, stolen=stolen, from_who=from_who))

            self.assertIn(expected, candidates)

    def test_list_daiminkan_candidates_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 2, 135])
        game.last_dahai = Hai(3)
        game.last_teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        game.yama = [Hai(i) for i in range(1)]
        self.assertEqual(len(player.list_daiminkan_candidates()), 1)

        game.yama = []
        self.assertEqual(len(player.list_daiminkan_candidates()), 0)

    def test_list_daiminkan_candidates_when_four_kans_exist(self):
        game = game_factory()
        player1 = game.players[0]
        player2 = game.players[1]

        player1.juntehai = HaiGroup.from_list([0, 1, 2, 135])
        game.last_dahai = Hai(3)
        game.last_teban = player1.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player2.huuros = []
        self.assertEqual(len(player1.list_daiminkan_candidates()), 1)

        player2.huuros = [
            Ankan(hais=HaiGroup.from_code("1111z")),
            Ankan(hais=HaiGroup.from_code("2222z")),
            Ankan(hais=HaiGroup.from_code("3333z")),
            Ankan(hais=HaiGroup.from_code("4444z")),
        ]
        self.assertEqual(len(player1.list_daiminkan_candidates()), 0)


class TestPlayerListAnkanCandidates(unittest.TestCase):
    def test_list_ankan_candidates(self):
        game = game_factory()
        player = game.players[0]

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

    def test_list_ankan_candidates_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 2, 3, 135])

        game.yama = [Hai(i) for i in range(1)]
        self.assertEqual(len(player.list_ankan_candidates()), 1)

        game.yama = []
        self.assertEqual(len(player.list_ankan_candidates()), 0)

    def test_list_ankan_candidates_when_four_kans_exist(self):
        game = game_factory()
        player1 = game.players[0]
        player2 = game.players[1]

        player1.juntehai = HaiGroup.from_list([0, 1, 2, 3, 135])

        player2.huuros = []
        self.assertEqual(len(player1.list_ankan_candidates()), 1)

        player2.huuros = [
            Ankan(hais=HaiGroup.from_code("1111z")),
            Ankan(hais=HaiGroup.from_code("2222z")),
            Ankan(hais=HaiGroup.from_code("3333z")),
            Ankan(hais=HaiGroup.from_code("4444z")),
        ]
        self.assertEqual(len(player1.list_ankan_candidates()), 0)
