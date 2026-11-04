# -*- coding: utf-8 -*-
"""批次10d：搭建「人物战斗模型」的可测试管线。

背景：`STS2 MomoiCharacter.CharacterScenePath` 一直指向 `res://scenes/creature_visuals/ironclad.tscn`，
所以进战斗站着的是原版铁甲战士。这里改成走 RitsuLib 的 VisualCueSet 方案：
  - 战斗场景换成模组自己的 tscn（Sprite2D 为视觉根）
  - cue 图放在 images/characters/cue/，文件名固定：idle / attack / cast / hit / dead / relaxed
  - 现在先用「双刀王小桃」卡面里抠出来的线稿半身像做占位，之后逐张替换同名文件即可

用法：python _batch10d.py [--dry]
"""
import os
import shutil
import sys

import numpy as np
import cv2
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
BACKUP = os.path.join(ROOT, "工作区", "_backup", "batch10d_pre")
SRC_CARD = os.path.join(MOD, "images", "cards", "DualBladeMomoi.png")
CUE_DIR = os.path.join(MOD, "images", "characters", "cue")
TSCN = os.path.join(MOD, "scenes", "characters", "STS2_Momoi_character.tscn")

CANVAS_W, CANVAS_H = 600, 820      # 画布：人物底边贴画布底 = 站在地面线上
CUES = ["idle", "attack", "cast", "hit", "dead", "relaxed"]


def extract_bust():
    """从卡面里抠出线稿半身像，返回 RGBA 图。"""
    a = np.array(Image.open(SRC_CARD).convert("RGB"))
    mask = (~((a > 238).all(axis=2))).astype(np.uint8)
    _, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    # 4=人物主体, 2=头顶光环, 11/12=脸部阴影块
    keep = np.zeros_like(mask)
    for i in (4, 2, 11, 12):
        keep |= (lab == i).astype(np.uint8)
    ys, xs = np.where(keep)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()

    rgba = np.zeros((a.shape[0], a.shape[1], 4), dtype=np.uint8)
    rgba[:, :, :3] = a
    rgba[:, :, 3] = np.where(keep > 0, 255, 0)
    bust = Image.fromarray(rgba[y0:y1 + 1, x0:x1 + 1], "RGBA")

    # 线条压黑一点，战场上更清楚
    arr = np.array(bust).astype(np.float32)
    alpha = arr[:, :, 3:4] / 255.0
    rgb = arr[:, :, :3] * 0.62                     # 提对比
    arr[:, :, :3] = np.clip(rgb, 0, 255)
    bust = Image.fromarray(arr.astype(np.uint8), "RGBA")

    # 等比缩放到画布内，底边对齐画布底边
    scale = min((CANVAS_W - 40) / bust.width, (CANVAS_H - 40) / bust.height)
    bust = bust.resize((max(1, int(bust.width * scale)), max(1, int(bust.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    canvas.alpha_composite(bust, ((CANVAS_W - bust.width) // 2, CANVAS_H - bust.height))
    return canvas


TSCN_TEXT = '''[gd_scene load_steps=3 format=3]

[ext_resource type="Texture2D" path="res://STS2_Momoi/images/characters/cue/idle.png" id="1_idle"]

[node name="STS2_MomoiCharacter" type="Node2D"]

[node name="Visuals" type="Sprite2D" parent="."]
unique_name_in_owner = true
position = Vector2(0, -246)
scale = Vector2(0.6, 0.6)
texture = ExtResource("1_idle")

[node name="Bounds" type="Control" parent="."]
unique_name_in_owner = true
layout_mode = 3
anchors_preset = 0
offset_left = -108.0
offset_top = -500.0
offset_right = 108.0
offset_bottom = 10.0

[node name="IntentPos" type="Marker2D" parent="."]
unique_name_in_owner = true
position = Vector2(28, -510)

[node name="CenterPos" type="Marker2D" parent="."]
unique_name_in_owner = true
position = Vector2(0, -246)

[node name="TalkPos" type="Marker2D" parent="."]
unique_name_in_owner = true
position = Vector2(0, -460)
'''


def main():
    print("[抠图] 从 %s 提取线稿半身像" % os.path.basename(SRC_CARD))
    bust = extract_bust()
    print("       画布 %dx%d，非透明像素 %d" % (bust.width, bust.height,
                                              int((np.array(bust)[:, :, 3] > 0).sum())))
    print("[cue ] 写入 %d 个文件: %s" % (len(CUES), ", ".join(c + ".png" for c in CUES)))
    print("[tscn] 重写 %s" % os.path.relpath(TSCN, ROOT))

    if DRY:
        print("\n--dry 结束，未改动任何文件。")
        return

    os.makedirs(BACKUP, exist_ok=True)
    os.makedirs(CUE_DIR, exist_ok=True)
    if os.path.exists(TSCN):
        shutil.copy2(TSCN, os.path.join(BACKUP, "STS2_Momoi_character.tscn"))

    for c in CUES:
        bust.save(os.path.join(CUE_DIR, c + ".png"))
    with open(TSCN, "w", encoding="utf-8") as f:
        f.write(TSCN_TEXT)
    print("\n完成。备份 -> %s" % os.path.relpath(BACKUP, ROOT))


if __name__ == "__main__":
    main()
