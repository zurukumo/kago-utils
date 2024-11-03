import unittest

from kago_utils.hai import Hai


class TestHaiInit(unittest.TestCase):
    def test_with_valid_id(self):
        for id in range(136):
            Hai(id)

    def test_with_negative_id(self):
        with self.assertRaises(ValueError):
            Hai(-1)

    def test_with_too_large_id(self):
        with self.assertRaises(ValueError):
            Hai(136)

    def test_init_with_float_id(self):
        with self.assertRaises(TypeError):
            Hai(0.0)


class TestHaiSuit(unittest.TestCase):
    def test_suit(self):
        for id in range(36):
            self.assertEqual(Hai(id).suit, "m")
        for id in range(36, 72):
            self.assertEqual(Hai(id).suit, "p")
        for id in range(72, 108):
            self.assertEqual(Hai(id).suit, "s")
        for id in range(108, 136):
            self.assertEqual(Hai(id).suit, "z")


class TestHaiNumber(unittest.TestCase):
    def test_number(self):
        for id in range(136):
            self.assertEqual(Hai(id).number, (id // 4) % 9 + 1)


class TestHaiFace(unittest.TestCase):
    def test_face(self):
        faces = [
            "1m",
            "2m",
            "3m",
            "4m",
            "5m",
            "6m",
            "7m",
            "8m",
            "9m",
            "1p",
            "2p",
            "3p",
            "4p",
            "5p",
            "6p",
            "7p",
            "8p",
            "9p",
            "1s",
            "2s",
            "3s",
            "4s",
            "5s",
            "6s",
            "7s",
            "8s",
            "9s",
            "1z",
            "2z",
            "3z",
            "4z",
            "5z",
            "6z",
            "7z",
        ]
        for id in range(136):
            self.assertEqual(Hai(id).face, faces[id // 4])


class TestHaiColor(unittest.TestCase):
    def test_color(self):
        self.assertEqual(Hai(15).color, "kuro")
        self.assertEqual(Hai(16).color, "aka")
        self.assertEqual(Hai(51).color, "kuro")
        self.assertEqual(Hai(52).color, "aka")
        self.assertEqual(Hai(87).color, "kuro")
        self.assertEqual(Hai(88).color, "aka")


class TestHaiComparison(unittest.TestCase):
    def test_comparison(self):
        self.assertEqual(Hai(0), Hai(0))
        self.assertNotEqual(Hai(0), Hai(1))
        self.assertLess(Hai(0), Hai(1))
        self.assertLessEqual(Hai(0), Hai(0))
        self.assertLessEqual(Hai(0), Hai(1))
        self.assertGreater(Hai(1), Hai(0))
        self.assertGreaterEqual(Hai(0), Hai(0))
        self.assertGreaterEqual(Hai(1), Hai(0))

    def test_eq_with_int(self):
        self.assertNotEqual(Hai(0), 0)


if __name__ == "__main__":
    unittest.main()
