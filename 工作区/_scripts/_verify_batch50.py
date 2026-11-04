# -*- coding: utf-8 -*-
"""批次50 自检：绝地求生括号仅局内 / 明日奈减伤文本带层数 / 循环叙事时机与一次性。"""
import io
import json
import os
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MODDIR = os.path.join(ROOT, "STS2 Momoi")
CODE = os.path.join(MODDIR, "STS2 MomoiCode")
RES = os.path.join(MODDIR, "STS2_Momoi")
LOC = os.path.join(RES, "localization")
OUT = os.path.join(ROOT, "工作区", "发布包")
WSMOD = os.path.join(ROOT, "工作区", "工坊发布", "STS2_Momoi", "Content", "STS2_Momoi")
DEPLOY = r"D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi"
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
        print("  FAIL " + label + ("  -> %r" % (detail,)))


def read(p):
    return io.open(p, encoding="utf-8-sig").read()


def loc(lang, name):
    return json.loads(read(os.path.join(LOC, lang, name)))


def block(text, name):
    """按花括号深度取 class name 的定义体。"""
    idx = text.index("class " + name)
    start = text.index("{", idx)
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise AssertionError("unbalanced: " + name)


print("[1] 绝地求生：括号内容只在战斗中显示")
for lang in ("zhs", "eng"):
    cards = loc(lang, "cards.json")
    for key in ("STS2_MOMOI_CARD_BATTLE_ROYALE.description", "STS2_MOMOI_CARD_BATTLE_ROYALE.smartDescription"):
        v = cards[key]
        chk("{InCombat:" in v and v.rstrip().endswith("|}"), "%s 的 %s 用 {InCombat:…|} 包裹" % (lang, key.split(".")[-1]), v)
        # 括号本体必须落在 InCombat 分支里（即 {InCombat: 之后、|} 之前）
        seg = v[v.index("{InCombat:"):]
        chk("CalculatedCards" in seg and "CalculatedEnergy" in seg, "%s 括号内容在局内分支" % lang, seg)

print("[2] 明日奈减伤：power 文本显示剩余回合数")
for lang, key_mark in (("zhs", "直到你的下[blue]{Amount}[/blue]个回合开始前"),
                       ("eng", "Until the start of your next [blue]{Amount}[/blue] turn(s)")):
    powers = loc(lang, "powers.json")
    for key in ("STS2_MOMOI_POWER_ASUNA_GUARD_POWER.description", "STS2_MOMOI_POWER_ASUNA_GUARD_POWER.smartDescription"):
        chk(key_mark in powers[key] and "{ReductionPct}%" in powers[key],
            "%s 的 %s 带 {Amount} 层数" % (lang, key.split(".")[-1]))
    cards = loc(lang, "cards.json")
    chk("{Amount}" not in cards["STS2_MOMOI_CARD_MOMOI_SUPPORT_ASUNA.description"],
        "%s 的卡面不使用 {Amount}（卡面数字是固定的）" % lang)

print("[3] 循环叙事：弃牌前结算 + 触发后移除 + 不做归位动画")
nb = read(os.path.join(CODE, "Cards", "NewCardsBatch.cs"))
cyc = block(nb, "CyclicNarrativePower")
chk("BeforeSideTurnEnd" in cyc, "挂在 BeforeSideTurnEnd（弃手牌之前，同原版炸弹/惊逃）")
chk("AfterSideTurnEnd" not in cyc, "不再挂在 AfterSideTurnEnd（弃手牌之后）")
chk("await PowerCmd.Remove(this);" in cyc, "结算后直接移除（一次性）")
chk("TickDownDuration" not in cyc, "不再按回合数递减")
chk("skipVisuals: true" in cyc, "洗入抽牌堆时跳过节点归位动画")
chk("[Cyclic]" in cyc, "有 [Cyclic] 日志兜底")
chk("catch (Exception" in cyc, "有 try/catch 兜底")
chk("0, max)" in " ".join(cyc.split()), "仍是 MinSelect=0 / MaxSelect=max")
chk("Cancelable = true" in cyc, "仍可跳过不选")
card = block(nb, "CyclicNarrative")
chk("PowerCmd.Apply<CyclicNarrativePower>" in card, "卡牌打出时施加能力")
chk("class CyclicNarrative : ModCardTemplate, IImbuedCard" in nb, "卡牌仍是注能牌")

print("[4] 版本与产物")
csproj = read(os.path.join(MODDIR, "STS2 Momoi.csproj"))
manifest = json.loads(read(os.path.join(MODDIR, "STS2_Momoi.json")))
chk("<Version>%s</Version>" % VER in csproj, "csproj 版本 %s" % VER)
chk(manifest["version"] == VER, "清单版本 %s" % VER, manifest["version"])
chk(manifest["dependencies"][0]["min_version"] == "0.6.7", "依赖 min_version 仍是 0.6.7")

pck = os.path.join(DEPLOY, "STS2_Momoi.pck")
zip_path = os.path.join(OUT, "STS2_Momoi_v%s.zip" % VER)
chk(os.path.isfile(zip_path), "发布包 v%s.zip 存在" % VER)
chk(not os.path.isfile(os.path.join(OUT, "STS2_Momoi_v1.0.5.zip")), "旧 v1.0.5.zip 已删除")
if os.path.isfile(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        chk(any(n == "STS2_Momoi/STS2_Momoi.pck" for n in names), "zip 顶层 STS2_Momoi/")
        chk(zf.getinfo("STS2_Momoi/STS2_Momoi.pck").file_size == os.path.getsize(pck),
            "zip 内 pck 与部署一致")
for f in ("STS2_Momoi.dll", "STS2_Momoi.json", "STS2_Momoi.pck"):
    a = os.path.getsize(os.path.join(DEPLOY, f))
    b = os.path.getsize(os.path.join(WSMOD, f))
    chk(a == b, "工坊 Content 的 %s 与部署一致" % f, (a, b))

print("[5] 文档")
doc = read(DOC)
_i = doc.find("### 21.57")
_j = doc.find("### 21.58")
sec57 = doc[_i:_j] if _i >= 0 and _j > _i else ""
chk(_i >= 0, "迁移文档有 §21.57")
chk("BeforeSideTurnEnd" in sec57, "§21.57 讲了结算时机")
chk("{InCombat:" in sec57, "§21.57 讲了绝地求生的局内括号")
chk("满溢灵感" in sec57, "§21.57 记了满溢灵感/绿色挂饰的多人修正")

print("[6] 多人：玩家级钩子都要判 Owner")
relics_dir = os.path.join(CODE, "Relics")
for fname, cls in (("DriedInspiration.cs", "DriedInspiration"), ("MoreRelics.cs", "OverflowingInspiration"),
                   ("MoreRelics.cs", "GreenCharm")):
    src = read(os.path.join(relics_dir, fname))
    body = block(src, cls)
    chk("if (player != Owner)" in body, "%s 的 AfterPlayerTurnStart 判了 player != Owner" % cls)
concept = read(os.path.join(CODE, "Cards", "ConceptCard.cs"))
chk("if (player != Owner ||" in concept, "ConceptCard 本来就判了 Owner")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
