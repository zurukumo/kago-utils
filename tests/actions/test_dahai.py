from kago_utils.actions import Dahai
from kago_utils.hai import Hai


def test_init():
    Dahai(hai=Hai(0))


def test_eq_with_dahai():
    dahai1 = Dahai(hai=Hai(0))
    dahai2 = Dahai(hai=Hai(0))
    assert dahai1 == dahai2


def test_eq_with_dahai_having_different_hai():
    dahai1 = Dahai(hai=Hai(0))
    dahai2 = Dahai(hai=Hai(1))
    assert dahai1 != dahai2


def test_eq_with_int():
    dahai = Dahai(hai=Hai(0))
    assert dahai != 0


def test_repr():
    dahai = Dahai(hai=Hai(0))
    assert repr(dahai) == "Dahai(hai=Hai(0))"
