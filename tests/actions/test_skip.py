from kago_utils.actions import Skip


def test_init():
    Skip()


def test_eq_with_skip():
    skip1 = Skip()
    skip2 = Skip()
    assert skip1 == skip2


def test_eq_with_int():
    skip = Skip()
    assert skip != 0


def test_repr():
    skip = Skip()
    assert repr(skip) == "Skip()"
