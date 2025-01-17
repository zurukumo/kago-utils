from __future__ import annotations

from typing import Literal

from kago_utils.action import Dahai, Riichi, Tsumoho, Waiting
from kago_utils.bot import Bot
from kago_utils.hai import Hai
from kago_utils.huuro import Ankan
from kago_utils.player import Player
from kago_utils.tsumoho_riichi_ankan_kakan_dahai_resolver import TsumohoRiichiAnkanKakanDahaiResolver
from kago_utils.yama import Yama


class Game:
    players: list[Player]
    yama: Yama
    tsumoho_riichi_ankan_kakan_dahai_resolver: TsumohoRiichiAnkanKakanDahaiResolver

    state: Literal["init_hanchan", "init_kyoku", "tsumo", "wait_tsumoho_riichi_ankan_dahai", "rinshan_tsumo", "agari"]

    kyoku: int
    honba: int
    kyoutaku: int

    teban: int
    last_teban: int | None
    last_dahai: Hai | None

    __slots__ = (
        "players",
        "yama",
        "tsumoho_riichi_ankan_kakan_dahai_resolver",
        "state",
        "kyoku",
        "honba",
        "kyoutaku",
        "teban",
        "last_teban",
        "last_dahai",
    )

    def __init__(self) -> None:
        self.players = []
        self.yama = Yama()
        self.tsumoho_riichi_ankan_kakan_dahai_resolver = TsumohoRiichiAnkanKakanDahaiResolver(self)

        self.state = "init_hanchan"

    def step(self) -> None:
        match self.state:
            case "init_hanchan":
                self.init_hanchan()
            case "init_kyoku":
                self.init_kyoku()
            case "tsumo":
                self.tsumo()
            case "wait_tsumoho_riichi_ankan_dahai":
                self.wait_tsumoho_riichi_ankan_dahai()
            case "rinshan_tsumo":
                self.rinshan_tsumo()

    def init_hanchan(self) -> None:
        self.kyoku = 0
        self.honba = 0
        self.kyoutaku = 0

        self.state = "init_kyoku"

    def init_kyoku(self) -> None:
        self.teban = self.kyoku % 4
        self.last_teban = None
        self.last_dahai = None

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

        self.state = "tsumo"

    def tsumo(self) -> None:
        # Tsumo
        tsumo_hai = self.yama.tsumo()
        self.teban_player.tsumo(tsumo_hai)

        # Prepare tsumoho, riichi, ankan and dahai candidates
        self.tsumoho_riichi_ankan_kakan_dahai_resolver.prepare()

        if isinstance(self.teban_player, Bot):
            self.teban_player.select_tsumoho_riichi_ankan_dahai()

        self.state = "wait_tsumoho_riichi_ankan_dahai"

    def wait_tsumoho_riichi_ankan_dahai(self) -> None:
        action = self.tsumoho_riichi_ankan_kakan_dahai_resolver.resolve()
        match action:
            case Tsumoho():
                self.teban_player.tsumoho()
                self.state = "agari"
            case Riichi():
                self.teban_player.riichi()
                self.state = "wait_tsumoho_riichi_ankan_dahai"
            case Ankan():
                self.teban_player.ankan(action)
                self.state = "rinshan_tsumo"
            case Dahai():
                self.teban_player.dahai(action)
                self.teban, self.last_teban = (self.teban + 1) % 4, self.teban
                self.state = "tsumo"
            case Waiting():
                pass

    def rinshan_tsumo(self) -> None:
        # Rinshan tsumo
        tsumo_hai = self.yama.rinshan_tsumo()
        self.teban_player.tsumo(tsumo_hai)

        # Prepare tsumoho, riichi, ankan and dahai candidates
        self.tsumoho_riichi_ankan_kakan_dahai_resolver.prepare()

        if isinstance(self.teban_player, Bot):
            self.teban_player.select_tsumoho_riichi_ankan_dahai()

        self.state = "wait_tsumoho_riichi_ankan_dahai"

    #######################
    ### Utility methods ###
    #######################

    def add_player(self, player: Player) -> None:
        player.game = self
        player.zaseki = len(self.players)
        self.players.append(player)

    def find_player_by_zaseki(self, zaseki: int) -> Player:
        return self.players[zaseki]

    def get_players_from_oya(self) -> list[Player]:
        return [self.players[(self.teban + i) % 4] for i in range(4)]

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
