from collections.abc import Sequence
from typing import Iterator, Self, overload

from kago_utils.hai import Hai


class Sutehai:
    hai: Hai


class Kawa(Sequence[Hai]):
    hais: list[Hai]

    __slot__ = ("hais",)

    def __init__(self, hais: list[Hai]) -> None:
        self.hais = hais

    def append(self, hai: Hai) -> None:
        if not isinstance(hai, Hai):
            raise TypeError(f"Expected Hai instance, got {type(hai)}")
        self.hais.append(hai)

    def __len__(self) -> int:
        return len(self.hais)

    @overload
    def __getitem__(self, key: int) -> Hai: ...

    @overload
    def __getitem__(self, key: slice) -> Self: ...

    def __getitem__(self, key: int | slice) -> Hai | Self:
        if isinstance(key, int):
            return self.hais[key]
        elif isinstance(key, slice):
            return self.__class__(self.hais[key])

        raise TypeError(f"Invalid type for key: {type(key).__name__}")

    def __iter__(self) -> Iterator[Hai]:
        return iter(self.hais)

    def __contains__(self, item: object) -> bool:
        if isinstance(item, Hai):
            return item in self.hais

        raise TypeError(f"Unsupported operand type(s) for in: '{type(self).__name__}' and '{type(item).__name__}'")

    def __repr__(self) -> str:
        return f"HaiGroup({self.hais})"
