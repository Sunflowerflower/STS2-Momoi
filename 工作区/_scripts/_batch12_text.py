# -*- coding: utf-8 -*-
"""批次12：power 文本规范化（数字蓝 / 关键词金）+ 花凛重做 + 吃豆人消耗金 + 恢复→回复。

颜色规则（对照原版 localization/zhs/powers.json）：
  数字（含百分比、张数、层数、回合数）→ [blue]N[/blue]
  回血数值                          → [green]{Heal}[/green]
  关键词                            → [gold]…[/gold]
用法：python _batch12_text.py [--dry]
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
LOC = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "localization")

# ───────────────────────── power 描述：(zhs, eng) ─────────────────────────
P = {
    "FIREPOWER_POWER": (
        "当[gold]活力[/gold]将被全部消耗时，改为消耗[blue]1[/blue]层[gold]火力[/gold]并保留[gold]活力[/gold]。",
        "When all your [gold]Vigor[/gold] would be consumed, consume [blue]1[/blue] [gold]Firepower[/gold] instead and keep the [gold]Vigor[/gold].",
    ),
    "WATCH_OUT_POWER": (
        "下[blue]{Amount}[/blue]次打出[gold]攻击牌[/gold]时，随机将[gold]抽牌堆[/gold]的[blue]1[/blue]张[gold]攻击牌[/gold]加入[gold]手牌[/gold]。",
        "The next [blue]{Amount}[/blue] times you play an [gold]Attack[/gold], add [blue]1[/blue] random [gold]Attack[/gold] from your [gold]Draw Pile[/gold] to your [gold]Hand[/gold].",
    ),
    "MAID_WEAPON_POWER": (
        "下[blue]{Amount}[/blue]次打出[gold]攻击牌[/gold]时，将一张[gold]当心误射！[/gold]加入你的[gold]手牌[/gold]并打出。",
        "The next [blue]{Amount}[/blue] times you play an [gold]Attack[/gold], add a [gold]Watch Out![/gold] to your [gold]Hand[/gold] and play it.",
    ),
    "MAID_WEAPON_UPGRADED_POWER": (
        "下[blue]{Amount}[/blue]次打出[gold]攻击牌[/gold]时，将一张[gold]当心误射！+[/gold]加入你的[gold]手牌[/gold]并打出。",
        "The next [blue]{Amount}[/blue] times you play an [gold]Attack[/gold], add a [gold]Watch Out!+[/gold] to your [gold]Hand[/gold] and play it.",
    ),
    "YUZU_ESCORT_POWER": (
        "你每回合打出的前[blue]{Amount}[/blue]张[gold]小游戏牌[/gold]会多打出一次，然后失去[blue]1[/blue]点[gold]活力[/gold]。",
        "The first [blue]{Amount}[/blue] [gold]Minigame[/gold] cards you play each turn are played an extra time, then you lose [blue]1[/blue] [gold]Vigor[/gold].",
    ),
    "BURN_POWER": (
        "在其回合开始时失去[blue]{Amount}[/blue]点生命。\n拥有[gold]灼烧[/gold]的敌人每次造成未被格挡的伤害时，附加[blue]1[/blue]层[gold]灼烧[/gold]。",
        "Loses [blue]{Amount}[/blue] HP at the start of its turn.\nWhenever a Burning enemy deals unblocked damage, apply [blue]1[/blue] [gold]Burn[/gold].",
    ),
    "BURN_TURNS_POWER": (
        "[gold]灼烧[/gold]的剩余回合数。归零时与[gold]灼烧[/gold]一起消失。",
        "Remaining turns of [gold]Burn[/gold]. Disappears together with [gold]Burn[/gold] when it reaches [blue]0[/blue].",
    ),
    "FLAME_ATTACH_POWER": (
        "当你拥有[gold]火力[/gold]时，每当你造成伤害时，被击中的敌人获得[blue]{BurnTotal}[/blue]层[gold]灼烧[/gold]。",
        "While you have [gold]Firepower[/gold], whenever you deal damage, the enemy hit gains [blue]{BurnTotal}[/blue] [gold]Burn[/gold].",
    ),
    "CONCEPT_SPEAR_POWER": (
        "当你打出[gold]构想[/gold]时，该[gold]构想[/gold]每有[blue]1[/blue]点数值，就对所有敌人造成[blue]{DamagePer}[/blue]点伤害[blue]1[/blue]次。",
        "When you play a [gold]Concept[/gold], deal [blue]{DamagePer}[/blue] damage to ALL enemies [blue]1[/blue] time for each point of its number.",
    ),
    "CONCEPT_SHIELD_POWER": (
        "在你的回合结束时，[gold]手牌[/gold]中每有一张[gold]构想[/gold]就获得[blue]{BlockPer}[/blue]点[gold]格挡[/gold]。",
        "At the end of your turn, gain [blue]{BlockPer}[/blue] [gold]Block[/gold] for each [gold]Concept[/gold] in your [gold]Hand[/gold].",
    ),
    "SPEAR_SHIELD_POWER": (
        "当你打出[gold]构想[/gold]时，该[gold]构想[/gold]每有[blue]1[/blue]点数值，就获得[blue]{BlockPer}[/blue]点[gold]格挡[/gold]。\n"
        "在你的回合结束时，[gold]手牌[/gold]中每有一张[gold]构想[/gold]就对所有敌人造成[blue]{DamagePer}[/blue]点伤害。",
        "When you play a [gold]Concept[/gold], gain [blue]{BlockPer}[/blue] [gold]Block[/gold] for each point of its number.\n"
        "At the end of your turn, deal [blue]{DamagePer}[/blue] damage to ALL enemies for each [gold]Concept[/gold] in your [gold]Hand[/gold].",
    ),
    "POST_QUEST_POWER": (
        "下回合开始时，将一张{UpgradedMark}随机[gold]小游戏牌[/gold]放入你的[gold]手牌[/gold]。",
        "At the start of your next turn, put a random {UpgradedMark}[gold]Minigame[/gold] card into your [gold]Hand[/gold].",
    ),
    "CREATIVE_TASTE_POWER": (
        "在你的回合开始时，将[blue]{Amount}[/blue]张随机[gold]小游戏牌[/gold]加入你的[gold]手牌[/gold]。",
        "At the start of your turn, add [blue]{Amount}[/blue] random [gold]Minigame[/gold] cards to your [gold]Hand[/gold].",
    ),
    "CREATIVE_TASTE_UPGRADED_POWER": (
        "在你的回合开始时，将[blue]{Amount}[/blue]张[gold]升级[/gold]过的随机[gold]小游戏牌[/gold]加入你的[gold]手牌[/gold]。",
        "At the start of your turn, add [blue]{Amount}[/blue] upgraded random [gold]Minigame[/gold] cards to your [gold]Hand[/gold].",
    ),
    "YOSHIMI_REPEAT_POWER": (
        "接下来的[blue]{Amount}[/blue]个回合结束时，重复：获得[blue]{Block}[/blue]点[gold]格挡[/gold]、[blue]1[/blue]层[gold]火力[/gold]，对随机敌人造成[blue]{Damage}[/blue]点伤害。",
        "At the end of each of the next [blue]{Amount}[/blue] turns, repeat: gain [blue]{Block}[/blue] [gold]Block[/gold], [blue]1[/blue] [gold]Firepower[/gold], and deal [blue]{Damage}[/blue] damage to a random enemy.",
    ),
    "ASUNA_GUARD_POWER": (
        "[blue]{Amount}[/blue]回合内，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。",
        "For [blue]{Amount}[/blue] turns, all damage you take is reduced by [blue]{ReductionPct}%[/blue].",
    ),
    "DEV_SECRETS_POWER": (
        "打出[gold]小游戏牌[/gold]时使[gold]构想[/gold]升级，数值+[blue]{Gain}[/blue]。",
        "Playing a [gold]Minigame[/gold] card upgrades your [gold]Concept[/gold] and increases its number by [blue]{Gain}[/blue].",
    ),
    "LEARN_BY_DOING_POWER": (
        "生成[gold]构想[/gold]时，立即使其数值+[blue]{Gain}[/blue]。",
        "Whenever a [gold]Concept[/gold] is created, immediately increase its number by [blue]{Gain}[/blue].",
    ),
    "DUAL_BLADE_MOMOI_POWER": (
        "本回合当你打出一张不为[gold]小刀[/gold]的[gold]攻击牌[/gold]后，添加[blue]{Amount}[/blue]张[gold]小刀[/gold]到你的[gold]手牌[/gold]。",
        "This turn, after you play an [gold]Attack[/gold] that isn't a [gold]Shiv[/gold], add [blue]{Amount}[/blue] [gold]Shiv[/gold] to your [gold]Hand[/gold].",
    ),
    "DUAL_BLADE_MOMOI_UPGRADED_POWER": (
        "本回合当你打出一张不为[gold]小刀[/gold]的[gold]攻击牌[/gold]后，添加[blue]{Amount}[/blue]张[gold]小刀+[/gold]到你的[gold]手牌[/gold]。",
        "This turn, after you play an [gold]Attack[/gold] that isn't a [gold]Shiv[/gold], add [blue]{Amount}[/blue] [gold]Shiv+[/gold] to your [gold]Hand[/gold].",
    ),
    "SHOW_MY_STRENGTH_POWER": (
        "你每打出[blue]10[/blue]张牌时，获得{EnergyPer:energyIcons()}。再打出[blue]{Countdown}[/blue]张牌获得能量。",
        "Every [blue]10[/blue] cards you play, gain {EnergyPer:energyIcons()}. [blue]{Countdown}[/blue] more cards until the next one.",
    ),
    "DEV_GREEN_POWER": (
        "在你的回合开始时获得[blue]{Amount}[/blue]点[gold]活力[/gold]。",
        "At the start of your turn, gain [blue]{Amount}[/blue] [gold]Vigor[/gold].",
    ),
    "RANK_UP_POWER": (
        "在战斗结束时，额外获得[blue]{GoldFull}[/blue][gold]金币[/gold]和[blue]1[/blue]份卡牌奖励。",
        "At the end of combat, gain an additional [blue]{GoldFull}[/blue] [gold]Gold[/gold] and [blue]1[/blue] card reward.",
    ),
    "FOCUS_POWER": (
        "连续[blue]2[/blue]回合没打游戏则回合结束时[gold]构想[/gold]数值+[blue]{Amount}[/blue]；"
        "连续[blue]2[/blue]回合没用[gold]构想[/gold]则回合结束时可选择最多[blue]{RetainCount}[/blue]张牌[gold]保留[/gold]。",
        "If you go [blue]2[/blue] turns without playing a game, increase your [gold]Concept[/gold] number by [blue]{Amount}[/blue] at end of turn; "
        "if you go [blue]2[/blue] turns without playing a [gold]Concept[/gold], choose up to [blue]{RetainCount}[/blue] cards to [gold]Retain[/gold] at end of turn.",
    ),
    "INSPIRATION_POWER": (
        "当你打出数值不低于[blue]6[/blue]的[gold]构想[/gold]后，将[blue]{Amount}[/blue]张[gold]我的回合！[/gold]加入你的[gold]手牌[/gold]。",
        "After you play a [gold]Concept[/gold] with a number of at least [blue]6[/blue], add [blue]{Amount}[/blue] [gold]My Turn![/gold] to your [gold]Hand[/gold].",
    ),
    "INSPIRATION_UPGRADED_POWER": (
        "当你打出数值不低于[blue]5[/blue]的[gold]构想[/gold]后，将[blue]{Amount}[/blue]张[gold]我的回合！+[/gold]加入你的[gold]手牌[/gold]。",
        "After you play a [gold]Concept[/gold] with a number of at least [blue]5[/blue], add [blue]{Amount}[/blue] [gold]My Turn!+[/gold] to your [gold]Hand[/gold].",
    ),
    "GAME_KING_FORM_POWER": (
        "每当你生成一张[gold]小游戏牌[/gold]时，为其添加[blue]1[/blue]个随机附魔。\n"
        "首次打出一个牌名的[gold]小游戏牌[/gold]后，获得[blue]{BufferPer}[/blue]层[gold]缓冲[/gold]。",
        "Whenever you create a [gold]Minigame[/gold] card, add [blue]1[/blue] random Enchantment to it.\n"
        "The first time you play a [gold]Minigame[/gold] card with a given name, gain [blue]{BufferPer}[/blue] [gold]Buffer[/gold].",
    ),
    "HELP_FROM_MANY_POWER": (
        "在你的回合开始时，将[blue]{Amount}[/blue]张随机[gold]支援牌[/gold]洗入你的[gold]抽牌堆[/gold]。优先生成未拥有的。",
        "At the start of your turn, shuffle [blue]{Amount}[/blue] random [gold]Support[/gold] cards into your [gold]Draw Pile[/gold]. Prioritizes ones you don't have.",
    ),
    "HELP_FROM_MANY_UPGRADED_POWER": (
        "在你的回合开始时，将[blue]{Amount}[/blue]张[gold]升级[/gold]过的随机[gold]支援牌[/gold]洗入你的[gold]抽牌堆[/gold]。优先生成未拥有的。",
        "At the start of your turn, shuffle [blue]{Amount}[/blue] upgraded random [gold]Support[/gold] cards into your [gold]Draw Pile[/gold]. Prioritizes ones you don't have.",
    ),
    "RALLY_AGAIN_POWER": (
        "每当你打出[gold]构想[/gold]后，回复[green]{HealPer}[/green]点生命并获得[blue]{VigorPer}[/blue]点[gold]活力[/gold]。",
        "Whenever you play a [gold]Concept[/gold], heal [green]{HealPer}[/green] HP and gain [blue]{VigorPer}[/blue] [gold]Vigor[/gold].",
    ),
    "SHMUP_POWER": (
        "当任何生物死亡时，获得[blue]{Block}[/blue]点[gold]格挡[/gold]，将[blue]1[/blue]张[gold]{FuelName}[/gold]放入你的[gold]手牌[/gold]，抽[blue]1[/blue]张牌。",
        "Whenever any creature dies, gain [blue]{Block}[/blue] [gold]Block[/gold], put [blue]1[/blue] [gold]{FuelName}[/gold] into your [gold]Hand[/gold], and draw [blue]1[/blue] card.",
    ),
    "RHYTHM_GAME_POWER": (
        "在你的回合开始时，将[blue]1[/blue]~[blue]4[/blue]张[gold]方块[/gold]加入你的[gold]手牌[/gold]。"
        "在你的回合结束时，[gold]消耗[/gold]所有[gold]方块[/gold]，并对所有敌人造成[blue]{DamageTotal}[/blue]点伤害；"
        "每以该法[gold]消耗[/gold][blue]1[/blue]张[gold]方块[/gold]，该伤害降低[blue]{PerBlockTotal}[/blue]点。",
        "At the start of your turn, add [blue]1[/blue]-[blue]4[/blue] [gold]Blocks[/gold] to your [gold]Hand[/gold]. "
        "At the end of your turn, [gold]Exhaust[/gold] all [gold]Blocks[/gold] and deal [blue]{DamageTotal}[/blue] damage to ALL enemies; "
        "this damage is reduced by [blue]{PerBlockTotal}[/blue] for each [gold]Block[/gold] [gold]Exhausted[/gold] this way.",
    ),
    "PAC_MAN_POWER": (
        "在你的回合开始时，若你有[red]诅咒[/red]牌，则打出[blue]1[/blue]张{FrenzyName}并随机[gold]消耗[/gold]你的[blue]1[/blue]张[red]诅咒[/red]牌；"
        "若你没有[red]诅咒[/red]牌则改为将[blue]1[/blue]张{AbundanceName}加入你的[gold]手牌[/gold]。",
        "At the start of your turn, if you have any [red]Curses[/red], play [blue]1[/blue] {FrenzyName} and [gold]Exhaust[/gold] a random [red]Curse[/red]; "
        "if you have no [red]Curses[/red], add [blue]1[/blue] {AbundanceName} to your [gold]Hand[/gold] instead.",
    ),
    "ROLE_PLAY_POWER": (
        "在你的回合开始时，将[blue]1[/blue]张[gold]{SplashName}[/gold]（[gold]消耗[/gold]）放入所有玩家的[gold]手牌[/gold]中。",
        "At the start of your turn, put [blue]1[/blue] [gold]{SplashName}[/gold] ([gold]Exhaust[/gold]) into every player's [gold]Hand[/gold].",
    ),
    "TETRIS_FULL_HAND_POWER": (
        "本回合[gold]手牌[/gold]达到上限时：[gold]消耗[/gold]所有[gold]手牌[/gold]，抽牌，获得能量，"
        "将[gold]弃牌堆[/gold]的所有[gold]方块[/gold]返回[gold]手牌[/gold]，并[gold]消耗[/gold][gold]俄罗斯方块[/gold]。",
        "When your [gold]Hand[/gold] is full this turn: [gold]Exhaust[/gold] your whole [gold]Hand[/gold], draw, gain Energy, "
        "return all [gold]Blocks[/gold] from your [gold]Discard Pile[/gold] to your [gold]Hand[/gold], and [gold]Exhaust[/gold] [gold]Tetris[/gold].",
    ),
    "KOTAMA_STRENGTH_POWER": (
        "本回合获得[gold]力量[/gold]，回合结束移除。",
        "Gain [gold]Strength[/gold] this turn. Removed at the end of the turn.",
    ),
    "PLANT_FORESHADOW_POWER": (
        "下[blue]{Amount}[/blue]次抽到[gold]构想[/gold]时，使[gold]构想[/gold]数值+[blue]1[/blue]。",
        "The next [blue]{Amount}[/blue] times you draw a [gold]Concept[/gold], increase its number by [blue]1[/blue].",
    ),
    "CYCLIC_NARRATIVE_POWER": (
        "本回合结束时，将本回合所有进入过[gold]弃牌堆[/gold]的牌洗入[gold]抽牌堆[/gold]。",
        "At the end of this turn, shuffle every card that entered your [gold]Discard Pile[/gold] this turn into your [gold]Draw Pile[/gold].",
    ),
    "MONTAGE_POWER": (
        "回合结束时，从你的[gold]抽牌堆[/gold]中选择[blue]{Amount}[/blue]张牌将其打出。"
        "如果这张牌与你打出的上一张牌类型相同/不同，将[blue]1[/blue]张[gold]构想[/gold]加入你的[gold]手牌[/gold]/使[gold]构想[/gold]数值+[blue]1[/blue]。",
        "At the end of your turn, choose [blue]{Amount}[/blue] cards from your [gold]Draw Pile[/gold] and play them. "
        "If a card's type matches / doesn't match the previous one, add [blue]1[/blue] [gold]Concept[/gold] to your [gold]Hand[/gold] / increase its number by [blue]1[/blue].",
    ),
    "FELL_TO_SECOND_TIER_POWER": (
        "在战斗结束时，获得[blue]{Gold}[/blue][gold]金币[/gold]。",
        "At the end of combat, gain [blue]{Gold}[/blue] [gold]Gold[/gold].",
    ),
    "DARK_PSYCHOLOGY_POWER": (
        "下[blue]{Amount}[/blue]次获得[gold]力量[/gold]时将不再获得，改为使[gold]构想[/gold]数值+[blue]1[/blue]。",
        "The next [blue]{Amount}[/blue] times you would gain [gold]Strength[/gold], increase your [gold]Concept[/gold] number by [blue]1[/blue] instead.",
    ),
    "REPEAT_MOVE_POWER": (
        "在你的回合开始时，将所选牌的复制品加入你的[gold]手牌[/gold]。",
        "At the start of your turn, add a copy of the chosen card to your [gold]Hand[/gold].",
    ),
}

# REPEAT_MOVE_POWER 的 smartDescription 带卡名
P_SMART_ONLY = {
    "REPEAT_MOVE_POWER": (
        "在你的回合开始时，将[gold]{Card}[/gold]的复制品加入你的[gold]手牌[/gold]。",
        "At the start of your turn, add a copy of [gold]{Card}[/gold] to your [gold]Hand[/gold].",
    ),
}

# ───────────────────────── 卡牌文本 ─────────────────────────
C = {
    "STS2_MOMOI_CARD_MOMOI_SUPPORT_KARIN.description": (
        "造成{CalculatedDamage:diff()}点伤害。\n对Boss造成的伤害增加[blue]{IfUpgraded:show:75%|50%}[/blue]。",
        "Deal {CalculatedDamage:diff()} damage.\nDeal [blue]{IfUpgraded:show:75%|50%}[/blue] more damage to Bosses.",
    ),
    "STS2_MOMOI_CARD_RALLY_AGAIN.description": (
        "回复已损生命的[blue]10%[/blue]的生命并获得等量的[gold]活力[/gold]。\n"
        "当你打出[gold]构想[/gold]后，重复此效果。\n"
        "当生命值低于[blue]20%[/blue]时，立即将此牌打出，并额外获得[blue]1[/blue]层[gold]无实体[/gold]。",
        "Heal [blue]10%[/blue] of your missing HP and gain [gold]Vigor[/gold] equal to it.\n"
        "Repeat after playing a [gold]Concept[/gold].\n"
        "If your HP is below [blue]20%[/blue], auto-play this card and gain [blue]1[/blue] [gold]Intangible[/gold].",
    ),
    "STS2_MOMOI_CARD_PAC_MAN.description": (
        "将[blue]4[/blue]张特定[red]诅咒[/red]加入你的[gold]手牌[/gold]。\n"
        "在你的回合开始时，若你有[red]诅咒[/red]牌，则打出[blue]1[/blue]张{IfUpgraded:show:[green]疯狂进食+[/green]|[gold]疯狂进食[/gold]}"
        "并随机[gold]消耗[/gold]你的[blue]1[/blue]张[red]诅咒[/red]牌；若你没有[red]诅咒[/red]牌则改为将[blue]1[/blue]张"
        "{IfUpgraded:show:[green]富足+[/green]|[gold]富足[/gold]}加入你的[gold]手牌[/gold]。",
        "Add [blue]4[/blue] specific [red]Curses[/red] to your [gold]Hand[/gold].\n"
        "At the start of your turn, if you have any [red]Curses[/red], play [blue]1[/blue] "
        "{IfUpgraded:show:[green]Feeding Frenzy+[/green]|[gold]Feeding Frenzy[/gold]} and [gold]Exhaust[/gold] a random [red]Curse[/red]; "
        "if you have no [red]Curses[/red], add [blue]1[/blue] {IfUpgraded:show:[green]Abundance+[/green]|[gold]Abundance[/gold]} "
        "to your [gold]Hand[/gold] instead.",
    ),
}


def apply(path, changes, only_if_exists_suffix=(".description", ".smartDescription")):
    d = json.load(open(path, encoding="utf-8"), object_pairs_hook=dict)
    n = 0
    for key, new in changes.items():
        if d.get(key) != new:
            d[key] = new
            n += 1
    return d, n


def main():
    total = 0
    for i, lang in enumerate(("zhs", "eng")):
        # ---- powers ----
        p = os.path.join(LOC, lang, "powers.json")
        d = json.load(open(p, encoding="utf-8"), object_pairs_hook=dict)
        n = 0
        for key, pair in P.items():
            full = "STS2_MOMOI_POWER_" + key
            for suf in (".description", ".smartDescription"):
                k = full + suf
                if k not in d:
                    continue
                new = pair[i]
                if d[k] != new:
                    d[k] = new
                    n += 1
        for key, pair in P_SMART_ONLY.items():
            k = "STS2_MOMOI_POWER_" + key + ".smartDescription"
            if k in d and d[k] != pair[i]:
                d[k] = pair[i]
                n += 1
        if not DRY:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write("\n")
        print("[%s] powers: %d 条" % (lang, n))
        total += n

        # ---- cards ----
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
