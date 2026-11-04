# -*- coding: utf-8 -*-
"""批次21 自检：阿比舒 3 段、曳光弹数值、两张卡的费。"""
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
a2 = code(os.path.join("Cards", "AssistCards2.cs"))
ff = code(os.path.join("Cards", "FirepowerFlowCards.cs"))

print("== 1. 系统：阿比舒 = 3 段 ==")
ab = body(a2, "SystemAbishu")
chk("for (int i = 0; i < 2; i++)" in ab, "第 1 段用循环打 2 次")
chk(ab.count("attackContext.AddHit(await CreatureCmd.Damage(") == 2
    or ab.count("attackContext.AddHit(") == 2, "共 2 处 AddHit（循环里 1 处 + 最后 1 处）",
    ab.count("attackContext.AddHit("))
chk("CreatureCmd.Damage 每次只结算**一次**伤害" in ab, "注释写明了为什么必须调两次")
chk("public SystemAbishu() : base(1," in ab, "费用 0 -> 1")
chk("_finalHit" in ab and "? 4m : 1m" in ab, "第 3 段仍是乘法 ×4")

print("== 2. 曳光弹 ==")
fb = body(ff, "FlameBullet")
chk("new CalculationBaseVar(6m)" in fb, "基础伤害 6（升级 8）")
chk("DynamicVars.CalculationBase.UpgradeValueBy(2)" in fb, "升级 +2")
chk('new DynamicVar("BurnBase", 3m)' in fb, "基础灼烧 3")
chk('DynamicVars["BurnBase"].UpgradeValueBy(1)' in fb, "升级灼烧 +1（3 -> 4）")
chk("vigor.Amount / 2" not in fb, "不再按每 2 点活力")
chk("return vigor != null ? vigor.Amount : 0;" in fb, "改为每 1 点活力 +1 层")
z = Z["STS2_MOMOI_CARD_FLAME_BULLET.description"]
chk("每有1点[gold]活力[/gold]，额外给予1层[gold]灼烧[/gold]。" in z, "zhs 文本", z)
chk("{CalculatedDamage:diff()}" in z and "{CalculatedBurn:diff()}" in z, "两个变量都在")
e = E["STS2_MOMOI_CARD_FLAME_BULLET.description"]
chk("For every 1 [gold]Vigor[/gold], apply 1 additional [gold]Burn[/gold]." in e, "eng 文本")

print("== 3. 来自时的援助 ==")
chk("public MomoiSupportToki() : base(0," in a2, "费用 2 -> 0")
tk = body(a2, "MomoiSupportToki")
chk("Apply<SystemAbishu>" in tk or "SystemAbishu" in tk, "仍然是给系统：阿比舒的卡")

print("== 4. 标签闭合 ==")
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
