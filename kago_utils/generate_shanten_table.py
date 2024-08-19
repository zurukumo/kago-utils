import os
import pickle
import time
from itertools import combinations_with_replacement, product

MAX_N_MENTSU = 4
MAX_N_JANTOU = 1

N_SUUHAI_KIND = 9
N_ZIHAI_KIND = 7


def list_suuhai_agari_patterns() -> list[tuple[int, ...]]:
    patterns = []
    for n_shuntsu in range(MAX_N_MENTSU + 1):
        for n_kootsu in range(MAX_N_MENTSU - n_shuntsu + 1):
            for n_jantou in range(MAX_N_JANTOU + 1):
                for shuntsu_positions in combinations_with_replacement(range(N_SUUHAI_KIND - 2), n_shuntsu):
                    for kootsu_positions in combinations_with_replacement(range(N_SUUHAI_KIND), n_kootsu):
                        for jantou_positions in combinations_with_replacement(range(N_SUUHAI_KIND), n_jantou):
                            pattern = [0] * N_SUUHAI_KIND
                            for i in shuntsu_positions:
                                pattern[i] += 1
                                pattern[i+1] += 1
                                pattern[i+2] += 1
                            for i in kootsu_positions:
                                pattern[i] += 3
                            for i in jantou_positions:
                                pattern[i] += 2
                            if all([pattern[i] <= 4 for i in range(N_SUUHAI_KIND)]):
                                patterns.append(tuple(pattern))
    return patterns


def list_zihai_agari_patterns() -> list[tuple[int, ...]]:
    patterns = []
    for n_kootsu in range(MAX_N_MENTSU + 1):
        for n_jantou in range(MAX_N_JANTOU + 1):
            for kootsu_positions in combinations_with_replacement(range(N_ZIHAI_KIND), n_kootsu):
                for jantou_positions in combinations_with_replacement(range(N_ZIHAI_KIND), n_jantou):
                    pattern = [0] * N_ZIHAI_KIND
                    for i in kootsu_positions:
                        pattern[i] += 3
                    for i in jantou_positions:
                        pattern[i] += 2
                    if all([pattern[i] <= 4 for i in range(N_ZIHAI_KIND)]):
                        patterns.append(tuple(pattern))
    return patterns


def list_suuhai_patterns() -> list[tuple[int, ...]]:
    patterns = []
    for pattern in product(range(5), repeat=N_SUUHAI_KIND):
        if sum(pattern) <= 14:
            patterns.append(pattern)
    return patterns


def list_zihai_patterns() -> list[tuple[int, ...]]:
    patterns = []
    for pattern in product(range(5), repeat=N_ZIHAI_KIND):
        if sum(pattern) <= 14:
            patterns.append(pattern)
    return patterns


def distance_between_patterns(before: tuple[int, ...], after: tuple[int, ...]) -> int:
    return sum([max(a - b, 0) for b, a in zip(before, after)])


def generate_patterns_pickle() -> None:
    suuhai_shanten: dict[tuple[tuple[int, ...], int], int] = dict()
    zihai_shanten: dict[tuple[tuple[int, ...], int], int] = dict()

    suuhai_patterns = list_suuhai_patterns()
    zihai_patterns = list_zihai_patterns()
    suuhai_agari_patterns = list_suuhai_agari_patterns()
    zihai_agari_patterns = list_zihai_agari_patterns()

    for pattern in suuhai_patterns:
        print('suuhai', pattern)
        for agari_pattern in suuhai_agari_patterns:
            distance = distance_between_patterns(pattern, agari_pattern)
            target_length = sum(agari_pattern)
            key = (pattern, target_length)

            if key not in suuhai_shanten:
                suuhai_shanten[key] = distance
            else:
                suuhai_shanten[key] = min(suuhai_shanten[key], distance)

    for pattern in zihai_patterns:
        print('zihai', pattern)
        for agari_pattern in zihai_agari_patterns:
            distance = distance_between_patterns(pattern, agari_pattern)
            target_length = sum(agari_pattern)
            key = (pattern, target_length)

            if key not in zihai_shanten:
                zihai_shanten[key] = distance
            else:
                zihai_shanten[key] = min(zihai_shanten[key], distance)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    suuhai_shanten_path = os.path.join(current_dir, 'data/suuhai_shanten.pickle')
    zihai_shanten_path = os.path.join(current_dir, 'data/zihai_shanten.pickle')
    with open(suuhai_shanten_path, 'wb') as f:
        pickle.dump(dict(suuhai_shanten), f)
    with open(zihai_shanten_path, 'wb') as f:
        pickle.dump(dict(zihai_shanten), f)


if __name__ == '__main__':
    start_time = time.time()
    generate_patterns_pickle()
    print('Time:', time.time() - start_time)
