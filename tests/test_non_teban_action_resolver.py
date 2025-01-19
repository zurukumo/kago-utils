import gzip
import os
import pickle
import unittest

from kago_utils.actions import Ankan, Chii, Daiminkan, Kakan, Pon, Ronho
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
    game.kyoku = 0
    game.honba = 0
    game.kyoutaku = 0
    game.teban = 3

    for i in range(4):
        player = Player(id=str(i))
        game.add_player(player)

    return game


class TestListRonhoCandidates(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver
        resolver = game.non_teban_action_resolver

        player.juntehai = HaiGroup.from_code("23456789m11p123s")
        game.last_dahai = HaiGroup.from_code("1m")[0]
        self.assertEqual(resolver.list_ronho_candidates(player), [Ronho()])

    def test_when_nooten(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver
        resolver = game.non_teban_action_resolver

        player.juntehai = HaiGroup.from_code("23456789m11p123s")
        game.last_dahai = HaiGroup.from_code("1m")[0]
        self.assertEqual(resolver.list_ronho_candidates(player), [Ronho()])

        player.juntehai = HaiGroup.from_code("23456789m11p122s")
        game.last_dahai = HaiGroup.from_code("1m")[0]
        self.assertEqual(resolver.list_ronho_candidates(player), [])


class TestListDaiminkanCandidates(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver
        resolver = game.non_teban_action_resolver

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

            candidates = map(simplify_huuro, resolver.list_daiminkan_candidates(player))
            expected = simplify_huuro(Daiminkan(hais=hais, stolen=stolen, from_who=from_who))

            self.assertIn(expected, candidates)

    def test_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver

        player.juntehai = HaiGroup.from_list([0, 1, 2, 135])
        game.last_dahai = Hai(3)

        game.yama.tsumo_hais = [Hai(i) for i in range(1)]
        self.assertEqual(len(resolver.list_daiminkan_candidates(player)), 1)

        game.yama.tsumo_hais = []
        self.assertEqual(len(resolver.list_daiminkan_candidates(player)), 0)

    def test_when_riichi_is_completed(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver

        player.juntehai = HaiGroup.from_list([0, 1, 2, 135])
        game.last_dahai = Hai(3)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player.is_riichi_completed = False
        self.assertEqual(len(resolver.list_daiminkan_candidates(player)), 1)

        player.is_riichi_completed = True
        self.assertEqual(len(resolver.list_daiminkan_candidates(player)), 0)

    def test_when_four_kans_exist(self):
        game = game_factory()
        player1 = game.players[0]
        player2 = game.players[1]
        resolver = game.non_teban_action_resolver

        player1.juntehai = HaiGroup.from_list([0, 1, 2, 135])
        game.last_dahai = Hai(3)
        game.teban = player1.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player2.huuros = []
        self.assertEqual(len(resolver.list_daiminkan_candidates(player1)), 1)

        player2.huuros = [
            Ankan(hais=HaiGroup.from_code("1111z")),
            Ankan(hais=HaiGroup.from_code("2222z")),
            Ankan(hais=HaiGroup.from_code("3333z")),
            Ankan(hais=HaiGroup.from_code("4444z")),
        ]
        self.assertEqual(len(resolver.list_daiminkan_candidates(player1)), 0)


class TestListPonCandidates(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver

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

            candidates = map(simplify_huuro, resolver.list_pon_candidates(player))
            expected = simplify_huuro(Pon(hais=hais, stolen=stolen, from_who=from_who))

            self.assertIn(expected, candidates)

    def test_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver

        player.juntehai = HaiGroup.from_list([0, 1, 134, 135])
        game.last_dahai = Hai(2)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        game.yama.tsumo_hais = [Hai(i) for i in range(1)]
        self.assertEqual(len(resolver.list_pon_candidates(player)), 1)

        game.yama.tsumo_hais = []
        self.assertEqual(len(resolver.list_pon_candidates(player)), 0)

    def test_when_riichi_is_completed(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver

        player.juntehai = HaiGroup.from_list([0, 1, 134, 135])
        game.last_dahai = Hai(2)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player.is_riichi_completed = False
        self.assertEqual(len(resolver.list_pon_candidates(player)), 1)

        player.is_riichi_completed = True
        self.assertEqual(len(resolver.list_pon_candidates(player)), 0)


class TestListChiiCandidates(unittest.TestCase):
    def test(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver

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

            candidates = map(simplify_huuro, resolver.list_chii_candidates(player))
            expected = simplify_huuro(Chii(hais=hais, stolen=stolen))

            self.assertIn(expected, candidates)

    def test_when_yama_is_not_enough(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver

        player.juntehai = HaiGroup.from_list([0, 4, 134, 135])
        game.last_dahai = Hai(8)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        game.yama.tsumo_hais = [Hai(i) for i in range(1)]
        self.assertEqual(len(resolver.list_chii_candidates(player)), 1)

        game.yama.tsumo_hais = []
        self.assertEqual(len(resolver.list_chii_candidates(player)), 0)

    def test_when_riichi_is_completed(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver

        player.juntehai = HaiGroup.from_list([0, 4, 134, 135])
        game.last_dahai = Hai(8)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player.is_riichi_completed = False
        self.assertEqual(len(resolver.list_chii_candidates(player)), 1)

        player.is_riichi_completed = True
        self.assertEqual(len(resolver.list_chii_candidates(player)), 0)

    def test_when_cannot_dahai_after_chii(self):
        game = game_factory()
        player = game.players[0]
        resolver = game.non_teban_action_resolver

        game.last_dahai = Hai(10)
        game.teban = player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

        player.juntehai = HaiGroup.from_list([0, 4, 8, 9, 133, 134, 135])
        self.assertEqual(len(resolver.list_chii_candidates(player)), 1)

        player.juntehai = HaiGroup.from_list([0, 4, 8, 9])
        self.assertEqual(len(resolver.list_chii_candidates(player)), 0)


if __name__ == "__main__":
    unittest.main()
