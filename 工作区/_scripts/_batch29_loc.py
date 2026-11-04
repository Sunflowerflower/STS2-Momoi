# -*- coding: utf-8 -*-
"""批次29 本地化：专注重做文本、跑酷删后半段、专注 power 文本。"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

LOC = r"C:\Users\asus\RiderProjects\STS2 Momoi\STS2 Momoi\STS2_Momoi\localization"


def load(lang, table):
    p = os.path.join(LOC, lang, table + ".json")
    return p, json.load(open(p, encoding="utf-8"), object_pairs_hook=dict)


def save(p, d):
    open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")


CARDS = {
    # 专注：连续 2 回合 -> 本回合；0 费
    "STS2_MOMOI_CARD_FOCUS.description": {
        "zhs": "在你的回合结束时，若你本回合没有打出过[gold]小游戏牌[/gold]，使[gold]构想[/gold]数值+1。\n"
               "在你的回合结束时，若你本回合没有打出过[gold]构想[/gold]，可选择最多[gold]构想[/gold]数值张"
               "[gold]手牌[/gold][gold]保留[/gold]。",
        "eng": "At the end of your turn, if you have not played a [gold]Minigame[/gold] card this turn, "
               "increase your [gold]Concept[/gold] number by 1.\n"
               "At the end of your turn, if you have not played a [gold]Concept[/gold] this turn, "
               "you may choose up to your [gold]Concept[/gold] number of cards in your [gold]Hand[/gold] to "
               "[gold]Retain[/gold].",
    },
    # 跑酷！：删掉「回合开始时重复」那句
    "STS2_MOMOI_CARD_PARKOUR.description": {
        "zhs": "从5张{IfUpgraded:show:升级过的|}随机特定卡牌中选择最多一张放入你的[gold]手牌[/gold]，"
               "这张牌在本{IfUpgraded:show:场战斗|回合}可以被免费打出。",
        "eng": "Choose up to 1 of 5 {IfUpgraded:show:Upgraded |}random specific cards to add to your "
               "[gold]Hand[/gold]; it can be played for free this {IfUpgraded:show:combat|turn}.",
    },
}
POWERS = {
    "STS2_MOMOI_POWER_FOCUS_POWER.description": {
        "zhs": "若你本回合没有打出过小游戏牌，在你的回合结束时使[gold]构想[/gold]数值+[blue]{Amount}[/blue]；"
               "若你本回合没有打出过[gold]构想[/gold]，在你的回合结束时可选择最多[blue]{RetainCount}[/blue]张"
               "[gold]手牌[/gold][gold]保留[/gold]。",
        "eng": "If you have not played a Minigame card this turn, increase your [gold]Concept[/gold] number by "
               "[blue]{Amount}[/blue] at the end of your turn; if you have not played a [gold]Concept[/gold] this "
               "turn, you may choose up to [blue]{RetainCount}[/blue] cards in your [gold]Hand[/gold] to "
               "[gold]Retain[/gold] at the end of your turn.",
    },
}
for base in list(CARDS):
    if base.endswith(".description"):
        CARDS[base.replace(".description", ".smartDescription")] = CARDS[base]
for base in list(POWERS):
    if base.endswith(".description"):
        POWERS[base.replace(".description", ".smartDescription")] = POWERS[base]

n = 0
for table, entries in (("cards", CARDS), ("powers", POWERS)):
    for key, per in entries.items():
        for lang, txt in per.items():
            p, d = load(lang, table)
            if d.get(key) != txt:
                d[key] = txt
                save(p, d)
                n += 1
print("本地化更新 %d 条" % n)

cz = load("zhs", "cards")[1]
ce = load("eng", "cards")[1]
pz = load("zhs", "powers")[1]
print("\n复核：")
print("  专注 z:", cz["STS2_MOMOI_CARD_FOCUS.description"].replace("\n", " / "))
print("  专注 power z:", pz["STS2_MOMOI_POWER_FOCUS_POWER.description"])
print("  跑酷 z:", cz["STS2_MOMOI_CARD_PARKOUR.description"])
print("  跑酷 eng 无 repeat:", "repeat" not in ce["STS2_MOMOI_CARD_PARKOUR.description"].lower())
print("  power 里还有「连续」吗:", "连续" in pz["STS2_MOMOI_POWER_FOCUS_POWER.description"])
