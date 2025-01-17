import random

from kago_utils.player import Player


class Bot(Player):
    def select_tsumoho_riichi_ankan_dahai(self) -> None:
        resolver = self.game.tsumoho_riichi_ankan_kakan_dahai_resolver
        resolver.register_dahai(self, random.choice(resolver.dahai_candidates[self.id]))
