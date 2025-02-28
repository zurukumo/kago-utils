from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from kago_utils.actions import Ankan, Chii, Dahai, Daiminkan, Kakan, Pon
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.zaichi import Zaichi

if TYPE_CHECKING:
    from kago_utils.game import Game


class Player:
    id: str
    game: Game
    zaseki: int
    ten: int

    juntehai: HaiGroup
    huuros: list[Chii | Pon | Kakan | Daiminkan | Ankan]
    last_tsumo: Hai | None
    is_riichi_completed: bool
    is_right_after_riichi: bool
    is_right_after_chii: bool
    is_right_after_pon: bool
    is_right_after_rinshan_tsumo: bool

    __slots__ = (
        "id",
        "game",
        "zaseki",
        "ten",
        "juntehai",
        "huuros",
        "last_tsumo",
        "is_riichi_completed",
        "is_right_after_riichi",
        "is_right_after_chii",
        "is_right_after_pon",
        "is_right_after_rinshan_tsumo",
    )

    def __init__(self, id: str) -> None:
        self.id = id
        self.ten = 25000
        self.reset()

    def reset(self) -> None:
        self.juntehai = HaiGroup([])
        self.huuros = []
        self.last_tsumo = None
        self.is_riichi_completed = False
        self.is_right_after_riichi = False
        self.is_right_after_chii = False
        self.is_right_after_pon = False

    def tsumo(self, hai: Hai) -> None:
        self.juntehai += hai
        self.last_tsumo = hai
        self.is_right_after_rinshan_tsumo = False

    def rinshan_tsumo(self, hai: Hai) -> None:
        self.juntehai += hai
        self.last_tsumo = hai
        self.is_right_after_rinshan_tsumo = True

    def tsumoho(self) -> None:
        pass

    def ronho(self) -> None:
        pass

    def riichi(self) -> None:
        self.is_right_after_riichi = True

    def dahai(self, dahai: Dahai) -> None:
        self.juntehai -= dahai.hai
        self.game.last_dahai = dahai.hai

    def chii(self, chii: Chii) -> None:
        for candidate in self.game.non_teban_action_resolver.chii_candidates[self.id]:
            if (
                chii.hais.to_code() == candidate.hais.to_code()
                and chii.stolen == candidate.stolen
                and chii.from_who == candidate.from_who
            ):
                self.huuros.append(chii)
                self.juntehai -= chii.hais - chii.stolen
                self.is_right_after_chii = True
                return

        raise ValueError("Invalid Chii")

    def pon(self, pon: Pon) -> None:
        for candidate in self.game.non_teban_action_resolver.pon_candidates[self.id]:
            if (
                pon.hais.to_code() == candidate.hais.to_code()
                and pon.stolen == candidate.stolen
                and pon.from_who == candidate.from_who
            ):
                self.huuros.append(pon)
                self.juntehai -= pon.hais - pon.stolen
                self.is_right_after_pon = True
                return

        raise ValueError("Invalid Pon")

    def kakan(self, kakan: Kakan) -> None:
        for candaidate in self.game.teban_action_resolver.kakan_candidates[self.id]:
            if (
                kakan.hais.to_code() == candaidate.hais.to_code()
                and kakan.stolen == candaidate.stolen
                and kakan.added == candaidate.added
                and kakan.from_who == candaidate.from_who
            ):
                for i, huuro in enumerate(self.huuros):
                    if isinstance(huuro, Pon) and huuro.can_become_kakan(kakan):
                        self.huuros[i] = kakan
                        self.juntehai -= kakan.added
                        return

        raise ValueError("Invalid Kakan")

    def daiminkan(self, daiminkan: Daiminkan) -> None:
        for candidate in self.game.non_teban_action_resolver.daiminkan_candidates[self.id]:
            if (
                daiminkan.hais.to_code() == candidate.hais.to_code()
                and daiminkan.stolen == candidate.stolen
                and daiminkan.from_who == candidate.from_who
            ):
                self.huuros.append(daiminkan)
                self.juntehai -= daiminkan.hais - daiminkan.stolen
                return

        raise ValueError("Invalid Daiminkan")

    def ankan(self, ankan: Ankan) -> None:
        for candidate in self.game.teban_action_resolver.ankan_candidates[self.id]:
            if ankan.hais.to_code() == candidate.hais.to_code():
                self.huuros.append(ankan)
                self.juntehai -= ankan.hais
                return

        raise ValueError("Invalid Ankan")

    @property
    def is_oya(self) -> bool:
        return self.zaseki == self.game.kyoku % 4

    @property
    def jikaze(self) -> Literal["東", "南", "西", "北"]:
        match (self.zaseki - self.game.kyoku) % 4:
            case 0:
                return "東"
            case 1:
                return "南"
            case 2:
                return "西"
            case 3:
                return "北"

        raise Exception()

    @property
    def pao_sekinin_player(self) -> Player | None:
        n_daisuushii_huuro = 0
        n_daisangen_huuro = 0
        for huuro in self.huuros:
            if huuro.hais[0].code in ("5z", "6z", "7z"):
                n_daisangen_huuro += 1
            if huuro.hais[0].code in ("1z", "2z", "3z", "4z"):
                n_daisuushii_huuro += 1

            if n_daisangen_huuro >= 3 or n_daisuushii_huuro >= 4:
                return self.find_player_by_zaichi(huuro.from_who)

        return None

    @property
    def is_menzen(self) -> bool:
        return not any(isinstance(huuro, (Chii, Pon, Kakan, Daiminkan)) for huuro in self.huuros)

    @property
    def jicha(self) -> Player:
        return self.find_player_by_zaichi(Zaichi.JICHA)

    @property
    def kamicha(self) -> Player:
        return self.find_player_by_zaichi(Zaichi.KAMICHA)

    @property
    def toimen(self) -> Player:
        return self.find_player_by_zaichi(Zaichi.TOIMEN)

    @property
    def shimocha(self) -> Player:
        return self.find_player_by_zaichi(Zaichi.SHIMOCHA)

    #######################
    ### Utility methods ###
    #######################

    def find_player_by_zaichi(self, zaichi: Zaichi) -> Player:
        zaseki = (self.zaseki + zaichi.value) % 4
        return self.game.find_player_by_zaseki(zaseki)

    def get_zaichi_from_zaseki(self, zaseki: int) -> Zaichi:
        return Zaichi((zaseki - self.zaseki) % 4)

    def get_zaseki_from_zaichi(self, zaichi: Zaichi) -> int:
        return (self.zaseki + zaichi.value) % 4
