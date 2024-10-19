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
        self.hais.validate()

        self.__validate_length_of_hais_is_3()
        self.__validate_hais_are_consecutive()
        self.__validate_hais_are_not_zihai()
        self.__validate_hais_are_same_suit()
        self.__validate_hais_contain_stolen()
        self.__validate_from_who_is_kamicha()

    def __validate_length_of_hais_is_3(self) -> None:
        if len(self.hais) != 3:
            raise ValueError('Invalid Chii: length of hais should be 3')

    def __validate_hais_are_consecutive(self) -> None:
        if not (self.hais[0].number == self.hais[1].number - 1 == self.hais[2].number - 2):
            raise ValueError('Invalid Chii: hais should be consecutive')

    def __validate_hais_are_not_zihai(self) -> None:
        if 'z' in (self.hais[0].suit, self.hais[1].suit, self.hais[2].suit):
            raise ValueError('Invalid Chii: hais should not contain zihai')

    def __validate_hais_are_same_suit(self) -> None:
        if not (self.hais[0].suit == self.hais[1].suit == self.hais[2].suit):
            raise ValueError('Invalid Chii: hais should be the same suit')

    def __validate_hais_contain_stolen(self) -> None:
        if self.stolen not in self.hais:
            raise ValueError('Invalid Chii: hais should contain stolen hai')

    def __validate_from_who_is_kamicha(self) -> None:
        if self.from_who != Zaichi.KAMICHA:
            raise ValueError('Invalid Chii: from_who should be Zaichi.KAMICHA')

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Chii):
            return all((
                self.hais == other.hais,
                self.stolen == other.stolen,
                self.from_who == other.from_who
            ))

        raise TypeError(f"Unsupported operand type(s) for =: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Chii):
            return not self == other

        raise TypeError(f"Unsupported operand type(s) for !=: '{type(self).__name__}' and '{type(other).__name__}'")


class Pon:
    hais: Hai136Group
    stolen: Hai136
    from_who: Zaichi

    __slots__ = ('hais', 'stolen', 'from_who')

    def __init__(self, hais: Hai136Group, stolen: Hai136, from_who: Zaichi) -> None:
        self.hais = hais
        self.stolen = stolen
        self.from_who = from_who

        self.__validate()

    def __validate(self) -> None:
        self.hais.validate()

        self.__validate_length_of_hais_is_3()
        self.__validate_hais_are_same_face()
        self.__validate_hais_contain_stolen()
        self.__validate_from_who_is_taacha()

    def __validate_length_of_hais_is_3(self) -> None:
        if len(self.hais) != 3:
            raise ValueError('Invalid Pon: length of hais should be 3')

    def __validate_hais_are_same_face(self) -> None:
        if not (self.hais[0].face == self.hais[1].face == self.hais[2].face):
            raise ValueError('Invalid Pon: hais should be the same face')

    def __validate_hais_contain_stolen(self) -> None:
        if self.stolen not in self.hais:
            raise ValueError('Invalid Pon: hais should contain stolen hai')

    def __validate_from_who_is_taacha(self) -> None:
        if self.from_who not in [Zaichi.KAMICHA, Zaichi.TOIMEN, Zaichi.SIMOCHA]:
            raise ValueError('Invalid Pon: from_who should be Zaichi.KAMICHA, Zaichi.TOIMEN, or Zaichi.SIMOCHA')

    def to_kakan(self) -> Kakan:
        base_id = self.hais[0].id - (self.hais[0].id % 4)
        new_hais = Hai136Group.from_list([base_id, base_id + 1, base_id + 2, base_id + 3])
        added = (new_hais - self.hais)[0]

        return Kakan(
            hais=new_hais,
            stolen=self.stolen,
            added=added,
            from_who=self.from_who,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Pon):
            return all((
                self.hais == other.hais,
                self.stolen == other.stolen,
                self.from_who == other.from_who
            ))

        raise TypeError(f"Unsupported operand type(s) for =: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Pon):
            return not self == other

        raise TypeError(f"Unsupported operand type(s) for !=: '{type(self).__name__}' and '{type(other).__name__}'")


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
        self.hais.validate()

        self.__validate_length_of_hais_is_4()
        self.__validate_hais_are_same_face()
        self.__validate_hais_contain_stolen()
        self.__validate_hais_contain_added()
        self.__validate_from_who_is_taacha()

    def __validate_length_of_hais_is_4(self) -> None:
        if len(self.hais) != 4:
            raise ValueError('Invalid Kakan: length of hais should be 4')

    def __validate_hais_are_same_face(self) -> None:
        if not (self.hais[0].face == self.hais[1].face == self.hais[2].face == self.hais[3].face):
            raise ValueError('Invalid Kakan: hais should be the same face')

    def __validate_hais_contain_stolen(self) -> None:
        if self.stolen not in self.hais:
            raise ValueError('Invalid Kakan: hais should contain stolen hai')

    def __validate_hais_contain_added(self) -> None:
        if self.added not in self.hais:
            raise ValueError('Invalid Kakan: hais should contain added hai')

    def __validate_from_who_is_taacha(self) -> None:
        if self.from_who not in [Zaichi.KAMICHA, Zaichi.TOIMEN, Zaichi.SIMOCHA]:
            raise ValueError('Invalid Kakan: from_who should be Zaichi.KAMICHA, Zaichi.TOIMEN, or Zaichi.SIMOCHA')

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Kakan):
            return all((
                self.hais == other.hais,
                self.stolen == other.stolen,
                self.added == other.added,
                self.from_who == other.from_who
            ))

        raise TypeError(f"Unsupported operand type(s) for =: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Kakan):
            return not self == other

        raise TypeError(f"Unsupported operand type(s) for !=: '{type(self).__name__}' and '{type(other).__name__}'")


class Daiminkan:
    hais: Hai136Group
    stolen: Hai136
    from_who: Zaichi

    __slots__ = ('hais', 'stolen', 'from_who')

    def __init__(self, hais: Hai136Group, stolen: Hai136, from_who: Zaichi) -> None:
        self.hais = hais
        self.stolen = stolen
        self.from_who = from_who

        self.__validate()

    def __validate(self) -> None:
        self.hais.validate()

        self.__validate_length_of_hais_is_4()
        self.__validate_hais_are_same_face()
        self.__validate_hais_contain_stolen()
        self.__validate_from_who_is_taacha()

    def __validate_length_of_hais_is_4(self) -> None:
        if len(self.hais) != 4:
            raise ValueError('Invalid Daiminkan: length of hais should be 4')

    def __validate_hais_are_same_face(self) -> None:
        if not (self.hais[0].face == self.hais[1].face == self.hais[2].face == self.hais[3].face):
            raise ValueError('Invalid Daiminkan: hais should be the same face')

    def __validate_hais_contain_stolen(self) -> None:
        if self.stolen not in self.hais:
            raise ValueError('Invalid Daiminkan: hais should contain stolen hai')

    def __validate_from_who_is_taacha(self) -> None:
        if self.from_who not in [Zaichi.KAMICHA, Zaichi.TOIMEN, Zaichi.SIMOCHA]:
            raise ValueError('Invalid Daiminkan: from_who should be Zaichi.KAMICHA, Zaichi.TOIMEN, or Zaichi.SIMOCHA')

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Daiminkan):
            return all((
                self.hais == other.hais,
                self.stolen == other.stolen,
                self.from_who == other.from_who
            ))

        raise TypeError(f"Unsupported operand type(s) for =: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Daiminkan):
            return not self == other

        raise TypeError(f"Unsupported operand type(s) for !=: '{type(self).__name__}' and '{type(other).__name__}'")


class Ankan:
    hais: Hai136Group
    from_who: Zaichi

    __slots__ = ('hais', 'from_who')

    def __init__(self, hais: Hai136Group) -> None:
        self.hais = hais
        self.from_who = Zaichi.JICHA

        self.__validate()

    def __validate(self) -> None:
        self.hais.validate()

        self.__validate_length_of_hais_is_4()
        self.__validate_hais_are_same_face()
        self.__validate_from_who_is_jicha()

    def __validate_length_of_hais_is_4(self) -> None:
        if len(self.hais.to_list()) != 4:
            raise ValueError('Invalid Ankan: length of hais should be 4')

    def __validate_hais_are_same_face(self) -> None:
        if not (self.hais[0].face == self.hais[1].face == self.hais[2].face == self.hais[3].face):
            raise ValueError('Invalid Ankan: hais should be the same face')

    def __validate_from_who_is_jicha(self) -> None:
        if self.from_who != Zaichi.JICHA:
            raise ValueError('Invalid Ankan: from_who should be Zaichi.JICHA')

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ankan):
            return all((
                self.hais == other.hais,
                self.from_who == other.from_who
            ))

        raise TypeError(f"Unsupported operand type(s) for =: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Ankan):
            return not self == other

        raise TypeError(f"Unsupported operand type(s) for !=: '{type(self).__name__}' and '{type(other).__name__}'")
