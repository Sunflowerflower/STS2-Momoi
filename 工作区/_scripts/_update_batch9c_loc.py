# -*- coding: utf-8 -*-
"""2026-10-12 批次9c · 三处修改

  1) 构想：局内描述去掉「（当前数值0）」（即 {InCombat:...} 那段）
  2) 吃豆人！：升级后「疯狂进食+」「富足+」整个卡名变绿（不只那个 + 号）
  3) 序章：代码侧见 Cards/ReworkBatch2.cs（升级删消耗、固有常驻）
用法：py -3 _update_batch9c_loc.py [--dry]
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "localization")
NL = "\n"

Z = {
    # 1) 构想：去掉括号里的实时数值
    "STS2_MOMOI_CARD_CONCEPT_CARD.description":
        "抽{ConceptDraw:diff()}张牌，获得{Energy:energyIcons()}，获得{ConceptVigor:diff()}点[gold]活力[/gold]。" + NL +
        "在你的回合开始时，若此牌在手牌中，则上方数值{IfUpgraded:show:+2|+1}，并根据数值将一张特定诅咒加入[gold]手牌[/gold]。",

    # 2) 吃豆人：整个卡名放进 IfUpgraded 的两个分支里 —— 升级走 [green] 分支，
    #    否则预览模式只会把分支内容（原来只有「+」）染绿，名字还是金色的。
    "STS2_MOMOI_CARD_PAC_MAN.description":
        "将4张特定诅咒加入你的[gold]手牌[/gold]。" + NL +
        "在你的回合开始时，若你有诅咒牌，则打出1张{IfUpgraded:show:[green]疯狂进食+[/green]|[gold]疯狂进食[/gold]}"
        "并随机消耗你的1张诅咒牌；若你没有诅咒牌则改为将1张{IfUpgraded:show:[green]富足+[/green]|[gold]富足[/gold]}"
        "加入你的[gold]手牌[/gold]。",
}

E = {
    "STS2_MOMOI_CARD_CONCEPT_CARD.description":
        "Draw {ConceptDraw:diff()} cards, gain {Energy:energyIcons()}, gain {ConceptVigor:diff()} Vigor." + NL +
        "At the start of your turn, if this card is in your [gold]Hand[/gold], its number increases by {IfUpgraded:show:2|1}, "
        "and add a specific Curse to your [gold]Hand[/gold] based on its number.",

    "STS2_MOMOI_CARD_PAC_MAN.description":
        "Add 4 specific Curses to your [gold]Hand[/gold]." + NL +
        "At the start of your turn, if you have any Curses, play a "
        "{IfUpgraded:show:[green]Feeding Frenzy+[/green]|[gold]Feeding Frenzy[/gold]} and exhaust a random Curse; "
        "if you have no Curses, add an {IfUpgraded:show:[green]Abundance+[/green]|[gold]Abundance[/gold]} "
        "to your [gold]Hand[/gold] instead.",
}


def apply(path, table):
    d = json.load(open(path, encoding="utf-8"))
    n = 0
    for key, val in table.items():
        if d.get(key) == val:
            continue
        d[key] = val
        n += 1
        sk = key[:-len("description")] + "smartDescription"
        if sk in d:
            d[sk] = val
            n += 1
    return d, n


def main():
    dry = "--dry" in sys.argv
    total = 0
    for lang, tbl in (("zhs", Z), ("eng", E)):
        p = os.path.join(MOD, lang, "cards.json")
        d, n = apply(p, tbl)
        total += n
        print("[%s] cards.json %d 处" % (lang, n))
        if not dry:
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("共 %d 处" % total, "[dry-run]" if dry else "已写入")


if __name__ == "__main__":
    main()
