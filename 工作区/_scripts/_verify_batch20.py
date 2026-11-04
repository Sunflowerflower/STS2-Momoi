# -*- coding: utf-8 -*-
"""批次20 自检：阿比舒 4 倍改乘法、来自勇者的加护 10 伤、消消乐首句，以及一次文件恢复的完整性核对。"""
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
rs = code(os.path.join("Cards", "RemainingSpecialCards.cs"))
m3 = code(os.path.join("Cards", "Match3.cs"))

print("== 1. 系统：阿比舒 ==")
ab = body(a2, "SystemAbishu")
chk("new DamageVar(1m, ValueProp.Move)" in ab, "基础伤害 1（升级 2）")
chk('new DynamicVar("Growth", 1m)' in ab, "Growth 1")
chk('DynamicVars["Growth"].UpgradeValueBy' not in ab, "Growth 不随升级变化")
chk("DynamicVars.Damage.UpgradeValueBy(1m)" in ab, "升级只加基础伤害 1 -> 2")
chk("_finalHit" in ab, "有最后一段的开关")
chk("cardSource == this && _finalHit ? 4m : 1m" in ab, "4 倍走 ModifyDamageMultiplicative（乘法修正）")
chk("AttackCommand.CreateContextAsync(combatState, choiceContext, cardPlay)" in ab, "整张牌一个 AttackContext")
chk(ab.count("attackContext.AddHit(") == 2, "两段命中都记进上下文", ab.count("attackContext.AddHit("))
chk(ab.count("CreatureCmd.Damage(choiceContext, targets, baseDamage, ValueProp.Move") == 2,
    "用 CreatureCmd.Damage 分两段（不是两次 AttackCommand.Execute）")
chk("baseDamage * 4" not in ab, "没有把面板数值乘 4")
chk("NHyperbeamVfx.Create" in ab and "NHyperbeamImpactVfx.Create" in ab, "最后一段用超能光束特效")
chk("await PlayHyperbeamVfx(combatState);" in ab, "特效只调一次")
z = Z["STS2_MOMOI_CARD_SYSTEM_ABISHU.description"]
chk("3次" in z and "4倍" in z and "{Damage:diff()}" in z, "卡面描述未变", z)

print("== 2. 来自勇者的加护：升级 10 伤 ==")
cb = body(rs, "CourageBoon")
chk("DynamicVars.CalculationBase.UpgradeValueBy(3)" in cb, "升级 +3（6 -> 9，批次46）")
chk("new CalculationBaseVar(6m)" in cb, "基础 6（批次46）")
chk("_finalMultiplier" in cb and "ModifyDamageMultiplicative" in cb, "伤害翻倍仍是乘法修正（参考实现）")

print("== 3. 消消乐首句 ==")
z = Z["STS2_MOMOI_CARD_MATCH3.description"]
plain = re.sub(r"\[/?[a-z]+\]", "", z)
chk(plain.startswith("选择任意张类型相同的牌消耗。"), "首句已缩短", plain)
chk("选择1张牌" not in plain, "不再提「选择1张牌」")
e = E["STS2_MOMOI_CARD_MATCH3.description"]
chk(e.startswith("Choose any number of cards with the same type"), "eng 同步", e[:60])

print("== 4. 文件恢复完整性（RemainingSpecialCards.cs）==")
chk("class MomoiImbued" not in rs, "附魔类仍是删除状态")
chk("ImbuedSupport.ImbuedTip" in rs, "注能侧栏仍在（统一到 ImbuedSupport）")
chk("AfterAutoPrePlayPhaseEntered" in rs, "注能效果仍在 DevGreen 卡里")
chk('new BlockVar(6m, ValueProp.Move)  // 升级 7' in rs, "相遇的 BlockVar 改动仍在（批次44：6/7）")
chk("DynamicVars.Block, cardPlay" in body(rs, "Encounter"), "相遇的 GainBlock 用 DynamicVars.Block")
chk("SetAmount(Math.Max(0, Amount - 1));" in rs, "能量保留的可叠加改动仍在")
chk("public override int DisplayAmount => Amount;" in body(rs, "DevSecretsPower")
    or "public override int DisplayAmount => (int)DynamicVars[\"Gain\"].BaseValue;" in body(rs, "DevSecretsPower"),
    "开发秘籍右下角语义仍在")
chk(rs.count("\n") + 1 > 900, "文件行数正常（未截断）", rs.count("\n") + 1)

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
