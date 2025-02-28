import pytest

from kago_utils.actions import Daiminkan
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi


def test_init():
    Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)


def test_init_with_hais_having_same_hai():
    with pytest.raises(ValueError):
        Daiminkan(hais=HaiGroup.from_list([0, 0, 0, 0]), stolen=Hai(0), from_who=Zaichi.KAMICHA)


def test_init_with_hais_whose_length_is_not_4():
    with pytest.raises(ValueError):
        Daiminkan(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)


def test_init_with_not_same_name_hais():
    with pytest.raises(ValueError):
        Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 4]), stolen=Hai(0), from_who=Zaichi.KAMICHA)


def test_init_with_hais_which_not_contains_stolen():
    with pytest.raises(ValueError):
        Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(4), from_who=Zaichi.KAMICHA)


def test_init_with_from_jicha():
    with pytest.raises(ValueError):
        Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.JICHA)


def test_eq_with_same_daiminkan():
    daiminkan1 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    daiminkan2 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    assert daiminkan1 == daiminkan2


def test_eq_with_not_same_stolen():
    daiminkan1 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    daiminkan2 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(1), from_who=Zaichi.KAMICHA)
    assert daiminkan1 != daiminkan2


def test_eq_with_not_same_from_who():
    daiminkan1 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    daiminkan2 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.SHIMOCHA)
    assert daiminkan1 != daiminkan2


def test_eq_with_int():
    daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    assert daiminkan != 0


def test_repr():
    daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    assert (
        repr(daiminkan)
        == "Daiminkan(hais=HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)]), stolen=Hai(0), from_who=Zaichi.KAMICHA)"
    )
