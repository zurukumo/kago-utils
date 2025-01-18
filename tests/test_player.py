import gzip
import os
import pickle
import unittest

from kago_utils.actions import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.game import Game
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
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
    game.yama.generate()

    for i in range(4):
        player = Player(id=str(i))
        game.add_player(player)

    return game


class TestChii(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52])
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)
        game.last_dahai = Hai(0)
        chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))
        player.chii(chii)

        self.assertIn(chii, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52]))

    def test_with_invalid_chii(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52])
        game.teban = player.get_zaseki_from_zaichi(Zaichi.TOIMEN)
        game.last_dahai = Hai(0)
        chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(4))
        with self.assertRaises(ValueError):
            player.chii(chii)


class TestPon(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24])
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)
        game.last_dahai = Hai(2)
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)
        player.pon(pon)

        self.assertIn(pon, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24]))

    def test_with_invalid_pon(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24])
        game.teban = player.get_zaseki_from_zaichi(Zaichi.TOIMEN)
        game.last_dahai = Hai(2)
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(1), from_who=Zaichi.KAMICHA)
        with self.assertRaises(ValueError):
            player.pon(pon)


class TestKakan(unittest.TestCase):
    def test(self):
        game = game_factory()
        game.teban = 0

        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(2), added=Hai(3), from_who=Zaichi.KAMICHA)

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([3, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25])
        player.last_tsumo = Hai(3)
        player.huuros = [pon]

        game.teban_action_resolver.prepare()
        player.kakan(kakan)
        self.assertIn(kakan, player.huuros)
        self.assertNotIn(pon, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25]))

    def test_with_invalid_kakan(self):
        game = game_factory()
        game.teban = 0

        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(2), added=Hai(1), from_who=Zaichi.KAMICHA)

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([3, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25])
        player.last_tsumo = Hai(3)
        player.huuros = [pon]

        game.teban_action_resolver.prepare()
        with self.assertRaises(ValueError):
            player.kakan(kakan)


class TestDaiminkan(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)
        game.last_dahai = Hai(3)
        daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(3), from_who=Zaichi.KAMICHA)
        player.daiminkan(daiminkan)

        self.assertIn(daiminkan, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 6, 8, 9, 10, 12, 13, 14, 16]))

    def test_with_invalid_daiminkan(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)
        game.last_dahai = Hai(3)
        daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(2), from_who=Zaichi.KAMICHA)
        with self.assertRaises(ValueError):
            player.daiminkan(daiminkan)


class TestAnkan(unittest.TestCase):
    def test(self):
        game = game_factory()
        game.teban = 0

        ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
        player.last_tsumo = Hai(3)

        game.teban_action_resolver.prepare()
        player.ankan(ankan)
        self.assertIn(ankan, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 6, 8, 9, 10, 12, 13, 14, 16]))

    def test_with_invalid_ankan(self):
        game = game_factory()
        game.teban = 0

        ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([0, 1, 2, 3, 4, 8, 12, 108, 109, 110, 112, 113, 114, 115])
        player.last_tsumo = Hai(12)
        player.is_riichi_completed = True

        game.teban_action_resolver.prepare()
        with self.assertRaises(ValueError):
            player.ankan(ankan)


class TestIsMenzen(unittest.TestCase):
    def test_without_huuros(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        self.assertTrue(player.is_menzen)

    def test_with_chii(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))]
        self.assertFalse(player.is_menzen)

    def test_with_pon(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)]
        self.assertFalse(player.is_menzen)

    def test_with_kakan(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        ]
        self.assertFalse(player.is_menzen)

    def test_with_daiminkan(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)]
        self.assertFalse(player.is_menzen)

    def test_with_ankan(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))]
        self.assertTrue(player.is_menzen)

    def test_with_ankan_and_chii(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list(list(range(14)))
        player.huuros = [
            Ankan(hais=HaiGroup.from_list([0, 1, 2, 3])),
            Chii(hais=HaiGroup.from_list([4, 8, 12]), stolen=Hai(4)),
        ]
        self.assertFalse(player.is_menzen)


class TestJicha(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]

        self.assertEqual(player.jicha, game.players[0])


class TestKamicha(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]

        self.assertEqual(player.kamicha, game.players[3])


class TestToimen(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]

        self.assertEqual(player.toimen, game.players[2])


class TestShimocha(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]

        self.assertEqual(player.shimocha, game.players[1])


class TestListChiiCandidates(unittest.TestCase):
    def test(self):
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
            game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

            candidates = map(simplify_huuro, player.list_chii_candidates())
            expected = simplify_huuro(Chii(hais=hais, stolen=stolen))

            self.assertIn(expected, candidates)

    def test_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 4, 134, 135])
        game.last_dahai = Hai(8)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        game.yama.tsumo_hais = [Hai(i) for i in range(1)]
        self.assertEqual(len(player.list_chii_candidates()), 1)

        game.yama.tsumo_hais = []
        self.assertEqual(len(player.list_chii_candidates()), 0)

    def test_when_riichi_is_completed(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 4, 134, 135])
        game.last_dahai = Hai(8)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player.is_riichi_completed = False
        self.assertEqual(len(player.list_chii_candidates()), 1)

        player.is_riichi_completed = True
        self.assertEqual(len(player.list_chii_candidates()), 0)

    def test_when_cannot_dahai_after_chii(self):
        game = game_factory()
        player = game.players[0]

        game.last_dahai = Hai(10)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player.juntehai = HaiGroup.from_list([0, 4, 8, 9, 133, 134, 135])
        self.assertEqual(len(player.list_chii_candidates()), 1)

        player.juntehai = HaiGroup.from_list([0, 4, 8, 9])
        self.assertEqual(len(player.list_chii_candidates()), 0)


class TestListPonCandidates(unittest.TestCase):
    def test(self):
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
            game.teban = player.get_zaseki_from_zaichi(from_who)

            candidates = map(simplify_huuro, player.list_pon_candidates())
            expected = simplify_huuro(Pon(hais=hais, stolen=stolen, from_who=from_who))

            self.assertIn(expected, candidates)

    def test_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 134, 135])
        game.last_dahai = Hai(2)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        game.yama.tsumo_hais = [Hai(i) for i in range(1)]
        self.assertEqual(len(player.list_pon_candidates()), 1)

        game.yama.tsumo_hais = []
        self.assertEqual(len(player.list_pon_candidates()), 0)

    def test_when_riichi_is_completed(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 134, 135])
        game.last_dahai = Hai(2)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player.is_riichi_completed = False
        self.assertEqual(len(player.list_pon_candidates()), 1)

        player.is_riichi_completed = True
        self.assertEqual(len(player.list_pon_candidates()), 0)


class TestListDaiminkanCandidates(unittest.TestCase):
    def test(self):
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
            game.teban = player.get_zaseki_from_zaichi(from_who)

            candidates = map(simplify_huuro, player.list_daiminkan_candidates())
            expected = simplify_huuro(Daiminkan(hais=hais, stolen=stolen, from_who=from_who))

            self.assertIn(expected, candidates)

    def test_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 2, 135])
        game.last_dahai = Hai(3)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        game.yama.tsumo_hais = [Hai(i) for i in range(1)]
        self.assertEqual(len(player.list_daiminkan_candidates()), 1)

        game.yama.tsumo_hais = []
        self.assertEqual(len(player.list_daiminkan_candidates()), 0)

    def test_when_riichi_is_completed(self):
        game = game_factory()
        player = game.players[0]

        player.juntehai = HaiGroup.from_list([0, 1, 2, 135])
        game.last_dahai = Hai(3)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player.is_riichi_completed = False
        self.assertEqual(len(player.list_daiminkan_candidates()), 1)

        player.is_riichi_completed = True
        self.assertEqual(len(player.list_daiminkan_candidates()), 0)

    def test_when_four_kans_exist(self):
        game = game_factory()
        player1 = game.players[0]
        player2 = game.players[1]

        player1.juntehai = HaiGroup.from_list([0, 1, 2, 135])
        game.last_dahai = Hai(3)
        game.teban = player1.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player2.huuros = []
        self.assertEqual(len(player1.list_daiminkan_candidates()), 1)

        player2.huuros = [
            Ankan(hais=HaiGroup.from_code("1111z")),
            Ankan(hais=HaiGroup.from_code("2222z")),
            Ankan(hais=HaiGroup.from_code("3333z")),
            Ankan(hais=HaiGroup.from_code("4444z")),
        ]
        self.assertEqual(len(player1.list_daiminkan_candidates()), 0)


if __name__ == "__main__":
    unittest.main()
