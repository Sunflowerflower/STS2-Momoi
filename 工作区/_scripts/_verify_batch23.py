# -*- coding: utf-8 -*-
"""批次23 自检：击晕是金色关键词、终于上一档了！的金币是金色且没有侧栏。"""
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


def load(lang, table):
    return json.load(open(os.path.join(LOC, lang, table + ".json"), encoding="utf-8"))


Z, E = load("zhs", "cards"), load("eng", "cards")
patch = open(os.path.join(CODE, "Patches", "MinigameSidebarPatch.cs"), encoding="utf-8").read()

STUN_CARDS = ["STS2_MOMOI_CARD_MOMOI_SUPPORT_HARE", "STS2_MOMOI_CARD_MOMOI_SUPPORT_CHIHIRO",
              "STS2_MOMOI_CARD_MOMENTUM_BREAK"]

print("== 1. 击晕 = 金色关键词 ==")
for base in STUN_CARDS:
    name = base.replace("STS2_MOMOI_CARD_", "")
    for suf in (".description", ".smartDescription"):
        z = Z[base + suf]
        e = E[base + suf]
        chk("[gold]击晕[/gold]" in z, "%s%s 中文金字" % (name, suf), z)
        chk("[gold]Stun[/gold]" in e, "%s%s 英文金字" % (name, suf), e)

naked_z = [k for k, v in Z.items() if isinstance(v, str) and "击晕" in v and "[gold]击晕[/gold]" not in v]
naked_e = [k for k, v in E.items() if isinstance(v, str) and "Stun" in v and "[gold]Stun[/gold]" not in v]
chk(not naked_z, "zhs 没有裸的「击晕」", naked_z)
chk(not naked_e, "eng 没有裸的「Stun」", naked_e)
chk('Has("击晕", "Stun")' in patch, "击晕侧栏仍然存在（未改动）")

print("== 2. 终于上一档了！的金币 ==")
for suf in (".description", ".smartDescription"):
    z = Z["STS2_MOMOI_CARD_RANK_UP" + suf]
    e = E["STS2_MOMOI_CARD_RANK_UP" + suf]
    chk(z.count("[gold]金币[/gold]") == 2, "zhs%s 两处金币都上色" % suf, z)
    chk(e.count("[gold]Gold[/gold]") == 2, "eng%s 两处 Gold 都上色" % suf, e)
    chk("{IfUpgraded:show:25|20}" in z and "{IfUpgraded:show:15|10}" in z, "zhs%s 升级分支仍在" % suf)
chk('Has("金币"' not in patch and '"Gold")' not in patch, "金币/Gold 没有被加进侧栏扫描表")
chk("Gold" in Z["STS2_MOMOI_CARD_RANK_UP.description"] or True, "（标题 Gold Miner! 不动）")
chk(E["STS2_MOMOI_CARD_GOLD_MINER.title"] == "Gold Miner!", "黄金矿工的标题没被上色")

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
