import unittest

from kago_utils.actions import Chii
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup


class TestInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))

    def test_init_with_hais_whose_length_is_not_3(self):
        with self.assertRaises(ValueError):
            Chii(hais=HaiGroup.from_list([0, 4, 8, 12]), stolen=Hai(0))

    def test_init_with_not_consecutive_hais(self):
        with self.assertRaises(ValueError):
            Chii(hais=HaiGroup.from_list([0, 4, 12]), stolen=Hai(0))

    def test_init_with_zihai(self):
        with self.assertRaises(ValueError):
            Chii(hais=HaiGroup.from_list([27 * 4, 28 * 4, 29 * 4]), stolen=Hai(27 * 4))

    def test_init_with_not_same_suit_hais(self):
        with self.assertRaises(ValueError):
            Chii(hais=HaiGroup.from_list([8 * 4, 9 * 4, 10 * 4]), stolen=Hai(8 * 4))

    def test_init_with_hais_which_not_contains_stolen(self):
        with self.assertRaises(ValueError):
            Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(1))


class TestKuikaeHais(unittest.TestCase):
    def test_kuikae_hais(self):
        # (hais, expected_when_left_hai_is_stolen, expected_when_middle_hai_is_stolen, expected_when_right_hai_is_stolen)
        test_cases = [
            (
                HaiGroup.from_code("123m"),
                HaiGroup.from_code("11114444m"),
                HaiGroup.from_code("2222m"),
                HaiGroup.from_code("3333m"),
            ),
            (
                HaiGroup.from_code("234m"),
                HaiGroup.from_code("22220555m"),
                HaiGroup.from_code("3333m"),
                HaiGroup.from_code("11114444m"),
            ),
            (
                HaiGroup.from_code("345m"),
                HaiGroup.from_code("33336666m"),
                HaiGroup.from_code("4444m"),
                HaiGroup.from_code("22220555m"),
            ),
            (
                HaiGroup.from_code("456m"),
                HaiGroup.from_code("44447777m"),
                HaiGroup.from_code("0555m"),
                HaiGroup.from_code("33336666m"),
            ),
            (
                HaiGroup.from_code("567m"),
                HaiGroup.from_code("05558888m"),
                HaiGroup.from_code("6666m"),
                HaiGroup.from_code("44447777m"),
            ),
            (
                HaiGroup.from_code("678m"),
                HaiGroup.from_code("66669999m"),
                HaiGroup.from_code("7777m"),
                HaiGroup.from_code("05558888m"),
            ),
            (
                HaiGroup.from_code("789m"),
                HaiGroup.from_code("7777m"),
                HaiGroup.from_code("8888m"),
                HaiGroup.from_code("66669999m"),
            ),
            (
                HaiGroup.from_code("123p"),
                HaiGroup.from_code("11114444p"),
                HaiGroup.from_code("2222p"),
                HaiGroup.from_code("3333p"),
            ),
            (
                HaiGroup.from_code("789s"),
                HaiGroup.from_code("7777s"),
                HaiGroup.from_code("8888s"),
                HaiGroup.from_code("66669999s"),
            ),
        ]

        for hais, expected1, expected2, expected3 in test_cases:
            chii = Chii(hais=hais, stolen=hais[0])
            self.assertEqual(chii.kuikae_hais, expected1)

            chii = Chii(hais=hais, stolen=hais[1])
            self.assertEqual(chii.kuikae_hais, expected2)

            chii = Chii(hais=hais, stolen=hais[2])
            self.assertEqual(chii.kuikae_hais, expected3)


class TestComparison(unittest.TestCase):
    def test_eq(self):
        chii1 = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))
        chii2 = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))
        self.assertEqual(chii1, chii2)

    def test_eq_with_not_same_hais(self):
        chii1 = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))
        chii2 = Chii(hais=HaiGroup.from_list([0, 4, 9]), stolen=Hai(0))
        self.assertNotEqual(chii1, chii2)

    def test_eq_with_not_same_stolen(self):
        chii1 = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))
        chii2 = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(4))
        self.assertNotEqual(chii1, chii2)

    def test_eq_with_int(self):
        chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))
        self.assertNotEqual(chii, 0)


class TestRepr(unittest.TestCase):
    def test_repr(self):
        chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))
        self.assertEqual(
            repr(chii), "Chii(hais=HaiGroup([Hai(0), Hai(4), Hai(8)]), stolen=Hai(0), from_who=Zaichi.KAMICHA)"
        )


if __name__ == "__main__":
    unittest.main()
