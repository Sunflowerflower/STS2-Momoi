# -*- coding: utf-8 -*-
"""批次14：若干 power 的文本 / 叠加语义规范化。

用法：python _batch14_text.py [--dry]
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
LOC = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "localization")

P = {
    "MINESWEEPER_POWER": (
        "当你下[blue]{Amount}[/blue]次抽到[gold]炸弹[/gold]时，将其直接打出。",
        "The next [blue]{Amount}[/blue] times you draw [gold]The Bomb[/gold], play it immediately.",
    ),
    "WIN_ENERGY_POWER": (
        "下[blue]{Amount}[/blue]个回合结束时，多余的能量可以留到下一回合。",
        "At the end of each of the next [blue]{Amount}[/blue] turns, leftover Energy carries over to the next turn.",
    ),
    "SHOW_MY_STRENGTH_POWER": (
        "你每打出[blue]10[/blue]张牌时，获得{EnergyPer:energyIcons()}。",
        "Every [blue]10[/blue] cards you play, gain {EnergyPer:energyIcons()}.",
    ),
    "MY_TURN_POWER": (
        "下[blue]{Amount}[/blue]个回合结束时，额外获得一回合。",
        "At the end of each of the next [blue]{Amount}[/blue] turns, take an extra turn.",
    ),
    "SNAKE_GAME_POWER": (
        "每当你打出一张牌时，随机化[gold]{MaulName}[/gold]，[gold]{SnakeName}[/gold]和[gold]{FireName}[/gold]的耗能。",
        "Whenever you play a card, randomize the cost of [gold]{MaulName}[/gold], [gold]{SnakeName}[/gold], "
        "and [gold]{FireName}[/gold].",
    ),
    "SNAKE_GAME_UPGRADED_POWER": (
        "每当你打出一张牌时，随机化[gold]{MaulName}[/gold]，[gold]{SnakeName}[/gold]和[gold]{FireName}[/gold]的耗能。",
        "Whenever you play a card, randomize the cost of [gold]{MaulName}[/gold], [gold]{SnakeName}[/gold], "
        "and [gold]{FireName}[/gold].",
    ),
    "PARKOUR_POWER": (
        "在你的回合开始时，从[blue]5[/blue]张随机特定牌中选择一张放入你的[gold]手牌[/gold]，"
        "直至你受到未被[gold]格挡[/gold]的伤害或失去生命。这张牌在本回合可以被免费打出。",
        "At the start of your turn, choose 1 of [blue]5[/blue] random specific cards and add it to your [gold]Hand[/gold], "
        "until you take unblocked damage or lose HP. That card costs nothing this turn.",
    ),
    "PARKOUR_UPGRADED_POWER": (
        "在你的回合开始时，从[blue]5[/blue]张[gold]升级[/gold]过的随机特定牌中选择一张放入你的[gold]手牌[/gold]，"
        "直至你受到未被[gold]格挡[/gold]的伤害或失去生命。这张牌在本场战斗可以被免费打出。",
        "At the start of your turn, choose 1 of [blue]5[/blue] random upgraded specific cards and add it to your "
        "[gold]Hand[/gold], until you take unblocked damage or lose HP. That card costs nothing this combat.",
    ),
}

# 贪吃蛇的话术说明里，卡名走 StringVar，所以中英同键即可。
NEW_TITLES = {
    "SNAKE_GAME_UPGRADED_POWER": ("贪吃蛇", "Snake Game"),
    "PARKOUR_UPGRADED_POWER": ("跑酷", "Parkour"),
}

# 力量（本回合）：KotamaStrengthPower 继承原版 TemporaryStrengthPower，
# 而原版基类把 Title 指向 OriginModel（= 卡「来自小玉的协助」）、Description 指向
# 硬编码的 TEMPORARY_STRENGTH_POWER.* ，所以这几个键永远不会被读到 —— 死键，删掉。
DEAD_KEYS = [
    "STS2_MOMOI_POWER_KOTAMA_STRENGTH_POWER.title",
    "STS2_MOMOI_POWER_KOTAMA_STRENGTH_POWER.description",
    "STS2_MOMOI_POWER_KOTAMA_STRENGTH_POWER.smartDescription",
]


def main():
    total = 0
    removed = 0
    for i, lang in enumerate(("zhs", "eng")):
        p = os.path.join(LOC, lang, "powers.json")
        d = json.load(open(p, encoding="utf-8"), object_pairs_hook=dict)
        n = 0
        for key, pair in P.items():
            full = "STS2_MOMOI_POWER_" + key
            for suf in (".description", ".smartDescription"):
                k = full + suf
                # 不存在的键也要创建（新增的升级版 power 需要全新的词条）。
                if d.get(k) != pair[i]:
                    d[k] = pair[i]
                    n += 1
        for key, pair in NEW_TITLES.items():
            k = "STS2_MOMOI_POWER_" + key + ".title"
            if d.get(k) != pair[i]:
                d[k] = pair[i]
                n += 1
        for k in DEAD_KEYS:
            if d.pop(k, None) is not None:
                removed += 1
        if not DRY:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write("\n")
        print("[%s] powers: %d 条" % (lang, n))
        total += n

    print("\n共改动 %d 条，删除死键 %d 个%s" % (total, removed, "（--dry，未写盘）" if DRY else ""))


if __name__ == "__main__":
    main()
