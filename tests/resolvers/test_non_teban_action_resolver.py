import gzip
import os
import pickle

from kago_utils.actions import Ankan, Chii, Daiminkan, Pon, Ronho
from kago_utils.game import Game
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.player import Player
from kago_utils.zaichi import Zaichi


def setup_game():
    game = Game()
    game.yama.generate()
    game.kyoku = 0
    game.honba = 0
    game.kyoutaku = 0

    for i in range(4):
        player = Player(id=str(i))
        game.add_player(player)

    return game


def setup_last_dahai(teban: int, last_dahai: Hai):
    game = setup_game()
    game.teban = teban

    game.teban_player.last_dahai = last_dahai

    return game, game.players[0]


def test_list_ronho_candidates():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, HaiGroup.from_code("1m")[0])
    resolver = game.non_teban_action_resolver

    non_teban_player.juntehai = HaiGroup.from_code("23456789m11p123s")
    assert resolver.list_ronho_candidates(non_teban_player) == [Ronho()]


def test_list_ronho_candidates_when_nooten():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, HaiGroup.from_code("1m")[0])
    resolver = game.non_teban_action_resolver

    non_teban_player.juntehai = HaiGroup.from_code("23456789m11p123s")
    assert resolver.list_ronho_candidates(non_teban_player) == [Ronho()]

    non_teban_player.juntehai = HaiGroup.from_code("23456789m11p122s")
    assert resolver.list_ronho_candidates(non_teban_player) == []


def test_list_daiminkan_candidates():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, "../data/resolvers/non_teban_action_resolver/daiminkan.pickle.gz")
    with gzip.open(filepath, "rb") as f:
        test_cases = pickle.load(f)

    for test_case in test_cases:
        juntehai = HaiGroup.from_list(test_case["juntehai"])
        hais = HaiGroup.from_list(test_case["hais"])
        stolen = Hai(test_case["stolen"])
        from_who = Zaichi(test_case["from_who"])

        game, non_teban_player = setup_last_dahai(from_who.value, stolen)
        resolver = game.non_teban_action_resolver

        non_teban_player.juntehai = juntehai

        candidates = resolver.list_daiminkan_candidates(non_teban_player)
        expected = Daiminkan(hais=hais, stolen=stolen, from_who=from_who)

        assert expected in candidates


def test_list_daiminkan_candidates_when_yama_is_not_enough():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, Hai(3))
    resolver = game.non_teban_action_resolver

    non_teban_player.juntehai = HaiGroup.from_list([0, 1, 2, 135])

    game.yama.tsumo_hais = [Hai(i) for i in range(1)]
    assert len(resolver.list_daiminkan_candidates(non_teban_player)) == 1

    game.yama.tsumo_hais = []
    assert len(resolver.list_daiminkan_candidates(non_teban_player)) == 0


def test_list_daiminkan_candidates_when_riichi_is_completed():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, Hai(3))
    resolver = game.non_teban_action_resolver

    non_teban_player.juntehai = HaiGroup.from_list([0, 1, 2, 135])

    non_teban_player.is_riichi_completed = False
    assert len(resolver.list_daiminkan_candidates(non_teban_player)) == 1

    non_teban_player.is_riichi_completed = True
    assert len(resolver.list_daiminkan_candidates(non_teban_player)) == 0


def test_list_daiminkan_candidates_when_four_kans_exist():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, Hai(3))
    resolver = game.non_teban_action_resolver

    non_teban_player.juntehai = HaiGroup.from_list([0, 1, 2, 135])
    non_teban_player.kamicha.last_dahai = Hai(3)
    game.teban = non_teban_player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

    assert len(resolver.list_daiminkan_candidates(non_teban_player)) == 1

    non_teban_player.huuros = [Ankan(hais=HaiGroup.from_code("1111z"))]
    non_teban_player.kamicha.huuros = [Ankan(hais=HaiGroup.from_code("2222z"))]
    non_teban_player.toimen.huuros = [Ankan(hais=HaiGroup.from_code("3333z"))]
    non_teban_player.shimocha.huuros = [Ankan(hais=HaiGroup.from_code("4444z"))]
    assert len(resolver.list_daiminkan_candidates(non_teban_player)) == 0


def test_list_pon_candidates():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, "../data/resolvers/non_teban_action_resolver/pon.pickle.gz")
    with gzip.open(filepath, "rb") as f:
        test_cases = pickle.load(f)

    for test_case in test_cases:
        juntehai = HaiGroup.from_list(test_case["juntehai"])
        hais = HaiGroup.from_list(test_case["hais"])
        stolen = Hai(test_case["stolen"])
        from_who = Zaichi(test_case["from_who"])

        game, non_teban_player = setup_last_dahai(from_who.value, stolen)
        resolver = game.non_teban_action_resolver

        non_teban_player.juntehai = juntehai

        candidates = resolver.list_pon_candidates(non_teban_player)
        expected = Pon(hais=hais, stolen=stolen, from_who=from_who)

        assert any(expected.is_similar_to(candidate) for candidate in candidates)


def test_list_pon_candidates_when_yama_is_not_enough():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, Hai(2))
    resolver = game.non_teban_action_resolver

    non_teban_player.juntehai = HaiGroup.from_list([0, 1, 134, 135])
    game.teban = non_teban_player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

    game.yama.tsumo_hais = [Hai(i) for i in range(1)]
    assert len(resolver.list_pon_candidates(non_teban_player)) == 1

    game.yama.tsumo_hais = []
    assert len(resolver.list_pon_candidates(non_teban_player)) == 0


def test_list_pon_candidates_when_riichi_is_completed():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, Hai(2))
    resolver = game.non_teban_action_resolver

    non_teban_player.juntehai = HaiGroup.from_list([0, 1, 134, 135])
    game.teban = non_teban_player.get_zaseki_from_zaichi(Zaichi.KAMICHA)

    non_teban_player.is_riichi_completed = False
    assert len(resolver.list_pon_candidates(non_teban_player)) == 1

    non_teban_player.is_riichi_completed = True
    assert len(resolver.list_pon_candidates(non_teban_player)) == 0


def test_list_chii_candidates():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, "../data/resolvers/non_teban_action_resolver/chii.pickle.gz")
    with gzip.open(filepath, "rb") as f:
        test_cases = pickle.load(f)

    for test_case in test_cases:
        juntehai = HaiGroup.from_list(test_case["juntehai"])
        hais = HaiGroup.from_list(test_case["hais"])
        stolen = Hai(test_case["stolen"])
        from_who = Zaichi(test_case["from_who"])

        game, non_teban_player = setup_last_dahai(from_who.value, stolen)
        resolver = game.non_teban_action_resolver

        non_teban_player.juntehai = juntehai

        candidates = resolver.list_chii_candidates(non_teban_player)
        expected = Chii(hais=hais, stolen=stolen)

        assert any(expected.is_similar_to(candidate) for candidate in candidates)


def test_list_chii_candidates_when_yama_is_not_enough():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, Hai(8))
    resolver = game.non_teban_action_resolver

    non_teban_player.juntehai = HaiGroup.from_list([0, 4, 134, 135])

    game.yama.tsumo_hais = [Hai(i) for i in range(1)]
    assert len(resolver.list_chii_candidates(non_teban_player)) == 1

    game.yama.tsumo_hais = []
    assert len(resolver.list_chii_candidates(non_teban_player)) == 0


def test_list_chii_candidates_when_riichi_is_completed():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, Hai(8))
    resolver = game.non_teban_action_resolver

    non_teban_player.juntehai = HaiGroup.from_list([0, 4, 134, 135])

    non_teban_player.is_riichi_completed = False
    assert len(resolver.list_chii_candidates(non_teban_player)) == 1

    non_teban_player.is_riichi_completed = True
    assert len(resolver.list_chii_candidates(non_teban_player)) == 0


def test_list_chii_candidates_when_cannot_dahai_after_chii():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, Hai(8))
    resolver = game.non_teban_action_resolver

    non_teban_player.juntehai = HaiGroup.from_list([0, 4, 8, 9, 133, 134, 135])
    assert len(resolver.list_chii_candidates(non_teban_player)) == 1

    non_teban_player.juntehai = HaiGroup.from_list([0, 4, 8, 9])
    assert len(resolver.list_chii_candidates(non_teban_player)) == 0


def test_list_chii_candidates_after_non_kamicha_player_dahai():
    game, non_teban_player = setup_last_dahai(Zaichi.KAMICHA.value, Hai(8))
    resolver = game.non_teban_action_resolver
    non_teban_player.juntehai = HaiGroup.from_list([0, 4, 133, 134, 135])
    assert len(resolver.list_chii_candidates(non_teban_player)) == 1

    game, non_teban_player = setup_last_dahai(Zaichi.TOIMEN.value, Hai(8))
    resolver = game.non_teban_action_resolver
    non_teban_player.juntehai = HaiGroup.from_list([0, 4, 133, 134, 135])
    assert len(resolver.list_chii_candidates(non_teban_player)) == 0

    game, non_teban_player = setup_last_dahai(Zaichi.SHIMOCHA.value, Hai(8))
    resolver = game.non_teban_action_resolver
    non_teban_player.juntehai = HaiGroup.from_list([0, 4, 133, 134, 135])
    assert len(resolver.list_chii_candidates(non_teban_player)) == 0
