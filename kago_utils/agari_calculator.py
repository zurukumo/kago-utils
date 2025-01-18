from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from kago_utils.actions import Ankan, Chii, Daiminkan, Kakan, Pon
from kago_utils.hai import Hai
from kago_utils.hai_group import HaiGroup
from kago_utils.player import Player
from kago_utils.tehai_decomposer import TehaiBlock, TehaiDecomposer

if TYPE_CHECKING:
    from kago_utils.game import Game


class AgariCalculator:
    YAOCHUHAI = (0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33)
    YAKU = (
        "門前清自摸和",
        "立直",
        "一発",
        "槍槓",
        "嶺上開花",
        "海底摸月",
        "河底撈魚",
        "平和",
        "断幺九",
        "一盃口",
        "自風 東",
        "自風 南",
        "自風 西",
        "自風 北",
        "場風 東",
        "場風 南",
        "場風 西",
        "場風 北",
        "役牌 白",
        "役牌 發",
        "役牌 中",
        "両立直",
        "七対子",
        "混全帯幺九",
        "一気通貫",
        "三色同順",
        "三色同刻",
        "三槓子",
        "対々和",
        "三暗刻",
        "小三元",
        "混老頭",
        "二盃口",
        "純全帯幺九",
        "混一色",
        "清一色",
        "天和",
        "地和",
        "大三元",
        "四暗刻",
        "四暗刻単騎",
        "字一色",
        "緑一色",
        "清老頭",
        "九蓮宝燈",
        "純正九蓮宝燈",
        "国士無双",
        "国士無双13面",
        "大四喜",
        "小四喜",
        "四槓子",
        "ドラ",
        "裏ドラ",
        "赤ドラ",
    )

    player: Player
    game: Game
    is_daburon: bool

    juntehai: HaiGroup
    huuros: list[Chii | Pon | Kakan | Daiminkan | Ankan]
    zentehai: HaiGroup

    is_tsumoho: bool
    agari_hai: Hai
    from_who: int

    yaku: dict[str, int]
    ten: int
    han: int
    hu: int
    ten_movement: list[int]

    __slots__ = (
        "player",
        "game",
        "is_daburon",
        "juntehai",
        "huuros",
        "agari_hai",
        "from_who",
        "zentehai",
        "is_tsumoho",
        "yaku",
        "ten",
        "han",
        "hu",
        "ten_movement",
    )

    def __init__(self, game: Game, player: Player, is_daburon: bool):
        self.game = game
        self.player = player
        self.is_daburon = is_daburon

        self.juntehai = copy.deepcopy(player.juntehai)
        self.huuros = copy.deepcopy(player.huuros)

        if game.last_teban == player.zaseki:
            if player.last_tsumo is None:
                raise Exception()

            self.agari_hai = player.last_tsumo
            self.from_who = player.zaseki
        else:
            if game.last_dahai is None or game.last_teban is None:
                raise Exception()

            self.juntehai += game.last_dahai
            self.agari_hai = game.last_dahai
            self.from_who = game.last_teban

        self.zentehai = copy.deepcopy(self.juntehai)
        for huuro in self.huuros:
            self.zentehai += huuro.hais

        self.is_tsumoho = self.player.zaseki == self.from_who

        self.calculate_agari()

    def calculate_agari(self) -> None:
        jokyo_yaku = self.get_jokyo_yaku()
        zenbu_yaku = self.get_zenbu_yaku()

        max_ten_han_hu = (0, 0, 0)
        max_yaku = dict()

        # Calculate ten for kokushimusou
        bubun_yaku_for_kokushimusou = self.get_bubun_yaku_for_kokushimusou()
        yaku = self.adjust_yaku(jokyo_yaku, zenbu_yaku, bubun_yaku_for_kokushimusou)
        if yaku is not None:
            han = sum(yaku.values())
            ten = self.calculate_ten(30, han)
            if (ten, han, 30) > max_ten_han_hu:
                max_ten_han_hu = (ten, han, 30)
                max_yaku = yaku

        # Calculate ten for chiitoitsu
        bubun_yaku_for_chiitoitsu = self.get_bubun_yaku_for_chiitoitsu()
        yaku = self.adjust_yaku(jokyo_yaku, zenbu_yaku, bubun_yaku_for_chiitoitsu)
        if yaku is not None:
            han = sum(yaku.values())
            ten = self.calculate_ten(25, han)
            if (ten, han, 25) > max_ten_han_hu:
                max_ten_han_hu = (ten, han, 25)
                max_yaku = yaku

        # Calculate ten for regular
        for decomposed_tehai in TehaiDecomposer(
            self.juntehai, self.huuros, self.agari_hai, self.is_tsumoho
        ).decompose():
            hu, is_pinhu = self.calculate_hu(decomposed_tehai)
            bubun_yaku = self.get_bubun_yaku_for_regular(decomposed_tehai, is_pinhu)

            yaku = self.adjust_yaku(jokyo_yaku, zenbu_yaku, bubun_yaku)
            if yaku is None:
                continue

            han = sum(yaku.values())
            ten = self.calculate_ten(hu, han)
            if (ten, han, hu) > max_ten_han_hu:
                max_ten_han_hu = (ten, han, hu)
                max_yaku = yaku

        self.yaku = max_yaku
        self.ten = max_ten_han_hu[0]
        self.han = max_ten_han_hu[1]
        self.hu = max_ten_han_hu[2]
        self.ten_movement = self.calculate_ten_movement(self.ten)

    def calculate_hu(self, blocks: list[TehaiBlock]) -> tuple[int, bool]:
        # Base hu
        hu = 20

        # Hu by blocks
        for block in blocks:
            if block.type == "jantou":
                if block.hais[0] == (self.player.zaseki - self.game.kyoku) % 4 + 27:
                    hu += 2
                if block.hais[0] == self.game.kyoku // 4 + 27:
                    hu += 2
                if 31 <= block.hais[0] <= 33:
                    hu += 2
            elif block.type == "koutsu":
                tmp = 2
                if block.hais[0] in AgariCalculator.YAOCHUHAI:
                    tmp *= 2
                if block.minan == "an":
                    tmp *= 2
                hu += tmp
            elif block.type == "kantsu":
                tmp = 8
                if block.hais[0] in AgariCalculator.YAOCHUHAI:
                    tmp *= 2
                if block.minan == "an":
                    tmp *= 2
                hu += tmp

        # Hu by machi type
        for block in blocks:
            # Tanki
            if block.type == "jantou" and block.agari_hai is not None:
                hu += 2
            # Penchan(123)
            if block.type == "shuntsu" and block.hais[0] % 9 == 0 and block.hais[2] == block.agari_hai:
                hu += 2
            # Penchan(789)
            if block.type == "shuntsu" and block.hais[2] % 9 == 8 and block.hais[0] == block.agari_hai:
                hu += 2
            # Kanchan
            if block.type == "shuntsu" and block.hais[1] == block.agari_hai:
                hu += 2

        is_pinhu = hu == 20 and self.player.is_menzen

        # Hu by agari type
        # Tsumo(exception for pinhu)
        if self.is_tsumoho and not is_pinhu:
            hu += 2
        # Menzen ron
        if not self.is_tsumoho and self.player.is_menzen:
            hu += 10

        # Adjust hu when it is kui pinhu
        if hu == 20 and not self.player.is_menzen:
            hu = 30

        hu = (hu + 9) // 10 * 10

        return hu, is_pinhu

    def calculate_ten(self, hu: int, han: int) -> int:
        ten: int = hu * pow(2, han + 2)

        # Adjust ten when it is over Mangan
        if ten >= 2000:
            if han >= 13:
                ten = 8000 * (han // 13)
            elif han >= 11:
                ten = 6000
            elif han >= 8:
                ten = 4000
            elif han >= 6:
                ten = 3000
            else:
                ten = 2000

        if self.player.is_oya:
            ten *= 6
        else:
            ten *= 4

        return (ten + 99) // 100

    def calculate_ten_movement(self, ten: int) -> list[int]:
        ten_movement = [0, 0, 0, 0]
        if self.is_tsumoho:
            # Tsumo and Pao
            if self.player.pao_sekinin_player is not None:
                ten_movement[self.player.zaseki] = ten + self.game.honba * 3 + self.game.kyoutaku * 10
                ten_movement[self.player.pao_sekinin_player.zaseki] = -ten - self.game.honba * 3

            # Tsumo by oya
            elif self.player.is_oya:
                for i in range(4):
                    if i == self.player.zaseki:
                        ten_movement[i] = -(-ten // 3) * 3 + (self.game.honba * 3) + (self.game.kyoutaku * 10)
                    else:
                        ten_movement[i] = -ten // 3 - self.game.honba

            # Tsumo by ko
            else:
                for i in range(4):
                    if i == self.player.zaseki:
                        ten_movement[i] += self.game.kyoutaku * 10
                    elif i == self.game.kyoku % 4:
                        ten_movement[i] = -ten // 2 - self.game.honba
                        ten_movement[self.player.zaseki] -= ten_movement[i]
                    else:
                        ten_movement[i] = -ten // 4 - self.game.honba
                        ten_movement[self.player.zaseki] -= ten_movement[i]

        else:
            # Ron and Pao (when houjuu player is not pao sekinin player)
            if self.player.pao_sekinin_player is not None and self.player.pao_sekinin_player.zaseki != self.from_who:
                ten_movement[self.player.zaseki] = ten
                ten_movement[self.from_who] = -ten // 2
                ten_movement[self.player.pao_sekinin_player.zaseki] = -ten // 2
                if not self.is_daburon:
                    ten_movement[self.player.zaseki] += self.game.honba * 3 + self.game.kyoutaku * 10
                    ten_movement[self.player.pao_sekinin_player.zaseki] -= self.game.honba * 3

            # Ron
            else:
                ten_movement[self.player.zaseki] = ten
                ten_movement[self.from_who] = -ten
                if not self.is_daburon:
                    ten_movement[self.player.zaseki] += self.game.honba * 3 + self.game.kyoutaku * 10
                    ten_movement[self.from_who] -= self.game.honba * 3

        ten_movement = [i * 100 for i in ten_movement]
        return ten_movement

    def get_jokyo_yaku(self) -> dict[str, int]:
        jokyo_yaku = AgariCalculator.initialize_yaku()

        # TODO: Not implemented yet
        return jokyo_yaku

    def get_zenbu_yaku(self) -> dict[str, int]:
        zenbu_yaku = AgariCalculator.initialize_yaku()
        counter = self.zentehai.to_counter34()
        total = sum(counter)

        if sum([counter[i] for i in AgariCalculator.YAOCHUHAI]) == 0:
            zenbu_yaku["断幺九"] = 1

        if sum([counter[i] for i in AgariCalculator.YAOCHUHAI]) == total:
            zenbu_yaku["混老頭"] = 2

        if (
            sum(counter[0:9]) + sum(counter[27:34]) == total
            or sum(counter[9:18]) + sum(counter[27:34]) == total
            or sum(counter[18:27]) + sum(counter[27:34]) == total
        ):
            zenbu_yaku["混一色"] = 2 + self.player.is_menzen

        if sum(counter[0:9]) == total or sum(counter[9:18]) == total or sum(counter[18:27]) == total:
            zenbu_yaku["清一色"] = 5 + self.player.is_menzen

        if sum(counter[27:34]) == total:
            zenbu_yaku["字一色"] = 13

        if sum([counter[i] for i in (19, 20, 21, 23, 25, 32)]) == total:
            zenbu_yaku["緑一色"] = 13

        if sum([counter[i] for i in (0, 8, 9, 17, 18, 26)]) == total:
            zenbu_yaku["清老頭"] = 13

        if len(self.huuros) == 0:
            for i in [0, 9, 18]:
                if counter[i] >= 3 and counter[i + 8] >= 3 and all(counter[i : i + 9]):
                    zenbu_yaku["九蓮宝燈"] = 13

        if len(self.huuros) == 0:
            for i in [0, 9, 18]:
                if (
                    counter[i] >= 3
                    and counter[i + 8] >= 3
                    and all(counter[i : i + 9])
                    and counter[self.agari_hai.id // 4] in [2, 4]
                ):
                    zenbu_yaku["純正九蓮宝燈"] = 13

        return zenbu_yaku

    # 部分役
    def get_bubun_yaku_for_regular(self, blocks: list[TehaiBlock], is_pinhu: bool) -> dict[str, int]:
        bubun_yaku = AgariCalculator.initialize_yaku()

        # Toistu, Shuntsu, Koutsu and Kantsu pattern counter
        tp = [0] * 34  # Toitsu pattern
        sp = [0] * 21  # Shuntsu pattern
        kp = [0] * 34  # Koutsu and Kantsu pattern
        for block in blocks:
            if block.type == "jantou":
                tp[block.hais[0]] += 1
            elif block.type == "shuntsu":
                sp[block.hais[0] // 9 * 7 + block.hais[0] % 9] += 1
            elif block.type in ("koutsu", "kantsu"):
                kp[block.hais[0]] += 1

        if is_pinhu:
            bubun_yaku["平和"] = 1

        if self.player.is_menzen and sum(c >= 2 for c in sp) == 1:
            bubun_yaku["一盃口"] = 1

        if self.player.jikaze == "東" and kp[27]:
            bubun_yaku["自風 東"] = 1
        if self.player.jikaze == "南" and kp[28]:
            bubun_yaku["自風 南"] = 1
        if self.player.jikaze == "西" and kp[29]:
            bubun_yaku["自風 西"] = 1
        if self.player.jikaze == "北" and kp[30]:
            bubun_yaku["自風 北"] = 1

        if self.game.bakaze == "東" and kp[27]:
            bubun_yaku["場風 東"] = 1
        if self.game.bakaze == "南" and kp[28]:
            bubun_yaku["場風 南"] = 1
        if self.game.bakaze == "西" and kp[29]:
            bubun_yaku["場風 西"] = 1
        if self.game.bakaze == "北" and kp[30]:
            bubun_yaku["場風 北"] = 1

        if kp[31]:
            bubun_yaku["役牌 白"] = 1
        if kp[32]:
            bubun_yaku["役牌 發"] = 1
        if kp[33]:
            bubun_yaku["役牌 中"] = 1

        if sum(tp[i] + kp[i] for i in AgariCalculator.YAOCHUHAI) + sum(sp[i] for i in (0, 6, 7, 13, 14, 20)) == 5:
            bubun_yaku["混全帯幺九"] = 1 + self.player.is_menzen

        if (sp[0] and sp[3] and sp[6]) or (sp[7] and sp[10] and sp[13]) or (sp[14] and sp[17] and sp[20]):
            bubun_yaku["一気通貫"] = 1 + self.player.is_menzen

        for i in range(7):
            if sp[i] and sp[i + 7] and sp[i + 14]:
                bubun_yaku["三色同順"] = 1 + self.player.is_menzen
                break

        for i in range(9):
            if kp[i] and kp[i + 9] and kp[i + 18]:
                bubun_yaku["三色同刻"] = 2
                break

        if sum(b.type == "kantsu" for b in blocks) == 3:
            bubun_yaku["三槓子"] = 2

        if sum(b.type in ("koutsu", "kantsu") for b in blocks) == 4:
            bubun_yaku["対々和"] = 2

        if sum(b.type in ("koutsu", "kantsu") and b.minan == "an" for b in blocks) == 3:
            bubun_yaku["三暗刻"] = 2

        if kp[31] + kp[32] + kp[33] == 2 and tp[31] + tp[32] + tp[33] == 1:
            bubun_yaku["小三元"] = 2

        if self.player.is_menzen and sum(c >= 2 for c in sp) == 2:
            bubun_yaku["二盃口"] = 3

        if sum(tp[i] + kp[i] for i in (0, 8, 9, 17, 18, 26)) + sum(sp[i] for i in (0, 6, 7, 13, 14, 20)) == 5:
            bubun_yaku["純全帯幺九"] = 2 + self.player.is_menzen

        if kp[31] and kp[32] and kp[33]:
            bubun_yaku["大三元"] = 13

        if sum(b.type in ("koutsu", "kantsu") and b.minan == "an" for b in blocks) == 4:
            bubun_yaku["四暗刻"] = 13

        if (
            sum(b.type in ("koutsu", "kantsu") and b.minan == "an" for b in blocks) == 4
            and sum(b.type == "jantou" and b.agari_hai is not None for b in blocks) == 1
        ):
            bubun_yaku["四暗刻単騎"] = 13

        if kp[27] and kp[28] and kp[29] and kp[30]:
            bubun_yaku["大四喜"] = 13

        if (kp[27] + kp[28] + kp[29] + kp[30] == 3) and (tp[27] + tp[28] + tp[29] + tp[30] == 1):
            bubun_yaku["小四喜"] = 13

        if sum(block.type == "kantsu" for block in blocks) == 4:
            bubun_yaku["四槓子"] = 13

        return bubun_yaku

    def get_bubun_yaku_for_kokushimusou(self) -> dict[str, int]:
        bubun_yaku = AgariCalculator.initialize_yaku()
        counter = self.juntehai.to_counter34()

        if all(counter[i] in [1, 2] for i in AgariCalculator.YAOCHUHAI):
            bubun_yaku["国士無双"] = 13

        if all(counter[i] in [1, 2] for i in AgariCalculator.YAOCHUHAI) and counter[self.agari_hai.id // 4] == 2:
            bubun_yaku["国士無双13面"] = 13

        return bubun_yaku

    def get_bubun_yaku_for_chiitoitsu(self) -> dict[str, int]:
        bubun_yaku = AgariCalculator.initialize_yaku()
        counter = self.juntehai.to_counter34()

        if sum(counter[i] == 2 for i in range(34)) == 7:
            bubun_yaku["七対子"] = 2

        return bubun_yaku

    def adjust_yaku(
        self,
        jokyo_yaku: dict[str, int],
        zenbu_yaku: dict[str, int],
        bubun_yaku: dict[str, int],
    ) -> dict[str, int] | None:
        yaku = AgariCalculator.initialize_yaku()
        for key in yaku.keys():
            yaku[key] = jokyo_yaku[key] + zenbu_yaku[key] + bubun_yaku[key]

        # When there are yakuman, remove other yaku
        if any(v >= 13 for v in yaku.values()):
            yaku = dict((k, v) if v >= 13 else (k, 0) for k, v in yaku.items())

        # Remove yaku that cannot be combined
        if yaku["両立直"]:
            yaku["立直"] = 0
        if yaku["混老頭"]:
            yaku["純全帯幺九"] = 0
            yaku["混全帯幺九"] = 0
        if yaku["純全帯幺九"]:
            yaku["混全帯幺九"] = 0
        if yaku["清一色"]:
            yaku["混一色"] = 0
        if yaku["国士無双13面"]:
            yaku["国士無双"] = 0
        if yaku["四暗刻単騎"]:
            yaku["四暗刻"] = 0
        if yaku["純正九蓮宝燈"]:
            yaku["九蓮宝燈"] = 0

        # When there are only dora, uradora, and akadora, return None
        if yaku["ドラ"] + yaku["裏ドラ"] + yaku["赤ドラ"] == sum(yaku.values()):
            return None

        return yaku

    @classmethod
    def initialize_yaku(cls) -> dict[str, int]:
        return dict((yaku, 0) for yaku in cls.YAKU)
