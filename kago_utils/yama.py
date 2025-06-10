import random

from kago_utils.hai import Hai


class Yama:
    tsumo_hais: list[Hai]
    rinshan_hais: list[Hai]
    dora_hyouji_hais: list[Hai]
    n_open_dora_hyouji_hais: int

    __slot__ = ("tsumo_hais", "rinshan_hais", "dora_hyouji_hais", "n_open_dora_hyouji_hais")

    def __init__(self) -> None:
        self.tsumo_hais = []
        self.rinshan_hais = []
        self.dora_hyouji_hais = []
        self.n_open_dora_hyouji_hais = 1

    def shuffle(self) -> list[Hai]:
        hais = [Hai(id) for id in range(136)]
        random.shuffle(hais)
        return hais

    def generate(self) -> None:
        hais = self.shuffle()
        self.rinshan_hais = [hais[2], hais[3], hais[0], hais[1]]
        self.dora_hyouji_hais = hais[4:14]
        self.tsumo_hais = hais[14:136]
        self.n_open_dora_hyouji_hais = 1

    def tsumo(self) -> Hai:
        if len(self.tsumo_hais) + len(self.rinshan_hais) == 4:
            raise ValueError("There is no tsumo hai.")

        return self.tsumo_hais.pop()

    def rinshan_tsumo(self) -> Hai:
        if len(self.rinshan_hais) == 0:
            raise ValueError("There is no rinshan tsumo hai.")

        return self.rinshan_hais.pop()

    def open_dora_hyouji_hai(self) -> None:
        self.n_open_dora_hyouji_hais += 1

    @property
    def opened_dora_hyouji_hais(self) -> list[Hai]:
        return self.dora_hyouji_hais[1 : self.n_open_dora_hyouji_hais * 2 : 2]

    @property
    def opened_uradora_hyouji_hais(self) -> list[Hai]:
        return self.dora_hyouji_hais[0 : self.n_open_dora_hyouji_hais * 2 : 2]

    @property
    def rest_tsumo_count(self) -> int:
        return len(self.tsumo_hais) + len(self.rinshan_hais) - 4
