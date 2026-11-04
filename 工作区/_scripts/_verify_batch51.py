# -*- coding: utf-8 -*-
"""批次51 自检：工坊简介追加「1.0.1更新」清单（[list]+[*]）+ 1.0.8 重新上传（id 不变）。"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MODDIR = os.path.join(ROOT, "STS2 Momoi")
OUT = os.path.join(ROOT, "工作区", "发布包")
WS = os.path.join(ROOT, "工作区", "工坊发布")
WSMOD = os.path.join(WS, "STS2_Momoi")
CONTENT = os.path.join(WSMOD, "Content", "STS2_Momoi")
DOC = os.path.join(ROOT, "STS2_Momoi_迁移文档.md")
RELEASE_DOC = os.path.join(ROOT, "工作区", "_docs", "_发布清单.md")
UPLOAD_DOC = os.path.join(WS, "上传步骤.md")
VER = "1.0.8"
ITEM_ID = "3830602273"
URL_RITSU = "https://steamcommunity.com/sharedfiles/filedetails/?id=3747602295"

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


print("[1] 简介（描述）：不含更新清单，以作者 qq 结尾")
txt = read(os.path.join(WS, "工坊简介.txt"))
ws = json.load(io.open(os.path.join(WSMOD, "workspace.json"), encoding="utf-8"))
wp = json.load(io.open(os.path.join(WSMOD, "workshop.json"), encoding="utf-8"))
chk(ws["description"] == txt, "workspace.json 描述 == 工坊简介.txt")
chk(wp["description"] == txt, "workshop.json 描述 == 工坊简介.txt")
chk("1.0.1更新" not in txt, "描述里不再放更新清单（批次51 修正：改放 changeNotes）")
chk(txt.rstrip().endswith("作者qq：2631262742"), "描述到「作者qq」结束", txt[-30:])
chk(txt.count("[h2]") == txt.count("[/h2]"), "[h2] 闭合数量一致", (txt.count("[h2]"), txt.count("[/h2]")))
chk(txt.count("[h3]") == txt.count("[/h3]"), "[h3] 闭合数量一致", (txt.count("[h3]"), txt.count("[/h3]")))
chk(txt.count("[b]") == txt.count("[/b]"), "[b] 闭合数量一致", (txt.count("[b]"), txt.count("[/b]")))
chk(txt.count("[*]") == 0, "描述里没有裸露的 [*]", txt.count("[*]"))
chk(txt.count("[url=") == 1, "只有 1 个 [url=]", txt.count("[url="))
chk("[h2]前置[/h2]" in txt and "[url=%s]RitsuLib[/url]" % URL_RITSU in txt, "前置小节与 RitsuLib 链接仍在")
chk("（必需，最低 0.6.7）" in txt, "前置写明最低 0.6.7")
chk("[b]135[/b]" in txt and "mod交流群：263898222" in txt and "作者qq：2631262742" in txt, "卡牌数与联系方式仍在")

print("[1b] 更新说明：草稿留本地文件，json 不写 changeNote（避免上传覆盖页面）")
notes = read(os.path.join(WS, "更新说明.txt"))
chk("changeNotes" not in ws and "changeNote" not in ws, "workspace.json 不写 changeNote")
chk("changeNotes" not in wp and "changeNote" not in wp, "workshop.json 同上")
chk(os.path.isfile(os.path.join(WS, "更新公告_标准格式.txt")), "有可直接粘贴的 更新公告_标准格式.txt")
std = read(os.path.join(WS, "更新公告_标准格式.txt"))
chk(std.count("[*]") >= 8, "标准格式公告里有 >=8 条 [*]", std.count("[*]"))
_lo = std.find("[list]")
_hi = std.find("[/list]")
chk(_lo != -1 and _hi > _lo, "标准格式公告有 [list]/[/list] 配对")
chk(all(_lo < i < _hi for i in range(len(std)) if std.startswith("[*]", i)), "所有 [*] 都在 [list] 内（Steam 要求）")
chk(std.rstrip().endswith("[/h3]"), "以 [h3] 小标题结尾", std[-24:])
chk("132MB→54MB" in std, "第一条是体积优化")
chk("循环叙事" in notes and "来自明日奈的援护" in notes, "更新说明涵盖本轮主要改动")
chk("visibility" not in ws, "workspace 不写 visibility（批次52：避免上传把页面可见性改回私密）")
chk(ws["tags"] == ["Characters", "schinese"], "tags 未被动过", ws["tags"])
chk(ws["dependencies"] == [3747602295], "dependencies 仍是 [3747602295]", ws["dependencies"])

print("[2] 工坊 Content：1.0.8 三件套")
cman = json.load(io.open(os.path.join(CONTENT, "STS2_Momoi.json"), encoding="utf-8"))
chk(cman["version"] == VER, "Content 清单版本 %s" % VER, cman["version"])
for f in ("STS2_Momoi.dll", "STS2_Momoi.pck", "STS2_Momoi.json"):
    chk(os.path.isfile(os.path.join(CONTENT, f)), "Content 有 " + f)
pck = os.path.getsize(os.path.join(CONTENT, "STS2_Momoi.pck"))
chk(40_000_000 <= pck <= 80_000_000, "Content PCK 在优化后的体积区间", pck)

print("[3] 上传记录")
chk(read(os.path.join(WSMOD, "mod_id.txt")).strip() == ITEM_ID, "mod_id.txt 是 %s（上传器据此复用同一条目）" % ITEM_ID)
log = io.open(os.path.join(WS, "mod-uploader.log"), encoding="utf-8", errors="replace").read()
chk("Successfully uploaded" in log, "上传日志有 Successfully uploaded")
chk(ITEM_ID in log, "上传日志里有条目 id %s" % ITEM_ID)
chk("No modifications were made to dependencies" in log or "dependencies" in log, "上传日志处理过 dependencies")
img = os.path.join(WSMOD, "image.png")
chk(os.path.isfile(img), "预览图 image.png 存在（这版 uploader 只认 png）")
chk(os.path.getsize(img) < 1024 * 1024, "预览图 < 1MB", os.path.getsize(img))

print("[4] 版本与发布包")
csproj = read(os.path.join(MODDIR, "STS2 Momoi.csproj"))
chk("<Version>%s</Version>" % VER in csproj, "csproj 版本 %s" % VER)
man = json.load(io.open(os.path.join(MODDIR, "STS2_Momoi.json"), encoding="utf-8"))
chk(man["version"] == VER, "清单版本 %s" % VER, man["version"])
chk(man["dependencies"] == [{"id": "STS2-RitsuLib", "min_version": "0.6.7"}], "清单依赖 min_version 0.6.7", man["dependencies"])
z = os.path.join(OUT, "STS2_Momoi_v%s.zip" % VER)
chk(os.path.isfile(z), "发布包 v%s.zip 存在" % VER)
chk(not os.path.isfile(os.path.join(OUT, "STS2_Momoi_v1.0.6.zip")), "旧 v1.0.6.zip 已删")

print("[5] 文档")
doc = read(DOC)
chk("### 21.58" in doc, "迁移文档有 §21.58")
tail = doc.split("### 21.58")[-1]
chk("changeNotes" in tail, "§21.58 记了更新说明改放 changeNotes")
chk("[list]" in tail, "§21.58 记了 [list]/[*] 的写法约束")
chk(ITEM_ID in tail, "§21.58 记了条目 id")
chk("批次51" in doc.split("### 21.58")[0], "顶部状态块提到批次51")
rd = read(RELEASE_DOC)
chk(VER in rd and ITEM_ID in rd, "发布清单写了 %s 与 %s" % (VER, ITEM_ID))
up = read(UPLOAD_DOC)
chk("mod_id.txt" in up, "上传步骤讲了 mod_id.txt 复用条目")
chk("image.png" in up, "上传步骤写明预览图是 image.png")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
