import unittest

from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.huuro import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.zaichi import Zaichi


class TestChiiInit(unittest.TestCase):
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


class TestPonInit(unittest.TestCase):
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


class TestKakanInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_having_same_hai(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 0, 0, 0]), stolen=Hai(0), added=Hai(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_whose_length_is_not_4(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)

    def test_init_with_not_same_name_hais(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 4]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_which_not_contains_stolen(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(4), added=Hai(1), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_which_not_contains_added(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(4), from_who=Zaichi.KAMICHA)

    def test_init_with_from_jicha(self):
        with self.assertRaises(ValueError):
            Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.JICHA)


class TestDaiminkanInit(unittest.TestCase):
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


class TestAnkanInit(unittest.TestCase):
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


class TestPonCanBecomeKakan(unittest.TestCase):
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
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(3), from_who=Zaichi.SIMOCHA)
        self.assertFalse(pon.can_become_kakan(kakan))


class TestPonToKakan(unittest.TestCase):
    def test_to_kakan(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        kakan = pon.to_kakan()
        self.assertEqual(
            kakan, Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(3), from_who=Zaichi.KAMICHA)
        )


class TestChiiComparison(unittest.TestCase):
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


class TestPonComparison(unittest.TestCase):
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
        pon2 = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.SIMOCHA)
        self.assertNotEqual(pon1, pon2)

    def test_eq_with_int(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(pon, 0)


class TestKakanComparison(unittest.TestCase):
    def test_eq(self):
        kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        self.assertEqual(kakan1, kakan2)

    def test_eq_with_not_same_stolen(self):
        kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(1), added=Hai(1), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(kakan1, kakan2)

    def test_eq_with_not_same_added(self):
        kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(2), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(kakan1, kakan2)

    def test_eq_with_not_same_from_who(self):
        kakan1 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.SIMOCHA)
        self.assertNotEqual(kakan1, kakan2)

    def test_eq_with_int(self):
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(kakan, 0)


class TestDaiminkanComparison(unittest.TestCase):
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
        daiminkan2 = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.SIMOCHA)
        self.assertNotEqual(daiminkan1, daiminkan2)

    def test_eq_with_int(self):
        daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(daiminkan, 0)


class TestAnkanComparison(unittest.TestCase):
    def test_eq(self):
        ankan1 = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
        ankan2 = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
        self.assertEqual(ankan1, ankan2)

    def test_eq_with_int(self):
        ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
        self.assertNotEqual(ankan, 0)


class TestChiiRepr(unittest.TestCase):
    def test_repr(self):
        chii = Chii(hais=HaiGroup.from_list([0, 4, 8]), stolen=Hai(0))
        self.assertEqual(
            repr(chii), "Chii(hais=HaiGroup([Hai(0), Hai(4), Hai(8)]), stolen=Hai(0), from_who=Zaichi.KAMICHA)"
        )


class TestPonRepr(unittest.TestCase):
    def test_repr(self):
        pon = Pon(hais=HaiGroup.from_list([0, 1, 2]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertEqual(
            repr(pon), "Pon(hais=HaiGroup([Hai(0), Hai(1), Hai(2)]), stolen=Hai(0), from_who=Zaichi.KAMICHA)"
        )


class TestKakanRepr(unittest.TestCase):
    def test_repr(self):
        kakan = Kakan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)
        self.assertEqual(
            repr(kakan),
            "Kakan(hais=HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)]), stolen=Hai(0), added=Hai(1), from_who=Zaichi.KAMICHA)",
        )


class TestDaiminkanRepr(unittest.TestCase):
    def test_repr(self):
        daiminkan = Daiminkan(hais=HaiGroup.from_list([0, 1, 2, 3]), stolen=Hai(0), from_who=Zaichi.KAMICHA)
        self.assertEqual(
            repr(daiminkan),
            "Daiminkan(hais=HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)]), stolen=Hai(0), from_who=Zaichi.KAMICHA)",
        )


class TestAnkanRepr(unittest.TestCase):
    def test_repr(self):
        ankan = Ankan(hais=HaiGroup.from_list([0, 1, 2, 3]))
        self.assertEqual(repr(ankan), "Ankan(hais=HaiGroup([Hai(0), Hai(1), Hai(2), Hai(3)]), from_who=Zaichi.JICHA)")


if __name__ == "__main__":
    unittest.main()
