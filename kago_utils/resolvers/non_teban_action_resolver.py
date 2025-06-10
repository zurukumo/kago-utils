from __future__ import annotations

import random
from itertools import product
from typing import TYPE_CHECKING

from kago_utils.actions import Chii, Daiminkan, Pon, Ronho, Skip
from kago_utils.agari_calculator import AgariCalculator
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.player import Player
from kago_utils.shanten_calculator import ShantenCalculator

from .results import ChiiResult, DaiminkanResult, Pending, PonResult, RonhoResult, SkipResult

if TYPE_CHECKING:
    from kago_utils.game import Game


class NonTebanActionResolver:
    game: Game
    ronho_candidates: dict[str, list[Ronho]]
    daiminkan_candidates: dict[str, list[Daiminkan]]
    pon_candidates: dict[str, list[Pon]]
    chii_candidates: dict[str, list[Chii]]
    skip_candidates: dict[str, list[Skip]]
    choice: dict[str, Ronho | Daiminkan | Pon | Chii | Skip | None]

    __slots__ = (
        "game",
        "ronho_candidates",
        "daiminkan_candidates",
        "pon_candidates",
        "chii_candidates",
        "skip_candidates",
        "choice",
    )

    def __init__(self, game: Game) -> None:
        self.game = game

    def reset(self) -> None:
        self.ronho_candidates = {player.id: [] for player in self.game.players}
        self.daiminkan_candidates = {player.id: [] for player in self.game.players}
        self.pon_candidates = {player.id: [] for player in self.game.players}
        self.chii_candidates = {player.id: [] for player in self.game.players}
        self.skip_candidates = {player.id: [] for player in self.game.players}
        self.choice = {player.id: None for player in self.game.players}

    def prepare(self) -> None:
        self.reset()

        for player in self.game.players:
            if player == self.game.teban_player:
                continue

            if player == self.game.teban_player.shimocha:
                self.chii_candidates[player.id] = self.list_chii_candidates(player)

            self.ronho_candidates[player.id] = self.list_ronho_candidates(player)
            self.daiminkan_candidates[player.id] = self.list_daiminkan_candidates(player)
            self.pon_candidates[player.id] = self.list_pon_candidates(player)
            self.skip_candidates[player.id] = self.list_skip_candidates()
            self.choice[player.id] = None

    def register_ronho(self, player: Player, ronho: Ronho) -> None:
        if self.choice[player.id] is not None:
            return
        if ronho in self.ronho_candidates[player.id]:
            self.choice[player.id] = ronho

    def register_daiminkan(self, player: Player, daiminkan: Daiminkan) -> None:
        if self.choice[player.id] is not None:
            return
        if daiminkan in self.daiminkan_candidates[player.id]:
            self.choice[player.id] = daiminkan

    def register_pon(self, player: Player, pon: Pon) -> None:
        if self.choice[player.id] is not None:
            return
        for candidate in self.pon_candidates[player.id]:
            if pon.is_similar_to(candidate):
                self.choice[player.id] = pon
                return

    def register_chii(self, player: Player, chii: Chii) -> None:
        if self.choice[player.id] is not None:
            return
        for candidate in self.chii_candidates[player.id]:
            if chii.is_similar_to(candidate):
                self.choice[player.id] = chii
                return

    def register_skip(self, player: Player, skip: Skip) -> None:
        if self.choice[player.id] is not None:
            return
        if skip in self.skip_candidates[player.id]:
            self.choice[player.id] = skip

    def resolve(self) -> RonhoResult | DaiminkanResult | PonResult | ChiiResult | SkipResult | Pending:
        ronho_choice_count = 0
        daiminkan_choice_count = 0
        pon_choice_count = 0
        chii_choice_count = 0
        skip_choice_count = 0
        rest_ronho_candidate_count = 0
        rest_daiminkan_candidate_count = 0
        rest_pon_candidate_count = 0
        rest_chii_candidate_count = 0
        rest_skip_candidate_count = 0

        for player in self.game.get_players_from_teban():
            c = self.choice[player.id]
            if c is not None:
                match c:
                    case Ronho():
                        ronho_choice_count += 1
                    case Daiminkan():
                        daiminkan_choice_count += 1
                    case Pon():
                        pon_choice_count += 1
                    case Chii():
                        chii_choice_count += 1
                    case Skip():
                        skip_choice_count += 1
            else:
                if self.ronho_candidates[player.id]:
                    rest_ronho_candidate_count += 1
                if self.daiminkan_candidates[player.id]:
                    rest_daiminkan_candidate_count += 1
                if self.pon_candidates[player.id]:
                    rest_pon_candidate_count += 1
                if self.chii_candidates[player.id]:
                    rest_chii_candidate_count += 1
                if self.skip_candidates[player.id]:
                    rest_skip_candidate_count += 1

        if rest_ronho_candidate_count > 0:
            return Pending()

        if ronho_choice_count > 0:
            actions = []
            for player in self.game.get_players_from_teban():
                c = self.choice[player.id]
                if isinstance(c, Ronho):
                    actions.append((player, c))
            return RonhoResult(actions)

        if rest_daiminkan_candidate_count > 0:
            return Pending()

        if daiminkan_choice_count > 0:
            for player in self.game.get_players_from_teban():
                c = self.choice[player.id]
                if isinstance(c, Daiminkan):
                    return DaiminkanResult(player, c)

        if rest_pon_candidate_count > 0:
            return Pending()

        if pon_choice_count > 0:
            for player in self.game.get_players_from_teban():
                c = self.choice[player.id]
                if isinstance(c, Pon):
                    return PonResult(player, c)

        if rest_chii_candidate_count > 0:
            return Pending()

        if chii_choice_count > 0:
            for player in self.game.get_players_from_teban():
                c = self.choice[player.id]
                if isinstance(c, Chii):
                    return ChiiResult(player, c)

        if rest_skip_candidate_count > 0:
            return Pending()

        if skip_choice_count > 0:
            return SkipResult()

        return Pending()

    def list_ronho_candidates(self, player: Player) -> list[Ronho]:
        if self.game.last_dahai is None:
            raise Exception()

        # Not agari
        if ShantenCalculator(player.juntehai + self.game.last_dahai).shanten != -1:
            return []

        # Not yakuari
        if not AgariCalculator(self.game, player).ten > 0:
            return []

        return [Ronho()]

    def list_daiminkan_candidates(self, player: Player) -> list[Daiminkan]:
        if self.game.last_dahai is None:
            raise Exception()

        # Not enough yama
        if self.game.yama.rest_tsumo_count == 0:
            return []

        # Riichi completed
        if player.is_riichi_completed:
            return []

        # Four kans exist
        if self.game.kan_count >= 4:
            return []

        stolen = self.game.last_dahai
        from_who = player.get_zaichi_from_zaseki(self.game.teban)

        candidates = []
        hais = [hai for hai in player.juntehai if hai.suit == stolen.suit and hai.number == stolen.number]
        if len(hais) >= 3:
            candidates.append(Daiminkan(hais=HaiGroup(hais + [stolen]), stolen=stolen, from_who=from_who))

        return candidates

    def list_pon_candidates(self, player: Player) -> list[Pon]:
        if self.game.last_dahai is None:
            raise Exception()

        # Not enough yama
        if self.game.yama.rest_tsumo_count == 0:
            return []

        # Riichi completed
        if player.is_riichi_completed:
            return []

        stolen = self.game.last_dahai
        from_who = player.get_zaichi_from_zaseki(self.game.teban)

        candidates = []
        b = []
        r = []
        # Shuffle juntehai to select b and r randomly.
        for hai in random.sample(player.juntehai, len(player.juntehai)):
            if hai.suit == stolen.suit and hai.number == stolen.number:
                if hai.color == "b":
                    b.append(hai)
                else:
                    r.append(hai)

        if len(b) >= 2:
            candidates.append(Pon(hais=HaiGroup([stolen, b[0], b[1]]), stolen=stolen, from_who=from_who))
        if len(b) >= 1 and len(r) >= 1:
            candidates.append(Pon(hais=HaiGroup([stolen, b[0], r[0]]), stolen=stolen, from_who=from_who))

        return candidates

    def list_chii_candidates(self, player: Player) -> list[Chii]:
        if self.game.last_dahai is None:
            raise Exception()

        # Not enoguh yama
        if self.game.yama.rest_tsumo_count == 0:
            return []

        # Riichi completed
        if player.is_riichi_completed:
            return []

        # Not Shimocha
        if player != self.game.teban_player.shimocha:
            return []

        stolen = self.game.last_dahai

        prev2: dict[str, Hai | None] = {"b": None, "r": None}
        prev1: dict[str, Hai | None] = {"b": None, "r": None}
        next1: dict[str, Hai | None] = {"b": None, "r": None}
        next2: dict[str, Hai | None] = {"b": None, "r": None}

        # Shuffle juntehai to select prev2, prev1, next1, and next2 randomly.
        for hai in random.sample(player.juntehai, len(player.juntehai)):
            if hai.suit == "z" or hai.suit != stolen.suit:
                continue

            if hai.number == stolen.number - 2:
                prev2[hai.color] = hai
            if hai.number == stolen.number - 1:
                prev1[hai.color] = hai
            if hai.number == stolen.number + 1:
                next1[hai.color] = hai
            if hai.number == stolen.number + 2:
                next2[hai.color] = hai

        candidates = []
        pattern1 = list(product(prev2.values(), prev1.values(), [stolen]))
        pattern2 = list(product(prev1.values(), [stolen], next1.values()))
        pattern3 = list(product([stolen], next1.values(), next2.values()))
        for hai1, hai2, hai3 in pattern1 + pattern2 + pattern3:
            if hai1 is None or hai2 is None or hai3 is None:
                continue

            chii = Chii(hais=HaiGroup([hai1, hai2, hai3]), stolen=stolen)

            # Pass if cannot dahai after chii
            kuikae_hais = player.juntehai & chii.kuikae_hais
            if len(player.juntehai) - 2 == len(kuikae_hais):
                continue

            candidates.append(chii)

        return candidates

    def list_skip_candidates(self) -> list[Skip]:
        return [Skip()]
