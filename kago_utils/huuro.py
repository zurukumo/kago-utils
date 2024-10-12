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
