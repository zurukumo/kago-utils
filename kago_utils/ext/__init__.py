from importlib.resources import files

from ._shanten import (
    calculate_chiitoitsu_shanten,
    calculate_kokushimusou_shanten,
    calculate_regular_shanten,
    init_tables_from_txt,
)

# Locate packaged .txt resources and initialize tables on import
_dist_dir = files("kago_utils.resources.distance_tables")
_suuhai_path = str(_dist_dir / "suuhai_distance_table.txt")
_zihai_path = str(_dist_dir / "zihai_distance_table.txt")
init_tables_from_txt(_suuhai_path, _zihai_path)

__all__ = [
    "calculate_regular_shanten",
    "calculate_chiitoitsu_shanten",
    "calculate_kokushimusou_shanten",
]
