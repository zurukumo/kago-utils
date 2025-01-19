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
    game.kyoku = 0
    game.honba = 0
    game.kyoutaku = 0

    for i in range(4):
        player = Player(id=str(i))
        game.add_player(player)

    return game


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

        ankan = Ankan(hais=HaiGroup.from_list([4, 5, 6, 7]))

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([0, 1, 2, 3, 4, 8, 12, 108, 109, 110, 112, 113, 114, 115])
        player.last_tsumo = Hai(12)

        game.teban_action_resolver.prepare()
        with self.assertRaises(ValueError):
            player.ankan(ankan)


class TestDaiminkan(unittest.TestCase):
    def test(self):
        game = game_factory()
        game.teban = 3

        daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(3), from_who=Zaichi.KAMICHA)

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
        game.last_dahai = Hai(3)

        game.non_teban_action_resolver.prepare()
        player.daiminkan(daiminkan)
        self.assertIn(daiminkan, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 6, 8, 9, 10, 12, 13, 14, 16]))

    def test_with_invalid_daiminkan(self):
        game = game_factory()
        game.teban = 3

        daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(2), from_who=Zaichi.KAMICHA)

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
        game.last_dahai = Hai(3)

        game.non_teban_action_resolver.prepare()
        with self.assertRaises(ValueError):
            player.daiminkan(daiminkan)


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


class TestPon(unittest.TestCase):
    def test(self):
        game = game_factory()
        game.teban = 3

        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24])
        game.last_dahai = Hai(2)

        game.non_teban_action_resolver.prepare()
        player.pon(pon)
        self.assertIn(pon, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24]))

    def test_with_invalid_pon(self):
        game = game_factory()
        game.teban = 3

        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(1), from_who=Zaichi.KAMICHA)

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24])
        game.last_dahai = Hai(2)

        game.non_teban_action_resolver.prepare()
        with self.assertRaises(ValueError):
            player.pon(pon)


class TestChii(unittest.TestCase):
    def test(self):
        game = game_factory()
        game.teban = 3

        chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52])
        game.last_dahai = Hai(0)

        game.non_teban_action_resolver.prepare()
        player.chii(chii)
        self.assertIn(chii, player.huuros)
        self.assertEqual(player.juntehai, HaiGroup.from_list([12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52]))

    def test_with_invalid_chii(self):
        game = game_factory()
        game.teban = 3

        chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(4))

        player = game.players[0]
        player.juntehai = HaiGroup.from_list([4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52])
        game.last_dahai = Hai(0)

        game.non_teban_action_resolver.prepare()
        with self.assertRaises(ValueError):
            player.chii(chii)


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


if __name__ == "__main__":
    unittest.main()
