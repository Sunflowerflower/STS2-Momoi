# -*- coding: utf-8 -*-
"""批次15 自检。"""
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

def load(lang, table):
    return json.load(open(os.path.join(LOC, lang, table + ".json"), encoding="utf-8"))

def cls_body(src, cls):
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

Z, E = load("zhs", "cards"), load("eng", "cards")
misc = code(os.path.join("Cards", "MiscRareCards.cs"))
a2 = code(os.path.join("Cards", "AssistCards2.cs"))
m3 = code(os.path.join("Cards", "Match3.cs"))
cs = code("CombatStats.cs")

print("== 1. 集结减费 ==")
r = cls_body(misc, "Rally")
chk("TryModifyEnergyCostInCombat" in r, "用现算 hook")
chk("CombatStats.SupportCardsPlayed" in r, "读实时支援牌计数")
chk(not [l for l in r.split("\n") if "AddThisCombat" in l and not l.strip().startswith("//")],
    "不再用会累加的 AddThisCombat")
chk("AfterCardChangedPiles" not in r, "不再在换堆时改状态（避免 UI 报错）")

print("== 2. 贪吃蛇注册重复 ==")
r4 = code(os.path.join("Cards", "RemainingCards4.cs"))
i = r4.find("public sealed class SnakeGamePower")
head = r4[max(0, i - 700):i]
chk(head.count("[RegisterPower]") == 1, "只剩一个 [RegisterPower]", head.count("[RegisterPower]"))
dup = []
for root, _, files in os.walk(CODE):
    for f in files:
        if not f.endswith(".cs"):
            continue
        t = open(os.path.join(root, f), encoding="utf-8").read()
        for m in re.finditer(r"\bclass\s+([A-Za-z_]\w*)", t):
            # 只看紧邻类声明的属性块：遇到非属性行（包括上一个类的 }）就停
            lines = t[:m.start()].split("\n")
            attrs = []
            for l in reversed(lines):
                ls = l.strip()
                if ls.startswith("///") or ls.startswith("//") or ls == "":
                    continue
                if ls.startswith("["):
                    attrs.append(ls.split("(")[0])
                    continue
                break
            d = [a for a in set(attrs) if attrs.count(a) > 1]
            if d:
                dup.append("%s %s %s" % (f, m.group(1), d))
chk(not dup, "全仓无重复注册特性", dup[:4])

print("== 3. 格挡预览与实际一致 ==")
BAD = {
    "AssistCards.cs": ["MomoiSupportKotori"],
    "CommonAttackCards.cs": ["RollAndShoot", "AllsWellThatEndsWell", "MailCare"],
    "FirepowerFlowCards.cs": ["GearUp"],
    "IntentCards.cs": ["Countermeasure"],
    "MinigameFlowCards.cs": ["PostQuest"],
    "RemainingCards3.cs": ["TravelFrog"],
    "RemainingSpecialCards.cs": ["Encounter"],
    "ReworkBatch.cs": ["FlowState"],
}
for f, classes in BAD.items():
    src = code(os.path.join("Cards", f))
    for c in classes:
        body = cls_body(src, c)
        chk("new BlockVar(" in body and 'new DynamicVar("Block"' not in body, "%s 用 BlockVar" % c)
        chk("DynamicVars.Block, cardPlay" in body, "%s GainBlock 用 DynamicVars.Block" % c)
# 全仓再扫一遍残留
left = []
for root, _, files in os.walk(CODE):
    for f in files:
        if not f.endswith(".cs"):
            continue
        t = open(os.path.join(root, f), encoding="utf-8").read()
        if 'new DynamicVar("Block"' in t and 'new BlockVar(DynamicVars["Block"].BaseValue' in t:
            left.append(f)
chk(not left, "没有残留的 DynamicVar(Block)+BlockVar(BaseValue) 组合", left)

print("== 4. 消消乐消耗 ==")
m3b = cls_body(m3, "Match3")
chk("skipVisuals: true" not in m3b and "null, null)).FirstOrDefault()" in m3b,
    "消消乐改为 source:null（当场完成选牌收尾），不再跳过动画")

print("== 5. 系统：阿比舒 ==")
a = cls_body(a2, "SystemAbishu")
chk("new DamageVar(1m, ValueProp.Move)" in a, "基础 1（DamageVar）")
chk("DynamicVars.Damage.UpgradeValueBy(1m)" in a, "升级 3")
chk('new DynamicVar("Growth", 1m)' in a, "Growth 变量")
chk('DynamicVars["Growth"].UpgradeValueBy(1m)' not in a, "Growth 不随升级变化（固定 +1）")
chk("BuffFromAbishuPlay" in a and "PlayerCombatState.AllCards.OfType<SystemAbishu>()" in a,
    "爪击写法：遍历本场同类型卡逐张加伤")
chk("AddAbishuBonus" not in cs, "CombatStats 里的旧加成已删")

print("== 6. 小玉 power 图标 ==")
chk(os.path.exists(os.path.join(MOD, "images", "powers", "kotama_strength_power.png")), "图标已放入 images/powers")
k = cls_body(a2, "KotamaStrengthPower")
chk("IModPowerAssetOverrides" in k, "实现 IModPowerAssetOverrides")
chk("kotama_strength_power.png" in k, "指向新图标")
chk("TemporaryStrengthPower" in k, "仍继承原版临时力量基类")

print("== 7. 注能改为卡牌自带 ==")
d = cls_body(code(os.path.join("Cards", "RemainingSpecialCards.cs")), "DevGreen")
chk("AfterAutoPrePlayPhaseEntered" in d, "卡里覆写了自动打出钩子")
chk("_imbuedApplied" in d and "ImbuedSupport.TryAutoPlayAsync(choiceContext, this" in d,
    "注能：AutoPlay 自动打出 + 只打一次（批次45 回退直接结算）")
chk("CardCmd.Enchant" not in d, "不再挂附魔")
chk("ImbuedSupport.ImbuedTip" in d, "保留注能词条的侧栏")
chk("class MomoiImbued" not in code(os.path.join("Cards", "RemainingSpecialCards.cs")), "附魔类已删")
chk(not os.path.exists(os.path.join(MOD, "images", "enchantments")), "附魔图标目录已删")
chk(os.path.exists(os.path.join(LOC, "zhs", "enchantments.json")), "注能词条保留")
zc = Z["STS2_MOMOI_CARD_DEV_GREEN.description"]
chk("[gold]注能[/gold]" in zc, "卡面仍显示「注能」")

print("== 8. 循环叙事卡牌文本回滚 ==")
zc = Z["STS2_MOMOI_CARD_CYCLIC_NARRATIVE.description"]
chk("重复打出可以叠加持续回合数" not in zc, "去掉了多余的说明", zc)
chk(zc == "[gold]注能[/gold]。\n本回合结束时，将[gold]弃牌堆[/gold]的最多1张牌洗入你的[gold]抽牌堆[/gold]。",
    "文本还原", zc)

print("== 9. 标签闭合（全表）==")
bad = []
for lang in ("zhs", "eng"):
    for f in os.listdir(os.path.join(LOC, lang)):
        if not f.endswith(".json"):
            continue
        dd = load(lang, f[:-5])
        for k, v in dd.items():
            if not isinstance(v, str):
                continue
            for tag in set(re.findall(r"\[([a-z]+)\]", v)):
                if v.count("[%s]" % tag) != v.count("[/%s]" % tag):
                    bad.append("%s/%s/%s[%s]" % (lang, f, k, tag))
chk(not bad, "标签全部闭合", bad[:6])

print("== 10. 无裸数字（power/cards 描述）==")
bad2 = []
for lang in ("zhs", "eng"):
    dd = load(lang, "powers")
    for k, v in dd.items():
        if not k.endswith(".description"):
            continue
        s = re.sub(r"\[blue\][^[]*?\[/blue\]|\[green\][^[]*?\[/green\]", "", v)
        s = re.sub(r"\{[^}]*\}", "", s)
        s = re.sub(r"\[[a-z/]+\]", "", s)
        if re.search(r"\d+%?", s):
            bad2.append("%s/%s" % (lang, k))
chk(not bad2, "power 无裸数字", bad2[:6])

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
