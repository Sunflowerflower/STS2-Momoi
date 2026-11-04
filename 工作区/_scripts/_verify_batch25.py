# -*- coding: utf-8 -*-
"""批次25 自检：攻击1/2/3、能力1/2、嘲讽1 的素材与按卡牌类型路由。"""
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

EXPECTED = {
    "attack1": (8, (600, 820), 21),
    "attack2": (24, (716, 820), 31),
    "attack3": (16, (644, 820), 31),
    "taunt1": (21, (600, 820), 38),
    "cast1": (24, (600, 820), 48),
    "cast2": (12, (600, 820), 46),
}

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


def parse_pairs(src, name):
    m = re.search(rf"{name}\s*=\s*\[(.*?)\];", src, re.S)
    if not m:
        return None
    return [(int(a), int(b)) for a, b in re.findall(r"\((\d+),\s*(\d+)\)", m.group(1))]


cs = read(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs"))
entry = read(os.path.join(CODE, "Entry.cs"))
patch = read(os.path.join(CODE, "Patches", "MomoiCardAnimationCuePatch.cs"))

print("== 1. 速度参数 ==")
for speed in ("Attack1Speed", "Attack2Speed", "Attack3Speed", "Cast1Speed", "Cast2Speed", "Taunt1Speed"):
    chk(f"private const float {speed} = 1f;" in cs, f"{speed} 存在且默认 1")

print("== 2. 序列数据 ==")
for name, (_, _, total) in EXPECTED.items():
    arr = parse_pairs(cs, name.replace("attack", "Attack").replace("cast", "Cast").replace("taunt", "Taunt") + "Frames")
    chk(arr is not None, f"{name} 数组可解析")
    if arr:
        chk(sum(h for _, h in arr) == total, f"{name} 总帧 {total}", sum(h for _, h in arr))
        chk(len(arr) > 0, f"{name} 有唯一帧", len(arr))

print("== 3. cue 集 ==")
for name in EXPECTED:
    cue = name
    chk(f'.Sequence("{cue}"' in cs, f"cue {cue} 已接入")
chk('.Single("attack"' not in cs and '.Single("cast"' not in cs, "旧 attack/cast 占位已移除")

print("== 4. 状态机 ==")
for state in ("attack1", "attack2", "attack3", "cast1", "cast2", "taunt1"):
    trigger = state[0].upper() + state[1:]
    chk(f'b.AddState("{state}")' in cs and f'b.AddAnyState("{trigger}"' in cs,
        f"状态/触发器 {state}")
chk('b.AddAnyState("Attack", "attack1")' in cs, "非卡牌 Attack 回退 attack1")
chk('b.AddAnyState("Cast", "cast1")' in cs and 'b.AddAnyState("PowerUp", "cast1")' in cs,
    "非卡牌 Cast/PowerUp 回退 cast1")

print("== 5. 卡牌分流 ==")
chk("card is Taunt or WinCard" in patch and '"Taunt1"' in patch, "嘲讽 / WIN！ -> Taunt1")
chk("card is ConceptCard" in patch and '"Attack3"' in patch, "构想 -> Attack3")
chk("MinigameSupport.IsSupportCardType(card) ? \"Attack2\" : \"Attack1\"" in patch,
    "支援攻击牌 -> Attack2，其他攻击 -> Attack1")
chk("card.Rarity == CardRarity.Rare ? \"Cast2\" : \"Cast1\"" in patch,
    "稀有 Power -> Cast2，其他 Power -> Cast1")
chk("return null;" in patch, "普通技能/状态/诅咒 -> 暂无动画")

print("== 6. 补丁 ==")
chk("MomoiBeforeCardPlayedCuePatch" in entry, "BeforeCardPlayed 补丁已登记")
chk("MomoiAfterCardPlayedCuePatch" in entry, "AfterCardPlayed 补丁已登记")
chk("MomoiStateMachineCueSuppressPatch" in entry, "SetTrigger 压制补丁已登记")
chk("Hook.BeforeCardPlayed" in patch, "目标 BeforeCardPlayed")
chk("Hook.AfterCardPlayed" in patch, "目标 AfterCardPlayed")
chk("ModAnimStateMachine.SetTrigger" in patch, "目标 SetTrigger")
chk("node.SetAnimationTrigger(cue)" in patch and "Suppress(node.Visuals)" in patch,
    "出牌时主动播 cue 并加压制")

print("== 7. PNG 文件 ==")
try:
    import numpy as np
    from PIL import Image
    have_pil = True
except Exception as e:  # pragma: no cover
    have_pil = False
    print("  (PIL/numpy 不可用，跳过像素检查)", e)

for cue, (count, size, _) in EXPECTED.items():
    files = sorted(glob.glob(os.path.join(CUE, cue + "*.png")))
    chk(len(files) == count, f"{cue} 文件数 {count}", len(files))
    chk(all(os.path.exists(f + ".import") for f in files), f"{cue} .import 齐全")
    if have_pil and files:
        sizes = set()
        spill = 0
        wm = 0
        bottoms = []
        for f in files:
            im = Image.open(f).convert("RGBA")
            sizes.add(im.size)
            a = np.array(im).astype(np.int16)
            rgb, al = a[..., :3], a[..., 3]
            m = al > 200
            if m.any():
                spill = max(spill, int((rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2]))[m].max()))
            wm = max(wm, int(al[0:100, 560:].max()))
            ys, _ = np.where(al > 8)
            bottoms.append(int(ys.max()))
        chk(sizes == {size}, f"{cue} 画布 {size}", sizes)
        chk(spill == 0, f"{cue} 无绿边", spill)
        chk(wm == 0, f"{cue} 无水印", wm)
        chk(min(bottoms) >= 795, f"{cue} 脚底接地", (min(bottoms), max(bottoms)))

print("== 8. manifest ==")
mpath = os.path.join(WORK, "anim_manifest.json")
chk(os.path.exists(mpath), "anim_manifest 存在")
if os.path.exists(mpath):
    man = json.load(open(mpath, encoding="utf-8"))
    chk(len(man.get("anims", [])) == 6, "6 个动画")
    for a in man.get("anims", []):
        cue = a.get("cue")
        if cue in EXPECTED:
            chk(a.get("frames") == EXPECTED[cue][2], f"{cue} 总帧", a.get("frames"))
            chk(len(a.get("groups", [])) == EXPECTED[cue][0], f"{cue} 唯一帧", len(a.get("groups", [])))

print()
print(f"结果：{ok} 通过 / {fail} 失败")
sys.exit(1 if fail else 0)
