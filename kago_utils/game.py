from __future__ import annotations

from typing import Literal

from kago_utils.bot import Bot
from kago_utils.hai import Hai
from kago_utils.player import Player
from kago_utils.resolvers import (
    ChankanActionResolver,
    NonTebanActionResolver,
    TebanActionResolver,
)
from kago_utils.resolvers.results import (
    AnkanResult,
    ChiiResult,
    DahaiResult,
    DaiminkanResult,
    KakanResult,
    KyuushuKyuuhaiResult,
    Pending,
    PonResult,
    RiichiResult,
    RonhoResult,
    SkipResult,
    TsumohoResult,
)
from kago_utils.yama import Yama

State = Literal[
    "none",
    "init_hanchan",
    "init_kyoku",
    "tsumo",
    "register_teban_action",
    "wait_teban_action",
    "tsumoho",
    "riichi",
    "ankan",
    "kakan",
    "dahai",
    "rinshan_tsumo",
    "register_non_teban_action",
    "wait_non_teban_action",
    "register_chankan_action",
    "wait_chankan_action",
    "ronho",
    "daiminkan",
    "pon",
    "chii",
    "skip",
    "agari",
    "ryuukyoku",
    "nagashi_mangan",
    "kyuushu_kyuuhai",
    "yoncha_riichi",
    "suuhuu_renda",
    "suukan_sanryou",
    "sancha_houra",
    "syuukyoku",
]


class Game:
    players: list[Player]
    yama: Yama
    teban_action_resolver: TebanActionResolver
    non_teban_action_resolver: NonTebanActionResolver

    state: State
    prev_state: State

    kyoku: int
    honba: int
    kyoutaku: int

    teban: int
    is_renchan: bool

    __slots__ = (
        "players",
        "yama",
        "teban_action_resolver",
        "non_teban_action_resolver",
        "chankan_action_resolver",
        "state",
        "prev_state",
        "kyoku",
        "honba",
        "kyoutaku",
        "teban",
        "is_renchan",
    )

    def __init__(self) -> None:
        self.players = []
        self.yama = Yama()
        self.teban_action_resolver = TebanActionResolver(self)
        self.non_teban_action_resolver = NonTebanActionResolver(self)
        self.chankan_action_resolver = ChankanActionResolver(self)

        self.state = "init_hanchan"
        self.prev_state = "none"
        self.kyoku, self.honba, self.kyoutaku = 0, 0, 0
        self.teban = 0
        self.is_renchan = False

    def step(self) -> None:
        method = getattr(self, self.state, None)
        if callable(method):
            method()
        else:
            raise ValueError(f"Unknown state: {self.state}")

    def init_hanchan(self) -> None:
        self.kyoku = 0
        self.honba = 0
        self.kyoutaku = 0

        self.update_state("init_kyoku")

    def init_kyoku(self) -> None:
        self.teban = self.kyoku % 4
        self.is_renchan = False

        for player in self.players:
            player.reset()

        # Haipai
        self.yama.generate()
        for _ in range(3):
            for player in self.get_players_from_oya():
                for _ in range(4):
                    tsumo_hai = self.yama.tsumo()
                    player.tsumo(tsumo_hai)
        for player in self.get_players_from_oya():
            tsumo_hai = self.yama.tsumo()
            player.tsumo(tsumo_hai)

        self.update_state("tsumo")

    def tsumo(self) -> None:
        # Tsumo
        tsumo_hai = self.yama.tsumo()
        self.teban_player.tsumo(tsumo_hai)

        self.update_state("register_teban_action")

    def register_teban_action(self) -> None:
        # Prepare teban action candidates
        self.teban_action_resolver.prepare()
        if isinstance(self.teban_player, Bot):
            self.teban_player.select_teban_action()

        self.update_state("wait_teban_action")

    def wait_teban_action(self) -> None:
        result = self.teban_action_resolver.resolve()
        if isinstance(result, Pending):
            return

        match result:
            case TsumohoResult():
                self.update_state("tsumoho")
            case RiichiResult():
                self.update_state("riichi")
            case AnkanResult():
                self.update_state("ankan")
            case KakanResult():
                self.update_state("kakan")
            case DahaiResult():
                self.update_state("dahai")
            case KyuushuKyuuhaiResult():
                self.update_state("kyuushu_kyuuhai")

    def tsumoho(self) -> None:
        result = self.teban_action_resolver.resolve()
        assert isinstance(result, TsumohoResult)

        result.player.tsumoho()
        if result.player.is_oya:
            self.is_renchan = True
        self.update_state("agari")

    def riichi(self) -> None:
        result = self.teban_action_resolver.resolve()
        assert isinstance(result, RiichiResult)

        result.player.riichi()
        self.update_state("register_teban_action")

    def ankan(self) -> None:
        result = self.teban_action_resolver.resolve()
        assert isinstance(result, AnkanResult)

        result.player.ankan(result.action)
        self.update_state("rinshan_tsumo")

    def kakan(self) -> None:
        result = self.teban_action_resolver.resolve()
        assert isinstance(result, KakanResult)

        result.player.kakan(result.action)
        self.update_state("register_chankan_action")

    def dahai(self) -> None:
        result = self.teban_action_resolver.resolve()
        assert isinstance(result, DahaiResult)

        result.player.dahai(result.action)
        self.update_state("register_non_teban_action")

    def rinshan_tsumo(self) -> None:
        tsumo_hai = self.yama.rinshan_tsumo()
        self.teban_player.rinshan_tsumo(tsumo_hai)

        self.update_state("register_teban_action")

    def register_non_teban_action(self) -> None:
        self.non_teban_action_resolver.prepare()
        for player in self.get_players_from_teban():
            if player == self.teban_player:
                continue
            if isinstance(player, Bot):
                player.select_non_teban_action()

        self.update_state("wait_non_teban_action")

    def wait_non_teban_action(self) -> None:
        result = self.non_teban_action_resolver.resolve()
        if isinstance(result, Pending):
            return

        if isinstance(result, RonhoResult):
            self.update_state("ronho")
            return

        # When not ronho, riichi is completed
        for player in self.players:
            if player.is_right_after_riichi:
                player.complete_riichi()
                # Yoncha Riichi
                if all(player.is_riichi_completed for player in self.players):
                    self.update_state("yoncha_riichi")
                    return

        # When not ronho and after kakan or daiminkan, open dora
        for player in self.players:
            if player.is_right_after_minkan:
                self.yama.open_dora_hyouji_hai()
                player.is_right_after_minkan = False

        # Suuhuu Renda
        first_dahais = [player.kawa[0] for player in self.players if len(player.kawa) > 0]
        if (
            self.huuro_count == 0
            and len(first_dahais) == 4
            and len(set(hai.code for hai in first_dahais)) == 1
            and first_dahais[0].code in ["1z", "2z", "3z", "4z"]
        ):
            self.update_state("suuhuu_renda")
            return

        # Suukan Sanryou
        if self.kan_count == 4 and all(player.kan_count < 4 for player in self.players):
            self.update_state("suukan_sanryou")
            return

        match result:
            case DaiminkanResult():
                self.update_state("daiminkan")
            case PonResult():
                self.update_state("pon")
            case ChiiResult():
                self.update_state("chii")
            case SkipResult():
                if self.yama.rest_tsumo_count == 0:
                    if any(player.nagashi_mangan_flg for player in self.players):
                        self.update_state("nagashi_mangan")
                    else:
                        self.update_state("ryuukyoku")
                else:
                    self.teban = (self.teban + 1) % 4
                    self.update_state("tsumo")

    def register_chankan_action(self) -> None:
        self.chankan_action_resolver.prepare()
        for player in self.get_players_from_teban():
            if player == self.teban_player:
                continue
            if isinstance(player, Bot):
                player.select_chankan_action()

        self.update_state("wait_chankan_action")

    def wait_chankan_action(self) -> None:
        result = self.chankan_action_resolver.resolve()
        if isinstance(result, Pending):
            return

        if isinstance(result, RonhoResult):
            self.update_state("ronho")
            return

        if isinstance(result, SkipResult):
            self.update_state("rinshan_tsumo")
            return

    def ronho(self) -> None:
        if self.prev_state == "wait_non_teban_action":
            result = self.non_teban_action_resolver.resolve()
        else:
            result = self.chankan_action_resolver.resolve()

        assert isinstance(result, RonhoResult)

        # Sancha Houra
        if len(result.actions) == 3:
            self.update_state("sancha_houra")
            return

        for i, (player, _) in enumerate(result.actions):
            player.ronho(is_daburon=(i > 0))
            if player.is_oya:
                self.is_renchan = True

        self.update_state("agari")

    def daiminkan(self) -> None:
        result = self.non_teban_action_resolver.resolve()
        assert isinstance(result, DaiminkanResult)

        result.player.daiminkan(result.action)
        self.teban = result.player.zaseki
        self.update_state("rinshan_tsumo")

    def pon(self) -> None:
        result = self.non_teban_action_resolver.resolve()
        assert isinstance(result, PonResult)

        result.player.pon(result.action)
        self.teban = result.player.zaseki
        self.update_state("register_teban_action")

    def chii(self) -> None:
        result = self.non_teban_action_resolver.resolve()
        assert isinstance(result, ChiiResult)

        result.player.chii(result.action)
        self.teban = result.player.zaseki
        self.update_state("register_teban_action")

    def agari(self) -> None:
        if self.is_renchan:
            self.honba += 1
        else:
            self.kyoku += 1
            self.honba = 0

        if self.is_syuukyoku:
            self.update_state("syuukyoku")
        else:
            self.update_state("init_kyoku")

    def ryuukyoku(self) -> None:
        tenpai_count = sum(player.is_tenpai for player in self.players)
        if tenpai_count == 3:
            for player in self.players:
                if player.is_tenpai:
                    player.ten += 1000
                else:
                    player.ten -= 3000
        elif tenpai_count == 2:
            for player in self.players:
                if player.is_tenpai:
                    player.ten += 1500
                else:
                    player.ten -= 1500
        elif tenpai_count == 1:
            for player in self.players:
                if player.is_tenpai:
                    player.ten += 3000
                else:
                    player.ten -= 1000

        if self.oya.is_tenpai:
            self.is_renchan = True

        self.honba += 1
        if not self.is_renchan:
            self.kyoku += 1

        if self.is_syuukyoku:
            self.update_state("syuukyoku")
        else:
            self.update_state("init_kyoku")

    def nagashi_mangan(self) -> None:
        for player in self.players:
            if player.nagashi_mangan_flg and not player.is_oya:
                player.ten += 8000
                for other in self.players:
                    if other == player:
                        continue
                    if other.is_oya:
                        other.ten -= 4000
                    else:
                        other.ten -= 2000
            elif player.nagashi_mangan_flg and player.is_oya:
                player.ten += 12000
                for other in self.players:
                    if other == player:
                        continue
                    other.ten -= 4000

        if self.oya.is_tenpai:
            self.is_renchan = True

        self.honba += 1
        if not self.is_renchan:
            self.kyoku += 1

        if self.is_syuukyoku:
            self.update_state("syuukyoku")
        else:
            self.update_state("init_kyoku")

    def kyuushu_kyuuhai(self) -> None:
        self.honba += 1

        if self.is_syuukyoku:
            self.update_state("syuukyoku")
        else:
            self.update_state("init_kyoku")

    def yoncha_riichi(self) -> None:
        self.honba += 1

        if self.is_syuukyoku:
            self.update_state("syuukyoku")
        else:
            self.update_state("init_kyoku")

    def suuhuu_renda(self) -> None:
        self.honba += 1

        if self.is_syuukyoku:
            self.update_state("syuukyoku")
        else:
            self.update_state("init_kyoku")

    def suukan_sanryou(self) -> None:
        self.honba += 1

        if self.is_syuukyoku:
            self.update_state("syuukyoku")
        else:
            self.update_state("init_kyoku")

    def sancha_houra(self) -> None:
        self.honba += 1

        if self.is_syuukyoku:
            self.update_state("syuukyoku")
        else:
            self.update_state("init_kyoku")

    def syuukyoku(self) -> None:
        if self.kyoutaku > 0:
            self.top_player.ten += self.kyoutaku * 1000
            self.kyoutaku = 0

        return

    #######################
    ### Utility methods ###
    #######################

    def add_player(self, player: Player) -> None:
        player.game = self
        player.zaseki = len(self.players)
        self.players.append(player)

    def find_player_by_zaseki(self, zaseki: int) -> Player:
        return self.players[zaseki]

    def get_players_from_teban(self) -> list[Player]:
        return [self.players[(self.teban + i) % 4] for i in range(4)]

    def get_players_from_oya(self) -> list[Player]:
        return [self.players[(self.kyoku + i) % 4] for i in range(4)]

    def update_state(self, new_state: State) -> None:
        self.prev_state = self.state
        self.state = new_state

    def reset_ippatsu_flg(self) -> None:
        for player in self.players:
            player.ippatsu_flg = False

    def set_chankan_flg(self) -> None:
        for player in self.players:
            if not player.is_teban:
                player.chankan_flg = True

    def reset_chankan_flg(self) -> None:
        for player in self.players:
            if not player.is_teban:
                player.chankan_flg = False

    @property
    def bakaze(self) -> Literal["東", "南", "西", "北"]:
        match self.kyoku // 4:
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
    def teban_player(self) -> Player:
        return self.players[self.teban]

    @property
    def top_player(self) -> Player:
        return max(self.players, key=lambda player: player.ten)

    @property
    def oya(self) -> Player:
        return self.players[self.kyoku % 4]

    @property
    def kan_count(self) -> int:
        return sum(player.kan_count for player in self.players)

    @property
    def huuro_count(self) -> int:
        return sum(len(player.huuros) for player in self.players)

    @property
    def last_dahai(self) -> Hai | None:
        return self.teban_player.last_dahai

    @property
    def last_added_hai(self) -> Hai | None:
        return self.teban_player.last_added_hai

    @property
    def is_syuukyoku(self) -> bool:
        # Normal
        if self.kyoku >= 8 and any(player.ten >= 30000 for player in self.players) and not self.is_renchan:
            return True
        # Agariyame
        elif (
            self.kyoku >= 7
            and self.oya.ten > max(player.ten for player in self.players if not player.is_oya)
            and self.oya.ten >= 30000
            and self.is_renchan
        ):
            return True
        # Tobi
        elif any(player.ten < 0 for player in self.players):
            return True
        # Peenyuu
        elif self.kyoku >= 12:
            return True

        return False
