import unittest

from kago_utils.hai import Hai


class TestInit(unittest.TestCase):
    def test_init_with_valid_id(self):
        for id in range(136):
            Hai(id)

    def test_init_with_negative_id(self):
        with self.assertRaises(ValueError):
            Hai(-1)

    def test_init_with_too_large_id(self):
        with self.assertRaises(ValueError):
            Hai(136)

    def test_init_with_float_id(self):
        with self.assertRaises(TypeError):
            Hai(0.0)


class TestSuit(unittest.TestCase):
    def test_suit(self):
        for id in range(36):
            self.assertEqual(Hai(id).suit, "m")
        for id in range(36, 72):
            self.assertEqual(Hai(id).suit, "p")
        for id in range(72, 108):
            self.assertEqual(Hai(id).suit, "s")
        for id in range(108, 136):
            self.assertEqual(Hai(id).suit, "z")


class TestNumber(unittest.TestCase):
    def test_number(self):
        for id in range(136):
            self.assertEqual(Hai(id).number, (id // 4) % 9 + 1)


class TestColor(unittest.TestCase):
    def test_color(self):
        self.assertEqual(Hai(15).color, "b")
        self.assertEqual(Hai(16).color, "r")
        self.assertEqual(Hai(51).color, "b")
        self.assertEqual(Hai(52).color, "r")
        self.assertEqual(Hai(87).color, "b")
        self.assertEqual(Hai(88).color, "r")


class TestCode(unittest.TestCase):
    def test_code(self):
        codes = (
            ["1m"] * 4
            + ["2m"] * 4
            + ["3m"] * 4
            + ["4m"] * 4
            + ["0m"] * 1
            + ["5m"] * 3
            + ["6m"] * 4
            + ["7m"] * 4
            + ["8m"] * 4
            + ["9m"] * 4
            + ["1p"] * 4
            + ["2p"] * 4
            + ["3p"] * 4
            + ["4p"] * 4
            + ["0p"] * 1
            + ["5p"] * 3
            + ["6p"] * 4
            + ["7p"] * 4
            + ["8p"] * 4
            + ["9p"] * 4
            + ["1s"] * 4
            + ["2s"] * 4
            + ["3s"] * 4
            + ["4s"] * 4
            + ["0s"] * 1
            + ["5s"] * 3
            + ["6s"] * 4
            + ["7s"] * 4
            + ["8s"] * 4
            + ["9s"] * 4
            + ["1z"] * 4
            + ["2z"] * 4
            + ["3z"] * 4
            + ["4z"] * 4
            + ["5z"] * 4
            + ["6z"] * 4
            + ["7z"] * 4
        )
        for id in range(136):
            self.assertEqual(Hai(id).code, codes[id])


class TestComparison(unittest.TestCase):
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


class TestRepr(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Hai(0)), "Hai(0)")


if __name__ == "__main__":
    unittest.main()
