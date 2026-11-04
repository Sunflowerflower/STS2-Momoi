# -*- coding: utf-8 -*-
"""批次10 · 清理废弃的 power 相关文件（图标 / 本地化）

安全规则（防止误删在用的）：
  1. 图标：文件名（含 .png）在**整个 C# 源码**里搜不到 → 才删（power 的 IconPath 都是字面量字符串，
     所以这个判定是可靠的）；同时排除任何在用的名字。
  2. 本地化：`STS2_MOMOI_POWER_<列名>` 不能由任何一个 [RegisterPower] 类推导出来，
     且该 key 字符串在源码里搜不到 → 才删。
  3. 删除前一律先复制到 工作区/_backup/batch10_dead/。
用法：py -3 _cleanup_dead.py [--dry]
"""
import json, os, re, shutil, sys, datetime

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
BAK = os.path.join(ROOT, "工作区", "_backup", "batch10_dead")

# 白名单：这些虽然一时搜不到，但要留着（用户在用的 / 有美术的 / 备用）
KEEP_ICON = set()
KEEP_KEY = {"STS2_MOMOI_POWER_POST_QUEST_UPGRADED_MARK"}   # PostQuestPower 用 LocString 读它


def read_code():
    t = ""
    for dp, _, fs in os.walk(CODE):
        for f in fs:
            if f.endswith(".cs"):
                t += open(os.path.join(dp, f), encoding="utf-8").read()
    return t


def main():
    dry = "--dry" in sys.argv
    code = read_code()
    classes = sorted(set(re.findall(r"\[RegisterPower\][\s\S]{0,400}?class\s+(\w+)", code)))
    live_keys = set("STS2_MOMOI_POWER_" + re.sub(r"(?<!^)(?=[A-Z])", "_", c).upper() for c in classes)

    # ── 1. 死图标
    d = os.path.join(MOD, "images", "powers")
    dead_icons = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".png"):
            continue
        if f in KEEP_ICON:
            continue
        # 用「去掉 .png 后的完整词」匹配，避免 dev_green 命中 dev_green_power
        if not re.search(r"(?<![A-Za-z0-9_])" + re.escape(f[:-4]) + r"(?![A-Za-z0-9_])", code):
            dead_icons.append(f)

    # ── 2. 死本地化
    dead_keys = []
    for lang in ("zhs", "eng"):
        p = os.path.join(MOD, "localization", lang, "powers.json")
        dd = json.load(open(p, encoding="utf-8"))
        for k in dd:
            base = k.rsplit(".", 1)[0]
            if not base.startswith("STS2_MOMOI_POWER_"):
                continue
            if base in live_keys or base in KEEP_KEY:
                continue
            if base in code:            # 代码里以字符串形式引用（如 LocString("powers", "...")）
                continue
            if base not in dead_keys:
                dead_keys.append(base)

    print("=== 判定 ===")
    print("在用的 power 类 %d 个；在用图标（代码里有字面量引用）%d 张"
          % (len(classes), len([f for f in os.listdir(d) if f.endswith('.png')]) - len(dead_icons)))
    print()
    print("① 可删图标 %d 张：" % len(dead_icons))
    for f in dead_icons:
        print("     %-42s %d B" % (f, os.path.getsize(os.path.join(d, f))))
    print()
    print("② 可删本地化 key %d 个：" % len(dead_keys))
    zz = json.load(open(os.path.join(MOD, "localization", "zhs", "powers.json"), encoding="utf-8"))
    for k in dead_keys:
        print("     %-46s %s" % (k, zz.get(k + ".title")))
    print()

    if dry:
        print("[dry-run] 不删除")
        return
    os.makedirs(BAK, exist_ok=True)
    n = 0
    for f in dead_icons:
        for ext in (".png", ".import"):
            src = os.path.join(d, f[:-4] + ext)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(BAK, os.path.basename(src)))
                os.remove(src)
                n += 1
    for lang in ("zhs", "eng"):
        p = os.path.join(MOD, "localization", lang, "powers.json")
        dd = json.load(open(p, encoding="utf-8"))
        shutil.copy2(p, os.path.join(BAK, "powers_%s.json" % lang))
        for k in list(dd):
            if k.rsplit(".", 1)[0] in dead_keys:
                del dd[k]
                n += 1
        json.dump(dd, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("已删除 %d 个文件/键；备份在 %s" % (n, os.path.relpath(BAK, ROOT)))


if __name__ == "__main__":
    main()
