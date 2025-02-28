from kago_utils.actions import Ankan, Daiminkan, Kakan
from kago_utils.game import Game
from kago_utils.hai_group import HaiGroup
from kago_utils.player import Player
from kago_utils.zaichi import Zaichi


def test_bakaze():
    game = Game()

    for i in range(0, 4):
        game.kyoku = i
        assert game.bakaze == "東"

    for i in range(4, 8):
        game.kyoku = i
        assert game.bakaze == "南"

    for i in range(8, 12):
        game.kyoku = i
        assert game.bakaze == "西"

    for i in range(12, 16):
        game.kyoku = i
        assert game.bakaze == "北"


def test_teban_player():
    game = Game()
    for id in range(4):
        game.add_player(Player(str(id)))

    for i in range(4):
        game.teban = i
        assert game.teban_player == game.players[i]


def test_kan_count():
    game = Game()
    for id in range(4):
        game.add_player(Player(str(id)))

    assert game.kan_count == 0

    game.players[0].huuros = [
        Daiminkan(hais=HaiGroup.from_code("1111z"), stolen=HaiGroup.from_code("1z")[0], from_who=Zaichi.KAMICHA)
    ]
    assert game.kan_count == 1

    game.players[1].huuros = [
        Kakan(
            hais=HaiGroup.from_code("2222z"),
            stolen=HaiGroup.from_code("22z")[0],
            added=HaiGroup.from_code("22z")[1],
            from_who=Zaichi.KAMICHA,
        )
    ]
    assert game.kan_count == 2

    game.players[2].huuros = [Ankan(hais=HaiGroup.from_code("3333z")), Ankan(hais=HaiGroup.from_code("4444z"))]
    assert game.kan_count == 4
