# -*- coding: utf-8 -*-
"""批次31 自检（**2026-10-24 重新生成**）：死亡动画 50 帧接入 + 能量图标尺寸 + 多人手臂尺寸。

⚠ 说明：这份脚本原先由 2026-10-22 的动画会话编写（死亡动画 50 帧接入那一批）。2026-10-24 的卡牌调整会话
新建自检脚本时误用了同名文件 `_verify_batch31.py`，把它覆盖了。这里按 §21.35 的实测数据与当前磁盘资产重建，
覆盖面一致：dead 50 帧 / 尺寸 / C# 接线 / 能量图标 24·256 / 多人手臂 422×1200 / 审阅图。
"""
import os
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
IMG = os.path.join(MOD, "images", "characters")
CUE = os.path.join(IMG, "cue")
WS = os.path.join(ROOT, "工作区", "编辑区", "人物")

ok = fail = 0


def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24]) + (head[24], head[25])


char = open(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs"), encoding="utf-8").read()

print("== 1. 死亡动画 50 帧 ==")
chk(os.path.exists(os.path.join(CUE, "dead.png")), "dead.png 存在")
missing = [i for i in range(1, 50) if not os.path.exists(os.path.join(CUE, f"dead_{i:02d}.png"))]
chk(not missing, "dead_01..dead_49 共 49 张都在", missing[:5])
chk(not os.path.exists(os.path.join(CUE, "dead_50.png")), "没有第 50 张（总数 50 = dead + 49）")
bad = []
for name in ["dead.png"] + [f"dead_{i:02d}.png" for i in range(1, 50)]:
    info = png_size(os.path.join(CUE, name))
    if info is None or info[:2] != (1400, 1250) or info[2] != 8 or info[3] != 6:
        bad.append((name, info))
chk(not bad, "50 张全是 1400×1250 / 8bit RGBA", bad[:3])

print("== 2. C# 接线 ==")
chk("DeadFrameCount = 50" in char, "DeadFrameCount = 50")
chk("DeadSpeed = 1f" in char, "DeadSpeed 可调")
chk('.Sequence("dead"' in char and '.Single("dead"' not in char, "dead 从 Single 改成 Sequence")
chk('seq.Frame(AnimFramePath("dead", i), 1f / CueFps / DeadSpeed);' in char, "每帧 1/24/DeadSpeed")
chk(".Loop()" not in char.split('.Sequence("dead"')[1][:300], "死亡序列不循环")
chk('d={DeadSpeed}' in char, "状态机日志带 DeadSpeed")

print("== 3. 能量图标尺寸 ==")
t = png_size(os.path.join(IMG, "energy_text.png"))
b = png_size(os.path.join(IMG, "energy_big.png"))
chk(t[:2] == (24, 24), "energy_text.png = 24×24（小/文本图标）", t)
chk(b[:2] == (256, 256), "energy_big.png = 256×256（大图标）", b)

print("== 4. 多人手势手臂 4 张（原版 422×1200）==")
for hand in ("point", "rock", "paper", "scissors"):
    p = os.path.join(IMG, f"STS2_Momoi_arm_{hand}.png")
    chk(os.path.exists(p), f"arm_{hand}.png 存在")
    if os.path.exists(p):
        chk(png_size(p)[:2] == (422, 1200), f"arm_{hand} = 422×1200", png_size(p))

print("== 5. 审阅图（工作区，不进 PCK）==")
for f in ("dead_cue_sheet.png", "dead_vs_idle.png", "arm_reference_sheet.png"):
    chk(os.path.exists(os.path.join(WS, "_work", f)), f"_work/{f} 存在")
chk(not os.path.exists(os.path.join(MOD, "死亡动画.aep")), "AEP 本体不在 mod 资源目录里")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
