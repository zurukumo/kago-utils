import unittest

from kago_utils.actions import Wait


class TestInit(unittest.TestCase):
    def test(self):
        Wait()


class TestEq(unittest.TestCase):
    def test_with_wait(self):
        wait1 = Wait()
        wait2 = Wait()
        self.assertEqual(wait1, wait2)

    def test_with_int(self):
        wait = Wait()
        self.assertNotEqual(wait, 0)


class TestRepr(unittest.TestCase):
    def test(self):
        wait = Wait()
        self.assertEqual(repr(wait), "Wait()")


if __name__ == "__main__":
    unittest.main()
