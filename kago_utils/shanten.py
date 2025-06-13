from __future__ import annotations

from kago_utils.ext._shanten import (
    calculate_chiitoitsu_shanten,
    calculate_kokushimusou_shanten,
    calculate_regular_shanten,
)
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup


def validate(juntehai: HaiGroup) -> None:
    if len(juntehai) > 14:
        raise ValueError(f"Invalid data: the total count of hais should be 14 or less. Data: {juntehai}")
    if len(juntehai) % 3 == 0:
        raise ValueError(f"Invalid data: the total count of hais should be 3n+1 or 3n+2. Data: {juntehai}")


def calculate_shanten(juntehai: HaiGroup) -> int:
    validate(juntehai)
    counter = juntehai.to_counter34()
    return min(
        calculate_regular_shanten(counter),
        calculate_chiitoitsu_shanten(counter),
        calculate_kokushimusou_shanten(counter),
    )


def calculate_yuukouhai(juntehai: HaiGroup) -> HaiGroup:
    if not isinstance(juntehai, HaiGroup):
        raise TypeError(f"juntehai should be HaiGroup, but {juntehai.__class__.__name__}")

    if len(juntehai) % 3 != 1:
        raise ValueError(f"Invalid data: HaiGroup's total count of hais should be 3n+1. Data: {juntehai.__repr__()}")

    current_shanten = calculate_shanten(juntehai)

    yuukouhai = []
    for i in range(136):
        if Hai(i) in juntehai:
            continue
        new_shanten = calculate_shanten(juntehai + Hai(i))
        if new_shanten < current_shanten:
            yuukouhai.append(i)

    return HaiGroup.from_list(yuukouhai)
