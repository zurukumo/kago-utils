import unittest

from kago_utils.hai import Hai136
from kago_utils.hai_group import Hai136Group
from kago_utils.huuro import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.zaichi import Zaichi


class TestChiiInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Chii(hais=Hai136Group.from_list([0, 4, 8]), stolen=Hai136(0))

    def test_init_with_hais_whose_length_is_not_3(self):
        with self.assertRaises(ValueError):
            Chii(hais=Hai136Group.from_list([0, 4, 8, 12]), stolen=Hai136(0))

    def test_init_with_not_consecutive_hais(self):
        with self.assertRaises(ValueError):
            Chii(hais=Hai136Group.from_list([0, 4, 12]), stolen=Hai136(0))

    def test_init_with_zihai(self):
        with self.assertRaises(ValueError):
            Chii(hais=Hai136Group.from_list([27 * 4, 28 * 4, 29 * 4]), stolen=Hai136(27 * 4))

    def test_init_with_not_same_suit_hais(self):
        with self.assertRaises(ValueError):
            Chii(hais=Hai136Group.from_list([8 * 4, 9 * 4, 10 * 4]), stolen=Hai136(8 * 4))

    def test_init_with_hais_which_not_contains_stolen(self):
        with self.assertRaises(ValueError):
            Chii(hais=Hai136Group.from_list([0, 4, 8]), stolen=Hai136(1))


class TestPonInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_having_same_hai(self):
        with self.assertRaises(ValueError):
            Pon(hais=Hai136Group.from_list([0, 0, 0]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_whose_length_is_not_3(self):
        with self.assertRaises(ValueError):
            Pon(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_not_same_face_hais(self):
        with self.assertRaises(ValueError):
            Pon(hais=Hai136Group.from_list([0, 1, 4]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_which_not_contains_stolen(self):
        with self.assertRaises(ValueError):
            Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(3), from_who=Zaichi.KAMICHA)

    def test_init_with_from_jicha(self):
        with self.assertRaises(ValueError):
            Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.JICHA)


class TestKakanInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_having_same_hai(self):
        with self.assertRaises(ValueError):
            Kakan(hais=Hai136Group.from_list([0, 0, 0, 0]), stolen=Hai136(0), added=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_whose_length_is_not_4(self):
        with self.assertRaises(ValueError):
            Kakan(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.KAMICHA)

    def test_init_with_not_same_face_hais(self):
        with self.assertRaises(ValueError):
            Kakan(hais=Hai136Group.from_list([0, 1, 2, 4]), stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_which_not_contains_stolen(self):
        with self.assertRaises(ValueError):
            Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(4), added=Hai136(1), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_which_not_contains_added(self):
        with self.assertRaises(ValueError):
            Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), added=Hai136(4), from_who=Zaichi.KAMICHA)

    def test_init_with_from_jicha(self):
        with self.assertRaises(ValueError):
            Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.JICHA)


class TestDaiminkanInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_having_same_hai(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=Hai136Group.from_list([0, 0, 0, 0]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_whose_length_is_not_4(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_not_same_face_hais(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 4]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_which_not_contains_stolen(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(4), from_who=Zaichi.KAMICHA)

    def test_init_with_from_jicha(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), from_who=Zaichi.JICHA)


class TestAnkanInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Ankan(hais=Hai136Group.from_list([0, 1, 2, 3]))

    def test_init_with_hais_having_same_hai(self):
        with self.assertRaises(ValueError):
            Ankan(hais=Hai136Group.from_list([0, 0, 0, 0]))

    def test_init_with_hais_whose_length_is_not_4(self):
        with self.assertRaises(ValueError):
            Ankan(hais=Hai136Group.from_list([0, 1, 2]))

    def test_init_with_not_same_face_hais(self):
        with self.assertRaises(ValueError):
            Ankan(hais=Hai136Group.from_list([0, 1, 2, 4]))


class TestChiiComparison(unittest.TestCase):
    def test_eq(self):
        chii1 = Chii(hais=Hai136Group.from_list([0, 4, 8]), stolen=Hai136(0))
        chii2 = Chii(hais=Hai136Group.from_list([0, 4, 8]), stolen=Hai136(0))
        self.assertEqual(chii1, chii2)

    def test_ne_with_not_same_hais(self):
        chii1 = Chii(hais=Hai136Group.from_list([0, 4, 8]), stolen=Hai136(0))
        chii2 = Chii(hais=Hai136Group.from_list([0, 4, 9]), stolen=Hai136(0))
        self.assertNotEqual(chii1, chii2)

    def test_ne_with_not_same_stolen(self):
        chii1 = Chii(hais=Hai136Group.from_list([0, 4, 8]), stolen=Hai136(0))
        chii2 = Chii(hais=Hai136Group.from_list([0, 4, 8]), stolen=Hai136(4))
        self.assertNotEqual(chii1, chii2)


class TestPonComparison(unittest.TestCase):
    def test_eq(self):
        pon1 = Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)
        pon2 = Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)
        self.assertEqual(pon1, pon2)

    def test_ne_with_not_same_hais(self):
        pon1 = Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)
        pon2 = Pon(hais=Hai136Group.from_list([0, 1, 3]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(pon1, pon2)

    def test_ne_with_not_same_stolen(self):
        pon1 = Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)
        pon2 = Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(1), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(pon1, pon2)

    def test_ne_with_not_same_from_who(self):
        pon1 = Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)
        pon2 = Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.SIMOCHA)
        self.assertNotEqual(pon1, pon2)


class TestKakanComparison(unittest.TestCase):
    def test_eq(self):
        kakan1 = Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]),
                       stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]),
                       stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.KAMICHA)
        self.assertEqual(kakan1, kakan2)

    def test_ne_with_not_same_stolen(self):
        kakan1 = Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]),
                       stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]),
                       stolen=Hai136(1), added=Hai136(1), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(kakan1, kakan2)

    def test_ne_with_not_same_added(self):
        kakan1 = Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]),
                       stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]),
                       stolen=Hai136(0), added=Hai136(2), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(kakan1, kakan2)

    def test_ne_with_not_same_from_who(self):
        kakan1 = Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]),
                       stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.KAMICHA)
        kakan2 = Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]),
                       stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.SIMOCHA)
        self.assertNotEqual(kakan1, kakan2)


class TestDaiminkanComparison(unittest.TestCase):
    def test_eq(self):
        daiminkan1 = Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)
        daiminkan2 = Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)
        self.assertEqual(daiminkan1, daiminkan2)

    def test_ne_with_not_same_stolen(self):
        daiminkan1 = Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)
        daiminkan2 = Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(1), from_who=Zaichi.KAMICHA)
        self.assertNotEqual(daiminkan1, daiminkan2)

    def test_ne_with_not_same_from_who(self):
        daiminkan1 = Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)
        daiminkan2 = Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), from_who=Zaichi.SIMOCHA)
        self.assertNotEqual(daiminkan1, daiminkan2)


class TestAnkanComparison(unittest.TestCase):
    def test_eq(self):
        ankan1 = Ankan(hais=Hai136Group.from_list([0, 1, 2, 3]))
        ankan2 = Ankan(hais=Hai136Group.from_list([0, 1, 2, 3]))
        self.assertEqual(ankan1, ankan2)
