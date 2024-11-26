import copy
from typing import Generator, Literal

from kago_utils.hai import Hai
from kago_utils.huuro import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.tehai import Tehai


class TehaiBlock:
    type: Literal["jantou", "shuntsu", "koutsu", "kantsu"]
    minan: Literal["min", "an"]
    hais: list[int]
    agarihai: int | None

    __slots__ = ("type", "hais", "minan", "agarihai")

    def __init__(
        self,
        type: Literal["jantou", "shuntsu", "koutsu", "kantsu"],
        hais: list[int],
        minan: Literal["min", "an"] = "an",
        agarihai: int | None = None,
    ):
        self.type = type
        self.hais = hais
        self.minan = minan
        self.agarihai = agarihai

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TehaiBlock):
            return False

        return (
            self.type == other.type
            and self.hais == other.hais
            and self.minan == other.minan
            and self.agarihai == other.agarihai
        )

    def __hash__(self) -> int:
        return hash((self.type, self.minan, tuple(self.hais), self.agarihai))

    def __repr__(self) -> str:
        return f'TehaiBlock("{self.type}", {self.minan}, {self.hais}, {self.agarihai})'


class TehaiDecomposer:
    tehai: Tehai
    agarihai: Hai
    is_tsumo_agari: bool

    __slots__ = ("tehai", "agarihai", "is_tsumo_agari")

    def __init__(self, tehai: Tehai, agarihai: Hai, is_tsumo_agari: bool):
        self.tehai = tehai
        self.agarihai = agarihai
        self.is_tsumo_agari = is_tsumo_agari

    def decompose(self) -> Generator[list[TehaiBlock], None, None]:
        huuro_blocks = []
        for huuro in self.tehai.huuros:
            hais = huuro.hais.to_list34()
            match huuro:
                case Chii():
                    huuro_blocks.append(TehaiBlock(type="shuntsu", hais=hais, minan="min"))
                case Pon():
                    huuro_blocks.append(TehaiBlock(type="koutsu", hais=hais, minan="min"))
                case Kakan() | Daiminkan():
                    huuro_blocks.append(TehaiBlock(type="kantsu", hais=hais, minan="min"))
                case Ankan():
                    huuro_blocks.append(TehaiBlock(type="kantsu", hais=hais, minan="an"))

        for juntehai_blocks in self.__decompose_juntehai_blocks():
            yield (juntehai_blocks + huuro_blocks)[::]

    def __decompose_juntehai_blocks(self) -> Generator[list[TehaiBlock], None, None]:
        counter = self.tehai.juntehai.to_counter34()
        for jantou in self.__decompose_juntehai_jantou(counter):
            for mentsus in self.__decompose_juntehai_mentsu(counter):
                for blocks in self.__select_block_including_agarihai(jantou + mentsus):
                    yield blocks

    def __decompose_juntehai_jantou(self, counter: list[int]) -> Generator[list[TehaiBlock], None, None]:
        for i in range(34):
            if counter[i] >= 2:
                jantou = TehaiBlock(type="jantou", hais=[i, i], minan="an")
                counter[i] -= 2
                yield [jantou]
                counter[i] += 2

    def __decompose_juntehai_mentsu(
        self, counter: list[int], start: int = 0
    ) -> Generator[list[TehaiBlock], None, None]:
        if sum(counter) == 0:
            yield []
            return

        for i in range(start, 34):
            if i <= 26 and i % 9 <= 6 and counter[i] and counter[i + 1] and counter[i + 2]:
                shuntsu = TehaiBlock(type="shuntsu", hais=[i, i + 1, i + 2], minan="an")
                counter[i] -= 1
                counter[i + 1] -= 1
                counter[i + 2] -= 1
                for mentsus in self.__decompose_juntehai_mentsu(counter, i):
                    yield [shuntsu] + mentsus
                counter[i] += 1
                counter[i + 1] += 1
                counter[i + 2] += 1

            if counter[i] >= 3:
                koutsu = TehaiBlock(type="koutsu", hais=[i, i, i], minan="an")
                counter[i] -= 3
                for mentsus in self.__decompose_juntehai_mentsu(counter, i + 1):
                    yield [koutsu] + mentsus
                counter[i] += 3

            if counter[i] > 0:
                break

    def __select_block_including_agarihai(self, blocks: list[TehaiBlock]) -> Generator[list[TehaiBlock], None, None]:
        seen = set()
        agarihai = self.agarihai.id // 4
        for block in blocks:
            if agarihai in block.hais and block not in seen:
                block.agarihai = agarihai
                if not self.is_tsumo_agari:
                    block.minan = "min"
                yield copy.deepcopy(blocks)
                block.agarihai = None
                block.minan = "an"
                seen.add(block)
