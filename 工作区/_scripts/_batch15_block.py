# -*- coding: utf-8 -*-
"""批次15：把「卡面 Block 用 DynamicVar、实际 GainBlock 用 BlockVar(Move)」的错配一次性改掉。

症状：卡面显示的格挡数不随敏捷/脆弱变化，与实际获得的格挡数不符。
原因：`new DynamicVar("Block", N)` 是普通变量，`UpdateCardPreview` 是空的，
      不会跑 `Hook.ModifyBlock`；而 `GainBlock` 那边用的是 `ValueProp.Move` 的 BlockVar，会跑。
修法：两边统一用 `new BlockVar(N, ValueProp.Move)` + `GainBlock(..., DynamicVars.Block, cardPlay)`
      （原版 Armaments / Backflip 的写法）。

用法：python _batch15_block.py [--dry]
"""
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode", "Cards")
BACKUP = os.path.join(ROOT, "工作区", "_backup", "batch15_pre")

# 类名 -> （文件, 期望的 Block 基础值）
TARGETS = {
    "MomoiSupportKotori": ("AssistCards.cs", 12),
    "RollAndShoot": ("CommonAttackCards.cs", 7),
    "AllsWellThatEndsWell": ("CommonAttackCards.cs", 16),
    "MailCare": ("CommonAttackCards.cs", 12),
    "GearUp": ("FirepowerFlowCards.cs", 8),
    "Countermeasure": ("IntentCards.cs", 6),
    "PostQuest": ("MinigameFlowCards.cs", 7),
    "TravelFrog": ("RemainingCards3.cs", 6),
    "Encounter": ("RemainingSpecialCards.cs", 8),
    "FlowState": ("ReworkBatch.cs", 16),
}


def class_span(src, cls):
    m = re.search(r"\bclass\s+" + cls + r"\b", src)
    if not m:
        return None
    i = src.find("{", m.end())
    if i < 0:
        return None
    depth = 0
    for j in range(i, len(src)):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                return m.start(), j + 1
    return None


# GainBlock(..., new BlockVar(DynamicVars["Block"].BaseValue, ValueProp.Move), cardPlay) —— 允许换行/空白差异
GAIN_RE = re.compile(
    r"GainBlock\(\s*(\w+)\s*,\s*new BlockVar\(\s*DynamicVars\[\"Block\"\]\.BaseValue\s*,\s*ValueProp\.Move\s*\)\s*,\s*cardPlay\s*\)",
    re.S)


def main():
    # 先按文件分组，避免「一个文件多个类」时后面的改动把前面的覆盖掉
    per_file = {}
    for cls, (fname, base) in TARGETS.items():
        per_file.setdefault(fname, []).append((cls, base))

    written = 0
    for fname, items in per_file.items():
        p = os.path.join(CODE, fname)
        src = open(p, encoding="utf-8").read()
        original = src

        for cls, base in items:
            span = class_span(src, cls)
            if span is None:
                print("  !! 找不到类", cls, fname)
                continue
            a, b = span
            body = src[a:b]

            old_decl = 'new DynamicVar("Block", %d)' % base
            new_decl = 'new BlockVar(%dm, ValueProp.Move)' % base
            if old_decl not in body:
                print("  !! %s 里没找到 %s" % (cls, old_decl))
                continue

            new_body = body.replace(old_decl, new_decl)
            new_body, n = GAIN_RE.subn(lambda m: "GainBlock(%s, DynamicVars.Block, cardPlay)" % m.group(1), new_body)

            # 类体长度可能变化，要按新长度重算后面类的偏移
            src = src[:a] + new_body + src[b:]
            print("  ok %-24s %-26s %s -> BlockVar(%d, Move)，改写 %d 处 GainBlock"
                  % (cls, fname, old_decl, base, n))

        if src != original:
            if DRY:
                pass
            else:
                os.makedirs(BACKUP, exist_ok=True)
                shutil.copy2(p, os.path.join(BACKUP, fname))
                open(p, "w", encoding="utf-8").write(src)
            written += 1

    if DRY:
        print("\n--dry 结束，未写盘。会改 %d 个文件。" % written)
    else:
        print("\n已改写 %d 个文件，备份 -> %s" % (written, os.path.relpath(BACKUP, ROOT)))


if __name__ == "__main__":
    main()
