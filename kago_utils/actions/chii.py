from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi


class Chii:
    hais: HaiGroup
    stolen: Hai
    from_who: Zaichi

    __slots__ = ("hais", "stolen", "from_who")

    def __init__(self, hais: HaiGroup, stolen: Hai) -> None:
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
            raise ValueError("Invalid Chii: length of hais should be 3")

    def __validate_hais_are_consecutive(self) -> None:
        if not (self.hais[0].number == self.hais[1].number - 1 == self.hais[2].number - 2):
            raise ValueError("Invalid Chii: hais should be consecutive")

    def __validate_hais_are_not_zihai(self) -> None:
        if "z" in (self.hais[0].suit, self.hais[1].suit, self.hais[2].suit):
            raise ValueError("Invalid Chii: hais should not contain zihai")

    def __validate_hais_are_same_suit(self) -> None:
        if not (self.hais[0].suit == self.hais[1].suit == self.hais[2].suit):
            raise ValueError("Invalid Chii: hais should be the same suit")

    def __validate_hais_contain_stolen(self) -> None:
        if self.stolen not in self.hais:
            raise ValueError("Invalid Chii: hais should contain stolen hai")

    def __validate_from_who_is_kamicha(self) -> None:
        if self.from_who != Zaichi.KAMICHA:
            raise ValueError("Invalid Chii: from_who should be Zaichi.KAMICHA")

    @property
    def kuikae_hais(self) -> HaiGroup:
        hais = HaiGroup([])
        if self.hais[0] == self.stolen:
            id1 = self.hais[0].id - self.hais[0].id % 4
            hais += HaiGroup.from_list([id1, id1 + 1, id1 + 2, id1 + 3])
            if self.hais[0].number != 7:
                id2 = id1 + 12
                hais += HaiGroup.from_list([id2, id2 + 1, id2 + 2, id2 + 3])
        elif self.hais[1] == self.stolen:
            id = self.hais[1].id - self.hais[1].id % 4
            hais += HaiGroup.from_list([id, id + 1, id + 2, id + 3])
        elif self.hais[2] == self.stolen:
            id1 = self.hais[2].id - self.hais[2].id % 4
            hais += HaiGroup.from_list([id1, id1 + 1, id1 + 2, id1 + 3])
            if self.hais[2].number != 3:
                id2 = id1 - 12
                hais += HaiGroup.from_list([id2, id2 + 1, id2 + 2, id2 + 3])

        return hais

    def is_similar_to(self, other: object) -> bool:
        if not isinstance(other, Chii):
            return False

        return all(
            (
                self.hais.to_code() == other.hais.to_code(),
                self.stolen == other.stolen,
                self.from_who == other.from_who,
            )
        )
        return self.stolen == other.stolen and self.from_who == other.from_who

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Chii):
            return all((self.hais == other.hais, self.stolen == other.stolen, self.from_who == other.from_who))

        return False

    def __repr__(self) -> str:
        return f"Chii(hais={self.hais}, stolen={self.stolen}, from_who={self.from_who})"
