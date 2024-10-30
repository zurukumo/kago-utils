from __future__ import annotations

from typing import Literal


class Hai34:
    id: int

    __slots__ = ('id',)

    def __init__(self, id: int) -> None:
        self.validate(id)
        self.id = id

    def validate(self, id: int) -> None:
        if not isinstance(id, int):
            raise TypeError(f"Invalid Hai34: id should be an integer, but got {type(id).__name__}")
        if not 0 <= id <= 33:
            raise ValueError(f"Invalid Hai34: id should be between 0 and 33, but got {id}")

    def to_hai34(self) -> Hai34:
        if isinstance(self, Hai34):
            return self

        raise TypeError(f"Unsupported operand type(s) for to_hai34: '{type(self).__name__}'")

    @property
    def suit(self) -> Literal['m', 'p', 's', 'z']:
        if 0 <= self.id < 9:
            return 'm'
        elif 9 <= self.id < 18:
            return 'p'
        elif 18 <= self.id < 27:
            return 's'
        elif 27 <= self.id < 34:
            return 'z'

        raise ValueError(f"Invalid Hai34: id should be between 0 and 33, but got {self.id}")

    @property
    def number(self) -> int:
        return self.id % 9

    @property
    def face(self) -> str:
        return f"{self.number + 1}{self.suit}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Hai34):
            return self.id == other.id

        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Hai34):
            return self.id < other.id

        raise TypeError(f"Unsupported operand type(s) for <: '{type(self).__name__}' and '{type(other).__name__}'")

    def __le__(self, other: object) -> bool:
        if isinstance(other, Hai34):
            return self.id <= other.id

        raise TypeError(f"Unsupported operand type(s) for <=: '{type(self).__name__}' and '{type(other).__name__}'")

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Hai34):
            return self.id > other.id

        raise TypeError(f"Unsupported operand type(s) for >: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Hai34):
            return self.id >= other.id

        raise TypeError(f"Unsupported operand type(s) for >=: '{type(self).__name__}' and '{type(other).__name__}'")


class Hai136:
    id: int

    __slots__ = ('id',)

    def __init__(self, id: int) -> None:
        self.validate(id)
        self.id = id

    def validate(self, id: int) -> None:
        if not isinstance(id, int):
            raise TypeError(f"Invalid Hai136: id should be an integer, but got {type(id).__name__}")
        if not 0 <= id <= 135:
            raise ValueError(f"Invalid Hai136: id should be between 0 and 135, but got {id}")

    def to_hai34(self) -> Hai34:
        if isinstance(self, Hai136):
            return Hai34(self.id // 4)

        raise TypeError(f"Unsupported operand type(s) for to_hai34: '{type(self).__name__}'")

    @property
    def suit(self) -> Literal['m', 'p', 's', 'z']:
        if 0 <= self.id < 36:
            return 'm'
        elif 36 <= self.id < 72:
            return 'p'
        elif 72 <= self.id < 108:
            return 's'
        elif 108 <= self.id < 136:
            return 'z'

        raise ValueError(f"Invalid Hai136: id should be between 0 and 135, but got {self.id}")

    @property
    def number(self) -> int:
        return (self.id // 4) % 9

    @property
    def face(self) -> str:
        return f"{self.number + 1}{self.suit}"

    def is_aka(self) -> bool:
        return self.id in (16, 52, 88)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Hai136):
            return self.id == other.id

        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Hai136):
            return self.id < other.id

        raise TypeError(f"Unsupported operand type(s) for <: '{type(self).__name__}' and '{type(other).__name__}'")

    def __le__(self, other: object) -> bool:
        if isinstance(other, Hai136):
            return self.id <= other.id

        raise TypeError(f"Unsupported operand type(s) for <=: '{type(self).__name__}' and '{type(other).__name__}'")

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Hai136):
            return self.id > other.id

        raise TypeError(f"Unsupported operand type(s) for >: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Hai136):
            return self.id >= other.id

        raise TypeError(f"Unsupported operand type(s) for >=: '{type(self).__name__}' and '{type(other).__name__}'")
