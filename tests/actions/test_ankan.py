import unittest

from kago_utils.actions import Ankan
from kago_utils.hai_group import HaiGroup


class TestInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))

    def test_init_with_hais_having_same_hai(self):
        with self.assertRaises(ValueError):
            Ankan(hais=HaiGroup.from_list([0, 0, 0, 0]))

    def test_init_with_hais_whose_length_is_not_4(self):
        with self.assertRaises(ValueError):
            Ankan(hais=HaiGroup.from_list([0, 1, 2]))

    def test_init_with_not_same_name_hais(self):
        with self.assertRaises(ValueError):
            Ankan(hais=HaiGroup.from_list([0, 1, 2, 4]))


class TestComparison(unittest.TestCase):
    def test_eq(self):
        ankan1 = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
        ankan2 = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
        self.assertEqual(ankan1, ankan2)

    def test_eq_with_int(self):
        ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
        self.assertNotEqual(ankan, 0)


class TestRepr(unittest.TestCase):
    def test_repr(self):
        ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
        self.assertEqual(repr(ankan), "Ankan(hais=HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)]), from_who=Zaichi.JICHA)")


if __name__ == "__main__":
    unittest.main()
