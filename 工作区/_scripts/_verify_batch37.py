# -*- coding: utf-8 -*-
"""批次37 自检：九张卡数值 + 三处费用/关键词 + 自助指南附魔（GainsBlock）与事件文本兜底。"""
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
r3 = read("Cards", "RemainingCards3.cs")
r4 = read("Cards", "RemainingCards4.cs")
r5 = read("Cards", "RemainingCards5.cs")
a1 = read("Cards", "AssistCards.cs")
a2 = read("Cards", "AssistCards2.cs")
m3 = read("Cards", "Match3.cs")

print("== 1. 节奏游戏 18/24 + 每方块 6/4 ==")
rg = body(r5, "RhythmGame")
chk('new DynamicVar("Damage", 18)' in rg and "// 升级 20" in rg, "卡：18/20（批次44）")
chk('new DynamicVar("PerBlock", 6)' in rg and "// 升级 5" in rg, "卡：每方块 6/5（批次44）")
chk('DynamicVars["Damage"].UpgradeValueBy(2);' in rg, "升级 +2")
chk('DynamicVars["PerBlock"].UpgradeValueBy(-1);' in rg, "升级 -1")
rgp = body(r5, "RhythmGamePower")
chk("? 20 : 18" in rgp and "? 5 : 6" in rgp, "power 叠加也按 18/20 + 6/5")

print("== 2. 打灰机 格挡 6/8、抽牌 1/2 ==")
sh = body(r4, "Shmup")
chk("new BlockVar(6m, ValueProp.Move)" in sh and "// 升级 8" in sh, "格挡 6/8")
chk("new CardsVar(1)" in sh, "抽牌数用 CardsVar")
chk("DynamicVars.Cards.IntValue" in sh, "实际抽牌读变量")
chk('DynamicVars.Cards.UpgradeValueBy(1)' in sh, "升级 +1 -> 2")
chk("抽{Cards:diff()}张牌。" in Z["STS2_MOMOI_CARD_SHMUP.description"], "zhs 文本用变量")
chk("Draw {Cards:diff()}" in E["STS2_MOMOI_CARD_SHMUP.description"], "eng 文本用变量")

print("== 3. 消消乐 1/0 费、升级不给保留 ==")
chk("public Match3() : base(1, CardType.Skill" in m3, "基础 1 费")
chk("EnergyCost.UpgradeBy(-1);" in body(m3, "Match3"), "升级 1 -> 0")
chk("AddKeyword(CardKeyword.Retain)" not in m3, "不再加保留")
chk("AfterDowngraded" not in body(m3, "Match3"), "降级钩子一起删掉")

print("== 4. 植物大战僵尸 1/0 费 ==")
pvz = body(r5, "PlantsVsZombies")
chk("public PlantsVsZombies() : base(1, CardType.Skill" in pvz, "基础 1 费")
chk("EnergyCost.UpgradeBy(-1);" not in pvz, "升级不再减费（批次44：1/1）")

print("== 5. 六张援护数值 ==")
chk('new CalculationBaseVar(32m),  // 升级 40' in body(a2, "MomoiSupportKarin"), "花凛 32/40")
chk('new CalculationBaseVar(6m),  // 升级 9' in body(a2, "MomoiSupportHare"), "晴 6/9")
chk('UpgradeValueBy(3);   // 6 -> 9' in body(a2, "MomoiSupportHare"), "晴 升级 +3")
chk('new CalculationBaseVar(7m),  // 升级 10' in body(a2, "MomoiSupportChihiro"), "千寻 7/10")
chk('UpgradeValueBy(3);   // 7 -> 10' in body(a2, "MomoiSupportChihiro"), "千寻 升级 +3")
chk('new CalculationBaseVar(12m),  // 升级 15' in body(a2, "MomoiSupportAkira"), "茜 12/15")
chk('UpgradeValueBy(3);   // 12 -> 15' in body(a2, "MomoiSupportAkira"), "茜 升级 +3")
yo = body(a1, "MomoiSupportYoshimi")
chk("new BlockVar(3m, ValueProp.Move)" in yo and "// 升级 4" in yo, "大师 格挡 3/4")
chk("new CalculationBaseVar(4m)" in yo and "// 升级 6" in yo, "大师 伤害 4/6")
chk('new DynamicVar("Strength", 3)  // 升级 4' in body(a2, "MomoiSupportKotama"), "小玉 力量 3/4")

print("== 6. 自助指南附魔：会获得格挡的卡必须 override GainsBlock ==")
missing = []
for f in glob.glob(os.path.join(CODE, "Cards", "*.cs")):
    src = open(f, encoding="utf-8").read()
    for m in re.finditer(r"\bclass\s+(\w+)\s*:\s*ModCardTemplate", src):
        seg = body(src, m.group(1))
        if "GainBlock" in seg and "override bool GainsBlock" not in seg:
            missing.append(m.group(1))
chk(not missing, "所有会给格挡的卡都有 GainsBlock 标志", missing)
ALL_SRC = {p: open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(CODE, "Cards", "*.cs"))}
def has_flag(cls):
    for src in ALL_SRC.values():
        seg = body(src, cls)
        if seg:
            return "public override bool GainsBlock" in seg
    return False

for cls in ("STS2_MomoiDefend", "RollAndShoot", "MailCare", "GearUp", "Encounter", "FlowState",
            "PostQuest", "TravelFrog", "Shmup", "MomoiSupportKotori", "MomoiSupportYoshimi",
            "MomoiSupportYoshimi", "AllsWellThatEndsWell", "Countermeasure",
            "YellowBlock", "BlueBlock", "PurpleBlock", "GreenBlock"):
    chk(has_flag(cls), f"{cls} 有 GainsBlock")

print("== 7. 事件文本 / 角色文本兜底 ==")
ev_z, ev_e = load("zhs", "events"), load("eng", "events")
k = "COLORFUL_PHILOSOPHERS.pages.INITIAL.options.STS2_MOMOI"
chk(ev_z.get(k + ".title") == "桃红色", "色彩哲学家：桃红色标题", ev_z.get(k + ".title"))
chk("{Cards}" in (ev_z.get(k + ".description") or ""), "色彩哲学家：zhs 描述带 {Cards}")
chk(k + ".description" in ev_e, "色彩哲学家：eng 键在")
cz, ce = load("zhs", "characters"), load("eng", "characters")
ck = "STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER"
chk(ck + ".bestiaryQuote" in cz and ck + ".bestiaryQuote" in ce, "图鉴台词 bestiaryQuote 已补")
chk(ck + ".aromaPrinciple" in cz, "AromaOfChaos 用的 aromaPrinciple 在")
chk(ck + ".pronounSubject" in cz and ck + ".possessiveAdjective" in cz, "代词键在")
patch = read("Patches", "MomoiEnergyIconPathPatch.cs")
chk("EnergyIconHelper.GetPath" in patch, "能量图标路径兜底补丁存在")
chk("MomoiEnergyIconPathPatch" in read("Entry.cs"), "补丁已登记")

print("== 8. 标签闭合 ==")
bad = []
for lang in ("zhs", "eng"):
    for f in os.listdir(os.path.join(LOC, lang)):
        if not f.endswith(".json"):
            continue
        d = load(lang, f[:-5])
        for kk, v in d.items():
            if not isinstance(v, str):
                continue
            for tag in set(re.findall(r"\[([a-z]+)\]", v)):
                if v.count("[%s]" % tag) != v.count("[/%s]" % tag):
                    bad.append("%s/%s/%s[%s]" % (lang, f, kk, tag))
chk(not bad, "标签全部闭合", bad[:6])

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
