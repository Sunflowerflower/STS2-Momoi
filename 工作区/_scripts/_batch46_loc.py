# -*- coding: utf-8 -*-
"""批次46 本地化：括号内容改「仅局内显示」、矛与盾 11/15、开荒侧栏、相遇关键词染金。"""
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
    # 火力爆发：括号只在局内显示
    "STS2_MOMOI_CARD_FIREPOWER_STRIKE.description": {
        "zhs": "造成{CalculatedDamage:diff()}点伤害。\n本场战斗中你每获得过1层[gold]火力[/gold]，伤害+{IfUpgraded:show:4|3}。\n"
               "{InCombat:（已获得过{FirepowerGained:diff()}层）|}",
        "eng": "Deal {CalculatedDamage:diff()} damage.\nFor each [gold]Firepower[/gold] gained this combat, this deals "
               "+{IfUpgraded:show:4|3} more damage.\n{InCombat:(Gained {FirepowerGained:diff()} so far)|}",
    },
    # 剧本打击：括号只在局内显示
    "STS2_MOMOI_CARD_SCRIPT_STRIKE.description": {
        "zhs": "造成{CalculatedDamage:diff()}点伤害。\n抽等同[gold]构想[/gold]数值{IfUpgraded:show:+1|}张牌。\n"
               "{InCombat:（抽{ConceptCards:diff()}张牌）|}",
        "eng": "Deal {CalculatedDamage:diff()} damage.\nDraw cards equal to your [gold]Concept[/gold] count"
               "{IfUpgraded:show:+1|}.\n{InCombat:(Draw {ConceptCards:diff()} cards)|}",
    },
    # 天马行空：括号只在局内显示
    "STS2_MOMOI_CARD_BULLET_RAIN.description": {
        "zhs": "对所有敌人造成{CalculatedDamage:diff()}点伤害。\n"
               "额外攻击等同[gold]构想[/gold]数值{IfUpgraded:show:+1|}次。{InCombat:（额外攻击{ExtraHits:diff()}次）|}",
        "eng": "Deal {CalculatedDamage:diff()} damage to ALL enemies.\n"
               "[gold]Attack[/gold] {ExtraHits:diff()} extra time(s), equal to your [gold]Concept[/gold] "
               "count{IfUpgraded:show: +1|}.{InCombat: (Attacks {ExtraHits:diff()} extra times)|}",
    },
    # 博览群游：括号只在局内显示
    "STS2_MOMOI_CARD_EXPERIENCE_COMBO.description": {
        "zhs": "本场战斗中每打出过一张[gold]小游戏牌[/gold]，就随机对敌人造成{CalculatedDamage:diff()}点伤害。"
               "{InCombat:（攻击{CalculatedHits:diff()}次）|}",
        "eng": "Deal {CalculatedDamage:diff()} damage to a random enemy for each [gold]Minigame[/gold] card played this combat."
               "{InCombat: (Attacks {CalculatedHits:diff()} times)|}",
    },
    # 矛与盾：卡面伤害 8/11 -> 11/15
    "STS2_MOMOI_CARD_SPEAR_SHIELD.description": {
        "zhs": "当你打出[gold]构想[/gold]时，该[gold]构想[/gold]每有1点数值，就获得{IfUpgraded:show:8|6}点[gold]格挡[/gold]。\n"
               "在你的回合结束时，[gold]手牌[/gold]中每有一张[gold]构想[/gold]就对所有敌人造成{IfUpgraded:show:15|11}点伤害。",
        "eng": "Whenever you play a [gold]Concept[/gold], gain {IfUpgraded:show:8|6} [gold]Block[/gold] for each point of its number.\n"
               "At the end of your turn, deal {IfUpgraded:show:15|11} damage to ALL enemies for each [gold]Concept[/gold] in your [gold]Hand[/gold].",
    },
    # 开荒：卡面「未获得过」->「未生成过」
    "STS2_MOMOI_CARD_GRINDING.description": {
        "zhs": "获得{Energy:energyIcons()}。\n将1张本场战斗中未生成过的特定[red]诅咒[/red]加入你的[gold]弃牌堆[/gold]。",
        "eng": "Gain {Energy:energyIcons()}.\nAdd 1 specific [red]Curse[/red] you have not yet generated this combat to your [gold]Discard Pile[/gold].",
    },
    # 开荒：侧栏改成「将依次生成以下诅咒：…」
    "STS2_MOMOI_CARD_GRINDING.sidebar": {
        "zhs": "将依次生成以下[red]诅咒[/red]：[red]苦恼[/red]，[red]睡眠不佳[/red]，[red]疑虑[/red]，[red]执迷[/red]。",
        "eng": "The following [red]Curses[/red] are generated in order: [red]Writhe[/red], [red]Poor Sleep[/red], [red]Doubt[/red], [red]Enthralled[/red].",
    },
    # 相遇：铸造 / 生成 作为关键词染金
    "STS2_MOMOI_CARD_ENCOUNTER.description": {
        "zhs": "获得{Block:diff()}点[gold]格挡[/gold]。\n在本场战斗中解锁一个新效果：添加{IfUpgraded:show:2|1}张[purple]墨影[/purple]"
               "[gold]小刀[/gold]到你的[gold]手牌[/gold]；[gold]铸造[/gold]{IfUpgraded:show:11|7}；[gold]生成[/gold]"
               "{IfUpgraded:show:2|1}个随机充能球并获得{IfUpgraded:show:2|1}个充能球栏位。",
        "eng": "Gain {Block:diff()} [gold]Block[/gold].\nUnlock a new effect this combat: add {IfUpgraded:show:2|1} "
               "[purple]Inky[/purple] [gold]Shiv[/gold] to your [gold]Hand[/gold]; [gold]Forge[/gold] {IfUpgraded:show:11|7}; "
               "[gold]Channel[/gold] {IfUpgraded:show:2|1} random orb(s) and gain {IfUpgraded:show:2|1} orb slot(s).",
    },
}
POWERS = {
    # 构想之矛 power：文本用变量，但确保和 11/15 一致（数值来自 power 内部叠加常数，批次46 已改）
}
for base in list(CARDS):
    if base.endswith(".description") or base.endswith(".sidebar"):
        suffix = ".description" if base.endswith(".description") else ".sidebar"
        CARDS[base.replace(suffix, ".smartDescription" if suffix == ".description" else suffix)] = CARDS[base] \
            if suffix == ".description" else CARDS[base]
for base in [k for k in CARDS if k.endswith(".description")]:
    CARDS[base.replace(".description", ".smartDescription")] = CARDS[base]

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
for k in ("FIREPOWER_STRIKE", "SCRIPT_STRIKE", "BULLET_RAIN", "EXPERIENCE_COMBO", "SPEAR_SHIELD", "GRINDING", "ENCOUNTER"):
    key = "STS2_MOMOI_CARD_" + k
    v = cz.get(key + ".description", "")
    print("\n%s: %s" % (k, v.replace("\n", " / ")))
print("\nGRINDING sidebar:", cz.get("STS2_MOMOI_CARD_GRINDING.sidebar"))
