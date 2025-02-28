from kago_utils.actions import Tsumoho


def test_init():
    Tsumoho()


def test_eq_with_tsumoho():
    tsumoho1 = Tsumoho()
    tsumoho2 = Tsumoho()
    assert tsumoho1 == tsumoho2


def test_eq_with_int():
    tsumoho = Tsumoho()
    assert tsumoho != 0


def test_repr():
    tsumoho = Tsumoho()
    assert repr(tsumoho) == "Tsumoho()"
