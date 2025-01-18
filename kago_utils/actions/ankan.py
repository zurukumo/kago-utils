from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi


class Ankan:
    hais: HaiGroup
    from_who: Zaichi

    __slots__ = ("hais", "from_who")

    def __init__(self, hais: HaiGroup) -> None:
        self.hais = hais
        self.from_who = Zaichi.JICHA

        self.__validate()

    def __validate(self) -> None:
        self.hais.validate()

        self.__validate_length_of_hais_is_4()
        self.__validate_hais_are_same_suit_and_number()
        self.__validate_from_who_is_jicha()

    def __validate_length_of_hais_is_4(self) -> None:
        if len(self.hais) != 4:
            raise ValueError("Invalid Ankan: length of hais should be 4")

    def __validate_hais_are_same_suit_and_number(self) -> None:
        if not (
            self.hais[0].suit == self.hais[1].suit == self.hais[2].suit == self.hais[3].suit
            and self.hais[0].number == self.hais[1].number == self.hais[2].number == self.hais[3].number
        ):
            raise ValueError("Invalid Ankan: hais should be the same name")

    def __validate_from_who_is_jicha(self) -> None:
        if self.from_who != Zaichi.JICHA:
            raise ValueError("Invalid Ankan: from_who should be Zaichi.JICHA")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ankan):
            return all((self.hais == other.hais, self.from_who == other.from_who))

        return False

    def __repr__(self) -> str:
        return f"Ankan(hais={self.hais}, from_who={self.from_who})"
