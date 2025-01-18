import unittest

from kago_utils.actions import Kakan
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi


class TestInit(unittest.TestCase):
    def test(self):
        Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)

    def test_with_hais_having_same_hai(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 0, 0, 0]), stolen=Hai(0), added=Hai(0), from_who=Zaichi.KAMICHA)

    def test_with_hais_whose_length_is_not_4(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)

    def test_with_not_same_name_hais(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 4]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)

    def test_with_hais_which_not_contains_stolen(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(4), added=Hai(1), from_who=Zaichi.KAMICHA)

    def test_with_hais_which_not_contains_added(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(4), from_who=Zaichi.KAMICHA)

    def test_with_from_jicha(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.JICHA)


class TestEq(unittest.TestCase):
    def test_with_same_kakan(self):
        kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        self.assertEqual(kakan1, kakan2)

    def test_with_not_same_stolen(self):
        kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(1), added=Hai(1), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(kakan1, kakan2)

    def test_with_not_same_added(self):
        kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(2), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(kakan1, kakan2)

    def test_with_not_same_from_who(self):
        kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.SHIMOCHA)
        self.assertNotEqual(kakan1, kakan2)

    def test_with_int(self):
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(kakan, 0)


class TestRepr(unittest.TestCase):
    def test(self):
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        self.assertEqual(
            repr(kakan),
            "Kakan(hais=HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)",
        )


if __name__ == "__main__":
    unittest.main()
