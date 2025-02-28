import gzip
import os
import pickle

from kago_utils.actions import Ankan, Chii, Dahai, Daiminkan, Kakan, Pon, Riichi, Tsumoho
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
    game.teban = 0

    for i in range(4):
        player = Player(id=str(i))
        game.add_player(player)

    return game


def test_resolve_when_tsumoho_is_registered():
    game = game_factory()
    player = game.teban_player
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11122z")
    player.last_tsumo = HaiGroup.from_code("1m")[0]

    resolver.prepare()
    resolver.register_tsumoho(player, resolver.tsumoho_candidates[player.id][0])
    assert isinstance(resolver.choice[player.id], Tsumoho)


def test_resolve_when_riichi_is_registered():
    game = game_factory()
    player = game.teban_player
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("12345678m111223z")
    player.last_tsumo = HaiGroup.from_code("1m")[0]

    resolver.prepare()
    resolver.register_riichi(player, resolver.riichi_candidates[player.id][0])
    assert isinstance(resolver.choice[player.id], Riichi)


def test_resolve_when_ankan_is_registered():
    game = game_factory()
    player = game.teban_player
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11112z")
    player.last_tsumo = HaiGroup.from_code("1m")[0]

    resolver.prepare()
    resolver.register_ankan(player, resolver.ankan_candidates[player.id][0])
    assert isinstance(resolver.choice[player.id], Ankan)


def test_resolve_when_kakan_is_registered():
    game = game_factory()
    player = game.teban_player
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123406789m11z")
    player.huuros = [Pon(hais=HaiGroup.from_code("555m"), stolen=HaiGroup.from_code("5m")[0], from_who=Zaichi.KAMICHA)]
    player.last_tsumo = HaiGroup.from_code("1m")[0]

    resolver.prepare()
    resolver.register_kakan(player, resolver.kakan_candidates[player.id][0])
    assert isinstance(resolver.choice[player.id], Kakan)


def test_resolve_when_dahai_is_registered():
    game = game_factory()
    player = game.teban_player
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11122z")
    player.last_tsumo = HaiGroup.from_code("1m")[0]

    resolver.prepare()
    resolver.register_dahai(player, resolver.dahai_candidates[player.id][0])
    assert isinstance(resolver.choice[player.id], Dahai)


def test_resolve_when_choice_is_already_registered():
    game = game_factory()
    player = game.teban_player
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11122z")
    player.last_tsumo = HaiGroup.from_code("1m")[0]

    resolver.prepare()
    resolver.register_tsumoho(player, resolver.tsumoho_candidates[player.id][0])
    assert isinstance(resolver.choice[player.id], Tsumoho)

    resolver.register_dahai(player, resolver.dahai_candidates[player.id][0])
    assert isinstance(resolver.choice[player.id], Tsumoho)


def test_list_tsumoho_candidates():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11p123s")
    player.last_tsumo = HaiGroup.from_code("1m")[0]
    assert resolver.list_tsumoho_candidates(player) == [Tsumoho()]


def test_list_tsumoho_candidates_resolve_when_nooten():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11p123s")
    player.last_tsumo = HaiGroup.from_code("1m")[0]
    assert resolver.list_tsumoho_candidates(player) == [Tsumoho()]

    player.juntehai = HaiGroup.from_code("123456789m11p122s")
    player.last_tsumo = HaiGroup.from_code("1m")[0]
    assert resolver.list_tsumoho_candidates(player) == []


def test_list_tsumoho_candidates_when_not_yakuari():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("234567m22p234s")
    player.huuros = [Chii(hais=HaiGroup.from_code("678s"), stolen=HaiGroup.from_code("6s")[0])]
    player.last_tsumo = HaiGroup.from_code("2p")[0]
    assert resolver.list_tsumoho_candidates(player) == [Tsumoho()]

    player.juntehai = HaiGroup.from_code("123456m22p234s")
    player.huuros = [Chii(hais=HaiGroup.from_code("678s"), stolen=HaiGroup.from_code("6s")[0])]
    player.last_tsumo = HaiGroup.from_code("2p")[0]
    assert resolver.list_tsumoho_candidates(player) == []


def test_list_riichi_candidates():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("12346666778899m")
    assert resolver.list_riichi_candidates(player) == [Riichi()]


def test_list_riichi_candidates_when_not_menzen():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456m11p112s")

    player.huuros = []
    assert resolver.list_riichi_candidates(player) == [Riichi()]

    player.huuros = [Chii(hais=HaiGroup.from_code("789s"), stolen=HaiGroup.from_code("789s")[0])]
    assert resolver.list_riichi_candidates(player) == []


def test_list_riichi_candidates_when_riichi_is_completed():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11p112s")

    player.is_riichi_completed = False
    assert resolver.list_riichi_candidates(player) == [Riichi()]

    player.is_riichi_completed = True
    assert resolver.list_riichi_candidates(player) == []


def test_list_riichi_candidates_right_after_calling_riichi():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11p112s")

    assert resolver.list_riichi_candidates(player) == [Riichi()]

    player.riichi()
    assert resolver.list_riichi_candidates(player) == []


def test_list_riichi_candidates_when_ten_is_not_enough():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11p112s")

    player.ten = 1000
    assert resolver.list_riichi_candidates(player) == [Riichi()]

    player.ten = 900
    assert resolver.list_riichi_candidates(player) == []


def test_list_riichi_candidates_when_yama_is_not_enough():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11p112s")

    game.yama.tsumo_hais = [Hai(i) for i in range(4)]
    assert resolver.list_riichi_candidates(player) == [Riichi()]

    game.yama.tsumo_hais = [Hai(i) for i in range(3)]
    assert resolver.list_riichi_candidates(player) == []


def test_list_riichi_candidates_when_not_tenpai():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11p111s")
    assert resolver.list_riichi_candidates(player) == [Riichi()]

    player.juntehai = HaiGroup.from_code("123456789m11p159s")
    assert resolver.list_riichi_candidates(player) == []


def test_list_ankan_candidates():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, "../data/resolvers/teban_action_resolver/ankan.pickle.gz")
    with gzip.open(filepath, "rb") as f:
        test_cases = pickle.load(f)

    for test_case in test_cases:
        juntehai = HaiGroup.from_list(test_case["juntehai"])
        hais = HaiGroup.from_list(test_case["hais"])

        player.juntehai = juntehai
        player.last_tsumo = juntehai[-1]

        candidates = map(simplify_huuro, resolver.list_ankan_candidates(player))
        expected = simplify_huuro(Ankan(hais=hais))

        assert expected in candidates


def test_list_ankan_candidates_right_after_calling_riichi():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("0555m7z")
    player.last_tsumo = HaiGroup.from_code("0m")[0]

    assert len(resolver.list_ankan_candidates(player)) == 1

    player.riichi()
    assert len(resolver.list_ankan_candidates(player)) == 0


def test_list_ankan_candidates_when_yama_is_not_enough():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("0555m7z")
    player.last_tsumo = HaiGroup.from_code("0m")[0]

    game.yama.tsumo_hais = [Hai(i) for i in range(1)]
    assert len(resolver.list_ankan_candidates(player)) == 1

    game.yama.tsumo_hais = []
    assert len(resolver.list_ankan_candidates(player)) == 0


def test_list_ankan_candidates_when_four_kans_exist():
    game = game_factory()
    player1 = game.players[0]
    player2 = game.players[1]
    resolver = game.teban_action_resolver

    player1.juntehai = HaiGroup.from_code("0555m7z")
    player1.last_tsumo = HaiGroup.from_code("0m")[0]

    player2.huuros = []
    assert len(resolver.list_ankan_candidates(player1)) == 1

    player2.huuros = [
        Ankan(hais=HaiGroup.from_code("1111z")),
        Ankan(hais=HaiGroup.from_code("2222z")),
        Ankan(hais=HaiGroup.from_code("3333z")),
        Ankan(hais=HaiGroup.from_code("4444z")),
    ]
    assert len(resolver.list_ankan_candidates(player1)) == 0


def test_list_ankan_candidates_when_riichi_is_completed():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    # Ankan without tsumohai
    player.juntehai = HaiGroup.from_code("1111234m1112223z")
    player.last_tsumo = HaiGroup.from_code("4m")[0]

    player.is_riichi_completed = False
    assert len(resolver.list_ankan_candidates(player)) == 1

    player.is_riichi_completed = True
    assert len(resolver.list_ankan_candidates(player)) == 0

    # Ankan that changes shanten
    player.juntehai = HaiGroup.from_code("055567m11122233z")
    player.last_tsumo = HaiGroup.from_code("0m")[0]

    player.is_riichi_completed = False
    assert len(resolver.list_ankan_candidates(player)) == 1

    player.is_riichi_completed = True
    assert len(resolver.list_ankan_candidates(player)) == 0

    # Ankan that changes machihais
    player.juntehai = HaiGroup.from_code("05556m111222333z")
    player.last_tsumo = HaiGroup.from_code("0m")[0]

    player.is_riichi_completed = False
    assert len(resolver.list_ankan_candidates(player)) == 1

    player.is_riichi_completed = True
    assert len(resolver.list_ankan_candidates(player)) == 0

    # Ankan that does not change shanten and machihais
    player.juntehai = HaiGroup.from_code("05559m111222333z")
    player.last_tsumo = HaiGroup.from_code("0m")[0]

    player.is_riichi_completed = False
    assert len(resolver.list_ankan_candidates(player)) == 1

    player.is_riichi_completed = True
    assert len(resolver.list_ankan_candidates(player)) == 1


def test_list_kakan_candidates():
    game = game_factory()
    player = game.teban_player
    resolver = game.teban_action_resolver

    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, "../data/resolvers/teban_action_resolver/kakan.pickle.gz")
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

        candidates = map(simplify_huuro, resolver.list_kakan_candidates(player))
        expected = simplify_huuro(Kakan(hais=hais, stolen=stolen, added=added, from_who=from_who))

        assert expected in candidates


def test_list_kakan_candidates_when_yama_is_not_enough():
    game = game_factory()
    player = game.teban_player
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_list([3, 135])
    player.huuros = [Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)]

    game.yama.tsumo_hais = [Hai(i) for i in range(1)]
    assert len(resolver.list_kakan_candidates(player)) == 1

    game.yama.tsumo_hais = []
    assert len(resolver.list_kakan_candidates(player)) == 0


def test_list_kakan_candidates_when_four_kans_exist():
    game = game_factory()
    player1 = game.teban_player
    player2 = player1.kamicha
    resolver = game.teban_action_resolver

    player1.juntehai = HaiGroup.from_list([3, 135])
    player1.huuros = [Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)]

    player2.huuros = []
    assert len(resolver.list_kakan_candidates(player1)) == 1

    player2.huuros = [
        Ankan(hais=HaiGroup.from_code("1111z")),
        Ankan(hais=HaiGroup.from_code("2222z")),
        Ankan(hais=HaiGroup.from_code("3333z")),
        Ankan(hais=HaiGroup.from_code("4444z")),
    ]
    assert len(resolver.list_kakan_candidates(player1)) == 0


def test_list_dahai_candidates():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11p112s")
    assert resolver.list_dahai_candidates(player) == [Dahai(hai) for hai in HaiGroup.from_code("123456789m11p112s")]


def test_list_dahai_candidates_when_riichi_is_completed():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("123456789m11p112s")
    player.last_tsumo = HaiGroup.from_code("1m")[0]
    player.is_riichi_completed = True
    assert resolver.list_dahai_candidates(player) == [Dahai(hai) for hai in HaiGroup.from_code("1m")]


def test_list_dahai_candidates_right_after_calling_riichi():
    game = game_factory()
    player = game.players[0]
    resolver = game.teban_action_resolver

    player.juntehai = HaiGroup.from_code("12346666778899m")
    player.riichi()
    assert resolver.list_dahai_candidates(player) == [Dahai(hai) for hai in HaiGroup.from_code("14666699m")]


def test_list_dahai_candidates_right_after_calling_chii():
    game = game_factory()
    player1 = game.players[3]
    player2 = game.players[0]
    resolver = game.teban_action_resolver

    game.teban = 3
    player1.juntehai = HaiGroup.from_code("4m1112223334445z")
    game.teban_action_resolver.prepare()
    player1.dahai(Dahai(hai=HaiGroup.from_code("4m")[0]))

    player2.juntehai = HaiGroup.from_code("123m1112223334z")
    game.non_teban_action_resolver.prepare()
    player2.chii(Chii(hais=HaiGroup.from_code("234m"), stolen=HaiGroup.from_code("4m")[0]))
    assert resolver.list_dahai_candidates(player2) == [Dahai(hai) for hai in HaiGroup.from_code("1112223334z")]


def test_list_dahai_candidates_right_after_calling_pon():
    game = game_factory()
    player1 = game.players[3]
    player2 = game.players[0]
    resolver = game.teban_action_resolver

    game.teban = 3
    player1.juntehai = HaiGroup.from_code("0m1112223334445z")
    game.teban_action_resolver.prepare()
    player1.dahai(Dahai(hai=HaiGroup.from_code("0m")[0]))

    player2.juntehai = HaiGroup.from_code("555m1112223334z")
    game.non_teban_action_resolver.prepare()
    player2.pon(Pon(hais=HaiGroup.from_code("055m"), stolen=HaiGroup.from_code("0m")[0], from_who=Zaichi.KAMICHA))
    assert resolver.list_dahai_candidates(player2) == [Dahai(hai) for hai in HaiGroup.from_code("1112223334z")]
