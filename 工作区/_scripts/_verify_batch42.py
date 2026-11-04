# -*- coding: utf-8 -*-
"""批次42 自检：正式名 / 清单字段 / 版本 / 免纪元 / 设置页四节 + 诊断 + 重置 + 工坊预览图。"""
import glob
import json
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MODDIR = os.path.join(ROOT, "STS2 Momoi")
MOD = os.path.join(MODDIR, "STS2_Momoi")
CODE = os.path.join(MODDIR, "STS2 MomoiCode")

ok = fail = 0


def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))


def read(*parts):
    return open(os.path.join(*parts), encoding="utf-8").read()


manifest = json.load(open(os.path.join(MODDIR, "STS2_Momoi.json"), encoding="utf-8"))
csproj = read(MODDIR, "STS2 Momoi.csproj")
settings = read(CODE, "Settings", "MomoiSettings.cs")
char = read(CODE, "Characters", "STS2 MomoiCharacter.cs")

print("== 1. 清单字段 ==")
chk(manifest["name"] == "游戏王小桃", "name = 游戏王小桃", manifest["name"])
chk(manifest["version"] == "1.0.8", "version = 1.0.8（批次46）", manifest["version"])
chk(manifest["author"] == "alkaid616", "author 不再是占位 Author", manifest["author"])
chk("template" not in manifest["description"].lower(), "description 不再是模板文案")
chk("RitsuLib" in manifest["description"], "description 提到依赖 RitsuLib")
chk(manifest["min_game_version"] == "0.111.0", "min_game_version = 0.111.0", manifest.get("min_game_version"))
chk(manifest["dependencies"][0]["id"] == "STS2-RitsuLib", "依赖仍是 STS2-RitsuLib")
chk(manifest["pck_name"] == "STS2_Momoi" and manifest["id"] == "STS2_Momoi", "id / pck_name 未变（存档与部署路径不变）")

print("== 2. 程序集版本 ==")
chk("<Version>1.0.8</Version>" in csproj, "csproj <Version>1.0.8</Version>（批次46）")
chk("MomoiModInfo" in settings and "ReadModVersion" in settings, "设置页读程序集版本")

print("== 3. 免纪元 / 时间线 ==")
chk("RequiresEpochAndTimeline => false" in char, "角色 RequiresEpochAndTimeline => false")
# 只看「真的挂了纪元要求」的代码（属性 [RequireEpoch… / 注册调用），不匹配说明文本里的字样
req = []
for p in glob.glob(os.path.join(CODE, "**", "*.cs"), recursive=True):
    txt = read(p)
    if re.search(r"\[RequireEpoch|ModUnlockRegistry\.RequireEpoch", txt):
        req.append(os.path.basename(p))
chk(not req, "全模组没有 RequireEpoch 属性/注册", req)

print("== 4. 设置页结构 ==")
chk('ModSettingsText.Literal("游戏王小桃")' in settings, "页标题 = 游戏王小桃")
for sec in ("general", "audio", "progress", "diagnostics"):
    chk('.AddSection("%s"' % sec in settings, "分节 %s" % sec)
chk("philosopher_pool" in settings and "seaglass_pool" in settings, "general 两个卡池开关")
chk(settings.count("AddIntSlider") == 6, "audio 六档音量", settings.count("AddIntSlider"))
chk("reset_settings" in settings and "ResetToDefaults" in settings, "progress：重置设置按钮")
chk("RequiresEpochAndTimeline = false" not in settings, "progress 不再放「不需要纪元」说明卡（批次43）")
chk("open_logs" in settings and "OS.ShellShowInFileManager" in settings, "diagnostics：打开日志目录")
chk("LogsDirectory" in settings and '"logs"' in settings, "日志目录 = user data / logs")
chk("ReleaseInfoManager" in settings, "游戏版本来自 ReleaseInfoManager")
chk("ModSettingsButtonTone.Danger" in settings, "重置按钮用 Danger 色调")
chk("TelemetryRegistry" not in settings and "TelemetryRegistry" not in read(CODE, "Entry.cs"),
    "本版没有注册遥测（用户决定先不接）")

print("== 5. 重置逻辑 ==")
for b in ("PhilosopherPool", "SeaGlassPool", "MasterVolume", "MusicVolume", "VoiceVolume",
          "SfxVolume", "HurtVoiceVolume", "DeathVoiceVolume"):
    chk("%s.Write(defaults." % b in settings and "%s.Save();" % b in settings, "重置 %s" % b)

print("== 6. 工坊配套 ==")
prev = os.path.join(ROOT, "工作区", "美术成品区", "模组头像.png")
chk(os.path.exists(prev), "预览图存在")
if os.path.exists(prev):
    size = os.path.getsize(prev)
    chk(size < 1024 * 1024, "预览图 < 1 MB（%d B）" % size)
    h = open(prev, "rb").read(33)
    wh = struct.unpack(">II", h[16:24])
    chk(wh == (512, 512), "预览图 512×512（用户指定 模组头像.png）", wh)
guide = os.path.join(ROOT, "工作区", "_docs", "_发布清单.md")
chk(os.path.exists(guide), "发布清单文档存在")
if os.path.exists(guide):
    g = open(guide, encoding="utf-8").read()
    chk("Characters" in g and "schinese" in g, "清单里写了工坊 tags（Characters + schinese）")
    chk("STS2-RitsuLib" in g and "依赖" in g, "清单里注明依赖 = STS2-RitsuLib（工坊 ID 留空靠清单解析）")
    chk("ModUpdateCheckOptions" in g, "清单里写了更新检查接入方式")

print("== 7. README 标题 ==")
chk(read(MODDIR, "README.md").startswith("# 游戏王小桃"), "README.md 标题")
chk("Game King Momoi" in read(MODDIR, "README.en.md").split("\n")[0], "README.en.md 标题")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
