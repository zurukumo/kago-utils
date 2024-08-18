from abc import ABC, abstractmethod
from typing import Self


class Hai(ABC):
    def __init__(self, data):
        self.data = self.normalize(data)

    @abstractmethod
    def normalize(self, data):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.data}"

    def __repr__(self):
        return self.__str__()


class Hai34(Hai):
    @abstractmethod
    def to_hai34_counter(self) -> 'Hai34Counter':
        pass

    @abstractmethod
    def to_hai34_list(self) -> 'Hai34List':
        pass

    @abstractmethod
    def to_hai34_string(self) -> 'Hai34String':
        pass

    @classmethod
    @abstractmethod
    def from_hai34_counter(cls, hai34_counter: 'Hai34Counter') -> Self:
        pass

    def __add__(self, other) -> Self:
        if isinstance(other, (Hai34, Hai136)):
            new_data = [a + b for a, b in zip(self.to_hai34_counter().data, other.to_hai34_counter().data)]
            return self.__class__.from_hai34_counter(Hai34Counter(new_data))

        raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __sub__(self, other) -> Self:
        if isinstance(other, (Hai34, Hai136)):
            new_data = [a - b for a, b in zip(self.to_hai34_counter().data, other.to_hai34_counter().data)]
            return self.__class__.from_hai34_counter(Hai34Counter(new_data))

        raise TypeError(f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")


class Hai136(Hai):
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
    def to_hai136_list(self) -> 'Hai136List':
        pass

    @classmethod
    @abstractmethod
    def from_hai136_list(cls, hai136_list: 'Hai136List') -> Self:
        pass

    def __add__(self, other) -> Self:
        if isinstance(other, Hai136):
            new_data = self.to_hai136_list().data + other.to_hai136_list().data
            return self.__class__.from_hai136_list(Hai136List(new_data))

        raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __sub__(self, other) -> Self:
        if isinstance(other, Hai136):
            new_data = self.to_hai136_list().data.copy()
            for hai in other.to_hai136_list().data:
                new_data.remove(hai)
            return self.__class__.from_hai136_list(Hai136List(new_data))

        raise TypeError(f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")


class Hai34Counter(Hai34):
    def normalize(self, data):
        if len(data) != 34:
            raise ValueError(f"invalid data: len(data) = {len(data)} (expected 34)")
        for k, v in enumerate(data):
            if not isinstance(v, int):
                raise ValueError(f"invalid data: type(data[{k}]) = {type(v)} (expected int)")
            if not 0 <= v <= 4:
                raise ValueError(f"invalid data: data[{k}] = {v} (expected 0 <= v <= 4)")

        return data

    def to_hai34_counter(self):
        return self

    def to_hai34_list(self):
        hai_list = []
        for hai, count in enumerate(self.data):
            for _ in range(count):
                hai_list.append(hai)
        return Hai34List(hai_list)

    def to_hai34_string(self):
        items = {'m': [], 'p': [], 's': [], 'z': []}
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

    @staticmethod
    def from_hai34_counter(hai34_counter: 'Hai34Counter'):
        return hai34_counter


class Hai34List(Hai34):
    def normalize(self, data):
        for hai in data:
            if not isinstance(hai, int):
                raise ValueError(f"invalid data: type({hai}) = {type(hai)} (expected int)")
            if not 0 <= hai <= 33:
                raise ValueError(f"invalid data: {hai} (expected 0 <= value <= 33)")

        for i in range(34):
            if not 0 <= data.count(i) <= 4:
                raise ValueError(f"invalid data: count({i}) = {data.count(i)} (expected 0 <= count <= 4)")
        return sorted(data)

    def to_hai34_counter(self):
        hai_counter = [0] * 34
        for hai in self.data:
            hai_counter[hai] += 1
        return Hai34Counter(hai_counter)

    def to_hai34_list(self):
        return self

    def to_hai34_string(self):
        return self.to_hai34_counter().to_hai34_string()

    @ staticmethod
    def from_hai34_counter(hai34_counter: 'Hai34Counter'):
        return hai34_counter.to_hai34_list()


class Hai34String(Hai34):
    def normalize(self, data):
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

    def to_hai34_counter(self):
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

    def to_hai34_list(self):
        return self.to_hai34_counter().to_hai34_list()

    def to_hai34_string(self):
        return self

    @ staticmethod
    def from_hai34_counter(hai34_counter: 'Hai34Counter'):
        return hai34_counter.to_hai34_string()


class Hai136List(Hai136):
    def normalize(self, data):
        for hai in data:
            if not isinstance(hai, int):
                raise ValueError(f"invalid data: type({hai}) = {type(hai)} (expected int)")
            if not 0 <= hai <= 135:
                raise ValueError(f"invalid data: {hai} (expected 0 <= value <= 135)")

        for i in range(136):
            if not 0 <= data.count(i) <= 1:
                raise ValueError(f"invalid data: count({i}) = {data.count(i)} (expected 0 <= count <= 1)")
        return sorted(data)

    def to_hai34_counter(self):
        hai_counter = [0] * 34
        for hai in self.data:
            hai_counter[hai // 4] += 1
        return Hai34Counter(hai_counter)

    def to_hai34_list(self):
        return self.to_hai34_counter().to_hai34_list()

    def to_hai34_string(self):
        return self.to_hai34_counter().to_hai34_string()

    def to_hai136_list(self):
        return self

    @ staticmethod
    def from_hai136_list(hai136_list: 'Hai136List'):
        return hai136_list
