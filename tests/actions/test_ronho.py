from kago_utils.actions import Ronho


def test_init():
    Ronho()


def test_eq_with_ronho():
    ronho1 = Ronho()
    ronho2 = Ronho()
    assert ronho1 == ronho2


def test_eq_with_int():
    ronho = Ronho()
    assert ronho != 0


def test_repr():
    ronho = Ronho()
    assert repr(ronho) == "Ronho()"
