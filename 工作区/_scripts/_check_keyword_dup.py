# -*- coding: utf-8 -*-
"""体检：找出「描述里手写了会在前后自动追加的关键词」的卡（会造成重复显示）

自动规则（原版 CardModel.GetFormattedDescription）：
  beforeDescription = Ethereal / Sly / Retain / Innate / Unplayable  → 插在描述**最前**
  afterDescription  = Exhaust / Eternal                              → 接在描述**最后**
所以描述里不能再写 固有。/ 保留。/ 消耗。/ 虚幻。/ 永恒。/ 无法打出。
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
z = json.load(open(os.path.join(MOD, "localization", "zhs", "cards.json"), encoding="utf-8"))
e = json.load(open(os.path.join(MOD, "localization", "eng", "cards.json"), encoding="utf-8"))

code = ""
for dp, _, fs in os.walk(CODE):
    for f in fs:
        if f.endswith(".cs"):
            code += open(os.path.join(dp, f), encoding="utf-8").read()

BEFORE = [("Ethereal", "虚幻"), ("Sly", "狡诈"), ("Retain", "保留"), ("Innate", "固有"), ("Unplayable", "无法打出")]
AFTER = [("Exhaust", "消耗"), ("Eternal", "永恒")]


def kw_of(cls):
    m = re.search(r"class\s+%s\b[\s\S]{0,2500}?CanonicalKeywords\s*=>[^;]*;" % re.escape(cls), code)
    if not m:
        m = re.search(r"class\s+%s\b[\s\S]{0,2500}?LocalKeywords\.Add\(([^)]*)\)" % re.escape(cls), code)
    return m.group(0) if m else ""


norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
CLASSES = {norm(c): c for c in re.findall(r"class\s+([A-Za-z0-9_]+)\s*:\s*\w*ModCardTemplate", code)}

bad = []
for k, title in sorted(z.items()):
    if not k.endswith(".title") or not k.startswith("STS2_MOMOI_CARD_"):
        continue
    base = k[:-len(".title")]
    cls = CLASSES.get(norm(base[len("STS2_MOMOI_CARD_"):]))
    if not cls:
        continue
    sk = kw_of(cls)
    desc = z.get(base + ".description", "") or ""
    edesc = e.get(base + ".description", "") or ""
    issues = []
    for en, cn in BEFORE:
        if en in sk and re.match(r"^\s*(\[gold\])?" + cn, desc):
            issues.append("开头重复了「%s」" % cn)
        if en in sk and edesc.lower().startswith(en.lower()):
            issues.append("eng 开头重复了 %s" % en)
    for en, cn in AFTER:
        if en in sk and re.search(r"(\[gold\])?" + cn + r"(\[\/gold\])?。?\s*$", desc):
            issues.append("结尾重复了「%s」" % cn)
        if en in sk and re.search(en + r"\.?\s*$", edesc):
            issues.append("eng 结尾重复了 %s" % en)
    if issues:
        bad.append((title, cls, issues, desc[:70]))

if bad:
    print("!! 可能重复显示关键词的卡：%d" % len(bad))
    for t, c, i, d in bad:
        print("  %-16s %-28s %s\n      desc: %s" % (t, c, "；".join(i), d))
else:
    print("OK：没有卡在描述里重复手写自动追加的关键词")
