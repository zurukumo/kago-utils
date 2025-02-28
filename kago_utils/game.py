from __future__ import annotations

from typing import Literal

from kago_utils.actions import Ankan, Daiminkan, Kakan
from kago_utils.bot import Bot
from kago_utils.hai import Hai
from kago_utils.player import Player
from kago_utils.resolvers import NonTebanActionResolver, TebanActionResolver
from kago_utils.resolvers.results import (
    AnkanResult,
    ChiiResult,
    DahaiResult,
    DaiminkanResult,
    Pending,
    PonResult,
    RiichiResult,
    RonhoResult,
    TsumohoResult,
)
from kago_utils.yama import Yama


class Game:
    players: list[Player]
    yama: Yama
    teban_action_resolver: TebanActionResolver
    non_teban_action_resolver: NonTebanActionResolver

    state: Literal[
        "init_hanchan", "init_kyoku", "tsumo", "wait_teban_action", "rinshan_tsumo", "wait_non_teban_action", "agari"
    ]

    kyoku: int
    honba: int
    kyoutaku: int

    teban: int
    last_teban: int | None
    last_dahai: Hai | None

    __slots__ = (
        "players",
        "yama",
        "teban_action_resolver",
        "non_teban_action_resolver",
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
        self.teban_action_resolver = TebanActionResolver(self)
        self.non_teban_action_resolver = NonTebanActionResolver(self)

        self.state = "init_hanchan"

    def step(self) -> None:
        match self.state:
            case "init_hanchan":
                self.init_hanchan()
            case "init_kyoku":
                self.init_kyoku()
            case "tsumo":
                self.tsumo()
            case "wait_teban_action":
                self.wait_teban_action()
            case "rinshan_tsumo":
                self.rinshan_tsumo()
            case "wait_non_teban_action":
                self.wait_non_teban_action()
            case "agari":
                self.agari()

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

        # Prepare teban action candidates
        self.teban_action_resolver.prepare()
        if isinstance(self.teban_player, Bot):
            self.teban_player.select_teban_action()

        self.state = "wait_teban_action"

    def wait_teban_action(self) -> None:
        result = self.teban_action_resolver.resolve()
        if isinstance(result, Pending):
            return

        match result:
            case TsumohoResult():
                result.player.tsumoho()
                self.state = "agari"
            case RiichiResult():
                result.player.riichi()
                self.state = "wait_teban_action"
            case AnkanResult():
                result.player.ankan(result.action)
                self.state = "rinshan_tsumo"
            case DahaiResult():
                result.player.dahai(result.action)

                # Prepare non teban action candidates
                self.non_teban_action_resolver.prepare()
                if isinstance(self.teban_player, Bot):
                    self.teban_player.select_non_teban_action()

                self.state = "wait_non_teban_action"

    def rinshan_tsumo(self) -> None:
        # Rinshan tsumo
        tsumo_hai = self.yama.rinshan_tsumo()
        self.teban_player.tsumo(tsumo_hai)

        # Prepare tsumoho, riichi, ankan and dahai candidates
        self.teban_action_resolver.prepare()

        if isinstance(self.teban_player, Bot):
            self.teban_player.select_teban_action()

        self.state = "wait_teban_action"

    def wait_non_teban_action(self) -> None:
        result = self.non_teban_action_resolver.resolve()
        if isinstance(result, Pending):
            return

        match result:
            case RonhoResult():
                for player, _ in result.actions:
                    player.ronho()
                self.state = "agari"
            case DaiminkanResult():
                result.player.daiminkan(result.action)
                self.teban = result.player.zaseki
                self.state = "rinshan_tsumo"
            case PonResult():
                result.player.pon(result.action)
                self.teban = result.player.zaseki
                self.state = "wait_teban_action"
            case ChiiResult():
                result.player.chii(result.action)
                self.teban = result.player.zaseki
                self.state = "wait_teban_action"

    def agari(self) -> None:
        pass

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
    def kan_count(self) -> int:
        count = 0
        for player in self.players:
            for huuro in player.huuros:
                if isinstance(huuro, (Ankan, Daiminkan, Kakan)):
                    count += 1
        return count
