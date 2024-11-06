from __future__ import annotations

from typing import Literal


class Hai:
    id: int

    __slots__ = ("id",)

    def __init__(self, id: int) -> None:
        self.validate(id)
        self.id = id

    def validate(self, id: int) -> None:
        if not isinstance(id, int):
            raise TypeError(f"Invalid Hai: id should be an integer, but got {type(id).__name__}")
        if not 0 <= id <= 135:
            raise ValueError(f"Invalid Hai: id should be between 0 and 135, but got {id}")

    @property
    def suit(self) -> Literal["m", "p", "s", "z"]:
        if 0 <= self.id < 36:
            return "m"
        elif 36 <= self.id < 72:
            return "p"
        elif 72 <= self.id < 108:
            return "s"
        elif 108 <= self.id < 136:
            return "z"

        raise ValueError(f"Invalid Hai: id should be between 0 and 135, but got {self.id}")

    @property
    def number(self) -> int:
        return (self.id // 4) % 9 + 1

    @property
    def color(self) -> Literal["b", "r"]:
        return "r" if self.id in (16, 52, 88) else "b"

    @property
    def face(self) -> str:
        return f"{self.number}{self.suit}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Hai):
            return self.id == other.id

        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Hai):
            return self.id < other.id

        raise TypeError(f"Unsupported operand type(s) for <: '{type(self).__name__}' and '{type(other).__name__}'")

    def __le__(self, other: object) -> bool:
        if isinstance(other, Hai):
            return self.id <= other.id

        raise TypeError(f"Unsupported operand type(s) for <=: '{type(self).__name__}' and '{type(other).__name__}'")

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Hai):
            return self.id > other.id

        raise TypeError(f"Unsupported operand type(s) for >: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Hai):
            return self.id >= other.id

        raise TypeError(f"Unsupported operand type(s) for >=: '{type(self).__name__}' and '{type(other).__name__}'")

    def __repr__(self) -> str:
        return f"Hai({self.id})"
