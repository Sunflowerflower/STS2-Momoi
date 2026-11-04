# -*- coding: utf-8 -*-
"""批次10b：
1) 删除废弃的 MomentumBreakPower（破势的 power 类）——效果早已内联进卡牌自身，无任何代码引用。
2) 删除 momentum_break_power.png / .import 与 powers.json 里该 power 的 3 个词条。
3) 把「美味饼干_王小桃.png」接入 VanillaRelicVisualOverrides。
用法：python _batch10b.py [--dry]
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
BACKUP = os.path.join(ROOT, "工作区", "_backup", "batch10b_dead")

CS_FILE = os.path.join(CODE, "Cards", "RemainingCards2.cs")

# ---------- 1. 删除 C# 里的 power 类 ----------
with open(CS_FILE, encoding="utf-8") as f:
    lines = f.readlines()

start = next(i for i, l in enumerate(lines) if "破势的最终伤害倍数" in l)  # 0-based
# 往前吃掉可能存在的空行（保留一个），往后找到类结束的 '}'
end = start
depth = 0
seen_brace = False
for i in range(start, len(lines)):
    depth += lines[i].count("{") - lines[i].count("}")
    if "{" in lines[i]:
        seen_brace = True
    if seen_brace and depth == 0:
        end = i
        break
# 连同类后面的空行一起删掉
while end + 1 < len(lines) and lines[end + 1].strip() == "":
    end += 1

removed = lines[start:end + 1]
print("[C#] RemainingCards2.cs 将删除第 %d~%d 行（共 %d 行）" % (start + 1, end + 1, len(removed)))
print("     首行: %s" % removed[0].strip())
print("     末行: %s" % removed[-1].strip())
assert any("class MomentumBreakPower" in l for l in removed), "没找到类定义"
assert lines[end + 1].lstrip().startswith("/// <summary>"), "删到了后面的内容: " + lines[end + 1][:60]

# ---------- 2. 删除图标 + 本地化 ----------
ICON = os.path.join(MOD, "images", "powers", "momentum_break_power.png")
dead_files = [ICON, ICON + ".import"]

dead_keys = ["STS2_MOMOI_POWER_MOMENTUM_BREAK_POWER.title",
             "STS2_MOMOI_POWER_MOMENTUM_BREAK_POWER.description",
             "STS2_MOMOI_POWER_MOMENTUM_BREAK_POWER.smartDescription"]

loc_files = [os.path.join(MOD, "localization", lang, "powers.json") for lang in ("zhs", "eng")]

if DRY:
    print("[图标] 将删除: %s" % [os.path.basename(f) for f in dead_files if os.path.exists(f)])
    for p in loc_files:
        d = json.load(open(p, encoding="utf-8"))
        print("[本地化] %s 将删除: %s" % (os.path.relpath(p, ROOT),
                                          [k for k in dead_keys if k in d]))
    print("\n--dry 结束，未改动任何文件。")
    sys.exit(0)

os.makedirs(BACKUP, exist_ok=True)
with open(CS_FILE, "w", encoding="utf-8") as f:
    f.writelines(lines[:start] + lines[end + 1:])
print("[C#] 已删除 MomentumBreakPower 类。")

for p in dead_files:
    if os.path.exists(p):
        shutil.copy2(p, os.path.join(BACKUP, os.path.basename(p)))
        os.remove(p)
        print("[图标] 已删除并备份: %s" % os.path.basename(p))

removed_keys = 0
for p in loc_files:
    d = json.load(open(p, encoding="utf-8"), object_pairs_hook=dict)
    for k in dead_keys:
        if d.pop(k, None) is not None:
            removed_keys += 1
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    shutil.copy2(p, os.path.join(BACKUP, "powers_%s.json" % os.path.basename(os.path.dirname(p))))
print("[本地化] 已删除 %d 个词条。" % removed_keys)

print("\n完成。备份在 %s" % os.path.relpath(BACKUP, ROOT))
