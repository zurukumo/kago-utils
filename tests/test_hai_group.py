import pytest

from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup


def test_init():
    HaiGroup([Hai(0), Hai(1), Hai(134), Hai(135)])


def test_from_counter34():
    counter = [0] * 34
    counter[0] = counter[33] = 1
    hais = [Hai(0), Hai(132)]
    assert HaiGroup.from_counter34(counter) == HaiGroup(hais)


def test_from_counter34_with_too_short_length():
    counter = [0] * 33
    with pytest.raises(ValueError):
        HaiGroup.from_counter34(counter)


def test_from_counter34_with_too_long_length():
    counter = [0] * 35
    with pytest.raises(ValueError):
        HaiGroup.from_counter34(counter)


def test_from_counter34_with_negative_value():
    counter = [-1] * 34
    with pytest.raises(ValueError):
        HaiGroup.from_counter34(counter)


def test_from_counter34_with_float_value():
    counter = [0.5] * 34
    with pytest.raises(ValueError):
        HaiGroup.from_counter34(counter)


def test_from_counter_():
    counter = [0] * 136
    counter[0] = counter[135] = 1
    hais = [Hai(0), Hai(135)]
    assert HaiGroup.from_counter(counter) == HaiGroup(hais)


def test_from_counter_with_too_short_length():
    counter = [0] * 135
    with pytest.raises(ValueError):
        HaiGroup.from_counter(counter)


def test_from_counter_with_too_long_length():
    counter = [0] * 137
    with pytest.raises(ValueError):
        HaiGroup.from_counter(counter)


def test_from_counter_with_negative_value():
    counter = [-1] * 136
    with pytest.raises(ValueError):
        HaiGroup.from_counter(counter)


def test_from_counter_with_float_value():
    counter = [0.5] * 136
    with pytest.raises(ValueError):
        HaiGroup.from_counter(counter)


def test_from_list_34():
    _list = [0, 33]
    hais = [Hai(0), Hai(132)]
    assert HaiGroup.from_list34(_list) == HaiGroup(hais)


def test_from_list_34_with_negative_value():
    _list = [-1]
    with pytest.raises(ValueError):
        HaiGroup.from_list34(_list)


def test_from_list_34_with_too_large_value():
    _list = [34]
    with pytest.raises(ValueError):
        HaiGroup.from_list34(_list)


def test_from_list_34_with_float_value():
    _list = [0.5]
    with pytest.raises(ValueError):
        HaiGroup.from_list34(_list)


def test_from_list():
    _list = [0, 135]
    hais = [Hai(0), Hai(135)]
    assert HaiGroup.from_list(_list) == HaiGroup(hais)


def test_from_list_with_negative_value():
    _list = [-1]
    with pytest.raises(ValueError):
        HaiGroup.from_list(_list)


def test_from_list_with_too_large_value():
    _list = [136]
    with pytest.raises(ValueError):
        HaiGroup.from_list(_list)


def test_from_list_with_float_value():
    _list = [0.5]
    with pytest.raises(ValueError):
        HaiGroup.from_list(_list)


def test_from_code():
    testcases = [
        ("1m1p1s1z", [0, 36, 72, 108]),
        ("1234m", [0, 4, 8, 12]),
        ("1m", [0]),
        ("11m", [0, 1]),
        ("111m", [0, 1, 2]),
        ("1111m", [0, 1, 2, 3]),
        ("05m", [16, 17]),
        ("55m", [17, 18]),
        ("0m0p0s", [16, 52, 88]),
    ]

    for code, _list in testcases:
        assert HaiGroup.from_code(code) == HaiGroup.from_list(_list)


def test_from_code_with_5_same_name_hai():
    code = "11111m"
    with pytest.raises(ValueError):
        HaiGroup.from_code(code)


def test_from_code_with_invalid_zihai():
    with pytest.raises(ValueError):
        HaiGroup.from_code("0z")

    with pytest.raises(ValueError):
        HaiGroup.from_code("8z")

    with pytest.raises(ValueError):
        HaiGroup.from_code("9z")


def test_from_code_with_invalid_format():
    code = "123"
    with pytest.raises(ValueError):
        HaiGroup.from_code(code)


def test_from_code_with_invalid_character():
    code = "1x"
    with pytest.raises(ValueError):
        HaiGroup.from_code(code)


def test_to_counter34():
    hais = [Hai(0), Hai(135)]
    counter = [0] * 34
    counter[0] = counter[33] = 1
    assert HaiGroup(hais).to_counter34() == counter


def test_to_counter():
    hais = [Hai(0), Hai(135)]
    counter = [0] * 136
    counter[0] = counter[135] = 1
    assert HaiGroup(hais).to_counter() == counter


def test_to_list34():
    hais = [Hai(0), Hai(135)]
    _list = [0, 33]
    assert HaiGroup(hais).to_list34() == _list


def test_to_list():
    hais = [Hai(0), Hai(135)]
    _list = [0, 135]
    assert HaiGroup(hais).to_list() == _list


def test_to_code():
    testcases = [
        ([Hai(0), Hai(135)], "1m7z"),
        ([Hai(16), Hai(52), Hai(88)], "0m0p0s"),
        ([Hai(0), Hai(8), Hai(16), Hai(24), Hai(32)], "13079m"),
        ([Hai(0), Hai(8), Hai(17), Hai(24), Hai(32)], "13579m"),
    ]

    for hais, code in testcases:
        assert HaiGroup(hais).to_code() == code


def test_validate():
    hai_group = HaiGroup.from_list([0, 1, 2])
    hai_group.validate()


def test_validate_when_2nd_hai_exists():
    hai_group = HaiGroup.from_list([0, 0, 1, 2])
    with pytest.raises(ValueError):
        hai_group.validate()


def test_eq_with_same_hai_group():
    hai_group1 = HaiGroup([Hai(1), Hai(2)])
    hai_group2 = HaiGroup([Hai(1), Hai(2)])
    hai_group3 = HaiGroup([Hai(2), Hai(1)])
    assert hai_group1 == hai_group1
    assert hai_group1 == hai_group2
    assert hai_group1 == hai_group3


def test_eq_with_not_same_hai_group():
    hai_group1 = HaiGroup([Hai(1), Hai(2)])
    hai_group2 = HaiGroup([Hai(1), Hai(3)])
    assert hai_group1 != hai_group2


def test_eq_with_int():
    hai_group = HaiGroup([Hai(1), Hai(2)])
    assert hai_group != 1


def test_add_with_hai():
    hai_group = HaiGroup([Hai(0), Hai(1)])
    hai = Hai(2)
    hai_group_sum = HaiGroup([Hai(0), Hai(1), Hai(2)])
    assert hai_group + hai == hai_group_sum


def test_add_with_hai_group():
    hai_group1 = HaiGroup([Hai(0), Hai(1)])
    hai_group2 = HaiGroup([Hai(2), Hai(3)])
    hai_group_sum = HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)])
    assert hai_group1 + hai_group2 == hai_group_sum


def test_add_with_int():
    hai_group = HaiGroup([Hai(0), Hai(1)])
    with pytest.raises(TypeError):
        hai_group + 1


def test_sub_with_hai():
    hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
    hai = Hai(2)
    hai_group_diff = HaiGroup([Hai(0), Hai(1)])
    assert hai_group - hai == hai_group_diff


def test_sub_with_hai_group():
    hai_group1 = HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)])
    hai_group2 = HaiGroup([Hai(2), Hai(3)])
    hai_group_diff = HaiGroup([Hai(0), Hai(1)])
    assert hai_group1 - hai_group2 == hai_group_diff


def test_sub_with_hai_group_when_diff_is_negative():
    hai_group1 = HaiGroup([Hai(0), Hai(1)])
    hai_group2 = HaiGroup([Hai(0), Hai(2)])
    with pytest.raises(ValueError):
        hai_group1 - hai_group2


def test_sub_with_int():
    hai_group = HaiGroup([Hai(0), Hai(1)])
    with pytest.raises(TypeError):
        hai_group - 1


def test_or_with_hai_group():
    hai_group1 = HaiGroup([Hai(0), Hai(1), Hai(2)])
    hai_group2 = HaiGroup([Hai(1), Hai(2), Hai(3)])
    hai_group_union = HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)])
    assert hai_group1 | hai_group2 == hai_group_union


def test_and_with_hai_group():
    hai_group1 = HaiGroup([Hai(0), Hai(1), Hai(2)])
    hai_group2 = HaiGroup([Hai(1), Hai(2), Hai(3)])
    hai_group_intersection = HaiGroup([Hai(1), Hai(2)])
    assert hai_group1 & hai_group2 == hai_group_intersection


def test_len():
    hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
    assert len(hai_group) == 3


def test_getitem_with_int():
    hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
    assert hai_group[0] == Hai(0)
    assert hai_group[1] == Hai(1)
    assert hai_group[2] == Hai(2)


def test_getitem_with_slice():
    hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
    assert hai_group[:2] == HaiGroup([Hai(0), Hai(1)])
    assert hai_group[1:] == HaiGroup([Hai(1), Hai(2)])


def test_getitem_with_float():
    hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
    with pytest.raises(TypeError):
        hai_group[1.0]


def test_iter():
    hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
    for i, hai in enumerate(hai_group):
        assert hai == Hai(i)


def test_contains_with_hai():
    hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
    assert Hai(0) in hai_group
    assert Hai(3) not in hai_group


def test_contains_with_int():
    hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
    with pytest.raises(TypeError):
        0 in hai_group


def test_repr():
    hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
    assert repr(hai_group) == "HaiGroup([Hai(0), Hai(1), Hai(2)])"
