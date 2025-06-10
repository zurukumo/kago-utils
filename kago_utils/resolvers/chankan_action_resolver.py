from __future__ import annotations

from typing import TYPE_CHECKING

from kago_utils.actions import Ronho, Skip
from kago_utils.agari_calculator import AgariCalculator
from kago_utils.player import Player
from kago_utils.shanten_calculator import ShantenCalculator

from .results import Pending, RonhoResult, SkipResult

if TYPE_CHECKING:
    from kago_utils.game import Game


# TODO: NonTebanActionResolverとコードが被っている
class ChankanActionResolver:
    game: Game
    ronho_candidates: dict[str, list[Ronho]]
    skip_candidates: dict[str, list[Skip]]
    choice: dict[str, Ronho | Skip | None]

    __slots__ = (
        "game",
        "ronho_candidates",
        "skip_candidates",
        "choice",
    )

    def __init__(self, game: Game) -> None:
        self.game = game

    def reset(self) -> None:
        self.ronho_candidates = {player.id: [] for player in self.game.players}
        self.skip_candidates = {player.id: [] for player in self.game.players}
        self.choice = {player.id: None for player in self.game.players}

    def prepare(self) -> None:
        self.reset()

        for player in self.game.players:
            if player == self.game.teban_player:
                continue

            self.ronho_candidates[player.id] = self.list_ronho_candidates(player)
            self.skip_candidates[player.id] = self.list_skip_candidates()
            self.choice[player.id] = None

    def register_ronho(self, player: Player, ronho: Ronho) -> None:
        # print("ronhoが登録されました")
        if self.choice[player.id] is not None:
            return
        if ronho in self.ronho_candidates[player.id]:
            self.choice[player.id] = ronho

    def register_skip(self, player: Player, skip: Skip) -> None:
        # print("skipが登録されました")
        if self.choice[player.id] is not None:
            return
        if skip in self.skip_candidates[player.id]:
            self.choice[player.id] = skip

    def resolve(self) -> RonhoResult | SkipResult | Pending:
        ronho_choice_count = 0
        skip_choice_count = 0
        rest_ronho_candidate_count = 0
        rest_skip_candidate_count = 0

        for player in self.game.get_players_from_teban():
            c = self.choice[player.id]
            if c is not None:
                match c:
                    case Ronho():
                        ronho_choice_count += 1
                    case Skip():
                        skip_choice_count += 1
            else:
                if self.ronho_candidates[player.id]:
                    rest_ronho_candidate_count += 1
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

        if rest_skip_candidate_count > 0:
            return Pending()

        if skip_choice_count > 0:
            return SkipResult()

        return Pending()

    def list_ronho_candidates(self, player: Player) -> list[Ronho]:
        if self.game.last_added_hai is None:
            raise Exception()

        # Not agari
        if ShantenCalculator(player.juntehai + self.game.last_added_hai).shanten != -1:
            return []

        # Not yakuari
        if not AgariCalculator(self.game, player).ten > 0:
            return []

        return [Ronho()]

    def list_skip_candidates(self) -> list[Skip]:
        return [Skip()]
