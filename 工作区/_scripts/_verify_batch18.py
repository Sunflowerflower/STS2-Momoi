# -*- coding: utf-8 -*-
"""批次18 自检：消消乐重做 + 妮露援护确认。"""
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
m3 = code(os.path.join("Cards", "Match3.cs"))
a2 = code(os.path.join("Cards", "AssistCards2.cs"))

print("== 1. 目标存活改动的归属确认 ==")
i = a2.find("IsAlive: true } ? target : null")
cls = re.findall(r"\bclass\s+([A-Za-z_]\w*)", a2[:i])[-1]
chk(cls == "MomoiSupportNeru", "改的是「来自妮露的援护」而不是双刀王小桃", cls)
seg = a2[a2.find("class MomoiSupportNeru"):]
seg = seg[: seg.find("\n}")]
chk("PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature, -stacks" in seg, "确实是消耗火力额外打出")
chk("target is { IsAlive: true } ? target : null" in seg, "目标死了就交给 AutoPlay 重挑存活目标")

print("== 2. 消消乐：第二次选牌提示 ==")
chk('new LocString("cards", "STS2_MOMOI_CARD_MATCH3.pickAny")' in m3, "第二段用自定义提示语")
chk(Z["STS2_MOMOI_CARD_MATCH3.pickAny"] == "选择任意张牌", "zhs 提示语 = 选择任意张牌")
chk(E["STS2_MOMOI_CARD_MATCH3.pickAny"] == "Choose Any Number of Cards", "eng 提示语")
chk('new LocString("gameplay_ui", "CHOOSE_CARD_HEADER")' in m3, "第一段仍是「选择一张牌」")

print("== 3. 消消乐：删掉两个侧栏 ==")
chk("AdditionalHoverTips" not in m3, "代码里没有侧栏")
chk("STS2_MOMOI_CARD_MATCH3.sidebar1" not in Z and "STS2_MOMOI_CARD_MATCH3.sidebar2" not in Z, "zhs 侧栏已删")
chk("STS2_MOMOI_CARD_MATCH3.sidebar1" not in E and "STS2_MOMOI_CARD_MATCH3.sidebar2" not in E, "eng 侧栏已删")

print("== 4. 消消乐：打出并消耗 ==")
chk("AutoPlayProbe.WillActuallyPlay(combatState, card)" in m3, "先探测能否打出")
chk("await CardCmd.AutoPlay(choiceContext, card, null);" in m3, "能打出的先打出")
chk("if (card.Pile?.Type is PileType.Hand or PileType.Draw or PileType.Discard or PileType.Play)" in m3,
    "只对还在战斗牌堆里的牌补消耗")
chk("card.Pile?.Type" in m3, "消耗前检查牌堆（避免重复消耗报错）")
chk("if (count >= 3)" in m3 and "var extra = count - 3;" in m3, "三消阈值与额外奖励")

print("== 5. 消消乐：升级改为费用 -1（2026-10-25 取消保留）==")
chk("EnergyCost.UpgradeBy(-1);" in m3, "OnUpgrade 费用 1 -> 0")
chk("AddKeyword(CardKeyword.Retain);" not in m3, "升级不再加保留")
chk("public Match3() : base(1, CardType.Skill" in m3, "基础 1 费")

print("== 6. 消消乐：文本 ==")
z = Z["STS2_MOMOI_CARD_MATCH3.description"]
plain = re.sub(r"\[/?[a-z]+\]", "", z)
chk(plain.startswith("选择任意张类型相同的牌消耗。"), "开头一句与要求一致", plain)
chk("若消耗的牌不低于3张则改为打出并消耗" in plain, "三消改为打出并消耗")
chk("超过3张则每超出一张就抽1张牌并获得" in plain, "超过 3 张的奖励")
chk("[gold]消耗[/gold]" in z, "消耗是金色的")
chk("小游戏牌。" not in z and "消耗。" not in z, "不手写会自动追加的「小游戏牌。」「消耗。」")
chk("{Energy:energyIcons()}" in z, "能量用能量图标")

print("== 7. 标签闭合 ==")
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
