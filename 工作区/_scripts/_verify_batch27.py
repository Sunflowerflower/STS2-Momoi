# -*- coding: utf-8 -*-
"""批次27 自检：游戏人生标签只本场战斗、激战/开发秘籍/100连抽/复盘、连连看/跑酷/节奏游戏、吃豆人 WIN！、黄金矿工死侧栏。"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
LOC = os.path.join(MOD, "localization")

ok = fail = 0


def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))


def code(path):
    return open(os.path.join(CODE, path), encoding="utf-8").read()


def body(src, cls):
    m = re.search(r"\bclass\s+" + cls + r"\b", src)
    if not m:
        return ""
    i = src.find("{", m.end())
    depth = 0
    for j in range(i, len(src)):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                return src[m.start():j + 1]
    return ""


def load(lang, table):
    return json.load(open(os.path.join(LOC, lang, table + ".json"), encoding="utf-8"))


Z, E = load("zhs", "cards"), load("eng", "cards")
PZ, PE = load("zhs", "powers"), load("eng", "powers")
SZ, SE = load("zhs", "card_selection"), load("eng", "card_selection")

ms = code(os.path.join("Cards", "MinigameSupport.cs"))
gl = code(os.path.join("Cards", "GameLife.cs"))
rs = code(os.path.join("Cards", "RemainingSpecialCards.cs"))
hp = code(os.path.join("Cards", "HundredPull.cs"))
ca = code(os.path.join("Cards", "CommonAttackCards.cs"))
lk = code(os.path.join("Cards", "LinkUp.cs"))
r4 = code(os.path.join("Cards", "RemainingCards4.cs"))
r5 = code(os.path.join("Cards", "RemainingCards5.cs"))
stats = code("CombatStats.cs")
entry = code("Entry.cs")
label = code(os.path.join("Patches", "CardKeywordLabelPatch.cs"))
sidebar = code(os.path.join("Patches", "MinigameSidebarPatch.cs"))

print("== 1. 游戏人生：标签只在本场战斗生效 ==")
chk("TemporaryGameCards" in ms, "新增本场战斗临时表")
chk("ReferenceEqualityComparer.Instance" in ms, "按实例引用（不按 Id）")
chk("MarkTemporaryGameCard" in ms and "ClearTemporaryGameCards" in ms, "标记 / 清空 API")
chk("IsTemporaryGameCard(card)" in ms.split("public static bool IsMinigameCard")[1].split(";")[0],
    "IsMinigameCard 把临时标记算进去")
chk(".AddModCardTag(" not in gl, "GameLife 不再写卡的标签集合（只剩注释里的提醒）")
chk("MinigameSupport.MarkTemporaryGameCard(card)" in gl, "改用临时标记")
chk("MinigameSupport.ClearTemporaryGameCards();" in stats, "战斗开始清空")
chk("StripLeakedGameCardTags" in entry, "开局清理旧版泄漏的标签")
chk("RemoveModCardTag(FullGameTag)" in ms, "清理用 RemoveModCardTag")
chk("IsTemporaryGameCard(card)" in label, "金色顶行文本认临时标记")
chk("IsTemporaryGameCard(__instance)" in sidebar, "侧栏认临时标记")
chk("IsUpgraded" in gl.split("ApplyToSameNameCards(picked);")[0][-400:], "升级才作用于同名牌")
chk("foreach (var pileType in new[] { PileType.Hand, PileType.Draw, PileType.Discard })" in gl,
    "同名牌覆盖手牌/抽牌堆/弃牌堆")
chk("catch (Exception ex) when (ex is ArgumentOutOfRangeException or InvalidOperationException)" in gl,
    "选牌异常兜底（QuickRestart 拆场）")

print("== 2. 激战 ==")
cs = body(rs, "ConfusedShot")
chk("public ConfusedShot() : base(0, CardType.Attack" in cs, "费用 1 -> 0（升级前后都是 0）")
chk("EnergyCost.UpgradeBy" not in cs, "升级不改费")
chk("new CalculationBaseVar(2m)" in cs, "伤害 -> 2（批次44）")
chk('new DynamicVar("Hits", 2)' in cs and 'DynamicVars["Hits"].UpgradeValueBy(1)' in cs, "升级仍是 +1 次")

print("== 3. 开发秘籍 / 100连抽 ==")
chk("public DevSecrets() : base(3, CardType.Power, CardRarity.Rare" in rs, "开发秘籍 罕见 -> 稀有")
pull = body(hp, "HundredPull")
chk("CardRarity.Rare" in pull, "100连抽 稀有（批次40 又改回稀有）")
chk("CardKeyword.Exhaust, CardKeyword.Innate" in pull, "固有升级前后都有")
chk("EnergyCost.UpgradeBy(-1)" in pull, "升级：费 4 -> 3")
chk("AddKeyword(CardKeyword.Innate)" not in pull, "升级不再加固有")

print("== 4. 连连看选牌文案 ==")
chk('new LocString("card_selection", "STS2_MOMOI_LINKUP_HEADER")' in lk, "用模组自带的文案键")
chk(SZ.get("STS2_MOMOI_LINKUP_HEADER") == "选择2张牌消耗", "zhs = 选择2张牌消耗", SZ.get("STS2_MOMOI_LINKUP_HEADER"))
chk("Choose 2 cards to Exhaust" in (SE.get("STS2_MOMOI_LINKUP_HEADER") or ""), "eng 同步")

print("== 5. 跑酷：最多一张（可跳过） ==")
chk('"STS2_MOMOI_PARKOUR_HEADER"), 0, 1' in r4, "MinSelect=0（可以跳过）")
chk("Cancelable = true" in body(r4, "Parkour").split("STS2_MOMOI_PARKOUR_HEADER")[1][:120], "可取消")
chk("选择最多一张" in Z["STS2_MOMOI_CARD_PARKOUR.description"], "卡面文本")
chk("STS2_MOMOI_POWER_PARKOUR_POWER.description" not in PZ, "跑酷 power 文本已随 power 一起删除")
chk(SZ.get("STS2_MOMOI_PARKOUR_HEADER") == "选择最多一张牌加入你的手牌", "选牌界面文案", SZ.get("STS2_MOMOI_PARKOUR_HEADER"))

print("== 6. 节奏游戏 power 右下角 = 将要造成的伤害 ==")
rg = body(r5, "RhythmGamePower")
chk("public override int DisplayAmount" in rg, "重写 DisplayAmount")
chk("data.Damage - blocks * data.PerBlock" in rg, "= 基础伤害 - 当前方块数 × 每方块降低")
chk("CardPile.Get(PileType.Hand, player)" in rg and "CardPile.Get(PileType.Discard, player)" in rg,
    "统计手牌 + 弃牌堆的方块")
chk(rg.count("InvokeDisplayAmountChanged();") == 2, "施加/回合开始各刷一次", rg.count("InvokeDisplayAmountChanged();"))

print("== 7. 吃豆人：富足 -> WIN！ ==")
z = Z["STS2_MOMOI_CARD_PAC_MAN.description"]
chk("{IfUpgraded:show:[green]WIN！+[/green]|[gold]WIN！[/gold]}" in z, "卡面 zhs", z)
chk("富足" not in z, "卡面不再提富足")
e = E["STS2_MOMOI_CARD_PAC_MAN.description"]
chk("[green]WIN!+[/green]" in e and "[gold]WIN![/gold]" in e, "卡面 eng", e)
chk("Abundance" not in e, "eng 不再提 Abundance")
chk("{WinName}" in PZ["STS2_MOMOI_POWER_PAC_MAN_POWER.description"], "能力文本用 {WinName}")
chk("AbundanceName" not in PZ["STS2_MOMOI_POWER_PAC_MAN_POWER.description"], "旧变量已换掉")
chk("ModelDb.Card<WinCard>()" in r5, "实际给 WIN！")
chk("ModelDb.Card<Abundance>()" not in r5.split("class PacManPower")[1], "不再给富足")
chk("疯狂进食" in Z["STS2_MOMOI_CARD_PAC_MAN.description"], "其他效果没动")

print("== 8. 复盘 ==")
gr = body(ca, "GameReview")
chk("public GameReview() : base(1, CardType.Skill" in gr, "1 费技能")
chk("TargetType.Self" in gr, "不再是敌方目标")
chk("DamageCmd" not in gr, "删去伤害")
chk("no DamageVar here" not in gr and "CalculationBaseVar" not in gr, "不再有伤害变量")
chk("PileType.Exhaust" in gr and "Add(card, PileType.Hand" in gr, "保留消耗堆回手")
chk("{IfUpgraded:show:[gold]升级并[/gold]|}" in Z["STS2_MOMOI_CARD_GAME_REVIEW.description"], "升级仍只影响那张牌")
chk("伤害" not in Z["STS2_MOMOI_CARD_GAME_REVIEW.description"], "卡面没有伤害了")

print("== 9. 黄金矿工死侧栏 ==")
chk("STS2_MOMOI_CARD_GOLD_MINER.sidebar2" not in Z, "zhs sidebar2 已删")
chk("STS2_MOMOI_CARD_GOLD_MINER.sidebar2" not in E, "eng sidebar2 已删")
chk("GOLD_MINER.sidebar2" not in code(os.path.join("Cards", "RemainingCards2.cs")), "代码里本来就没引用")
chk("金币" not in json.dumps(Z, ensure_ascii=False) or "金币" in Z["STS2_MOMOI_CARD_RANK_UP.description"],
    "金币只剩终于上一档了（金色）")

print("== 10. 标签闭合 ==")
bad = []
for lang in ("zhs", "eng"):
    for f in os.listdir(os.path.join(LOC, lang)):
        if not f.endswith(".json"):
            continue
        d = load(lang, f[:-5])
        for k, v in d.items():
            if not isinstance(v, str):
                continue
            for tag in set(re.findall(r"\[([a-z]+)\]", v)):
                if v.count("[%s]" % tag) != v.count("[/%s]" % tag):
                    bad.append("%s/%s/%s[%s]" % (lang, f, k, tag))
chk(not bad, "标签全部闭合", bad[:6])

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
