# -*- coding: utf-8 -*-
"""批次26 自检：受击动画.psd -> hit 序列（9 帧 / 1.0s / HitSpeed）。"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
CUE = os.path.join(MOD, "images", "characters", "cue")
WORK = os.path.join(ROOT, "工作区", "编辑区", "人物", "_work")

ok = fail = 0


def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))


def read(path):
    return open(path, encoding="utf-8").read()


cs = read(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs"))

print("== 1. C# ==")
chk("private const float HitSpeed = 1f;" in cs, "HitSpeed 默认 1")
m = re.search(r"HitFrames\s*=\s*\[(.*?)\];", cs, re.S)
chk(m is not None, "HitFrames 可解析")
frames = [(int(a), int(b)) for a, b in re.findall(r"\((\d+),\s*(\d+)\)", m.group(1))] if m else []
chk(len(frames) == 8, "8 个序列条目（1,3,5,7,8,9,8,7）", len(frames))
chk(sum(h for _, h in frames) == 24, "Hold 合计 24（24fps 下 1.0s）", sum(h for _, h in frames))
chk([f for f, _ in frames] == [0,2,4,6,7,8,7,6], "帧顺序 1,3,5,7,8,9,8,7")
chk('.Sequence("hit"' in cs, "hit 使用 Sequence")
chk('.Single("hit"' not in cs, "旧单张 hit 已移除")
chk('b.AddState("hit").WithNext("idle")' in cs, "状态机 hit -> idle")

print("== 2. 文件 / 像素 ==")
names = ["hit.png"] + [f"hit_{i:02d}.png" for i in range(1, 9)]
missing = [n for n in names if not os.path.exists(os.path.join(CUE, n))]
chk(not missing, "9 张 hit 帧都存在", missing)
chk(all(os.path.exists(os.path.join(CUE, n + ".import")) for n in names), ".import 齐全")
chk(len(glob.glob(os.path.join(CUE, "hit*.png"))) == 9, "目录里正好 9 张 hit PNG")

try:
    import numpy as np
    from PIL import Image
    have_pil = True
except Exception as e:  # pragma: no cover
    have_pil = False
    print("  (PIL/numpy 不可用，跳过像素检查)", e)

if have_pil:
    sizes = set()
    spill = 0
    wm = 0
    bottoms = []
    for n in names:
        im = Image.open(os.path.join(CUE, n)).convert("RGBA")
        sizes.add(im.size)
        a = np.array(im).astype(np.int16)
        rgb, al = a[..., :3], a[..., 3]
        msk = al > 200
        if msk.any():
            spill = max(spill, int((rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2]))[msk].max()))
        wm = max(wm, int(al[0:100, 560:].max()))
        ys, _ = np.where(al > 8)
        bottoms.append(int(ys.max()))
    chk(sizes == {(600, 820)}, "画布 600×820", sizes)
    chk(spill == 0, "无绿边", spill)
    chk(wm == 0, "无水印", wm)
    chk(min(bottoms) >= 810, "脚底接地", (min(bottoms), max(bottoms)))

    # head/body size: compare blonde hair area with idle
    def hair_px(path):
        a = np.array(Image.open(path).convert("RGBA"))
        m = a[..., 3] > 200
        c = a[m][:, :3]
        h = (c[:, 0] > 200) & (c[:, 1] > 160) & (c[:, 1] < 225) & (c[:, 2] > 80) & (c[:, 2] < 170)
        return int(h.sum())
    hi = hair_px(os.path.join(CUE, "hit.png"))
    ii = hair_px(os.path.join(CUE, "idle.png"))
    chk(abs(hi / ii - 1.0) < 0.12, "受击头部大小与待机接近", (hi, ii, hi / ii))

print("== 3. manifest ==")
mpath = os.path.join(WORK, "hit_manifest.json")
chk(os.path.exists(mpath), "hit_manifest 存在")
if os.path.exists(mpath):
    man = json.load(open(mpath, encoding="utf-8"))
    chk(man.get("frames") == 9, "manifest 9 帧")
    chk(man.get("holds") == [1, 0, 1, 0, 1, 0, 18, 2, 1], "manifest holds", man.get("holds"))
    chk(man.get("duration_seconds") == 1.0, "manifest 1.0s")
    chk(man.get("total_slots") == 24, "manifest 24 槽")
    chk([(x["frame"], x["hold"]) for x in man.get("sequence", [])] == [(0,1),(2,1),(4,1),(6,1),(7,1),(8,1),(7,1),(6,17)], "manifest 回弹顺序")
    chk(man.get("canvas") == [600, 820], "manifest 600×820")
    chk(man.get("files") == names, "manifest 文件列表")

print()
print(f"结果：{ok} 通过 / {fail} 失败")
sys.exit(1 if fail else 0)
