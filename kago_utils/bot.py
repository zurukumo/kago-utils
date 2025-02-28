import random

from kago_utils.player import Player


class Bot(Player):
    def select_teban_action(self) -> None:
        resolver = self.game.teban_action_resolver
        resolver.register_dahai(self, random.choice(resolver.dahai_candidates[self.id]))

    def select_non_teban_action(self) -> None:
        resolver = self.game.non_teban_action_resolver
        resolver.register_skip(self, random.choice(resolver.skip_candidates[self.id]))
