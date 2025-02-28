import pytest

from kago_utils.hai import Hai
from kago_utils.yama import Yama


def test_init():
    Yama()


def test_generate():
    yama1 = Yama()
    yama1.generate()

    assert len(yama1.tsumo_hais) == 122
    assert len(yama1.rinshan_hais) == 4
    assert len(yama1.dora_hyouji_hais) == 10

    yama2 = Yama()
    yama2.generate()

    assert yama1.tsumo_hais != yama2.tsumo_hais


def tes_tsumo():
    yama = Yama()
    yama.generate()

    tsumo_hai = yama.tsumo()
    assert isinstance(tsumo_hai, Hai)
    assert len(yama.tsumo_hais) == 121


def test_tsumo_after_10_tsumo_and_2_rinshan_tsumo():
    yama = Yama()
    yama.generate()

    for _ in range(10):
        yama.tsumo()
    for _ in range(2):
        yama.rinshan_tsumo()

    yama.tsumo()


def test_tsumo_after_122_tsumo():
    yama = Yama()
    yama.generate()

    for _ in range(122):
        yama.tsumo()

    with pytest.raises(ValueError):
        yama.tsumo()


def test_tsumo_after_121_tsumo_and_1_rinshan_tsumo():
    yama = Yama()
    yama.generate()

    for _ in range(121):
        yama.tsumo()
    for _ in range(1):
        yama.rinshan_tsumo()

    with pytest.raises(ValueError):
        yama.tsumo()


def test_tsumo_after_118_tsumo_and_4_rinshan_tsumo():
    yama = Yama()
    yama.generate()

    for _ in range(118):
        yama.tsumo()
    for _ in range(4):
        yama.rinshan_tsumo()

    with pytest.raises(ValueError):
        yama.tsumo()


def test_rinshan_tsumo():
    yama = Yama()
    yama.generate()

    rinshan_hai = yama.rinshan_tsumo()
    assert isinstance(rinshan_hai, Hai)
    assert len(yama.rinshan_hais) == 3


def test_rinshan_tsumo_after_3_rinshan_tsumo():
    yama = Yama()
    yama.generate()

    for _ in range(3):
        yama.rinshan_tsumo()

    yama.rinshan_tsumo()


def test_rinshan_tsumo_after_4_rinshan_tsumo():
    yama = Yama()
    yama.generate()

    for _ in range(4):
        yama.rinshan_tsumo()

    with pytest.raises(ValueError):
        yama.rinshan_tsumo()


def test_open_dora_hyouji_hai():
    yama = Yama()
    yama.generate()

    assert yama.n_open_dora_hyouji_hais == 1

    yama.open_dora_hyouji_hai()
    assert yama.n_open_dora_hyouji_hais == 2


def test_opened_dora_hyouji_hais():
    yama = Yama()
    yama.generate()

    assert len(yama.opened_dora_hyouji_hais) == 1

    yama.open_dora_hyouji_hai()
    assert len(yama.opened_dora_hyouji_hais) == 2


def test_opened_uradora_hyouji_hais():
    yama = Yama()
    yama.generate()

    assert len(yama.opened_uradora_hyouji_hais) == 1

    yama.open_dora_hyouji_hai()
    assert len(yama.opened_uradora_hyouji_hais) == 2


def test_rest_tsumo_count():
    yama = Yama()
    yama.generate()

    assert yama.rest_tsumo_count == 122

    yama.tsumo()
    assert yama.rest_tsumo_count == 121

    yama.rinshan_tsumo()
    assert yama.rest_tsumo_count == 120
