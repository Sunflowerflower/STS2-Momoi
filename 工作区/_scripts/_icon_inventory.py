# -*- coding: utf-8 -*-
"""统计 Mod 里所有 Power（buff/debuff）及其图标现状 —— 产出待做图标清单"""
import json, os, re, sys, hashlib

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
IMGDIR = os.path.join(MOD, "images", "powers")
zp = json.load(open(os.path.join(MOD, "localization", "zhs", "powers.json"), encoding="utf-8"))
ep = json.load(open(os.path.join(MOD, "localization", "eng", "powers.json"), encoding="utf-8"))

# 1) 扫描 power 类
files = []
for dp, _, fs in os.walk(CODE):
    for f in fs:
        if f.endswith(".cs"):
            files.append(os.path.join(dp, f))

entries = {}
for p in files:
    t = open(p, encoding="utf-8").read()
    for m in re.finditer(r"\[RegisterPower\][\s\S]{0,1200}?class\s+(\w+)\s*:\s*(\w+)", t):
        cls = m.group(1)
        seg = t[m.start():m.start() + 4000]
        icon = re.search(r'IconPath:\s*\$?"[^"]*powers/([^"]+)"', seg)
        big = re.search(r'BigIconPath:\s*\$?"[^"]*powers/([^"]+)"', seg)
        ptype = re.search(r'PowerType\s+Type\s*=>\s*PowerType\.(\w+)', seg)
        stack = re.search(r'PowerStackType\s+StackType\s*=>\s*PowerStackType\.(\w+)', seg)
        inst = re.search(r'PowerInstanceType\s+InstanceType\s*=>\s*PowerInstanceType\.(\w+)', seg)
        entries[cls] = dict(
            file=os.path.relpath(p, CODE),
            icon=icon.group(1) if icon else None,
            big=big.group(1) if big else None,
            type=ptype.group(1) if ptype else "?",
            stack=stack.group(1) if stack else "?",
            inst=inst.group(1) if inst else "Default",
        )

# 2) 本地化标题（类名 → SNAKE_CASE 键）
def key_of(cls):
    return "STS2_MOMOI_POWER_" + re.sub(r"(?<!^)(?=[A-Z])", "_", cls).upper()

# 3) 占位判定：按文件 md5 聚簇 + 尺寸
def info(name):
    p = os.path.join(IMGDIR, name) if name else None
    if not p or not os.path.exists(p):
        return None
    b = open(p, "rb").read()
    return dict(size=len(b), md5=hashlib.md5(b).hexdigest())

groups = {}
for cls, d in entries.items():
    for k in ("icon", "big"):
        i = info(d.get(k))
        if i:
            groups.setdefault(i["md5"], []).append((cls + "/" + k, i["size"]))

rows = []
used = set()
for cls, d in sorted(entries.items()):
    k = key_of(cls)
    title_z = zp.get(k + ".title")
    title_e = ep.get(k + ".title")
    ic = info(d.get("icon"))
    big = info(d.get("big"))
    # 图标缺失 / 复用（同一 md5 被多张图共用 = 占位）
    dup = groups.get(ic["md5"], []) if ic else []
    dupn = len(dup)
    unused = not title_z and not title_e
    rows.append(dict(cls=cls, key=k, title=title_z or title_e or "（无本地化）",
                     type=d["type"], stack=d["stack"], inst=d["inst"],
                     icon=d.get("icon"), size=(ic or {}).get("size", 0),
                     dup=dupn, file=d["file"], unused=unused))
    used.add(d.get("icon"))

print("Power 类总数: %d" % len(rows))
print()
print("%-34s %-12s %-9s %-10s %-8s %s" % ("类", "中文名", "类型", "叠加", "图标B", "图标文件"))
print("-" * 118)
for r in rows:
    print("%-34s %-12s %-9s %-10s %-8d %s" % (r["cls"], r["title"], r["type"], r["stack"],
                                               r["size"], r["icon"]))
print()
# 图标文件里没被任何 power 引用的
allpng = sorted(f for f in os.listdir(IMGDIR) if f.endswith(".png"))
unref = [f for f in allpng if f not in used]
print("icons/powers 下 PNG: %d，未被 RegisterPower 引用: %d" % (len(allpng), len(unref)))
print("未引用:", ", ".join(unref))
print()
print("按 md5 复用（占位嫌疑）的 icon 文件：")
for md5, lst in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    if len(lst) > 1:
        print("  %d 张共用: %s" % (len(lst), ", ".join(x[0] for x in lst)))

out = os.path.join(ROOT, "工作区", "_data", "_power_icon_inventory.json")
json.dump(dict(powers=rows, unreferenced=unref,
               dup_groups={k: v for k, v in groups.items() if len(v) > 1}),
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n→", out)
