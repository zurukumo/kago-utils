# kago-utils
Python用の麻雀ライブラリ。

Mahjong library for Python.

## インストール
```sh
pip install kago-utils
```

## 使い方
### 牌姿の定義
```python
from kago_utils.hai_group import HaiGroup

# from_codeの0は赤5を意味します。天鳳の牌理ツールと同じ仕様です。
tehai1 = HaiGroup.from_code("123m406p789s11122z")
tehai2 = HaiGroup.from_list34([0, 1, 2, 12, 13, 14, 24, 25, 26, 27, 27, 27, 28, 28])
tehai3 = HaiGroup.from_counter34([
    1, 1, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 1,
    3, 2, 0, 0, 0, 0, 0
])

print(tehai1 == tehai2 == tehai3)  # True
```

`from_list136`と`from_counter136`も同様に使えます。

### 向聴数の計算
```python
from kago_utils.hai_group import HaiGroup
from kago_utils.shanten_calculator import ShantenCalculator

# 手牌
tehai = HaiGroup.from_code("123m456p789s11122z")

# 向聴数
shanten = ShantenCalculator(tehai).shanten
print(shanten)  # -1
```


## 謝辞
- `tests/data/p_hon_10000.txt`
- `tests/data/p_koku_10000.txt`
- `tests/data/p_normal_10000.txt`
- `tests/data/p_tin_10000.txt`

は、[あらの一人麻雀研究所](https://mahjong.ara.black/etc/shanten/shanten9.htm) からお借りしました。

その他、一部のテストデータは天鳳の牌譜から作成しました。

## Benchmark
https://zurukumo.github.io/kago-utils/dev/bench/
