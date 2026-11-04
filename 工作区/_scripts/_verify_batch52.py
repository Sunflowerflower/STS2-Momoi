# -*- coding: utf-8 -*-
"""批次52 自检：贴图大小默认 1.0（小桃本体 0.7）+ 出牌卡顿优化（材质/音频缓存、cue 预热、诊断日志开关）。"""
import io
import json
import os
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MODDIR = os.path.join(ROOT, "STS2 Momoi")
CODE = os.path.join(MODDIR, "STS2 MomoiCode")
DEPLOY = r"D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi"
OUT = os.path.join(ROOT, "工作区", "发布包")
WSMOD = os.path.join(ROOT, "工作区", "工坊发布", "STS2_Momoi")
CONTENT = os.path.join(WSMOD, "Content", "STS2_Momoi")
DOC = os.path.join(ROOT, "STS2_Momoi_迁移文档.md")
VER = "1.0.8"

ok = fail = 0


def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("" if detail == "" else "  → " + repr(detail)))


def read(p):
    return io.open(p, encoding="utf-8").read()


def flat(s):
    return " ".join(s.split())


def block(text, name):
    """按花括号深度截出 class/interface name 的定义体。"""
    idx = text.find(name)
    if idx < 0:
        return ""
    start = text.find("{", idx)
    if start < 0:
        return ""
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return ""


print("[1] 设置：贴图大小默认 1.0，范围 0.5~1.5")
cfg = read(os.path.join(CODE, "Settings", "MomoiSettings.cs"))
chk("public double CharacterTextureScale { get; set; } = 1.0;" in cfg, "默认值 1.0",
    cfg.count("CharacterTextureScale { get; set; }"))
chk("Math.Clamp(CharacterTextureScale.Read(), 0.5, 1.5)" in cfg, "读取时钳到 0.5~1.5")
sl = flat(cfg)
chk('"character_texture_scale"' in sl and "0.5," in sl and "1.5," in sl, "滑块范围 0.5~1.5")
chk("0.2," not in sl.replace("0.25", ""), "旧下限 0.2 已移除")
chk('static v => $"{v:0.00}x"' in cfg, "滑块仍显示两位小数")

print("[2] 小桃本体额外 0.7（设置界面不暴露）")
patch = read(os.path.join(CODE, "Patches", "MomoiCharacterScalePatch.cs"))
chk("public const float MomoiDefaultScale = 0.7f;" in patch, "写死 0.7 常量")
chk("size *= MomoiSettingsStore.TextureScaleFactor;" in patch, "先乘设置倍率")
chk("size *= MomoiDefaultScale;" in patch, "小桃再乘 0.7")
chk("is STS2_MomoiCharacter" in patch, "按角色类判定是否小桃")
chk("using STS2_Momoi.Characters;" in patch, "引入角色命名空间")
chk(patch.count("size *=") == 2, "只有两处相乘（不重复叠加设置倍率）", patch.count("size *="))

print("[3] 诊断日志开关 + MomoiDiag")
diag_path = os.path.join(CODE, "Diagnostics", "MomoiDiag.cs")
chk(os.path.exists(diag_path), "Diagnostics/MomoiDiag.cs 存在")
diag = read(diag_path) if os.path.exists(diag_path) else ""
chk("public static bool Enabled => MomoiSettingsStore.VerboseLogging.Read();" in diag, "Enabled 读设置")
chk("public static void Log(" in diag and "public static void Warn(" in diag, "Log/Warn 两个入口")
chk("public bool VerboseLogging { get; set; }" in cfg, "设置项 VerboseLogging（默认 false）")
chk("ModSettingsValueBinding<MomoiModSettings, bool> VerboseLogging" in cfg, "设置绑定")
chk('"verbose_logging"' in flat(cfg), "诊断页新增开关 id")
chk("VerboseLogging.Write(defaults.VerboseLogging);" in cfg and "VerboseLogging.Save();" in cfg, "恢复默认也覆盖")

print("[4] 热路径日志已收口（不再每张牌写盘）")
hot = {
    "Patches/VigorFirepowerPatch.cs": "MomoiDiag.Log",
    "Patches/MomoiCardAnimationCuePatch.cs": "MomoiDiag.Log",
    "Cards/ReworkBatch.cs": "MomoiDiag.Log",
    "Cards/MinigameFlowCards.cs": "MomoiDiag.Log",
}
for rel, needle in hot.items():
    t = read(os.path.join(CODE, rel))
    chk(needle in t, "%s 用 MomoiDiag" % rel)
    chk("Entry.Logger.Info" not in t, "%s 不再有无条件 Info" % rel)
vf = read(os.path.join(CODE, "Patches", "VigorFirepowerPatch.cs"))
chk(vf.count("MomoiDiag.Log") == 6, "活力/火力 6 条日志全部改走开关", vf.count("MomoiDiag.Log"))

print("[5] 卡框材质：只读一次 + 每种图集区域复用一个材质")
mat = read(os.path.join(CODE, "Patches", "MomoiCardFrameMaterialPatch.cs"))
chk("private static Material? _cached;" in mat and "_loadAttempted" in mat, "材质静态缓存")
chk(mat.count("ResourceLoader.Load<Material>") == 1, "只在首次读盘", mat.count("ResourceLoader.Load<Material>"))
vis = read(os.path.join(CODE, "Patches", "MomoiCardFrameVisualPatch.cs"))
chk("static readonly Dictionary<(Vector2 Offset, Vector2 Scale), ShaderMaterial> Variants" in vis, "按 UV 缓存材质变体")
chk("if (!Variants.TryGetValue(key, out var material))" in vis, "命中缓存不再 Duplicate")
chk("ReferenceEquals(frame.Material, material)" in vis, "已赋值就不重复赋值")
chk(vis.count("Duplicate()") == 1, "Duplicate 只保留缓存未命中那一处", vis.count("Duplicate()"))
chk("_source ??= ResourceLoader.Load<ShaderMaterial>" in vis, "源材质只读一次")

print("[6] 音频直放：AudioStream 缓存")
aud = read(os.path.join(CODE, "Audio", "MomoiAudio.cs"))
chk("ConcurrentDictionary<string, AudioStream> StreamCache" in aud, "Stream 缓存表")
chk("StreamCache.GetOrAdd(resourcePath" in aud, "GetOrAdd 读流")
chk(aud.count("ResourceLoader.Load<AudioStream>") == 1, "只在一处读盘", aud.count("ResourceLoader.Load<AudioStream>"))

print("[7] cue 帧贴图预热")
warm_path = os.path.join(CODE, "Patches", "MomoiCueWarmupPatch.cs")
chk(os.path.exists(warm_path), "MomoiCueWarmupPatch.cs 存在")
warm = read(warm_path) if os.path.exists(warm_path) else ""
chk('new(typeof(NCombatRoom), nameof(NCombatRoom.AddCreature))' in warm, "挂在角色加入战斗房间")
chk("ResourceLoader.CacheMode.Reuse" in warm, "用 CacheMode.Reuse 常驻缓存")
chk("DirAccess.Open(" in warm, "枚举 cue 目录")
chk("private const int PerFrame = 4;" in warm, "每帧 4 张，避免开局一次性卡死")
chk("SceneTree.SignalName.ProcessFrame" in warm, "逐帧 await")
chk("creature.Player?.Character is not STS2_MomoiCharacter" in warm, "只对小桃生效")
entry = read(os.path.join(CODE, "Entry.cs"))
chk("patcher.RegisterPatch<Patches.MomoiCueWarmupPatch>();" in entry, "补丁已注册")
chk(entry.index("MomoiCombatRoomAddCreaturePatch") < entry.index("MomoiCueWarmupPatch"), "注册顺序合理")

print("[8] 动画面板监听瘦身")
lowhp = read(os.path.join(CODE, "Patches", "MomoiLowHpPatch.cs"))
track = block(lowhp, "class MomoiAnimMachineTrackPatch")
chk("nameof(ModAnimStateMachine.Start)" in track, "仍在 Start 注册状态机")
chk("nameof(ModAnimStateMachine.SetTrigger)" not in track, "不再挂 SetTrigger（每次触发器都写一次）")

print("[9] 版本与产物")
csproj = read(os.path.join(MODDIR, "STS2 Momoi.csproj"))
man = json.load(io.open(os.path.join(MODDIR, "STS2_Momoi.json"), encoding="utf-8"))
dm = json.load(io.open(os.path.join(DEPLOY, "STS2_Momoi.json"), encoding="utf-8"))
chk("<Version>%s</Version>" % VER in csproj, "csproj 版本 %s" % VER)
chk(man["version"] == VER, "清单版本 %s" % VER, man["version"])
chk(dm["version"] == VER, "部署目录清单版本 %s" % VER, dm["version"])
chk(man["dependencies"] == [{"id": "STS2-RitsuLib", "min_version": "0.6.7"}], "依赖 min_version 0.6.7 未变", man["dependencies"])
dll = os.path.getsize(os.path.join(DEPLOY, "STS2_Momoi.dll"))
pck = os.path.getsize(os.path.join(DEPLOY, "STS2_Momoi.pck"))
chk(500_000 <= dll <= 600_000, "DLL 大小正常", dll)
chk(50_000_000 <= pck <= 70_000_000, "PCK 仍是优化后体积（约 55MB）", pck)
zp = os.path.join(OUT, "STS2_Momoi_v%s.zip" % VER)
chk(os.path.exists(zp), "发布包 %s 存在" % os.path.basename(zp))
if os.path.exists(zp):
    names = zipfile.ZipFile(zp).namelist()
    chk(any(n == "STS2_Momoi/STS2_Momoi.dll" for n in names), "zip 顶层 STS2_Momoi/")
    chk(any(n == "STS2_Momoi/README.txt" for n in names), "zip 含 README.txt")
    old = os.path.join(OUT, "STS2_Momoi_v1.0.7.zip")
    chk(not os.path.exists(old), "旧 1.0.7 压缩包已清理")

print("[10] 工坊 Content 同步")
cm = json.load(io.open(os.path.join(CONTENT, "STS2_Momoi.json"), encoding="utf-8"))
chk(cm["version"] == VER, "工坊 Content 清单 %s" % VER, cm["version"])
chk(os.path.getsize(os.path.join(CONTENT, "STS2_Momoi.dll")) == dll, "工坊 Content DLL 与部署一致")
ws = json.load(io.open(os.path.join(WSMOD, "workspace.json"), encoding="utf-8"))
chk(ws["dependencies"] == [3747602295], "workspace 依赖 RitsuLib 工坊条目", ws["dependencies"])
chk("visibility" not in ws, "workspace 不写 visibility（避免覆盖页面可见性）")

print("[11] 文档")
doc = read(DOC)
chk("### 21.59" in doc, "迁移文档有 §21.59")
tail = doc[doc.index("### 21.59"):] if "### 21.59" in doc else ""
chk("MomoiDefaultScale" in tail or "0.7" in tail, "§21.59 记了小桃 0.7")
chk("MomoiCueWarmup" in tail or "预热" in tail, "§21.59 记了 cue 预热")
chk("VerboseLogging" in tail or "详细日志" in tail, "§21.59 记了诊断日志开关")
chk("2026-11-04 批次52" in doc, "顶部状态块是批次52")

print()
print("结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(0 if fail == 0 else 1)
