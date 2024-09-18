import os
import random
import unittest

import numpy as np
from shanten_tools import shanten as external_shanten

from kago_utils.hai import Hai34List, Hai34String, Hai136List
from kago_utils.shanten import Shanten


def generate_random_jun_tehai(jun_tehai_length: int):
    # manzu, pinzu, souzu and zihai
    yama = random.sample(range(34 * 4), jun_tehai_length)
    jun_tehai = Hai136List(yama)
    return jun_tehai


def generate_random_jun_tehai_for_honitsu(jun_tehai_length: int):
    # manzu and zihai
    yama = random.sample(list(range(9 * 4)) + list(range(27 * 4, 34 * 4)), jun_tehai_length)
    jun_tehai = Hai136List(yama)
    return jun_tehai


def generate_random_jun_tehai_for_chinitsu(jun_tehai_length: int):
    # manzu
    yama = random.sample(range(9 * 4), jun_tehai_length)
    jun_tehai = Hai136List(yama)
    return jun_tehai


def calculate_shanten_external(jun_tehai: Hai136List):
    jun_tehai = jun_tehai.to_hai34_counter()
    return external_shanten(np.array(jun_tehai.data, dtype=np.uint8)) - 1


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
            with self.subTest(jun_tehai_length=jun_tehai_length, n_huuro=n_huuro):
                for _ in range(self.n_assertion):
                    jun_tehai = generate_random_jun_tehai(jun_tehai_length)
                    result = Shanten.calculate_shanten(jun_tehai)
                    expected = calculate_shanten_external(jun_tehai)
                    msg = f"jun_tehai: {jun_tehai.to_hai34_string()}, n_huuro: {n_huuro}"
                    self.assertEqual(result, expected, msg)

    def test_shanten_honitsu(self):
        for jun_tehai_length, n_huuro in self.tehai_patterns:
            with self.subTest(jun_tehai_length=jun_tehai_length, n_huuro=n_huuro):
                for _ in range(self.n_assertion):
                    jun_tehai = generate_random_jun_tehai_for_honitsu(jun_tehai_length)
                    result = Shanten.calculate_shanten(jun_tehai)
                    expected = calculate_shanten_external(jun_tehai)
                    msg = f"jun_tehai: {jun_tehai.to_hai34_string()}, n_huuro: {n_huuro}"
                    self.assertEqual(result, expected, msg)

    def test_shanten_chinitsu(self):
        for jun_tehai_length, n_huuro in self.tehai_patterns:
            with self.subTest(jun_tehai_length=jun_tehai_length, n_huuro=n_huuro):
                for _ in range(self.n_assertion):
                    jun_tehai = generate_random_jun_tehai_for_chinitsu(jun_tehai_length)
                    result = Shanten.calculate_shanten(jun_tehai)
                    expected = calculate_shanten_external(jun_tehai)
                    msg = f"jun_tehai: {jun_tehai.to_hai34_string()}, n_huuro: {n_huuro}"
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
                jun_tehai = Hai34List(problem[:14])
                result = [
                    Shanten.calculate_regular_shanten(jun_tehai),
                    Shanten.calculate_kokushimusou_shanten(jun_tehai),
                    Shanten.calculate_chiitoitsu_shanten(jun_tehai),
                ]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_hai34_string()}"
                self.assertEqual(result, expected, msg)

    def test_shanten_hon_10000(self):
        with open(self.p_hon_10000_txt, 'rb') as f:
            for row in f.readlines():
                problem = list(map(int, row.split()))
                jun_tehai = Hai34List(problem[:14])
                result = [
                    Shanten.calculate_regular_shanten(jun_tehai),
                    Shanten.calculate_kokushimusou_shanten(jun_tehai),
                    Shanten.calculate_chiitoitsu_shanten(jun_tehai),
                ]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_hai34_string()}"
                self.assertEqual(result, expected, msg)

    def test_shanten_tin_10000(self):
        with open(self.p_tin_10000_txt, 'rb') as f:
            for row in f.readlines():
                problem = list(map(int, row.split()))
                jun_tehai = Hai34List(problem[:14])
                result = [
                    Shanten.calculate_regular_shanten(jun_tehai),
                    Shanten.calculate_kokushimusou_shanten(jun_tehai),
                    Shanten.calculate_chiitoitsu_shanten(jun_tehai),
                ]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_hai34_string()}"
                self.assertEqual(result, expected, msg)

    def test_shanten_koku_10000(self):
        with open(self.p_koku_10000_txt, 'rb') as f:
            for row in f.readlines():
                problem = list(map(int, row.split()))
                jun_tehai = Hai34List(problem[:14])
                result = [
                    Shanten.calculate_regular_shanten(jun_tehai),
                    Shanten.calculate_kokushimusou_shanten(jun_tehai),
                    Shanten.calculate_chiitoitsu_shanten(jun_tehai),
                ]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_hai34_string()}"
                self.assertEqual(result, expected, msg)


class TestCalculateShantenWithHandmadeTehai(unittest.TestCase):
    # format: (jun_tehai, expected)
    test_cases = [
        (Hai34String('23466669999m111z'), 1),
        (Hai34String('1111345567m111z'), 1)
    ]

    def test_shanten(self):
        for jun_tehai, expected in self.test_cases:
            with self.subTest(jun_tehai=jun_tehai):
                result = Shanten.calculate_shanten(jun_tehai)
                msg = f"jun_tehai: {jun_tehai.to_hai34_string()}"
                self.assertEqual(result, expected, msg)


class TestCalculateShantenWithInvalidTehai(unittest.TestCase):
    test_cases = [
        Hai34String(''),
        Hai34String('111m'),
        Hai34String('111m111s'),
        Hai34String('111m111s111p'),
        Hai34String('111m111s111p111z'),
    ]

    def test_shanten(self):
        for jun_tehai in self.test_cases:
            with self.subTest(jun_tehai=jun_tehai):
                with self.assertRaises(ValueError):
                    Shanten.calculate_shanten(jun_tehai)


class TestCalculateYuukouhaiWithHandmadeTehai(unittest.TestCase):
    # format: (jun_tehai, expected)
    test_cases = [
        (Hai34String('6688m117p699s134z'), Hai34String('7p6s134z').data),
        (Hai34String('123577m3479p79s6z'), Hai34String('258p8s').data),
        (Hai34String('2233m2267p1368s1z'), Hai34String('1234m25678p123678s1z').data),
        (Hai34String('179m4479p13444s5z'), Hai34String('8m8p2s').data),
        (Hai34String('1111m257p578s156z'), Hai34String('23m12346p3456789s156z').data),
        (Hai34String('2557m38p1578s237z'), Hai34String('27m38p1578s237z').data),
        (Hai34String('124699m126p1s233z'), Hai34String('359m3p3z').data),
        (Hai34String('449m67p4568s1226z'), Hai34String('4789m58p36789s126z').data),
        (Hai34String('358m4579p6678s25z'), Hai34String('48m368p69s25z').data),
        (Hai34String('234m12p47s133466z'), Hai34String('3p23456789s1346z').data),
        (Hai136List([0, 4, 5, 8, 36, 40, 44, 60, 64, 68, 76, 80, 84]), Hai136List([6, 7]).data),
        (Hai136List([12, 16, 20, 24, 25, 28, 32, 33, 44, 72, 76, 100, 101]),
         Hai136List([29, 30, 31, 80, 81, 82, 83]).data),
        (Hai136List([0, 12, 20, 21, 24, 28, 36, 40, 80, 84, 92, 93, 96]),
         Hai136List([16, 17, 18, 19, 44, 45, 46, 47, 76, 77, 78, 79, 88, 89, 90, 91]).data),
        (Hai136List([16, 17, 18, 76, 77, 78, 88, 89, 108, 109, 110, 128, 129]),
         Hai136List([90, 91, 130, 131]).data),
        (Hai136List([20, 28, 36, 40, 64, 72, 73, 92, 96, 100, 101, 128, 129]),
         Hai136List([24, 25, 26, 27, 44, 45, 46, 47, 74, 75, 130, 131]).data)
    ]

    def test_yuukouhai(self):
        for jun_tehai, expected in self.test_cases:
            with self.subTest(jun_tehai=jun_tehai):
                result = Shanten.calculate_yuukouhai(jun_tehai).data
                msg = f"jun_tehai: {jun_tehai.to_hai34_string()}"
                self.assertEqual(result, expected, msg)


class TestCalculateYuukouhaiWithInvalidTehai(unittest.TestCase):
    def test_yuukouhai_when_jun_tehai_length_is_14(self):
        jun_tehai = Hai34String('11123455678999m')
        with self.assertRaises(ValueError):
            Shanten.calculate_yuukouhai(jun_tehai)


if __name__ == '__main__':
    unittest.main()
