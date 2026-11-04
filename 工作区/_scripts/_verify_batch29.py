# -*- coding: utf-8 -*-
"""批次29 自检：跑酷删 power、七张卡数值、两张卡稀有度、专注重做。"""
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

r4 = code(os.path.join("Cards", "RemainingCards4.cs"))
r3 = code(os.path.join("Cards", "RemainingCards3.cs"))
rs = code(os.path.join("Cards", "RemainingSpecialCards.cs"))
fa = code(os.path.join("Cards", "FlameAttach.cs"))
cf = code(os.path.join("Cards", "ConceptFlowCards.cs"))
mf = code(os.path.join("Cards", "MinigameFlowCards.cs"))
ff = code(os.path.join("Cards", "FirepowerFlowCards.cs"))
ca = code(os.path.join("Cards", "CommonAttackCards.cs"))

print("== 1. 跑酷：后半段与 power 整体删除 ==")
chk("ParkourPower" not in r4, "两个 power 类已删除")
chk("ParkourPowerBase" not in r4, "基类已删除")
chk("PowerCmd.Apply<Parkour" not in r4, "OnPlay 不再施加 power")
chk("repeat this" not in E["STS2_MOMOI_CARD_PARKOUR.description"].lower(), "eng 后半段已删")
chk("重复此效果" not in Z["STS2_MOMOI_CARD_PARKOUR.description"], "zhs 后半段已删")
chk("STS2_MOMOI_POWER_PARKOUR_POWER.description" not in PZ, "power 本地化键已删")
chk("STS2_MOMOI_POWER_PARKOUR_UPGRADED_POWER.title" not in PE, "eng power 本地化键已删")
chk(not os.path.exists(os.path.join(MOD, "images", "powers", "parkour_power.png")), "死图标已删")
chk("CardKeyword.Exhaust" in body(r4, "Parkour"), "仍是一次性（消耗）")
chk("选择最多一张" in Z["STS2_MOMOI_CARD_PARKOUR.description"], "「最多一张」保留")

print("== 2. 数值 ==")
chk('new EnergyVar(3)  // 升级 4' in rs and 'DynamicVars["Energy"].UpgradeValueBy(1);' in rs,
    "WIN！能量 3 / 升级 4")
chk('new DynamicVar("Burn", 2)' in fa and "灼烧 2 -> 3" in fa, "火焰附加灼烧 2 / 升级 3")
chk('new DynamicVar("Firepower", 2),  // 升级 3' in ff, "热火热力 2 / 升级 3")
chk('new DynamicVar("Damage", 11)  // 升级 15' in cf, "构想之矛 11 / 升级 15（批次40）")
chk('DynamicVars["Damage"].UpgradeValueBy(4)' in cf, "构想之矛升级 +4")
chk("new CalculationBaseVar(5m),  // 升级 7" in ca, "博览群游 5 / 升级 7（批次44）")
chk("ForcePlaceholder" == "x" or "DynamicVars.CalculationBase.UpgradeValueBy(2);   // 5 -> 7" in ca, "博览群游升级 +2")
chk('new DynamicVar("Vigor", 3),          // 升级 4' in cf, "再起新篇活力 3 / 升级 4")

print("== 3. 稀有度 ==")
chk("public BottleneckBreak() : base(2, CardType.Attack, CardRarity.Common" in cf, "瓶颈突破 -> 普通")
chk("public Salvage() : base(1, CardType.Skill, CardRarity.Uncommon" in mf, "玩玩新作！ -> 罕见")

print("== 4. 专注重做 ==")
fo = body(r3, "Focus")
chk("public Focus() : base(1, CardType.Power" in fo, "1 费（升级 0，批次30 修正）")
chk("EnergyCost.UpgradeBy(-1)" in fo, "升级 -1 -> 0 费")
fp = body(r3, "FocusPower")
chk("PlayedMinigameThisTurn" in fp and "PlayedConceptThisTurn" in fp, "改成「本回合是否打出过」标记")
chk("TurnsNoMinigame" not in fp and "TurnsNoConcept" not in fp, "旧的「连续 N 回合」计数已删")
chk("if (!data.PlayedConceptThisTurn && player != null)" in fp, "保留：本回合没打构想")
chk("if (!data.PlayedMinigameThisTurn && player != null)" in fp, "构想 +1：本回合没打小游戏牌")
chk("data.PlayedMinigameThisTurn = false;" in fp and "data.PlayedConceptThisTurn = false;" in fp,
    "回合结束重置标记")
z = Z["STS2_MOMOI_CARD_FOCUS.description"]
chk(chr(10) not in z, "卡面合成一句（批次30）")
chk("小游戏牌[/gold]/[gold]构想" in z and "数值+1/选择最多" in z, "「A/B，X/Y」结构", z)
chk("连续" not in z, "卡面不再提连续")
pz = PZ["STS2_MOMOI_POWER_FOCUS_POWER.description"]
chk("连续" not in pz, "power 文本不再提连续")
chk("本回合" in pz, "power 文本改成本回合")
chk("[gold]小游戏牌[/gold]" in pz and "[gold]构想[/gold]" in pz and "[gold]保留[/gold]" in pz,
    "power 文本关键词都染了金")
chk("{Amount}" in pz and "{RetainCount}" in pz, "power 变量都在")
pe = PE["STS2_MOMOI_POWER_FOCUS_POWER.description"]
chk("this turn" in pe and "[gold]Minigame[/gold]" in pe, "eng power 文本同步")

print("== 5. 标签闭合 ==")
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
