# -*- coding: utf-8 -*-
"""2026-10-11 批次9 · 卡牌文本修改（zhs + eng）

覆盖：
  * 重振旗鼓 → 重整旗鼓（改名）
  * 双线叙事 / 吃豆人！ / 渔获 / 秒人斧 / 相遇 / 俄罗斯方块！ / 构想 / 连连看！ /
    消消乐！ / 植物大战僵尸 / 绝地求生 / 扫雷 / 大姐头 / 火焰附加 等
用法：py -3 _update_batch9_loc.py [--dry]
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "localization")
NL = "\n"

# ---------------------------------------------------------------- zhs
# (key, old, new)；old=None 表示"不管旧值，直接覆盖"
Z = [
    # ── 吃豆人！：先判诅咒牌，有才打出疯狂进食（不进牌堆），没有就给富足
    ("STS2_MOMOI_CARD_PAC_MAN.description",
     "将4张特定诅咒放入你的[gold]手牌[/gold]。" + NL +
     "回合开始时，自动打出1张[gold]疯狂进食{IfUpgraded:show:+}[/gold]并将其[gold]消耗[/gold]，然后随机[gold]消耗[/gold]你的1张诅咒牌。" + NL +
     "若你没有诅咒牌，改为将一张[gold]富足{IfUpgraded:show:+}[/gold]加入你的[gold]手牌[/gold]。",
     "将4张特定诅咒放入你的[gold]手牌[/gold]。" + NL +
     "在你的回合开始时，若你有诅咒牌，则直接打出1张[gold]疯狂进食{IfUpgraded:show:+}[/gold]，然后随机[gold]消耗[/gold]你的1张诅咒牌。" + NL +
     "若你没有诅咒牌，改为将1张[gold]富足{IfUpgraded:show:+}[/gold]加入你的[gold]手牌[/gold]。"),

    # ── 双线叙事：只复制选中的那张，并给原构想加一层重放
    ("STS2_MOMOI_CARD_DUAL_NARRATIVE.description",
     "使[gold]构想[/gold]数值+2。" + NL +
     "将[gold]构想[/gold]的一张复制品加入你的[gold]手牌[/gold]，然后为其附魔[gold]灵魂之力[/gold]。",
     "固有。" + NL +
     "使[gold]构想[/gold]数值+2。" + NL +
     "选择1张[gold]构想[/gold]复制，并为被复制的[gold]构想[/gold]添加1层[gold]重放[/gold]，然后为复制品附魔[gold]灵魂之力[/gold]。" + NL +
     "消耗。"),

    # ── 渔获 / 秒人斧：打出时立即移除
    ("STS2_MOMOI_CARD_CATCH.description",
     "战斗结束时，从你的[gold]牌组[/gold]中移除这张牌。",
     "打出时，从你的[gold]牌组[/gold]中移除这张牌。"),
    ("STS2_MOMOI_CARD_ONE_SHOT_AXE.description",
     "战斗结束时，从你的[gold]牌组[/gold]中移除这张牌。",
     "打出时，从你的[gold]牌组[/gold]中移除这张牌。"),

    # ── 援助系：后两句连成一句
    ("STS2_MOMOI_CARD_ENGINEERING_DEPT_AID.description",
     "从3张{IfUpgraded:show:升级过的|}牌中选择一张放入你的[gold]手牌[/gold]。" + NL + "无法连续选择相同的选项。",
     "从3张{IfUpgraded:show:升级过的|}牌中选择一张放入你的[gold]手牌[/gold]，无法连续选择相同的选项。"),
    ("STS2_MOMOI_CARD_VERITAS_DEPT_AID.description",
     "从3张{IfUpgraded:show:升级过的|}牌中选择一张放入你的[gold]手牌[/gold]。" + NL + "无法连续选择相同的选项。",
     "从3张{IfUpgraded:show:升级过的|}牌中选择一张放入你的[gold]手牌[/gold]，无法连续选择相同的选项。"),
    ("STS2_MOMOI_CARD_CN_C_AID.description",
     "从4张{IfUpgraded:show:升级过的|}牌中选择一张放入你的[gold]手牌[/gold]。" + NL + "无法连续选择相同的选项。",
     "从4张{IfUpgraded:show:升级过的|}牌中选择一张放入你的[gold]手牌[/gold]，无法连续选择相同的选项。"),

    # ── 相遇：改写成一句话 + 墨影紫色
    ("STS2_MOMOI_CARD_ENCOUNTER.description",
     "获得{Block:diff()}点[gold]格挡[/gold]。" + NL +
     "本场战斗中，该牌每打出一次，解锁一个新效果（获得{IfUpgraded:show:2|1}张[gold]墨影小刀[/gold] → 铸造{IfUpgraded:show:11|7} → 生成{IfUpgraded:show:2|1}个随机充能球并获得{IfUpgraded:show:2|1}个充能球栏位），最多3次。",
     "获得{Block:diff()}点[gold]格挡[/gold]。" + NL +
     "在本场战斗中解锁一个新效果：添加{IfUpgraded:show:2|1}张[purple]墨影[/purple][gold]小刀[/gold]到你的[gold]手牌[/gold]；铸造{IfUpgraded:show:11|7}；生成{IfUpgraded:show:2|1}个随机充能球并获得{IfUpgraded:show:2|1}个充能球栏位。"),

    # ── 俄罗斯方块！：精简
    ("STS2_MOMOI_CARD_TETRIS.description",
     None,
     "将随机1~4张[gold]方块[/gold]加入你的[gold]手牌[/gold]。" + NL +
     "将此牌返回你的[gold]手牌[/gold]。" + NL +
     "在这个回合，当你的[gold]手牌[/gold]达到上限时，[gold]消耗[/gold]所有[gold]手牌[/gold]，抽{Cards:diff()}张牌，获得{Energy:energyIcons()}，并[gold]消耗[/gold]这张牌，将[gold]弃牌堆[/gold]的所有[gold]方块[/gold]返回[gold]手牌[/gold]。"),

    # ── 构想：三句合并成一句
    ("STS2_MOMOI_CARD_CONCEPT_CARD.description",
     "抽{ConceptDraw:diff()}张牌。" + NL + "获得{Energy:energyIcons()}。" + NL + "获得{ConceptVigor:diff()}点[gold]活力[/gold]。" + NL +
     "回合开始时，若此牌仍在手上，则上方数值{IfUpgraded:show:+2|+1}，并根据数值将一张特定诅咒加入[gold]手牌[/gold]。",
     "抽{ConceptDraw:diff()}张牌，获得{Energy:energyIcons()}，获得{ConceptVigor:diff()}点[gold]活力[/gold]。" + NL +
     "在你的回合开始时，若此牌在手牌中，则上方数值{IfUpgraded:show:+2|+1}，并根据数值将一张特定诅咒加入[gold]手牌[/gold]。"),

    # ── 连连看！：删去"（无论是否升级）"
    ("STS2_MOMOI_CARD_LINK_UP.description",
     "若[gold]消耗[/gold]的牌名称相同（无论是否[gold]升级[/gold]），则抽{Cards:diff()}张牌并获得{Energy:energyIcons()}。",
     "若[gold]消耗[/gold]的牌名称相同，则抽{Cards:diff()}张牌并获得{Energy:energyIcons()}。"),

    # ── 消消乐！：改写成一段
    ("STS2_MOMOI_CARD_MATCH3.description",
     None,
     "选择1张牌并选择任意张与其类型相同的牌[gold]消耗[/gold]。若[gold]消耗[/gold]的牌不低于3张，根据[gold]消耗[/gold]牌的类型触发{IfUpgraded:show:更强的|}额外效果；若[gold]消耗[/gold]的牌超过3张，每超出1张牌就抽1张牌并获得{Energy:energyIcons()}。"),

    # ── 植物大战僵尸：改写成一段 + 耗能归零
    ("STS2_MOMOI_CARD_PLANTS_VS_ZOMBIES.description",
     None,
     "从随机两张{IfUpgraded:show:升级过的|}特定牌中选择一张放入你的[gold]手牌[/gold]，下回合将另一张牌放入你的[gold]手牌[/gold]。它们的耗能在下次打出前变为0{Energy:energyIcons()}。"),

    # ── 大姐头
    ("STS2_MOMOI_CARD_BIG_SISTER.description",
     "复制出的牌本回合", "复制品本回合"),

    # ── 回合开始/结束措辞统一
    ("STS2_MOMOI_CARD_RHYTHM_GAME.description", "回合开始时，将随机1~4张", "在你的回合开始时，将随机1~4张"),
    ("STS2_MOMOI_CARD_RHYTHM_GAME.description", "回合结束时，[gold]消耗[/gold]所有", "在你的回合结束时，[gold]消耗[/gold]所有"),
    ("STS2_MOMOI_CARD_SPEAR_SHIELD.description", "回合结束时，[gold]手牌[/gold]中每有一张", "在你的回合结束时，[gold]手牌[/gold]中每有一张"),
    ("STS2_MOMOI_CARD_CONCEPT_SHIELD.description", "回合结束时，[gold]手牌[/gold]中每有一张", "在你的回合结束时，[gold]手牌[/gold]中每有一张"),
    ("STS2_MOMOI_CARD_DEV_GREEN.description", "回合开始时获得", "在你的回合开始时获得"),
    ("STS2_MOMOI_CARD_ROLE_PLAY.description", "回合开始时，将一张", "在你的回合开始时，将一张"),
    ("STS2_MOMOI_CARD_HELP_FROM_MANY.description", "回合开始时，将一张", "在你的回合开始时，将一张"),
    ("STS2_MOMOI_CARD_PARKOUR.description", "回合开始时，重复此效果", "在你的回合开始时，重复此效果"),

    # ── 火焰附加：改成原版口吻
    ("STS2_MOMOI_CARD_FLAME_ATTACH.description",
     "当你拥有[gold]火力[/gold]时，每当你造成伤害，被击中的敌人获得{Burn:diff()}层[gold]灼烧[/gold]。",
     "每有一次拥有[gold]火力[/gold]的攻击造成伤害，就给予{Burn:diff()}层[gold]灼烧[/gold]。"),

    # ── 见识下我的实力吧
    ("STS2_MOMOI_CARD_SHOW_MY_STRENGTH.description", "每打出10张牌，", "你每打出10张牌，"),

    # ── 绝地求生：主行显示最大值，括号显示实时值
    ("STS2_MOMOI_CARD_BATTLE_ROYALE.description",
     None,
     "抽{Cards:diff()}张牌，获得{Energy:energyIcons()}。" + NL +
     "你的[gold]手牌[/gold]中每有一张其他牌，此牌的数值就降低1点。（抽{CalculatedCards:diff()}张牌，获得{CalculatedEnergy:energyIcons()}）" + NL +
     "消耗。"),

    # ── 扫雷
    ("STS2_MOMOI_CARD_MINESWEEPER.description",
     "直接打出这张牌。", "直接打出那张炸弹。"),

    # ── 改名
    ("STS2_MOMOI_CARD_RALLY_AGAIN.title", "重振旗鼓", "重整旗鼓"),
]

# ---------------------------------------------------------------- eng
E = [
    ("STS2_MOMOI_CARD_PAC_MAN.description",
     "At the start of your turn, auto-play a Feeding Frenzy{IfUpgraded:show:+} and [gold]Exhaust[/gold] it, then [gold]Exhaust[/gold] a random Curse.",
     "At the start of your turn, if you have any Curses, play a Feeding Frenzy{IfUpgraded:show:+} directly, then [gold]Exhaust[/gold] a random Curse."),
    ("STS2_MOMOI_CARD_DUAL_NARRATIVE.description",
     "Increase [gold]Concept[/gold] count by 2." + NL +
     "Add a copy of [gold]Concept[/gold] to your [gold]Hand[/gold], then Enchant it with [gold]Souls Power[/gold].",
     "Innate." + NL +
     "Increase [gold]Concept[/gold] count by 2." + NL +
     "Choose 1 [gold]Concept[/gold] to copy, give the original 1 [gold]Replay[/gold], then Enchant the copy with [gold]Souls Power[/gold]." + NL +
     "Exhaust."),
    ("STS2_MOMOI_CARD_CATCH.description",
     "At the end of combat, remove this card from your [gold]Deck[/gold].",
     "When played, remove this card from your [gold]Deck[/gold]."),
    ("STS2_MOMOI_CARD_ONE_SHOT_AXE.description",
     "At the end of combat, remove this card from your [gold]Deck[/gold].",
     "When played, remove this card from your [gold]Deck[/gold]."),
    ("STS2_MOMOI_CARD_ENGINEERING_DEPT_AID.description",
     "to add to your [gold]Hand[/gold]." + NL + "You cannot pick the same option twice in a row.",
     "to add to your [gold]Hand[/gold], and you cannot pick the same option twice in a row."),
    ("STS2_MOMOI_CARD_VERITAS_DEPT_AID.description",
     "to add to your [gold]Hand[/gold]." + NL + "You cannot pick the same option twice in a row.",
     "to add to your [gold]Hand[/gold], and you cannot pick the same option twice in a row."),
    ("STS2_MOMOI_CARD_CN_C_AID.description",
     "to add to your [gold]Hand[/gold]." + NL + "You cannot pick the same option twice in a row.",
     "to add to your [gold]Hand[/gold], and you cannot pick the same option twice in a row."),
    ("STS2_MOMOI_CARD_ENCOUNTER.description",
     None,
     "Gain {Block:diff()} [gold]Block[/gold]." + NL +
     "Unlock a new effect this combat: add {IfUpgraded:show:2|1} [purple]Inky[/purple] [gold]Shiv[/gold] to your [gold]Hand[/gold]; Forge {IfUpgraded:show:11|7}; channel {IfUpgraded:show:2|1} random orb(s) and gain {IfUpgraded:show:2|1} orb slot(s)."),
    ("STS2_MOMOI_CARD_TETRIS.description",
     None,
     "Add 1-4 random [gold]Blocks[/gold] to your [gold]Hand[/gold]." + NL +
     "Return this card to your [gold]Hand[/gold]." + NL +
     "This turn, when your [gold]Hand[/gold] reaches its limit, [gold]Exhaust[/gold] your whole [gold]Hand[/gold], draw {Cards:diff()} cards, gain {Energy:energyIcons()}, [gold]Exhaust[/gold] this card, then return all [gold]Blocks[/gold] from your [gold]Discard Pile[/gold] to your [gold]Hand[/gold]."),
    ("STS2_MOMOI_CARD_CONCEPT_CARD.description",
     "Draw {ConceptDraw:diff()} cards." + NL + "Gain {Energy:energyIcons()}." + NL + "Gain {ConceptVigor:diff()} Vigor." + NL,
     "Draw {ConceptDraw:diff()} cards, gain {Energy:energyIcons()}, gain {ConceptVigor:diff()} Vigor." + NL),
    ("STS2_MOMOI_CARD_CONCEPT_CARD.description",
     "At the start of your turn, if this card is still in your [gold]Hand[/gold], its number increases",
     "At the start of your turn, if this card is in your [gold]Hand[/gold], its number increases"),
    ("STS2_MOMOI_CARD_LINK_UP.description",
     "If they share the same name (upgrades do not matter), draw",
     "If they share the same name, draw"),
    ("STS2_MOMOI_CARD_MATCH3.description",
     None,
     "Choose a card and [gold]Exhaust[/gold] any number of cards with the same type. If at least 3 cards are [gold]Exhausted[/gold], trigger a {IfUpgraded:show:stronger |}bonus effect based on their type; if more than 3 cards are [gold]Exhausted[/gold], draw 1 card and gain {Energy:energyIcons()} for each card beyond 3."),
    ("STS2_MOMOI_CARD_PLANTS_VS_ZOMBIES.description",
     None,
     "Choose 1 of 2 {IfUpgraded:show:Upgraded |}random specific cards to add to your [gold]Hand[/gold]; next turn, add the other one. Their energy cost becomes 0{Energy:energyIcons()} until they are next played."),
    ("STS2_MOMOI_CARD_RHYTHM_GAME.description", "At the start of your turn, add 1-4", "At the start of your turn, add 1-4"),
    ("STS2_MOMOI_CARD_RHYTHM_GAME.description", "At end of turn, [gold]Exhaust[/gold] all Block", "At the end of your turn, [gold]Exhaust[/gold] all Block"),
    ("STS2_MOMOI_CARD_SPEAR_SHIELD.description", "At the end of your turn, deal", "At the end of your turn, deal"),
    ("STS2_MOMOI_CARD_DEV_GREEN.description", "At the start of your turn, gain {Vigor:diff()}",
     "At the start of your turn, gain {Vigor:diff()}"),
    ("STS2_MOMOI_CARD_FLAME_ATTACH.description",
     "While you have Firepower, whenever you deal damage, the hit enemy gains {Burn:diff()} Burn.",
     "Each time an attack with Firepower deals damage, apply {Burn:diff()} Burn."),
    ("STS2_MOMOI_CARD_SHOW_MY_STRENGTH.description", "Every 10 cards played,", "Every 10 cards you play,"),
    ("STS2_MOMOI_CARD_BATTLE_ROYALE.description",
     None,
     "Draw {Cards:diff()} cards, gain {Energy:energyIcons()}." + NL +
     "Each OTHER card in your [gold]Hand[/gold] reduces this card's numbers by 1. (Draw {CalculatedCards:diff()} cards, gain {CalculatedEnergy:energyIcons()})" + NL +
     "Exhaust."),
    ("STS2_MOMOI_CARD_MINESWEEPER.description",
     "The next time you draw The Bomb, play it automatically.",
     "The next time you draw The Bomb, play that Bomb directly."),
]

# 纯替换（zhs）：同一段文本在 description / smartDescription 里都要改
MIRROR_KEYS = ("description",)


def apply(path, table, mirror=True):
    d = json.load(open(path, encoding="utf-8"))
    changed = 0
    for key, old, new in table:
        keys = [key]
        if mirror and key.endswith(".description"):
            sk = key[:-len("description")] + "smartDescription"
            if sk in d:
                keys.append(sk)
        for k in keys:
            cur = d.get(k)
            if cur is None:
                print("  !! 缺 key:", k)
                continue
            if old is None:
                if cur == new:
                    continue
                d[k] = new
                changed += 1
            else:
                if old not in cur:
                    print("  !! 未匹配:", k, "| 找不到:", old[:60])
                    continue
                d[k] = cur.replace(old, new)
                changed += 1
    return d, changed


def main():
    dry = "--dry" in sys.argv
    total = 0
    for lang, table in (("zhs", Z), ("eng", E)):
        p = os.path.join(MOD, lang, "cards.json")
        d, n = apply(p, table)
        total += n
        print("[%s] cards.json 改动 %d 处" % (lang, n))
        if not dry:
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # powers.json：重振旗鼓 → 重整旗鼓
    for lang in ("zhs",):
        p = os.path.join(MOD, lang, "powers.json")
        d = json.load(open(p, encoding="utf-8"))
        for k in list(d):
            if isinstance(d[k], str) and "重振旗鼓" in d[k]:
                d[k] = d[k].replace("重振旗鼓", "重整旗鼓")
                total += 1
                print("[%s] powers.json 改名:", k)
        if not dry:
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # 新增卡牌选择提示词
    for lang, txt in (("zhs", "选择1张构想复制"), ("eng", "Choose 1 Concept to copy")):
        p = os.path.join(MOD, lang, "card_selection.json")
        d = json.load(open(p, encoding="utf-8"))
        d["TO_CLONE_CONCEPT"] = txt
        if not dry:
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("[%s] card_selection.json += TO_CLONE_CONCEPT" % lang)

    print("共改动 %d 处" % total, "[dry-run]" if dry else "已写入")


if __name__ == "__main__":
    main()
