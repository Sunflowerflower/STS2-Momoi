# -*- coding: utf-8 -*-
"""批次43 自检：设置页微调（隐藏简介 / progress 去掉说明卡）+ 预览图 + 本地发布 zip。"""
import json
import os
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MODDIR = os.path.join(ROOT, "STS2 Momoi")
CODE = os.path.join(MODDIR, "STS2 MomoiCode")
MODS = r"D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi"
OUT = os.path.join(ROOT, "工作区", "发布包")

ok = fail = 0


def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))


settings = open(os.path.join(CODE, "Settings", "MomoiSettings.cs"), encoding="utf-8").read()
manifest = json.load(open(os.path.join(MODDIR, "STS2_Momoi.json"), encoding="utf-8"))

print("== 1. 设置页（批次43 微调）==")
chk("WithDescriptionHidden(true)" in settings, "隐藏设置页的模组简介")
chk("RequiresEpochAndTimeline = false" not in settings, "progress 不再解释「不需要纪元/时间线」")
i = settings.find('.AddSection("progress"')
j = settings.find('.AddSection("diagnostics"')
seg = settings[i:j]
chk("AddInfoCard" not in seg, "progress 里没有说明卡了")
chk("reset_settings" in seg and "ResetToDefaults" in seg, "progress 只留「重置本模组设置」")
chk('ModSettingsText.Literal("其他")' in seg, "该节标题改成「其他」")
chk("OS.GetUserDataDir()" in settings and '"logs"' in settings, "日志目录按当前账号 user:// 解析（跨平台）")
chk("%APPDATA%" not in settings, "界面文案里不再写死 Windows 路径")

print("== 2. 预览图 ==")
prev = os.path.join(ROOT, "工作区", "美术成品区", "模组头像.png")
chk(os.path.exists(prev), "使用用户给的 模组头像.png")
if os.path.exists(prev):
    chk(os.path.getsize(prev) < 1024 * 1024, "预览图 < 1 MB（%d B）" % os.path.getsize(prev))
chk(not os.path.exists(os.path.join(ROOT, "工作区", "美术成品区", "工坊预览图_512.png")),
    "我合成的旧预览图已删除")

print("== 3. 部署目录（本地 mod 形态）==")
mod_id = manifest["id"]
for f in (f"{mod_id}.dll", f"{mod_id}.pck", f"{mod_id}.json"):
    chk(os.path.isfile(os.path.join(MODS, f)), "mods/STS2_Momoi/%s 存在" % f)
chk(manifest.get("has_dll") is True and manifest.get("has_pck") is True, "清单 has_dll / has_pck = true")
chk([d.get("id") for d in manifest.get("dependencies", [])] == ["STS2-RitsuLib"], "dependencies = RitsuLib")

print("== 4. 发布 zip ==")
zip_path = os.path.join(OUT, "STS2_Momoi_v%s.zip" % manifest["version"])
chk(os.path.isfile(zip_path), "zip 已生成：%s" % os.path.basename(zip_path))
if os.path.isfile(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        tops = {n.split("/")[0] for n in names}
        chk(tops == {"STS2_Momoi"}, "zip 顶层就是 STS2_Momoi/ 文件夹", tops)
        for f in ("STS2_Momoi.json", "STS2_Momoi.dll", "STS2_Momoi.pck"):
            chk("STS2_Momoi/" + f in names, "包内包含 " + f)
        chk("STS2_Momoi/README.txt" in names, "包内有安装说明 README.txt")
        inner = json.loads(z.read("STS2_Momoi/STS2_Momoi.json").decode("utf-8-sig"))
        chk(inner["name"] == "游戏王小桃" and inner["version"] == manifest["version"], "包内清单版本一致")
        txt = z.read("STS2_Momoi/README.txt").decode("utf-8-sig")
        chk("RitsuLib" in txt and "mods/" in txt, "安装说明提到依赖与解压路径")

print("== 5. 发布清单文档 ==")
guide = os.path.join(ROOT, "工作区", "_docs", "_发布清单.md")
g = open(guide, encoding="utf-8").read()
chk("模组头像.png" in g, "清单引用 模组头像.png")
chk("_make_release_zip.py" in g and "发布包" in g, "清单写了本地 zip 打包方式")
chk("禁用" in g and "版本号" in g, "清单里有「本地版与工坊版 id 冲突」提醒")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
