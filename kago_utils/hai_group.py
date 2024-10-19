from __future__ import annotations

from typing import Self

from kago_utils.hai import Hai34, Hai136


class Hai34Group:
    hais: list[Hai34]

    __slots__ = ('hais',)

    def __init__(self, hais: list[Hai34]) -> None:
        self.hais = sorted(hais)

    def to_hai34_group(self) -> Hai34Group:
        return self

    @classmethod
    def from_counter(cls, counter: list[int]) -> Self:
        cls.__validate_counter(counter)
        hais = []
        for hai, count in enumerate(counter):
            for _ in range(count):
                hais.append(Hai34(hai))
        return cls(hais)

    def to_counter(self) -> list[int]:
        counter = [0] * 34
        for hai in self.hais:
            counter[hai.id] += 1
        return counter

    @staticmethod
    def __validate_counter(counter: list[int]) -> None:
        if len(counter) != 34:
            raise ValueError(f"Invalid counter: length of counter is {len(counter)}, but expected 34.")

        if any(v < 0 for v in counter):
            raise ValueError(f"Invalid counter: found negative values in counter. Data: {counter}")

        if any(not isinstance(v, int) for v in counter):
            raise ValueError(f"Invalid counter: found non-integer values in counter. Data: {counter}")

    @classmethod
    def from_list(cls, _list: list[int]) -> Self:
        cls.__validate_list(_list)
        return cls([Hai34(hai) for hai in _list])

    def to_list(self) -> list[int]:
        return [hai.id for hai in self.hais]

    @staticmethod
    def __validate_list(_list: list[int]) -> None:
        if any(not isinstance(v, int) for v in _list):
            raise ValueError(f"Invalid list: found non-integer values in list. Data: {_list}")

        if any(not 0 <= v <= 33 for v in _list):
            raise ValueError(f"Invalid list: values should be between 0 and 33. Data: {_list}")

    @classmethod
    def from_string(cls, string: str) -> Self:
        cls.__validate_string(string)
        hais = []
        suit = ''
        for c in reversed(string):
            if c in '123456789':
                if suit == '':
                    raise ValueError(f"Invalid string: found values without suit. Data: {string}")
                hais.append(Hai34(int(c) - 1 + {'m': 0, 'p': 9, 's': 18, 'z': 27}[suit]))
            elif c in 'mpsz':
                suit = c
        return cls(hais)

    def to_string(self) -> str:
        items = {'m': [0] * 9, 'p': [0] * 9, 's': [0] * 9, 'z': [0] * 7}
        for hai in self.hais:
            items[{'m': 'm', 'p': 'p', 's': 's', 'z': 'z'}[hai.suit]][hai.number] += 1
        string = ''
        for suit in items:
            for k, v in enumerate(items[suit]):
                string += f"{k + 1}" * v
            if sum(items[suit]) > 0:
                string += suit
        return string

    @staticmethod
    def __validate_string(string: str) -> None:
        suit = ''
        for c in reversed(string):
            if c in '123456789':
                if suit == '':
                    raise ValueError(f"Invalid string: found values without suit. Data: {string}")
            elif c in 'mpsz':
                suit = c
            else:
                raise ValueError(
                    f"Invalid string: found invalid character '{c}'. "
                    f"Expected 'm', 'p', 's', 'z', or '1'-'9'. Data: {string}"
                )

    def validate(self) -> None:
        counter = self.to_counter()
        if any(not 0 <= v <= 4 for v in counter):
            raise ValueError(f"Invalid data: the count of each hai should be between 0 and 4. Data: {self.__repr__()}")

    def validate_as_jun_tehai(self) -> None:
        self.validate()

        counter = self.to_counter()
        if sum(counter) > 14:
            raise ValueError(f"Invalid data: the total count of hais should be 14 or less. Data: {self.__repr__()}")
        if sum(counter) % 3 == 0:
            raise ValueError(f"Invalid data: the total count of hais should be 3n+1 or 3n+2. Data: {self.__repr__()}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Hai34Group):
            return self.hais == other.hais

        raise TypeError(f"Unsupported operand type(s) for ==: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Hai34Group):
            return self.hais != other.hais

        raise TypeError(f"Unsupported operand type(s) for !=: '{type(self).__name__}' and '{type(other).__name__}'")

    def __add__(self, other: object) -> Self:
        match other:
            case Hai34():
                new_hais = self.hais + [other]
                return self.__class__(new_hais)
            case Hai34Group():
                new_hais = self.hais + other.hais
                return self.__class__(new_hais)

        raise TypeError(f"Unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __sub__(self, other: object) -> Self:
        match other:
            case Hai34():
                new_hais = self.hais.copy()
                if other not in new_hais:
                    raise ValueError(f"Invalid data: {other} is not in left-hand data, so cannot be subtracted.")
                new_hais.remove(other)
                return self.__class__(new_hais)
            case Hai34Group():
                new_hais = self.hais.copy()
                for hai in other.hais:
                    if hai not in new_hais:
                        raise ValueError(
                            f"Invalid data: {hai} is not in left-hand data, so cannot be subtracted.")
                    new_hais.remove(hai)
                return self.__class__(new_hais)

        raise TypeError(f"Unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")

    def __or__(self, other: object) -> Self:
        if isinstance(other, Hai34Group):
            new_hais = [max(a, b) for a, b in zip(self.to_counter(), other.to_counter())]
            return self.__class__.from_counter(new_hais)
        elif isinstance(other, Hai136Group):
            new_hais = [max(a, b) for a, b in zip(self.to_counter(), other.to_hai34_group().to_counter())]
            return self.__class__.from_counter(new_hais)

        raise TypeError(f"Unsupported operand type(s) for |: '{type(self).__name__}' and '{type(other).__name__}'")

    def __and__(self, other: object) -> Self:
        if isinstance(other, Hai34Group):
            new_hais = [min(a, b) for a, b in zip(self.to_counter(), other.to_counter())]
            return self.__class__.from_counter(new_hais)
        elif isinstance(other, Hai136Group):
            new_hais = [min(a, b) for a, b in zip(self.to_counter(), other.to_hai34_group().to_counter())]
            return self.__class__.from_counter(new_hais)

        raise TypeError(f"Unsupported operand type(s) for &: '{type(self).__name__}' and '{type(other).__name__}'")

    def __len__(self) -> int:
        return len(self.hais)

    def __getitem__(self, key: int) -> Hai34:
        return self.hais[key]

    def __contains__(self, item: object) -> bool:
        if isinstance(item, Hai34):
            return item in self.hais

        raise TypeError(f"Unsupported operand type(s) for in: '{type(self).__name__}' and '{type(item).__name__}'")


class Hai136Group:
    hais: list[Hai136]

    __slots__ = ('hais',)

    def __init__(self, hais: list[Hai136]) -> None:
        self.hais = sorted(hais)

    def to_hai34_group(self) -> Hai34Group:
        return Hai34Group([hai.to_hai34() for hai in self.hais])

    @classmethod
    def from_counter(cls, counter: list[int]) -> Self:
        cls.__validate_counter(counter)
        hais = []
        for hai, count in enumerate(counter):
            for _ in range(count):
                hais.append(Hai136(hai))
        return cls(hais)

    def to_counter(self) -> list[int]:
        counter = [0] * 136
        for hai in self.hais:
            counter[hai.id] += 1
        return counter

    @staticmethod
    def __validate_counter(counter: list[int]) -> None:
        if len(counter) != 136:
            raise ValueError(f"Invalid counter: length of counter is {len(counter)}, but expected 136.")

        if any(v < 0 for v in counter):
            raise ValueError(f"Invalid counter: found negative values in counter. Data: {counter}")

        if any(not isinstance(v, int) for v in counter):
            raise ValueError(f"Invalid counter: found non-integer values in counter. Data: {counter}")

    @classmethod
    def from_list(cls, _list: list[int]) -> Self:
        cls.__validate_list(_list)
        return cls([Hai136(hai) for hai in sorted(_list)])

    def to_list(self) -> list[int]:
        return [hai.id for hai in self.hais]

    @staticmethod
    def __validate_list(_list: list[int]) -> None:
        if any(not isinstance(v, int) for v in _list):
            raise ValueError(f"Invalid list: found non-integer values in list. Data: {_list}")

        if any(not 0 <= v <= 135 for v in _list):
            raise ValueError(f"Invalid list: values should be between 0 and 135. Data: {_list}")

    def to_string(self) -> str:
        return self.to_hai34_group().to_string()

    def validate(self) -> None:
        counter = self.to_counter()
        if any(not 0 <= v <= 1 for v in counter):
            raise ValueError(f"Invalid data: the count of each hai should be between 0 and 4. Data: {self.__repr__()}")

    def validate_as_jun_tehai(self) -> None:
        self.validate()

        counter = self.to_counter()
        if sum(counter) > 14:
            raise ValueError(f"Invalid data: the total count of hais should be 14 or less. Data: {self.__repr__()}")
        if sum(counter) % 3 == 0:
            raise ValueError(f"Invalid data: the total count of hais should be 3n+1 or 3n+2. Data: {self.__repr__()}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Hai136Group):
            return self.hais == other.hais

        raise TypeError(f"Unsupported operand type(s) for ==: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Hai136Group):
            return self.hais != other.hais

        raise TypeError(f"Unsupported operand type(s) for !=: '{type(self).__name__}' and '{type(other).__name__}'")

    def __add__(self, other: object) -> Self:
        match other:
            case Hai136():
                new_hais = self.hais + [other]
                return self.__class__(new_hais)
            case Hai136Group():
                new_hais = self.hais + other.hais
                return self.__class__(new_hais)

        raise TypeError(f"Unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __sub__(self, other: object) -> Self:
        match other:
            case Hai136():
                new_hais = self.hais.copy()
                if other not in new_hais:
                    raise ValueError(f"Invalid data: {other} is not in left-hand side data, so cannot be subtracted.")
                new_hais.remove(other)
                return self.__class__(new_hais)
            case Hai136Group():
                new_hais = self.hais.copy()
                for hai in other.hais:
                    if hai not in new_hais:
                        raise ValueError(
                            f"Invalid data: {hai} is not in left-hand side data, so cannot be subtracted.")
                    new_hais.remove(hai)
                return self.__class__(new_hais)

        raise TypeError(f"Unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")

    def __or__(self, other: object) -> Self:
        if isinstance(other, Hai136Group):
            new_hais = [max(a, b) for a, b in zip(self.to_counter(), other.to_counter())]
            return self.__class__.from_counter(new_hais)

        raise TypeError(f"Unsupported operand type(s) for |: '{type(self).__name__}' and '{type(other).__name__}'")

    def __and__(self, other: object) -> Self:
        if isinstance(other, Hai136Group):
            new_hais = [min(a, b) for a, b in zip(self.to_counter(), other.to_counter())]
            return self.__class__.from_counter(new_hais)

        raise TypeError(f"Unsupported operand type(s) for &: '{type(self).__name__}' and '{type(other).__name__}'")

    def __len__(self) -> int:
        return len(self.hais)

    def __getitem__(self, key: int) -> Hai136:
        return self.hais[key]

    def __contains__(self, item: object) -> bool:
        if isinstance(item, Hai136):
            return item in self.hais

        raise TypeError(f"Unsupported operand type(s) for in: '{type(self).__name__}' and '{type(item).__name__}'")
