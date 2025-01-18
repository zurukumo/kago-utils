import unittest

from kago_utils.actions import Kakan, Pon
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi


class TestInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_having_same_hai(self):
        with self.assertRaises(ValueError):
            Pon(hais=HaiGroup.from_list([0, 0, 0]), stolen=Hai(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_whose_length_is_not_3(self):
        with self.assertRaises(ValueError):
            Pon(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)

    def test_init_with_not_same_name_hais(self):
        with self.assertRaises(ValueError):
            Pon(hais=HaiGroup.from_list([0, 1, 4]), stolen=Hai(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_which_not_contains_stolen(self):
        with self.assertRaises(ValueError):
            Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(3), from_who=Zaichi.KAMICHA)

    def test_init_with_from_jicha(self):
        with self.assertRaises(ValueError):
            Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.JICHA)


class TestCanBecomeKakan(unittest.TestCase):
    def test_can_become_kakan_with_valid_kakan(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(3), from_who=Zaichi.KAMICHA)
        self.assertTrue(pon.can_become_kakan(kakan))

    def test_can_become_kakan_with_not_same_hais(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        kakan = Kakan(hais=HaiGroup.from_list([4, 5, 6, 7]), stolen=Hai(4), added=Hai(7), from_who=Zaichi.KAMICHA)
        self.assertFalse(pon.can_become_kakan(kakan))

    def test_can_become_kakan_with_not_same_stolen(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(1), added=Hai(3), from_who=Zaichi.KAMICHA)
        self.assertFalse(pon.can_become_kakan(kakan))

    def test_can_become_kakan_with_not_same_added(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(2), from_who=Zaichi.KAMICHA)
        self.assertFalse(pon.can_become_kakan(kakan))

    def test_can_become_kakan_with_not_same_from_who(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(3), from_who=Zaichi.SHIMOCHA)
        self.assertFalse(pon.can_become_kakan(kakan))


class TestToKakan(unittest.TestCase):
    def test_to_kakan(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        kakan = pon.to_kakan()
        self.assertEqual(
            kakan, Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(3), from_who=Zaichi.KAMICHA)
        )


class TestKuikaeHais(unittest.TestCase):
    def test_kuikae_hais(self):
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
            self.assertEqual(pon.kuikae_hais, expected)


class TestComparison(unittest.TestCase):
    def test_eq(self):
        pon1 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        pon2 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertEqual(pon1, pon2)

    def test_eq_with_not_same_hais(self):
        pon1 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        pon2 = Pon(hais=HaiGroup.from_list([0, 1, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(pon1, pon2)

    def test_eq_with_not_same_stolen(self):
        pon1 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        pon2 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(1), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(pon1, pon2)

    def test_eq_with_not_same_from_who(self):
        pon1 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        pon2 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.SHIMOCHA)
        self.assertNotEqual(pon1, pon2)

    def test_eq_with_int(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(pon, 0)


class TestRepr(unittest.TestCase):
    def test_repr(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertEqual(
            repr(pon), "Pon(hais=HaiGroup([Hai(0), Hai(1), Hai(2)]), stolen=Hai(0), from_who=Zaichi.KAMICHA)"
        )


if __name__ == "__main__":
    unittest.main()
