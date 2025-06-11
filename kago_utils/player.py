from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from kago_utils.actions import Ankan, Chii, Dahai, Daiminkan, Kakan, Pon
from kago_utils.agari_calculator import AgariCalculator
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.kawa import Kawa
from kago_utils.shanten import calculate_shanten
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
    kawa: Kawa
    last_tsumo: Hai | None
    last_dahai: Hai | None
    last_added_hai: Hai | None
    is_riichi_completed: bool
    is_right_after_riichi: bool
    is_right_after_pon: bool
    is_right_after_chii: bool
    ippatsu_flg: bool
    chankan_flg: bool
    rinshankaihou_flg: bool
    dabururiichi_flg: bool
    nagashi_mangan_flg: bool

    __slots__ = (
        "id",
        "game",
        "zaseki",
        "ten",
        "juntehai",
        "huuros",
        "kawa",
        "last_tsumo",
        "last_dahai",
        "last_added_hai",
        "is_riichi_completed",
        "is_right_after_riichi",
        "is_right_after_pon",
        "is_right_after_chii",
        "is_right_after_minkan",
        "ippatsu_flg",
        "chankan_flg",
        "rinshankaihou_flg",
        "dabururiichi_flg",
        "nagashi_mangan_flg",
    )

    def __init__(self, id: str) -> None:
        self.id = id
        self.ten = 25000
        self.reset()

    def reset(self) -> None:
        self.juntehai = HaiGroup([])
        self.huuros = []
        self.kawa = Kawa([])
        self.last_tsumo = None
        self.last_dahai = None
        self.last_added_hai = None
        self.is_riichi_completed = False
        self.is_right_after_riichi = False
        self.is_right_after_chii = False
        self.is_right_after_pon = False
        self.is_right_after_minkan = False
        self.ippatsu_flg = False
        self.chankan_flg = False
        self.rinshankaihou_flg = False
        self.dabururiichi_flg = False
        self.nagashi_mangan_flg = True

    def tsumo(self, hai: Hai) -> None:
        self.juntehai += hai
        self.last_tsumo = hai

    def rinshan_tsumo(self, hai: Hai) -> None:
        self.juntehai += hai
        self.last_tsumo = hai
        self.rinshankaihou_flg = True
        self.game.reset_chankan_flg()

    def tsumoho(self) -> None:
        agari = AgariCalculator(game=self.game, player=self, is_daburon=False)
        for i in range(4):
            self.game.players[i].ten += agari.ten_movement[i]
        self.game.kyoutaku = 0

    def ronho(self, is_daburon: bool) -> None:
        agari = AgariCalculator(game=self.game, player=self, is_daburon=is_daburon)
        for i in range(4):
            self.game.players[i].ten += agari.ten_movement[i]
        self.game.kyoutaku = 0

    def riichi(self) -> None:
        self.is_right_after_riichi = True

    def complete_riichi(self) -> None:
        self.game.kyoutaku += 1
        self.ten -= 1000
        self.is_right_after_riichi = False
        self.is_riichi_completed = True
        self.ippatsu_flg = True
        if self.game.huuro_count == 0 and len(self.kawa) == 1:
            self.dabururiichi_flg = True

    def dahai(self, dahai: Dahai) -> None:
        self.juntehai -= dahai.hai
        self.last_dahai = dahai.hai
        self.kawa.append(dahai.hai)
        self.ippatsu_flg = False
        self.rinshankaihou_flg = False
        if dahai.hai.suit != "z" and dahai.hai.number not in (1, 9):
            self.nagashi_mangan_flg = False
        self.is_right_after_chii = False
        self.is_right_after_pon = False
        if self.is_right_after_minkan:
            self.game.yama.open_dora_hyouji_hai()
            self.is_right_after_minkan = False

    def chii(self, chii: Chii) -> None:
        for candidate in self.game.non_teban_action_resolver.chii_candidates[self.id]:
            if chii.is_similar_to(candidate):
                self.huuros.append(chii)
                self.juntehai -= chii.hais - chii.stolen
                self.game.reset_ippatsu_flg()
                self.find_player_by_zaichi(chii.from_who).nagashi_mangan_flg = False
                self.is_right_after_chii = True
                return

        raise ValueError("Invalid Chii")

    def pon(self, pon: Pon) -> None:
        for candidate in self.game.non_teban_action_resolver.pon_candidates[self.id]:
            if pon.is_similar_to(candidate):
                self.huuros.append(pon)
                self.juntehai -= pon.hais - pon.stolen
                self.game.reset_ippatsu_flg()
                self.find_player_by_zaichi(pon.from_who).nagashi_mangan_flg = False
                self.is_right_after_pon = True
                return

        raise ValueError("Invalid Pon")

    def kakan(self, kakan: Kakan) -> None:
        if kakan in self.game.teban_action_resolver.kakan_candidates[self.id]:
            for i, huuro in enumerate(self.huuros):
                if isinstance(huuro, Pon) and huuro.can_become_kakan(kakan):
                    self.huuros[i] = kakan
                    self.juntehai -= kakan.added
                    self.last_added_hai = kakan.added
                    self.game.reset_ippatsu_flg()
                    self.game.set_chankan_flg()
                    if self.is_right_after_minkan:
                        self.game.yama.open_dora_hyouji_hai()
                    self.is_right_after_minkan = True
                    return

        raise ValueError("Invalid Kakan")

    def daiminkan(self, daiminkan: Daiminkan) -> None:
        if daiminkan in self.game.non_teban_action_resolver.daiminkan_candidates[self.id]:
            self.huuros.append(daiminkan)
            self.juntehai -= daiminkan.hais - daiminkan.stolen
            self.game.reset_ippatsu_flg()
            self.find_player_by_zaichi(daiminkan.from_who).nagashi_mangan_flg = False
            if self.is_right_after_minkan:
                self.game.yama.open_dora_hyouji_hai()
            self.is_right_after_minkan = True
            return

        raise ValueError("Invalid Daiminkan")

    def ankan(self, ankan: Ankan) -> None:
        if ankan in self.game.teban_action_resolver.ankan_candidates[self.id]:
            self.huuros.append(ankan)
            self.juntehai -= ankan.hais
            self.game.reset_ippatsu_flg()
            if self.is_right_after_minkan:
                self.game.yama.open_dora_hyouji_hai()
                self.is_right_after_minkan = False
            self.game.yama.open_dora_hyouji_hai()
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
    def is_tenpai(self) -> bool:
        shanten = calculate_shanten(juntehai=self.juntehai)
        return shanten == 0

    @property
    def is_teban(self) -> bool:
        return self.game.teban_player == self

    @property
    def kan_count(self) -> int:
        return sum(isinstance(huuro, (Kakan, Daiminkan, Ankan)) for huuro in self.huuros)

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
