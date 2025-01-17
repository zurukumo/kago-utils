import unittest

from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup


class TestInit(unittest.TestCase):
    def test_init(self):
        HaiGroup([Hai(0), Hai(1), Hai(134), Hai(135)])


class TestFromCounter34(unittest.TestCase):
    def test_from_counter34(self):
        counter = [0] * 34
        counter[0] = counter[33] = 1
        hais = [Hai(0), Hai(132)]
        self.assertEqual(HaiGroup.from_counter34(counter), HaiGroup(hais))

    def test_from_counter34_with_too_short_length(self):
        counter = [0] * 33
        with self.assertRaises(ValueError):
            HaiGroup.from_counter34(counter)

    def test_from_counter34_with_too_long_length(self):
        counter = [0] * 35
        with self.assertRaises(ValueError):
            HaiGroup.from_counter34(counter)

    def test_from_counter34_with_negative_value(self):
        counter = [-1] * 34
        with self.assertRaises(ValueError):
            HaiGroup.from_counter34(counter)

    def test_from_counter34_with_float_value(self):
        counter = [0.5] * 34
        with self.assertRaises(ValueError):
            HaiGroup.from_counter34(counter)


class TestFromCounter(unittest.TestCase):
    def test_from_counter(self):
        counter = [0] * 136
        counter[0] = counter[135] = 1
        hais = [Hai(0), Hai(135)]
        self.assertEqual(HaiGroup.from_counter(counter), HaiGroup(hais))

    def test_from_counter_with_too_short_length(self):
        counter = [0] * 135
        with self.assertRaises(ValueError):
            HaiGroup.from_counter(counter)

    def test_from_counter_with_too_long_length(self):
        counter = [0] * 137
        with self.assertRaises(ValueError):
            HaiGroup.from_counter(counter)

    def test_from_counter_with_negative_value(self):
        counter = [-1] * 136
        with self.assertRaises(ValueError):
            HaiGroup.from_counter(counter)

    def test_from_counter_with_float_value(self):
        counter = [0.5] * 136
        with self.assertRaises(ValueError):
            HaiGroup.from_counter(counter)


class TestFromList34(unittest.TestCase):
    def test_from_list34(self):
        _list = [0, 33]
        hais = [Hai(0), Hai(132)]
        self.assertEqual(HaiGroup.from_list34(_list), HaiGroup(hais))

    def test_from_list34_with_negative_value(self):
        _list = [-1]
        with self.assertRaises(ValueError):
            HaiGroup.from_list34(_list)

    def test_from_list34_with_too_large_value(self):
        _list = [34]
        with self.assertRaises(ValueError):
            HaiGroup.from_list34(_list)

    def test_from_list34_with_float_value(self):
        _list = [0.5]
        with self.assertRaises(ValueError):
            HaiGroup.from_list34(_list)


class TestFromList(unittest.TestCase):
    def test_from_list(self):
        _list = [0, 135]
        hais = [Hai(0), Hai(135)]
        self.assertEqual(HaiGroup.from_list(_list), HaiGroup(hais))

    def test_from_list_with_negative_value(self):
        _list = [-1]
        with self.assertRaises(ValueError):
            HaiGroup.from_list(_list)

    def test_from_list_with_too_large_value(self):
        _list = [136]
        with self.assertRaises(ValueError):
            HaiGroup.from_list(_list)

    def test_from_list_with_float_value(self):
        _list = [0.5]
        with self.assertRaises(ValueError):
            HaiGroup.from_list(_list)


class TestFromCode(unittest.TestCase):
    def test_from_code(self):
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
            self.assertEqual(HaiGroup.from_code(code), HaiGroup.from_list(_list))

    def test_from_code_with_5_same_name_hai(self):
        code = "11111m"
        with self.assertRaises(ValueError):
            HaiGroup.from_code(code)

    def test_from_code_with_invalid_zihai(self):
        with self.assertRaises(ValueError):
            HaiGroup.from_code("0z")

        with self.assertRaises(ValueError):
            HaiGroup.from_code("8z")

        with self.assertRaises(ValueError):
            HaiGroup.from_code("9z")

    def test_from_code_with_invalid_format(self):
        code = "123"
        with self.assertRaises(ValueError):
            HaiGroup.from_code(code)

    def test_from_code_with_invalid_character(self):
        code = "1x"
        with self.assertRaises(ValueError):
            HaiGroup.from_code(code)


class TestToCounter34(unittest.TestCase):
    def test_to_counter34(self):
        hais = [Hai(0), Hai(135)]
        counter = [0] * 34
        counter[0] = counter[33] = 1
        self.assertEqual(HaiGroup(hais).to_counter34(), counter)


class TestToCounter(unittest.TestCase):
    def test_to_counter(self):
        hais = [Hai(0), Hai(135)]
        counter = [0] * 136
        counter[0] = counter[135] = 1
        self.assertEqual(HaiGroup(hais).to_counter(), counter)


class TestToList34(unittest.TestCase):
    def test_to_list34(self):
        hais = [Hai(0), Hai(135)]
        _list = [0, 33]
        self.assertEqual(HaiGroup(hais).to_list34(), _list)


class TestToList(unittest.TestCase):
    def test_to_list(self):
        hais = [Hai(0), Hai(135)]
        _list = [0, 135]
        self.assertEqual(HaiGroup(hais).to_list(), _list)


class TestToCode(unittest.TestCase):
    def test_to_code(self):
        testcases = [
            ([Hai(0), Hai(135)], "1m7z"),
            ([Hai(16), Hai(52), Hai(88)], "0m0p0s"),
            ([Hai(0), Hai(8), Hai(16), Hai(24), Hai(32)], "13079m"),
            ([Hai(0), Hai(8), Hai(17), Hai(24), Hai(32)], "13579m"),
        ]

        for hais, code in testcases:
            self.assertEqual(HaiGroup(hais).to_code(), code)


class TestValidate(unittest.TestCase):
    def test_validate(self):
        hai_group = HaiGroup.from_list([0, 1, 2])
        hai_group.validate()

    def test_validate_when_2nd_hai_exists(self):
        hai_group = HaiGroup.from_list([0, 0, 1, 2])
        with self.assertRaises(ValueError):
            hai_group.validate()


class TestEq(unittest.TestCase):
    def test_eq(self):
        hai_group1 = HaiGroup([Hai(1), Hai(2)])
        hai_group2 = HaiGroup([Hai(1), Hai(2)])
        hai_group3 = HaiGroup([Hai(2), Hai(1)])
        hai_group4 = HaiGroup([Hai(1), Hai(3)])
        self.assertEqual(hai_group1, hai_group1)
        self.assertEqual(hai_group1, hai_group2)
        self.assertEqual(hai_group1, hai_group3)
        self.assertNotEqual(hai_group1, hai_group4)

    def test_eq_with_int(self):
        hai_group = HaiGroup([Hai(1), Hai(2)])
        self.assertNotEqual(hai_group, 1)


class TestAdd(unittest.TestCase):
    def test_add_hai_group_and_hai(self):
        hai_group = HaiGroup([Hai(0), Hai(1)])
        hai = Hai(2)
        hai_group_sum = HaiGroup([Hai(0), Hai(1), Hai(2)])
        self.assertEqual(hai_group + hai, hai_group_sum)

    def test_add_hai_group_and_hai_group(self):
        hai_group1 = HaiGroup([Hai(0), Hai(1)])
        hai_group2 = HaiGroup([Hai(2), Hai(3)])
        hai_group_sum = HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)])
        self.assertEqual(hai_group1 + hai_group2, hai_group_sum)

    def test_add_hai_group_and_int(self):
        hai_group = HaiGroup([Hai(0), Hai(1)])
        with self.assertRaises(TypeError):
            hai_group + 1


class TestSub(unittest.TestCase):
    def test_sub_hai_group_and_hai(self):
        hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
        hai = Hai(2)
        hai_group_diff = HaiGroup([Hai(0), Hai(1)])
        self.assertEqual(hai_group - hai, hai_group_diff)

    def test_sub_hai_group_and_hai_group(self):
        hai_group1 = HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)])
        hai_group2 = HaiGroup([Hai(2), Hai(3)])
        hai_group_diff = HaiGroup([Hai(0), Hai(1)])
        self.assertEqual(hai_group1 - hai_group2, hai_group_diff)

    def test_sub_hai_group_and_hai_group_when_diff_is_negative(self):
        hai_group1 = HaiGroup([Hai(0), Hai(1)])
        hai_group2 = HaiGroup([Hai(0), Hai(2)])
        with self.assertRaises(ValueError):
            hai_group1 - hai_group2

    def test_sub_hai_group_and_int(self):
        hai_group = HaiGroup([Hai(0), Hai(1)])
        with self.assertRaises(TypeError):
            hai_group - 1


class TestOr(unittest.TestCase):
    def test_or_hai_group_and_hai_group(self):
        hai_group1 = HaiGroup([Hai(0), Hai(1), Hai(2)])
        hai_group2 = HaiGroup([Hai(1), Hai(2), Hai(3)])
        hai_group_union = HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)])
        self.assertEqual(hai_group1 | hai_group2, hai_group_union)


class TestAnd(unittest.TestCase):
    def test_and_hai_group_and_hai_group(self):
        hai_group1 = HaiGroup([Hai(0), Hai(1), Hai(2)])
        hai_group2 = HaiGroup([Hai(1), Hai(2), Hai(3)])
        hai_group_intersection = HaiGroup([Hai(1), Hai(2)])
        self.assertEqual(hai_group1 & hai_group2, hai_group_intersection)


class TestLen(unittest.TestCase):
    def test_len(self):
        hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
        self.assertEqual(len(hai_group), 3)


class TestGetitem(unittest.TestCase):
    def test_getitem_with_int(self):
        hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
        self.assertEqual(hai_group[0], Hai(0))
        self.assertEqual(hai_group[1], Hai(1))
        self.assertEqual(hai_group[2], Hai(2))

    def test_getitem_with_slice(self):
        hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
        self.assertEqual(hai_group[:2], HaiGroup([Hai(0), Hai(1)]))
        self.assertEqual(hai_group[1:], HaiGroup([Hai(1), Hai(2)]))

    def test_getitem_with_float(self):
        hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
        with self.assertRaises(TypeError):
            hai_group[1.0]


class TestIter(unittest.TestCase):
    def test_iter(self):
        hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
        for i, hai in enumerate(hai_group):
            self.assertEqual(hai, Hai(i))


class TestContains(unittest.TestCase):
    def test_contains(self):
        hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
        self.assertEqual(Hai(0) in hai_group, True)
        self.assertEqual(Hai(3) in hai_group, False)

    def test_contains_with_int(self):
        hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
        with self.assertRaises(TypeError):
            0 in hai_group


class TestRepr(unittest.TestCase):
    def test_repr(self):
        hai_group = HaiGroup([Hai(0), Hai(1), Hai(2)])
        self.assertEqual(repr(hai_group), "HaiGroup([Hai(0), Hai(1), Hai(2)])")


if __name__ == "__main__":
    unittest.main()
