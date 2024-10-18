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
        self.__validate_suuhai()
        self.__validate_same_suit()

    def __validate_length_3(self) -> None:
        if len(self.hais) != 3:
            raise ValueError('Invalid Chii: length should be 3')

    def __validate_consecutive(self) -> None:
        if not (self.hais[0].number == self.hais[1].number - 1 == self.hais[2].number - 2):
            raise ValueError('Invalid Chii: should be consecutive')

    def __validate_suuhai(self) -> None:
        if 'z' in (self.hais[0].suit, self.hais[1].suit, self.hais[2].suit):
            raise ValueError('Invalid Chii: should not contain zihai')

    def __validate_same_suit(self) -> None:
        if not (self.hais[0].suit == self.hais[1].suit == self.hais[2].suit):
            raise ValueError('Invalid Chii: should be the same suit')

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

    def __validate(self) -> None:
        self.__validate_length_3()
        self.__validate_same_face()

    def __validate_length_3(self) -> None:
        if len(self.hais) != 3:
            raise ValueError('Invalid Pon: length should be 3')

    def __validate_same_face(self) -> None:
        if not (self.hais[0].face == self.hais[1].face == self.hais[2].face):
            raise ValueError('Invalid Pon: should be the same hai')

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
        self.__validate_length_4()
        self.__validate_same_face()

    def __validate_length_4(self) -> None:
        if len(self.hais) != 4:
            raise ValueError('Invalid Kakan: length should be 4')

    def __validate_same_face(self) -> None:
        if not (self.hais[0].face == self.hais[1].face == self.hais[2].face == self.hais[3].face):
            raise ValueError('Invalid Kakan: should be the same hai')

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
        self.__validate_length_4()
        self.__validate_same_face()

    def __validate_length_4(self) -> None:
        if len(self.hais) != 4:
            raise ValueError('Invalid Daiminkan: length should be 4')

    def __validate_same_face(self) -> None:
        if not (self.hais[0].face == self.hais[1].face == self.hais[2].face == self.hais[3].face):
            raise ValueError('Invalid Daiminkan: should be the same hai')

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
        self.__validate_length_4()
        self.__validate_same_face()

    def __validate_length_4(self) -> None:
        if len(self.hais.to_list()) != 4:
            raise ValueError('Invalid Ankan: length should be 4')

    def __validate_same_face(self) -> None:
        if not (self.hais[0].face == self.hais[1].face == self.hais[2].face == self.hais[3].face):
            raise ValueError('Invalid Ankan: should be the same hai')

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
