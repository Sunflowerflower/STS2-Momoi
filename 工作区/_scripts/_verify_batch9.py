# -*- coding: utf-8 -*-
"""批次9 / 9b 自检：逐条断言用户要求都已落地（本地化 + 代码）"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "localization")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
CARDIMG = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "images", "cards")

z = json.load(open(os.path.join(MOD, "zhs", "cards.json"), encoding="utf-8"))
e = json.load(open(os.path.join(MOD, "eng", "cards.json"), encoding="utf-8"))
zp = json.load(open(os.path.join(MOD, "zhs", "powers.json"), encoding="utf-8"))

OK = 0
BAD = 0


def chk(label, cond, extra=""):
    global OK, BAD
    if cond:
        OK += 1
        print("  ok   %s" % label)
    else:
        BAD += 1
        print("  FAIL %s   %s" % (label, str(extra)[:160]))


def has(key, *subs):
    v = (z.get(key) or "")
    # 批次18：卡面数字现在会染成 [blue]，比对时先去标记，只校验文案。
    plain = re.sub(r"\[/?[a-z]+\]", "", v)
    miss = [s for s in subs if s not in v and s not in plain]
    chk("zhs %s" % key.split(".")[-1][:36], not miss, "缺 %r | 实际 %r" % (miss, v[:140]))


def text_of(name):
    base = [k[:-6] for k, v in z.items() if k.endswith(".title") and v == name][0]
    return z[base + ".description"], e.get(base + ".description", "")


def code(fname, *subs):
    t = open(os.path.join(CODE, fname), encoding="utf-8").read()
    miss = [s for s in subs if s not in t]
    chk("code %s" % fname, not miss, "缺 %r" % (miss,))


def nocode(fname, *subs):
    t = open(os.path.join(CODE, fname), encoding="utf-8").read()
    bad = [s for s in subs if s in t]
    chk("code %s 无旧写法" % fname, not bad, "仍有 %r" % (bad,))


print("── 1. 改名 重振旗鼓 → 重整旗鼓")
chk("zhs 卡名", z.get("STS2_MOMOI_CARD_RALLY_AGAIN.title") == "重整旗鼓")
chk("zhs power 名", zp.get("STS2_MOMOI_POWER_RALLY_AGAIN_POWER.title") == "重整旗鼓")
chk("全库无残留", "重振旗鼓" not in json.dumps(z, ensure_ascii=False))

print("── 2. 双线叙事")
d, ed = text_of("双线叙事")
chk("无手写「固有。」", "固有。" not in d)
chk("无手写「消耗。」", not d.rstrip().endswith("消耗。"))
chk("无「1层」", "1层" not in d)
has("STS2_MOMOI_CARD_DUAL_NARRATIVE.description", "选择1张", "重放", "灵魂之力")
code("Cards/RemainingCards3.cs", "picked.BaseReplayCount++", "TO_CLONE_CONCEPT", "c is ConceptCard")
nocode("Cards/RemainingCards3.cs", "foreach (var original in PileType.Hand.GetPile(player).Cards.Where(c => c is ConceptCard)")

print("── 3. 吃豆人！")
d, ed = text_of("吃豆人！")
want = ("将4张特定[red]诅咒[/red]加入你的[gold]手牌[/gold]。\n"
        "在你的回合开始时，若你有[red]诅咒[/red]牌，则打出1张{IfUpgraded:show:[green]疯狂进食+[/green]|[gold]疯狂进食[/gold]}"
        "并随机[gold]消耗[/gold]你的1张[red]诅咒[/red]牌；若你没有[red]诅咒[/red]牌则改为将1张"
        "{IfUpgraded:show:[green]WIN！+[/green]|[gold]WIN！[/gold]}加入你的[gold]手牌[/gold]。")  # 批次19：数字不上色；批次24：富足→WIN！
chk("吃豆人 描述文本（含绿色卡名）", d == want, d)
chk("无「直接打出」", "直接打出" not in d)
chk("power 侧栏用疯狂进食", "疯狂进食" not in zp.get("STS2_MOMOI_POWER_PAC_MAN_POWER.description", "")
    or "{FrenzyName}" in zp.get("STS2_MOMOI_POWER_PAC_MAN_POWER.description", ""))
code("Cards/RemainingCards5.cs", "ModelDb.Card<FeedingFrenzy>().Title", "frenzy.CreateDupe(player)", "curses.Count == 0")
nocode("Cards/RemainingCards5.cs", "ModelDb.Card<Maul>().Title")

print("── 4. 渔获 / 秒人斧")
for nm in ("渔获", "秒人斧"):
    d, ed = text_of(nm)
    chk("%s 无「打出时，」" % nm, "打出时，" not in d, d)
    chk("%s 有「从你的[gold]牌组[/gold]中移除这张牌。」" % nm, "从你的[gold]牌组[/gold]中移除这张牌。" in d)
    chk("%s 无「战斗结束时」" % nm, "战斗结束时" not in d)
    chk("%s eng 无 When played" % nm, "When played" not in ed)
for f in ("Cards/RemainingCards2.cs", "Cards/MinigameFlowCards.cs"):
    code(f, "RemoveSelfFromDeck", "await RemoveSelfFromDeck();", "IsClone",
         "Owner.Deck.Cards.FirstOrDefault", "MomoiDiag.Log")
    nocode(f, "TaskHelper.RunSafely(CardPileCmd.RemoveFromDeck")

print("── 5. 相遇")
has("STS2_MOMOI_CARD_ENCOUNTER.description", "[purple]墨影[/purple]", "在本场战斗中解锁一个新效果：", "铸造", "充能球栏位")
code("Cards/RemainingSpecialCards.cs", "HoverTipFactory.FromEnchantment<Inky>()")

print("── 6. 援助三兄弟")
for k in ("ENGINEERING_DEPT_AID", "VERITAS_DEPT_AID", "CN_C_AID"):
    v = z["STS2_MOMOI_CARD_" + k + ".description"]
    ev = e["STS2_MOMOI_CARD_" + k + ".description"]
    chk("zhs %s 已连句" % k, "放入你的[gold]手牌[/gold]，无法连续选择相同的选项。" in v and "手牌[/gold]。\n无法连续" not in v)
    chk("eng %s 已连句" % k, "cannot pick the same option twice in a row." in ev and "Hand[/gold].\nYou cannot" not in ev)

print("── 7. 俄罗斯方块！")
d, _ = text_of("俄罗斯方块！")
chk("无「溢出部分」", "溢出部分" not in d)
chk("无「该效果不可叠加」", "该效果不可叠加" not in d)
chk("有「在这个回合，当你的[gold]手牌[/gold]达到上限时」", "在这个回合，当你的[gold]手牌[/gold]达到上限时" in d)

print("── 8. 构想")
has("STS2_MOMOI_CARD_CONCEPT_CARD.description",
    "抽{ConceptDraw:diff()}张牌，获得{Energy:energyIcons()}，获得{ConceptVigor:diff()}点[gold]活力[/gold]。",
    "在你的回合开始时，若此牌在手牌中")
chk("构想 无「（当前数值」", "当前数值" not in z["STS2_MOMOI_CARD_CONCEPT_CARD.description"])

print("── 8b. 序章（固有常驻 + 升级删消耗）")
code("Cards/ReworkBatch2.cs",
     "CardKeyword.Innate, CardKeyword.Exhaust", "LocalKeywords.Remove(CardKeyword.Exhaust)")
nocode("Cards/ReworkBatch2.cs", "LocalKeywords.Add(CardKeyword.Innate)")

print("── 9. 连连看 / 消消乐 / 植物大战僵尸")
chk("连连看去掉（无论是否升级）", "无论是否" not in z["STS2_MOMOI_CARD_LINK_UP.description"])
# 批次18：消消乐重做 —— 侧栏删除，三消改为「打出并消耗」，升级改为加保留。
has("STS2_MOMOI_CARD_MATCH3.description", "选择任意张类型相同的牌", "超过3张则每超出一张就抽1张牌")
d, _ = text_of("植物大战僵尸")
has("STS2_MOMOI_CARD_PLANTS_VS_ZOMBIES.description", "耗能在下次打出前变为{Energy:energyIcons()}。")
chk("植物大战僵尸 没有 0+图标 的双写", "0{Energy" not in d, d)
code("Cards/RemainingCards5.cs", "new EnergyVar(0)")

print("── 10. 绝地求生")
d, _ = text_of("绝地求生")
chk("无手写「消耗」", "消耗" not in d, d)
chk("括号显示实时值", "（抽{CalculatedCards:diff()}张牌，获得{CalculatedEnergy:energyIcons()}）" in d)
has("STS2_MOMOI_CARD_BATTLE_ROYALE.description", "抽{Cards:diff()}张牌，获得{Energy:energyIcons()}。")
code("Cards/RemainingCards4.cs", 'new DynamicVar("Cards", 4)', 'new EnergyVar("Energy", 3)',
     'DynamicVars["Cards"].UpgradeValueBy(1)', 'DynamicVars["Energy"].UpgradeValueBy(1)')

print("── 11. 其它文本")
chk("大姐头 复制品", "复制品本回合" in z["STS2_MOMOI_CARD_BIG_SISTER.description"])
for k in ("RHYTHM_GAME", "SPEAR_SHIELD", "CONCEPT_SHIELD", "DEV_GREEN", "ROLE_PLAY", "HELP_FROM_MANY"):   # 批次28：跑酷的 power 已删除
    v = z["STS2_MOMOI_CARD_" + k + ".description"]
    chk("%s 在你的回合开始/结束" % k, "在你的回合开始" in v or "在你的回合结束" in v)
chk("火焰附加", "每有一次拥有[gold]火力[/gold]的攻击造成伤害" in z["STS2_MOMOI_CARD_FLAME_ATTACH.description"])
chk("见识下我的实力吧", "你每打出10张牌" in z["STS2_MOMOI_CARD_SHOW_MY_STRENGTH.description"])
chk("扫雷", "直接打出那张炸弹。" in z["STS2_MOMOI_CARD_MINESWEEPER.description"])

print("── 12. 卡面")
for f in ("DualNarrative.png", "PickRed.png", "RallyAgain.png"):
    p = os.path.join(CARDIMG, f)
    chk("卡面 %s" % f, os.path.exists(p) and os.path.getsize(p) > 200000)

print()
print("结果：%d 通过 / %d 失败" % (OK, BAD))
sys.exit(1 if BAD else 0)
