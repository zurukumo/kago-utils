import os
import pickle
import time
from collections import defaultdict
from itertools import combinations_with_replacement, product

MAX_N_MENTSU = 4
MAX_N_JANTOU = 1

N_SUUHAI_KIND = 9
N_ZIHAI_KIND = 7


def list_suuhai_completed_patterns():
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
                                yield pattern


def list_zihai_completed_patterns():
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
                        yield pattern


def list_suuhai_patterns():
    for pattern in product(range(5), repeat=N_SUUHAI_KIND):
        if sum(pattern) <= 14:
            yield pattern


def list_zihai_patterns():
    for pattern in product(range(5), repeat=N_ZIHAI_KIND):
        if sum(pattern) <= 14:
            yield pattern


def distance_between_patterns(before, after):
    return sum([max(a - b, 0) for b, a in zip(before, after)])


def generate_patterns_pickle():
    suuhai_shanten = defaultdict(lambda: float('inf'))
    zihai_shanten = defaultdict(lambda: float('inf'))

    completed_suuhai_patterns = list(list_suuhai_completed_patterns())
    completed_zihai_patterns = list(list_zihai_completed_patterns())

    for pattern in list_suuhai_patterns():
        print('suuhai', pattern)
        for completed_pattern in completed_suuhai_patterns:
            distance = distance_between_patterns(pattern, completed_pattern)
            target_length = sum(completed_pattern)
            key = (pattern, target_length)

            suuhai_shanten[key] = min(suuhai_shanten[key], distance)

    for pattern in list_zihai_patterns():
        print('zihai', pattern)
        for completed_pattern in completed_zihai_patterns:
            distance = distance_between_patterns(pattern, completed_pattern)
            target_length = sum(completed_pattern)
            key = (pattern, target_length)

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

    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # suuhai_shanten_path = os.path.join(current_dir, 'data/suuhai_shanten.pickle')
    # with open(suuhai_shanten_path, 'rb') as f:
    #     a = pickle.load(f)

    # for k, v in a.items():
    #     print(k, v)
