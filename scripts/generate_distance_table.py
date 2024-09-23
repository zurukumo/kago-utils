import gzip
import os
import pickle
import time
from heapq import heappop, heappush
from itertools import combinations_with_replacement, product
from typing import Literal


class DistanceTableGenerator:
    def __init__(self, type: Literal["suuhai", "zihai"]) -> None:
        self.distance_table: dict[tuple[tuple[int, ...], int], int] = dict()
        self.heap_queue: list[tuple[int, list[int], int]] = []

        match type:
            case 'suuhai':
                self.n_hai_kind = 9
                self.max_n_shuntsu = 4
                self.max_n_koutsu = 4
                self.max_n_jantou = 1
                self.filename = 'suuhai_distance_table.pickle.gz'
            case 'zihai':
                self.n_hai_kind = 7
                self.max_n_shuntsu = 0
                self.max_n_koutsu = 4
                self.max_n_jantou = 1
                self.filename = 'zihai_distance_table.pickle.gz'

    def list_agari_patterns(self) -> list[list[int]]:
        patterns = []
        counts = (
            range(self.max_n_shuntsu + 1),
            range(self.max_n_koutsu + 1),
            range(self.max_n_jantou + 1)
        )
        for (n_shuntsu, n_koutsu, n_jantou) in product(*counts):
            if n_shuntsu + n_koutsu > 4:
                continue

            positions = (
                combinations_with_replacement(range(self.n_hai_kind - 2), n_shuntsu),
                combinations_with_replacement(range(self.n_hai_kind), n_koutsu),
                combinations_with_replacement(range(self.n_hai_kind), n_jantou)
            )
            for (shuntsu_positions, kootsu_positions, jantou_positions) in product(*positions):
                pattern = [0] * self.n_hai_kind
                for i in shuntsu_positions:
                    pattern[i] += 1
                    pattern[i+1] += 1
                    pattern[i+2] += 1
                for i in kootsu_positions:
                    pattern[i] += 3
                for i in jantou_positions:
                    pattern[i] += 2

                if all([v <= 4 for v in pattern]):
                    patterns.append(pattern)
        return patterns

    @staticmethod
    def distance_between_patterns(before: tuple[int, ...], after: tuple[int, ...]) -> int:
        return sum([max(a - b, 0) for b, a in zip(before, after)])

    def update_table_and_queue(self, distance: int, pattern: list[int], length: int) -> None:
        key = (tuple(pattern), length)
        if key not in self.distance_table or distance < self.distance_table[key]:
            self.distance_table[key] = distance
            heappush(self.heap_queue, (distance, pattern, length))

    def generate(self) -> None:
        # Initialize
        for pattern in self.list_agari_patterns():
            distance, pattern, length = 0, pattern, sum(pattern)
            self.update_table_and_queue(distance, pattern, length)

        # Dijkstra
        while self.heap_queue:
            distance, pattern, length = heappop(self.heap_queue)
            if distance > self.distance_table[(tuple(pattern), length)]:
                continue

            # Decreasing the number of hais increases the distance
            for i in range(self.n_hai_kind):
                if pattern[i] > 0:
                    pattern[i] -= 1
                    self.update_table_and_queue(distance + 1, pattern.copy(), length)
                    pattern[i] += 1

            # When the number of hais is 14, can't increase the number of hais
            if sum(pattern) == 14:
                continue

            # Increasing the number of hais keeps the distance the same
            for i in range(self.n_hai_kind):
                if pattern[i] < 4:
                    pattern[i] += 1
                    self.update_table_and_queue(distance, pattern.copy(), length)
                    pattern[i] -= 1

        self.save_table()

    def save_table(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, f'../kago_utils/data/{self.filename}')
        with gzip.open(file_path, 'wb') as f:
            pickle.dump(dict(self.distance_table), f)


if __name__ == '__main__':
    suuhai_start_time = time.time()
    DistanceTableGenerator('suuhai').generate()
    print(f'Suuhai Distance Table Generation Time: {time.time() - suuhai_start_time} seconds')

    zihai_start_time = time.time()
    DistanceTableGenerator('zihai').generate()
    print(f'Zihai Distance Table Generation Time: {time.time() - zihai_start_time} seconds')
