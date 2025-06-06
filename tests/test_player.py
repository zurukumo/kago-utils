import pytest

from kago_utils.actions import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.game import Game
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.player import Player
from kago_utils.zaichi import Zaichi


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


def test_ankan():
    game = game_factory()
    game.teban = 0

    ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))

    player = game.players[0]
    player.juntehai = HaiGroup.from_list([0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
    player.last_tsumo = Hai(3)

    game.teban_action_resolver.prepare()
    player.ankan(ankan)
    assert ankan in player.huuros
    assert player.juntehai == HaiGroup.from_list([4, 5, 6, 8, 9, 10, 12, 13, 14, 16])


def test_ankan_with_invalid_ankan():
    game = game_factory()
    game.teban = 0

    ankan = Ankan(hais=HaiGroup.from_list([4, 5, 6, 7]))

    player = game.players[0]
    player.juntehai = HaiGroup.from_list([0, 1, 2, 3, 4, 8, 12, 108, 109, 110, 112, 113, 114, 115])
    player.last_tsumo = Hai(12)

    game.teban_action_resolver.prepare()
    with pytest.raises(ValueError):
        player.ankan(ankan)


def test_daiminkan():
    game = game_factory()
    game.teban = 3

    daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(3), from_who=Zaichi.KAMICHA)

    player = game.players[0]
    player.juntehai = HaiGroup.from_list([0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
    player.kamicha.last_dahai = Hai(3)

    game.non_teban_action_resolver.prepare()
    player.daiminkan(daiminkan)
    assert daiminkan in player.huuros
    assert player.juntehai == HaiGroup.from_list([4, 5, 6, 8, 9, 10, 12, 13, 14, 16])


def test_daiminkan_with_invalid_daiminkan():
    game = game_factory()
    game.teban = 3

    daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(2), from_who=Zaichi.KAMICHA)

    player = game.players[0]
    player.juntehai = HaiGroup.from_list([0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16])
    player.kamicha.last_dahai = Hai(3)

    game.non_teban_action_resolver.prepare()
    with pytest.raises(ValueError):
        player.daiminkan(daiminkan)


def test_kakan():
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
    assert kakan in player.huuros
    assert pon not in player.huuros
    assert player.juntehai == HaiGroup.from_list([4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25])


def test_kakan_with_invalid_kakan():
    game = game_factory()
    game.teban = 0

    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)
    kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(2), added=Hai(1), from_who=Zaichi.KAMICHA)

    player = game.players[0]
    player.juntehai = HaiGroup.from_list([3, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25])
    player.last_tsumo = Hai(3)
    player.huuros = [pon]

    game.teban_action_resolver.prepare()
    with pytest.raises(ValueError):
        player.kakan(kakan)


def test_pon():
    game = game_factory()
    game.teban = 3

    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(2), from_who=Zaichi.KAMICHA)

    player = game.players[0]
    player.juntehai = HaiGroup.from_list([0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24])
    player.kamicha.last_dahai = Hai(2)

    game.non_teban_action_resolver.prepare()
    player.pon(pon)
    assert pon in player.huuros
    assert player.juntehai == HaiGroup.from_list([4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24])


def test_pon_with_invalid_pon():
    game = game_factory()
    game.teban = 3

    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(1), from_who=Zaichi.KAMICHA)

    player = game.players[0]
    player.juntehai = HaiGroup.from_list([0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24])
    player.kamicha.last_dahai = Hai(2)

    game.non_teban_action_resolver.prepare()
    with pytest.raises(ValueError):
        player.pon(pon)


def test_chii():
    game = game_factory()
    game.teban = 3

    chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))

    player = game.players[0]
    player.juntehai = HaiGroup.from_list([4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52])
    player.kamicha.last_dahai = Hai(0)

    game.non_teban_action_resolver.prepare()
    player.chii(chii)
    assert chii in player.huuros
    assert player.juntehai == HaiGroup.from_list([12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52])


def test_chii_with_invalid_chii():
    game = game_factory()
    game.teban = 3

    chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(4))

    player = game.players[0]
    player.juntehai = HaiGroup.from_list([4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52])
    player.kamicha.last_dahai = Hai(0)

    game.non_teban_action_resolver.prepare()
    with pytest.raises(ValueError):
        player.chii(chii)


def test_is_menzen_without_huuros():
    game = game_factory()
    player = game.players[0]

    player.juntehai = HaiGroup.from_list(list(range(14)))
    assert player.is_menzen


def test_is_menzen_with_chii():
    game = game_factory()
    player = game.players[0]

    player.juntehai = HaiGroup.from_list(list(range(14)))
    player.huuros = [Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))]
    assert not (player.is_menzen)


def test_is_menzen_with_pon():
    game = game_factory()
    player = game.players[0]

    player.juntehai = HaiGroup.from_list(list(range(14)))
    player.huuros = [Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)]
    assert not player.is_menzen


def test_is_menzen_with_kakan():
    game = game_factory()
    player = game.players[0]

    player.juntehai = HaiGroup.from_list(list(range(14)))
    player.huuros = [
        Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
    ]
    assert not player.is_menzen


def test_is_menzen_with_daiminkan():
    game = game_factory()
    player = game.players[0]

    player.juntehai = HaiGroup.from_list(list(range(14)))
    player.huuros = [Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)]
    assert not player.is_menzen


def test_is_menzen_with_ankan():
    game = game_factory()
    player = game.players[0]

    player.juntehai = HaiGroup.from_list(list(range(14)))
    player.huuros = [Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))]
    assert player.is_menzen


def test_is_menzen_with_ankan_and_chii():
    game = game_factory()
    player = game.players[0]

    player.juntehai = HaiGroup.from_list(list(range(14)))
    player.huuros = [
        Ankan(hais=HaiGroup.from_list([0, 1, 2, 3])),
        Chii(hais=HaiGroup.from_list([4, 8, 12]), stolen=Hai(4)),
    ]
    assert not player.is_menzen


def test_jicha():
    game = game_factory()
    player = game.players[0]

    assert player.jicha == game.players[0]


def test_kamicha():
    game = game_factory()
    player = game.players[0]

    assert player.kamicha == game.players[3]


def test():
    game = game_factory()
    player = game.players[0]

    assert player.toimen == game.players[2]


def test_simocha():
    game = game_factory()
    player = game.players[0]

    assert player.shimocha == game.players[1]
