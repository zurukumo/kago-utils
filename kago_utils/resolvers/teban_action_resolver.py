from __future__ import annotations

from typing import TYPE_CHECKING

from kago_utils.actions import Ankan, Chii, Dahai, Kakan, KyuushuKyuuhai, Pon, Riichi, Tsumoho
from kago_utils.agari_calculator import AgariCalculator
from kago_utils.hai_group import HaiGroup
from kago_utils.player import Player
from kago_utils.shanten import calculate_shanten, calculate_yuukouhai

from .results import AnkanResult, DahaiResult, KakanResult, KyuushuKyuuhaiResult, Pending, RiichiResult, TsumohoResult

if TYPE_CHECKING:
    from kago_utils.game import Game


class TebanActionResolver:
    game: Game
    tsumoho_candidates: dict[str, list[Tsumoho]]
    riichi_candidates: dict[str, list[Riichi]]
    ankan_candidates: dict[str, list[Ankan]]
    kakan_candidates: dict[str, list[Kakan]]
    dahai_candidates: dict[str, list[Dahai]]
    kyuushu_kyuuhai_candidates: dict[str, list[KyuushuKyuuhai]]
    choice: dict[str, Tsumoho | Riichi | Ankan | Kakan | Dahai | KyuushuKyuuhai | None]

    __slots__ = (
        "game",
        "tsumoho_candidates",
        "riichi_candidates",
        "ankan_candidates",
        "kakan_candidates",
        "dahai_candidates",
        "kyuushu_kyuuhai_candidates",
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
        self.kyuushu_kyuuhai_candidates = {player.id: [] for player in self.game.players}
        self.choice = {player.id: None for player in self.game.players}

    def prepare(self) -> None:
        self.reset()

        self.tsumoho_candidates[self.game.teban_player.id] = self.list_tsumoho_candidates(self.game.teban_player)
        self.riichi_candidates[self.game.teban_player.id] = self.list_riichi_candidates(self.game.teban_player)
        self.ankan_candidates[self.game.teban_player.id] = self.list_ankan_candidates(self.game.teban_player)
        self.kakan_candidates[self.game.teban_player.id] = self.list_kakan_candidates(self.game.teban_player)
        self.dahai_candidates[self.game.teban_player.id] = self.list_dahai_candidates(self.game.teban_player)
        self.kyuushu_kyuuhai_candidates[self.game.teban_player.id] = self.list_kyuushu_kyuuhai_candidates(
            self.game.teban_player
        )
        self.choice[self.game.teban_player.id] = None

    def register_tsumoho(self, player: Player, tsumoho: Tsumoho) -> None:
        if self.choice[player.id] is not None:
            return
        if tsumoho in self.tsumoho_candidates[player.id]:
            self.choice[player.id] = tsumoho

    def register_riichi(self, player: Player, riichi: Riichi) -> None:
        if self.choice[player.id] is not None:
            return
        if riichi in self.riichi_candidates[player.id]:
            self.choice[player.id] = riichi

    def register_ankan(self, player: Player, ankan: Ankan) -> None:
        if self.choice[player.id] is not None:
            return
        if ankan in self.ankan_candidates[player.id]:
            self.choice[player.id] = ankan

    def register_kakan(self, player: Player, kakan: Kakan) -> None:
        if self.choice[player.id] is not None:
            return
        if kakan in self.kakan_candidates[player.id]:
            self.choice[player.id] = kakan

    def register_dahai(self, player: Player, dahai: Dahai) -> None:
        if self.choice[player.id] is not None:
            return
        if dahai in self.dahai_candidates[player.id]:
            self.choice[player.id] = dahai

    def register_kyuushu_kyuuhai(self, player: Player, kyuushu_kyuuhai: KyuushuKyuuhai) -> None:
        if self.choice[player.id] is not None:
            return
        if kyuushu_kyuuhai in self.kyuushu_kyuuhai_candidates[player.id]:
            self.choice[player.id] = kyuushu_kyuuhai

    def resolve(
        self,
    ) -> TsumohoResult | RiichiResult | AnkanResult | KakanResult | DahaiResult | KyuushuKyuuhaiResult | Pending:
        c = self.choice[self.game.teban_player.id]
        match c:
            case Tsumoho():
                return TsumohoResult(self.game.teban_player, c)
            case Riichi():
                return RiichiResult(self.game.teban_player, c)
            case Ankan():
                return AnkanResult(self.game.teban_player, c)
            case Kakan():
                return KakanResult(self.game.teban_player, c)
            case Dahai():
                return DahaiResult(self.game.teban_player, c)
            case KyuushuKyuuhai():
                return KyuushuKyuuhaiResult(self.game.teban_player, c)

        return Pending()

    def list_tsumoho_candidates(self, player: Player) -> list[Tsumoho]:
        # Not agari
        if calculate_shanten(player.juntehai) != -1:
            return []

        # Not yakuari
        if not AgariCalculator(self.game, player).ten > 0:
            return []

        return [Tsumoho()]

    def list_riichi_candidates(self, player: Player) -> list[Riichi]:
        # Not menzen
        if not player.is_menzen:
            return []

        # Riichi completed
        if player.is_riichi_completed:
            return []

        # Right after calling riichi
        if player.is_right_after_riichi:
            return []

        # Not enough ten
        if player.ten < 1000:
            return []

        # Not enough yama
        if self.game.yama.rest_tsumo_count < 4:
            return []

        # Not tenpai
        if calculate_shanten(player.juntehai) > 0:
            return []

        return [Riichi()]

    def list_ankan_candidates(self, player: Player) -> list[Ankan]:
        assert player.last_tsumo is not None

        # Right after calling riichi
        if player.is_right_after_riichi:
            return []

        # Not enough yama
        if self.game.yama.rest_tsumo_count == 0:
            return []

        # Four kans exist
        if self.game.kan_count >= 4:
            return []

        candidates = []
        counter = player.juntehai.to_counter34()

        # When riichi completed, only ankan that does not change shanten and machi is allowed
        if player.is_riichi_completed:
            if counter[player.last_tsumo.id // 4] >= 4:
                base_id = player.last_tsumo.id // 4 * 4
                ankan = Ankan(hais=HaiGroup.from_list([base_id, base_id + 1, base_id + 2, base_id + 3]))

                shanten1 = calculate_shanten(player.juntehai - player.last_tsumo)
                shanten2 = calculate_shanten(player.juntehai - ankan.hais)
                yuukouhai1 = calculate_yuukouhai(player.juntehai - ankan.hais)
                yuukouhai2 = calculate_yuukouhai(player.juntehai - player.last_tsumo)
                if shanten1 == shanten2 and yuukouhai1 == yuukouhai2:
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
        if self.game.kan_count >= 4:
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
        elif player.is_right_after_riichi:
            candidates = []
            for hai in player.juntehai:
                new_juntehai = player.juntehai - hai
                if calculate_shanten(new_juntehai) == 0:
                    candidates.append(Dahai(hai))
            return candidates

        # Right after calling chii or pon
        elif player.is_right_after_chii or player.is_right_after_pon:
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

    def list_kyuushu_kyuuhai_candidates(self, player: Player) -> list[KyuushuKyuuhai]:
        # Huuro exists
        if self.game.huuro_count != 0:
            return []

        # Not first teban
        if len(player.kawa) != 0:
            return []

        # Not KyuushuKyuuhai
        if sum(hai.suit == "z" or hai.number in [1, 9] for hai in player.juntehai) < 9:
            return []

        return [KyuushuKyuuhai()]
