import os
import random
import unittest

import numpy as np
from shanten_tools import shanten as external_shanten

from kago_utils.hai_group import Hai34Group, Hai136Group
from kago_utils.shanten import Shanten


def generate_random_jun_tehai(jun_tehai_length: int):
    # manzu, pinzu, souzu and zihai
    yama = random.sample(range(34 * 4), jun_tehai_length)
    jun_tehai = Hai136Group.from_list(yama)
    return jun_tehai


def generate_random_jun_tehai_for_honitsu(jun_tehai_length: int):
    # manzu and zihai
    yama = random.sample(list(range(9 * 4)) + list(range(27 * 4, 34 * 4)), jun_tehai_length)
    jun_tehai = Hai136Group.from_list(yama)
    return jun_tehai


def generate_random_jun_tehai_for_chinitsu(jun_tehai_length: int):
    # manzu
    yama = random.sample(range(9 * 4), jun_tehai_length)
    jun_tehai = Hai136Group.from_list(yama)
    return jun_tehai


def calculate_shanten_external(jun_tehai: Hai136Group):
    jun_tehai = jun_tehai.to_hai34_group().to_counter()
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
                jun_tehai = Hai34Group.from_list(problem[:14])
                shanten = Shanten(jun_tehai)
                result = [shanten.regular_shanten, shanten.kokushimusou_shanten, shanten.chiitoitsu_shanten]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_string()}"
                self.assertEqual(result, expected, msg)

    def test_shanten_hon_10000(self):
        with open(self.p_hon_10000_txt, 'rb') as f:
            for row in f.readlines():
                problem = list(map(int, row.split()))
                jun_tehai = Hai34Group.from_list(problem[:14])
                shanten = Shanten(jun_tehai)
                result = [shanten.regular_shanten, shanten.kokushimusou_shanten, shanten.chiitoitsu_shanten]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_string()}"
                self.assertEqual(result, expected, msg)

    def test_shanten_tin_10000(self):
        with open(self.p_tin_10000_txt, 'rb') as f:
            for row in f.readlines():
                problem = list(map(int, row.split()))
                jun_tehai = Hai34Group.from_list(problem[:14])
                shanten = Shanten(jun_tehai)
                result = [shanten.regular_shanten, shanten.kokushimusou_shanten, shanten.chiitoitsu_shanten]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_string()}"
                self.assertEqual(result, expected, msg)

    def test_shanten_koku_10000(self):
        with open(self.p_koku_10000_txt, 'rb') as f:
            for row in f.readlines():
                problem = list(map(int, row.split()))
                jun_tehai = Hai34Group.from_list(problem[:14])
                shanten = Shanten(jun_tehai)
                result = [shanten.regular_shanten, shanten.kokushimusou_shanten, shanten.chiitoitsu_shanten]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_string()}"
                self.assertEqual(result, expected, msg)


class TestCalculateShantenWithHandmadeTehai(unittest.TestCase):
    # format: (jun_tehai, expected)
    test_cases = [
        (Hai34Group.from_string('23466669999m111z'), 1),
        (Hai34Group.from_string('1111345567m111z'), 1)
    ]

    def test_shanten_when_jun_tehai_length_is_invalid(self):
        for jun_tehai, expected in self.test_cases:
            result = Shanten(jun_tehai).shanten
            msg = f"jun_tehai: {jun_tehai}"
            self.assertEqual(result, expected, msg)


class TestCalculateShantenWithInvalidTehai(unittest.TestCase):
    test_cases = [
        Hai34Group.from_string(''),
        Hai34Group.from_string('111m'),
        Hai34Group.from_string('111m111s'),
        Hai34Group.from_string('111m111s111p'),
        Hai34Group.from_string('111m111s111p111z'),
    ]

    def test_shanten(self):
        for jun_tehai in self.test_cases:
            with self.assertRaises(ValueError):
                Shanten(jun_tehai).shanten


class TestCalculateYuukouhaiWithHandmadeTehai(unittest.TestCase):
    # format: (jun_tehai, expected)
    test_cases: list[tuple[Hai34Group, Hai34Group] | tuple[Hai136Group, Hai136Group]] = [
        # 14枚 Hai34Group
        (Hai34Group.from_string('1111m257p578s156z'), Hai34Group.from_string('23m12346p3456789s156z')),
        (Hai34Group.from_string('2233m2267p1368s1z'), Hai34Group.from_string('1234m25678p123678s1z')),
        (Hai34Group.from_string('449m67p4568s1226z'), Hai34Group.from_string('4789m58p36789s126z')),
        (Hai34Group.from_string('2557m38p1578s237z'), Hai34Group.from_string('27m38p1578s237z')),
        (Hai34Group.from_string('234m12p47s133466z'), Hai34Group.from_string('3p23456789s1346z')),
        (Hai34Group.from_string('358m4579p6678s25z'), Hai34Group.from_string('48m368p69s25z')),
        (Hai34Group.from_string('124699m126p1s233z'), Hai34Group.from_string('359m3p3z')),
        (Hai34Group.from_string('6688m117p699s134z'), Hai34Group.from_string('7p6s134z')),
        (Hai34Group.from_string('123577m3479p79s6z'), Hai34Group.from_string('258p8s')),
        (Hai34Group.from_string('179m4479p13444s5z'), Hai34Group.from_string('8m8p2s')),
        # 10枚 Hai34Group
        (Hai34Group.from_string('34589m56p79s3z'), Hai34Group.from_string('789m4567p789s3z')),
        (Hai34Group.from_string('123m2p399s337z'), Hai34Group.from_string('1234p123459s37z')),
        (Hai34Group.from_string('1166m569p67s1z'), Hai34Group.from_string('16m47p58s')),
        (Hai34Group.from_string('267m47p66788s'), Hai34Group.from_string('258m47p7s')),
        (Hai34Group.from_string('1355m11345p3s'), Hai34Group.from_string('25m1p')),
        # 7枚 Hai34Group
        (Hai34Group.from_string('2m6p11s223z'), Hai34Group.from_string('1234m45678p1s23z')),
        (Hai34Group.from_string('13m6p358s1z'), Hai34Group.from_string('2m6p48s1z')),
        (Hai34Group.from_string('2p6s11557z'), Hai34Group.from_string('1234p45678s157z')),
        (Hai34Group.from_string('4668m2p59s'), Hai34Group.from_string('57m2p59s')),
        (Hai34Group.from_string('88m569p89s'), Hai34Group.from_string('47p7s')),
        # 4枚 Hai34Group
        (Hai34Group.from_string('1m9p2s5z'), Hai34Group.from_string('123m789p1234s5z')),
        (Hai34Group.from_string('1m28s6z'), Hai34Group.from_string('123m12346789s6z')),
        (Hai34Group.from_string('2m99s1z'), Hai34Group.from_string('1234m9s1z')),
        (Hai34Group.from_string('55m29s'), Hai34Group.from_string('5m1234789s')),
        (Hai34Group.from_string('4p678s'), Hai34Group.from_string('4p')),
        # 1枚 Hai34Group
        (Hai34Group.from_string('5m'), Hai34Group.from_string('5m')),
        (Hai34Group.from_string('9p'), Hai34Group.from_string('9p')),
        # 13枚 Hai136Group
        (Hai136Group.from_list([12, 16, 20, 24, 25, 28, 32, 33, 44, 72, 76, 100, 101]),
         Hai136Group.from_list([29, 30, 31, 80, 81, 82, 83])),
        (Hai136Group.from_list([0, 12, 20, 21, 24, 28, 36, 40, 80, 84, 92, 93, 96]),
         Hai136Group.from_list([16, 17, 18, 19, 44, 45, 46, 47, 76, 77, 78, 79, 88, 89, 90, 91])),
        (Hai136Group.from_list([20, 28, 36, 40, 64, 72, 73, 92, 96, 100, 101, 128, 129]),
         Hai136Group.from_list([24, 25, 26, 27, 44, 45, 46, 47, 74, 75, 130, 131])),
        (Hai136Group.from_list([4, 7, 8, 19, 47, 48, 54, 55, 57, 89, 99, 102, 104]),
         Hai136Group.from_list([12, 13, 14, 15, 49, 50, 51, 60, 61, 62, 63])),
        (Hai136Group.from_list([33, 51, 57, 59, 60, 66, 73, 77, 83, 93, 96, 97, 103]),
         Hai136Group.from_list([32, 34, 35, 98, 99, 52, 53, 54, 55])),
        (Hai136Group.from_list([14, 34, 61, 69, 71, 73, 87, 94, 95, 96, 97, 106, 107]),
         Hai136Group.from_list([12, 13, 15, 32, 33, 35, 60, 62, 63, 72, 74, 75, 84, 85, 86])),
        (Hai136Group.from_list([27, 29, 34, 40, 48, 51, 52, 53, 55, 57, 117, 118, 133]),
         Hai136Group.from_list([44, 45, 46, 47, 54, 116, 119])),
        (Hai136Group.from_list([9, 10, 40, 58, 66, 68, 83, 91, 92, 95, 103, 107, 108]),
         Hai136Group.from_list([8, 11, 60, 61, 62, 63, 84, 85, 86, 87, 93, 94, 96, 97, 98, 99])),
        (Hai136Group.from_list([16, 17, 18, 76, 77, 78, 88, 89, 108, 109, 110, 128, 129]),
         Hai136Group.from_list([90, 91, 130, 131])),
        (Hai136Group.from_list([0, 4, 5, 8, 36, 40, 44, 60, 64, 68, 76, 80, 84]), Hai136Group.from_list([6, 7])),
        # 10枚 Hai136Group
        (Hai136Group.from_list([9, 17, 46, 54, 64, 70, 77, 80, 83, 106]),
         Hai136Group.from_list([12, 13, 14, 15, 48, 49, 50, 51, 60, 61, 62, 63])),
        (Hai136Group.from_list([8, 11, 42, 48, 56, 83, 86, 94, 99, 133]),
         Hai136Group.from_list([44, 45, 46, 47, 52, 53, 54, 55, 76, 77, 78, 79, 88, 89, 90, 91, 100, 101, 102, 103])),
        (Hai136Group.from_list([6, 7, 19, 24, 48, 52, 88, 101, 129, 131]),
         Hai136Group.from_list([4, 5, 20, 21, 22, 23, 44, 45, 46, 47, 56, 57, 58, 59, 128, 130])),
        (Hai136Group.from_list([4, 10, 16, 19, 23, 31, 50, 55, 57, 124]),
         Hai136Group.from_list([0, 1, 2, 3, 12, 13, 14, 15, 24, 25, 26, 27])),
        (Hai136Group.from_list([6, 10, 13, 17, 19, 60, 70, 83, 90, 94]),
         Hai136Group.from_list([64, 65, 66, 67, 84, 85, 86, 87, 96, 97, 98, 99])),
        # 7枚 Hai136Group
        (Hai136Group.from_list([12, 14, 27, 42, 47, 132, 135]),
         Hai136Group.from_list([13, 15, 36, 37, 38, 39, 48, 49, 50, 51, 133, 134])),
        (Hai136Group.from_list([15, 18, 58, 82, 83, 110, 111]),
         Hai136Group.from_list([8, 9, 10, 11, 20, 21, 22, 23, 80, 81, 108, 109])),
        (Hai136Group.from_list([16, 19, 29, 31, 84, 92, 100]), Hai136Group.from_list(
            [17, 18, 28, 30, 88, 89, 90, 91, 96, 97, 98, 99])),
        (Hai136Group.from_list([9, 14, 58, 67, 70, 94, 95]), Hai136Group.from_list(
            [4, 5, 6, 7, 16, 17, 18, 19, 60, 61, 62, 63])),
        (Hai136Group.from_list([10, 12, 18, 51, 53, 56, 94]), Hai136Group.from_list([92, 93, 95])),
        # 4枚 Hai136Group
        (Hai136Group.from_list([21, 60, 98, 107]), Hai136Group.from_list(
            [20, 22, 23, 61, 62, 63, 100, 101, 102, 103])),
        (Hai136Group.from_list([52, 84, 92, 132]), Hai136Group.from_list(
            [53, 54, 55, 88, 89, 90, 91, 133, 134, 135])),
        (Hai136Group.from_list([14, 22, 33, 123]), Hai136Group.from_list(
            [16, 17, 18, 19, 32, 34, 35, 120, 121, 122])),
        (Hai136Group.from_list([92, 94, 111, 127]), Hai136Group.from_list(
            [93, 95, 108, 109, 110, 124, 125, 126])),
        (Hai136Group.from_list([7, 10, 36, 38]), Hai136Group.from_list([0, 1, 2, 3, 12, 13, 14, 15])),
        # 1枚 Hai136Group
        (Hai136Group.from_list([37]), Hai136Group.from_list([36, 38, 39])),
        (Hai136Group.from_list([128]), Hai136Group.from_list([129, 130, 131])),
    ]

    def test_yuukouhai(self):
        for jun_tehai, expected in self.test_cases:
            result = Shanten(jun_tehai).yuukouhai
            msg = (
                f"jun_tehai: {jun_tehai.to_string()}, "
                f"expected: {expected.to_string()}, "
                f"result: {result.to_string()}"
            )
            self.assertEqual(result, expected, msg)


class TestCalculateYuukouhaiWithInvalidTehai(unittest.TestCase):
    test_cases = [
        Hai34Group.from_string(''),
        Hai34Group.from_string('11m'),
        Hai34Group.from_string('111m'),
        Hai34Group.from_string('111m11s'),
        Hai34Group.from_string('111m111s'),
        Hai34Group.from_string('111m111s11p'),
        Hai34Group.from_string('111m111s111p'),
        Hai34Group.from_string('111m111s111p11z'),
        Hai34Group.from_string('111m111s111p111z'),
    ]

    def test_yuukouhai_when_jun_tehai_length_is_invalid(self):
        for jun_tehai in self.test_cases:
            with self.assertRaises(ValueError):
                Shanten(jun_tehai).yuukouhai


if __name__ == '__main__':
    unittest.main()
