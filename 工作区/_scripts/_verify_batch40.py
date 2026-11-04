# -*- coding: utf-8 -*-
"""批次40 自检：本批所有卡牌改动 + 新卡「传送门悖论」「过载」+ 建筑师对打演出补丁。"""
import glob
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


ALL = {p: open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(CODE, "Cards", "*.cs"))}


def body(cls):
    for src in ALL.values():
        m = re.search(r"\bclass\s+" + cls + r"\b", src)
        if not m:
            continue
        brace = src.find("{", m.end())
        depth = 0
        for j in range(brace, len(src)):
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
PZ = load("zhs", "powers")

print("== 1. 消耗类改动（升级前消耗、升级后删去）==")
gr = body("GameReview")
chk("CardKeyword.Exhaust" in gr and "RemoveKeyword(CardKeyword.Exhaust);" in gr, "复盘：消耗 → 升级删去")
chk("AfterDowngraded" in gr, "复盘：降级恢复消耗")
kn = body("KingsNeverMeet")
chk("CardKeyword.Exhaust" in kn and "RemoveKeyword(CardKeyword.Exhaust);" in kn, "王不见王：消耗 → 升级删去")
chk("public KingsNeverMeet() : base(1, CardType.Skill" in kn, "王不见王：费 1/1")
chk("EnergyCost.UpgradeBy" not in kn, "王不见王：升级不再减费")

print("== 2. 稀有度 ==")
chk("CardRarity.Uncommon" in body("ForeshadowRecovery"), "伏笔回收 → 罕见")
chk("CardRarity.Rare" in body("HundredPull"), "100连抽！→ 稀有")

print("== 3. 费用 / 关键词 ==")
cn = body("CyclicNarrative")
chk("public CyclicNarrative() : base(1, CardType.Skill, CardRarity.Uncommon" in cn,
    "循环叙事 1 费技能罕见（批次49）")
chk("EnergyCost.UpgradeBy(-1);" in cn, "循环叙事：升级减 1 费")
lb = body("LearnByDoing")
chk("public LearnByDoing() : base(3, CardType.Power" in lb, "日复一日 3 费")
chk("EnergyCost.UpgradeBy(-1);" not in lb, "日复一日 3/3（批次46 升级不减费）")
chk("CanonicalKeywords => new() { CardKeyword.Retain }" in lb, "日复一日 保留在 CanonicalKeywords（不会重复）")
chk("LocalKeywords.Add(CardKeyword.Retain)" not in lb, "日复一日 升级里不再重复加保留")
chk("public PostQuest() : base(2, CardType.Skill" in body("PostQuest"), "发布委托 2/2 费")
chk("public PlayWithFire() : base(2, CardType.Attack" in body("PlayWithFire"), "局势升温 2/2 费")
chk("public GoldMiner() : base(0, CardType.Skill" in body("GoldMiner"), "黄金矿工 0 费（批次46）")
chk("EnergyCost.UpgradeBy" not in body("GoldMiner"), "黄金矿工 0/0（升级只给保留）")
chk("public AngryBirds() : base(1, CardType.Skill" in body("AngryBirds"), "愤怒的小鸟 1/1 费")

print("== 4. 数值 ==")
chk("new BlockVar(11m, ValueProp.Move)  // 升级 14" in body("PostQuest"), "发布委托 11/14")
bo = body("BottleneckBreak")
chk('new DynamicVar("ConceptGain", 1)' in bo and 'DynamicVars["ConceptGain"].UpgradeValueBy(1)' in bo, "瓶颈突破 构想 1/2")
chk('DynamicVars["ConceptGain"].IntValue' in bo, "瓶颈突破 实际用变量")
chk('new DynamicVar("Damage", 11)  // 升级 15' in body("ConceptSpear"), "构想之矛 11/15")
chk("(upgraded ? 15 : 11)" in body("SpearShieldPower"), "矛与盾 伤害 11/15")
gu = body("GearUp")
chk("new BlockVar(4m, ValueProp.Move)" in gu and "// 升级 6" in gu, "整装待发 格挡 4/6（批次44）")
chk('new DynamicVar("Vigor", 2)' in gu and 'new DynamicVar("Firepower", 2)' in gu, "整装待发 活力/火力 2/3")
chk("new CalculationBaseVar(12m),  // 升级 16" in body("PlayWithFire"), "局势升温 12/16")
chk("Firepower" not in body("CreativePain"), "创作的痛苦：批次41 已删去火力效果")
chk("PowerCmd.Apply<FirepowerPower>" not in body("CreativePain"), "创作的痛苦：不再施加火力")

print("== 5. 再启新篇：只在没有构想时才加费 ==")
nc = body("NewChapter")
i_if = nc.find("if (!hasConcept)")
i_cost = nc.find("EnergyCost.SetThisCombat")
chk(i_if > 0 and i_cost > i_if, "费用增加写在「没有构想」分支里")
chk("EnergyCost.SetThisCombat" in nc[i_if:i_if + 900], "位置核对")

print("== 6. 扫雷：随机位置 ==")
chk("PileType.Draw, Owner, CardPilePosition.Random" in body("Minesweeper"), "炸弹洗到抽牌堆随机位置")
chk("CardPilePosition.Top" not in body("Minesweeper"), "不再放在顶部")

print("== 7. 博览群游：随机敌人 ==")
ec = body("ExperienceCombo")
chk("TargetType.RandomEnemy" in ec, "目标类型 随机敌人")
chk("TargetingRandomOpponents(combatState)" in ec, "结算走 TargetingRandomOpponents")
chk("随机对敌人造成{CalculatedDamage:diff()}点伤害" in Z["STS2_MOMOI_CARD_EXPERIENCE_COMBO.description"], "zhs 文本同步")

print("== 8. 新卡：传送门悖论 ==")
pp = body("PortalParadox")
chk(pp != "", "PortalParadox 类存在")
chk("public PortalParadox() : base(1, CardType.Skill, CardRarity.Uncommon" in pp, "1 费技能（罕见，批次44）")
chk("CardKeyword.Exhaust" in pp and "RemoveKeyword(CardKeyword.Exhaust);" in pp, "消耗 → 升级删去")
chk("HoverTipFactory.FromCard<PortalParadoxOne>(IsUpgraded)" in pp
    and "HoverTipFactory.FromCard<PortalParadoxTwo>(IsUpgraded)" in pp, "侧栏预览两张衍生牌")
chk("CardCmd.Upgrade(card);" in pp, "升级给升级过的衍生牌")
for cls in ("PortalParadoxOne", "PortalParadoxTwo"):
    b = body(cls)
    chk("CardRarity.Token" in b, f"{cls} 改成衍生（Token 稀有度）")
    chk("TokenCardPool" in ALL[[k for k, v in ALL.items() if f"class {cls}" in v][0]], f"{cls} 注册到 Token 池")
chk(os.path.exists(os.path.join(MOD, "images", "cards", "PortalParadox.png")), "卡面 = 其一 的图")
chk(Z["STS2_MOMOI_CARD_PORTAL_PARADOX.title"] == "传送门悖论", "标题")
chk("从两张牌中选择一张加入你的[gold]手牌[/gold]。" in Z["STS2_MOMOI_CARD_PORTAL_PARADOX.description"], "描述")

print("== 9. 新卡：过载 ==")
ol = body("Overload")
chk("public Overload() : base(2, CardType.Power, CardRarity.Uncommon" in ol, "2 费能力（罕见，批次44）")
chk('new DynamicVar("Firepower", 2)' in ol and 'new DynamicVar("Vigor", 2)' in ol, "火力 2/3、活力 2/3（批次44）")
chk("PowerCmd.Apply<OverloadPower>" in ol, "施加过载 power")
op = body("OverloadPower")
chk("PowerStackType.Counter" in op, "power 叠层（Amount 累加）")
chk("power is FirepowerPower" in op and "amount < 0" in op, "监听火力减少")
chk("PowerCmd.Apply<VigorPower>" in op, "获得活力")
chk(os.path.exists(os.path.join(MOD, "images", "cards", "Overload.png")), "过载卡面存在")
chk(os.path.exists(os.path.join(MOD, "images", "powers", "overload_power.png")), "过载 power 图标存在")
chk("每当你的[gold]火力[/gold]层数减少时，获得[blue]{Amount}[/blue]点[gold]活力[/gold]。"
    in PZ["STS2_MOMOI_POWER_OVERLOAD_POWER.description"], "power 文本")

print("== 10. 建筑师对打演出 ==")
patch = open(os.path.join(CODE, "Patches", "MomoiArchitectCutscenePatch.cs"), encoding="utf-8").read()
chk("TheArchitect" in patch and "LoadDialogue" in patch, "挂在 TheArchitect.LoadDialogue")
chk("ArchitectAttackers.Both" in patch and "ArchitectAttackers.Player" in patch, "补上攻击者配置")
chk("MomoiArchitectCutscenePatch" in open(os.path.join(CODE, "Entry.cs"), encoding="utf-8").read(), "补丁已登记")
char = open(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs"), encoding="utf-8").read()
chk("GetArchitectAttackVfx" in char and "vfx/vfx_attack_blunt" in char, "角色提供了攻击 vfx 路径")
an = load("zhs", "ancients")
chk(any(k.startswith("THE_ARCHITECT.talk.STS2_MOMOI") for k in an), "建筑师对话文本在")

print("== 11. 标签闭合 ==")
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
