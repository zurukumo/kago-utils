import unittest

from kago_utils.actions import Riichi


class TestInit(unittest.TestCase):
    def test(self):
        Riichi()


class TestEq(unittest.TestCase):
    def test_with_riichi(self):
        riichi1 = Riichi()
        riichi2 = Riichi()
        self.assertEqual(riichi1, riichi2)

    def test_with_int(self):
        riichi = Riichi()
        self.assertNotEqual(riichi, 0)


class TestRepr(unittest.TestCase):
    def test(self):
        riichi = Riichi()
        self.assertEqual(repr(riichi), "Riichi()")


if __name__ == "__main__":
    unittest.main()
