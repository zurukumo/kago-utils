import unittest
from itertools import product

from kago_utils.hai import Hai34, Hai136


class TestHai34Init(unittest.TestCase):
    def test_init_with_valid_id(self):
        for id in range(34):
            Hai34(id)

    def test_init_with_negative_id(self):
        with self.assertRaises(ValueError):
            Hai34(-1)

    def test_init_with_too_large_id(self):
        with self.assertRaises(ValueError):
            Hai34(34)

    def test_init_with_float_id(self):
        with self.assertRaises(TypeError):
            Hai34(0.0)


class TestHai136Init(unittest.TestCase):
    def test_with_valid_id(self):
        for id in range(136):
            Hai136(id)

    def test_with_negative_id(self):
        with self.assertRaises(ValueError):
            Hai136(-1)

    def test_with_too_large_id(self):
        with self.assertRaises(ValueError):
            Hai136(136)

    def test_init_with_float_id(self):
        with self.assertRaises(TypeError):
            Hai136(0.0)


class TestHai34ToHai34(unittest.TestCase):
    def test_to_hai34(self):
        for id in range(34):
            self.assertEqual(Hai34(id).to_hai34(), Hai34(id))


class TestHai136ToHai34(unittest.TestCase):
    def test_to_hai34(self):
        for id in range(136):
            self.assertEqual(Hai136(id).to_hai34(), Hai34(id//4))


class TestHai34Suit(unittest.TestCase):
    def test_suit(self):
        for id in range(9):
            self.assertEqual(Hai34(id).suit, 'm')
        for id in range(9, 18):
            self.assertEqual(Hai34(id).suit, 'p')
        for id in range(18, 27):
            self.assertEqual(Hai34(id).suit, 's')
        for id in range(27, 34):
            self.assertEqual(Hai34(id).suit, 'z')


class TestHai136Suit(unittest.TestCase):
    def test_suit(self):
        for id in range(36):
            self.assertEqual(Hai136(id).suit, 'm')
        for id in range(36, 72):
            self.assertEqual(Hai136(id).suit, 'p')
        for id in range(72, 108):
            self.assertEqual(Hai136(id).suit, 's')
        for id in range(108, 136):
            self.assertEqual(Hai136(id).suit, 'z')


class TestHai34Number(unittest.TestCase):
    def test_number(self):
        for id in range(34):
            self.assertEqual(Hai34(id).number, id % 9)


class TestHai136Number(unittest.TestCase):
    def test_number(self):
        for id in range(136):
            self.assertEqual(Hai136(id).number, (id // 4) % 9)


class TestHai136IsAka(unittest.TestCase):
    def test_is_aka(self):
        for id in range(136):
            self.assertEqual(Hai136(id).is_aka(), id in (16, 52, 88))


class TestHai34Comparison(unittest.TestCase):
    def test_comparison(self):
        for id1, id2 in product(range(34), repeat=2):
            self.assertEqual(id1 == id2, Hai34(id1) == Hai34(id2))
            self.assertEqual(id1 != id2, Hai34(id1) != Hai34(id2))
            self.assertEqual(id1 < id2, Hai34(id1) < Hai34(id2))
            self.assertEqual(id1 <= id2, Hai34(id1) <= Hai34(id2))
            self.assertEqual(id1 > id2, Hai34(id1) > Hai34(id2))
            self.assertEqual(id1 >= id2, Hai34(id1) >= Hai34(id2))


class TestHai136Comparison(unittest.TestCase):
    def test_comparison(self):
        for id1, id2 in product(range(136), repeat=2):
            self.assertEqual(Hai136(id1) == Hai136(id2), id1 == id2)
            self.assertEqual(Hai136(id1) != Hai136(id2), id1 != id2)
            self.assertEqual(Hai136(id1) < Hai136(id2), id1 < id2)
            self.assertEqual(Hai136(id1) <= Hai136(id2), id1 <= id2)
            self.assertEqual(Hai136(id1) > Hai136(id2), id1 > id2)
            self.assertEqual(Hai136(id1) >= Hai136(id2), id1 >= id2)


if __name__ == '__main__':
    unittest.main()
