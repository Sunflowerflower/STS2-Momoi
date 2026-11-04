# -*- coding: utf-8 -*-
"""导出 卡名 → 本地化key → 代码文件 的对照表"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
ZHS = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "localization", "zhs")
cards = json.load(open(os.path.join(ZHS, "cards.json"), encoding="utf-8"))

# 收集代码里所有 class 定义
classes = {}
for dp, _, fs in os.walk(CODE):
    for f in fs:
        if not f.endswith(".cs"):
            continue
        p = os.path.join(dp, f)
        t = open(p, encoding="utf-8").read()
        for m in re.finditer(r'\bclass\s+(\w+)', t):
            classes[m.group(1)] = os.path.relpath(p, CODE)

rows = []
for k, v in sorted(cards.items()):
    if not k.endswith(".title"):
        continue
    base = k[:-len(".title")]
    if not base.startswith("STS2_MOMOI_CARD_"):
        continue
    cls = base[len("STS2_MOMOI_CARD_"):]
    rows.append((v, cls, classes.get(cls, "?"), base))

rows.sort()
out = []
for name, cls, f, base in rows:
    out.append("%-22s %-32s %s" % (name, cls, f))
open(os.path.join(ROOT, "工作区", "_data", "_card_index.txt"), "w", encoding="utf-8").write("\n".join(out))
print("卡片总数:", len(rows))
print("\n".join(out))
