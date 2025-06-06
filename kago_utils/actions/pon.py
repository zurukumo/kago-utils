from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi

from .kakan import Kakan


class Pon:
    hais: HaiGroup
    stolen: Hai
    from_who: Zaichi

    __slots__ = ("hais", "stolen", "from_who")

    def __init__(self, hais: HaiGroup, stolen: Hai, from_who: Zaichi) -> None:
        self.hais = hais
        self.stolen = stolen
        self.from_who = from_who

        self.__validate()

    def __validate(self) -> None:
        self.hais.validate()

        self.__validate_length_of_hais_is_3()
        self.__validate_hais_are_same_suit_and_number()
        self.__validate_hais_contain_stolen()
        self.__validate_from_who_is_taacha()

    def __validate_length_of_hais_is_3(self) -> None:
        if len(self.hais) != 3:
            raise ValueError("Invalid Pon: length of hais should be 3")

    def __validate_hais_are_same_suit_and_number(self) -> None:
        if not (
            self.hais[0].suit == self.hais[1].suit == self.hais[2].suit
            and self.hais[0].number == self.hais[1].number == self.hais[2].number
        ):
            raise ValueError("Invalid Pon: hais should be the same name")

    def __validate_hais_contain_stolen(self) -> None:
        if self.stolen not in self.hais:
            raise ValueError("Invalid Pon: hais should contain stolen hai")

    def __validate_from_who_is_taacha(self) -> None:
        if self.from_who not in [Zaichi.KAMICHA, Zaichi.TOIMEN, Zaichi.SHIMOCHA]:
            raise ValueError("Invalid Pon: from_who should be Zaichi.KAMICHA, Zaichi.TOIMEN, or Zaichi.SHIMOCHA")

    def can_become_kakan(self, kakan: Kakan) -> bool:
        return all(
            (
                self.hais == kakan.hais - kakan.added,
                self.stolen == kakan.stolen,
                self.from_who == kakan.from_who,
            )
        )

    def to_kakan(self) -> Kakan:
        base_id = self.hais[0].id - (self.hais[0].id % 4)
        new_hais = HaiGroup.from_list([base_id, base_id + 1, base_id + 2, base_id + 3])
        added = (new_hais - self.hais)[0]

        return Kakan(
            hais=new_hais,
            stolen=self.stolen,
            added=added,
            from_who=self.from_who,
        )

    def is_similar_to(self, other: object) -> bool:
        if not isinstance(other, Pon):
            return False

        return all(
            (
                self.hais.to_code() == other.hais.to_code(),
                self.stolen == other.stolen,
                self.from_who == other.from_who,
            )
        )

    @property
    def kuikae_hais(self) -> HaiGroup:
        id = self.hais[0].id - self.hais[0].id % 4
        return HaiGroup.from_list([id, id + 1, id + 2, id + 3])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Pon):
            return all((self.hais == other.hais, self.stolen == other.stolen, self.from_who == other.from_who))

        return False

    def __repr__(self) -> str:
        return f"Pon(hais={self.hais}, stolen={self.stolen}, from_who={self.from_who})"
