import unittest

from kago_utils.actions import Chii
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.tehai_decomposer import TehaiBlock, TehaiDecomposer


class TestDecompose(unittest.TestCase):
    def test_decompose(self):
        juntehai = HaiGroup.from_code("111222333m66677z")
        huuros = []
        decomposed_tehais = list(TehaiDecomposer(juntehai, huuros, juntehai[0], is_tsumoho=True).decompose())

        self.assertEqual(len(decomposed_tehais), 2)
        self.assertEqual(
            decomposed_tehais[0],
            [
                TehaiBlock("jantou", [33, 33]),
                TehaiBlock("shuntsu", [0, 1, 2], agari_hai=0),
                TehaiBlock("shuntsu", [0, 1, 2]),
                TehaiBlock("shuntsu", [0, 1, 2]),
                TehaiBlock("koutsu", [32, 32, 32]),
            ],
        )
        self.assertEqual(
            decomposed_tehais[1],
            [
                TehaiBlock("jantou", [33, 33]),
                TehaiBlock("koutsu", [0, 0, 0], agari_hai=0),
                TehaiBlock("koutsu", [1, 1, 1]),
                TehaiBlock("koutsu", [2, 2, 2]),
                TehaiBlock("koutsu", [32, 32, 32]),
            ],
        )

    def test_decompose_with_penchan_kanchan_tehai(self):
        juntehai = HaiGroup.from_code("122334m55566677z")
        huuros = []
        decomposed_tehais = list(TehaiDecomposer(juntehai, huuros, juntehai[3], is_tsumoho=True).decompose())

        self.assertEqual(len(decomposed_tehais), 2)
        self.assertEqual(
            decomposed_tehais[0],
            [
                TehaiBlock("jantou", [33, 33]),
                TehaiBlock("shuntsu", [0, 1, 2], agari_hai=2),
                TehaiBlock("shuntsu", [1, 2, 3]),
                TehaiBlock("koutsu", [31, 31, 31]),
                TehaiBlock("koutsu", [32, 32, 32]),
            ],
        )
        self.assertEqual(
            decomposed_tehais[1],
            [
                TehaiBlock("jantou", [33, 33]),
                TehaiBlock("shuntsu", [0, 1, 2]),
                TehaiBlock("shuntsu", [1, 2, 3], agari_hai=2),
                TehaiBlock("koutsu", [31, 31, 31]),
                TehaiBlock("koutsu", [32, 32, 32]),
            ],
        )

    def test_decompose_with_huuros(self):
        juntehai = HaiGroup.from_code("112233m66677z")
        huuros = [Chii(hais=HaiGroup.from_list([2, 6, 10]), stolen=Hai(2))]
        decomposed_tehais = list(TehaiDecomposer(juntehai, huuros, juntehai[0], is_tsumoho=True).decompose())

        self.assertEqual(len(decomposed_tehais), 1)
        self.assertEqual(
            decomposed_tehais[0],
            [
                TehaiBlock("jantou", [33, 33]),
                TehaiBlock("shuntsu", [0, 1, 2], agari_hai=0),
                TehaiBlock("shuntsu", [0, 1, 2]),
                TehaiBlock("koutsu", [32, 32, 32]),
                TehaiBlock("shuntsu", [0, 1, 2], minan="min"),
            ],
        )

    def test_decompose_when_ron_agari(self):
        juntehai = HaiGroup.from_code("111m44455566677z")
        huuros = []
        decomposed_tehais = list(TehaiDecomposer(juntehai, huuros, juntehai[0], is_tsumoho=False).decompose())

        self.assertEqual(len(decomposed_tehais), 1)
        self.assertEqual(
            decomposed_tehais[0],
            [
                TehaiBlock("jantou", [33, 33]),
                TehaiBlock("koutsu", [0, 0, 0], minan="min", agari_hai=0),
                TehaiBlock("koutsu", [30, 30, 30]),
                TehaiBlock("koutsu", [31, 31, 31]),
                TehaiBlock("koutsu", [32, 32, 32]),
            ],
        )


if __name__ == "__main__":
    unittest.main()
