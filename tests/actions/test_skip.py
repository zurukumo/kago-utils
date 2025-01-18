import unittest

from kago_utils.actions import Skip


class TestInit(unittest.TestCase):
    def test(self):
        Skip()


class TestEq(unittest.TestCase):
    def test_with_skip(self):
        skip1 = Skip()
        skip2 = Skip()
        self.assertEqual(skip1, skip2)

    def test_with_int(self):
        skip = Skip()
        self.assertNotEqual(skip, 0)


class TestRepr(unittest.TestCase):
    def test(self):
        skip = Skip()
        self.assertEqual(repr(skip), "Skip()")


if __name__ == "__main__":
    unittest.main()
