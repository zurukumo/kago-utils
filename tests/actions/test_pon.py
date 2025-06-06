import pytest

from kago_utils.actions import Kakan, Pon
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi


def test_init():
    Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)


def test_init_with_hais_having_same_hai():
    with pytest.raises(ValueError):
        Pon(hais=HaiGroup.from_list([0, 0, 0]), stolen=Hai(0), from_who=Zaichi.KAMICHA)


def test_init_with_hais_whose_length_is_not_3():
    with pytest.raises(ValueError):
        Pon(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)


def test_init_with_not_same_name_hais():
    with pytest.raises(ValueError):
        Pon(hais=HaiGroup.from_list([0, 1, 4]), stolen=Hai(0), from_who=Zaichi.KAMICHA)


def test_init_with_hais_which_not_contains_stolen():
    with pytest.raises(ValueError):
        Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(3), from_who=Zaichi.KAMICHA)


def test_init_with_from_jicha():
    with pytest.raises(ValueError):
        Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.JICHA)


def test_can_become_kakan_with_valid_kakan():
    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(3), from_who=Zaichi.KAMICHA)
    assert pon.can_become_kakan(kakan)


def test_can_become_kakan_with_not_same_hais():
    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    kakan = Kakan(hais=HaiGroup.from_list([4, 5, 6, 7]), stolen=Hai(4), added=Hai(7), from_who=Zaichi.KAMICHA)
    assert not pon.can_become_kakan(kakan)


def test_can_become_kakan_with_not_same_stolen():
    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(1), added=Hai(3), from_who=Zaichi.KAMICHA)
    assert not pon.can_become_kakan(kakan)


def test_can_become_kakan_with_not_same_added():
    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(2), from_who=Zaichi.KAMICHA)
    assert not pon.can_become_kakan(kakan)


def test_can_become_kakan_with_not_same_from_who():
    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(3), from_who=Zaichi.SHIMOCHA)
    assert not pon.can_become_kakan(kakan)


def test_to_kakan():
    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    kakan = pon.to_kakan()
    assert kakan == Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(3), from_who=Zaichi.KAMICHA)


def test_is_similar_to():
    pon1 = Pon(hais=HaiGroup.from_list([16, 17, 19]), stolen=Hai(19), from_who=Zaichi.KAMICHA)
    pon2 = Pon(hais=HaiGroup.from_list([16, 18, 19]), stolen=Hai(19), from_who=Zaichi.KAMICHA)
    pon3 = Pon(hais=HaiGroup.from_list([17, 18, 19]), stolen=Hai(19), from_who=Zaichi.KAMICHA)

    assert pon1.is_similar_to(pon2)
    assert not pon1.is_similar_to(pon3)
    assert not pon2.is_similar_to(pon3)


def test_kuikae_hais():
    # (hais, expected)
    test_cases = [
        (HaiGroup.from_code("111m"), HaiGroup.from_code("1111m")),
        (HaiGroup.from_code("222m"), HaiGroup.from_code("2222m")),
        (HaiGroup.from_code("333m"), HaiGroup.from_code("3333m")),
        (HaiGroup.from_code("444m"), HaiGroup.from_code("4444m")),
        (HaiGroup.from_code("555m"), HaiGroup.from_code("0555m")),
        (HaiGroup.from_code("666m"), HaiGroup.from_code("6666m")),
        (HaiGroup.from_code("777m"), HaiGroup.from_code("7777m")),
        (HaiGroup.from_code("888m"), HaiGroup.from_code("8888m")),
        (HaiGroup.from_code("999m"), HaiGroup.from_code("9999m")),
        (HaiGroup.from_code("111p"), HaiGroup.from_code("1111p")),
        (HaiGroup.from_code("999p"), HaiGroup.from_code("9999p")),
        (HaiGroup.from_code("555z"), HaiGroup.from_code("5555z")),
    ]

    for hais, expected in test_cases:
        pon = Pon(hais=hais, stolen=hais[0], from_who=Zaichi.KAMICHA)
        assert pon.kuikae_hais == expected


def test_eq_with_same_pon():
    pon1 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    pon2 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    assert pon1 == pon2


def test_eq_with_not_same_hais():
    pon1 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    pon2 = Pon(hais=HaiGroup.from_list([0, 1, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    assert pon1 != pon2


def test_eq_with_not_same_stolen():
    pon1 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    pon2 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(1), from_who=Zaichi.KAMICHA)
    assert pon1 != pon2


def test_eq_with_not_same_from_who():
    pon1 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    pon2 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.SHIMOCHA)
    assert pon1 != pon2


def test_eq_with_int():
    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    assert pon != 0


def test_repr():
    pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
    assert repr(pon) == "Pon(hais=HaiGroup([Hai(0), Hai(1), Hai(2)]), stolen=Hai(0), from_who=Zaichi.KAMICHA)"
