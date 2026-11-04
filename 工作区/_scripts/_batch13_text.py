# -*- coding: utf-8 -*-
"""批次13：循环叙事（可叠加）/ 植物大战僵尸（显示实际卡名）/ 俄罗斯方块（显示抽牌数与能量）。

用法：python _batch13_text.py [--dry]
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
LOC = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "localization")

P = {
    "CYCLIC_NARRATIVE_POWER": (
        "接下来的[blue]{Amount}[/blue]个回合结束时，将本回合所有进入过[gold]弃牌堆[/gold]的牌洗入[gold]抽牌堆[/gold]。",
        "At the end of each of the next [blue]{Amount}[/blue] turns, shuffle every card that entered your "
        "[gold]Discard Pile[/gold] this turn into your [gold]Draw Pile[/gold].",
    ),
    "PLANTS_NEXT_TURN_POWER": (
        "下回合将[gold]{Card}[/gold]加入你的[gold]手牌[/gold]。",
        "At the start of your next turn, add [gold]{Card}[/gold] to your [gold]Hand[/gold].",
    ),
    "TETRIS_FULL_HAND_POWER": (
        "本回合[gold]手牌[/gold]达到上限时：[gold]消耗[/gold]所有[gold]手牌[/gold]，抽[blue]{Cards}[/blue]张牌，"
        "获得{Energy:energyIcons()}，将[gold]弃牌堆[/gold]的所有[gold]方块[/gold]返回[gold]手牌[/gold]，"
        "并[gold]消耗[/gold][gold]俄罗斯方块[/gold]。",
        "When your [gold]Hand[/gold] is full this turn: [gold]Exhaust[/gold] your whole [gold]Hand[/gold], "
        "draw [blue]{Cards}[/blue] cards, gain {Energy:energyIcons()}, return all [gold]Blocks[/gold] from your "
        "[gold]Discard Pile[/gold] to your [gold]Hand[/gold], and [gold]Exhaust[/gold] [gold]Tetris[/gold].",
    ),
}

# 卡牌文本同步（循环叙事卡：说明可叠加数量由能力层数决定）
C = {
    "STS2_MOMOI_CARD_CYCLIC_NARRATIVE.description": (
        "将本回合所有进入过[gold]弃牌堆[/gold]的牌洗入[gold]抽牌堆[/gold]。\n"
        "接下来的[blue]1[/blue]个回合结束时，重复此效果（重复打出可以叠加持续回合数）。",
        "Shuffle all cards that entered your [gold]Discard Pile[/gold] this turn into your [gold]Draw Pile[/gold].\n"
        "Repeat this effect at the end of each of the next [blue]1[/blue] turns (playing it again extends the duration).",
    ),
}


def main():
    total = 0
    for i, lang in enumerate(("zhs", "eng")):
        p = os.path.join(LOC, lang, "powers.json")
        d = json.load(open(p, encoding="utf-8"), object_pairs_hook=dict)
        n = 0
        for key, pair in P.items():
            full = "STS2_MOMOI_POWER_" + key
            for suf in (".description", ".smartDescription"):
                k = full + suf
                if k in d and d[k] != pair[i]:
                    d[k] = pair[i]
                    n += 1
        if not DRY:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write("\n")
        print("[%s] powers: %d 条" % (lang, n))
        total += n

        p = os.path.join(LOC, lang, "cards.json")
        d = json.load(open(p, encoding="utf-8"), object_pairs_hook=dict)
        n = 0
        for key, pair in C.items():
            base = key[:-len(".description")]
            for suf in (".description", ".smartDescription"):
                k = base + suf
                if k in d and d[k] != pair[i]:
                    d[k] = pair[i]
                    n += 1
        if not DRY:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write("\n")
        print("[%s] cards: %d 条" % (lang, n))
        total += n

    print("\n共改动 %d 条%s" % (total, "（--dry，未写盘）" if DRY else ""))


if __name__ == "__main__":
    main()
