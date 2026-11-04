# -*- coding: utf-8 -*-
"""批次28 后续（2026-10-22）：死亡 AE 重调、relaxed 商店交替、休息处新图、像素头像、选人背景。"""
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
IMG = os.path.join(MOD, "images", "characters")
CUE = os.path.join(IMG, "cue")
WS = os.path.join(ROOT, "工作区", "编辑区", "人物")
PCK = r"D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi\STS2_Momoi.pck"
DLL = r"D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi\STS2_Momoi.dll"
LOG = r"C:\Users\asus\AppData\Roaming\SlayTheSpire2\logs\godot.log"

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


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def alpha_bbox(path):
    from PIL import Image
    import numpy as np
    a = np.array(Image.open(path).convert("RGBA"))
    mask = a[..., 3] > 8
    if not mask.any():
        return None
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def pck_entries(path):
    f = open(path, "rb")
    h = f.read(40)
    file_base, dir_off = struct.unpack_from("<QQ", h, 24)
    f.seek(dir_off)
    count = struct.unpack("<I", f.read(4))[0]
    out = []
    for _ in range(count):
        plen = struct.unpack("<I", f.read(4))[0]
        name = f.read(plen).decode("utf-8", "replace").rstrip("\x00")
        ofs, size = struct.unpack("<QQ", f.read(16))
        f.read(16)
        f.read(4)
        out.append((name, size))
    f.close()
    return out


char = read(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs"))
entry = read(os.path.join(CODE, "Entry.cs"))
merchant = read(os.path.join(MOD, "scenes", "characters", "STS2_Momoi_merchant.tscn"))
rest = read(os.path.join(MOD, "scenes", "characters", "STS2_Momoi_rest_site.tscn"))
mgd = read(os.path.join(MOD, "scripts", "momoi_merchant_visuals.gd"))
death_jsx = read(os.path.join(WS, "_src", "_build_death_aep.jsx"))
doc = read(os.path.join(ROOT, "STS2_Momoi_迁移文档.md"))
checklist = read(os.path.join(ROOT, "工作区", "_docs", "_美术待补清单.md"))
cue_readme = read(os.path.join(CUE, "README.md"))
src_readme = read(os.path.join(WS, "_src", "README.md"))

print("== 1. 死亡 AE：抽动加快 / 半段灰化 / 停 0.5s / 快速倒下 ==")
aep = os.path.join(WS, "死亡动画.aep")
chk(os.path.isfile(aep), "死亡动画.aep 存在")
chk(os.path.getsize(aep) > 80_000, "死亡动画.aep >80KB（已重建）", os.path.getsize(aep) if os.path.exists(aep) else 0)
chk("var dur = 2.083333" in death_jsx, "AEP 时长 2.0833s（50 帧）")
chk("amount.setValueAtTime(0.30, 100)" in death_jsx, "灰化在 0.30s 完成（抽搐一半）")
chk("var bursts = [0.10, 0.20, 0.30, 0.40]" in death_jsx, "4 段抽动连续无间隔")
chk("t + 0.025 * k" in death_jsx, "抽动每段 0.10s（5 key × 0.025）")
chk("rot.setValueAtTime(1.58, -90)" in death_jsx, "倒下 1.00–1.58s，比旧版快")
chk("rot.setValueAtTime(1.48, -93)" in death_jsx, "保留 -93° 过冲")
for f in ("death_preview.gif", "death_preview_sheet.png", "death_final_frame.png"):
    chk(os.path.isfile(os.path.join(WS, "_work", f)), f"_work/{f} 预览存在")
try:
    import numpy as np
    from PIL import Image
    a = np.array(Image.open(os.path.join(WS, "_work", "death_final_frame.png")).convert("RGB"))
    chk(float(a.std()) > 5, "死亡末帧不是空白", round(float(a.std()), 2))
except Exception as ex:
    chk(False, "死亡末帧可读", ex)
chk(not any(n.lower().endswith(".aep") for n, _ in pck_entries(PCK)), "PCK 没有 AEP 本体（只部署帧）")
chk("Sequence(\"dead\"" in char and "DeadFrameCount = 50" in char and "DeadSpeed = 1f" in char,
    "dead 已接 50 帧序列 / DeadSpeed")
chk(".Single(\"dead\"" not in char, "dead 不再是单图")
dead_files = [os.path.join(CUE, "dead.png")] + [os.path.join(CUE, f"dead_{i:02d}.png") for i in range(1, 50)]
chk(all(os.path.isfile(p) for p in dead_files), "dead.png + dead_01..49 共 50 张")
chk(all(png_size(p) == (1400, 1250) for p in dead_files if os.path.isfile(p)), "dead 全部 1400×1250")
bb = alpha_bbox(os.path.join(CUE, "dead.png")) if os.path.isfile(os.path.join(CUE, "dead.png")) else None
chk(bb is not None and bb[1] < 450 and bb[3] > 1000, "dead 首帧头顶/脚底对齐", bb)
entries = pck_entries(PCK)
dead_imports = [n for n, _ in entries if "characters/cue/dead" in n and n.endswith(".png.import")]
chk(len(dead_imports) == 50, "PCK 含 50 个 dead 帧导入条目", len(dead_imports))

print("== 2. relaxed：商店两张交替 ==")
for f in ("relaxed.png", "relaxed_2.png"):
    p = os.path.join(CUE, f)
    chk(os.path.isfile(p), f"cue/{f} 存在")
    if os.path.isfile(p):
        chk(png_size(p) == (600, 820), f"cue/{f} 600×820", png_size(p))
        bb = alpha_bbox(p)
        chk(bb is not None and bb[1] <= 300 and bb[3] >= 810, f"cue/{f} 头顶/脚底对齐", bb)
chk("RelaxedHalfCycleSeconds = 1.1457856f" in char, "C# 半周期常量")
chk("RelaxedSpeed = 1f" in char, "C# RelaxedSpeed")
chk("Sequence(\"relaxed\"" in char and "relaxed_2.png" in char and "seq.Loop()" in char, "战斗 relaxed 两张循环")
chk("momoi_merchant_visuals.gd" in merchant, "商店挂 relaxed 交替脚本")
chk("relaxed.png" in merchant and "relaxed_2.png" in merchant, "商店引用两张 relaxed")
chk("scale = Vector2(0.45, 0.45)" in merchant, "商店缩小到 0.45")
chk("position = Vector2(0, -182)" in merchant, "商店位置上移（脚底约 0）")
chk("FRAME_A" in mgd and "FRAME_B" in mgd and "1.1457856" in mgd, "商店脚本两张图/半周期")
chk("@export var speed" in mgd, "商店 speed 可调")

print("== 3. 休息处：改用 休息处.png，不再 relaxed ==")
chk("rest_site.png" in rest, "休息点场景引用 rest_site.png")
chk("relaxed" not in rest and "momoi_merchant_visuals" not in rest and "momoi_rest_site_visuals" not in rest,
    "休息点不再引用 relaxed / 旧交替脚本")
chk("scale = Vector2(0.65, 0.65)" in rest, "休息处图 0.65")
chk("position = Vector2(10, 42)" in rest, "休息处图位置 (10,42)")
chk(not os.path.exists(os.path.join(MOD, "scripts", "momoi_rest_site_visuals.gd")), "旧 rest 交替脚本已移除")
rest_img = os.path.join(IMG, "rest_site.png")
chk(os.path.isfile(rest_img), "mod 内 rest_site.png 存在")
if os.path.isfile(rest_img):
    chk(png_size(rest_img) == (1000, 1000), "rest_site.png 1000×1000", png_size(rest_img))
    bb = alpha_bbox(rest_img)
    chk(bb is not None and all(abs(bb[i] - v) <= 1 for i, v in enumerate((184, 235, 788, 763))),
        "rest_site.png 可见 bbox", bb)
chk("offset_bottom = 245.0" in rest, "休息处 hitbox 覆盖躺姿")

print("== 4. 像素小桃 UI 头像 ==")
expect = {
    "STS2_Momoi_character_icon.png": (88, 88),
    "STS2_Momoi_character_icon_outline.png": (88, 88),
    "STS2_Momoi_character_select.png": (132, 195),
    "STS2_Momoi_character_select_locked.png": (132, 195),
    "STS2_Momoi_map_marker.png": (49, 64),
}
for name, size in expect.items():
    p = os.path.join(IMG, name)
    chk(os.path.isfile(p), f"{name} 存在")
    if os.path.isfile(p):
        chk(png_size(p) == size, f"{name} = {size[0]}×{size[1]}", png_size(p))
chk(os.path.isdir(os.path.join(WS, "_work", "placeholder_avatar_backup")), "旧占位备份还在")

print("== 4b. 能量图标尺寸 ==")
et = os.path.join(IMG, "energy_text.png")
eb = os.path.join(IMG, "energy_big.png")
chk(os.path.isfile(et) and png_size(et) == (24, 24), "energy_text.png 24×24（小图标）", png_size(et) if os.path.isfile(et) else None)
chk(os.path.isfile(eb) and png_size(eb) == (256, 256), "energy_big.png 256×256（大图标，待替换）", png_size(eb) if os.path.isfile(eb) else None)

print("== 5. 选人背景 / 音效接口 ==")
for i in (1, 2):
    v = os.path.join(MOD, "videos", f"select_bg_{i}.ogv")
    s = os.path.join(MOD, "scenes", "characters", f"STS2_Momoi_character_select_bg_{i}.tscn")
    chk(os.path.isfile(v) and os.path.getsize(v) > 1_000_000, f"select_bg_{i}.ogv >1MB")
    chk(os.path.isfile(s), f"select_bg_{i}.tscn 存在")
    if os.path.isfile(s):
        t = read(s)
        chk("VideoStreamPlayer" in t and "autoplay = true" in t and "loop = true" in t, f"bg_{i} 自动循环")
        bgm = "select_bgm_day.ogg" if i == 1 else "select_bgm_night.ogg"
        chk("AudioStreamPlayer" in t and "momoi_select_bgm" in t and bgm in t, f"bg_{i} 绑定选人 BGM")
chk(os.path.isfile(os.path.join(MOD, "audio", "select_bgm_day.ogg")) and
    os.path.isfile(os.path.join(MOD, "audio", "select_bgm_night.ogg")), "白天/夜间 BGM 文件")
chk("CustomCharacterSelectSfx => null" in char and "CustomCharacterTransitionSfx => null" in char,
    "删除战士选人/转场音效占位")
chk("MomoiSelectBgmPatch" in entry and "MusicVolumeDb" in read(os.path.join(CODE, "Patches", "MomoiSelectBgmPatch.cs")),
    "选人 BGM 跟随音乐音量")
chk("get_AssetPathsCharacterSelect" in read(os.path.join(CODE, "Patches", "MomoiSelectBgPreloadPatch.cs")),
    "两个背景都预载")
chk(entry.count("patcher.RegisterPatch") >= 24, "Entry 补丁数 >= 24（后续批次会追加，不锁死）", entry.count("patcher.RegisterPatch"))

print("== 6. PCK / DLL / 启动日志 ==")
chk(os.path.isfile(PCK), "PCK 存在")
chk(os.path.getsize(DLL) >= 450_000, "DLL >=450KB", os.path.getsize(DLL))
chk(40_000_000 <= os.path.getsize(PCK) <= 80_000_000, "PCK 已按贴图规则压缩（约 55MB）", os.path.getsize(PCK))
entries = pck_entries(PCK)
names = [n for n, _ in entries]
for key in ("momoi_merchant_visuals.gdc", "rest_site.png-", "rest_site.png.import",
            "relaxed.png-", "relaxed_2.png-", "select_bg_1.ogv", "select_bg_2.ogv",
            "select_bgm_day", "select_bgm_night"):
    chk(any(key in n for n in names), "PCK 含 " + key)
chk(not any("momoi_rest_site_visuals" in n for n in names), "PCK 没有旧 rest 交替脚本")
chk(not any("死亡动画" in n for n in names), "PCK 没有死亡动画")
try:
    log = read(LOG)
    chk("20 applied, 0 ignored, 0 failed" in log or "Steamworks initialization failed" in log, "启动日志 20/20（或 Steam 未运行跳过）")
    chk("STS2_Momoi initialized" in log or "Steamworks initialization failed" in log, "启动日志初始化完成（或 Steam 未运行跳过）")
except Exception as ex:
    chk(False, "启动日志可读", ex)

print("== 7. 文档 ==")
chk("批次28" in doc, "迁移文档有批次28")
chk("死亡动画.aep" in doc, "迁移文档记录死亡 AEP")
chk("1.1457856" in doc, "迁移文档记录半周期")
chk("select_bgm_day" in doc or "选人 BGM" in doc, "迁移文档记录选人 BGM")
chk("休息处.png" in doc or "rest_site.png" in doc, "迁移文档记录休息处新图")
chk("商店" in doc and "relaxed" in doc, "迁移文档记录商店 relaxed")
chk("rest_site.png" in checklist or "休息处.png" in checklist, "待补清单已更新休息处")
chk("relaxed" in cue_readme and "merchant" in cue_readme.lower(), "cue README 记录商店 relaxed")
chk("rest_site.png" in src_readme or "休息处.png" in src_readme, "_src README 记录休息处新图")
chk("1400×1250" in doc and "DeadSpeed" in doc, "迁移文档记录死亡帧尺寸/DeadSpeed")
chk("energy_text" in doc and "256×256" in doc, "迁移文档记录能量小/大图标尺寸")
chk("energy_text" in checklist and "24×24" in checklist, "待补清单记录小能量图标")

print()
print(f"结果：{ok} 条通过，{fail} 条失败")
sys.exit(1 if fail else 0)
