import unittest

from kago_utils.hai import Hai34, Hai136
from kago_utils.hai_group import Hai34Group, Hai136Group


class TestHai34GroupInit(unittest.TestCase):
    def test_init(self):
        Hai34Group([Hai34(0), Hai34(1), Hai34(32), Hai34(33)])


class TestHai136GroupInit(unittest.TestCase):
    def test_init(self):
        Hai136Group([Hai136(0), Hai136(1), Hai136(134), Hai136(135)])


class TestHai34GroupFromCounter(unittest.TestCase):
    def test_from_counter(self):
        counter = [0] * 34
        counter[0] = counter[33] = 1
        hais = [Hai34(0), Hai34(33)]
        self.assertEqual(Hai34Group.from_counter(counter), Hai34Group(hais))

    def test_from_counter_with_too_short_length(self):
        counter = [0] * 33
        with self.assertRaises(ValueError):
            Hai34Group.from_counter(counter)

    def test_from_counter_with_too_long_length(self):
        counter = [0] * 35
        with self.assertRaises(ValueError):
            Hai34Group.from_counter(counter)

    def test_from_counter_with_negative_value(self):
        counter = [-1] * 34
        with self.assertRaises(ValueError):
            Hai34Group.from_counter(counter)

    def test_from_counter_with_float_value(self):
        counter = [0.5] * 34
        with self.assertRaises(ValueError):
            Hai34Group.from_counter(counter)


class TestHai136GroupFromCounter136(unittest.TestCase):
    def test_from_counter136(self):
        counter = [0] * 136
        counter[0] = counter[135] = 1
        hais = [Hai136(0), Hai136(135)]
        self.assertEqual(Hai136Group.from_counter136(counter), Hai136Group(hais))

    def test_from_counter136_with_too_short_length(self):
        counter = [0] * 135
        with self.assertRaises(ValueError):
            Hai136Group.from_counter136(counter)

    def test_from_counter136_with_too_long_length(self):
        counter = [0] * 137
        with self.assertRaises(ValueError):
            Hai136Group.from_counter136(counter)

    def test_from_counter136_with_negative_value(self):
        counter = [-1] * 136
        with self.assertRaises(ValueError):
            Hai136Group.from_counter136(counter)

    def test_from_counter136_with_float_value(self):
        counter = [0.5] * 136
        with self.assertRaises(ValueError):
            Hai136Group.from_counter136(counter)


class TestHai34GroupFromList(unittest.TestCase):
    def test_from_list(self):
        _list = [0, 33]
        hais = [Hai34(0), Hai34(33)]
        self.assertEqual(Hai34Group.from_list(_list), Hai34Group(hais))

    def test_from_list_with_negative_value(self):
        _list = [-1]
        with self.assertRaises(ValueError):
            Hai34Group.from_list(_list)

    def test_from_list_with_too_large_value(self):
        _list = [34]
        with self.assertRaises(ValueError):
            Hai34Group.from_list(_list)

    def test_from_list_with_float_value(self):
        _list = [0.5]
        with self.assertRaises(ValueError):
            Hai34Group.from_list(_list)


class TestHai136GroupFromList136(unittest.TestCase):
    def test_from_list136(self):
        _list = [0, 135]
        hais = [Hai136(0), Hai136(135)]
        self.assertEqual(Hai136Group.from_list136(_list), Hai136Group(hais))

    def test_from_list136_with_negative_value(self):
        _list = [-1]
        with self.assertRaises(ValueError):
            Hai136Group.from_list136(_list)

    def test_from_list136_with_too_large_value(self):
        _list = [136]
        with self.assertRaises(ValueError):
            Hai136Group.from_list136(_list)

    def test_from_list136_with_float_value(self):
        _list = [0.5]
        with self.assertRaises(ValueError):
            Hai136Group.from_list136(_list)


class TestHai34GroupFromString(unittest.TestCase):
    def test_from_string(self):
        string = '1m7z'
        hais = [Hai34(0), Hai34(33)]
        self.assertEqual(Hai34Group.from_string(string), Hai34Group(hais))

    def test_from_string_with_invalid_format(self):
        string = '123'
        with self.assertRaises(ValueError):
            Hai34Group.from_string(string)

    def test_from_string_with_invalid_character(self):
        string = '1x'
        with self.assertRaises(ValueError):
            Hai34Group.from_string(string)


class TestHai136GroupFromString(unittest.TestCase):
    def test_from_string(self):
        testcases = [
            ('1m1p1s1z', [0, 36, 72, 108]),
            ('1234m', [0, 4, 8, 12]),
            ('1m', [0]),
            ('11m', [0, 1]),
            ('111m', [0, 1, 2]),
            ('1111m', [0, 1, 2, 3]),
            ('05m', [16, 17]),
            ('55m', [17, 18]),
            ('0m0p0s', [16, 52, 88]),
        ]

        for string, _list in testcases:
            self.assertEqual(Hai136Group.from_string(string), Hai136Group.from_list136(_list))

    def test_from_string_with_5_same_face_hai(self):
        string = '11111m'
        with self.assertRaises(ValueError):
            Hai136Group.from_string(string)

    def test_from_string_with_invalid_zihai(self):
        with self.assertRaises(ValueError):
            Hai136Group.from_string("0z")

        with self.assertRaises(ValueError):
            Hai136Group.from_string("8z")

        with self.assertRaises(ValueError):
            Hai136Group.from_string("9z")

    def test_from_string_with_invalid_format(self):
        string = '123'
        with self.assertRaises(ValueError):
            Hai136Group.from_string(string)

    def test_from_string_with_invalid_character(self):
        string = '1x'
        with self.assertRaises(ValueError):
            Hai136Group.from_string(string)


class TestHai34GroupToCounter(unittest.TestCase):
    def test_to_counter(self):
        hais = [Hai34(0), Hai34(33)]
        counter = [0] * 34
        counter[0] = counter[33] = 1
        self.assertEqual(Hai34Group(hais).to_counter(), counter)


class TestHai136GroupToCounter136(unittest.TestCase):
    def test_to_counter136(self):
        hais = [Hai136(0), Hai136(135)]
        counter = [0] * 136
        counter[0] = counter[135] = 1
        self.assertEqual(Hai136Group(hais).to_counter136(), counter)


class TestHai34GroupToList136(unittest.TestCase):
    def test_to_list(self):
        hais = [Hai34(0), Hai34(33)]
        _list = [0, 33]
        self.assertEqual(Hai34Group(hais).to_list(), _list)


class TestHai136GroupToList136(unittest.TestCase):
    def test_to_list136(self):
        hais = [Hai136(0), Hai136(135)]
        _list = [0, 135]
        self.assertEqual(Hai136Group(hais).to_list136(), _list)


class TestHai34GroupToString(unittest.TestCase):
    def test_to_string(self):
        hais = [Hai34(0), Hai34(33)]
        string = '1m7z'
        self.assertEqual(Hai34Group(hais).to_string(), string)


class TestHai136GroupToString(unittest.TestCase):
    def test_to_string(self):
        testcases = [
            ([Hai136(0), Hai136(135)], '1m7z'),
            ([Hai136(16), Hai136(52), Hai136(88)], '0m0p0s'),
            ([Hai136(0), Hai136(8), Hai136(16), Hai136(24), Hai136(32)], '13079m'),
            ([Hai136(0), Hai136(8), Hai136(17), Hai136(24), Hai136(32)], '13579m'),
        ]

        for hais, string in testcases:
            self.assertEqual(Hai136Group(hais).to_string(), string)


class TestHai34GroupValidate(unittest.TestCase):
    def test_validate(self):
        hai_group = Hai34Group.from_list([0, 0, 0])
        hai_group.validate()

    def test_validate_when_5th_hai_exists(self):
        hai_group = Hai34Group.from_list([0, 0, 0, 0, 0])
        with self.assertRaises(ValueError):
            hai_group.validate()


class TestHai136GroupValidate(unittest.TestCase):
    def test_validate(self):
        hai_group = Hai136Group.from_list136([0, 1, 2])
        hai_group.validate()

    def test_validate_when_2nd_hai_exists(self):
        hai_group = Hai136Group.from_list136([0, 0, 1, 2])
        with self.assertRaises(ValueError):
            hai_group.validate()


class TestHai34GroupValidateAsJunTehai(unittest.TestCase):
    def test_validate_as_jun_tehai(self):
        hai_group = Hai34Group.from_list(list(range(14)))
        hai_group.validate_as_jun_tehai()

    def test_validate_as_jun_tehai_when_length_is_not_invalid(self):
        hai_group = Hai34Group.from_list(list(range(3)))
        with self.assertRaises(ValueError):
            hai_group.validate_as_jun_tehai()

    def test_validate_as_jun_tehai_when_length_is_too_long(self):
        hai_group = Hai34Group.from_list(list(range(15)))
        with self.assertRaises(ValueError):
            hai_group.validate_as_jun_tehai()

    def test_validate_as_jun_tehai_when_5th_hai_exists(self):
        hai_group = Hai34Group.from_list(list(range(9)) + [9] * 5)
        with self.assertRaises(ValueError):
            hai_group.validate_as_jun_tehai()


class TestHai136GroupValidateAsJunTehai(unittest.TestCase):
    def test_validate_as_jun_tehai(self):
        hai_group = Hai136Group.from_list136(list(range(14)))
        hai_group.validate_as_jun_tehai()

    def test_validate_as_jun_tehai_when_length_is_not_invalid(self):
        hai_group = Hai136Group.from_list136(list(range(3)))
        with self.assertRaises(ValueError):
            hai_group.validate_as_jun_tehai()

    def test_validate_as_jun_tehai_when_length_is_too_long(self):
        hai_group = Hai136Group.from_list136(list(range(15)))
        with self.assertRaises(ValueError):
            hai_group.validate_as_jun_tehai()

    def test_validate_as_jun_tehai_when_2nd_hai_exists(self):
        hai_group = Hai136Group.from_list136(list(range(12)) + [12] * 2)
        with self.assertRaises(ValueError):
            hai_group.validate_as_jun_tehai()


class TestHai34GroupEq(unittest.TestCase):
    def test_eq(self):
        hai_group1 = Hai34Group([Hai34(1), Hai34(2)])
        hai_group2 = Hai34Group([Hai34(1), Hai34(2)])
        hai_group3 = Hai34Group([Hai34(2), Hai34(1)])
        hai_group4 = Hai34Group([Hai34(1), Hai34(3)])
        self.assertEqual(hai_group1, hai_group1)
        self.assertEqual(hai_group1, hai_group2)
        self.assertEqual(hai_group1, hai_group3)
        self.assertNotEqual(hai_group1, hai_group4)

    def test_eq_with_int(self):
        hai_group = Hai34Group([Hai34(1), Hai34(2)])
        self.assertNotEqual(hai_group, 1)


class TestHai136GroupEq(unittest.TestCase):
    def test_eq(self):
        hai_group1 = Hai136Group([Hai136(1), Hai136(2)])
        hai_group2 = Hai136Group([Hai136(1), Hai136(2)])
        hai_group3 = Hai136Group([Hai136(2), Hai136(1)])
        hai_group4 = Hai136Group([Hai136(1), Hai136(3)])
        self.assertEqual(hai_group1, hai_group1)
        self.assertEqual(hai_group1, hai_group2)
        self.assertEqual(hai_group1, hai_group3)
        self.assertNotEqual(hai_group1, hai_group4)

    def test_eq_with_int(self):
        hai_group = Hai136Group([Hai136(1), Hai136(2)])
        self.assertNotEqual(hai_group, 1)


class TestHai34GroupAdd(unittest.TestCase):
    def test_add_hai34_group_and_hai34(self):
        hai_group = Hai34Group([Hai34(0), Hai34(1)])
        hai = Hai34(2)
        hai_group_sum = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        self.assertEqual(hai_group + hai, hai_group_sum)

    def test_add_hai34_group_and_hai34_group(self):
        hai_group1 = Hai34Group([Hai34(0), Hai34(1)])
        hai_group2 = Hai34Group([Hai34(2), Hai34(3)])
        hai_group_sum = Hai34Group([Hai34(0), Hai34(1), Hai34(2), Hai34(3)])
        self.assertEqual(hai_group1 + hai_group2, hai_group_sum)

    def test_add_hai34_group_and_int(self):
        hai_group = Hai34Group([Hai34(0), Hai34(1)])
        with self.assertRaises(TypeError):
            hai_group + 1


class TestHai136GroupAdd(unittest.TestCase):
    def test_add_hai136_group_and_hai136(self):
        hai_group = Hai136Group([Hai136(0), Hai136(1)])
        hai = Hai136(2)
        hai_group_sum = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        self.assertEqual(hai_group + hai, hai_group_sum)

    def test_add_hai136_group_and_hai136_group(self):
        hai_group1 = Hai136Group([Hai136(0), Hai136(1)])
        hai_group2 = Hai136Group([Hai136(2), Hai136(3)])
        hai_group_sum = Hai136Group([Hai136(0), Hai136(1), Hai136(2), Hai136(3)])
        self.assertEqual(hai_group1 + hai_group2, hai_group_sum)

    def test_add_hai136_group_and_int(self):
        hai_group = Hai136Group([Hai136(0), Hai136(1)])
        with self.assertRaises(TypeError):
            hai_group + 1


class TestHai34GroupSub(unittest.TestCase):
    def test_sub_hai34_group_and_hai34(self):
        hai_group = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        hai = Hai34(2)
        hai_group_diff = Hai34Group([Hai34(0), Hai34(1)])
        self.assertEqual(hai_group - hai, hai_group_diff)

    def test_sub_hai34_group_and_hai34_group(self):
        hai_group1 = Hai34Group([Hai34(0), Hai34(1), Hai34(2), Hai34(3)])
        hai_group2 = Hai34Group([Hai34(2), Hai34(3)])
        hai_group_diff = Hai34Group([Hai34(0), Hai34(1)])
        self.assertEqual(hai_group1 - hai_group2, hai_group_diff)

    def test_sub_hai34_group_and_hai34_group_when_diff_is_negative(self):
        hai_group1 = Hai34Group([Hai34(0), Hai34(1)])
        hai_group2 = Hai34Group([Hai34(0), Hai34(2)])
        with self.assertRaises(ValueError):
            hai_group1 - hai_group2

    def test_sub_hai34_group_and_int(self):
        hai_group = Hai34Group([Hai34(0), Hai34(1)])
        with self.assertRaises(TypeError):
            hai_group - 1


class TestHai136GroupSub(unittest.TestCase):
    def test_sub_hai136_group_and_hai136(self):
        hai_group = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        hai = Hai136(2)
        hai_group_diff = Hai136Group([Hai136(0), Hai136(1)])
        self.assertEqual(hai_group - hai, hai_group_diff)

    def test_sub_hai136_group_and_hai136_group(self):
        hai_group1 = Hai136Group([Hai136(0), Hai136(1), Hai136(2), Hai136(3)])
        hai_group2 = Hai136Group([Hai136(2), Hai136(3)])
        hai_group_diff = Hai136Group([Hai136(0), Hai136(1)])
        self.assertEqual(hai_group1 - hai_group2, hai_group_diff)

    def test_sub_hai136_group_and_hai34_group(self):
        hai_group1 = Hai136Group([Hai136(0), Hai136(1), Hai136(2), Hai136(3)])
        hai_group2 = Hai34Group([Hai34(2), Hai34(3)])
        with self.assertRaises(TypeError):
            hai_group1 - hai_group2

    def test_sub_hai136_group_and_hai136_group_when_diff_is_negative(self):
        hai_group1 = Hai136Group([Hai136(0), Hai136(1)])
        hai_group2 = Hai136Group([Hai136(0), Hai136(2)])
        with self.assertRaises(ValueError):
            hai_group1 - hai_group2

    def test_sub_hai136_group_and_int(self):
        hai_group = Hai136Group([Hai136(0), Hai136(1)])
        with self.assertRaises(TypeError):
            hai_group - 1


class TestHai34GroupOr(unittest.TestCase):
    def test_or_hai34_group_and_hai34_group(self):
        hai_group1 = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        hai_group2 = Hai34Group([Hai34(1), Hai34(2), Hai34(3)])
        hai_group_union = Hai34Group([Hai34(0), Hai34(1), Hai34(2), Hai34(3)])
        self.assertEqual(hai_group1 | hai_group2, hai_group_union)

    def test_or_hai34_group_and_hai136_group(self):
        hai_group1 = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        hai_group2 = Hai136Group([Hai136(4), Hai136(8), Hai136(12)])
        hai_group_union = Hai34Group([Hai34(0), Hai34(1), Hai34(2), Hai34(3)])
        self.assertEqual(hai_group1 | hai_group2, hai_group_union)


class TestHai136GroupOr(unittest.TestCase):
    def test_or_hai136_group_and_hai136_group(self):
        hai_group1 = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        hai_group2 = Hai136Group([Hai136(1), Hai136(2), Hai136(3)])
        hai_group_union = Hai136Group([Hai136(0), Hai136(1), Hai136(2), Hai136(3)])
        self.assertEqual(hai_group1 | hai_group2, hai_group_union)

    def test_or_hai136_group_and_hai34_group(self):
        hai_group1 = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        hai_group2 = Hai34Group([Hai34(4), Hai34(8), Hai34(12)])
        with self.assertRaises(TypeError):
            hai_group1 | hai_group2


class TestHai34GroupAnd(unittest.TestCase):
    def test_and_hai34_group_and_hai34_group(self):
        hai_group1 = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        hai_group2 = Hai34Group([Hai34(1), Hai34(2), Hai34(3)])
        hai_group_intersection = Hai34Group([Hai34(1), Hai34(2)])
        self.assertEqual(hai_group1 & hai_group2, hai_group_intersection)

    def test_and_hai34_group_and_hai136_group(self):
        hai_group1 = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        hai_group2 = Hai136Group([Hai136(4), Hai136(8), Hai136(12)])
        hai_group_intersection = Hai34Group([Hai34(1), Hai34(2)])
        self.assertEqual(hai_group1 & hai_group2, hai_group_intersection)


class TestHai136GroupAnd(unittest.TestCase):
    def test_and_hai136_group_and_hai136_group(self):
        hai_group1 = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        hai_group2 = Hai136Group([Hai136(1), Hai136(2), Hai136(3)])
        hai_group_intersection = Hai136Group([Hai136(1), Hai136(2)])
        self.assertEqual(hai_group1 & hai_group2, hai_group_intersection)

    def test_and_hai136_group_and_hai34_group(self):
        hai_group1 = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        hai_group2 = Hai34Group([Hai34(4), Hai34(8), Hai34(12)])
        with self.assertRaises(TypeError):
            hai_group1 & hai_group2


class TestHai34GroupLen(unittest.TestCase):
    def test_len(self):
        hai_group = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        self.assertEqual(len(hai_group), 3)


class TestHai136GroupLen(unittest.TestCase):
    def test_len(self):
        hai_group = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        self.assertEqual(len(hai_group), 3)


class TestHai34GroupGetitem(unittest.TestCase):
    def test_getitem(self):
        hai_group = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        self.assertEqual(hai_group[0], Hai34(0))
        self.assertEqual(hai_group[1], Hai34(1))
        self.assertEqual(hai_group[2], Hai34(2))


class TestHai136GroupGetitem(unittest.TestCase):
    def test_getitem(self):
        hai_group = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        self.assertEqual(hai_group[0], Hai136(0))
        self.assertEqual(hai_group[1], Hai136(1))
        self.assertEqual(hai_group[2], Hai136(2))


class TestHai34GroupIter(unittest.TestCase):
    def test_iter(self):
        hai_group = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        for i, hai in enumerate(hai_group):
            self.assertEqual(hai, Hai34(i))


class TestHai136GroupIter(unittest.TestCase):
    def test_iter(self):
        hai_group = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        for i, hai in enumerate(hai_group):
            self.assertEqual(hai, Hai136(i))


class TestHai34GroupContains(unittest.TestCase):
    def test_contains(self):
        hai_group = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        self.assertEqual(Hai34(0) in hai_group, True)
        self.assertEqual(Hai34(3) in hai_group, False)

    def test_contais_with_int(self):
        hai_group = Hai34Group([Hai34(0), Hai34(1), Hai34(2)])
        with self.assertRaises(TypeError):
            0 in hai_group


class TestHai136GroupContains(unittest.TestCase):
    def test_contains(self):
        hai_group = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        self.assertEqual(Hai136(0) in hai_group, True)
        self.assertEqual(Hai136(3) in hai_group, False)

    def test_contains_with_int(self):
        hai_group = Hai136Group([Hai136(0), Hai136(1), Hai136(2)])
        with self.assertRaises(TypeError):
            0 in hai_group


if __name__ == '__main__':
    unittest.main()
