# -*- coding: utf-8 -*-
"""批次46 自检：黄金矿工当前耗能、费用/数值、仅局内括号、构想之矛/矛与盾文本、开荒侧栏、相遇关键词、卡牌统计。"""
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
LOC = os.path.join(MODDIR, "STS2_Momoi", "localization")
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


ALL = {p: open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(CODE, "**", "*.cs"), recursive=True)}


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


def load(lang, table):
    return json.load(open(os.path.join(LOC, lang, table + ".json"), encoding="utf-8"))


Z, E = load("zhs", "cards"), load("eng", "cards")
PZ = load("zhs", "powers")

print("== 1. 黄金矿工：0/0 费 + 读当前耗能 ==")
gm = body("GoldMiner")
chk("public GoldMiner() : base(0, CardType.Skill" in gm, "基础 0 费")
chk("EnergyCost.UpgradeBy" not in gm, "升级不减费（0/0）")
chk("LocalKeywords.Add(CardKeyword.Retain)" in gm, "升级仍给保留")
chk("GetWithModifiers(CostModifiers.All)" in gm, "按当前耗能分支（不是 Canonical）")
chk("EnergyCost.Canonical" not in gm, "不再用卡面 Canonical")

print("== 2. 费用 ==")
for cls, cost in (("ShowMyStrength", 0), ("LearnByDoing", 3), ("Inspiration", 1)):
    chk("public %s() : base(%d, " % (cls, cost) in body(cls), "%s %d 费" % (cls, cost))
chk("EnergyCost.UpgradeBy(-1)" not in body("ShowMyStrength"), "见识实力 0/0")
chk("EnergyCost.UpgradeBy(-1)" not in body("LearnByDoing"), "日复一日 3/3")
chk("EnergyCost.UpgradeBy(-1)" in body("Inspiration"), "灵感爆发 升级 1 -> 0")

print("== 3. 数值 ==")
chk("new CalculationBaseVar(4m)" in body("BottleneckBreak"), "瓶颈突破 4/4")
cb = body("CourageBoon")
chk("new CalculationBaseVar(6m)" in cb and "UpgradeValueBy(3)" in cb, "勇者加护 6/9")
chk("? 15 : 11" in body("ConceptSpearPower"), "构想之矛 power 11/15")
chk("? 15 : 11" in body("SpearShieldPower"), "矛与盾 power 伤害 11/15")

print("== 4. 仅局内显示的括号 ==")
for key, needle in (
    ("STS2_MOMOI_CARD_FIREPOWER_STRIKE", "已获得过{FirepowerGained:diff()}层"),
    ("STS2_MOMOI_CARD_SCRIPT_STRIKE", "（抽{ConceptCards:diff()}张牌）"),
    ("STS2_MOMOI_CARD_BULLET_RAIN", "（额外攻击{ExtraHits:diff()}次）"),
    ("STS2_MOMOI_CARD_EXPERIENCE_COMBO", "（攻击{CalculatedHits:diff()}次）"),
):
    z = Z[key + ".description"]
    chk("{InCombat:" in z and needle in z.split("{InCombat:")[1], "%s 括号在 InCombat 里" % key.split("_")[-1], z)
    chk(z.rstrip().endswith("|}") or "|}" in z, "%s 局外分支为空（图鉴不显示）" % key.split("_")[-1])

print("== 5. 文本 ==")
chk("未生成过" in Z["STS2_MOMOI_CARD_GRINDING.description"], "开荒卡面 获得→生成")
sb = Z["STS2_MOMOI_CARD_GRINDING.sidebar"]
chk(sb.startswith("将依次生成以下[red]诅咒[/red]：") and "[red]苦恼[/red]" in sb, "开荒侧栏新描述（诅咒仍红）", sb)
enc = Z["STS2_MOMOI_CARD_ENCOUNTER.description"]
chk("[gold]铸造[/gold]" in enc and "[gold]生成[/gold]" in enc, "相遇：铸造/生成 染金", enc)
chk("[gold]Forge[/gold]" in E["STS2_MOMOI_CARD_ENCOUNTER.description"]
    and "[gold]Channel[/gold]" in E["STS2_MOMOI_CARD_ENCOUNTER.description"], "相遇 eng：Forge/Channel 染金")
ss = Z["STS2_MOMOI_CARD_SPEAR_SHIELD.description"]
chk("{IfUpgraded:show:15|11}" in ss, "矛与盾卡面伤害 11/15", ss)
chk("{IfUpgraded:show:8|6}" in ss, "矛与盾卡面格挡仍是 8/6")

print("== 6. 卡牌统计 ==")
files = {p: t for p, t in ALL.items() if os.sep + "Cards" + os.sep in p}
char_pool, token_pool = [], []
for p, src in files.items():
    for m in re.finditer(r"\[RegisterCard\(typeof\(([^)]*)\)\)\]\s*(?:\[[^\]]*\]\s*)*public sealed class (\w+)", src):
        pool, cls = m.group(1), m.group(2)
        mm = re.search(r"\bclass\s+" + cls + r"\b", src)
        brace = src.find("{", mm.end())
        depth = 0
        for j in range(brace, len(src)):
            if src[j] == "{":
                depth += 1
            elif src[j] == "}":
                depth -= 1
                if depth == 0:
                    break
        seg = src[mm.start():j + 1]
        tag = "minigame" if "MinigameSupport.Tag" in seg else ("fullgame" if "MinigameSupport.FullGameTag" in seg else "")
        (token_pool if "TokenCardPool" in pool else char_pool).append((cls, tag))
print("     角色卡池 %d / 衍生牌 %d / 合计 %d" % (len(char_pool), len(token_pool), len(char_pool) + len(token_pool)))
chk(len(char_pool) == 91, "角色卡池 91 张", len(char_pool))
chk(len(token_pool) == 44, "衍生牌 44 张", len(token_pool))
mini = [c for c, t in char_pool + token_pool if t == "minigame"]
game = [c for c, t in char_pool + token_pool if t == "fullgame"]
chk(len(mini) == 14, "小游戏牌 14 张", len(mini))
chk(len(game) == 6, "游戏牌 6 张", len(game))
chk(len(char_pool) + len(token_pool) == 135, "合计 135 张", len(char_pool) + len(token_pool))

print("== 7. 版本与发布包 ==")
manifest = json.load(open(os.path.join(MODDIR, "STS2_Momoi.json"), encoding="utf-8"))
chk(manifest["version"] == "1.0.8", "仓库清单 1.0.8", manifest["version"])
chk("<Version>1.0.8</Version>" in open(os.path.join(MODDIR, "STS2 Momoi.csproj"), encoding="utf-8").read(), "csproj 1.0.8")
zp = os.path.join(OUT, "STS2_Momoi_v1.0.8.zip")
chk(os.path.isfile(zp), "zip 1.0.8 已生成")
if os.path.isfile(zp):
    with zipfile.ZipFile(zp) as z:
        names = z.namelist()
        chk({n.split("/")[0] for n in names} == {"STS2_Momoi"}, "顶层 STS2_Momoi/")
        inner = json.loads(z.read("STS2_Momoi/STS2_Momoi.json").decode("utf-8-sig"))
        chk(inner["version"] == "1.0.8", "包内 1.0.8")
chk(not os.path.isfile(os.path.join(OUT, "STS2_Momoi_v1.0.2.zip")), "旧 v1.0.2 包已删")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
