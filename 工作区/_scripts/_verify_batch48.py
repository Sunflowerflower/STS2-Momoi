# -*- coding: utf-8 -*-
"""批次48 自检：RitsuLib 前置依赖（清单 min_version + 工坊 dependencies + 简介前置链接）。"""
import io
import json
import os
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MODDIR = os.path.join(ROOT, "STS2 Momoi")
WS = os.path.join(ROOT, "工作区", "工坊发布")
WSMOD = os.path.join(WS, "STS2_Momoi")
OUT = os.path.join(ROOT, "工作区", "发布包")
DEPLOY = r"D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi"
DOC = os.path.join(ROOT, "STS2_Momoi_迁移文档.md")
URL_RITSU = "https://steamcommunity.com/sharedfiles/filedetails/?id=3747602295"

ok = fail = 0


def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  -> %r" % (detail,)))


def read(p):
    return io.open(p, encoding="utf-8").read()


print("[1] manifest：dependencies 用 min_version")
man = json.loads(io.open(os.path.join(MODDIR, "STS2_Momoi.json"), encoding="utf-8-sig").read())
deps = man.get("dependencies") or []
chk(len(deps) == 1, "只有一个依赖项", deps)
d0 = deps[0] if deps else {}
chk(d0.get("id") == "STS2-RitsuLib", "依赖 id = STS2-RitsuLib", d0)
chk("min_version" in d0, "依赖项有 min_version 键", d0)
chk(d0.get("min_version") == "0.6.7", "min_version = 0.6.7（实测编译底线）", d0.get("min_version"))
chk("version" not in d0, "依赖项不再有会被静默忽略的 version 键", sorted(d0))
chk(man.get("version") == "1.0.8", "mod 自身版本仍是 1.0.8", man.get("version"))

print("[2] csproj：只校验、不改写 min_version")
csproj = read(os.path.join(MODDIR, "STS2 Momoi.csproj"))
chk("ValidateManifestDependencies" in csproj, "csproj 里有 ValidateManifestDependencies 目标")
chk("SyncManifestDependencies" not in csproj, "旧的 SyncManifestDependencies 目标已删除")
chk("min_version" in csproj, "csproj 校验的正则是 min_version")
chk("HIGHER than the RitsuLib package" in csproj, "下限高于编译包时构建报错")
chk("WriteLinesToFile" not in csproj.split("ValidateManifestDependencies")[1],
    "校验目标不再回写 manifest")
chk(re.search(r'Include="STS2\.RitsuLib" Version="\*"', csproj) is not None,
    "包引用恢复为 Version=\"*\"（跟随最新）")

print("[3] 部署目录 + 工坊 Content 的清单同步")
for label, base in (("部署目录", DEPLOY), ("工坊 Content", os.path.join(WSMOD, "Content", "STS2_Momoi"))):
    p = os.path.join(base, "STS2_Momoi.json")
    if not os.path.isfile(p):
        chk(False, "%s 清单存在" % label, p)
        continue
    m = json.loads(io.open(p, encoding="utf-8-sig").read())
    d = (m.get("dependencies") or [{}])[0]
    chk(d.get("min_version") == "0.6.7", "%s 清单 min_version = 0.6.7" % label, d)
    chk("version" not in d, "%s 清单没有 version 键" % label, sorted(d))

print("[4] workspace.json / workshop.json：工坊依赖 + 简介")
for name in ("workspace.json", "workshop.json"):
    p = os.path.join(WSMOD, name)
    chk(os.path.isfile(p), "%s 存在" % name)
    if not os.path.isfile(p):
        continue
    j = json.loads(io.open(p, encoding="utf-8").read())
    chk(j.get("dependencies") == [3747602295], "%s dependencies = [3747602295]" % name, j.get("dependencies"))
    chk(all(isinstance(x, int) for x in j.get("dependencies") or []),
        "%s 依赖是数字（不加引号）" % name, j.get("dependencies"))
    chk("visibility" not in j, "%s 不写 visibility（避免上传覆盖页面可见性）" % name, j.get("visibility"))
    desc = j.get("description") or ""
    chk(j.get("tags") == ["Characters", "schinese"], "%s tags = [Characters, schinese]" % name, j.get("tags"))
    chk("Chinese" not in (j.get("tags") or []) and "English" not in (j.get("tags") or []),
        "%s 没有用不存在的 Chinese/English 标签键" % name, j.get("tags"))
    chk("[h2]前置[/h2]" in desc, "%s 简介有 [h2]前置[/h2]" % name)
    chk("[url=%s]RitsuLib[/url]" % URL_RITSU in desc, "%s 简介有 RitsuLib 工坊链接" % name)
    chk("（必需，最低 0.6.7）" in desc, "%s 简介写明最低 0.6.7" % name)
    chk("（需要RitsuLib）" not in desc, "%s 简介里旧的「（需要RitsuLib）」已移除" % name)
    chk("作者qq：2631262742" in desc, "%s 简介含作者 qq" % name)

print("[5] 工坊简介.txt 与 json 描述一致")
txt = read(os.path.join(WS, "工坊简介.txt"))
chk("[h2]前置[/h2]" in txt, "简介.txt 有前置小节")
chk("[url=%s]RitsuLib[/url]（必需，最低 0.6.7）" % URL_RITSU in txt, "简介.txt 前置行完整")
chk(txt.count("[h2]") == txt.count("[/h2]"), "[h2] 全闭合", (txt.count("[h2]"), txt.count("[/h2]")))
chk(txt.count("[h3]") == txt.count("[/h3]"), "[h3] 全闭合", (txt.count("[h3]"), txt.count("[/h3]")))
chk(txt.count("[url=") == 1, "只有一个 [url= 链接", txt.count("[url="))
chk("（需要RitsuLib）" not in txt, "简介.txt 旧措辞已移除")
wj = json.loads(io.open(os.path.join(WSMOD, "workspace.json"), encoding="utf-8").read())
chk(wj.get("description") == txt, "workspace.json 描述与简介.txt 完全一致")

print("[6] README 不再教错误的 version 键")
for name in ("README.md", "README.en.md"):
    t = read(os.path.join(MODDIR, name))
    chk("min_version" in t, "%s 提到 min_version" % name)
    chk("dependencies[].version" not in t and "dependencies[STS2-RitsuLib].version" not in t,
        "%s 删掉了 dependencies[].version 的错误说明" % name)
    chk("ValidateManifestDependencies" in t, "%s 记录了只校验不改写的行为" % name)

print("[7] 发布包 + 文档")
zp = os.path.join(OUT, "STS2_Momoi_v1.0.8.zip")
chk(os.path.isfile(zp), "发布包 v1.0.8 存在")
if os.path.isfile(zp):
    with zipfile.ZipFile(zp) as zf:
        names = zf.namelist()
        chk(all(n == "STS2_Momoi" or n.startswith("STS2_Momoi/") for n in names), "zip 顶层是 STS2_Momoi/", names[:4])
        m = json.loads(zf.read("STS2_Momoi/STS2_Momoi.json").decode("utf-8-sig"))
        chk((m.get("dependencies") or [{}])[0].get("min_version") == "0.6.7", "zip 内清单 min_version = 0.6.7")
doc = read(DOC)
chk("§21.55" in doc, "迁移文档有 §21.55")
chk("min_version" in doc.split("§21.55")[-1], "§21.55 讲了 min_version")
chk("3747602295" in doc.split("§21.55")[-1], "§21.55 记了工坊依赖 id")
chk("3830602273" in doc, "文档记了工坊条目 id")

print("[8] 文档写明「工坊页面没有 tag 入口 + 用 schinese」")
guide = read(os.path.join(ROOT, "工作区", "_docs", "_发布清单.md"))
stepdoc = read(os.path.join(WS, "上传步骤.md"))
for nm, t in (("发布清单", guide), ("上传步骤.md", stepdoc)):
    chk("schinese" in t, "%s 写了 schinese 标签键" % nm)
    chk("改 tag 的入口" in t and "没有" in t, "%s 写明工坊页面没有 tag 入口" % nm)

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
