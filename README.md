# kago-utils

## インストール
```sh
pip install kago-utils
```

## 前提
### 牌番号
以下の牌の番号を定義します。

34インデックス牌番号は見た目が同じ4つの牌の区別をしないものです。

136インデックス牌番号は見た目が同じ4つの牌の区別をするものです。

136インデックス牌番号の19、55、91は赤牌を表します。

| 牌 | 34インデックス | 136インデックス |
| --- | --- | --- |
| 1m | 0 | 0 ~ 3 |
| 2m | 1 | 4 ~ 7 |
| 3m | 2 | 8 ~ 11 |
| 4m | 3 | 12 ~ 15 |
| 5m | 4 | 16 ~ 19 |
| 6m | 5 | 20 ~ 23 |
| 7m | 6 | 24 ~ 27 |
| 8m | 7 | 28 ~ 31 |
| 9m | 8 | 32 ~ 35 |
| 1p | 9 | 36 ~ 39 |
| 2p | 10 | 40 ~ 43 |
| 3p | 11 | 44 ~ 47 |
| 4p | 12 | 48 ~ 51 |
| 5p | 13 | 52 ~ 55 |
| 6p | 14 | 56 ~ 59 |
| 7p | 15 | 60 ~ 63 |
| 8p | 16 | 64 ~ 67 |
| 9p | 17 | 68 ~ 71 |
| 1s | 18 | 72 ~ 75 |
| 2s | 19 | 76 ~ 79 |
| 3s | 20 | 80 ~ 83 |
| 4s | 21 | 84 ~ 87 |
| 5s | 22 | 88 ~ 91 |
| 6s | 23 | 92 ~ 95 |
| 7s | 24 | 96 ~ 99 |
| 8s | 25 | 100 ~ 103 |
| 9s | 26 | 104 ~ 107 |
| 東 | 27 | 108 ~ 111 |
| 南 | 28 | 112 ~ 115 |
| 西 | 29 | 116 ~ 119 |
| 北 | 30 | 120 ~ 123 |
| 白 | 31 | 124 ~ 127 |
| 發 | 32 | 128 ~ 131 |
| 中 | 33 | 132 ~ 135 |

## 使い方
### `Hai`系クラス
牌の集合を表現するクラスです。

#### `Hai34Counter`クラス
牌の集合を表現するクラスです。同じ種類の牌の区別をしません。

長さ34の配列で牌の集合を表現します。配列のインデックスが牌の種類(34インデックス牌番号)に、値が牌の枚数に対応しています。

以下のようにしてインスタンスを生成します。引数はint型の配列です。
```python
from kago_utils.hai import Hai34Counter

hai34_counter = Hai34Counter([
    1, 1, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 1,
    3, 2, 0, 0, 0, 0, 0
])
```

#### `Hai34List`クラス
牌の集合を表現するクラスです。同じ種類の牌の区別をしません。

可変長の配列で牌の集合を表現します。配列の値が牌そのものに対応しています。牌の種類は34インデックス牌番号で表現します。

以下のようにしてインスタンスを生成します。引数はint型の配列です。
```python
from kago_utils.hai import Hai34List

hai34_list = Hai34List([0, 1, 2, 12, 13, 14, 24, 25, 26, 27, 27, 27, 28, 28])
```

#### `Hai34String`クラス
牌の集合を表現するクラスです。同じ種類の牌の区別をしません。

文字列で牌の集合を表現します。フォーマットは[天鳳の牌理](https://tenhou.net/2/)とほぼ同じです。赤牌だけは未対応です。

以下のようにしてインスタンスを生成します。引数はstr型です。
```python
from kago_utils.hai import Hai34String

hai34_string = Hai34String("123m456p789s11122z")
```

#### `Hai136Counter`クラス
牌の集合を表現するクラスです。同じ種類の牌の区別をします。

`Hai34Counter`クラスの136インデックス牌番号版です。

以下のようにしてインスタンスを生成します。引数はint型の配列です。
```python
from kago_utils.hai import Hai136Counter

hai136_counter = Hai136Counter([
    1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
    1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
])
```

#### `Hai136List`クラス
牌の集合を表現するクラスです。同じ種類の牌の区別をします。

`Hai34List`クラスの136インデックス牌番号版です。

以下のようにしてインスタンスを生成します。引数はint型の配列です。
```python
from kago_utils.hai import Hai136List

hai136_list = Hai136List([0, 4, 8, 48, 52, 56, 96, 100, 104, 108, 109, 110, 112, 113])
```

#### `Hai`系クラスのデータの取得
`data`メンバでデータを取得できます。
```python
from kago_utils.hai import Hai34List, Hai34String

hai34_list = Hai34List([0, 1, 2, 12, 13, 14, 24, 25, 26, 27, 27, 27, 28, 28])
hai34_string = Hai34String("123m456p789s11122z")

print(hai34_list.data)
# [0, 1, 2, 12, 13, 14, 24, 25, 26, 27, 27, 27, 28, 28]

print(hai34_string.data)
# 123m456p789s11122z
```

#### `Hai`系クラスから`Hai`系クラスへの変換
`to_hai34_counter`、`to_hai34_list`、`to_hai34_string`、`to_hai136_counter`、`to_hai136_list`メソッドを使うことでそれぞれのクラスに変換することができます。

ただし、`Hai34`系のクラスから`Hai136`系のクラスへの変換はできない仕様になっています。
```python
from kago_utils.hai import Hai34Counter, Hai34List, Hai34String, Hai136Counter

hai34_counter = Hai34Counter([
    1, 1, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 1,
    3, 2, 0, 0, 0, 0, 0
])
hai34_list = Hai34List([0, 1, 2, 12, 13, 14, 24, 25, 26, 27, 27, 27, 28, 28])
hai34_string = Hai34String("123m456p789s11122z")
hai136_counter = Hai136Counter([
    1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
    1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
])

print(hai34_counter.to_hai34_list())
# [Hai34List] [0, 1, 2, 12, 13, 14, 24, 25, 26, 27, 27, 27, 28, 28]

print(hai34_list.to_hai34_string())
# [Hai34String] 123m456p789s11122z

print(hai136_counter.to_hai34_string())
# [Hai34String] 123m456p789s11122z

print(hai136_counter.to_hai136_list())
# [Hai136List] [0, 4, 8, 48, 52, 56, 96, 100, 104, 108, 109, 110, 112, 113]
```

#### 加算
`Hai`系のクラス同士は加算することができます。

`Hai34Counter`や`Hai34String`のようにクラスが異なっていても加算ができます。

異なるクラス同士の加算をすると結果のクラスは左辺のクラスと同じになります。

ただし、左辺が`Hai136`系、右辺が`Hai34`系の場合は加算できません。

```python
from kago_utils.hai import (Hai34Counter, Hai34List, Hai34String,
                            Hai136Counter, Hai136List)

a = Hai34List([0, 1, 2]) + Hai34String("123m")
print(a)
# [Hai34List] [0, 0, 1, 1, 2, 2]

b = Hai34Counter([1, 1, 1] + [0] * 31) + Hai136List([0, 4, 8])
print(b)
# [Hai34Counter] [2, 2, 2, 0, 0, ...]

c = Hai136Counter([1, 0, 0, 0] + [0] * 132) + Hai136List([1, 2, 3])
print(c)
# [Hai136Counter] [1, 1, 1, 1, 0, ...]

d = Hai136List([0, 1, 4, 5, 8, 10]) + Hai34String('123m')
# TypeError: unsupported operand type(s) for +: 'Hai136List' and 'Hai34String'
```

#### 減算
`Hai`系のクラス同士は減算することができます。

`Hai34Counter`や`Hai34String`のようにクラスが異なっていても減算ができます。

異なるクラス同士の減算をすると結果のクラスは左辺のクラスと同じになります。

ただし、左辺が`Hai136`系、右辺が`Hai34`系の場合は減算できません。

```python
from kago_utils.hai import Hai34Counter, Hai34List, Hai34String, Hai136Counter, Hai136List

a = Hai34List([0, 1, 2]) - Hai34String("12m")
print(a)
# [Hai34List] [2]

b = Hai34Counter([1, 1, 1] + [0] * 31) - Hai136List([4, 8])
print(b)
# [Hai34Counter] [1, 0, 0, 0, 0, ...]

c = Hai136Counter([1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0] + [0] * 124) - Hai136List([4, 8])
print(c)
# [Hai136Counter] [1, 0, 0, 0, 0, ...]

d = Hai136List([0, 1, 4, 5, 8, 10]) - Hai34String('123m')
# TypeError: unsupported operand type(s) for -: 'Hai136List' and 'Hai34String'
```

### Shantenクラス
向聴数や有効牌を計算するクラスです。

#### インスタンス化
引数は`Hai`系クラスのインスタンスである必要があります。
```python
from kago_utils.hai import Hai34String
from kago_utils.shanten import Shanten

jun_tehai = Hai34String("167m699p16s122345z")
shanten = Shanten(jun_tehai)
```

#### 向聴数の取得
`shanten`メンバで向聴数を取得できます。

向聴数の計算は初回のみ行われ、以降は結果をキャッシュしています。

```python
from kago_utils.hai import Hai34String
from kago_utils.shanten import Shanten

jun_tehai = Hai34String("167m699p16s122345z")
shanten = Shanten(jun_tehai)
print(shanten.shanten)
# 4
```

一般形、七対子形、国士無双形の向聴数を個別に取得したい場合はそれぞれ`regular_shanten`、`chiitoitsu_shanten`、`kokushimusou_shanten`メンバを使います。
```python
from kago_utils.hai import Hai34String
from kago_utils.shanten import Shanten

jun_tehai = Hai34String("167m699p16s122345z")
shanten = Shanten(jun_tehai)
print(shanten.regular_shanten, shanten.chiitoitsu_shanten, shanten.kokushimusou_shanten)
# 5 4 4
```

#### 有効牌の取得
`yuukouhai`メンバで有効牌を取得できます。

有効牌の計算は初回のみ行われ、以降は結果をキャッシュしています。

```python
from kago_utils.hai import Hai34String
from kago_utils.shanten import Shanten

jun_tehai = Hai34String("67m699p16s122345z")
shanten = Shanten(jun_tehai)
print(shanten.yuukouhai)
# [Hai34String] 67m6p16s1345z
