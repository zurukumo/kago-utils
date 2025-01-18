import unittest

from kago_utils.actions import Daiminkan
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi


class TestInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_having_same_hai(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=HaiGroup.from_list([0, 0, 0, 0]), stolen=Hai(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_whose_length_is_not_4(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)

    def test_init_with_not_same_name_hais(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 4]), stolen=Hai(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_which_not_contains_stolen(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(4), from_who=Zaichi.KAMICHA)

    def test_init_with_from_jicha(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.JICHA)


class TestComparison(unittest.TestCase):
    def test_eq(self):
        daiminkan1 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        daiminkan2 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertEqual(daiminkan1, daiminkan2)

    def test_eq_with_not_same_stolen(self):
        daiminkan1 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        daiminkan2 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(1), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(daiminkan1, daiminkan2)

    def test_eq_with_not_same_from_who(self):
        daiminkan1 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        daiminkan2 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.SHIMOCHA)
        self.assertNotEqual(daiminkan1, daiminkan2)

    def test_eq_with_int(self):
        daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(daiminkan, 0)


class TestRepr(unittest.TestCase):
    def test_repr(self):
        daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertEqual(
            repr(daiminkan),
            "Daiminkan(hais=HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)]), stolen=Hai(0), from_who=Zaichi.KAMICHA)",
        )


if __name__ == "__main__":
    unittest.main()
