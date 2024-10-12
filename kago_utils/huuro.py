from __future__ import annotations

from kago_utils.hai import Hai136
from kago_utils.hai_group import Hai136Group
from kago_utils.zaichi import Zaichi


class Chii:
    hais: Hai136Group
    stolen: Hai136
    from_who: Zaichi

    __slots__ = ('hais', 'stolen', 'from_who')

    def __init__(self, hais: Hai136Group, stolen: Hai136) -> None:
        self.hais = hais
        self.stolen = stolen
        self.from_who = Zaichi.KAMICHA

        self.__validate()

    def __validate(self) -> None:
        self.__validate_length_3()
        self.__validate_consecutive()
        self.__validate_same_suit()

    def __validate_length_3(self) -> None:
        if len(self.hais.to_list()) != 3:
            raise ValueError('Invalid Chii: length should be 3')

    def __validate_consecutive(self) -> None:
        hai_list = self.hais.to_list()
        if not (hai_list[0] == hai_list[1] - 1 == hai_list[2] - 2):
            raise ValueError('Invalid Chii: should be consecutive')

    def __validate_same_suit(self) -> None:
        hai_list = self.hais.to_list()
        if not (hai_list[0] // 9 == hai_list[1] // 9 == hai_list[2] // 9):
            raise ValueError('Invalid Chii: should be the same suit')


class Pon:
    hais: Hai136Group
    stolen: Hai136
    from_who: Zaichi

    __slots__ = ('hais', 'stolen', 'from_who')

    def __init__(self, hai: Hai136Group, stolen: Hai136, from_who: Zaichi) -> None:
        self.hais = hai
        self.stolen = stolen
        self.from_who = from_who

    def validate(self) -> None:
        self.validate_length_3()
        self.validate_same_hai()

    def validate_length_3(self) -> None:
        if len(self.hais.to_list()) != 3:
            raise ValueError('Invalid Pon: length should be 3')

    def validate_same_hai(self) -> None:
        hai_list = self.hais.to_list()
        if not (hai_list[0] == hai_list[1] == hai_list[2]):
            raise ValueError('Invalid Pon: should be the same hai')


class Ankan:
    hais: Hai136Group

    __slots__ = ('hais',)

    def __init__(self, hais: Hai136Group) -> None:
        self.hais = hais

        self.__validate()

    def __validate(self) -> None:
        self.__validate_length_4()
        self.__validate_same_hai()

    def __validate_length_4(self) -> None:
        if len(self.hais.to_list()) != 4:
            raise ValueError('Invalid Ankan: length should be 4')

    def __validate_same_hai(self) -> None:
        hai_list = self.hais.to_list()
        if not (hai_list[0] == hai_list[1] == hai_list[2] == hai_list[3]):
            raise ValueError('Invalid Ankan: should be the same hai')


class Daiminkan:
    hais: Hai136Group
    stolen: Hai136
    from_who: Zaichi

    def __init__(self, hais: Hai136Group, stolen: Hai136, from_who: Zaichi) -> None:
        self.hais = hais
        self.stolen = stolen
        self.from_who = from_who

        self.__validate()

    def __validate(self) -> None:
        self.__validate_length_4()
        self.__validate_same_hai()

    def __validate_length_4(self) -> None:
        if len(self.hais.to_list()) != 4:
            raise ValueError('Invalid Daiminkan: length should be 4')

    def __validate_same_hai(self) -> None:
        hai_list = self.hais.to_list()
        if not (hai_list[0] == hai_list[1] == hai_list[2] == hai_list[3]):
            raise ValueError('Invalid Daiminkan: should be the same hai')


class Kakan:
    hais: Hai136Group
    stolen: Hai136
    added: Hai136
    from_who: Zaichi

    __slots__ = ('hais', 'stolen', 'added', 'from_who')

    def __init__(self, hais: Hai136Group, stolen: Hai136, added: Hai136, from_who: Zaichi) -> None:
        self.hais = hais
        self.stolen = stolen
        self.added = added
        self.from_who = from_who

        self.__validate()

    def __validate(self) -> None:
        self.__validate_length_4()
        self.__validate_same_hai()

    def __validate_length_4(self) -> None:
        if len(self.hais.to_list()) != 4:
            raise ValueError('Invalid Kakan: length should be 4')

    def __validate_same_hai(self) -> None:
        hai_list = self.hais.to_list()
        if not (hai_list[0] == hai_list[1] == hai_list[2] == hai_list[3]):
            raise ValueError('Invalid Kakan: should be the same hai')


class Huuro:
    @classmethod
    def from_haihu(cls, m: int) -> (Chii | Pon | Ankan | Daiminkan | Kakan):
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
    def parse_ankan(cls, m: int) -> Ankan:
        h1 = ((m & 0xFF00) >> 8) // 4 * 4
        return Ankan(hais=Hai136Group.from_list([h1, h1 + 1, h1 + 2, h1 + 3]))

    @classmethod
    def parse_daiminkan(cls, m: int) -> Daiminkan:
        stolen_hai = (m & 0xFF00) >> 8
        h1 = stolen_hai - stolen_hai % 4
        from_who = cls.parse_from_who(m)
        return Daiminkan(
            hais=Hai136Group.from_list([h1, h1+1, h1+2, h1+3]),
            stolen=Hai136(stolen_hai),
            from_who=from_who
        )

    @classmethod
    def parse_kakan(cls, m: int) -> Kakan:
        stolen_hai = (m & 0xFE00) >> 9
        h1 = stolen_hai - stolen_hai % 4
        added_hai = h1 + ((m & 0x0060) >> 5)
        from_who = cls.parse_from_who(m)
        return Kakan(
            hais=Hai136Group.from_list([h1, h1+1, h1+2, h1+3]),
            stolen=Hai136(stolen_hai),
            added=Hai136(added_hai),
            from_who=from_who
        )

    @classmethod
    def parse_pon(cls, m: int) -> Pon:
        pattern = (m & 0xFE00) >> 9
        h1 = pattern - pattern % 4
        stolen_hai = pattern
        unused_hai = h1 + ((m & 0x0060) >> 5)
        from_who = cls.parse_from_who(m)
        return Pon(
            hai=Hai136Group.from_list([h1, h1+1, h1+2, h1+3]) - Hai136Group.from_list([unused_hai]),
            stolen=Hai136(stolen_hai),
            from_who=from_who
        )

    @classmethod
    def parse_chii(cls, m: int) -> Chii:
        pattern = (m & 0xFC00) >> 10
        h1 = ((pattern // 21) * 9 + (pattern // 3) % 7) * 4 + (m & 0x0018) >> 3
        h2 = ((pattern // 21) * 9 + (pattern // 3) % 7 + 1) * 4 + (m & 0x0060) >> 5
        h3 = ((pattern // 21) * 9 + (pattern // 3) % 7 + 2) * 4 + (m & 0x0180) >> 7
        stolen_hai = [h1, h2, h3][pattern % 3]
        return Chii(
            hais=Hai136Group.from_list([h1, h2, h3]),
            stolen=Hai136(stolen_hai),
        )

    @classmethod
    def parse_from_who(cls, m: int) -> Zaichi:
        return [Zaichi.JICHA, Zaichi.SIMOCHA, Zaichi.TOIMEN, Zaichi.KAMICHA][m & 0x0003]
