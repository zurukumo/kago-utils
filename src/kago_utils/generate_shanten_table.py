import pickle
from collections import deque
from itertools import product


def extract_shuntsu(tehai):
    N = len(tehai)

    # queue format: [tehai, n_shuntsu, start]
    queue = deque([])
    queue.append([tehai.copy(), 0, 0])

    while queue:
        tehai, n_shuntsu, start = queue.popleft()
        yield tehai.copy(), n_shuntsu

        for i in range(start, N):
            if i + 2 < N and i <= 6 and tehai[i] >= 1 and tehai[i+1] >= 1 and tehai[i+2] >= 1:
                tehai[i] -= 1
                tehai[i+1] -= 1
                tehai[i+2] -= 1
                queue.append([tehai.copy(), n_shuntsu + 1, i])
                tehai[i] += 1
                tehai[i+1] += 1
                tehai[i+2] += 1


def extract_kootsu(tehai):
    N = len(tehai)

    # queue format: [tehai, n_kootsu, start]
    queue = deque([])
    queue.append([tehai.copy(), 0, 0])

    while queue:
        tehai, n_kootsu, start = queue.popleft()
        yield tehai.copy(), n_kootsu

        for i in range(start, N):
            if tehai[i] >= 3:
                tehai[i] -= 3
                queue.append([tehai.copy(), n_kootsu + 1, i])
                tehai[i] += 3


def extract_toitsu(tehai):
    N = len(tehai)

    # queue format: [tehai, n_toitsu, start]
    queue = deque([])
    queue.append([tehai.copy(), 0, 0])

    while queue:
        tehai, n_toitsu, start = queue.popleft()
        yield tehai.copy(), n_toitsu

        for i in range(start, N):
            if tehai[i] >= 2:
                tehai[i] -= 2
                queue.append([tehai.copy(), n_toitsu + 1, i])
                tehai[i] += 2


def extract_taatsu(tehai):
    N = len(tehai)

    # queue format: [tehai, n_taatsu, start]
    queue = deque([])
    queue.append([tehai.copy(), 0, 0])

    while queue:
        tehai, n_taatsu, start = queue.popleft()
        yield tehai.copy(), n_taatsu

        for i in range(start, N):
            if i + 1 < N and tehai[i] >= 1 and tehai[i+1] >= 1:
                tehai[i] -= 1
                tehai[i+1] -= 1
                queue.append([tehai.copy(), n_taatsu + 1, i])
                tehai[i] += 1
                tehai[i+1] += 1

            if i + 2 < N and tehai[i] >= 1 and tehai[i+2] >= 1:
                tehai[i] -= 1
                tehai[i+2] -= 1
                queue.append([tehai.copy(), n_taatsu + 1, i])
                tehai[i] += 1
                tehai[i+2] += 1


def list_suuhai_patterns(tehai):
    tehai = list(tehai)
    for rest_tehai, n_kootsu in extract_kootsu(tehai):
        for rest_tehai, n_shuntsu in extract_shuntsu(rest_tehai):
            for rest_tehai, n_toitsu in extract_toitsu(rest_tehai):
                for rest_tehai, n_taatsu in extract_taatsu(rest_tehai):
                    yield n_kootsu, n_shuntsu, n_toitsu, n_taatsu


def list_zihai_patterns(tehai):
    tehai = list(tehai)
    for rest_tehai, n_kootsu in extract_kootsu(tehai):
        for rest_tehai, n_toitsu in extract_toitsu(rest_tehai):
            yield n_kootsu, 0, n_toitsu, 0


def select_better_pattern1(max1, current):
    max_score = max1[0] * 2 + max1[1]
    current_score = current[0] * 2 + current[1]
    if current_score > max_score or (current_score == max_score and current[2]):
        return current
    else:
        return max1


def select_better_pattern2(max2, current):
    max_score = max2[0] * 8 + max2[1]
    current_score = current[0] * 8 + current[1]
    if current_score > max_score or (current_score == max_score and current[2]):
        return current
    else:
        return max2


def select_better_pattern3(max3, current):
    max_score = max3[0] * 2 + max3[1] + (100 if max3[2] else 0)
    current_score = current[0] * 2 + current[1] + (100 if current[2] else 0)
    if current_score > max_score or (current_score == max_score and current[2]):
        return current
    else:
        return max3


def select_better_pattern4(max4, current):
    max_score = max4[0] * 8 + max4[1] + (100 if max4[2] else 0)
    current_score = current[0] * 8 + current[1] + (100 if current[2] else 0)
    if current_score > max_score or (current_score == max_score and current[2]):
        return current
    else:
        return max4


# generate patterns
def generate_patterns():
    suuhai_patterns = dict()
    zihai_patterns = dict()

    # generate suuhai patterns
    for tehai in product([0, 1, 2, 3, 4], repeat=9):
        if sum(tehai) > 14:
            continue

        print(tehai)

        # pattern format: [n_mentsu, n_pre_mentsu, has_toitsu]
        max_pattern1 = 0, 0, False  # maximize n_mentsu * 2 + n_pre_mentsu
        max_pattern2 = 0, 0, False  # maximize n_mentsu * 8 + n_pre_mentsu
        max_pattern3 = 0, 0, False  # maximize n_mentsu * 2 + n_pre_mentsu + 100 if has_toitsu
        max_pattern4 = 0, 0, False  # maximize n_mentsu * 8 + n_pre_mentsu + 100 if has_toitsu
        for n_kootsu, n_shuntsu, n_toitsu, n_taatsu in list_suuhai_patterns(tehai):
            n_mentsu = n_kootsu + n_shuntsu
            n_pre_mentsu = n_toitsu + n_taatsu
            has_toitsu = n_toitsu > 0
            current_pattern = n_mentsu, n_pre_mentsu, has_toitsu
            max_pattern1 = select_better_pattern1(max_pattern1, current_pattern)
            max_pattern2 = select_better_pattern2(max_pattern2, current_pattern)
            max_pattern3 = select_better_pattern3(max_pattern3, current_pattern)
            max_pattern4 = select_better_pattern4(max_pattern4, current_pattern)

        # when max1 is same as max2, only store max1 because of memory efficiency
        suuhai_patterns[tehai] = list(set([max_pattern1, max_pattern2, max_pattern3, max_pattern4]))

    # generate zihai patterns
    for tehai in product([0, 1, 2, 3, 4], repeat=7):
        if sum(tehai) > 14:
            continue

        print(tehai)

        # pattern format: [n_mentsu, n_pre_mentsu, has_toitsu]
        max_pattern1 = 0, 0, False  # maximize n_mentsu * 2 + n_pre_mentsu
        max_pattern2 = 0, 0, False  # maximize n_mentsu * 8 + n_pre_mentsu
        max_pattern3 = 0, 0, False  # maximize n_mentsu * 2 + n_pre_mentsu + (100 if has_toitsu)
        max_pattern4 = 0, 0, False  # maximize n_mentsu * 8 + n_pre_mentsu + (100 if has_toitsu)
        for n_kootsu, n_shuntsu, n_toitsu, n_taatsu in list_zihai_patterns(tehai):
            n_mentsu = n_kootsu + n_shuntsu
            n_pre_mentsu = n_toitsu + n_taatsu
            has_toitsu = n_toitsu > 0
            current_pattern = n_mentsu, n_pre_mentsu, has_toitsu
            max_pattern1 = select_better_pattern1(max_pattern1, current_pattern)
            max_pattern2 = select_better_pattern2(max_pattern2, current_pattern)
            max_pattern3 = select_better_pattern3(max_pattern3, current_pattern)
            max_pattern4 = select_better_pattern4(max_pattern4, current_pattern)

        # when max1 is same as max2, only store max1 because of memory efficiency
        zihai_patterns[tehai] = list(set([max_pattern1, max_pattern2, max_pattern3, max_pattern4]))

    with open('suuhai_patterns.pickle', 'wb') as f:
        pickle.dump(suuhai_patterns, f)
    with open('zihai_patterns.pickle', 'wb') as f:
        pickle.dump(zihai_patterns, f)


if __name__ == '__main__':
    generate_patterns()
