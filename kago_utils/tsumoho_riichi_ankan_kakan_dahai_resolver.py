from __future__ import annotations

from typing import TYPE_CHECKING

from kago_utils.action import Dahai, Riichi, Tsumoho, Waiting
from kago_utils.hai_group import HaiGroup
from kago_utils.huuro import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.player import Player
from kago_utils.shanten_calculator import ShantenCalculator

if TYPE_CHECKING:
    from kago_utils.game import Game


class TsumohoRiichiAnkanKakanDahaiResolver:
    game: Game
    tsumoho_candidates: dict[str, list[Tsumoho]]
    riichi_candidates: dict[str, list[Riichi]]
    ankan_candidates: dict[str, list[Ankan]]
    kakan_candidates: dict[str, list[Kakan]]
    dahai_candidates: dict[str, list[Dahai]]
    choice: dict[str, Tsumoho | Riichi | Ankan | Kakan | Dahai | None]

    __slots__ = (
        "game",
        "tsumoho_candidates",
        "riichi_candidates",
        "ankan_candidates",
        "kakan_candidates",
        "dahai_candidates",
        "choice",
    )

    def __init__(self, game: Game) -> None:
        self.game = game

    def reset(self) -> None:
        self.tsumoho_candidates = {player.id: [] for player in self.game.players}
        self.riichi_candidates = {player.id: [] for player in self.game.players}
        self.ankan_candidates = {player.id: [] for player in self.game.players}
        self.kakan_candidates = {player.id: [] for player in self.game.players}
        self.dahai_candidates = {player.id: [] for player in self.game.players}
        self.choice = {player.id: None for player in self.game.players}

    def prepare(self) -> None:
        self.reset()

        self.tsumoho_candidates[self.game.teban_player.id] = self.list_tsumoho_candidates(self.game.teban_player)
        self.riichi_candidates[self.game.teban_player.id] = self.list_riichi_candidates(self.game.teban_player)
        self.ankan_candidates[self.game.teban_player.id] = self.list_ankan_candidates(self.game.teban_player)
        self.kakan_candidates[self.game.teban_player.id] = self.list_kakan_candidates(self.game.teban_player)
        self.dahai_candidates[self.game.teban_player.id] = self.list_dahai_candidates(self.game.teban_player)
        self.choice[self.game.teban_player.id] = None

    def register_tsumoho(self, player: Player, tsumoho: Tsumoho) -> None:
        if player != self.game.teban_player:
            return
        if self.choice[player.id] is not None:
            return
        if tsumoho in self.tsumoho_candidates[player.id]:
            self.choice[player.id] = tsumoho

    def register_riichi(self, player: Player, riichi: Riichi) -> None:
        if player != self.game.teban_player:
            return
        if self.choice[player.id] is not None:
            return
        if riichi in self.riichi_candidates[player.id]:
            self.choice[player.id] = riichi

    def register_ankan(self, player: Player, ankan: Ankan) -> None:
        if player != self.game.teban_player:
            return
        if self.choice[player.id] is not None:
            return
        if ankan in self.ankan_candidates[player.id]:
            self.choice[player.id] = ankan

    def register_kakan(self, player: Player, kakan: Kakan) -> None:
        if player != self.game.teban_player:
            return
        if self.choice[player.id] is not None:
            return
        if kakan in self.kakan_candidates[player.id]:
            self.choice[player.id] = kakan

    def register_dahai(self, player: Player, dahai: Dahai) -> None:
        if player != self.game.teban_player:
            return
        if self.choice[player.id] is not None:
            return
        if dahai in self.dahai_candidates[player.id]:
            self.choice[player.id] = dahai

    def resolve(self) -> Tsumoho | Riichi | Ankan | Kakan | Dahai | Waiting:
        choice = self.choice[self.game.teban_player.id]
        if choice is not None:
            return choice

        return Waiting()

    def list_tsumoho_candidates(self, player: Player) -> list[Tsumoho]:
        return [Tsumoho()]

    def list_riichi_candidates(self, player: Player) -> list[Riichi]:
        # Not menzen
        if not player.is_menzen:
            return []

        # Riichi completed
        if player.is_riichi_completed:
            return []

        # Right after calling riichi
        if player.is_right_after_riichi_called:
            return []

        # Not enough ten
        if player.ten < 1000:
            return []

        # Not enough yama
        if self.game.yama.rest_tsumo_count < 4:
            return []

        # Not tenpai
        if ShantenCalculator(player.juntehai).shanten > 0:
            return []

        return [Riichi()]

    def list_ankan_candidates(self, player: Player) -> list[Ankan]:
        # Right after calling riichi
        if player.is_right_after_riichi_called:
            return []

        # Not enough yama
        if self.game.yama.rest_tsumo_count == 0:
            return []

        # Four kans exist
        # TODO: Move n_kan to `Game` class
        n_kan = 0
        for p in self.game.players:
            for huuro in p.huuros:
                if isinstance(huuro, (Kakan, Daiminkan, Ankan)):
                    n_kan += 1
        if n_kan >= 4:
            return []

        candidates = []
        counter = player.juntehai.to_counter34()

        # When riichi completed, only ankan that does not change shanten and machihais is allowed
        if player.is_riichi_completed:
            if player.last_tsumo is not None and counter[player.last_tsumo.id // 4] >= 4:
                base_id = player.last_tsumo.id // 4 * 4
                ankan = Ankan(hais=HaiGroup.from_list([base_id, base_id + 1, base_id + 2, base_id + 3]))

                shanten1 = ShantenCalculator(player.juntehai - player.last_tsumo)
                shanten2 = ShantenCalculator(player.juntehai - ankan.hais)
                if shanten1.shanten == shanten2.shanten and shanten1.yuukouhai == shanten2.yuukouhai:
                    candidates.append(ankan)

        # Otherwise, all ankans are allowed
        else:
            for i in range(34):
                if counter[i] >= 4:
                    base_id = i * 4
                    ankan = Ankan(hais=HaiGroup.from_list([base_id, base_id + 1, base_id + 2, base_id + 3]))
                    candidates.append(ankan)

        return candidates

    def list_kakan_candidates(self, player: Player) -> list[Kakan]:
        # Not enough yama
        if self.game.yama.rest_tsumo_count == 0:
            return []

        # Four kans exist
        # TODO: Move n_kan to `Game` class
        n_kan = 0
        for p in self.game.players:
            for huuro in p.huuros:
                if isinstance(huuro, (Kakan, Daiminkan, Ankan)):
                    n_kan += 1
        if n_kan >= 4:
            return []

        candidates = []
        for huuro in player.huuros:
            if isinstance(huuro, Pon) and huuro.to_kakan().added in player.juntehai:
                candidates.append(huuro.to_kakan())

        return candidates

    def list_dahai_candidates(self, player: Player) -> list[Dahai]:
        # Riichi completed
        if player.is_riichi_completed:
            if player.last_tsumo is None:
                raise Exception()

            return [Dahai(player.last_tsumo)]

        # Right after calling riichi
        elif player.is_right_after_riichi_called:
            candidates = []
            for hai in player.juntehai:
                new_juntehai = player.juntehai - hai
                if ShantenCalculator(new_juntehai).shanten == 0:
                    candidates.append(Dahai(hai))
            return candidates

        # Right after calling chii or pon
        elif player.is_right_after_chii_called or player.is_right_after_pon_called:
            last_huuro = player.huuros[-1]
            if not isinstance(last_huuro, (Chii, Pon)):
                raise Exception()

            candidates = []
            for hai in player.juntehai:
                if hai not in last_huuro.kuikae_hais:
                    candidates.append(Dahai(hai))
            return candidates

        else:
            return [Dahai(hai) for hai in player.juntehai]
