# -*- coding: utf-8 -*-
"""把 mod 的贴图导入参数调小（pck 体积优化，可反复执行）。

背景：pck 里 95% 是贴图，且全部按「无损」存放（1000x760 的卡图 ctex 约 0.5 MB/张）。
Godot 的导入参数写在 `*.png.import` 里（**被 .gitignore 忽略**），所以这脚本就是唯一真源：
清掉 .godot 缓存 / 换机器之后，先跑这个再导出 pck。

规则：
  images/cards/**            → process/size_limit=512（卡面实际显示 < 500px，512 无损够用）
  images/characters/cue/**    → compress/mode=1 有损 + compress/lossy_quality=0.95
                               （600x820 的逐帧动画，q95 可见像素 PSNR ≈ 42 dB，肉眼无差）

用法：
  python 工作区/_scripts/_optimize_textures.py           # 应用
  python 工作区/_scripts/_optimize_textures.py --check   # 只检查是否已应用
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMG = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "images")

CARD_LIMIT = 512
CUE_QUALITY = 0.95

RULES = [
    # (子目录, [(旧片段, 新片段), ...])
    (os.path.join(IMG, "cards"), [("process/size_limit=0", "process/size_limit=%d" % CARD_LIMIT)]),
    (os.path.join(IMG, "characters", "cue"), [
        ("compress/mode=0", "compress/mode=1"),
    ]),
]

# 有损质量强制成 CUE_QUALITY（不论原文件写的是 0.7 / 0.9 还是空），否则只改 mode 不改质量。
CUE_QUALITY_RE = re.compile(r"^compress/lossy_quality=.*$", re.MULTILINE)


def main(check_only):
    changed = already = 0
    touched = []
    for d, pairs in RULES:
        if not os.path.isdir(d):
            print("skip missing dir:", d)
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".png.import"):
                continue
            p = os.path.join(d, name)
            src = io.open(p, encoding="utf-8").read()
            out = src
            for a, b in pairs:
                out = out.replace(a, b)
            if d.endswith("cue"):
                want = "compress/lossy_quality=%s" % CUE_QUALITY
                out = CUE_QUALITY_RE.sub(want, out) if CUE_QUALITY_RE.search(out) else out + want + "\n"
            if out == src:
                already += 1
                continue
            changed += 1
            touched.append(os.path.relpath(p, ROOT))
            if not check_only:
                io.open(p, "w", encoding="utf-8", newline="").write(out)
    verb = "待应用" if check_only else "已更新"
    print("%s %d 个 .import，已是最新 %d 个" % (verb, changed, already))
    for t in touched[:5]:
        print("   ", t)
    if len(touched) > 5:
        print("    ... 共 %d 个" % len(touched))
    if check_only and changed:
        sys.exit(1)


if __name__ == "__main__":
    main("--check" in sys.argv)
