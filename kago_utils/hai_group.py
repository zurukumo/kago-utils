from __future__ import annotations

import warnings
from collections.abc import Sequence
from typing import Iterator, Self, overload

from kago_utils.hai import Hai


class HaiGroup(Sequence[Hai]):
    hais: list[Hai]

    __slots__ = ("hais",)

    def __init__(self, hais: list[Hai]) -> None:
        self.hais = sorted(hais)

    @classmethod
    def from_counter34(cls, counter: list[int]) -> Self:
        warnings.warn(
            "Hai.from_counter34 forcibly converts args into Hai instances, which may lead to inconsistencies.",
            UserWarning,
        )

        if len(counter) != 34:
            raise ValueError(f"Invalid counter: length of counter is {len(counter)}, but expected 34.")

        if any(v < 0 for v in counter):
            raise ValueError(f"Invalid counter: found negative values in counter. Data: {counter}")

        if any(not isinstance(v, int) for v in counter):
            raise ValueError(f"Invalid counter: found non-integer values in counter. Data: {counter}")

        hais = []
        for id, count in enumerate(counter):
            for offset in range(count):
                hais.append(Hai(id * 4 + offset))
        return cls(hais)

    def to_counter34(self) -> list[int]:
        counter = [0] * 34
        for hai in self.hais:
            counter[hai.id // 4] += 1
        return counter

    @classmethod
    def from_counter(cls, counter: list[int]) -> Self:
        if len(counter) != 136:
            raise ValueError(f"Invalid counter: length of counter is {len(counter)}, but expected 136.")

        if any(v < 0 for v in counter):
            raise ValueError(f"Invalid counter: found negative values in counter. Data: {counter}")

        if any(not isinstance(v, int) for v in counter):
            raise ValueError(f"Invalid counter: found non-integer values in counter. Data: {counter}")

        hais = []
        for id, count in enumerate(counter):
            for _ in range(count):
                hais.append(Hai(id))
        return cls(hais)

    def to_counter(self) -> list[int]:
        counter = [0] * 136
        for hai in self.hais:
            counter[hai.id] += 1
        return counter

    @classmethod
    def from_list34(cls, _list: list[int]) -> Self:
        warnings.warn(
            "Hai.from_list34 forcibly converts args into Hai instances, which may lead to inconsistencies.",
            UserWarning,
        )

        if any(not isinstance(v, int) for v in _list):
            raise ValueError(f"Invalid list: found non-integer values in list. Data: {_list}")

        if any(not 0 <= v <= 33 for v in _list):
            raise ValueError(f"Invalid list: values should be between 0 and 33. Data: {_list}")

        hais = []
        offsets = [0] * 34
        for id in sorted(_list):
            hais.append(Hai(id * 4 + offsets[id]))
            offsets[id] += 1
        return cls(hais)

    def to_list34(self) -> list[int]:
        return [hai.id // 4 for hai in self.hais]

    @classmethod
    def from_list(cls, _list: list[int]) -> Self:
        if any(not isinstance(v, int) for v in _list):
            raise ValueError(f"Invalid list: found non-integer values in list. Data: {_list}")

        if any(not 0 <= v <= 135 for v in _list):
            raise ValueError(f"Invalid list: values should be between 0 and 135. Data: {_list}")

        return cls([Hai(hai) for hai in sorted(_list)])

    def to_list(self) -> list[int]:
        return [hai.id for hai in self.hais]

    @classmethod
    def from_string(cls, string: str) -> Self:
        warnings.warn(
            "Hai.from_string forcibly converts args into Hai instances, which may lead to inconsistencies.",
            UserWarning,
        )

        hais = []
        rest = cls.from_list(list(range(136)))
        suit = ""
        for c in reversed(string):
            if c in "0123456789":
                if suit == "":
                    raise ValueError(f"Invalid string: found values without suit. Data: {string}")
                if suit == "z" and c in "089":
                    raise ValueError(f"Invalid string: found invalid value '{c}' in suit 'z'. Data: {string}")

                for hai in rest:
                    if c != "0" and hai.suit == suit and hai.number == int(c) and hai.color == "b":
                        hais.append(hai)
                        rest -= hai
                        break
                    if c == "0" and hai.suit == suit and hai.number == 5 and hai.color == "r":
                        hais.append(hai)
                        rest -= hai
                        break
                else:
                    raise ValueError(f"Invalid string: found too many same hais. Data: {string}")
            elif c in "mpsz":
                suit = c
            else:
                raise ValueError(
                    f"Invalid string: found invalid character '{c}'. "
                    f"Expected 'm', 'p', 's', 'z', or '0'-'9'. Data: {string}"
                )
        return cls(hais)

    def to_string(self) -> str:
        parts = {"m": "", "p": "", "s": "", "z": ""}
        for hai in self.hais:
            if hai.color == "r":
                parts[hai.suit] += "0"
            else:
                parts[hai.suit] += str(hai.number)

        string = ""
        for suit, v in parts.items():
            if v != "":
                string += v + suit
        return string

    def validate(self) -> None:
        counter = self.to_counter()
        if any(not 0 <= v <= 1 for v in counter):
            raise ValueError(f"Invalid data: the count of each hai should be between 0 and 1. Data: {self.__repr__()}")

    def validate_as_juntehai(self) -> None:
        self.validate()

        counter = self.to_counter()
        if sum(counter) > 14:
            raise ValueError(f"Invalid data: the total count of hais should be 14 or less. Data: {self.__repr__()}")
        if sum(counter) % 3 == 0:
            raise ValueError(f"Invalid data: the total count of hais should be 3n+1 or 3n+2. Data: {self.__repr__()}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HaiGroup):
            return self.hais == other.hais

        return False

    def __add__(self, other: object) -> Self:
        match other:
            case Hai():
                new_hais = self.hais + [other]
                return self.__class__(new_hais)
            case HaiGroup():
                new_hais = self.hais + other.hais
                return self.__class__(new_hais)

        raise TypeError(f"Unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __sub__(self, other: object) -> Self:
        match other:
            case Hai():
                new_hais = self.hais.copy()
                if other not in new_hais:
                    raise ValueError(f"Invalid data: {other} is not in left-hand side data, so cannot be subtracted.")
                new_hais.remove(other)
                return self.__class__(new_hais)
            case HaiGroup():
                new_hais = self.hais.copy()
                for hai in other.hais:
                    if hai not in new_hais:
                        raise ValueError(
                            f"Invalid data: {hai} is not in left-hand side data, so cannot be subtracted."
                        )
                    new_hais.remove(hai)
                return self.__class__(new_hais)

        raise TypeError(f"Unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")

    def __or__(self, other: object) -> Self:
        if isinstance(other, HaiGroup):
            new_hais = [max(a, b) for a, b in zip(self.to_counter(), other.to_counter())]
            return self.__class__.from_counter(new_hais)

        raise TypeError(f"Unsupported operand type(s) for |: '{type(self).__name__}' and '{type(other).__name__}'")

    def __and__(self, other: object) -> Self:
        if isinstance(other, HaiGroup):
            new_hais = [min(a, b) for a, b in zip(self.to_counter(), other.to_counter())]
            return self.__class__.from_counter(new_hais)

        raise TypeError(f"Unsupported operand type(s) for &: '{type(self).__name__}' and '{type(other).__name__}'")

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
