# -*- coding: utf-8 -*-
"""批次19 自检：颜色标记的「按表」规范。

原版惯例（逐表核对过 Slay the Spire 2/localization/zhs）：
  cards   —— 数字**不上色**（去标记后 605 张里仅 1 张带 [blue]，且是整句高亮）；
             卡牌描述基本只用 [gold] 标关键词；变量数字用 {X:diff()} 由格式化器自动染色。
  powers  —— 数字用 [blue]（原版 174 处）。
  relics / potions —— 数字用 [blue]，回血用 [green]。
"""
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
VAN = r"C:\Users\asus\Desktop\Slay the Spire 2\localization\zhs"

ok = fail = 0
def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))

def load(lang, table, base=MOD):
    p = os.path.join(base, "localization", lang, table + ".json") if base == MOD else os.path.join(base, table + ".json")
    return json.load(open(p, encoding="utf-8"))

def tags(d):
    c = Counter()
    for k, v in d.items():
        if isinstance(v, str) and k.endswith(".description"):
            for m in re.finditer(r"\[([a-z]+)\]", v):
                c[m.group(1)] += 1
    return c

print("== 1. 原版基准 ==")
v_cards = tags(load("zhs", "cards", VAN))
print("   原版 cards 标记:", dict(v_cards))
chk(v_cards.get("blue", 0) <= 1, "原版卡面几乎不用 [blue]")

print("== 2. 模组卡面不再有 [blue] ==")
for lang in ("zhs", "eng"):
    d = load(lang, "cards")
    hits = [k for k, v in d.items() if isinstance(v, str) and "[blue]" in v]
    chk(not hits, "[%s] cards.json 无 [blue]" % lang, hits[:6])

print("== 3. power 仍然按原版用 [blue] ==")
for lang in ("zhs", "eng"):
    c = tags(load(lang, "powers"))
    chk(c.get("blue", 0) > 0, "[%s] powers 仍有 [blue]（%d 处）" % (lang, c.get("blue", 0)))

print("== 4. 遗物 / 药水允许 [blue]（原版就是这么写的）==")
v_rel = tags(load("zhs", "relics", VAN))
chk(v_rel.get("blue", 0) > 0, "原版 relics 用 [blue]")
for lang in ("zhs", "eng"):
    c = tags(load(lang, "relics"))
    chk(c.get("blue", 0) > 0, "[%s] relics 保留 [blue]" % lang)

print("== 5. 卡面数字确实不上色（抽查 5 张）==")
d = load("zhs", "cards")
for key in ("STS2_MOMOI_CARD_MATCH3", "STS2_MOMOI_CARD_MINIGUN",
            "STS2_MOMOI_CARD_PAC_MAN", "STS2_MOMOI_CARD_PICK_RED", "STS2_MOMOI_CARD_SYSTEM_ABISHU"):
    pass
for key in ("STS2_MOMOI_CARD_MATCH3.description", "STS2_MOMOI_CARD_MINIGUN.description",
            "STS2_MOMOI_CARD_PAC_MAN.description", "STS2_MOMOI_CARD_PICK_RED.description",
            "STS2_MOMOI_CARD_SYSTEM_ABISHU.description"):
    v = d.get(key)
    if v is None:
        continue
    chk("[blue]" not in v, "%s 无 [blue]" % key.split(".")[0].replace("STS2_MOMOI_CARD_", ""))

print("== 6. 标签闭合（全表）==")
bad = []
for lang in ("zhs", "eng"):
    for f in os.listdir(os.path.join(MOD, "localization", lang)):
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

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
