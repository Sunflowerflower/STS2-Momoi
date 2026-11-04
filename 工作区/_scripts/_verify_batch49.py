# -*- coding: utf-8 -*-
"""批次49 自检：体积优化 / 多人构想 bug / 角色贴图缩放 / 明日奈持续 / 能力伤害 Unpowered / 数值 / 循环叙事重做。"""
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
RES = os.path.join(MODDIR, "STS2_Momoi")
LOC = os.path.join(RES, "localization")
OUT = os.path.join(ROOT, "工作区", "发布包")
SCRIPTS = os.path.join(ROOT, "工作区", "_scripts")
DEPLOY = r"D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi"
DOC = os.path.join(ROOT, "STS2_Momoi_迁移文档.md")

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


def flat(text):
    return re.sub(r"\s+", " ", text)


def class_block(text, name):
    """按花括号深度取一个类/结构的完整定义。"""
    i = text.index("class " + name)
    j = text.index("{", i)
    depth = 0
    for k in range(j, len(text)):
        c = text[k]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i:k + 1]
    raise ValueError("unbalanced braces: " + name)


print("[1] 体积：pck 已按贴图规则压缩")
pck = os.path.join(DEPLOY, "STS2_Momoi.pck")
chk(os.path.isfile(pck), "部署目录有 pck", pck)
if os.path.isfile(pck):
    size = os.path.getsize(pck)
    chk(size < 70 * 1024 * 1024, "pck < 70MB（压缩后约 55MB）", size)
    print("       实际 pck = %.1f MB" % (size / 1048576.0))
opt = os.path.join(SCRIPTS, "_optimize_textures.py")
chk(os.path.isfile(opt), "有可复跑的 _optimize_textures.py", opt)
opt_src = read(opt)
chk("size_limit" in opt_src and "512" in opt_src, "脚本给 cards 设 size_limit=512")
chk("CUE_QUALITY_RE" in opt_src, "脚本用正则强制 lossy_quality（不只匹配 0.7）")

card_imps = sorted(glob.glob(os.path.join(RES, "images", "cards", "*.png.import")))
cue_imps = sorted(glob.glob(os.path.join(RES, "images", "characters", "cue", "*.png.import")))
chk(len(card_imps) > 100, "cards 有 .import", len(card_imps))
chk(len(cue_imps) > 200, "cue 有 .import", len(cue_imps))
if card_imps:
    t = read(card_imps[0]).replace(" ", "")
    chk("size_limit=512" in t, "cards 卡图导入 size_limit=512", os.path.basename(card_imps[0]))
    chk("compress/mode=0" in t, "cards 保持无损（mode=0）")
if cue_imps:
    t = read(cue_imps[0]).replace(" ", "")
    chk("compress/mode=1" in t, "cue 用有损（mode=1）", os.path.basename(cue_imps[0]))
    chk("compress/lossy_quality=0.95" in t, "cue 有损质量 0.95")
junk = [p for p in glob.glob(os.path.join(RES, "**", "*"), recursive=True)
        if os.path.splitext(p)[1].lower() in (".psd", ".aseprite", ".blend", ".pdb", ".kra")]
chk(not junk, "资源目录没有 psd/aseprite/blend/pdb 杂物", junk[:3])

print("[2] 多人：枯竭灵感只给主人发构想")
dried = read(os.path.join(CODE, "Relics", "DriedInspiration.cs"))
chk("player != Owner" in dried, "AfterPlayerTurnStart 有 player != Owner 守卫")

print("[3] 角色贴图大小设置（0.5~1.5，默认 1.0；批次52 改）")
settings = read(os.path.join(CODE, "Settings", "MomoiSettings.cs"))
fs = flat(settings)
chk("CharacterTextureScale" in settings, "设置项 CharacterTextureScale 存在")
chk("CharacterTextureScale { get; set; } = 1.0" in settings, "默认 1.0（批次52：小桃本体的 0.7 写死在补丁里）")
chk("TextureScaleFactor" in settings and "Math.Clamp" in settings, "TextureScaleFactor 有 Clamp")
chk("AddSlider(" in fs and '"character_texture_scale"' in fs, "设置页有滑块 character_texture_scale")
chk("0.5, 1.5, 0.05" in fs, "滑块范围 0.5~1.5 / 步长 0.05")
chk("CharacterTextureScale.Write(" in settings, "ResetToDefaults 写了这项")
scale = read(os.path.join(CODE, "Patches", "MomoiCharacterScalePatch.cs"))
chk("NCreature" in scale and "ScaleTo" in scale, "补丁打在 NCreature.ScaleTo")
chk("IsPlayer" in scale, "只对玩家生效（Entity.IsPlayer）")
chk("TextureScaleFactor" in scale, "Prefix 里乘 TextureScaleFactor")
chk("NCombatRoom" in scale and "AddCreature" in scale and "GetCreatureNode" in scale,
    "AddCreature 后补一次 ScaleTo（进战斗房间）")
entry = read(os.path.join(CODE, "Entry.cs"))
chk("MomoiCreatureScaleToPatch" in entry, "Entry 注册了 MomoiCreatureScaleToPatch")
chk("MomoiCombatRoomAddCreaturePatch" in entry, "Entry 注册了 MomoiCombatRoomAddCreaturePatch")

print("[4] 来自明日奈的援护：持续到你下回合开始前")
asuna2 = read(os.path.join(CODE, "Cards", "AssistCards2.cs"))
asuna_pw = class_block(asuna2, "AsunaGuardPower")
chk("AfterSideTurnStart" in asuna_pw, "减伤时长在 AfterSideTurnStart 里扣")
chk("TickDownDuration" in asuna_pw, "AfterSideTurnStart 里 TickDownDuration")
chk("AfterSideTurnEnd" not in asuna_pw, "不再在回合结束时扣层")
zhs_cards = json.loads(io.open(os.path.join(LOC, "zhs", "cards.json"), encoding="utf-8-sig").read())
zhs_powers = json.loads(io.open(os.path.join(LOC, "zhs", "powers.json"), encoding="utf-8-sig").read())
eng_cards = json.loads(io.open(os.path.join(LOC, "eng", "cards.json"), encoding="utf-8-sig").read())
eng_powers = json.loads(io.open(os.path.join(LOC, "eng", "powers.json"), encoding="utf-8-sig").read())
zhs_asuna = zhs_cards["STS2_MOMOI_CARD_MOMOI_SUPPORT_ASUNA.description"]
eng_asuna = eng_cards["STS2_MOMOI_CARD_MOMOI_SUPPORT_ASUNA.description"]
chk("直到你的下回合开始前" in zhs_asuna, "卡面写「直到你的下回合开始前」", zhs_asuna)
chk("本回合受到的所有伤害降低" not in zhs_asuna, "卡面不再写「本回合」")
chk("Until the start of your next turn" in eng_asuna, "eng 卡面同步", eng_asuna)
chk("直到你的下[blue]{Amount}[/blue]个回合开始前" in zhs_powers["STS2_MOMOI_POWER_ASUNA_GUARD_POWER.description"],
    "power 文本同步（zhs，批次50 带层数）")
chk("Until the start of your next [blue]{Amount}[/blue] turn(s)"
    in eng_powers["STS2_MOMOI_POWER_ASUNA_GUARD_POWER.description"],
    "power 文本同步（eng，批次50）")
chk("回合内" not in zhs_powers["STS2_MOMOI_POWER_ASUNA_GUARD_POWER.description"],
    "power 不再写「N 回合内」")

print("[5] 能力伤害改 ValueProp.Unpowered（同 Panache/Juggernaut）")
flow = read(os.path.join(CODE, "Cards", "ConceptFlowCards.cs"))
spear = class_block(flow, "ConceptSpearPower")
chk("ValueProp.Unpowered" in spear and "CreatureCmd.Damage" in spear, "构想之矛用 CreatureCmd.Damage + Unpowered")
chk("DamageCmd.Attack" not in spear, "构想之矛不再用 DamageCmd.Attack")
shield = class_block(flow, "SpearShieldPower")
chk("ValueProp.Unpowered" in shield and "CreatureCmd.Damage" in shield, "矛与盾用 CreatureCmd.Damage + Unpowered")
chk("DamageCmd.Attack" not in shield, "矛与盾不再用 DamageCmd.Attack")
r5 = read(os.path.join(CODE, "Cards", "RemainingCards5.cs"))
rhythm = class_block(r5, "RhythmGamePower")
chk("ValueProp.Unpowered" in rhythm and "CreatureCmd.Damage" in rhythm, "节奏游戏用 Unpowered")
chk("DamageCmd.Attack" not in rhythm, "节奏游戏不再用 DamageCmd.Attack")
assist = read(os.path.join(CODE, "Cards", "AssistCards.cs"))
yoshimi = class_block(assist, "YoshimiRepeatPower")
chk("ValueProp.Unpowered" in yoshimi and "CreatureCmd.Damage" in yoshimi, "来自大师的援护用 Unpowered")
chk("FirepowerHooks.SpendVigorAsync" not in yoshimi, "不再自己扣活力")
chk("_vigorThisAttack" not in yoshimi, "删掉了手工补活力的字段")
chk("ModifyDamageMultiplicative" not in yoshimi, "删掉了手工补易伤的修正")

print("[6] 数值：BA启动！/ 再启新篇")
fire = read(os.path.join(CODE, "Cards", "FirepowerFlowCards.cs"))
ba = class_block(fire, "BaBoot")
chk("CardRarity.Uncommon" in ba, "BA启动！改罕见（Uncommon）")
chk('DynamicVar("Vigor", 3)' in ba, "BA启动！活力 3（升级 4）")
chk("CardRarity.Common" not in ba, "BA启动！不再是普通")
chapter = class_block(flow, "NewChapter")
chk("CardRarity.Common" in chapter, "再启新篇改普通（Common）")

print("[7] 循环叙事重做（注能 + 回合结束选牌洗回）")
nb = read(os.path.join(CODE, "Cards", "NewCardsBatch.cs"))
cyc = class_block(nb, "CyclicNarrative")
chk("ModCardTemplate, IImbuedCard" in cyc, "卡实现 IImbuedCard（注能）")
chk("base(1, CardType.Skill, CardRarity.Uncommon" in cyc, "1 费技能罕见")
chk("EnergyCost.UpgradeBy(-1)" in cyc, "升级减 1 费（0 费）")
chk("CardKeyword.Retain" not in cyc, "不再有保留")
chk("ImbuedSupport.ImbuedTip" in cyc, "侧栏用注能词条")
chk("ImbuedSupport.TryAutoPlayAsync" in cyc, "开局自动打出走 ImbuedSupport")
cycp = class_block(nb, "CyclicNarrativePower")
chk("PowerStackType.Counter" in cycp, "层数型能力")
chk("DisplayAmount => Amount" in cycp, "右下角层数 = Amount（可叠加）")
chk("CardSelectCmd.FromCombatPile" in cycp, "用 FromCombatPile 让玩家选弃牌堆的牌")
chk("PileType.Discard" in cycp, "来源是弃牌堆")
chk("CardPilePosition.Random" in cycp, "洗入抽牌堆")
chk("Cancelable = true" in cycp, "可以跳过不选")
chk("0, max" in flat(cycp), "MinSelect=0 / MaxSelect=max（保留手动确认）")
chk("BeforeSideTurnEnd" in cycp and "PowerCmd.Remove(this)" in cycp,
    "弃手牌前结算 + 触发后直接移除（批次50）")
chk("skipVisuals: true" in cycp, "洗入抽牌堆时跳过归位动画（避免下回合抽牌报错）")
chk("ShuffleDiscardsEnteredThisTurn" not in nb, "旧的「本回合进入过弃牌堆」实现已删除")
imb = read(os.path.join(CODE, "Cards", "ImbuedSupport.cs"))
chk("public interface IImbuedCard" in imb, "有 IImbuedCard 接口")
chk("ImbuedTip" in imb and "MOMOI_IMBUED.title" in imb, "注能词条文案复用 enchantments")
chk("CanAutoPlayNow" in imb and "TurnNumber: <= 1" in imb, "注能只在第 1 回合生效")
chk("CardCmd.AutoPlay" in imb and "catch (Exception" in imb, "AutoPlay 有 try/catch 兜底")
patch = read(os.path.join(CODE, "Patches", "MomoiImbuedAndCompendiumPatches.cs"))
chk("c is IImbuedCard" in patch, "置底补丁按 IImbuedCard 筛选")
special = read(os.path.join(CODE, "Cards", "RemainingSpecialCards.cs"))
chk("DevGreen : ModCardTemplate, IImbuedCard" in special, "开发者协同：绿 也实现 IImbuedCard")
chk("ImbuedSupport.TryAutoPlayAsync" in special, "开发者协同：绿 用共用注能逻辑")
zhs_cyc = zhs_cards["STS2_MOMOI_CARD_CYCLIC_NARRATIVE.description"]
chk("[gold]注能[/gold]" in zhs_cyc, "卡面写注能", zhs_cyc)
chk("最多1张牌洗入你的[gold]抽牌堆[/gold]" in zhs_cyc, "卡面写选 1 张洗回", zhs_cyc)
chk("重复此效果" not in zhs_cyc, "卡面删掉旧的「重复此效果」")
chk("{Amount}" in zhs_powers["STS2_MOMOI_POWER_CYCLIC_NARRATIVE_POWER.description"],
    "power 文本用 {Amount} 显示可叠加张数")
sel_z = json.loads(io.open(os.path.join(LOC, "zhs", "card_selection.json"), encoding="utf-8-sig").read())
sel_e = json.loads(io.open(os.path.join(LOC, "eng", "card_selection.json"), encoding="utf-8-sig").read())
chk("STS2_MOMOI_CYCLIC_NARRATIVE_HEADER" in sel_z, "有选择界面文本（zhs）")
chk("{Amount}" in sel_z["STS2_MOMOI_CYCLIC_NARRATIVE_HEADER"], "选择界面文本带 {Amount}",
    sel_z["STS2_MOMOI_CYCLIC_NARRATIVE_HEADER"])
chk("STS2_MOMOI_CYCLIC_NARRATIVE_HEADER" in sel_e, "有选择界面文本（eng）")

print("[8] 版本 1.0.8 + 发布包")
man = json.loads(io.open(os.path.join(MODDIR, "STS2_Momoi.json"), encoding="utf-8-sig").read())
chk(man.get("version") == "1.0.8", "清单版本 1.0.8", man.get("version"))
chk("<Version>1.0.8</Version>" in read(os.path.join(MODDIR, "STS2 Momoi.csproj")), "csproj 版本 1.0.8")
zp = os.path.join(OUT, "STS2_Momoi_v1.0.8.zip")
chk(os.path.isfile(zp), "发布包 STS2_Momoi_v1.0.8.zip 存在", zp)
if os.path.isfile(zp):
    with zipfile.ZipFile(zp) as zf:
        names = zf.namelist()
        chk(all(n == "STS2_Momoi" or n.startswith("STS2_Momoi/") for n in names), "zip 顶层是 STS2_Momoi/")
        m = json.loads(zf.read("STS2_Momoi/STS2_Momoi.json").decode("utf-8-sig"))
        chk(m.get("version") == "1.0.8", "zip 内清单版本 1.0.8")
        chk(bool(m.get("dependencies")) and m["dependencies"][0].get("min_version") == "0.6.7",
            "zip 内清单 min_version 仍是 0.6.7")
        dll = [n for n in names if n.endswith("STS2_Momoi.dll")]
        pckn = [n for n in names if n.endswith("STS2_Momoi.pck")]
        chk(len(dll) == 1 and len(pckn) == 1, "zip 内有 dll + pck", (dll, pckn))
        if pckn and os.path.isfile(pck):
            chk(zf.getinfo(pckn[0]).file_size == os.path.getsize(pck), "zip 内 pck 与部署一致")

print("[9] 文档")
doc = read(DOC)
chk("§21.56" in doc, "迁移文档有 §21.56")
tail = doc.split("§21.56")[-1]
chk("Unpowered" in tail, "§21.56 讲了 Unpowered 能力伤害")
chk("注能" in tail, "§21.56 讲了循环叙事的注能")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
