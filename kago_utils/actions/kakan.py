from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi


class Kakan:
    hais: HaiGroup
    stolen: Hai
    added: Hai
    from_who: Zaichi

    __slots__ = ("hais", "stolen", "added", "from_who")

    def __init__(self, hais: HaiGroup, stolen: Hai, added: Hai, from_who: Zaichi) -> None:
        self.hais = hais
        self.stolen = stolen
        self.added = added
        self.from_who = from_who

        self.__validate()

    def __validate(self) -> None:
        self.hais.validate()

        self.__validate_length_of_hais_is_4()
        self.__validate_hais_are_same_suit_and_number()
        self.__validate_hais_contain_stolen()
        self.__validate_hais_contain_added()
        self.__validate_from_who_is_taacha()

    def __validate_length_of_hais_is_4(self) -> None:
        if len(self.hais) != 4:
            raise ValueError("Invalid Kakan: length of hais should be 4")

    def __validate_hais_are_same_suit_and_number(self) -> None:
        if not (
            self.hais[0].suit == self.hais[1].suit == self.hais[2].suit == self.hais[3].suit
            and self.hais[0].number == self.hais[1].number == self.hais[2].number == self.hais[3].number
        ):
            raise ValueError("Invalid Kakan: hais should be the same name")

    def __validate_hais_contain_stolen(self) -> None:
        if self.stolen not in self.hais:
            raise ValueError("Invalid Kakan: hais should contain stolen hai")

    def __validate_hais_contain_added(self) -> None:
        if self.added not in self.hais:
            raise ValueError("Invalid Kakan: hais should contain added hai")

    def __validate_from_who_is_taacha(self) -> None:
        if self.from_who not in [Zaichi.KAMICHA, Zaichi.TOIMEN, Zaichi.SHIMOCHA]:
            raise ValueError("Invalid Kakan: from_who should be Zaichi.KAMICHA, Zaichi.TOIMEN, or Zaichi.SHIMOCHA")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Kakan):
            return all(
                (
                    self.hais == other.hais,
                    self.stolen == other.stolen,
                    self.added == other.added,
                    self.from_who == other.from_who,
                )
            )

        return False

    def __repr__(self) -> str:
        return f"Kakan(hais={self.hais}, stolen={self.stolen}, added={self.added}, from_who={self.from_who})"
