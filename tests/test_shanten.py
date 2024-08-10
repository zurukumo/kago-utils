import os
import random
import unittest

import numpy as np
from shanten_tools import shanten as external_shanten

from kago_utils.hai import Hai34List, Hai136List
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


class TestShantenRandomTehai(unittest.TestCase):
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
                    result = Shanten.calculate_shanten(jun_tehai, n_huuro)
                    expected = calculate_shanten_external(jun_tehai)
                    msg = f"jun_tehai: {jun_tehai.to_hai34_string()}, n_huuro: {n_huuro}"
                    self.assertEqual(result, expected, msg)

    def test_shanten_honitsu(self):
        for jun_tehai_length, n_huuro in self.tehai_patterns:
            with self.subTest(jun_tehai_length=jun_tehai_length, n_huuro=n_huuro):
                for _ in range(self.n_assertion):
                    jun_tehai = generate_random_jun_tehai_for_honitsu(jun_tehai_length)
                    result = Shanten.calculate_shanten(jun_tehai, n_huuro)
                    expected = calculate_shanten_external(jun_tehai)
                    msg = f"jun_tehai: {jun_tehai.to_hai34_string()}, n_huuro: {n_huuro}"
                    self.assertEqual(result, expected, msg)

    def test_shanten_chinitsu(self):
        for jun_tehai_length, n_huuro in self.tehai_patterns:
            with self.subTest(jun_tehai_length=jun_tehai_length, n_huuro=n_huuro):
                for _ in range(self.n_assertion):
                    jun_tehai = generate_random_jun_tehai_for_chinitsu(jun_tehai_length)
                    result = Shanten.calculate_shanten(jun_tehai, n_huuro)
                    expected = calculate_shanten_external(jun_tehai)
                    msg = f"jun_tehai: {jun_tehai.to_hai34_string()}, n_huuro: {n_huuro}"
                    self.assertEqual(result, expected, msg)


# ref: https://mahjong.ara.black/etc/shanten/shanten9.htm
class TestShantenAraTehai(unittest.TestCase):
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
                    Shanten.calculate_shanten_for_regular(jun_tehai, 0),
                    Shanten.calculate_shanten_for_kokushimusou(jun_tehai),
                    Shanten.calculate_shanten_for_chiitoitsu(jun_tehai),
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
                    Shanten.calculate_shanten_for_regular(jun_tehai, 0),
                    Shanten.calculate_shanten_for_kokushimusou(jun_tehai),
                    Shanten.calculate_shanten_for_chiitoitsu(jun_tehai),
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
                    Shanten.calculate_shanten_for_regular(jun_tehai, 0),
                    Shanten.calculate_shanten_for_kokushimusou(jun_tehai),
                    Shanten.calculate_shanten_for_chiitoitsu(jun_tehai),
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
                    Shanten.calculate_shanten_for_regular(jun_tehai, 0),
                    Shanten.calculate_shanten_for_kokushimusou(jun_tehai),
                    Shanten.calculate_shanten_for_chiitoitsu(jun_tehai),
                ]
                expected = problem[14:]
                msg = f"jun_tehai: {jun_tehai.to_hai34_string()}"
                self.assertEqual(result, expected, msg)


if __name__ == '__main__':
    unittest.main()
