import unittest

from kago_utils.actions import Ronho


class TestInit(unittest.TestCase):
    def test(self):
        Ronho()


class TestEq(unittest.TestCase):
    def test_with_ronho(self):
        ronho1 = Ronho()
        ronho2 = Ronho()
        self.assertEqual(ronho1, ronho2)

    def test_with_int(self):
        ronho = Ronho()
        self.assertNotEqual(ronho, 0)


class TestRepr(unittest.TestCase):
    def test(self):
        ronho = Ronho()
        self.assertEqual(repr(ronho), "Ronho()")


if __name__ == "__main__":
    unittest.main()
