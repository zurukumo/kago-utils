from __future__ import annotations

from typing import override

from kago_utils.hai import (Hai34Counter, Hai34List, Hai34String,
                            Hai136Counter, Hai136List)
from kago_utils.zaichi import Zaichi


class Huuro[T: Hai34Counter | Hai34List | Hai34String | Hai136Counter | Hai136List]:
    hai: T
    stolen: T | None
    added: T | None
    from_who: Zaichi

    __slots__ = ('hai', 'stolen', 'added', 'from_who')

    def __init__(self, hai: T, stolen: T | None, added: T | None, from_who: Zaichi) -> None:
        self.hai = hai
        self.stolen = stolen
        self.added = added
        self.from_who = from_who

    def validate(self) -> None:
        pass

    @classmethod
    def from_haihu(cls, m: int) -> (
        Chii[Hai136List] | Pon[Hai136List] | Ankan[Hai136List] | Daiminkan[Hai136List] | Kakan[Hai136List]
    ):
        if cls.is_ankan(m):
            return cls.parse_ankan(m)
        elif cls.is_daiminkan(m):
            return cls.parse_daiminkan(m)
        elif cls.is_kakan(m):
            return cls.parse_kakan(m)

        raise ValueError('Invalid Huuro')

    @classmethod
    def is_ankan(cls, m: int) -> bool:
        return (m & 0x003c) == 0 and cls.parse_from_who(m) == Zaichi.JICHA

    @classmethod
    def is_daiminkan(cls, m: int) -> bool:
        return (m & 0x003c) == 0 and cls.parse_from_who(m) != Zaichi.JICHA

    @classmethod
    def is_kakan(cls, m: int) -> bool:
        return (m & 0x0004) == 0 and (m & 0x0010) == 1

    @classmethod
    def is_pon(cls, m: int) -> bool:
        return (m & 0x0004) == 0 and (m & 0x0008) == 1

    @classmethod
    def is_chii(cls, m: int) -> bool:
        return (m & 0x0004) == 1

    @classmethod
    def parse_ankan(cls, m: int) -> Ankan[Hai136List]:
        h1 = ((m & 0xFF00) >> 8) // 4 * 4
        return Ankan(hai=Hai136List([h1, h1 + 1, h1 + 2, h1 + 3]))

    @classmethod
    def parse_daiminkan(cls, m: int) -> Daiminkan[Hai136List]:
        stolen_hai = (m & 0xFF00) >> 8
        h1 = stolen_hai - stolen_hai % 4
        from_who = cls.parse_from_who(m)
        return Daiminkan(
            hai=Hai136List([h1, h1+1, h1+2, h1+3]),
            stolen=Hai136List([stolen_hai]),
            from_who=from_who
        )

    @classmethod
    def parse_kakan(cls, m: int) -> Kakan[Hai136List]:
        stolen_hai = (m & 0xFE00) >> 9
        h1 = stolen_hai - stolen_hai % 4
        added_hai = h1 + ((m & 0x0060) >> 5)
        from_who = cls.parse_from_who(m)
        return Kakan(
            hai=Hai136List([h1, h1+1, h1+2, h1+3]),
            stolen=Hai136List([stolen_hai]),
            added=Hai136List([added_hai]),
            from_who=from_who
        )

    @classmethod
    def parse_pon(cls, m: int) -> Pon[Hai136List]:
        pattern = (m & 0xFE00) >> 9
        h1 = pattern - pattern % 4
        stolen_hai = pattern
        unused_hai = h1 + ((m & 0x0060) >> 5)
        from_who = cls.parse_from_who(m)
        return Pon(
            hai=Hai136List([h1, h1+1, h1+2, h1+3]) - Hai136List([unused_hai]),
            stolen=Hai136List([stolen_hai]),
            from_who=from_who
        )

    @classmethod
    def parse_chii(cls, m: int) -> Chii[Hai136List]:
        pattern = (m & 0xFC00) >> 10
        h1 = ((pattern // 21) * 9 + (pattern // 3) % 7) * 4 + (m & 0x0018) >> 3
        h2 = ((pattern // 21) * 9 + (pattern // 3) % 7 + 1) * 4 + (m & 0x0060) >> 5
        h3 = ((pattern // 21) * 9 + (pattern // 3) % 7 + 2) * 4 + (m & 0x0180) >> 7
        stolen_hai = [h1, h2, h3][pattern % 3]
        return Chii(
            hai=Hai136List([h1, h2, h3]),
            stolen=Hai136List([stolen_hai]),
        )

    @classmethod
    def parse_from_who(cls, m: int) -> Zaichi:
        return [Zaichi.JICHA, Zaichi.SIMOCHA, Zaichi.TOIMEN, Zaichi.KAMICHA][m & 0x0003]


class Chii[T: Hai34Counter | Hai34List | Hai34String | Hai136Counter | Hai136List](Huuro[T]):
    def __init__(self, hai: T, stolen: T) -> None:
        super().__init__(hai, stolen, None, Zaichi.KAMICHA)

    @override
    def validate(self) -> None:
        self.validate_length_3()

    def validate_length_3(self) -> None:
        if len(self.hai.to_hai34_list().data) != 3:
            raise ValueError('Invalid Chii: length should be 3')

    def validate_consecutive(self) -> None:
        hai_list = self.hai.to_hai34_list()
        if not (hai_list.data[0] == hai_list.data[1] - 1 == hai_list.data[2] - 2):
            raise ValueError('Invalid Chii: should be consecutive')

    def validate_same_suit(self) -> None:
        hai_list = self.hai.to_hai34_list()
        if not (hai_list.data[0] // 9 == hai_list.data[1] // 9 == hai_list.data[2] // 9):
            raise ValueError('Invalid Chii: should be the same suit')


class Pon[T: Hai34Counter | Hai34List | Hai34String | Hai136Counter | Hai136List](Huuro[T]):
    def __init__(self, hai: T, stolen: T, from_who: Zaichi) -> None:
        super().__init__(hai, stolen, None, from_who)

    @override
    def validate(self) -> None:
        self.validate_length_3()

    def validate_length_3(self) -> None:
        if len(self.hai.to_hai34_list().data) != 3:
            raise ValueError('Invalid Pon: length should be 3')

    def validate_same_hai(self) -> None:
        hai_list = self.hai.to_hai34_list()
        if not (hai_list.data[0] == hai_list.data[1] == hai_list.data[2]):
            raise ValueError('Invalid Pon: should be the same hai')


class Ankan[T: Hai34Counter | Hai34List | Hai34String | Hai136Counter | Hai136List](Huuro[T]):
    def __init__(self, hai: T) -> None:
        super().__init__(hai, None, None, Zaichi.JICHA)

    @override
    def validate(self) -> None:
        self.validate_length_4()
        self.validate_same_hai()

    def validate_length_4(self) -> None:
        if len(self.hai.to_hai34_list().data) != 4:
            raise ValueError('Invalid Ankan: length should be 4')

    def validate_same_hai(self) -> None:
        hai_list = self.hai.to_hai34_list()
        if not (hai_list.data[0] == hai_list.data[1] == hai_list.data[2] == hai_list.data[3]):
            raise ValueError('Invalid Ankan: should be the same hai')


class Daiminkan[T: Hai34Counter | Hai34List | Hai34String | Hai136Counter | Hai136List](Huuro[T]):
    def __init__(self, hai: T, stolen: T, from_who: Zaichi) -> None:
        super().__init__(hai, stolen, None, from_who)

    @override
    def validate(self) -> None:
        self.validate_length_4()
        self.validate_same_hai()

    def validate_length_4(self) -> None:
        if len(self.hai.to_hai34_list().data) != 4:
            raise ValueError('Invalid Daiminkan: length should be 4')

    def validate_same_hai(self) -> None:
        hai_list = self.hai.to_hai34_list()
        if not (hai_list.data[0] == hai_list.data[1] == hai_list.data[2] == hai_list.data[3]):
            raise ValueError('Invalid Daiminkan: should be the same hai')


class Kakan[T: Hai34Counter | Hai34List | Hai34String | Hai136Counter | Hai136List](Huuro[T]):
    def __init__(self, hai: T, stolen: T, added: T, from_who: Zaichi) -> None:
        super().__init__(hai, stolen, added, from_who)

    @override
    def validate(self) -> None:
        self.validate_length_4()
        self.validate_same_hai()

    def validate_length_4(self) -> None:
        if len(self.hai.to_hai34_list().data) != 4:
            raise ValueError('Invalid Kakan: length should be 4')

    def validate_same_hai(self) -> None:
        hai_list = self.hai.to_hai34_list()
        if not (hai_list.data[0] == hai_list.data[1] == hai_list.data[2] == hai_list.data[3]):
            raise ValueError('Invalid Kakan: should be the same hai')
