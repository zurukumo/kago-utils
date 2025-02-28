import pytest

from kago_utils.actions import Kakan
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi


def test_init():
    Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)


def test_init_with_hais_having_same_hai():
    with pytest.raises(ValueError):
        Kakan(hais=HaiGroup.from_list([0, 0, 0, 0]), stolen=Hai(0), added=Hai(0), from_who=Zaichi.KAMICHA)


def test_init_with_hais_whose_length_is_not_4():
    with pytest.raises(ValueError):
        Kakan(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)


def test_init_with_not_same_name_hais():
    with pytest.raises(ValueError):
        Kakan(hais=HaiGroup.from_list([0, 1, 2, 4]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)


def test_init_with_hais_which_not_contains_stolen():
    with pytest.raises(ValueError):
        Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(4), added=Hai(1), from_who=Zaichi.KAMICHA)


def test_init_with_hais_which_not_contains_added():
    with pytest.raises(ValueError):
        Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(4), from_who=Zaichi.KAMICHA)


def test_init_with_from_jicha():
    with pytest.raises(ValueError):
        Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.JICHA)


def test_eq_with_same_kakan():
    kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
    kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
    assert kakan1 == kakan2


def test_eq_with_not_same_stolen():
    kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
    kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(1), added=Hai(1), from_who=Zaichi.KAMICHA)
    assert kakan1 != kakan2


def test_eq_with_not_same_added():
    kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
    kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(2), from_who=Zaichi.KAMICHA)
    assert kakan1 != kakan2


def test_eq_with_not_same_from_who():
    kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
    kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.SHIMOCHA)
    assert kakan1 != kakan2


def test_eq_with_int():
    kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
    assert kakan != 0


def test_repr():
    kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
    assert (
        repr(kakan)
        == "Kakan(hais=HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)"
    )
