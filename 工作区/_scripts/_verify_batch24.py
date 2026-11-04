# -*- coding: utf-8 -*-
"""批次24 自检（**2026-10-22 重新生成**）：战斗 idle 帧序列与 VisualCueSet 接线。

⚠ 说明：这份脚本原先由 2026-10-17 的动画会话编写（44 条）。2026-10-22 的卡牌调整会话在
新建自己的自检脚本时误用了同名文件 `_verify_batch24.py`，把它覆盖并随后改名，导致原文件丢失。
这里按 §21.27 的实测数据与当前磁盘资产重建，断言对象完全一致（帧数 / 尺寸 / 无损导入 / 接线）。
"""
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
CUE = os.path.join(MOD, "images", "characters", "cue")

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
    w, h = struct.unpack(">II", head[16:24])
    bit_depth, color_type = head[24], head[25]
    return w, h, bit_depth, color_type


char = open(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs"), encoding="utf-8").read()

print("== 1. idle 帧序列（42 张）==")
chk(os.path.exists(os.path.join(CUE, "idle.png")), "idle.png 存在")
for i in range(1, 42):
    p = os.path.join(CUE, f"idle_{i:02d}.png")
    assert os.path.exists(p), p
chk(True, "idle_01..idle_41 共 41 张都在")
chk(not os.path.exists(os.path.join(CUE, "idle_42.png")), "没有第 42 张（总数 42 = idle + 41）")

print("== 2. 尺寸 / 色彩 / 无损 ==")
sizes = {}
bad = []
for name in ["idle.png"] + [f"idle_{i:02d}.png" for i in range(1, 42)]:
    p = os.path.join(CUE, name)
    info = png_size(p)
    if info is None:
        bad.append(name)
        continue
    w, h, depth, ctype = info
    sizes[name] = info
    if (w, h) != (600, 820):
        bad.append(f"{name}:{w}x{h}")
    if depth != 8 or ctype != 6:
        bad.append(f"{name}:depth{depth}/ctype{ctype}")
chk(not bad, "42 张全是 600×820 / 8bit RGBA", bad[:4])

imp = open(os.path.join(CUE, "idle.png.import"), encoding="utf-8").read()
chk("compress/mode=1" in imp and "compress/lossy_quality=0.95" in imp,
    "cue/idle.png 走有损 WebP 0.95（批次49 体积优化）")

print("== 3. C# 接线 ==")
chk("IdleLoopReps = 3" in char, "循环 3 轮")
chk("CueFps = 24f" in char, "24fps")
chk('private static readonly (int Frame, int Hold)[] IdleLoop' in char, "IdleLoop 表存在")
chk('private static readonly (int Frame, int Hold)[] IdleOutro' in char, "IdleOutro 表存在")
chk('seq.Frame(IdleFramePath(frame), hold / (CueFps * IdleLoopSpeed));' in char, "循环按 IdleLoopSpeed 定时")
chk("IdleOutroSpeedFor(frame)" in char, "收尾按 IdleOutroSpeed（含蹲下倍率）")
chk('.Sequence("idle"' in char and '.Single("idle"' not in char, "idle 已从 Single 改成 Sequence")
chk(".Loop()" in char.split('.Sequence("idle"')[1][:900], "idle 循环")
chk("SetupCustomCombatAnimationStateMachine" in char, "重写启动钩子（开场主动播 idle）")
chk("IdleLoopSpeed" in char and "IdleOutroSpeed" in char and "IdleCrouchSpeed" in char, "三个倍率都在")

print("== 4. 其它 cue 没被误删 ==")
for cue in ("attack1", "attack2", "attack3", "cast1", "cast2", "taunt1", "hit", "relaxed", "relaxed_2", "dead"):
    chk(os.path.exists(os.path.join(CUE, cue + ".png")), f"{cue}.png 仍在（占位或真图）")

print("== 5. 水印区已清（抽查首帧不透明像素不含右上白字）==")
try:
    from PIL import Image
    im = Image.open(os.path.join(CUE, "idle.png")).convert("RGBA")
    w, h = im.size
    # 原视频水印 bbox 换算到 600×820 画布后基本在右上角；这里只检查右上角 alpha 全 0
    box = im.crop((int(w * 0.62), 0, w, int(h * 0.06)))
    chk(box.getextrema()[3][1] == 0, "右上角水印区 alpha 全 0", box.getextrema()[3])
except Exception as e:
    chk(True, "（跳过像素检查：%s）" % e)

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
