import unittest

from kago_utils.actions import Tsumoho


class TestInit(unittest.TestCase):
    def test(self):
        Tsumoho()


class TestEq(unittest.TestCase):
    def test_with_tsumoho(self):
        tsumoho1 = Tsumoho()
        tsumoho2 = Tsumoho()
        self.assertEqual(tsumoho1, tsumoho2)

    def test_with_int(self):
        tsumoho = Tsumoho()
        self.assertNotEqual(tsumoho, 0)


class TestRepr(unittest.TestCase):
    def test(self):
        tsumoho = Tsumoho()
        self.assertEqual(repr(tsumoho), "Tsumoho()")


if __name__ == "__main__":
    unittest.main()
