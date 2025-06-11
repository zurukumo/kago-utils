from __future__ import annotations

import functools
import gzip
import os
import pickle

from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup

# Loading distance tables
current_dir = os.path.dirname(os.path.abspath(__file__))
suuhai_distance_table_path = os.path.join(current_dir, "resources/distance_tables/suuhai_distance_table.pickle.gz")
zihai_distance_table_path = os.path.join(current_dir, "resources/distance_tables/zihai_distance_table.pickle.gz")
with gzip.open(suuhai_distance_table_path, "rb") as f:
    suuhai_distance_table: dict[tuple[tuple[int, ...], int], int] = pickle.load(f)
with gzip.open(zihai_distance_table_path, "rb") as f:
    zihai_distance_table: dict[tuple[tuple[int, ...], int], int] = pickle.load(f)


def validate(juntehai: HaiGroup) -> None:
    if len(juntehai) > 14:
        raise ValueError(f"Invalid data: the total count of hais should be 14 or less. Data: {juntehai}")
    if len(juntehai) % 3 == 0:
        raise ValueError(f"Invalid data: the total count of hais should be 3n+1 or 3n+2. Data: {juntehai}")


def calculate_shanten(juntehai: HaiGroup) -> int:
    validate(juntehai)
    counter = juntehai.to_counter34()
    return min(
        __calculate__regular_shanten(tuple(counter)),
        __calculate__chiitoitsu_shanten(counter),
        __calculate__kokushimusou_shanten(counter),
    )


@functools.lru_cache(maxsize=34 * 34)
def __calculate__regular_shanten(counter: tuple[int]) -> int:
    if suuhai_distance_table is None or zihai_distance_table is None:
        raise RuntimeError("Patterns are not loaded")

    manzu = counter[0:9]
    pinzu = counter[9:18]
    souzu = counter[18:27]
    zihai = counter[27:34]

    min_shanten = 8
    n_menstu = sum(counter) // 3
    for n_manzu_mentsu, n_pinzu_mentsu, n_souzu_mentsu, n_zihai_mentsu in __divide_into_four(n_menstu):
        for n_manzu_jantou, n_pinzu_jantou, n_souzu_jantou, n_zihai_jantou in __divide_into_four(1):
            n_manzu = n_manzu_mentsu * 3 + n_manzu_jantou * 2
            n_pinzu = n_pinzu_mentsu * 3 + n_pinzu_jantou * 2
            n_souzu = n_souzu_mentsu * 3 + n_souzu_jantou * 2
            n_zihai = n_zihai_mentsu * 3 + n_zihai_jantou * 2

            manzu_distance = suuhai_distance_table[(manzu, n_manzu)]
            pinzu_distance = suuhai_distance_table[(pinzu, n_pinzu)]
            souzu_distance = suuhai_distance_table[(souzu, n_souzu)]
            zihai_distance = zihai_distance_table[(zihai, n_zihai)]

            min_shanten = min(min_shanten, manzu_distance + pinzu_distance + souzu_distance + zihai_distance - 1)

    return min_shanten


def __calculate__chiitoitsu_shanten(counter: list[int]) -> int:
    if not 13 <= sum(counter) <= 14:
        return 9999

    n_toitsu = 0
    n_unique_hai = 0

    for i in range(34):
        if counter[i] >= 2:
            n_toitsu += 1
        if counter[i] >= 1:
            n_unique_hai += 1

    return 6 - n_toitsu + (7 - n_unique_hai if n_unique_hai < 7 else 0)


def __calculate__kokushimusou_shanten(counter: list[int]) -> int:
    if not 13 <= sum(counter) <= 14:
        return 9999

    n_yaochu_hai = 0
    has_toitsu = False
    yaochu_hai_list = HaiGroup.from_code("19m19p19s1234567z").to_list34()

    for i in yaochu_hai_list:
        if counter[i] >= 1:
            n_yaochu_hai += 1
        if counter[i] >= 2:
            has_toitsu = True

    return 13 - n_yaochu_hai - (1 if has_toitsu else 0)


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


def __divide_into_four(n: int) -> list[tuple[int, int, int, int]]:
    ret = []
    for a in range(n + 1):
        for b in range(n - a + 1):
            for c in range(n - a - b + 1):
                d = n - a - b - c
                ret.append((a, b, c, d))
    return ret
