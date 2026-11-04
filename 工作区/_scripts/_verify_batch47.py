# -*- coding: utf-8 -*-
"""批次47 自检：飞溅/万花筒/棱彩宝石 三个角色隔离开关 + 工坊发布素材（v1.0.8）。"""
import glob
import io
import json
import os
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MODDIR = os.path.join(ROOT, "STS2 Momoi")
CODE = os.path.join(MODDIR, "STS2 MomoiCode")
WS = os.path.join(ROOT, "工作区", "工坊发布")
WSMOD = os.path.join(WS, "STS2_Momoi")
OUT = os.path.join(ROOT, "工作区", "发布包")
LIMIT = 1024 * 1024

ok = fail = 0


def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))


def read(p):
    return io.open(p, encoding="utf-8-sig").read()


# ---------------------------------------------------------------- 设置项
print("[1] 设置项")
st = read(os.path.join(CODE, "Settings", "MomoiSettings.cs"))
for prop in ("SplashPool", "KaleidoscopePool", "PrismaticGemPool"):
    chk(f"public bool {prop} {{ get; set; }} = true;" in st, f"MomoiModSettings.{prop} 默认 true")
    chk(f"ModSettingsValueBinding<MomoiModSettings, bool> {prop}" in st, f"binding {prop} 已声明")
    chk(f"static s => s.{prop}" in st and f"static (s, v) => s.{prop} = v" in st, f"binding {prop} 读写映射")
for key, label, prop in (
    ("splash_pool", "飞溅出现该角色卡牌", "SplashPool"),
    ("kaleidoscope_pool", "万花筒出现该角色卡牌", "KaleidoscopePool"),
    ("prismatic_gem_pool", "棱彩宝石出现该角色卡牌", "PrismaticGemPool"),
):
    chk(
        re.search(r'AddToggle\(\s*"' + key + r'",\s*ModSettingsText\.Literal\("' + label + r'"\),\s*' + prop + r'\)', st)
        is not None,
        f"设置页开关 {key}「{label}」",
    )
    chk(f"{prop}.Write(defaults.{prop})" in st, f"ResetToDefaults 写 {prop}")
chk(st.count(".Save();") >= st.count("Write(defaults."), "ResetToDefaults 每个写回都 Save")

# ---------------------------------------------------------------- 补丁
print("\n[2] 跨角色池补丁")
pp = os.path.join(CODE, "Patches", "MomoiRandomPoolPatches.cs")
chk(os.path.isfile(pp), "Patches/MomoiRandomPoolPatches.cs 存在")
src = read(pp) if os.path.isfile(pp) else ""
chk("public static class MomoiPoolIsolation" in src, "MomoiPoolIsolation 工具类")
chk("namespace STS2_Momoi.Patches;" in src, "命名空间 STS2_Momoi.Patches")
chk("[ThreadStatic]" in src and "_splashDepth" in src and "_kaleidoscopeDepth" in src and "_prismaticGemDepth" in src,
    "三个作用域计数（ThreadStatic）")
chk("public static bool HideOurPoolNow" in src, "HideOurPoolNow")
for prop in ("SplashPool", "KaleidoscopePool", "PrismaticGemPool"):
    chk(f"MomoiSettingsStore.{prop}.Read()" in src, f"HideOurPoolNow 读 {prop}")
chk("pool is STS2_MomoiCardPool" in src, "IsOurPool 判定 STS2_MomoiCardPool")
chk("public static void EnterSplash() => _splashDepth++;" in src, "EnterSplash ++")
chk("_splashDepth = Math.Max(0, _splashDepth - 1)" in src, "ExitSplash 防负")

# 角色池集合收口
chk('new(typeof(UnlockState), "get_CharacterCardPools")' in src, "目标 UnlockState.get_CharacterCardPools")
chk("Postfix(ref IEnumerable<CardPoolModel> __result)" in src, "getter Postfix 签名")
chk("__result = __result.Where(pool => !MomoiPoolIsolation.IsOurPool(pool));" in src, "作用域内摘掉本模组池")
# 三个入口
chk('new(typeof(Splash), "OnPlay", new[] { typeof(PlayerChoiceContext), typeof(CardPlay) })' in src,
    "飞溅目标 Splash.OnPlay(PlayerChoiceContext, CardPlay)")
chk("typeof(Kaleidoscope), \"AfterObtained\"" in src, "万花筒目标 Kaleidoscope.AfterObtained")
chk("typeof(PrismaticGem), nameof(PrismaticGem.ModifyCardRewardCreationOptions)" in src,
    "棱彩宝石目标 PrismaticGem.ModifyCardRewardCreationOptions")
for cls, enter, exit_ in (
    ("MomoiSplashPoolPatch", "EnterSplash", "ExitSplash"),
    ("MomoiKaleidoscopePoolPatch", "EnterKaleidoscope", "ExitKaleidoscope"),
    ("MomoiPrismaticGemPoolPatch", "EnterPrismaticGem", "ExitPrismaticGem"),
):
    chk(f"class {cls} : IPatchMethod" in src, f"{cls} 是 IPatchMethod")
    chk(f"public static void Prefix() => MomoiPoolIsolation.{enter}();" in src, f"{cls}.Prefix -> {enter}")
    chk(f"public static void Postfix() => MomoiPoolIsolation.{exit_}();" in src, f"{cls}.Postfix -> {exit_}")
# 不能把 CanBeGeneratedInCombat 一起挡掉
hit = [p for p, s in ((p, read(p)) for p in glob.glob(os.path.join(CODE, "**", "*.cs"), recursive=True))
       if any("CanBeGeneratedInCombat" in ln and not ln.strip().startswith(("//", "///", "*", "/*"))
              for ln in s.splitlines())]
chk(not hit, "没有用 CanBeGeneratedInCombat 实现（否则会挡掉自己角色的战斗内生成）", hit)

# Entry 注册
entry = read(os.path.join(CODE, "Entry.cs"))
for patch in ("MomoiCharacterCardPoolsPatch", "MomoiSplashPoolPatch", "MomoiKaleidoscopePoolPatch",
              "MomoiPrismaticGemPoolPatch"):
    chk(f"patcher.RegisterPatch<Patches.{patch}>();" in entry, f"Entry 注册 {patch}")
chk(entry.index("MomoiSeaGlassPoolPatch") < entry.index("MomoiCharacterCardPoolsPatch"), "注册顺序在 SeaGlass 之后")

# ---------------------------------------------------------------- 版本 / 发布包
print("\n[3] 版本与发布包")
manifest = json.load(io.open(os.path.join(MODDIR, "STS2_Momoi.json"), encoding="utf-8-sig"))
csproj = read(os.path.join(MODDIR, "STS2 Momoi.csproj"))
chk(manifest["version"] == "1.0.8", "仓库清单 1.0.8", manifest["version"])
chk("<Version>1.0.8</Version>" in csproj, "csproj 1.0.8")
chk("135 张卡牌" in manifest["description"], "清单简介写入 135 张卡牌")
chk(manifest["dependencies"][0]["id"] == "STS2-RitsuLib", "清单依赖 STS2-RitsuLib")
zp = os.path.join(OUT, "STS2_Momoi_v1.0.8.zip")
chk(os.path.isfile(zp), "zip 1.0.8 已生成")
if os.path.isfile(zp):
    with zipfile.ZipFile(zp) as z:
        names = z.namelist()
        chk({n.split("/")[0] for n in names} == {"STS2_Momoi"}, "顶层 STS2_Momoi/")
        inner = json.loads(z.read("STS2_Momoi/STS2_Momoi.json").decode("utf-8-sig"))
        chk(inner["version"] == "1.0.8", "包内清单 1.0.8")
        chk("STS2_Momoi/README.txt" in names, "包内含 README.txt")
chk(not os.path.isfile(os.path.join(OUT, "STS2_Momoi_v1.0.3.zip")), "旧 v1.0.3 包已删")

# ---------------------------------------------------------------- 工坊素材
print("\n[4] 工坊发布素材")
desc_path = os.path.join(WS, "工坊简介.txt")
chk(os.path.isfile(desc_path), "工坊简介.txt 存在")
desc = read(desc_path) if os.path.isfile(desc_path) else ""
chk("作者qq：2631262742" in desc, "简介含作者 qq")
chk(desc.rstrip().endswith("作者qq：2631262742"), "简介到「作者qq」结束（批次51 起更新说明改放 changeNotes）")
chk("mod交流群：263898222" in desc, "简介含交流群号")
chk("[b]135[/b]" in desc, "简介写 135 张卡牌")
chk("[h2]前置[/h2]" in desc and "（必需，最低 0.6.7）" in desc, "简介用前置小节注明需要 RitsuLib（批次48 取代旧的「（需要RitsuLib）」）")
for bad in ("[*]", "[table]", "[color", "[size", "[align", "[font"):
    chk(bad not in desc, f"没有使用 Steam 不支持的 {bad}")
for tag in ("b", "h2", "h3"):
    chk(desc.count(f"[{tag}]") == desc.count(f"[/{tag}]"), f"[{tag}] 开闭配对", (desc.count(f"[{tag}]"), desc.count(f"[/{tag}]")))
chk(desc.count("[h3]") == 7, "七个机制小标题", desc.count("[h3]"))

img = os.path.join(WSMOD, "image.png")
chk(os.path.isfile(img), "工作区内 image.png 存在（上传器只认 png）")
chk(os.path.getsize(img) < LIMIT, "image.png < 1MB", os.path.getsize(img) if os.path.isfile(img) else 0)
mid = os.path.join(WSMOD, "mod_id.txt")
chk(os.path.isfile(mid), "mod_id.txt 已生成（首次上传后）")
if os.path.isfile(mid):
    chk(io.open(mid, encoding="utf-8-sig").read().strip() == "3830602273", "mod_id = 3830602273", io.open(mid, encoding="utf-8-sig").read().strip())
shots = sorted(glob.glob(os.path.join(WS, "截图", "*.jpg")))
chk(len(shots) == 16, "16 张截图", len(shots))
chk(all(os.path.getsize(p) < LIMIT for p in shots), "截图全部 < 1MB",
    [os.path.basename(p) for p in shots if os.path.getsize(p) >= LIMIT])
chk(all(os.path.basename(p)[:2].isdigit() for p in shots), "截图按 01..16 命名")

for name in ("workspace.json", "workshop.json"):
    p = os.path.join(WSMOD, name)
    chk(os.path.isfile(p), f"{name} 存在")
    if os.path.isfile(p):
        d = json.load(io.open(p, encoding="utf-8-sig"))
        chk(d.get("description") == desc, f"{name} 简介与 txt 一致")
        chk("title" not in d, f"{name} 不写 title（否则每次上传会覆盖页面标题）", d.get("title"))
        chk("visibility" not in d, f"{name} 不写 visibility（交给工坊页面维护）", d.get("visibility"))
content = os.path.join(WSMOD, "Content", "STS2_Momoi")
chk(os.path.isdir(content), "Content/STS2_Momoi 存在")
got = sorted(os.listdir(content)) if os.path.isdir(content) else []
chk(got == ["STS2_Momoi.dll", "STS2_Momoi.json", "STS2_Momoi.pck"], "Content 三件套", got)
if "STS2_Momoi.json" in got:
    cm = json.load(io.open(os.path.join(content, "STS2_Momoi.json"), encoding="utf-8-sig"))
    chk(cm["version"] == "1.0.8", "Content 内清单 1.0.8", cm["version"])
chk(os.path.isfile(os.path.join(WS, "上传.bat")), "上传.bat 存在")
bat = read(os.path.join(WS, "上传.bat")) if os.path.isfile(os.path.join(WS, "上传.bat")) else ""
chk("ModUploader.exe upload -w STS2_Momoi" in bat, "bat 使用 upload -w STS2_Momoi")
chk(os.path.isfile(os.path.join(WS, "上传步骤.md")), "上传步骤.md 存在")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
