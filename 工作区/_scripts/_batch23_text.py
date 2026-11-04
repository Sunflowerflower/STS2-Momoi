# -*- coding: utf-8 -*-
"""批次23：击晕 → 金色关键词（3 张卡）；终于上一档了！的金币 → 金色（无侧栏）。"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

LOC = r"C:\Users\asus\RiderProjects\STS2 Momoi\STS2 Momoi\STS2_Momoi\localization"

# 只替换「还没被染色」的裸关键词，避免重复加标记
SUBS = {
    "zhs": [
        ("击晕所有敌人。", "[gold]击晕[/gold]所有敌人。"),
        ("击晕该敌人。", "[gold]击晕[/gold]该敌人。"),
        ("击晕该敌人并将", "[gold]击晕[/gold]该敌人并将"),
        ("{IfUpgraded:show:25|20}金币", "{IfUpgraded:show:25|20}[gold]金币[/gold]"),
        ("{IfUpgraded:show:15|10}金币", "{IfUpgraded:show:15|10}[gold]金币[/gold]"),
    ],
    "eng": [
        ("Stun all enemies.", "[gold]Stun[/gold] all enemies."),
        ("Stun it.", "[gold]Stun[/gold] it."),
        ("Stun it and increase", "[gold]Stun[/gold] it and increase"),
        ("{IfUpgraded:show:25|20} gold", "{IfUpgraded:show:25|20} [gold]Gold[/gold]"),
        ("{IfUpgraded:show:15|10} gold", "{IfUpgraded:show:15|10} [gold]Gold[/gold]"),
    ],
}

hits = {}
for lang in ("zhs", "eng"):
    p = os.path.join(LOC, lang, "cards.json")
    d = json.load(open(p, encoding="utf-8"), object_pairs_hook=dict)
    n = 0
    for key, v in d.items():
        if not isinstance(v, str):
            continue
        new = v
        for old, rep in SUBS[lang]:
            if old in new and rep not in new:
                new = new.replace(old, rep)
        if new != v:
            d[key] = new
            hits.setdefault(lang, []).append(key)
            n += 1
    open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    print("%s 改了 %d 条：" % (lang, n))
    for k in hits.get(lang, []):
        print("   ", k)

# 复核：不应该再有裸的 击晕 / Stun / 金币 / gold
print("\n== 复核 ==")
for lang, kw in (("zhs", "击晕"), ("eng", "Stun")):
    d = json.load(open(os.path.join(LOC, lang, "cards.json"), encoding="utf-8"))
    naked = [k for k, v in d.items() if isinstance(v, str) and kw in v and "[gold]%s[/gold]" % kw not in v]
    print("  %s 裸「%s」剩余：%s" % (lang, kw, naked or "无 ✓"))

for lang, kw in (("zhs", "金币"), ("eng", "Gold")):
    d = json.load(open(os.path.join(LOC, lang, "cards.json"), encoding="utf-8"))
    naked = [k for k, v in d.items() if isinstance(v, str) and kw in v and "[gold]%s[/gold]" % kw not in v]
    print("  %s 裸「%s」剩余：%s" % (lang, kw, naked or "无 ✓"))
