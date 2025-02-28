import pytest

from kago_utils.hai import Hai


def test_init():
    for id in range(136):
        Hai(id)


def test_init_with_negative_id():
    with pytest.raises(ValueError):
        Hai(-1)


def test_init_with_too_large_id():
    with pytest.raises(ValueError):
        Hai(136)


def test_init_with_float_id():
    with pytest.raises(TypeError):
        Hai(0.0)


def test_suit():
    for id in range(36):
        assert Hai(id).suit == "m"
    for id in range(36, 72):
        assert Hai(id).suit == "p"
    for id in range(72, 108):
        assert Hai(id).suit == "s"
    for id in range(108, 136):
        assert Hai(id).suit == "z"


def test_number():
    for id in range(136):
        assert Hai(id).number == (id // 4) % 9 + 1


def test_color():
    assert Hai(15).color == "b"
    assert Hai(16).color == "r"
    assert Hai(51).color == "b"
    assert Hai(52).color == "r"
    assert Hai(87).color == "b"
    assert Hai(88).color == "r"


def test_code():
    codes = (
        ["1m"] * 4
        + ["2m"] * 4
        + ["3m"] * 4
        + ["4m"] * 4
        + ["0m"] * 1
        + ["5m"] * 3
        + ["6m"] * 4
        + ["7m"] * 4
        + ["8m"] * 4
        + ["9m"] * 4
        + ["1p"] * 4
        + ["2p"] * 4
        + ["3p"] * 4
        + ["4p"] * 4
        + ["0p"] * 1
        + ["5p"] * 3
        + ["6p"] * 4
        + ["7p"] * 4
        + ["8p"] * 4
        + ["9p"] * 4
        + ["1s"] * 4
        + ["2s"] * 4
        + ["3s"] * 4
        + ["4s"] * 4
        + ["0s"] * 1
        + ["5s"] * 3
        + ["6s"] * 4
        + ["7s"] * 4
        + ["8s"] * 4
        + ["9s"] * 4
        + ["1z"] * 4
        + ["2z"] * 4
        + ["3z"] * 4
        + ["4z"] * 4
        + ["5z"] * 4
        + ["6z"] * 4
        + ["7z"] * 4
    )
    for id in range(136):
        assert Hai(id).code == codes[id]


def test_comparison_with_hai():
    assert Hai(0) == Hai(0)
    assert Hai(0) != Hai(1)
    assert Hai(0) < Hai(1)
    assert Hai(0) <= Hai(0)
    assert Hai(1) > Hai(0)
    assert Hai(0) >= Hai(0)


def test_comparison_with_int():
    assert Hai(0) != 0


def test_repr():
    assert repr(Hai(0)) == "Hai(0)"
