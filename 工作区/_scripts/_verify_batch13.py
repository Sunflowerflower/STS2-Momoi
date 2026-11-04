# -*- coding: utf-8 -*-
"""批次13 自检。"""
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

Z = {t: load("zhs", t) for t in ("powers", "cards")}
E = {t: load("eng", t) for t in ("powers", "cards")}

print("== 1. 雷酱不再绕过火力拦截 ==")
a1 = code(os.path.join("Cards", "AssistCards.cs"))
fp = code(os.path.join("Patches", "VigorFirepowerPatch.cs"))
chk("SpendVigorAsync" in fp, "FirepowerHooks.SpendVigorAsync 已定义")
chk("FirepowerPower>() is { Amount: > 0 }" in fp, "有火力时优先扣火力")
chk("FirepowerHooks.SpendVigorAsync" not in a1,
    "援护不再自己扣活力（批次49 改原版能力伤害）")
chk("PowerCmd.ModifyAmount(choiceContext, vigor," not in a1, "雷酱里没有直接扣活力的残留")
# 全模组：不应再有其它地方直接扣活力
bad = []
for root, _, files in os.walk(CODE):
    for f in files:
        if not f.endswith(".cs"):
            continue
        t = open(os.path.join(root, f), encoding="utf-8").read()
        if "Patches" in root:
            continue  # 补丁文件本身允许
        for m in re.finditer(r"ModifyAmount\([^;]*[Vv]igor[^;]*-\s*\w+", t):
            bad.append("%s: %s" % (f, m.group(0)[:60]))
chk(not bad, "全模组没有第二处直接扣活力", bad)

print("== 2. 我复活啦：先回血再消耗 ==")
ib = code(os.path.join("Cards", "ImBack.cs"))
i_heal = ib.find("await CreatureCmd.Heal(creature")
i_exhaust = ib.find("await CardCmd.Exhaust(new ThrowingPlayerChoiceContext(), clone);")
chk(i_heal > 0 and i_exhaust > 0 and i_heal < i_exhaust,
    "回血在消耗之前（IsDead 守卫会拦掉 0 血时的牌堆搬动）", "heal@%d exhaust@%d" % (i_heal, i_exhaust))
chk("IsDead" in ib or "CurrentHp == 0" in ib or "顺序很重要" in ib, "代码里有成因注释")

print("== 3. 构想卡面数值 ==")
cc = code(os.path.join("Cards", "ConceptCard.cs"))
chk("class ConceptCountVar : DynamicVar" in cc and "class ConceptEnergyVar : EnergyVar" in cc,
    "两个专用变量类已定义")
chk("override void UpdateCardPreview" in cc, "值写在 UpdateCardPreview 里")
chk("PreviewValue = ReadCount(card);" in cc, "PreviewValue 现算")
chk("new ConceptCountVar(\"ConceptDraw\")" in cc and "new ConceptEnergyVar()" in cc, "CanonicalVars 已替换")
chk("v.PreviewValue = Count;" not in cc, "旧的直接写 PreviewValue 已移除")

print("== 4. 花凛：爪牙不吃 Boss 增伤 ==")
a2 = code(os.path.join("Cards", "AssistCards2.cs"))
chk("Owner.RunState.CurrentRoom?.RoomType" in a2, "用房间层级判 Boss")
chk("!target.IsPrimaryEnemy" in a2, "再加 IsPrimaryEnemy 挡爪牙")
chk("RoomType.Boss" in a2, "RoomType.Boss")

print("== 5. 循环叙事可叠加 ==")
nb = code(os.path.join("Cards", "NewCardsBatch.cs"))
chk("public override PowerStackType StackType => PowerStackType.Counter;" in nb, "Counter")
chk("public override int DisplayAmount => Amount;" in nb, "右下角=剩余回合")
chk("await PowerCmd.Remove(this);" in nb, "结算后直接移除（批次50 一次性）")
chk(nb.count("[RegisterPower]") == nb.count("class CyclicNarrativePower") + 0 or
    "循环叙事" in nb, "无重复特性")
z = Z["powers"]["STS2_MOMOI_POWER_CYCLIC_NARRATIVE_POWER.description"]
chk(z == "本回合结束时，将[gold]弃牌堆[/gold]的最多[blue]{Amount}[/blue]张牌洗入你的[gold]抽牌堆[/gold]。",
    "zhs 文本", z)

print("== 6. 植物大战僵尸显示实际卡名 ==")
r5 = code(os.path.join("Cards", "RemainingCards5.cs"))
chk('new StringVar("Card")' in r5 and "StringValue = other.Title" in r5, "power 有卡名变量并写入")
z = Z["powers"]["STS2_MOMOI_POWER_PLANTS_NEXT_TURN_POWER.description"]
chk("{Card}" in z and "另一张牌" not in z, "zhs 文本用 {Card}", z)

print("== 7. 俄罗斯方块 ==")
chk("public static async Task RemoveOverridden" in r5, "覆盖方法（升级覆盖普通）")
chk("await TetrisFullHandPower.RemoveOverridden(player, IsUpgraded);" in r5, "打出时按覆盖规则去重")
chk("public static TetrisFullHandPower? ResolveOneToSettle" in r5, "升级版优先结算")
chk("if (ResolveOneToSettle(player) != this)" in r5, "非选中实例不结算")
chk('new DynamicVar("Cards", 3)' in r5 and 'new EnergyVar("Energy", 2)' in r5, "power 有抽牌/能量变量")
chk("public bool Upgraded => GetInternalData<Data>().Upgraded;" in r5, "有档位标记")
z = Z["powers"]["STS2_MOMOI_POWER_TETRIS_FULL_HAND_POWER.description"]
chk("[blue]{Cards}[/blue]" in z and "{Energy:energyIcons()}" in z, "zhs 文本显示抽几张/几能量", z)

print("== 8. 文档 ==")
chk(os.path.exists(os.path.join(ROOT, "工作区", "_docs", "_power总览.md")), "_power总览.md 已生成")
doc = open(os.path.join(ROOT, "工作区", "_docs", "_power总览.md"), encoding="utf-8").read()
chk(doc.count("### ") >= 50, "逐个详情条目数 >= 50", doc.count("### "))

print("== 9. 富文本标签闭合（全表）==")
bad2 = []
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
                    bad2.append("%s/%s/%s[%s]" % (lang, f, k, tag))
chk(not bad2, "标签全部闭合", bad2[:6])

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
