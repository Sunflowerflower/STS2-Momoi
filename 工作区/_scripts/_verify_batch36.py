# -*- coding: utf-8 -*-
"""批次36 自检：桃味气泡水变牌（source:null + 逐张变换）与「任意张」选择界面。"""
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


pot = open(os.path.join(CODE, "Potions", "MomoiPotions.cs"), encoding="utf-8").read()
SEL_Z, SEL_E = load("zhs", "card_selection"), load("eng", "card_selection")

ps = body(pot, "PeachSoda")

print("== 1. 选牌界面：任意张（不再 99）==")
chk('"STS2_MOMOI_ANY_TRANSFORM"), 0, 999999999' in ps, "MaxSelect = 999999999（原版「任意张」写法）")
chk(", 0, 99)" not in ps, "不再用 99")
chk('"TO_TRANSFORM"' not in ps, "不再复用带 {Amount} 的原版文案")
chk(SEL_Z.get("STS2_MOMOI_ANY_TRANSFORM") == "选择任意张牌来[gold]变化[/gold]。",
    "zhs = 选择任意张牌来变化。", SEL_Z.get("STS2_MOMOI_ANY_TRANSFORM"))
chk("any number" in (SEL_E.get("STS2_MOMOI_ANY_TRANSFORM") or ""), "eng 同步", SEL_E.get("STS2_MOMOI_ANY_TRANSFORM"))

print("== 2. 变牌写法（整活 / 原版护驾 同路径）==")
chk("await CardCmd.Transform(card, replacement);" in ps, "逐张 CardCmd.Transform(单张)")
chk("CardCmd.Transform(transformations" not in ps, "不再用批量变换")
chk("new CardTransformation(" not in ps, "不再自己构造 CardTransformation")
chk("foreach (var card in picked)" in ps, "按选中的牌逐张处理")

print("== 3. 关键修复：source 传 null（否则药水永远不触发 ExecutionFinished）==")
chk("}, null, null))" in ps, "FromHand 的 filter=null / source=null")
chk("}, null, this))" not in ps, "不再把药水模型当 source 传进去")
hand = open(os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode", "Cards", "Match3.cs"), encoding="utf-8").read()
chk("source: null" in ps or "}, null, null))" in ps, "与消消乐同一套写法")

print("== 4. 药水其它部分没动 ==")
chk("PotionRarity.Rare" in ps, "稀有度仍是稀有")
chk("PotionUsage.CombatOnly" in ps, "仍是战斗中可用")
chk("PotionAssetProfile" in ps and "images/potions/" in ps, "贴图 profile 仍在")
chk("MomoiSidebarTips.MinigameKeyword" in ps and "MomoiSidebarTips.Transform" in ps, "两条侧栏仍在")
chk('MinigameSupport.CreateRandomMinigameCard(combatState, Owner, false)' in ps, "仍生成未升级的随机小游戏牌")
chk("CombatStats.RecordMinigameObtained(replacement)" in ps, "仍记录获得的小游戏牌")

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
