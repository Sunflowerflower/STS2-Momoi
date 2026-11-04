# -*- coding: utf-8 -*-
"""批次35 自检：剧本打击括号跟着升级（0/1）、重整旗鼓阈值 20% -> 25%。"""
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
cf = open(os.path.join(CODE, "Cards", "ConceptFlowCards.cs"), encoding="utf-8").read()
rc3 = open(os.path.join(CODE, "Cards", "RemainingCards3.cs"), encoding="utf-8").read()

print("== 1. 剧本打击：括号里的抽牌数跟着升级走（0 张 / 1 张）==")
z = Z["STS2_MOMOI_CARD_SCRIPT_STRIKE.description"]
chk("（抽{ConceptCards:diff()}张牌）" in z, "zhs 括号用 ConceptCards", z)
chk("{InCombat:" in z, "括号内容改回「仅局内显示」（批次46 用户要求）")
chk("抽0张牌" not in z, "不再写死「抽0张牌」")
e = E["STS2_MOMOI_CARD_SCRIPT_STRIKE.description"]
chk("{ConceptCards:diff()}" in e and "{InCombat:" in e, "eng 同步（含 InCombat 包装）")

ss = body(cf, "ScriptStrike")
chk('new DynamicVar("CardsBase", 0m)' in ss, "CardsBase 基础 0")
chk('ConceptCounterCapability.GetMaxCountInHand(card.Owner.Creature))' in ss
    and "+ (card.IsUpgraded ? 1 : 0)" not in ss, "multiplier 只算构想数值（+1 不再写在 multiplier 里）")
chk('DynamicVars["CardsBase"].UpgradeValueBy(1)' in ss, "升级 CardsBase +1 -> 局外显示 1")
chk("Convert.ToInt32(DynamicVars[\"ConceptCards\"])" in ss, "实际抽牌仍读 ConceptCards")
chk('DynamicVars.CalculationBase.UpgradeValueBy(2);' in ss, "伤害升级 +2 未动")

print("== 2. 重整旗鼓：阈值 20% -> 25% ==")
ra = body(rc3, "RallyAgain")
chk("me.CurrentHp > me.MaxHp / 4" in ra, "卡：MaxHp / 4（25%）")
chk("me.MaxHp / 5" not in ra, "卡：旧的 / 5 已去掉")
chk("低于最大生命的 25% 才触发" in ra, "卡：注释同步")
rap = body(rc3, "RallyAgainPower")
chk("Owner.CurrentHp * 4 >= Owner.MaxHp" in rap, "power：* 4（25%）")
chk("Owner.CurrentHp * 5" not in rap, "power：旧的 * 5 已去掉")
chk("25%（原 20%）" in rap, "power：注释标了原值")
z = Z["STS2_MOMOI_CARD_RALLY_AGAIN.description"]
chk("当生命值低于25%时" in z, "zhs 文本 25%", z)
chk("20%" not in z, "zhs 不再有 20%")
e = E["STS2_MOMOI_CARD_RALLY_AGAIN.description"]
chk("below 25%" in e and "20%" not in e, "eng 文本 25%", e)
chk("回复已损生命的10%的生命" in z, "只改了阈值（其它效果没动）")
chk("立即将此牌打出，并额外获得1层[gold]无实体[/gold]" in z, "无实体那句没动")

print("== 3. 标签闭合 ==")
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
