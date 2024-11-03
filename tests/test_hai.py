import unittest

from kago_utils.hai import Hai136


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


class TestHai136Number(unittest.TestCase):
    def test_number(self):
        for id in range(136):
            self.assertEqual(Hai136(id).number, (id // 4) % 9 + 1)


class TestHai136Face(unittest.TestCase):
    def test_face(self):
        faces = [
            '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
            '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
            '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
            '1z', '2z', '3z', '4z', '5z', '6z', '7z'
        ]
        for id in range(136):
            self.assertEqual(Hai136(id).face, faces[id//4])


class TestHai136Color(unittest.TestCase):
    def test_color(self):
        self.assertEqual(Hai136(15).color, 'kuro')
        self.assertEqual(Hai136(16).color, 'aka')
        self.assertEqual(Hai136(51).color, 'kuro')
        self.assertEqual(Hai136(52).color, 'aka')
        self.assertEqual(Hai136(87).color, 'kuro')
        self.assertEqual(Hai136(88).color, 'aka')


class TestHai136Comparison(unittest.TestCase):
    def test_comparison(self):
        self.assertEqual(Hai136(0), Hai136(0))
        self.assertNotEqual(Hai136(0), Hai136(1))
        self.assertLess(Hai136(0), Hai136(1))
        self.assertLessEqual(Hai136(0), Hai136(0))
        self.assertLessEqual(Hai136(0), Hai136(1))
        self.assertGreater(Hai136(1), Hai136(0))
        self.assertGreaterEqual(Hai136(0), Hai136(0))
        self.assertGreaterEqual(Hai136(1), Hai136(0))

    def test_eq_with_int(self):
        self.assertNotEqual(Hai136(0), 0)


if __name__ == '__main__':
    unittest.main()
