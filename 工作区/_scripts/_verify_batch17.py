# -*- coding: utf-8 -*-
"""批次17 自检。"""
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

Z, E = load("zhs", "cards"), load("eng", "cards")

print("== 1. 消消乐幽灵牌 ==")
m3 = code(os.path.join("Cards", "Match3.cs"))
chk(m3.count("null, null)).FirstOrDefault()") == 1 or "null, null)).ToList()" in m3,
    "第一段选牌 source 传 null")
chk("(CardModel c) => c.Type == cardType, null)).ToList()" in m3, "第二段选牌 source 传 null")
chk("skipVisuals: true" not in m3, "恢复正常消耗动画（不再跳过）")
chk("选牌的收尾（OnSelectModeSourceFinished）当场完成" in m3, "注释写清了成因")

print("== 2. 系统：阿比舒（爪击/撕咬写法）==")
a2 = code(os.path.join("Cards", "AssistCards2.cs"))
seg = a2[a2.find("class SystemAbishu"):]
seg = seg[: seg.find("\n}")]
chk("new DamageVar(1m, ValueProp.Move)" in seg, "用 DamageVar 做主变量（基础 1）")
chk('new DynamicVar("Growth", 1m)' in seg, "Growth 变量")
chk("BuffFromAbishuPlay" in seg, "同类型卡逐张加伤")
chk("PlayerCombatState.AllCards.OfType<SystemAbishu>()" in seg, "遍历本场所有阿比舒")
chk("AfterDowngraded" in seg, "降级补回加成")
chk(not [x for x in seg.split(chr(10)) if "CombatStats" in x and not x.strip().startswith("//")],
    "不再用 CombatStats 现算加成（只在注释里提到旧写法）")
cs = code("CombatStats.cs")
chk("AbishuDamageBonus" not in cs and "AddAbishuBonus" not in cs, "CombatStats 死代码已删")
z = Z["STS2_MOMOI_CARD_SYSTEM_ABISHU.description"]
chk("{Damage:diff()}" in z, "文本用 {Damage:diff()}", z)
chk("{CalculatedDamage" not in z, "不再用 CalculatedDamage")
chk("+{Growth:diff()}" in z and "[blue]{Growth}" not in z, "伤害+2 的 2 不是蓝色", z)

print("== 3. 局势升温 ==")
chk(Z["STS2_MOMOI_CARD_PLAY_WITH_FIRE.title"] == "局势升温", "标题已是局势升温")
bf = code(os.path.join("Cards", "BurnFlowCards.cs"))
chk("局势升温（原「玩火」）" in bf, "注释同步改名")

print("== 4. 心流：减费可叠加 ==")
rw = code(os.path.join("Cards", "ReworkBatch.cs"))
chk("EnergyCost.AddUntilPlayed(-reduce);" in rw, "回到 AddUntilPlayed（可叠加）")
chk("ApplyCostReduce" not in rw, "覆盖式辅助方法已删")
chk("不要改成 SetUntilPlayed" in rw, "注释标明是设计意图")

print("== 5. 机会难得，选红色！补文本 ==")
z = Z["STS2_MOMOI_CARD_PICK_RED.description"]
chk("这张牌在本回合可以免费打出。" in z, "补上免费打出说明", z)
chk("SetUntilPlayed(0)" in code(os.path.join("Cards", "PickRed.cs")), "代码未改")

print("== 6. 蒙太奇：AutoPlay 被阻止则不发奖励 ==")
chk("class AutoPlayProbe" in rw, "新增 AutoPlayProbe")
chk("AutoPlayProbe.WillActuallyPlay(combatState, picked)" in rw, "蒙太奇先探测再发奖励")
chk("if (!willPlay)" in rw and "continue;" in rw, "被阻止则跳过奖励")
chk("CardKeyword.Unplayable" in rw and "AutoPlayType.Default" in rw, "判定含 Unplayable 与 ShouldPlay")

print("== 7. 幸运儿的祝福不加门控 ==")
seg = a2[a2.find("class AsunaGuardPower"):]
seg = seg[: seg.find("\n}")]
chk("IsPoweredAttack" not in seg, "减伤对所有伤害生效（含 DoT），不按 props 门控")

print("== 8. 王道不改 ==")
nb = code(os.path.join("Cards", "NewCardsBatch.cs"))
chk("rebate.Pending = DynamicVars[\"CostReduce\"].IntValue;" in nb, "王道手牌满进弃牌堆 + 减费照挂（保持原样）")

print("== 9. 标签闭合 ==")
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
