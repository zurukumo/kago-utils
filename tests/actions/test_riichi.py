from kago_utils.actions import Riichi


def test_init():
    Riichi()


def test_eq_with_riichi():
    riichi1 = Riichi()
    riichi2 = Riichi()
    assert riichi1 == riichi2


def test_eq_with_int():
    riichi = Riichi()
    assert riichi != 0


def test_repr():
    riichi = Riichi()
    assert repr(riichi) == "Riichi()"
