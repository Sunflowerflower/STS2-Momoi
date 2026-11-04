# -*- coding: utf-8 -*-
"""批次44 自检：22 项平衡调整 + 注能置底/直接结算 + 图鉴全解锁 + 1.0.1 发布包。"""
import glob
import json
import os
import re
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


ALL = {}
for p in glob.glob(os.path.join(CODE, "**", "*.cs"), recursive=True):
    ALL[p] = open(p, encoding="utf-8").read()


def body(cls):
    for src in ALL.values():
        m = re.search(r"\bclass\s+" + cls + r"\b", src)
        if not m:
            continue
        brace = src.find("{", m.end())
        depth = 0
        for j in range(brace, len(src)):
            if src[j] == "{":
                depth += 1
            elif src[j] == "}":
                depth -= 1
                if depth == 0:
                    return src[m.start():j + 1]
    return ""


def allcode():
    return "\n".join(ALL.values())


print("== 1. 费用 ==")
for cls, cost in (("Overload", 2), ("AsceticTraining", 2), ("PortalParadox", 1), ("RhythmGame", 1)):
    chk("public %s() : base(%d, " % (cls, cost) in body(cls), "%s %d 费" % (cls, cost))
chk("EnergyCost.UpgradeBy" not in body("PlantsVsZombies"), "植物大战僵尸 1/1（升级不减费）")
chk("public PlantsVsZombies() : base(1, " in body("PlantsVsZombies"), "植物大战僵尸 1 费")

print("== 2. 数值 ==")
checks = [
    ("Overload", 'new DynamicVar("Vigor", 2)', "过载 活力 2/3"),
    ("BaBoot", 'new DynamicVar("Vigor", 3)', "BA启动 活力 3/4（批次49）"),
    ("GearUp", "new BlockVar(4m, ValueProp.Move)", "整装待发 格挡 4/6"),
    ("BulletRain", "new CalculationBaseVar(4m)", "天马行空 4/4"),
    ("ExperienceCombo", "new CalculationBaseVar(5m)", "博览群游 5/7"),
    ("ConfusedShot", "new CalculationBaseVar(2m)", "激战 2/2"),
    ("RollAndShoot", "new BlockVar(6m, ValueProp.Move)", "翻滚射击 6/8"),
    ("Countermeasure", 'new DynamicVar("Vigor", 4)', "对策 活力 4/5"),
    ("ImBack", 'new DynamicVar("Vigor", 2)', "我复活啦 活力 2/3"),
    ("FishingMaster", "new CalculationBaseVar(8m)", "捕鱼达人 8/8"),
    ("TravelFrog", "new BlockVar(6m, ValueProp.Move)", "旅行异蛙 6/6"),
    ("Encounter", "new BlockVar(6m, ValueProp.Move)", "相遇 6/7"),
    ("MomoiSupportToki", 'new DynamicVar("Firepower", 2)', "时 火力 2/3"),
    ("LoseCard", 'new DynamicVar("Vigor", 2)', "LOSE！活力 2/3"),
    ("RhythmGame", 'new DynamicVar("Damage", 18)', "节奏游戏 18/20"),
    ("ItCrackedMe", "new HpLossVar(2m)", "绷到我了 失去 2 血"),
    ("ItCrackedMe", "new BlockVar(6, ValueProp.Move)", "绷到我了 格挡 6/8"),
    ("FiftyThousandYears", "new BlockVar(4, ValueProp.Move)", "五万年 格挡 4/6"),
]
for cls, needle, label in checks:
    chk(needle in body(cls), label)
chk("? 20 : 18" in body("RhythmGamePower") and "? 5 : 6" in body("RhythmGamePower"), "节奏游戏 power 叠加 20/5")
chk("(upgraded ? 15 : 11)" in body("SpearShieldPower"), "矛与盾 伤害 11/15（批次40 已是）")
chk("CalculationBase.UpgradeValueBy" not in body("BulletRain"), "天马行空 升级不再加伤害")
chk("Block\"].UpgradeValueBy" not in body("TravelFrog"), "旅行异蛙 升级不再加格挡")
chk("Innate" not in body("ConceptShield"), "构想之盾 升级不再给固有")
chk('DynamicVars["Damage"].UpgradeValueBy(2)' in body("RhythmGame"), "节奏游戏 升级 +2")
chk('DynamicVars["PerBlock"].UpgradeValueBy(-1)' in body("RhythmGame"), "节奏游戏 每方块 -1")

print("== 3. 注能（开发者协同：绿）==")
dg = body("DevGreen")
chk("_imbuedApplied" in dg, "每张牌只自动打出一次")
chk("ImbuedSupport.TryAutoPlayAsync(choiceContext, this" in dg, "注能走共用 ImbuedSupport 自动打出（批次49）")
chk("RemoveFromCombat(this, skipVisuals: true)" not in dg, "不再手动 RemoveFromCombat（改为正常打出）")
chk("PowerCmd.Apply<DexterityPower>" in dg and "PowerCmd.Apply<DevGreenPower>" in dg, "OnPlay 仍挂敏捷/活力")
patch = open(os.path.join(CODE, "Patches", "MomoiImbuedAndCompendiumPatches.cs"), encoding="utf-8").read()
chk("SetupPlayerTurn" in patch and "MoveToBottomInternal" in patch, "第 1 回合抽牌前置底（等价原版注能）")
chk("TurnNumber: 1" in patch, "只在第 1 回合")

print("== 4. 图鉴全解锁 ==")
chk("MarkCardAsSeen" in patch and "MarkRelicAsSeen" in patch and "MarkPotionAsSeen" in patch, "卡/遗物/药水都标记")
chk("SaveProgressFile()" in patch, "标记后落盘")
chk("InitProgressData" in patch, "挂在档案进度加载之后")
chk("SaveManager.Instance.MarkCardAsSeen" not in patch, "没用要求 LocalContext 的那个重载")
chk("ModIdPrefix" in patch and "StartsWith(ModIdPrefix" in patch, "按 id 前缀覆盖衍生/Token 牌（批次46 修问号）")
chk("c.Pool is STS2_MomoiCardPool" not in patch, "不再只按角色卡池过滤")
settings = open(os.path.join(CODE, "Settings", "MomoiSettings.cs"), encoding="utf-8").read()
chk("unlock_compendium" in settings and "MomoiCompendiumUnlock.MarkAll" in settings, "设置里也有一键解锁图鉴按钮")
chk("MomoiImbuedDrawPilePatch" in open(os.path.join(CODE, "Entry.cs"), encoding="utf-8").read(), "置底补丁已登记")
chk("MomoiCompendiumUnlockPatch" in open(os.path.join(CODE, "Entry.cs"), encoding="utf-8").read(), "图鉴补丁已登记")

print("== 5. 版本与发布包 ==")
manifest = json.load(open(os.path.join(MODDIR, "STS2_Momoi.json"), encoding="utf-8"))
deployed = json.load(open(os.path.join(MODS, "STS2_Momoi.json"), encoding="utf-8-sig"))
csproj = open(os.path.join(MODDIR, "STS2 Momoi.csproj"), encoding="utf-8").read()
chk(manifest["version"] == "1.0.8", "仓库清单 1.0.8", manifest["version"])
chk(deployed["version"] == "1.0.8", "部署清单 1.0.8", deployed["version"])
chk("<Version>1.0.8</Version>" in csproj, "csproj 1.0.8")
zip_path = os.path.join(OUT, "STS2_Momoi_v1.0.8.zip")
chk(os.path.isfile(zip_path), "zip 已生成 v1.0.8")
if os.path.isfile(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        tops = {n.split("/")[0] for n in names}
        chk(tops == {"STS2_Momoi"}, "zip 顶层只有 STS2_Momoi/", tops)
        for f in ("STS2_Momoi.json", "STS2_Momoi.dll", "STS2_Momoi.pck", "README.txt"):
            chk("STS2_Momoi/" + f in names, "包内 " + f)
        inner = json.loads(z.read("STS2_Momoi/STS2_Momoi.json").decode("utf-8-sig"))
        chk(inner["version"] == "1.0.8", "包内清单 1.0.8")
chk(not os.path.exists(os.path.join(OUT, "STS2_Momoi_v1.0.1.zip")), "没有残留的 v1.0.1 zip（批次46）")
chk(not os.path.exists(os.path.join(OUT, "STS2_Momoi_v1.0.0")), "没有残留的 v1.0.0 目录")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
