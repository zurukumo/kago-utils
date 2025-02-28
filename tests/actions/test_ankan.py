import pytest

from kago_utils.actions import Ankan
from kago_utils.hai_group import HaiGroup


def test_init():
    Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))


def test_init_with_hais_having_same_hai():
    with pytest.raises(ValueError):
        Ankan(hais=HaiGroup.from_list([0, 0, 0, 0]))


def test_init_with_hais_whose_length_is_not_4():
    with pytest.raises(ValueError):
        Ankan(hais=HaiGroup.from_list([0, 1, 2]))


def test_init_with_not_same_name_hais():
    with pytest.raises(ValueError):
        Ankan(hais=HaiGroup.from_list([0, 1, 2, 4]))


def test_eq_with_same_ankan():
    ankan1 = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
    ankan2 = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
    assert ankan1 == ankan2


def test_eq_with_ankan_having_different_hais():
    ankan1 = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
    ankan2 = Ankan(hais=HaiGroup.from_list([4, 5, 6, 7]))
    assert ankan1 != ankan2


def test_eq_with_int():
    ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
    assert ankan != 0


def test_repr():
    ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
    assert repr(ankan) == "Ankan(hais=HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)]), from_who=Zaichi.JICHA)"
