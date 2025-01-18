import unittest

from kago_utils.hai import Hai
from kago_utils.yama import Yama


class TestInit(unittest.TestCase):
    def test(self):
        Yama()


class TestGenerate(unittest.TestCase):
    def test(self):
        yama1 = Yama()
        yama1.generate()

        self.assertEqual(len(yama1.tsumo_hais), 122)
        self.assertEqual(len(yama1.rinshan_hais), 4)
        self.assertEqual(len(yama1.dora_hyouji_hais), 10)

        yama2 = Yama()
        yama2.generate()

        self.assertNotEqual(yama1.tsumo_hais, yama2.tsumo_hais)


class TestTsumo(unittest.TestCase):
    def test(self):
        yama = Yama()
        yama.generate()

        tsumo_hai = yama.tsumo()
        self.assertIsInstance(tsumo_hai, Hai)
        self.assertEqual(len(yama.tsumo_hais), 121)

    def test_after_10_tsumo_and_2_rinshan_tsumo(self):
        yama = Yama()
        yama.generate()

        for _ in range(10):
            yama.tsumo()
        for _ in range(2):
            yama.rinshan_tsumo()

        yama.tsumo()

    def test_after_122_tsumo(self):
        yama = Yama()
        yama.generate()

        for _ in range(122):
            yama.tsumo()

        with self.assertRaises(ValueError):
            yama.tsumo()

    def test_after_121_tsumo_and_1_rinshan_tsumo(self):
        yama = Yama()
        yama.generate()

        for _ in range(121):
            yama.tsumo()
        for _ in range(1):
            yama.rinshan_tsumo()

        with self.assertRaises(ValueError):
            yama.tsumo()

    def test_after_118_tsumo_and_4_rinshan_tsumo(self):
        yama = Yama()
        yama.generate()

        for _ in range(118):
            yama.tsumo()
        for _ in range(4):
            yama.rinshan_tsumo()

        with self.assertRaises(ValueError):
            yama.tsumo()


class TestRinshanTsumo(unittest.TestCase):
    def test(self):
        yama = Yama()
        yama.generate()

        rinshan_hai = yama.rinshan_tsumo()
        self.assertIsInstance(rinshan_hai, Hai)
        self.assertEqual(len(yama.rinshan_hais), 3)

    def test_after_3_rinshan_tsumo(self):
        yama = Yama()
        yama.generate()

        for _ in range(3):
            yama.rinshan_tsumo()

        yama.rinshan_tsumo()

    def test_after_4_rinshan_tsumo(self):
        yama = Yama()
        yama.generate()

        for _ in range(4):
            yama.rinshan_tsumo()

        with self.assertRaises(ValueError):
            yama.rinshan_tsumo()


class TestOpenDoraHyoujiHai(unittest.TestCase):
    def test(self):
        yama = Yama()
        yama.generate()

        self.assertEqual(yama.n_open_dora_hyouji_hais, 1)

        yama.open_dora_hyouji_hai()
        self.assertEqual(yama.n_open_dora_hyouji_hais, 2)


class TestOpenedDoraHyoujiHais(unittest.TestCase):
    def test(self):
        yama = Yama()
        yama.generate()

        self.assertEqual(len(yama.opened_dora_hyouji_hais), 1)

        yama.open_dora_hyouji_hai()
        self.assertEqual(len(yama.opened_dora_hyouji_hais), 2)


class TestOpenedUradoraHyoujiHais(unittest.TestCase):
    def test(self):
        yama = Yama()
        yama.generate()

        self.assertEqual(len(yama.opened_uradora_hyouji_hais), 1)

        yama.open_dora_hyouji_hai()
        self.assertEqual(len(yama.opened_uradora_hyouji_hais), 2)


class TestRestTsumoCount(unittest.TestCase):
    def test(self):
        yama = Yama()
        yama.generate()

        self.assertEqual(yama.rest_tsumo_count, 122)

        yama.tsumo()
        self.assertEqual(yama.rest_tsumo_count, 121)

        yama.rinshan_tsumo()
        self.assertEqual(yama.rest_tsumo_count, 120)


if __name__ == "__main__":
    unittest.main()
