# -*- coding: utf-8 -*-
"""导出指定卡牌的中英文本地化（title/description/upgrade_description/sidebar...）"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
z = json.load(open(os.path.join(MOD, "localization/zhs/cards.json"), encoding="utf-8"))
e = json.load(open(os.path.join(MOD, "localization/eng/cards.json"), encoding="utf-8"))
zp = json.load(open(os.path.join(MOD, "localization/zhs/powers.json"), encoding="utf-8"))
ep = json.load(open(os.path.join(MOD, "localization/eng/powers.json"), encoding="utf-8"))

NAMES = ["吃豆人！", "渔获", "秒人斧", "来自大师们的援助", "来自骇客们的协助", "来自C&C的援护",
         "相遇", "俄罗斯方块！", "构想", "连连看！", "消消乐！", "植物大战僵尸", "大姐头",
         "节奏游戏！", "矛与盾", "构想之盾", "开发者协同：绿", "角色扮演！", "得道多助",
         "跑酷！", "火焰附加", "见识下我的实力吧", "绝地求生", "扫雷", "重振旗鼓", "双线叙事"]

if len(sys.argv) > 1:
    NAMES = sys.argv[1:]

for nm in NAMES:
    bases = [k[:-6] for k, v in z.items() if k.endswith(".title") and v == nm]
    if not bases:
        print("!! 未找到", nm); continue
    for b in bases:
        print("=" * 78)
        print("### %s   [%s]" % (nm, b))
        keys = [k[len(b) + 1:] for k in z if k.startswith(b + ".") and k != b + ".title"]
        for kk in sorted(keys):
            zv = z.get(b + "." + kk)
            ev = e.get(b + "." + kk)
            print("  --%s" % kk)
            print("     zhs:", repr(zv))
            if ev is not None and ev != zv:
                print("     eng:", repr(ev))
        # 相关 power
        for pk, pv in list(zp.items()) + list(ep.items()):
            if any(w in pv for w in (nm,)):
                print("  POWER", pk, "=", repr(pv))
