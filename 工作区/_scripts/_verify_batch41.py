# -*- coding: utf-8 -*-
"""批次41 自检：创作的痛苦删火力 + 多段攻击合成单条命令（活力/火力只消耗一次）+ 全卡扫描。"""
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


def read(*parts):
    return open(os.path.join(CODE, *parts), encoding="utf-8").read()


def body(src, cls):
    m = re.search(r"\bclass\s+" + cls + r"\b", src)
    if not m:
        return ""
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
creative = read("Cards", "CreativePain.cs")
hundred = read("Cards", "HundredPull.cs")

print("== 1. 创作的痛苦：删去火力 ==")
cp = body(creative, "CreativePain")
chk("Firepower" not in cp, "类里没有 Firepower 变量/施加")
chk("PowerCmd.Apply<BurnPower>" in cp, "灼烧仍在")
chk("Firepower" not in Z["STS2_MOMOI_CARD_CREATIVE_PAIN.description"], "zhs 文本已删火力行")
chk("Firepower" not in E["STS2_MOMOI_CARD_CREATIVE_PAIN.description"], "eng 文本已删火力行")
chk(Z["STS2_MOMOI_CARD_CREATIVE_PAIN.description"].startswith("对所有敌人造成"), "首行变成伤害")

print("== 2. 创作的痛苦：三段 = 一条命令（活力/火力只消耗一次）==")
chk("WithHitCount(3)" in cp, "WithHitCount(3)")
chk("WithWaitBeforeHit(0.5f, 0.5f)" in cp, "段间 0.5s 间隔（WithWaitBeforeHit）")
chk("for (var hit = 0; hit < 3" not in cp, "不再 for 循环发多条命令")
chk(cp.count("DamageCmd.Attack(") == 1, "只有一条 AttackCommand")
chk("ApplyBarrage" in cp, "弹幕特效仍走 ApplyBarrage（每段一次）")
chk(".OnlyPlayAnimOnce()" not in cp, "没有加 OnlyPlayAnimOnce（否则每段弹幕只会播一次）")
chk("persistent: true" in cp, "旋风仍是 persistent")

print("== 3. 100连抽：100 段也合成一条命令 ==")
chk("WithHitCount(DynamicVars.Repeat.IntValue)" in hundred, "WithHitCount(Repeat)")
chk("OnlyPlayAnimOnce()" in hundred, "只播一次攻击动画")
chk("for (int i = 0; i < DynamicVars.Repeat.IntValue" not in hundred, "不再 for 循环 100 条命令")
chk(hundred.count("DamageCmd.Attack(") == 1, "只有一条 AttackCommand")

print("== 4. 全卡扫描：没有别的卡在一次打出里发多条攻击命令 ==")
bad = []
for f in glob.glob(os.path.join(CODE, "Cards", "*.cs")):
    src = open(f, encoding="utf-8").read()
    for m in re.finditer(r"\bclass\s+(\w+)\s*:\s*ModCardTemplate", src):
        seg = body(src, m.group(1))
        n = seg.count("DamageCmd.Attack(")
        loop_attack = re.search(r"(for|foreach)\s*\([^)]*\)\s*\{[^{}]*DamageCmd\.Attack\(", seg, re.S)
        if n > 1 and "else if" not in seg and "else" not in seg:
            bad.append((m.group(1), "多条 AttackCommand"))
        if loop_attack:
            bad.append((m.group(1), "循环里发攻击命令"))
chk(not bad, "没有遗漏的多命令/循环攻击卡", bad)

print("== 5. 用 WithHitCount 的卡（正确写法）==")
for cls in ("MomoiSupportNeru", "FishingMaster", "ConfusedShot"):
    src = next((open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(CODE, "Cards", "*.cs"))
                if f"class {cls}" in open(p, encoding="utf-8").read()), "")
    chk("WithHitCount(" in body(src, cls), f"{cls} 用 WithHitCount（本来就正确）")

print("== 6. 标签闭合 ==")
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
