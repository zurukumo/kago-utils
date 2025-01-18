import copy
from typing import Generator, Literal

from kago_utils.actions import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup


class TehaiBlock:
    type: Literal["jantou", "shuntsu", "koutsu", "kantsu"]
    minan: Literal["min", "an"]
    hais: list[int]
    agari_hai: int | None

    __slots__ = ("type", "hais", "minan", "agari_hai")

    def __init__(
        self,
        type: Literal["jantou", "shuntsu", "koutsu", "kantsu"],
        hais: list[int],
        minan: Literal["min", "an"] = "an",
        agari_hai: int | None = None,
    ):
        self.type = type
        self.hais = hais
        self.minan = minan
        self.agari_hai = agari_hai

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TehaiBlock):
            return False

        return (
            self.type == other.type
            and self.hais == other.hais
            and self.minan == other.minan
            and self.agari_hai == other.agari_hai
        )

    def __hash__(self) -> int:
        return hash((self.type, self.minan, tuple(self.hais), self.agari_hai))

    def __repr__(self) -> str:
        return f'TehaiBlock("{self.type}", {self.minan}, {self.hais}, {self.agari_hai})'


class TehaiDecomposer:
    juntehai: HaiGroup
    huuros: list[Chii | Pon | Kakan | Daiminkan | Ankan]
    agari_hai: Hai
    is_tsumoho: bool

    __slots__ = ("juntehai", "huuros", "agari_hai", "is_tsumoho")

    def __init__(
        self,
        juntehai: HaiGroup,
        huuros: list[Chii | Pon | Kakan | Daiminkan | Ankan],
        agari_hai: Hai,
        is_tsumoho: bool,
    ):
        self.juntehai = juntehai
        self.huuros = huuros
        self.agari_hai = agari_hai
        self.is_tsumoho = is_tsumoho

    def decompose(self) -> Generator[list[TehaiBlock], None, None]:
        huuro_blocks = []
        for huuro in self.huuros:
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
        counter = self.juntehai.to_counter34()
        for jantou in self.__decompose_juntehai_jantou(counter):
            for mentsus in self.__decompose_juntehai_mentsu(counter):
                for blocks in self.__select_block_including_agari_hai(jantou + mentsus):
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

    def __select_block_including_agari_hai(self, blocks: list[TehaiBlock]) -> Generator[list[TehaiBlock], None, None]:
        seen = set()
        agari_hai = self.agari_hai.id // 4
        for block in blocks:
            if agari_hai in block.hais and block not in seen:
                block.agari_hai = agari_hai
                if not self.is_tsumoho:
                    block.minan = "min"
                yield copy.deepcopy(blocks)
                block.agari_hai = None
                block.minan = "an"
                seen.add(block)
