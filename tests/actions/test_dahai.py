import unittest

from kago_utils.actions import Dahai
from kago_utils.hai import Hai


class TestInit(unittest.TestCase):
    def test(self):
        Dahai(hai=Hai(0))


class TestEq(unittest.TestCase):
    def test_with_dahai(self):
        dahai1 = Dahai(hai=Hai(0))
        dahai2 = Dahai(hai=Hai(0))
        self.assertEqual(dahai1, dahai2)

    def test_with_dahai_having_different_hai(self):
        dahai1 = Dahai(hai=Hai(0))
        dahai2 = Dahai(hai=Hai(1))
        self.assertNotEqual(dahai1, dahai2)

    def test_with_int(self):
        dahai = Dahai(hai=Hai(0))
        self.assertNotEqual(dahai, 0)


class TestRepr(unittest.TestCase):
    def test(self):
        dahai = Dahai(hai=Hai(0))
        self.assertEqual(repr(dahai), "Dahai(hai=Hai(0))")


if __name__ == "__main__":
    unittest.main()
