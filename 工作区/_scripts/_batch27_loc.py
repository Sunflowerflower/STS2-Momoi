# -*- coding: utf-8 -*-
"""批次27 本地化：吃豆人 WIN！、跑酷「最多一张」、复盘去伤害、连连看选牌文案、黄金矿工死侧栏。"""
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


changed = 0

# ---------- cards ----------
CARDS = {
    # 吃豆人：富足 -> WIN！
    "STS2_MOMOI_CARD_PAC_MAN.description": {
        "zhs": "将4张特定[red]诅咒[/red]加入你的[gold]手牌[/gold]。\n"
               "在你的回合开始时，若你有[red]诅咒[/red]牌，则打出1张{IfUpgraded:show:[green]疯狂进食+[/green]|[gold]疯狂进食[/gold]}"
               "并随机[gold]消耗[/gold]你的1张[red]诅咒[/red]牌；若你没有[red]诅咒[/red]牌则改为将1张"
               "{IfUpgraded:show:[green]WIN！+[/green]|[gold]WIN！[/gold]}加入你的[gold]手牌[/gold]。",
        "eng": "Add 4 specific [red]Curses[/red] to your [gold]Hand[/gold].\n"
               "At the start of your turn, if you have any [red]Curses[/red], play 1 "
               "{IfUpgraded:show:[green]Feeding Frenzy+[/green]|[gold]Feeding Frenzy[/gold]} and "
               "[gold]Exhaust[/gold] a random [red]Curse[/red]; if you have no [red]Curses[/red], add 1 "
               "{IfUpgraded:show:[green]WIN!+[/green]|[gold]WIN![/gold]} to your [gold]Hand[/gold] instead.",
    },
    # 跑酷：选择一张 -> 选择最多一张
    "STS2_MOMOI_CARD_PARKOUR.description": {
        "zhs": "从5张{IfUpgraded:show:升级过的|}随机特定卡牌中选择最多一张放入你的[gold]手牌[/gold]，"
               "这张牌在本{IfUpgraded:show:场战斗|回合}可以被免费打出。\n"
               "在你的回合开始时，重复此效果，直至你受到伤害或失去生命。",
        "eng": "Choose up to 1 of 5 {IfUpgraded:show:Upgraded |}random specific cards to add to your "
               "[gold]Hand[/gold]; it can be played for free this {IfUpgraded:show:combat|turn}.\n"
               "At the start of your turn, repeat this until you take damage or lose HP.",
    },
    # 复盘：只留回手效果
    "STS2_MOMOI_CARD_GAME_REVIEW.description": {
        "zhs": "将[gold]消耗牌堆[/gold]中的一张随机[gold]小游戏牌[/gold]{IfUpgraded:show:[gold]升级并[/gold]|}"
               "放入你的[gold]手牌[/gold]。",
        "eng": "Put a random [gold]Minigame[/gold] card from your [gold]Exhaust Pile[/gold] "
               "{IfUpgraded:show:upgraded |}into your [gold]Hand[/gold].",
    },
}
# smartDescription 与 description 同步
for base in list(CARDS):
    if base.endswith(".description"):
        CARDS[base.replace(".description", ".smartDescription")] = CARDS[base]

for key, per in CARDS.items():
    for lang, txt in per.items():
        p, d = load(lang, "cards")
        if d.get(key) != txt:
            d[key] = txt
            save(p, d)
            changed += 1

# ---------- powers ----------
POWERS = {
    # 吃豆人能力：{AbundanceName} -> {WinName}
    "STS2_MOMOI_POWER_PAC_MAN_POWER.description": {
        "zhs": "在你的回合开始时，若你有[red]诅咒[/red]牌，则打出[blue]1[/blue]张{FrenzyName}并随机[gold]消耗[/gold]"
               "你的[blue]1[/blue]张[red]诅咒[/red]牌；若你没有[red]诅咒[/red]牌则改为将[blue]1[/blue]张{WinName}"
               "加入你的[gold]手牌[/gold]。",
        "eng": "At the start of your turn, if you have any [red]Curses[/red], play [blue]1[/blue] {FrenzyName} "
               "and [gold]Exhaust[/gold] a random [red]Curse[/red]; if you have no [red]Curses[/red], add "
               "[blue]1[/blue] {WinName} to your [gold]Hand[/gold] instead.",
    },
    # 跑酷能力：选择一张 -> 选择最多一张
    "STS2_MOMOI_POWER_PARKOUR_POWER.description": {
        "zhs": "在你的回合开始时，从[blue]5[/blue]张随机特定牌中选择最多一张放入你的[gold]手牌[/gold]，"
               "直至你受到未被[gold]格挡[/gold]的伤害或失去生命。这张牌在本回合可以被免费打出。",
        "eng": "At the start of your turn, choose up to [blue]1[/blue] of [blue]5[/blue] random specific cards "
               "and add it to your [gold]Hand[/gold], until you take unblocked damage or lose HP. "
               "That card costs nothing this turn.",
    },
    "STS2_MOMOI_POWER_PARKOUR_UPGRADED_POWER.description": {
        "zhs": "在你的回合开始时，从[blue]5[/blue]张[gold]升级[/gold]过的随机特定牌中选择最多一张放入你的[gold]手牌[/gold]，"
               "直至你受到未被[gold]格挡[/gold]的伤害或失去生命。这张牌在本场战斗可以被免费打出。",
        "eng": "At the start of your turn, choose up to [blue]1[/blue] of [blue]5[/blue] random upgraded specific "
               "cards and add it to your [gold]Hand[/gold], until you take unblocked damage or lose HP. "
               "That card costs nothing this combat.",
    },
}
for base in list(POWERS):
    if base.endswith(".description"):
        POWERS[base.replace(".description", ".smartDescription")] = POWERS[base]

for key, per in POWERS.items():
    for lang, txt in per.items():
        p, d = load(lang, "powers")
        if d.get(key) != txt:
            d[key] = txt
            save(p, d)
            changed += 1

# ---------- card_selection：连连看 / 跑酷 的选牌界面文案 ----------
SELECT = {
    "STS2_MOMOI_LINKUP_HEADER": {"zhs": "选择2张牌消耗", "eng": "Choose 2 cards to Exhaust"},
    "STS2_MOMOI_PARKOUR_HEADER": {"zhs": "选择最多一张牌加入你的手牌", "eng": "Choose up to 1 card to add to your hand"},
}
for key, per in SELECT.items():
    for lang, txt in per.items():
        p, d = load(lang, "card_selection")
        if d.get(key) != txt:
            d[key] = txt
            save(p, d)
            changed += 1

# ---------- 黄金矿工：sidebar2 是死键（代码只引用 sidebar1），且内容已过时（不再给金币） ----------
removed = 0
for lang in ("zhs", "eng"):
    p, d = load(lang, "cards")
    for k in ("STS2_MOMOI_CARD_GOLD_MINER.sidebar2",):
        if k in d:
            del d[k]
            save(p, d)
            removed += 1

print("本地化更新 %d 条，删除死键 %d 条" % (changed, removed))

# ---------- 复核 ----------
cz, _ = "zhs", None
d = load("zhs", "cards")[1]
e = load("eng", "cards")[1]
print("\n复核：")
print("  吃豆人 z:", d["STS2_MOMOI_CARD_PAC_MAN.description"].split("\n")[-1][-60:])
print("  跑酷 z 首句:", d["STS2_MOMOI_CARD_PARKOUR.description"].split("\n")[0][:60])
print("  复盘 z:", d["STS2_MOMOI_CARD_GAME_REVIEW.description"])
print("  GOLD_MINER.sidebar2 还在吗:", "STS2_MOMOI_CARD_GOLD_MINER.sidebar2" in d)
pz = load("zhs", "powers")[1]
print("  吃豆人 power 用 {WinName}:", "{WinName}" in pz["STS2_MOMOI_POWER_PAC_MAN_POWER.description"])
print("  {AbundanceName} 残留:", any("{AbundanceName}" in v for v in pz.values() if isinstance(v, str)))
