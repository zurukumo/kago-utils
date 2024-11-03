import os
import random
import unittest

import numpy as np
from shanten_tools import shanten as external_shanten

from kago_utils.hai_group import Hai136Group
from kago_utils.shanten import Shanten


def generate_random_jun_tehai(jun_tehai_length: int):
    # manzu, pinzu, souzu and zihai
    yama = random.sample(range(34 * 4), jun_tehai_length)
    jun_tehai = Hai136Group.from_list136(yama)
    return jun_tehai


def generate_random_jun_tehai_for_honitsu(jun_tehai_length: int):
    # manzu and zihai
    yama = random.sample(list(range(9 * 4)) + list(range(27 * 4, 34 * 4)), jun_tehai_length)
    jun_tehai = Hai136Group.from_list136(yama)
    return jun_tehai


def generate_random_jun_tehai_for_chinitsu(jun_tehai_length: int):
    # manzu
    yama = random.sample(range(9 * 4), jun_tehai_length)
    jun_tehai = Hai136Group.from_list136(yama)
    return jun_tehai


def calculate_shanten_external(jun_tehai: Hai136Group):
    jun_tehai = jun_tehai.to_counter34()
    return external_shanten(np.array(jun_tehai, dtype=np.uint8)) - 1


class TestCalculateShantenWithRandomTehai(unittest.TestCase):
    n_assertion = 10000
    # format: (jun_tehai_length, n_huuro)
    tehai_patterns = [
        (14, 0),
        (13, 0),
        (11, 1),
        (10, 1),
        (8, 2),
        (7, 2),
        (5, 3),
        (4, 3),
        (2, 4),
        (1, 4)
    ]

    def test_shanten(self):
        for jun_tehai_length, n_huuro in self.tehai_patterns:
            for _ in range(self.n_assertion):
                jun_tehai = generate_random_jun_tehai(jun_tehai_length)
                result = Shanten(jun_tehai).shanten
                expected = calculate_shanten_external(jun_tehai)
                msg = f"jun_tehai: {jun_tehai.to_string()}, n_huuro: {n_huuro}"
                self.assertEqual(result, expected, msg)

    def test_shanten_honitsu(self):
        for jun_tehai_length, n_huuro in self.tehai_patterns:
            for _ in range(self.n_assertion):
                jun_tehai = generate_random_jun_tehai_for_honitsu(jun_tehai_length)
                result = Shanten(jun_tehai).shanten
                expected = calculate_shanten_external(jun_tehai)
                msg = f"jun_tehai: {jun_tehai.to_string()}, n_huuro: {n_huuro}"
                self.assertEqual(result, expected, msg)

    def test_shanten_chinitsu(self):
        for jun_tehai_length, n_huuro in self.tehai_patterns:
            for _ in range(self.n_assertion):
                jun_tehai = generate_random_jun_tehai_for_chinitsu(jun_tehai_length)
                result = Shanten(jun_tehai).shanten
                expected = calculate_shanten_external(jun_tehai)
                msg = f"jun_tehai: {jun_tehai.to_string()}, n_huuro: {n_huuro}"
                self.assertEqual(result, expected, msg)


# ref: https://mahjong.ara.black/etc/shanten/shanten9.htm
class TestCalculateShantenWithAraTehai(unittest.TestCase):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    p_normal_10000_txt = os.path.join(current_dir, 'data/p_normal_10000.txt')
    p_hon_10000_txt = os.path.join(current_dir, 'data/p_hon_10000.txt')
    p_tin_10000_txt = os.path.join(current_dir, 'data/p_tin_10000.txt')
    p_koku_10000_txt = os.path.join(current_dir, 'data/p_koku_10000.txt')

    def test_shanten_normal_10000(self):
        with open(self.p_normal_10000_txt, 'rb') as f:
            for row in f.readlines():
                problem = list(map(int, row.split()))
                jun_tehai = Hai136Group.from_list34(problem[:14])
                shanten = Shanten(jun_tehai)
                result = [shanten.regular_shanten, shanten.kokushimusou_shanten, shanten.chiitoitsu_shanten]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_string()}"
                self.assertEqual(result, expected, msg)

    def test_shanten_hon_10000(self):
        with open(self.p_hon_10000_txt, 'rb') as f:
            for row in f.readlines():
                problem = list(map(int, row.split()))
                jun_tehai = Hai136Group.from_list34(problem[:14])
                shanten = Shanten(jun_tehai)
                result = [shanten.regular_shanten, shanten.kokushimusou_shanten, shanten.chiitoitsu_shanten]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_string()}"
                self.assertEqual(result, expected, msg)

    def test_shanten_tin_10000(self):
        with open(self.p_tin_10000_txt, 'rb') as f:
            for row in f.readlines():
                problem = list(map(int, row.split()))
                jun_tehai = Hai136Group.from_list34(problem[:14])
                shanten = Shanten(jun_tehai)
                result = [shanten.regular_shanten, shanten.kokushimusou_shanten, shanten.chiitoitsu_shanten]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_string()}"
                self.assertEqual(result, expected, msg)

    def test_shanten_koku_10000(self):
        with open(self.p_koku_10000_txt, 'rb') as f:
            for row in f.readlines():
                problem = list(map(int, row.split()))
                jun_tehai = Hai136Group.from_list34(problem[:14])
                shanten = Shanten(jun_tehai)
                result = [shanten.regular_shanten, shanten.kokushimusou_shanten, shanten.chiitoitsu_shanten]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_string()}"
                self.assertEqual(result, expected, msg)


class TestCalculateShantenWithHandmadeTehai(unittest.TestCase):
    # format: (jun_tehai, expected)
    test_cases = [
        (Hai136Group.from_string('23466669999m111z'), 1),
        (Hai136Group.from_string('1111345567m111z'), 1)
    ]

    def test_shanten_when_jun_tehai_length_is_invalid(self):
        for jun_tehai, expected in self.test_cases:
            result = Shanten(jun_tehai).shanten
            msg = f"jun_tehai: {jun_tehai}"
            self.assertEqual(result, expected, msg)


class TestCalculateShantenWithInvalidTehai(unittest.TestCase):
    test_cases = [
        Hai136Group.from_string(''),
        Hai136Group.from_string('111m'),
        Hai136Group.from_string('111m111s'),
        Hai136Group.from_string('111m111s111p'),
        Hai136Group.from_string('111m111s111p111z'),
    ]

    def test_shanten(self):
        for jun_tehai in self.test_cases:
            with self.assertRaises(ValueError):
                Shanten(jun_tehai).shanten


class TestCalculateYuukouhaiWithHandmadeTehai(unittest.TestCase):
    # format: (jun_tehai, expected)
    string_test_cases: list[tuple[str, str]] = [
        # 13
        ('1111m257p578s156z', '22223333m1111222333344446666p3333444405566667778889999s111555666z'),
        ('2233m2267p1368s1z', '111122334444m2205556667778888p11122223336667777888s111z'),
        ('449m67p4568s1226z', '4477778888999m05558888p333366677778889999s11122666z'),
        ('2557m38p1578s237z', '222777m333888p111055777888s222333777z'),
        ('234m12p47s133466z', '3333p222233334440555666677788889999s1113344466z'),
        ('358m4579p6678s25z', '4444888m333366668888p669999s222555z'),
        ('124699m126p1s233z', '3333055599m3333p33z'),
        ('6688m117p699s134z', '777p666s111333444z'),
        ('123577m3479p79s6z', '222205558888p8888s'),
        ('179m4479p13444s5z', '8888m8888p2222s'),
        # 10
        ('34589m56p79s3z', '7777888999m44440556667777p7778888999s333z'),
        ('123m2p399s337z', '111122233334444p111122223334444055599s33777z'),
        ('1166m569p67s1z', '1166m44447777p05558888s'),
        ('267m47p66788s', '22205558888m444777p777s'),
        ('1355m11345p3s', '222205m11p'),
        # 7
        ('2m6p11s223z', '111122233334444m4444055566677778888p11s22333z'),
        ('13m6p358s1z', '2222m666p4444888s111z'),
        ('2p6s11557z', '111122233334444p4444055566677778888s1155777z'),
        ('4668m2p59s', '05557777m222p055999s'),
        ('88m569p89s', '44447777p7777s'),
        # 4
        ('1m9p2s5z', '11122223333m77778888999p111122233334444s555z'),
        ('1m28s6z', '11122223333m111122233334444666677778889999s666z'),
        ('2m99s1z', '111122233334444m99s111z'),
        ('05m29s', '55m11112223333444477778888999s'),
        ('4p678s', '444p'),
        # 1
        ('5m', '055m'),
        ('9p', '999p')
    ]

    list_test_cases: list[tuple[list[int], list[int]]] = [
        # 13
        ([12, 16, 20, 24, 25, 28, 32, 33, 44, 72, 76, 100, 101], [29, 30, 31, 80, 81, 82, 83]),
        ([0, 12, 20, 21, 24, 28, 36, 40, 80, 84, 92, 93, 96],
         [16, 17, 18, 19, 44, 45, 46, 47, 76, 77, 78, 79, 88, 89, 90, 91]),
        ([20, 28, 36, 40, 64, 72, 73, 92, 96, 100, 101, 128, 129], [24, 25, 26, 27, 44, 45, 46, 47, 74, 75, 130, 131]),
        ([4, 7, 8, 19, 47, 48, 54, 55, 57, 89, 99, 102, 104], [12, 13, 14, 15, 49, 50, 51, 60, 61, 62, 63]),
        ([33, 51, 57, 59, 60, 66, 73, 77, 83, 93, 96, 97, 103], [32, 34, 35, 52, 53, 54, 55, 98, 99]),
        ([14, 34, 61, 69, 71, 73, 87, 94, 95, 96, 97, 106, 107],
         [12, 13, 15, 32, 33, 35, 60, 62, 63, 72, 74, 75, 84, 85, 86]),
        ([27, 29, 34, 40, 48, 51, 52, 53, 55, 57, 117, 118, 133], [44, 45, 46, 47, 54, 116, 119]),
        ([9, 10, 40, 58, 66, 68, 83, 91, 92, 95, 103, 107, 108],
         [8, 11, 60, 61, 62, 63, 84, 85, 86, 87, 93, 94, 96, 97, 98, 99]),
        ([16, 17, 18, 76, 77, 78, 88, 89, 108, 109, 110, 128, 129],
         [90, 91, 130, 131]),
        ([0, 4, 5, 8, 36, 40, 44, 60, 64, 68, 76, 80, 84], [6, 7]),
        # 10
        ([9, 17, 46, 54, 64, 70, 77, 80, 83, 106], [12, 13, 14, 15, 48, 49, 50, 51, 60, 61, 62, 63]),
        ([8, 11, 42, 48, 56, 83, 86, 94, 99, 133], [44, 45, 46, 47, 52,
         53, 54, 55, 76, 77, 78, 79, 88, 89, 90, 91, 100, 101, 102, 103]),
        ([6, 7, 19, 24, 48, 52, 88, 101, 129, 131], [4, 5, 20, 21, 22, 23, 44, 45, 46, 47, 56, 57, 58, 59, 128, 130]),
        ([4, 10, 16, 19, 23, 31, 50, 55, 57, 124], [0, 1, 2, 3, 12, 13, 14, 15, 24, 25, 26, 27]),
        ([6, 10, 13, 17, 19, 60, 70, 83, 90, 94], [64, 65, 66, 67, 84, 85, 86, 87, 96, 97, 98, 99]),
        # 7
        ([12, 14, 27, 42, 47, 132, 135], [13, 15, 36, 37, 38, 39, 48, 49, 50, 51, 133, 134]),
        ([15, 18, 58, 82, 83, 110, 111], [8, 9, 10, 11, 20, 21, 22, 23, 80, 81, 108, 109]),
        ([16, 19, 29, 31, 84, 92, 100], [17, 18, 28, 30, 88, 89, 90, 91, 96, 97, 98, 99]),
        ([9, 14, 58, 67, 70, 94, 95], [4, 5, 6, 7, 16, 17, 18, 19, 60, 61, 62, 63]),
        ([10, 12, 18, 51, 53, 56, 94], [92, 93, 95]),
        # 4
        ([21, 60, 98, 107], [20, 22, 23, 61, 62, 63, 100, 101, 102, 103]),
        ([52, 84, 92, 132], [53, 54, 55, 88, 89, 90, 91, 133, 134, 135]),
        ([14, 22, 33, 123], [16, 17, 18, 19, 32, 34, 35, 120, 121, 122]),
        ([92, 94, 111, 127], [93, 95, 108, 109, 110, 124, 125, 126]),
        ([7, 10, 36, 38], [0, 1, 2, 3, 12, 13, 14, 15]),
        # 1
        ([37], [36, 38, 39]),
        ([128], [129, 130, 131]),
    ]

    def test_yuukouhai(self):
        for jun_tehai, expected in self.string_test_cases:
            result = Shanten(Hai136Group.from_string(jun_tehai)).yuukouhai.to_string()
            msg = (
                f"jun_tehai: {jun_tehai}, "
                f"expected: {expected}, "
                f"result: {result}"
            )
            self.assertEqual(result, expected, msg)

        for jun_tehai, expected in self.list_test_cases:
            result = Shanten(Hai136Group.from_list136(jun_tehai)).yuukouhai.to_list136()
            msg = (
                f"jun_tehai: {jun_tehai}, "
                f"expected: {expected}, "
                f"result: {result}"
            )
            self.assertEqual(result, expected, msg)


class TestCalculateYuukouhaiWithInvalidTehai(unittest.TestCase):
    test_cases = [
        Hai136Group.from_string(''),
        Hai136Group.from_string('11m'),
        Hai136Group.from_string('111m'),
        Hai136Group.from_string('111m11s'),
        Hai136Group.from_string('111m111s'),
        Hai136Group.from_string('111m111s11p'),
        Hai136Group.from_string('111m111s111p'),
        Hai136Group.from_string('111m111s111p11z'),
        Hai136Group.from_string('111m111s111p111z'),
    ]

    def test_yuukouhai_when_jun_tehai_length_is_invalid(self):
        for jun_tehai in self.test_cases:
            with self.assertRaises(ValueError):
                Shanten(jun_tehai).yuukouhai


if __name__ == '__main__':
    unittest.main()
