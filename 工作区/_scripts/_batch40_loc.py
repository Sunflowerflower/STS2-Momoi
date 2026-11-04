# -*- coding: utf-8 -*-
"""批次40 本地化：创作的痛苦/瓶颈突破/博览群游 文本 + 新卡「传送门悖论」「过载」（卡 + power）。"""
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
    # 创作的痛苦：第一行新增「获得火力」
    "STS2_MOMOI_CARD_CREATIVE_PAIN.description": {
        "zhs": "获得{Firepower:diff()}层[gold]火力[/gold]。\n对所有敌人造成{CalculatedDamage:diff()}点伤害3次。\n"
               "给予所有敌人{Burn:diff()}层[gold]灼烧[/gold]。\n"
               "每当你打出[gold]构想[/gold]时，此牌的耗能将在下一次打出前减少{CostReduce:energyIcons()}。",
        "eng": "Gain {Firepower:diff()} [gold]Firepower[/gold].\nDeal {CalculatedDamage:diff()} damage to ALL enemies 3 times.\n"
               "Apply {Burn:diff()} [gold]Burn[/gold] to ALL enemies.\n"
               "Whenever you play a [gold]Concept[/gold], this card costs {CostReduce:energyIcons()} less until its next play.",
    },
    # 瓶颈突破：构想 +1/2
    "STS2_MOMOI_CARD_BOTTLENECK_BREAK.description": {
        "zhs": "造成{CalculatedDamage:diff()}点伤害{Hits:diff()}次。\n使[gold]构想[/gold]数值+{ConceptGain:diff()}。",
        "eng": "Deal {CalculatedDamage:diff()} damage {Hits:diff()} times.\nIncrease your [gold]Concept[/gold] number by {ConceptGain:diff()}.",
    },
    # 博览群游：随机敌人
    "STS2_MOMOI_CARD_EXPERIENCE_COMBO.description": {
        "zhs": "本场战斗中每打出过一张[gold]小游戏牌[/gold]，就随机对敌人造成{CalculatedDamage:diff()}点伤害。（攻击{CalculatedHits:diff()}次）",
        "eng": "Deal {CalculatedDamage:diff()} damage to a random enemy for each [gold]Minigame[/gold] card played this combat. "
               "(Attacks {CalculatedHits:diff()} times)",
    },
    # 新卡：传送门悖论
    "STS2_MOMOI_CARD_PORTAL_PARADOX.title": {"zhs": "传送门悖论", "eng": "Portal Paradox"},
    "STS2_MOMOI_CARD_PORTAL_PARADOX.description": {
        "zhs": "从两张牌中选择一张加入你的[gold]手牌[/gold]。",
        "eng": "Choose 1 of 2 cards to add to your [gold]Hand[/gold].",
    },
    "STS2_MOMOI_CARD_PORTAL_PARADOX.flavor": {"zhs": "", "eng": ""},
    # 新卡：过载
    "STS2_MOMOI_CARD_OVERLOAD.title": {"zhs": "过载", "eng": "Overload"},
    "STS2_MOMOI_CARD_OVERLOAD.description": {
        "zhs": "获得{Firepower:diff()}层[gold]火力[/gold]。\n每当你的[gold]火力[/gold]层数减少时，获得{Vigor:diff()}点[gold]活力[/gold]。",
        "eng": "Gain {Firepower:diff()} [gold]Firepower[/gold].\nWhenever your [gold]Firepower[/gold] decreases, gain {Vigor:diff()} [gold]Vigor[/gold].",
    },
    "STS2_MOMOI_CARD_OVERLOAD.flavor": {"zhs": "", "eng": ""},
}
POWERS = {
    "STS2_MOMOI_POWER_OVERLOAD_POWER.title": {"zhs": "过载", "eng": "Overload"},
    "STS2_MOMOI_POWER_OVERLOAD_POWER.description": {
        "zhs": "每当你的[gold]火力[/gold]层数减少时，获得[blue]{Amount}[/blue]点[gold]活力[/gold]。",
        "eng": "Whenever your [gold]Firepower[/gold] decreases, gain [blue]{Amount}[/blue] [gold]Vigor[/gold].",
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
print("\n创作痛苦:", cz["STS2_MOMOI_CARD_CREATIVE_PAIN.description"].replace("\n", " / ")[:120])
print("瓶颈:", cz["STS2_MOMOI_CARD_BOTTLENECK_BREAK.description"].replace("\n", " / "))
print("博览:", cz["STS2_MOMOI_CARD_EXPERIENCE_COMBO.description"])
print("传送门:", cz["STS2_MOMOI_CARD_PORTAL_PARADOX.description"])
print("过载:", cz["STS2_MOMOI_CARD_OVERLOAD.description"].replace("\n", " / "))
print("过载 power:", pz["STS2_MOMOI_POWER_OVERLOAD_POWER.description"])
