from abc import ABC, abstractmethod
from typing import Self


class Hai(ABC):
    @abstractmethod
    def to_hai34_counter(self) -> 'Hai34Counter':
        pass

    @abstractmethod
    def to_hai34_list(self) -> 'Hai34List':
        pass

    @abstractmethod
    def to_hai34_string(self) -> 'Hai34String':
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class Hai34(Hai):
    @classmethod
    @abstractmethod
    def from_hai34(cls, hai34: 'Hai34') -> Self:
        pass

    def __add__(self, other: Hai) -> Self:
        if isinstance(other, Hai):
            new_data = [a + b for a, b in zip(self.to_hai34_counter().data, other.to_hai34_counter().data)]
            return self.__class__.from_hai34(Hai34Counter(new_data))

        raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __sub__(self, other: Hai) -> Self:
        if isinstance(other, Hai):
            new_data = [a - b for a, b in zip(self.to_hai34_counter().data, other.to_hai34_counter().data)]
            return self.__class__.from_hai34(Hai34Counter(new_data))

        raise TypeError(f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")


class Hai136(Hai):
    @abstractmethod
    def to_hai136_counter(self) -> 'Hai136Counter':
        pass

    @abstractmethod
    def to_hai136_list(self) -> 'Hai136List':
        pass

    @classmethod
    @abstractmethod
    def from_hai136(cls, hai136: 'Hai136') -> Self:
        pass

    def __add__(self, other: 'Hai136') -> Self:
        if isinstance(other, Hai136):
            new_data = [a + b for a, b in zip(self.to_hai136_counter().data, other.to_hai136_counter().data)]
            return self.__class__.from_hai136(Hai136Counter(new_data))

        raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __sub__(self, other: 'Hai136') -> Self:
        if isinstance(other, Hai136):
            new_data = [a - b for a, b in zip(self.to_hai136_counter().data, other.to_hai136_counter().data)]
            return self.__class__.from_hai136(Hai136Counter(new_data))

        raise TypeError(f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")


class Hai34Counter(Hai34):
    data: list[int]

    def __init__(self, data: list[int]):
        self.data = self.normalize(data)

    def normalize(self, data: list[int]) -> list[int]:
        if len(data) != 34:
            raise ValueError(f"invalid data: len(data) = {len(data)} (expected 34)")
        for k, v in enumerate(data):
            if not isinstance(v, int):
                raise ValueError(f"invalid data: type(data[{k}]) = {type(v)} (expected int)")
            if not 0 <= v <= 4:
                raise ValueError(f"invalid data: data[{k}] = {v} (expected 0 <= v <= 4)")

        return data

    def to_hai34_counter(self) -> 'Hai34Counter':
        return self

    def to_hai34_list(self) -> 'Hai34List':
        hai_list = []
        for hai, count in enumerate(self.data):
            for _ in range(count):
                hai_list.append(hai)
        return Hai34List(hai_list)

    def to_hai34_string(self) -> 'Hai34String':
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
    def from_hai34(cls, hai34: 'Hai34') -> 'Hai34Counter':
        return hai34.to_hai34_counter()

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.data}"

    def __repr__(self) -> str:
        return self.__str__()


class Hai34List(Hai34):
    data: list[int]

    def __init__(self, data: list[int]):
        self.data = self.normalize(data)

    def normalize(self, data: list[int]) -> list[int]:
        for hai in data:
            if not isinstance(hai, int):
                raise ValueError(f"invalid data: type({hai}) = {type(hai)} (expected int)")
            if not 0 <= hai <= 33:
                raise ValueError(f"invalid data: {hai} (expected 0 <= value <= 33)")

        for i in range(34):
            if not 0 <= data.count(i) <= 4:
                raise ValueError(f"invalid data: count({i}) = {data.count(i)} (expected 0 <= count <= 4)")
        return sorted(data)

    def to_hai34_counter(self) -> 'Hai34Counter':
        hai_counter = [0] * 34
        for hai in self.data:
            hai_counter[hai] += 1
        return Hai34Counter(hai_counter)

    def to_hai34_list(self) -> 'Hai34List':
        return self

    def to_hai34_string(self) -> 'Hai34String':
        return self.to_hai34_counter().to_hai34_string()

    @classmethod
    def from_hai34(cls, hai34: 'Hai34') -> 'Hai34List':
        return hai34.to_hai34_list()

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.data}"

    def __repr__(self) -> str:
        return self.__str__()


class Hai34String(Hai34):
    data: str

    def __init__(self, data: str):
        self.data = self.normalize(data)

    def normalize(self, data: str) -> str:
        items = {'m': [0] * 9, 'p': [0] * 9, 's': [0] * 9, 'z': [0] * 9}
        suit = ''
        for c in reversed(data):
            if c in '123456789':
                if suit == '':
                    raise ValueError("invalid data: there is a number without suit")
                items[suit][int(c) - 1] += 1
            elif c in 'mpsz':
                suit = c
            else:
                raise ValueError(f"invalid data: {c} (expected 'mpsz' or '123456789')")

        for suit in items:
            for k, v in enumerate(items[suit]):
                if not 0 <= v <= 4:
                    raise ValueError(f"invalid data: count({suit}{k + 1}) = {v} (expected 0 <= count <= 4)")

        data = ''
        for suit in items:
            for k, v in enumerate(items[suit]):
                data += f"{k + 1}" * v
            if sum(items[suit]) > 0:
                data += suit

        return data

    def to_hai34_counter(self) -> 'Hai34Counter':
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

    def to_hai34_list(self) -> 'Hai34List':
        return self.to_hai34_counter().to_hai34_list()

    def to_hai34_string(self) -> 'Hai34String':
        return self

    @classmethod
    def from_hai34(cls, hai34: 'Hai34') -> 'Hai34String':
        return hai34.to_hai34_string()

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.data}"

    def __repr__(self) -> str:
        return self.__str__()


class Hai136Counter(Hai136):
    data: list[int]

    def __init__(self, data: list[int]):
        self.data = self.normalize(data)

    def normalize(self, data: list[int]) -> list[int]:
        if len(data) != 136:
            raise ValueError(f"invalid data: len(data) = {len(data)} (expected 136)")
        for k, v in enumerate(data):
            if not isinstance(v, int):
                raise ValueError(f"invalid data: type(data[{k}]) = {type(v)} (expected int)")
            if not 0 <= v <= 1:
                raise ValueError(f"invalid data: data[{k}] = {v} (expected 0 <= v <= 1)")

        return data

    def to_hai34_counter(self) -> 'Hai34Counter':
        hai_counter = [0] * 34
        for hai, count in enumerate(self.data):
            hai_counter[hai // 4] += count
        return Hai34Counter(hai_counter)

    def to_hai34_list(self) -> 'Hai34List':
        return self.to_hai34_counter().to_hai34_list()

    def to_hai34_string(self) -> 'Hai34String':
        return self.to_hai34_counter().to_hai34_string()

    def to_hai136_counter(self) -> 'Hai136Counter':
        return self

    def to_hai136_list(self) -> 'Hai136List':
        hai_list = []
        for hai, count in enumerate(self.data):
            if count == 1:
                hai_list.append(hai)
        return Hai136List(hai_list)

    @classmethod
    def from_hai136(cls, hai136: 'Hai136') -> 'Hai136Counter':
        return hai136.to_hai136_counter()

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.data}"

    def __repr__(self) -> str:
        return self.__str__()


class Hai136List(Hai136):
    data: list[int]

    def __init__(self, data: list[int]):
        self.data = self.normalize(data)

    def normalize(self, data: list[int]) -> list[int]:
        for hai in data:
            if not isinstance(hai, int):
                raise ValueError(f"invalid data: type({hai}) = {type(hai)} (expected int)")
            if not 0 <= hai <= 135:
                raise ValueError(f"invalid data: {hai} (expected 0 <= value <= 135)")

        for i in range(136):
            if not 0 <= data.count(i) <= 1:
                raise ValueError(f"invalid data: count({i}) = {data.count(i)} (expected 0 <= count <= 1)")
        return sorted(data)

    def to_hai34_counter(self) -> 'Hai34Counter':
        hai_counter = [0] * 34
        for hai in self.data:
            hai_counter[hai // 4] += 1
        return Hai34Counter(hai_counter)

    def to_hai34_list(self) -> 'Hai34List':
        return self.to_hai34_counter().to_hai34_list()

    def to_hai34_string(self) -> 'Hai34String':
        return self.to_hai34_counter().to_hai34_string()

    def to_hai136_counter(self) -> 'Hai136Counter':
        hai_counter = [0] * 136
        for hai in self.data:
            hai_counter[hai] += 1
        return Hai136Counter(hai_counter)

    def to_hai136_list(self) -> 'Hai136List':
        return self

    @classmethod
    def from_hai136(cls, hai136: 'Hai136') -> 'Hai136List':
        return hai136.to_hai136_list()

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.data}"

    def __repr__(self) -> str:
        return self.__str__()
