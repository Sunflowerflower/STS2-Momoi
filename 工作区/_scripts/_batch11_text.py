# -*- coding: utf-8 -*-
"""批次11：遗物 / 药水 / 卡牌的文本、关键词染色、侧栏。

规则（全部对照原版 localization/zhs 与 eng 的实际写法）：
  [gold] 关键词 / 牌堆 / 手牌 / 升级 / 消耗 / 保留 / 变化 / 金币 / 休息处 / 商店房间
  [blue] 数值（含最大生命值提升量、金币数、张数）
  [green] 回血数值，以及升级后的衍生牌名
  [red]  诅咒、诅咒牌名、遗物 flavor（原版未揭晓的那句）

用法：python _batch11_text.py [--dry]
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
LOC = os.path.join(MOD, "localization")
BACKUP = os.path.join(ROOT, "工作区", "_backup", "batch11_pre")

FLAVOR_ZH = "[red]这个遗物的细节将在未来揭晓……[/red]"
FLAVOR_EN = "[red]Details for this relic will be revealed in the future...[/red]"

# ─────────────────────────── 遗物 ───────────────────────────

RELICS = {
    "zhs": {
        "DRIED_INSPIRATION.description":
            "在你的回合开始时，若[gold]手牌[/gold]中没有[gold]构想[/gold]，将[blue]1[/blue]张[gold]构想[/gold]加入你的[gold]手牌[/gold]。",
        "OVERFLOWING_INSPIRATION.description":
            "在你的回合开始时，若[gold]手牌[/gold]中没有[gold]构想[/gold]，将[blue]1[/blue]张[green]构想+[/green]加入你的[gold]手牌[/gold]。",
        "OVERFLOWING_INSPIRATION.smartDescription":
            "在你的回合开始时，若[gold]手牌[/gold]中没有[gold]构想[/gold]，将[blue]1[/blue]张[green]构想+[/green]加入你的[gold]手牌[/gold]。",
        "UNFINISHED_CHIPS.description":
            "你每有[blue]50[/blue][gold]金币[/gold]，当你进入[gold]商店房间[/gold]和[gold]休息处[/gold]时就将你的最大生命值提升[blue]1[/blue]点。",
        "WINNING_SCRIPT.description":
            "每当你打出[gold]构想[/gold]时，[gold]升级[/gold]你[gold]手牌[/gold]中的所有牌。",
        "OLD_GAME_CONSOLE.description":
            "在每场战斗开始时，将一张随机[gold]小游戏牌[/gold]加入你的[gold]手牌[/gold]。",
        "GREEN_CHARM.description":
            "在你的回合开始时，你可以[gold]消耗[/gold]一张[red]诅咒[/red]牌来使[gold]构想[/gold]数值+[blue]1[/blue]。",
        "BOARD_GAME_OF_LIFE.description":
            "每当你打出一张[gold]小游戏牌[/gold]时，将一张随机牌添加到你的[gold]手牌[/gold]。",
        "G_BIBLE.description":
            "你每打出[blue]5[/blue]张[gold]小游戏牌[/gold]，就回复[green]6[/green]点生命。",
        "MIRROR.description":
            "在你的第一个回合结束时，你可以选择一张牌复制并将它们[gold]保留[/gold]一回合。",
    },
    "eng": {
        "DRIED_INSPIRATION.description":
            "At the start of your turn, if you have no [gold]Concept[/gold] in your [gold]Hand[/gold], add [blue]1[/blue] [gold]Concept[/gold] to your [gold]Hand[/gold].",
        "OVERFLOWING_INSPIRATION.description":
            "At the start of your turn, if you have no [gold]Concept[/gold] in your [gold]Hand[/gold], add [blue]1[/blue] [green]Concept+[/green] to your [gold]Hand[/gold].",
        "OVERFLOWING_INSPIRATION.smartDescription":
            "At the start of your turn, if you have no [gold]Concept[/gold] in your [gold]Hand[/gold], add [blue]1[/blue] [green]Concept+[/green] to your [gold]Hand[/gold].",
        "UNFINISHED_CHIPS.description":
            "For every [blue]50[/blue] [gold]Gold[/gold] you have, raise your Max HP by [blue]1[/blue] whenever you enter a [gold]Shop[/gold] or a [gold]Rest Site[/gold].",
        "WINNING_SCRIPT.description":
            "Whenever you play a [gold]Concept[/gold], [gold]Upgrade[/gold] all cards in your [gold]Hand[/gold].",
        "OLD_GAME_CONSOLE.description":
            "At the start of each combat, add a random [gold]Minigame[/gold] card to your [gold]Hand[/gold].",
        "GREEN_CHARM.description":
            "At the start of your turn, you may [gold]Exhaust[/gold] a [red]Curse[/red] to increase your [gold]Concept[/gold] number by [blue]1[/blue].",
        "BOARD_GAME_OF_LIFE.description":
            "Whenever you play a [gold]Minigame[/gold] card, add a random card to your [gold]Hand[/gold].",
        "G_BIBLE.description":
            "Every [blue]5[/blue] [gold]Minigame[/gold] cards you play, heal [green]6[/green] HP.",
        "MIRROR.description":
            "At the end of your first turn, you may choose a card to copy and [gold]Retain[/gold] them for one turn.",
    },
}

RELIC_FLAVORS = [
    "DRIED_INSPIRATION", "OVERFLOWING_INSPIRATION", "UNFINISHED_CHIPS", "WINNING_SCRIPT",
    "OLD_GAME_CONSOLE", "GREEN_CHARM", "BOARD_GAME_OF_LIFE", "G_BIBLE", "MIRROR",
]

# ─────────────────────────── 药水 ───────────────────────────

POTIONS = {
    "zhs": {
        "INSTANT_COFFEE.description":
            "将一张[gold]构想[/gold]与一张[red]睡眠不佳[/red]加入你的[gold]手牌[/gold]。",
        "STRAWBERRY_MILK.description":
            "清空所有能力与状态。\n获得[blue]7[/blue]点最大生命值。\n获得[blue]1[/blue]点[gold]力量[/gold]。",
        "PEACH_SODA.description":
            "将你[gold]手牌[/gold]中的任意张牌[gold]变化[/gold]为随机[gold]小游戏牌[/gold]。",
    },
    "eng": {
        "INSTANT_COFFEE.description":
            "Add a [gold]Concept[/gold] and a [red]Poor Sleep[/red] to your [gold]Hand[/gold].",
        "STRAWBERRY_MILK.description":
            "Clear all powers and statuses.\nGain [blue]7[/blue] Max HP.\nGain [blue]1[/blue] [gold]Strength[/gold].",
        "PEACH_SODA.description":
            "[gold]Transform[/gold] any number of cards in your [gold]Hand[/gold] into random [gold]Minigame[/gold] cards.",
    },
}

# ─────────────────────────── 卡牌 ───────────────────────────
# 键 -> (zhs 新文本, eng 新文本)，逐字替换（只改标点/颜色/删词，不动数值与格式标记）

CARDS = {
    "STS2_MOMOI_CARD_FISHING_MASTER.description": (
        "造成{CalculatedDamage:diff()}点伤害{IfUpgraded:show:X+1|X}次。\n"
        "[gold]斩杀[/gold]时，战斗结束时将1张{IfUpgraded:show:[green]渔获+[/green]|[gold]渔获[/gold]}"
        "加入[gold]牌组[/gold]（精英2张，Boss 3张）。",
        "Deal {CalculatedDamage:diff()} damage {IfUpgraded:show:X+1|X} times.\n"
        "On a kill, add a {IfUpgraded:show:[green]Catch+[/green]|[gold]Catch[/gold]} to your [gold]Deck[/gold] "
        "at the end of combat (2 for Elites, 3 for Bosses).",
    ),
    "STS2_MOMOI_CARD_CONCEPT_CARD.description": (
        "抽{ConceptDraw:diff()}张牌，获得{Energy:energyIcons()}，获得{ConceptVigor:diff()}点[gold]活力[/gold]。\n"
        "在你的回合开始时，若此牌在手牌中，则上方数值{IfUpgraded:show:+2|+1}，"
        "并根据数值将一张特定[red]诅咒[/red]加入[gold]手牌[/gold]。",
        "Draw {ConceptDraw:diff()} cards, gain {Energy:energyIcons()}, gain {ConceptVigor:diff()} Vigor.\n"
        "At the start of your turn, if this card is in your [gold]Hand[/gold], its number increases by "
        "{IfUpgraded:show:2|1}, and add a specific [red]Curse[/red] to your [gold]Hand[/gold] based on its number.",
    ),
    "STS2_MOMOI_CARD_STAY_UP_LATE.description": (
        "选择[gold]抽牌堆[/gold]的1张牌，将其[gold]变化[/gold]为1张{IfUpgraded:show:升级过的|}"
        "随机[gold]小游戏牌[/gold]。\n将一张[red]睡眠不佳[/red]放入你的[gold]手牌[/gold]。",
        "Choose a card in your [gold]Draw Pile[/gold] and [gold]Transform[/gold] it into a "
        "{IfUpgraded:show:Upgraded |}random [gold]Minigame[/gold] card.\n"
        "Add a [red]Poor Sleep[/red] to your [gold]Hand[/gold].",
    ),
    "STS2_MOMOI_CARD_DESTRUCTION_AND_REBIRTH.description": (
        "[gold]消耗[/gold]你所有的[red]诅咒[/red]牌。\n"
        "每有一张被[gold]消耗[/gold]的牌，将一张{IfUpgraded:show:升级过的|}随机[gold]小游戏牌[/gold]"
        "加入你的[gold]手牌[/gold]。",
        "[gold]Exhaust[/gold] all your [red]Curses[/red].\n"
        "For each card [gold]Exhausted[/gold], add a random {IfUpgraded:show:upgraded |}[gold]Minigame[/gold] "
        "card to your [gold]Hand[/gold].",
    ),
    "STS2_MOMOI_CARD_GRINDING.description": (
        "获得{Energy:energyIcons()}。\n将1张本场战斗中未获得过的特定[red]诅咒[/red]加入你的[gold]弃牌堆[/gold]。",
        "Gain {Energy:energyIcons()}.\n"
        "Add 1 specific [red]Curse[/red] you have not yet obtained this combat to your [gold]Discard Pile[/gold].",
    ),
    "STS2_MOMOI_CARD_PAC_MAN.description": (
        "将4张特定[red]诅咒[/red]加入你的[gold]手牌[/gold]。\n"
        "在你的回合开始时，若你有[red]诅咒[/red]牌，则打出1张{IfUpgraded:show:[green]疯狂进食+[/green]|[gold]疯狂进食[/gold]}"
        "并随机消耗你的1张[red]诅咒[/red]牌；若你没有[red]诅咒[/red]牌则改为将1张"
        "{IfUpgraded:show:[green]富足+[/green]|[gold]富足[/gold]}加入你的[gold]手牌[/gold]。",
        "Add 4 specific [red]Curses[/red] to your [gold]Hand[/gold].\n"
        "At the start of your turn, if you have any [red]Curses[/red], play a "
        "{IfUpgraded:show:[green]Feeding Frenzy+[/green]|[gold]Feeding Frenzy[/gold]} and exhaust a random "
        "[red]Curse[/red]; if you have no [red]Curses[/red], add an "
        "{IfUpgraded:show:[green]Abundance+[/green]|[gold]Abundance[/gold]} to your [gold]Hand[/gold] instead.",
    ),
    # 侧栏：诅咒与诅咒牌名都改成红色
    "STS2_MOMOI_CARD_CONCEPT_CARD.sidebarCurse": (
        "根据以下数值获得[red]诅咒[/red]：\n"
        "数值为3：[red]苦恼[/red]\n数值为4：[red]睡眠不佳[/red]\n"
        "数值为5：[red]疑虑[/red]\n数值为6及以上：[red]执迷[/red]",
        "[red]Curses[/red] by number:\n"
        "3: [red]Writhe[/red]\n4: [red]Poor Sleep[/red]\n5: [red]Doubt[/red]\n6+: [red]Enthralled[/red]",
    ),
    "STS2_MOMOI_CARD_GRINDING.sidebar": (
        "特定[red]诅咒[/red]：[red]苦恼[/red]，[red]睡眠不佳[/red]，[red]疑虑[/red]，[red]执迷[/red]。",
        "Specific [red]Curses[/red]: [red]Writhe[/red], [red]Poor Sleep[/red], [red]Doubt[/red], [red]Enthralled[/red].",
    ),
}


def apply(path, changes, lang):
    """把 changes 里的 'XXX.suffix' -> 文本 写进表（键前缀 = STS2_MOMOI_RELIC_ / _POTION_ / 卡牌原键）。"""
    d = json.load(open(path, encoding="utf-8"), object_pairs_hook=dict)
    n = 0
    for key, new in changes.items():
        full = key if key.startswith("STS2_MOMOI_CARD_") else None
        if full is None:
            if path.endswith("relics.json"):
                full = "STS2_MOMOI_RELIC_" + key
            elif path.endswith("potions.json"):
                full = "STS2_MOMOI_POTION_" + key
        cur = d.get(full)
        if cur is None:
            print("   !! %s 里没有 %s" % (os.path.basename(path), full))
            continue
        if cur != new:
            d[full] = new
            n += 1
    if not DRY:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return n


def main():
    os.makedirs(BACKUP, exist_ok=True)
    total = 0
    for lang in ("zhs", "eng"):
        # ---- 遗物 ----
        p = os.path.join(LOC, lang, "relics.json")
        changes = dict(RELICS[lang])
        total += apply(p, changes, lang)
        # flavor：9 个遗物统一成原版那句
        d = json.load(open(p, encoding="utf-8"), object_pairs_hook=dict)
        flav = FLAVOR_ZH if lang == "zhs" else FLAVOR_EN
        n = 0
        for r in RELIC_FLAVORS:
            k = "STS2_MOMOI_RELIC_" + r + ".flavor"
            if d.get(k) != flav:
                d[k] = flav
                n += 1
        if not DRY:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write("\n")
        print("[%s] relics: 描述 %d 条 + flavor %d 条" % (lang, len(RELICS[lang]), n))
        total += n

        # ---- 药水 ----
        p = os.path.join(LOC, lang, "potions.json")
        total += apply(p, POTIONS[lang], lang)
        print("[%s] potions: 描述 %d 条" % (lang, len(POTIONS[lang])))

        # ---- 卡牌 ----
        p = os.path.join(LOC, lang, "cards.json")
        idx = 0 if lang == "zhs" else 1
        changes = {k: v[idx] for k, v in CARDS.items()}
        # smartDescription 跟着 description 一起改（只有键存在时才写）
        extra = {}
        for k in list(changes):
            if k.endswith(".description"):
                extra[k[:-len(".description")] + ".smartDescription"] = changes[k]
        changes.update(extra)
        n = apply(p, changes, lang)
        print("[%s] cards: %d 条（含 smartDescription）" % (lang, n))
        total += n

    if DRY:
        print("\n--dry 结束，共会改动 %d 条，未写盘。" % total)
        return
    print("\n共改动 %d 条。" % total)


if __name__ == "__main__":
    main()
