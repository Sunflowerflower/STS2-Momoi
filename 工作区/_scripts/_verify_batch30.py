# -*- coding: utf-8 -*-
"""批次30 自检：专注 1→0 费、卡面/power 文本合成一句、天马行空升级版补「+1」。"""
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
PZ, PE = load("zhs", "powers"), load("eng", "powers")
rc3 = open(os.path.join(CODE, "Cards", "RemainingCards3.cs"), encoding="utf-8").read()

print("== 1. 专注：1 费 / 升级 0 费 ==")
fo = body(rc3, "Focus")
chk("public Focus() : base(1, CardType.Power" in fo, "基础 1 费")
chk("EnergyCost.UpgradeBy(-1)" in fo, "升级 -1 -> 0 费")

print("== 2. 专注卡面：一句（A/B，X/Y）==")
z = Z["STS2_MOMOI_CARD_FOCUS.description"]
want = ("在你的回合结束时，若你本回合没有打出过[gold]小游戏牌[/gold]/[gold]构想[/gold]，"
        "使[gold]构想[/gold]数值+1/选择最多[gold]构想[/gold]数值张牌[gold]保留[/gold]。")
chk(z == want, "zhs 与要求逐字一致", z)
chk("\n" not in z, "只有一句（没有换行）")
chk(z.count("在你的回合结束时") == 1, "「在你的回合结束时」只出现一次")
chk("[gold]小游戏牌[/gold]/[gold]构想[/gold]" in z, "「小游戏牌/构想」合在一起")
chk("数值+1/选择最多" in z, "「+1/选择最多」合在一起")
chk("[gold]手牌[/gold]" not in z, "按新措辞去掉了「手牌」")
e = E["STS2_MOMOI_CARD_FOCUS.description"]
chk("\n" not in e and "Minigame[/gold] card / a [gold]Concept" in e, "eng 同样一句", e)

print("== 3. 专注 power：一句 + 关键词 + 实际数值 ==")
pz = PZ["STS2_MOMOI_POWER_FOCUS_POWER.description"]
chk("\n" not in pz and pz.count("在你的回合结束时") == 1, "power 也是一句")
chk("[gold]小游戏牌[/gold]/[gold]构想[/gold]" in pz, "power 的「小游戏牌/构想」")
chk("[blue]{Amount}[/blue]" in pz, "构想 +N 用 Amount")
chk("[blue]{RetainCount}[/blue]" in pz, "「最多 N 张」用 RetainCount（显示实际数值）")
chk("[gold]保留[/gold]" in pz, "保留染金")
pe = PE["STS2_MOMOI_POWER_FOCUS_POWER.description"]
chk("{Amount}" in pe and "{RetainCount}" in pe and "\n" not in pe, "eng 变量与单句", pe)

print("== 4. 天马行空：升级版才有 +1 ==")
z = Z["STS2_MOMOI_CARD_BULLET_RAIN.description"]
chk("额外攻击等同[gold]构想[/gold]数值{IfUpgraded:show:+1|}次" in z, "zhs 升级分支补 +1", z)
chk("（额外攻击{ExtraHits:diff()}次）" in z, "括号里的实际次数没动")
e = E["STS2_MOMOI_CARD_BULLET_RAIN.description"]
chk("count{IfUpgraded:show: +1|}" in e, "eng 升级分支补 +1", e)
br = open(os.path.join(CODE, "Cards", "RemainingCards5.cs"), encoding="utf-8").read()
if "class BulletRain" not in br:
    import glob
    for f in glob.glob(os.path.join(CODE, "Cards", "*.cs")):
        t = open(f, encoding="utf-8").read()
        if "class BulletRain" in t:
            br = t
            break
bb = body(br, "BulletRain")
chk('DynamicVars["HitsBase"].UpgradeValueBy(1)' in bb, "实际效果本来就是升级 +1 次（未改动）")
chk("new DynamicVar(\"HitsBase\", 0m)" in bb, "升级前没有 +1（HitsBase = 0）")

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
