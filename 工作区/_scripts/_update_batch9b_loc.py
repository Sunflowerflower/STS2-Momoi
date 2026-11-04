# -*- coding: utf-8 -*-
"""2026-10-12 批次9b · 修正上一批的文本问题

  * 固有。/消耗。 会被游戏自动追加（CardKeywordOrder.beforeDescription/afterDescription），
    描述里不能再写一遍 —— 双线叙事出现 2 个固有 + 2 个消耗、绝地求生出现 2 个消耗，都是这个原因。
  * 植物大战僵尸：{Energy:energyIcons()} 需要卡上有 Energy 变量，否则报
    "No source extension could handle the selector named Energy"；另外 0+图标 会变成 00c。
  * 秒人斧 / 渔获：按用户要求删掉「打出时，」。
  * 吃豆人！：按用户给的原文重写（含能力侧栏）。
用法：py -3 _update_batch9b_loc.py [--dry]
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "localization")
NL = "\n"

Z = {
    # ── 双线叙事：去掉自动追加的 固有。/消耗。，并删去「1层」
    "STS2_MOMOI_CARD_DUAL_NARRATIVE.description":
        "使[gold]构想[/gold]数值+2。" + NL +
        "选择1张[gold]构想[/gold]复制，并为被复制的[gold]构想[/gold]添加[gold]重放[/gold]，然后为复制品附魔[gold]灵魂之力[/gold]。",

    # ── 绝地求生：去掉多余的第二行「消耗。」
    "STS2_MOMOI_CARD_BATTLE_ROYALE.description":
        "抽{Cards:diff()}张牌，获得{Energy:energyIcons()}。" + NL +
        "你的[gold]手牌[/gold]中每有一张其他牌，此牌的数值就降低1点。（抽{CalculatedCards:diff()}张牌，获得{CalculatedEnergy:energyIcons()}）",

    # ── 秒人斧 / 渔获：删「打出时，」
    "STS2_MOMOI_CARD_ONE_SHOT_AXE.description":
        "造成{CalculatedDamage:diff()}点伤害。" + NL +
        "从你的[gold]牌组[/gold]中移除这张牌。",
    "STS2_MOMOI_CARD_CATCH.description":
        "抽{Cards:diff()}张牌，获得{Energy:energyIcons()}，获得{Vigor:diff()}点[gold]活力[/gold]，回复{Heal:diff()}点生命。" + NL +
        "从你的[gold]牌组[/gold]中移除这张牌。",

    # ── 吃豆人！：用户原文
    "STS2_MOMOI_CARD_PAC_MAN.description":
        "将4张特定诅咒加入你的[gold]手牌[/gold]。" + NL +
        "在你的回合开始时，若你有诅咒牌，则打出1张[gold]疯狂进食{IfUpgraded:show:+}[/gold]并随机消耗你的1张诅咒牌；"
        "若你没有诅咒牌则改为将1张[gold]富足{IfUpgraded:show:+}[/gold]加入你的[gold]手牌[/gold]。",

    # ── 植物大战僵尸：0 + 图标 → 直接用能量图标（EnergyVar=0）
    "STS2_MOMOI_CARD_PLANTS_VS_ZOMBIES.description":
        "从随机两张{IfUpgraded:show:升级过的|}特定牌中选择一张放入你的[gold]手牌[/gold]，"
        "下回合将另一张牌放入你的[gold]手牌[/gold]。它们的耗能在下次打出前变为{Energy:energyIcons()}。",
}

E = {
    "STS2_MOMOI_CARD_DUAL_NARRATIVE.description":
        "Increase [gold]Concept[/gold] count by 2." + NL +
        "Choose 1 [gold]Concept[/gold] to copy, give the copied [gold]Concept[/gold] [gold]Replay[/gold], "
        "then Enchant the copy with [gold]Souls Power[/gold].",
    "STS2_MOMOI_CARD_BATTLE_ROYALE.description":
        "Draw {Cards:diff()} cards, gain {Energy:energyIcons()}." + NL +
        "Each OTHER card in your [gold]Hand[/gold] reduces this card's numbers by 1. "
        "(Draw {CalculatedCards:diff()} cards, gain {CalculatedEnergy:energyIcons()})",
    "STS2_MOMOI_CARD_ONE_SHOT_AXE.description":
        "Deal {CalculatedDamage:diff()} damage." + NL +
        "Remove this card from your [gold]Deck[/gold].",
    "STS2_MOMOI_CARD_CATCH.description":
        "Draw {Cards:diff()} card(s), gain {Energy:energyIcons()}, gain {Vigor:diff()} [gold]Vigor[/gold], "
        "and heal {Heal:diff()} HP." + NL +
        "Remove this card from your [gold]Deck[/gold].",
    "STS2_MOMOI_CARD_PAC_MAN.description":
        "Add 4 specific Curses to your [gold]Hand[/gold]." + NL +
        "At the start of your turn, if you have any Curses, play a Feeding Frenzy{IfUpgraded:show:+} and exhaust a random Curse; "
        "if you have no Curses, add an Abundance{IfUpgraded:show:+} to your [gold]Hand[/gold] instead.",
    "STS2_MOMOI_CARD_PLANTS_VS_ZOMBIES.description":
        "Choose 1 of 2 {IfUpgraded:show:Upgraded |}random specific cards to add to your [gold]Hand[/gold]; "
        "next turn, add the other one. Their energy cost becomes {Energy:energyIcons()} until they are next played.",
}

ZP = {
    "STS2_MOMOI_POWER_PAC_MAN_POWER.description":
        "在你的回合开始时，若你有诅咒牌，则打出1张{FrenzyName}并随机消耗你的1张诅咒牌；"
        "若你没有诅咒牌则改为将1张{AbundanceName}加入你的手牌。",
}
EP = {
    "STS2_MOMOI_POWER_PAC_MAN_POWER.description":
        "At the start of your turn, if you have any Curses, play {FrenzyName} and exhaust a random Curse; "
        "if you have no Curses, add {AbundanceName} to your hand instead.",
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
    for lang, tbl in (("zhs", ZP), ("eng", EP)):
        p = os.path.join(MOD, lang, "powers.json")
        d, n = apply(p, tbl)
        total += n
        print("[%s] powers.json %d 处" % (lang, n))
        if not dry:
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("共 %d 处" % total, "[dry-run]" if dry else "已写入")


if __name__ == "__main__":
    main()
