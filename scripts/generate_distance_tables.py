import csv
import os
import time
from collections import deque
from itertools import combinations_with_replacement, product
from typing import Literal


class DistanceTableGenerator:
    def __init__(self, _type: Literal["suuhai", "zihai"]) -> None:
        match _type:
            case "suuhai":
                self.n_hai_kind = 9
                self.max_n_shuntsu = 4
                self.max_n_koutsu = 4
                self.max_n_jantou = 1
                self.filename = "suuhai_distance_table.txt"
            case "zihai":
                self.n_hai_kind = 7
                self.max_n_shuntsu = 0
                self.max_n_koutsu = 4
                self.max_n_jantou = 1
                self.filename = "zihai_distance_table.txt"

        self.distance_table = [[8] * (5**self.n_hai_kind) for _ in range(10)]
        self.queue: deque[tuple[int, list[int], int]] = deque()

    def list_agari_patterns(self) -> list[list[int]]:
        patterns = []
        counts = (range(self.max_n_shuntsu + 1), range(self.max_n_koutsu + 1), range(self.max_n_jantou + 1))
        for n_shuntsu, n_koutsu, n_jantou in product(*counts):
            if n_shuntsu + n_koutsu > 4:
                continue

            positions = (
                combinations_with_replacement(range(self.n_hai_kind - 2), n_shuntsu),
                combinations_with_replacement(range(self.n_hai_kind), n_koutsu),
                combinations_with_replacement(range(self.n_hai_kind), n_jantou),
            )
            for shuntsu_positions, kootsu_positions, jantou_positions in product(*positions):
                pattern = [0] * self.n_hai_kind
                for i in shuntsu_positions:
                    pattern[i] += 1
                    pattern[i + 1] += 1
                    pattern[i + 2] += 1
                for i in kootsu_positions:
                    pattern[i] += 3
                for i in jantou_positions:
                    pattern[i] += 2

                if all([v <= 4 for v in pattern]):
                    patterns.append(pattern)
        return patterns

    def generate_length_key(self, length: int) -> int:
        if length % 3 == 2:
            return (length - 2) * 2 // 3
        else:
            return (length - 3) * 2 // 3 + 1

    def generate_pattern_key(self, pattern: list[int]) -> int:
        k = 0
        for p in pattern:
            k = k * 5 + p
        return k

    def generate(self) -> None:
        # Initialize
        for pattern in self.list_agari_patterns():
            distance, pattern, length = 0, pattern, sum(pattern)
            self.queue.append((distance, pattern, length))
            lkey = self.generate_length_key(length)
            pkey = self.generate_pattern_key(pattern)
            self.distance_table[lkey][pkey] = distance

        # Dijkstra
        while self.queue:
            distance, pattern, length = self.queue.popleft()
            lkey = self.generate_length_key(length)
            pkey = self.generate_pattern_key(pattern)
            if distance > self.distance_table[lkey][pkey]:
                continue

            # Decreasing the number of hais increases the distance
            for i in range(self.n_hai_kind):
                if pattern[i] > 0:
                    pattern[i] -= 1
                    lkey = self.generate_length_key(length)
                    pkey = self.generate_pattern_key(pattern)
                    if distance + 1 < self.distance_table[lkey][pkey]:
                        self.distance_table[lkey][pkey] = distance + 1
                        self.queue.append((distance + 1, pattern.copy(), length))
                    pattern[i] += 1

            # When the number of hais is 14, can't increase the number of hais
            if sum(pattern) == 14:
                continue

            # Increasing the number of hais keeps the distance the same
            for i in range(self.n_hai_kind):
                if pattern[i] < 4:
                    pattern[i] += 1
                    lkey = self.generate_length_key(length)
                    pkey = self.generate_pattern_key(pattern)
                    if distance < self.distance_table[lkey][pkey]:
                        self.distance_table[lkey][pkey] = distance
                        self.queue.appendleft((distance, pattern.copy(), length))
                    pattern[i] -= 1

        self.save_table()

    def save_table(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, f"../kago_utils/resources/distance_tables/{self.filename}")
        with open(file_path, "w") as f:
            writer = csv.writer(f, delimiter=" ")
            writer.writerows(self.distance_table)


if __name__ == "__main__":
    suuhai_start_time = time.time()
    DistanceTableGenerator("suuhai").generate()
    print(f"Suuhai Distance Table Generation Time: {time.time() - suuhai_start_time} seconds")

    zihai_start_time = time.time()
    DistanceTableGenerator("zihai").generate()
    print(f"Zihai Distance Table Generation Time: {time.time() - zihai_start_time} seconds")
