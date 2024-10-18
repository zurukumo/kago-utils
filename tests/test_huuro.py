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

    def test_init_with_not_suuhai(self):
        with self.assertRaises(ValueError):
            Chii(hais=Hai136Group.from_list([27 * 4, 28 * 4, 29 * 4]), stolen=Hai136(27 * 4))

    def test_init_with_not_same_suit_hais(self):
        with self.assertRaises(ValueError):
            Chii(hais=Hai136Group.from_list([8 * 4, 9 * 4, 10 * 4]), stolen=Hai136(8 * 4))


class TestPonInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Pon(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_whose_length_is_not_3(self):
        with self.assertRaises(ValueError):
            Pon(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), from_who=Zaichi.TOIMEN)

    def test_init_with_not_same_face_hais(self):
        with self.assertRaises(ValueError):
            Pon(hais=Hai136Group.from_list([0, 1, 4]), stolen=Hai136(0), from_who=Zaichi.SIMOCHA)


class TestKakanInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Kakan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_whose_length_is_not_4(self):
        with self.assertRaises(ValueError):
            Kakan(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.TOIMEN)

    def test_init_with_not_same_face_hais(self):
        with self.assertRaises(ValueError):
            Kakan(hais=Hai136Group.from_list([0, 1, 2, 4]), stolen=Hai136(0), added=Hai136(1), from_who=Zaichi.SIMOCHA)


class TestDaiminkanInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 3]), stolen=Hai136(0), from_who=Zaichi.KAMICHA)

    def test_init_with_hais_whose_length_is_not_4(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=Hai136Group.from_list([0, 1, 2]), stolen=Hai136(0), from_who=Zaichi.TOIMEN)

    def test_init_with_not_same_face_hais(self):
        with self.assertRaises(ValueError):
            Daiminkan(hais=Hai136Group.from_list([0, 1, 2, 4]), stolen=Hai136(0), from_who=Zaichi.SIMOCHA)


class TestAnkanInit(unittest.TestCase):
    def test_init_with_valid_args(self):
        Ankan(hais=Hai136Group.from_list([0, 0, 0, 0]))

    def test_init_with_hais_whose_length_is_not_4(self):
        with self.assertRaises(ValueError):
            Ankan(hais=Hai136Group.from_list([0, 0, 0]))

    def test_init_with_not_same_face_hais(self):
        with self.assertRaises(ValueError):
            Ankan(hais=Hai136Group.from_list([0, 1, 2, 4]))
