import unittest

from kago_utils.hai import (Hai34Counter, Hai34List, Hai34String,
                            Hai136Counter, Hai136List)


class TestInit(unittest.TestCase):
    def test_hai34_counter_valid(self):
        data = [1] * 34
        Hai34Counter(data)

    def test_hai34_counter_too_short_length(self):
        data = [0] * 33
        with self.assertRaises(ValueError):
            Hai34Counter(data)

    def test_hai34_counter_too_long_length(self):
        data = [0] * 35
        with self.assertRaises(ValueError):
            Hai34Counter(data)

    def test_hai34_counter_negative_value(self):
        data = [-1] * 34
        with self.assertRaises(ValueError):
            Hai34Counter(data)

    def test_hai34_counter_float_value(self):
        data = [0.5] * 34
        with self.assertRaises(ValueError):
            Hai34Counter(data)

    def test_hai34_list_valid(self):
        data = [0]
        Hai34List(data)

    def test_hai34_list_negative_value(self):
        data = [-1]
        with self.assertRaises(ValueError):
            Hai34List(data)

    def test_hai34_list_too_large_value(self):
        data = [34]
        with self.assertRaises(ValueError):
            Hai34List(data)

    def test_hai34_list_float_value(self):
        data = [0.5]
        with self.assertRaises(ValueError):
            Hai34List(data)

    def test_hai34_string_valid(self):
        data = '123m'
        Hai34String(data)

    def test_hai34_string_invalid_format(self):
        data = '123m123'
        with self.assertRaises(ValueError):
            Hai34String(data)

    def test_hai34_string_invalid_character(self):
        data = '123x'
        with self.assertRaises(ValueError):
            Hai34String(data)

    def test_hai136_counter_valid(self):
        data = [1] * 136
        Hai136Counter(data)

    def test_hai136_counter_too_short_length(self):
        data = [1] * 135
        with self.assertRaises(ValueError):
            Hai136Counter(data)

    def test_hai136_counter_too_long_length(self):
        data = [1] * 137
        with self.assertRaises(ValueError):
            Hai136Counter(data)

    def test_hai136_counter_negative_value(self):
        data = [-1] * 136
        with self.assertRaises(ValueError):
            Hai136Counter(data)

    def test_hai136_counter_float_value(self):
        data = [0.5] * 136
        with self.assertRaises(ValueError):
            Hai136Counter(data)

    def test_hai136_list_valid(self):
        data = [0]
        Hai136List(data)

    def test_hai136_list_negative_value(self):
        data = [-1]
        with self.assertRaises(ValueError):
            Hai136List(data)

    def test_hai136_list_too_large_value(self):
        data = [136]
        with self.assertRaises(ValueError):
            Hai136List(data)

    def test_hai136_list_float_value(self):
        data = [0.5]
        with self.assertRaises(ValueError):
            Hai136List(data)


class TestConvert(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hai34_counter_data = [
            1, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 1, 1, 1, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1, 1, 1,
            2, 0, 0, 0, 0, 0, 0
        ]
        cls.hai136_counter_data = [
            1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
            1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
        cls.hai34_list_data = [0, 1, 2, 12, 13, 14, 24, 25, 26, 27, 27]
        cls.hai136_list_data = [0, 4, 8, 48, 52, 56, 96, 100, 104, 108, 109]
        cls.hai34_string_data = '123m456p789s11z'

    def test_hai34_counter_to_hai34_counter(self):
        result = Hai34Counter(self.hai34_counter_data).to_hai34_counter().data
        expected = self.hai34_counter_data
        self.assertEqual(result, expected)

    def test_hai34_counter_to_hai34_list(self):
        result = Hai34Counter(self.hai34_counter_data).to_hai34_list().data
        expected = self.hai34_list_data
        self.assertEqual(result, expected)

    def test_hai34_counter_to_hai34_string(self):
        result = Hai34Counter(self.hai34_counter_data).to_hai34_string().data
        expected = self.hai34_string_data
        self.assertEqual(result, expected)

    def test_hai34_list_to_hai34_counter(self):
        result = Hai34List(self.hai34_list_data).to_hai34_counter().data
        expected = self.hai34_counter_data
        self.assertEqual(result, expected)

    def test_hai34_list_to_hai34_list(self):
        result = Hai34List(self.hai34_list_data).to_hai34_list().data
        expected = self.hai34_list_data
        self.assertEqual(result, expected)

    def test_hai34_list_to_hai34_string(self):
        result = Hai34List(self.hai34_list_data).to_hai34_string().data
        expected = self.hai34_string_data
        self.assertEqual(result, expected)

    def test_hai34_string_to_hai34_counter(self):
        result = Hai34String(self.hai34_string_data).to_hai34_counter().data
        expected = self.hai34_counter_data
        self.assertEqual(result, expected)

    def test_hai34_string_to_hai34_list(self):
        result = Hai34String(self.hai34_string_data).to_hai34_list().data
        expected = self.hai34_list_data
        self.assertEqual(result, expected)

    def test_hai34_string_to_hai34_string(self):
        result = Hai34String(self.hai34_string_data).to_hai34_string().data
        expected = self.hai34_string_data
        self.assertEqual(result, expected)

    def test_hai136_counter_to_hai34_counter(self):
        result = Hai136Counter(self.hai136_counter_data).to_hai34_counter().data
        expected = self.hai34_counter_data
        self.assertEqual(result, expected)

    def test_hai136_counter_to_hai34_list(self):
        result = Hai136Counter(self.hai136_counter_data).to_hai34_list().data
        expected = self.hai34_list_data
        self.assertEqual(result, expected)

    def test_hai136_counter_to_hai34_string(self):
        result = Hai136Counter(self.hai136_counter_data).to_hai34_string().data
        expected = self.hai34_string_data
        self.assertEqual(result, expected)

    def test_hai136_counter_to_hai136_counter(self):
        result = Hai136Counter(self.hai136_counter_data).to_hai136_counter().data
        expected = self.hai136_counter_data
        self.assertEqual(result, expected)

    def test_hai136_counter_to_hai136_list(self):
        result = Hai136Counter(self.hai136_counter_data).to_hai136_list().data
        expected = self.hai136_list_data
        self.assertEqual(result, expected)

    def test_hai136_list_to_hai34_counter(self):
        result = Hai136List(self.hai136_list_data).to_hai34_counter().data
        expected = self.hai34_counter_data
        self.assertEqual(result, expected)

    def test_hai136_list_to_hai34_list(self):
        result = Hai136List(self.hai136_list_data).to_hai34_list().data
        expected = self.hai34_list_data
        self.assertEqual(result, expected)

    def test_hai136_list_to_hai34_string(self):
        result = Hai136List(self.hai136_list_data).to_hai34_string().data
        expected = self.hai34_string_data
        self.assertEqual(result, expected)

    def test_hai136_list_to_hai136_counter(self):
        result = Hai136List(self.hai136_list_data).to_hai136_counter().data
        expected = self.hai136_counter_data
        self.assertEqual(result, expected)

    def test_hai136_list_to_hai136_list(self):
        result = Hai136List(self.hai136_list_data).to_hai136_list().data
        expected = self.hai136_list_data
        self.assertEqual(result, expected)


class TestAdd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hai34_string1 = Hai34String('123m456p789s11z')
        cls.hai34_counter1 = cls.hai34_string1.to_hai34_counter()
        cls.hai34_list1 = cls.hai34_string1.to_hai34_list()
        cls.hai136_list1 = Hai136List([0, 4, 8, 48, 52, 56, 96, 100, 104, 108, 109])
        cls.hai136_counter1 = cls.hai136_list1.to_hai136_counter()

        cls.hai34_string2 = Hai34String('23m456p78s1z')
        cls.hai34_counter2 = cls.hai34_string2.to_hai34_counter()
        cls.hai34_list2 = cls.hai34_string2.to_hai34_list()
        cls.hai136_list2 = Hai136List([5, 9, 49, 53, 57, 97, 101, 110])
        cls.hai136_counter2 = cls.hai136_list2.to_hai136_counter()

        cls.hai34_string_sum = Hai34String('12233m445566p77889s111z')
        cls.hai34_counter_sum = cls.hai34_string_sum.to_hai34_counter()
        cls.hai34_list_sum = cls.hai34_string_sum.to_hai34_list()
        cls.hai136_list_sum = Hai136List([0, 4, 5, 8, 9, 48, 49, 52, 53, 56, 57, 96, 97, 100, 101, 104, 108, 109, 110])
        cls.hai136_counter_sum = cls.hai136_list_sum.to_hai136_counter()

    def test_add_hai34_counter_and_hai34_counter(self):
        result = self.hai34_counter1 + self.hai34_counter2
        expected = self.hai34_counter_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_counter_and_hai34_list(self):
        result = self.hai34_counter1 + self.hai34_list2
        expected = self.hai34_counter_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_counter_and_hai34_string(self):
        result = self.hai34_counter1 + self.hai34_string2
        expected = self.hai34_counter_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_counter_and_hai136_counter(self):
        result = self.hai34_counter1 + self.hai136_counter2
        expected = self.hai34_counter_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_counter_and_hai136_list(self):
        result = self.hai34_counter1 + self.hai136_list2
        expected = self.hai34_counter_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_counter_and_int(self):
        with self.assertRaises(TypeError):
            self.hai34_counter1 + 1

    def test_add_hai34_list_and_hai34_counter(self):
        result = self.hai34_list1 + self.hai34_counter2
        expected = self.hai34_list_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_list_and_hai34_list(self):
        result = self.hai34_list1 + self.hai34_list2
        expected = self.hai34_list_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_list_and_hai34_string(self):
        result = self.hai34_list1 + self.hai34_string2
        expected = self.hai34_list_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_list_and_hai136_counter(self):
        result = self.hai34_list1 + self.hai136_counter2
        expected = self.hai34_list_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_list_and_hai136_list(self):
        result = self.hai34_list1 + self.hai136_list2
        expected = self.hai34_list_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_list_and_int(self):
        with self.assertRaises(TypeError):
            self.hai34_list1 + 1

    def test_add_hai34_string_and_hai34_counter(self):
        result = self.hai34_string1 + self.hai34_counter2
        expected = self.hai34_string_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_string_and_hai34_list(self):
        result = self.hai34_string1 + self.hai34_list2
        expected = self.hai34_string_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_string_and_hai34_string(self):
        result = self.hai34_string1 + self.hai34_string2
        expected = self.hai34_string_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_string_and_hai136_counter(self):
        result = self.hai34_string1 + self.hai136_counter2
        expected = self.hai34_string_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_string_and_hai136_list(self):
        result = self.hai34_string1 + self.hai136_list2
        expected = self.hai34_string_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai34_string_and_int(self):
        with self.assertRaises(TypeError):
            self.hai34_string1 + 1

    def test_add_hai136_counter_and_hai136_counter(self):
        result = self.hai136_counter1 + self.hai136_counter2
        expected = self.hai136_counter_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai136_counter_and_hai136_list(self):
        result = self.hai136_counter1 + self.hai136_list2
        expected = self.hai136_counter_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai136_counter_and_int(self):
        with self.assertRaises(TypeError):
            self.hai136_counter1 + 1

    def test_add_hai136_list_and_hai136_counter(self):
        result = self.hai136_list1 + self.hai136_counter2
        expected = self.hai136_list_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai136_list_and_hai136_list(self):
        result = self.hai136_list1 + self.hai136_list2
        expected = self.hai136_list_sum
        self.assertEqual(result.data, expected.data)

    def test_add_hai136_list_and_int(self):
        hai136_list = self.hai136_list1
        with self.assertRaises(TypeError):
            hai136_list + 1


class TestSub(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hai34_string1 = Hai34String('123m456p789s11z')
        cls.hai34_counter1 = cls.hai34_string1.to_hai34_counter()
        cls.hai34_list1 = cls.hai34_string1.to_hai34_list()
        cls.hai136_list1 = Hai136List([0, 4, 8, 48, 52, 56, 96, 100, 104, 108, 109])
        cls.hai136_counter1 = cls.hai136_list1.to_hai136_counter()

        cls.hai34_string2 = Hai34String('23m456p78s1z')
        cls.hai34_counter2 = cls.hai34_string2.to_hai34_counter()
        cls.hai34_list2 = cls.hai34_string2.to_hai34_list()
        cls.hai136_list2 = Hai136List([4, 8, 48, 52, 56, 96, 100, 108])
        cls.hai136_counter2 = cls.hai136_list2.to_hai136_counter()

        cls.hai34_string_diff = Hai34String('1m9s1z')
        cls.hai34_counter_diff = cls.hai34_string_diff.to_hai34_counter()
        cls.hai34_list_diff = cls.hai34_string_diff.to_hai34_list()
        cls.hai136_list_diff = Hai136List([0, 104, 109])
        cls.hai136_counter_diff = cls.hai136_list_diff.to_hai136_counter()

    def test_sub_hai34_counter_and_hai34_counter(self):
        result = self.hai34_counter1 - self.hai34_counter2
        expected = self.hai34_counter_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_counter_and_hai34_list(self):
        result = self.hai34_counter1 - self.hai34_list2
        expected = self.hai34_counter_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_counter_and_hai34_string(self):
        result = self.hai34_counter1 - self.hai34_string2
        expected = self.hai34_counter_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_counter_and_hai136_counter(self):
        result = self.hai34_counter1 - self.hai136_counter2
        expected = self.hai34_counter_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_counter_and_hai136_list(self):
        result = self.hai34_counter1 - self.hai136_list2
        expected = self.hai34_counter_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_counter_and_hai34_counter_when_diff_is_negative(self):
        hai34_counter1 = Hai34Counter([0] * 34)
        hai34_counter2 = Hai34Counter([1] + [0] * 33)
        with self.assertRaises(ValueError):
            hai34_counter1 - hai34_counter2

    def test_sub_hai34_counter_and_int(self):
        with self.assertRaises(TypeError):
            self.hai34_counter1 - 1

    def test_sub_hai34_list_and_hai34_counter(self):
        result = self.hai34_list1 - self.hai34_counter2
        expected = self.hai34_list_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_list_and_hai34_list(self):
        result = self.hai34_list1 - self.hai34_list2
        expected = self.hai34_list_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_list_and_hai34_string(self):
        result = self.hai34_list1 - self.hai34_string2
        expected = self.hai34_list_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_list_and_hai136_counter(self):
        result = self.hai34_list1 - self.hai136_counter2
        expected = self.hai34_list_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_list_and_hai136_list(self):
        result = self.hai34_list1 - self.hai136_list2
        expected = self.hai34_list_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_list_and_hai34_counter_when_diff_is_negative(self):
        hai34_list = Hai34List([])
        hai34_counter = Hai34Counter([1] + [0] * 33)
        with self.assertRaises(ValueError):
            hai34_list - hai34_counter

    def test_sub_hai34_list_and_int(self):
        with self.assertRaises(TypeError):
            self.hai34_list1 - 1

    def test_sub_hai34_string_and_hai34_counter(self):
        result = self.hai34_string1 - self.hai34_counter2
        expected = self.hai34_string_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_string_and_hai34_list(self):
        result = self.hai34_string1 - self.hai34_list2
        expected = self.hai34_string_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_string_and_hai34_string(self):
        result = self.hai34_string1 - self.hai34_string2
        expected = self.hai34_string_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_string_and_hai136_counter(self):
        result = self.hai34_string1 - self.hai136_counter2
        expected = self.hai34_string_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_string_and_hai136_list(self):
        result = self.hai34_string1 - self.hai136_list2
        expected = self.hai34_string_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai34_string_and_hai34_counter_when_diff_is_negative(self):
        hai34_string = Hai34String('')
        hai34_counter = Hai34Counter([1] + [0] * 33)
        with self.assertRaises(ValueError):
            hai34_string - hai34_counter

    def test_sub_hai34_string_and_int(self):
        with self.assertRaises(TypeError):
            self.hai34_string1 - 1

    def test_sub_hai136_counter_and_hai136_counter(self):
        result = self.hai136_counter1 - self.hai136_counter2
        expected = self.hai136_counter_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai136_counter_and_hai136_list(self):
        result = self.hai136_counter1 - self.hai136_list2
        expected = self.hai136_counter_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai136_counter_and_hai136_counter_when_diff_is_negative(self):
        hai136_counter1 = Hai136Counter([0] * 136)
        hai136_counter2 = Hai136Counter([1] + [0] * 135)
        with self.assertRaises(ValueError):
            hai136_counter1 - hai136_counter2

    def test_sub_hai136_counter_and_int(self):
        with self.assertRaises(TypeError):
            self.hai136_counter1 - 1

    def test_sub_hai136_list_and_hai136_counter(self):
        result = self.hai136_list1 - self.hai136_counter2
        expected = self.hai136_list_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai136_list_and_hai136_list(self):
        result = self.hai136_list1 - self.hai136_list2
        expected = self.hai136_list_diff
        self.assertEqual(result.data, expected.data)

    def test_sub_hai136_list_and_hai136_counter_when_diff_is_negative(self):
        hai136_list = Hai136List([])
        hai136_counter = Hai136Counter([1] + [0] * 135)
        with self.assertRaises(ValueError):
            hai136_list - hai136_counter

    def test_sub_hai136_list_and_int(self):
        hai136_list = self.hai136_list1
        with self.assertRaises(TypeError):
            hai136_list + 1


class TestValidateAsJunTehai(unittest.TestCase):
    def test_valid_jun_tehai(self):
        Hai34String('11123455678999m').validate_as_jun_tehai()

    def test_jun_tehai_whose_length_is_not_invalid(self):
        with self.assertRaises(ValueError):
            Hai34String('111m').validate_as_jun_tehai()

    def test_jun_tehai_whose_length_is_too_long(self):
        with self.assertRaises(ValueError):
            Hai34String('111234556789999m').validate_as_jun_tehai()

    def test_jun_tehai_which_has_5th_hai(self):
        with self.assertRaises(ValueError):
            Hai34String('11111m').validate_as_jun_tehai()


if __name__ == '__main__':
    unittest.main()
