from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self, override


class Hai[T](ABC):
    data: T

    __slots__ = ('data',)

    def __init__(self, data: T) -> None:
        self.data = self.normalize(data)

    @abstractmethod
    def normalize(self, data: T) -> T:
        return data

    @abstractmethod
    def to_hai34_counter(self) -> Hai34Counter:
        pass

    @abstractmethod
    def to_hai34_list(self) -> Hai34List:
        pass

    @abstractmethod
    def to_hai34_string(self) -> Hai34String:
        pass

    @abstractmethod
    def validate_as_jun_tehai(self) -> None:
        pass

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.data}"

    def __repr__(self) -> str:
        return self.__str__()


class Hai34[T](Hai[T]):
    @classmethod
    @abstractmethod
    def from_hai34(cls, hai34: Hai34Counter | Hai34List | Hai34String) -> Self:
        pass

    @override
    def validate_as_jun_tehai(self) -> None:
        hai34_counter = self.to_hai34_counter()
        if sum(hai34_counter.data) > 14:
            raise ValueError(f"Invalid data: the total count of hais should be 14 or less. Data: {self.__repr__()}")
        if sum(hai34_counter.data) % 3 == 0:
            raise ValueError(f"Invalid data: the total count of hais should be 3n+1 or 3n+2. Data: {self.__repr__()}")
        if any(not 0 <= count <= 4 for count in hai34_counter.data):
            raise ValueError(f"Invalid data: the count of each hai should be between 0 and 4. Data: {self.__repr__()}")

    def __add__(self, other: Hai34Counter | Hai34List | Hai34String | Hai136Counter | Hai136List) -> Self:
        if isinstance(other, (Hai34Counter, Hai34List, Hai34String, Hai136Counter, Hai136List)):
            new_data = [a + b for a, b in zip(self.to_hai34_counter().data, other.to_hai34_counter().data)]
            return self.__class__.from_hai34(Hai34Counter(new_data))

        raise TypeError(f"Unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __sub__(self, other: Hai34Counter | Hai34List | Hai34String | Hai136Counter | Hai136List) -> Self:
        if isinstance(other, (Hai34Counter, Hai34List, Hai34String, Hai136Counter, Hai136List)):
            new_data = [a - b for a, b in zip(self.to_hai34_counter().data, other.to_hai34_counter().data)]
            return self.__class__.from_hai34(Hai34Counter(new_data))

        raise TypeError(f"Unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")


class Hai136[T](Hai[T]):
    @abstractmethod
    def to_hai136_counter(self) -> Hai136Counter:
        pass

    @abstractmethod
    def to_hai136_list(self) -> Hai136List:
        pass

    @classmethod
    @abstractmethod
    def from_hai136(cls, hai136: Hai136Counter | Hai136List) -> Self:
        pass

    @override
    def validate_as_jun_tehai(self) -> None:
        hai136_counter = self.to_hai136_counter()
        if sum(hai136_counter.data) > 14:
            raise ValueError(f"Invalid data: the total count of hais should be 14 or less. Data: {self.__repr__()}")

        if sum(hai136_counter.data) % 3 == 0:
            raise ValueError(f"Invalid data: the total count of hais should be 3n+1 or 3n+2. Data: {self.__repr__()}")

        if any(not 0 <= count <= 1 for count in hai136_counter.data):
            raise ValueError(f"Invalid data: the count of each hai should be between 0 and 1. Data: {self.__repr__()}")

    def __add__(self, other: Hai136Counter | Hai136List) -> Self:
        if isinstance(other, (Hai136Counter, Hai136List)):
            new_data = [a + b for a, b in zip(self.to_hai136_counter().data, other.to_hai136_counter().data)]
            return self.__class__.from_hai136(Hai136Counter(new_data))

        raise TypeError(f"Unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __sub__(self, other: Hai136Counter | Hai136List) -> Self:
        if isinstance(other, (Hai136Counter, Hai136List)):
            new_data = [a - b for a, b in zip(self.to_hai136_counter().data, other.to_hai136_counter().data)]
            return self.__class__.from_hai136(Hai136Counter(new_data))

        raise TypeError(f"Unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")


class Hai34Counter(Hai34[list[int]]):
    @override
    def normalize(self, data: list[int]) -> list[int]:
        if len(data) != 34:
            raise ValueError(f"Invalid data: length of data is {len(data)}, but expected 34.")

        if any(v < 0 for v in data):
            raise ValueError(f"Invalid data: found negative values in data. Data: {data}")

        if any(not isinstance(v, int) for v in data):
            raise ValueError(f"Invalid data: found non-integer values in data. Data: {data}")

        return data

    @override
    def to_hai34_counter(self) -> Hai34Counter:
        return self

    @override
    def to_hai34_list(self) -> Hai34List:
        hai_list = []
        for hai, count in enumerate(self.data):
            for _ in range(count):
                hai_list.append(hai)
        return Hai34List(hai_list)

    @override
    def to_hai34_string(self) -> Hai34String:
        items: dict[str, list[int]] = {'m': [], 'p': [], 's': [], 'z': []}
        for hai, count in enumerate(self.data):
            for _ in range(count):
                if hai < 9:
                    items['m'] .append(hai + 1)
                elif hai < 18:
                    items['p'].append(hai - 8)
                elif hai < 27:
                    items['s'].append(hai - 17)
                else:
                    items['z'].append(hai - 26)

        hai_string = ''
        for suit in items:
            if items[suit]:
                hai_string += f"{''.join(map(str, items[suit]))}{suit}"
        return Hai34String(hai_string)

    @classmethod
    @override
    def from_hai34(cls, hai34: Hai34Counter | Hai34List | Hai34String) -> Hai34Counter:
        return hai34.to_hai34_counter()


class Hai34List(Hai34[list[int]]):
    @override
    def normalize(self, data: list[int]) -> list[int]:
        if any(not isinstance(v, int) for v in data):
            raise ValueError(f"Invalid data: found non-integer values in data. Data: {data}")

        if any(not 0 <= v <= 33 for v in data):
            raise ValueError(f"Invalid data: values should be between 0 and 33. Data: {data}")

        return sorted(data)

    @override
    def to_hai34_counter(self) -> Hai34Counter:
        hai_counter = [0] * 34
        for hai in self.data:
            hai_counter[hai] += 1
        return Hai34Counter(hai_counter)

    @override
    def to_hai34_list(self) -> Hai34List:
        return self

    @override
    def to_hai34_string(self) -> Hai34String:
        return self.to_hai34_counter().to_hai34_string()

    @classmethod
    @override
    def from_hai34(cls, hai34: Hai34Counter | Hai34List | Hai34String) -> Hai34List:
        return hai34.to_hai34_list()


class Hai34String(Hai34[str]):
    @override
    def normalize(self, data: str) -> str:
        items = {'m': [0] * 9, 'p': [0] * 9, 's': [0] * 9, 'z': [0] * 9}
        suit = ''
        for c in reversed(data):
            if c in '123456789':
                if suit == '':
                    raise ValueError("Invalid data: found values without suit. Data: {data}")
                items[suit][int(c) - 1] += 1
            elif c in 'mpsz':
                suit = c
            else:
                raise ValueError(
                    f"Invalid data: found invalid character '{c}'. "
                    f"Expected 'm', 'p', 's', 'z', or '1'-'9'. Data: {data}"
                )

        data = ''
        for suit in items:
            for k, v in enumerate(items[suit]):
                data += f"{k + 1}" * v
            if sum(items[suit]) > 0:
                data += suit

        return data

    @override
    def to_hai34_counter(self) -> Hai34Counter:
        hai_counter = [0] * 34
        suit = ''
        for c in reversed(self.data):
            if c in '123456789':
                hai = int(c) - 1
                if suit == 'm':
                    hai_counter[hai] += 1
                elif suit == 'p':
                    hai_counter[hai + 9] += 1
                elif suit == 's':
                    hai_counter[hai + 18] += 1
                elif suit == 'z':
                    hai_counter[hai + 27] += 1
            elif c in 'mpsz':
                suit = c
        return Hai34Counter(hai_counter)

    @override
    def to_hai34_list(self) -> Hai34List:
        return self.to_hai34_counter().to_hai34_list()

    @override
    def to_hai34_string(self) -> Hai34String:
        return self

    @classmethod
    @override
    def from_hai34(cls, hai34: Hai34Counter | Hai34List | Hai34String) -> Hai34String:
        return hai34.to_hai34_string()


class Hai136Counter(Hai136[list[int]]):
    @override
    def normalize(self, data: list[int]) -> list[int]:
        if len(data) != 136:
            raise ValueError(f"Invalid data: length of data is {len(data)}, but expected 136.")

        if any(v < 0 for v in data):
            raise ValueError(f"Invalid data: found negative values in data. Data: {data}")

        if any(not isinstance(v, int) for v in data):
            raise ValueError(f"Invalid data: found non-integer values in data. Data: {data}")

        return data

    @override
    def to_hai34_counter(self) -> Hai34Counter:
        hai_counter = [0] * 34
        for hai, count in enumerate(self.data):
            hai_counter[hai // 4] += count
        return Hai34Counter(hai_counter)

    @override
    def to_hai34_list(self) -> Hai34List:
        return self.to_hai34_counter().to_hai34_list()

    @override
    def to_hai34_string(self) -> Hai34String:
        return self.to_hai34_counter().to_hai34_string()

    @override
    def to_hai136_counter(self) -> Hai136Counter:
        return self

    @override
    def to_hai136_list(self) -> Hai136List:
        hai_list = []
        for hai, count in enumerate(self.data):
            if count == 1:
                hai_list.append(hai)
        return Hai136List(hai_list)

    @classmethod
    @override
    def from_hai136(cls, hai136: Hai136Counter | Hai136List) -> Hai136Counter:
        return hai136.to_hai136_counter()


class Hai136List(Hai136[list[int]]):
    @override
    def normalize(self, data: list[int]) -> list[int]:
        if any(not isinstance(v, int) for v in data):
            raise ValueError(f"Invalid data: found non-integer values in data. Data: {data}")

        if any(not 0 <= v <= 135 for v in data):
            raise ValueError(f"Invalid data: values should be between 0 and 135. Data: {data}")

        return sorted(data)

    @override
    def to_hai34_counter(self) -> Hai34Counter:
        hai_counter = [0] * 34
        for hai in self.data:
            hai_counter[hai // 4] += 1
        return Hai34Counter(hai_counter)

    @override
    def to_hai34_list(self) -> Hai34List:
        return self.to_hai34_counter().to_hai34_list()

    @override
    def to_hai34_string(self) -> Hai34String:
        return self.to_hai34_counter().to_hai34_string()

    @override
    def to_hai136_counter(self) -> Hai136Counter:
        hai_counter = [0] * 136
        for hai in self.data:
            hai_counter[hai] += 1
        return Hai136Counter(hai_counter)

    @override
    def to_hai136_list(self) -> Hai136List:
        return self

    @classmethod
    @override
    def from_hai136(cls, hai136: Hai136Counter | Hai136List) -> Hai136List:
        return hai136.to_hai136_list()
