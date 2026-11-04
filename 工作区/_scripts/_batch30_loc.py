# -*- coding: utf-8 -*-
"""批次30 本地化：专注合成一句（卡面 + power）、天马行空升级版补「+1」。"""
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
    # 专注：两句并成一句（「A/B，X/Y」的样式）
    "STS2_MOMOI_CARD_FOCUS.description": {
        "zhs": "在你的回合结束时，若你本回合没有打出过[gold]小游戏牌[/gold]/[gold]构想[/gold]，"
               "使[gold]构想[/gold]数值+1/选择最多[gold]构想[/gold]数值张牌[gold]保留[/gold]。",
        "eng": "At the end of your turn, if you have not played a [gold]Minigame[/gold] card / a [gold]Concept[/gold] "
               "this turn, increase your [gold]Concept[/gold] number by 1 / choose up to your [gold]Concept[/gold] "
               "number of cards to [gold]Retain[/gold].",
    },
    # 天马行空：升级版补 +1（升级前不动）
    "STS2_MOMOI_CARD_BULLET_RAIN.description": {
        "zhs": "对所有敌人造成{CalculatedDamage:diff()}点伤害。\n"
               "额外攻击等同[gold]构想[/gold]数值{IfUpgraded:show:+1|}次。（额外攻击{ExtraHits:diff()}次）",
        "eng": "Deal {CalculatedDamage:diff()} damage to ALL enemies.\n"
               "[gold]Attack[/gold] {ExtraHits:diff()} extra time(s), equal to your [gold]Concept[/gold] "
               "count{IfUpgraded:show: +1|}.",
    },
}
POWERS = {
    # 专注 power：同样并成一句；构想数值仍用 {RetainCount} 显示实际数值
    "STS2_MOMOI_POWER_FOCUS_POWER.description": {
        "zhs": "在你的回合结束时，若你本回合没有打出过[gold]小游戏牌[/gold]/[gold]构想[/gold]，"
               "使[gold]构想[/gold]数值+[blue]{Amount}[/blue]/选择最多[blue]{RetainCount}[/blue]张牌[gold]保留[/gold]。",
        "eng": "At the end of your turn, if you have not played a [gold]Minigame[/gold] card / a [gold]Concept[/gold] "
               "this turn, increase your [gold]Concept[/gold] number by [blue]{Amount}[/blue] / choose up to "
               "[blue]{RetainCount}[/blue] cards to [gold]Retain[/gold].",
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
pz = load("zhs", "powers")[1]
print("\n复核：")
print("  专注 z:", cz["STS2_MOMOI_CARD_FOCUS.description"])
print("  专注 power z:", pz["STS2_MOMOI_POWER_FOCUS_POWER.description"])
print("  天马行空 z:", cz["STS2_MOMOI_CARD_BULLET_RAIN.description"].replace("\n", " / "))
