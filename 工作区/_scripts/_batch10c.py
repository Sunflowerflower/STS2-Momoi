# -*- coding: utf-8 -*-
"""批次10c：
1) 把「美味饼干_王小桃.png」接入 VanillaRelicVisualOverrides（原版遗物 YUMMY_COOKIE 的角色专属贴图）。
2) 为 9 个自建遗物 + 美味饼干生成正确的白色剪影轮廓图（原版 relic_outline_atlas 就是纯白剪影），
   替换掉现在「轮廓图 = 彩色原图」的错误写法。
用法：python _batch10c.py [--dry]
"""
import os
import shutil
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
BACKUP = os.path.join(ROOT, "工作区", "_backup", "batch10c_pre")
SRC_COOKIE = os.path.join(ROOT, "工作区", "遗物成品区", "美味饼干_王小桃.png")
RELICS_DIR = os.path.join(MOD, "images", "relics")

COOKIE_NAME = "YummyCookie_Momoi"


def silhouette(src_path, dst_path):
    """把一张图变成纯白剪影（保留整体外轮廓，填掉内部所有孔洞），透明底。"""
    im = Image.open(src_path).convert("RGBA")
    a = np.array(im)[:, :, 3]
    mask = a > 32

    # 从四条边洪水填充求“外部”，剩下的非 mask 区域就是孔洞 → 填满
    h, w = mask.shape
    outside = np.zeros_like(mask)
    stack = []
    for x in range(w):
        for y in (0, h - 1):
            if not mask[y, x] and not outside[y, x]:
                stack.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if not mask[y, x] and not outside[y, x]:
                stack.append((y, x))
    while stack:
        y, x = stack.pop()
        if outside[y, x] or mask[y, x]:
            continue
        outside[y, x] = True
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not outside[ny, nx] and not mask[ny, nx]:
                stack.append((ny, nx))

    solid = mask | (~outside)
    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[solid] = (255, 255, 255, 255)
    Image.fromarray(out, "RGBA").save(dst_path)
    return int(solid.sum()), int(mask.sum())


def main():
    if not os.path.exists(SRC_COOKIE):
        raise SystemExit("找不到源图: " + SRC_COOKIE)

    # 1) 复制美味饼干
    dst_cookie = os.path.join(RELICS_DIR, COOKIE_NAME + ".png")
    print("[复制] %s -> images/relics/%s.png" % ("美味饼干_王小桃.png", COOKIE_NAME))

    # 2) 生成轮廓
    targets = sorted(f for f in os.listdir(RELICS_DIR) if f.endswith(".png"))
    print("[轮廓] 将为以下 %d 张图生成 _outline.png：%s" % (len(targets), targets))

    if DRY:
        print("\n--dry 结束，未改动任何文件。")
        return

    os.makedirs(BACKUP, exist_ok=True)
    shutil.copy2(SRC_COOKIE, dst_cookie)
    print("  已写入 %s" % os.path.relpath(dst_cookie, ROOT))

    for f in targets:
        src = os.path.join(RELICS_DIR, f)
        dst = os.path.join(RELICS_DIR, f[:-4] + "_outline.png")
        solid, mask = silhouette(src, dst)
        print("  %-28s 轮廓像素 %6d / 原不透明 %6d" % (f, solid, mask))

    print("\n备份目录: %s（本次未覆盖旧文件，仅新增）" % os.path.relpath(BACKUP, ROOT))


if __name__ == "__main__":
    main()
