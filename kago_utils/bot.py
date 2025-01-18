import random

from kago_utils.player import Player


class Bot(Player):
    def select_teban_action(self) -> None:
        resolver = self.game.teban_action_resolver
        resolver.register_dahai(self, random.choice(resolver.dahai_candidates[self.id]))
