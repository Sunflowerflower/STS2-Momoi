# -*- coding: utf-8 -*-
"""工坊发布图：模组头像.png -> image.jpg(<1MB)；工坊预览图/*.png -> 截图/NN.jpg(<1MB)。
规则：不要用中文文件名当命令行参数，路径在脚本里用 os.listdir/glob 拼。
"""
import os
import glob
import shutil
from PIL import Image

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
ART = os.path.join(ROOT, "工作区", "美术成品区")
OUT = os.path.join(ROOT, "工作区", "工坊发布")
SHOT_OUT = os.path.join(OUT, "截图")
LIMIT = 1 * 1024 * 1024 - 4096  # 官方限制 1MB，留点余量

os.makedirs(SHOT_OUT, exist_ok=True)


def flatten(im):
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (0, 0, 0))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def save_jpeg(im, path, q):
    while True:
        im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        size = os.path.getsize(path)
        if size <= LIMIT or q <= 60:
            return size, q
        q -= 5


def compress(src, dst, max_w=None, q=90):
    im = Image.open(src)
    im = flatten(im)
    if max_w and im.width > max_w:
        h = round(im.height * max_w / im.width)
        im = im.resize((max_w, h), Image.LANCZOS)
    size, used_q = save_jpeg(im, dst, q)
    return im.size, size, used_q


# 1) 工坊预览图（单个 image.jpg，<1MB）
avatar = None
for name in os.listdir(ART):
    if name.endswith(".png") and "头像" in name:
        avatar = os.path.join(ART, name)
        break
assert avatar, "找不到模组头像.png"
dst = os.path.join(OUT, "image.jpg")
size, bytes_, q = compress(avatar, dst, q=92)
print(f"image.jpg  <- {os.path.basename(avatar)}  {size[0]}x{size[1]}  {bytes_/1024:.0f}KB  q{q}")

# 2) 截图
shots_dir = os.path.join(ART, "工坊预览图")
shots = sorted(glob.glob(os.path.join(shots_dir, "*.png")),
               key=lambda p: int(os.path.splitext(os.path.basename(p))[0])
               if os.path.splitext(os.path.basename(p))[0].isdigit() else 999)
print(f"\n截图 {len(shots)} 张 -> {SHOT_OUT}")
total = 0
for src in shots:
    stem = os.path.splitext(os.path.basename(src))[0]
    if stem.isdigit():
        stem = f"{int(stem):02d}"
    dst = os.path.join(SHOT_OUT, stem + ".jpg")
    size, bytes_, q = compress(src, dst, max_w=1920, q=88)
    total += bytes_
    print(f"  {os.path.basename(src):>12} -> {stem}.jpg  {size[0]}x{size[1]}  {bytes_/1024:.0f}KB  q{q}")
print(f"截图合计 {total/1024/1024:.1f}MB")
