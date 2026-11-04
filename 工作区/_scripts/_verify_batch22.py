# -*- coding: utf-8 -*-
"""批次22 自检：曳光弹升级灼烧、整活/堕落/破势文本、吃豆人诅咒范围、稀有度与费用。"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
LOC = os.path.join(MOD, "localization")

ok = fail = 0


def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))


def code(path):
    return open(os.path.join(CODE, path), encoding="utf-8").read()


def body(src, cls):
    m = re.search(r"\bclass\s+" + cls + r"\b", src)
    if not m:
        return ""
    i = src.find("{", m.end())
    depth = 0
    for j in range(i, len(src)):
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
dv = code(os.path.join("Cards", "DynamicVarSupport.cs"))
ff = code(os.path.join("Cards", "FirepowerFlowCards.cs"))
rb2 = code(os.path.join("Cards", "ReworkBatch2.cs"))
ncb2 = code(os.path.join("Cards", "NewCardsBatch2.cs"))
rc2 = code(os.path.join("Cards", "RemainingCards2.cs"))
ca = code(os.path.join("Cards", "CommonAttackCards.cs"))
rc3 = code(os.path.join("Cards", "RemainingCards3.cs"))
rc5 = code(os.path.join("Cards", "RemainingCards5.cs"))
vig = code(os.path.join("Patches", "VigorMultiplierPatch.cs"))

print("== 1. 曳光弹：升级后灼烧 3 -> 4（IndependentCalculatedVar 的 Clone 浅拷贝 bug）==")
chk("_baseName" in dv and "Resolve(_baseName, _baseFallback)" in dv, "按名字实时解析 base")
chk("set.TryGetValue(name, out var v)" in dv, "从持有者的 DynamicVars 取当前实例")
chk("MemberwiseClone" in dv, "注释写明了真因")
fb = body(ff, "FlameBullet")
chk('new DynamicVar("BurnBase", 3m)' in fb, "基础灼烧 3")
chk('DynamicVars["BurnBase"].UpgradeValueBy(1)' in fb, "升级 +1 -> 4")
chk("IndependentCalculatedVar" in fb, "曳光弹仍用 IndependentCalculatedVar")

print("== 2. 整活：卡面补「升级过的」==")
z = Z["STS2_MOMOI_CARD_SLAPSTICK.description"]
chk("{IfUpgraded:show:升级过的|}随机[gold]小游戏牌[/gold]" in z, "zhs", z)
chk("{Cards:diff()}" in z, "抽牌数仍是变量")
e = E["STS2_MOMOI_CARD_SLAPSTICK.description"]
chk("{IfUpgraded:show:an upgraded|a} random [gold]Minigame[/gold]" in e, "eng", e)
chk("IsUpgraded" in body(rb2, "Slapstick"), "效果本来就按升级走（未改动）")

print("== 3. 吃豆人：诅咒范围 = 抽牌堆 + 手牌 + 弃牌堆 ==")
pm = body(rc5, "PacManPower")
chk("new[] { PileType.Draw, PileType.Hand, PileType.Discard }" in pm, "三堆都查")
chk("PileType.Hand.GetPile(player).Cards" not in pm, "不再只看手牌")
chk("CardPile.Get(pileType, player)" in pm, "用 CardPile.Get（非战斗安全）")
chk("await CardCmd.Exhaust(ctx, curse);" in pm, "仍然随机消耗 1 张（含抽/弃牌堆里的）")

print("== 4. 堕落 ==")
chk("public Depravity() : base(0, CardType.Skill, CardRarity.Uncommon" in ncb2, "稀有度 普通 -> 罕见")
dp = body(ncb2, "Depravity")
chk("PowerCmd.Apply<FrailPower>" in dp and "PowerCmd.Apply<WeakPower>" in dp, "脆弱 + 虚弱都给")
chk(dp.count("PowerCmd.Apply<") == 2, "没有多给别的 debuff")
up = dp.split("OnUpgrade")[-1]
chk("DynamicVars" not in up, "升级效果不变（只切升级版小游戏牌）")
z = Z["STS2_MOMOI_CARD_DEPRAVITY.description"]
chk("给予自身1层[gold]脆弱[/gold]和1层[gold]虚弱[/gold]。" in z, "zhs 只在脆弱后加「和1层虚弱」", z)
chk(z.count("[gold]") == 4, "没有乱加关键词（脆弱/虚弱/小游戏牌/手牌 各一处）", z)
e = E["STS2_MOMOI_CARD_DEPRAVITY.description"]
chk("Gain 1 [gold]Frail[/gold] and 1 [gold]Weak[/gold]." in e, "eng 文本", e)

print("== 5. 独特点子：稀有度改普通 ==")
chk("public UniqueIdea() : base(1, CardType.Attack, CardRarity.Common" in ca, "罕见 -> 普通")

print("== 6. 破势 ==")
mb = body(rc2, "MomentumBreak")
chk("public MomentumBreak() : base(2, CardType.Attack" in mb, "费用 2（升级前后都是 2）")
chk("EnergyCost.UpgradeBy" not in mb, "升级不再减费")
chk("new CalculationBaseVar(16m)" in mb, "基础伤害 16")
chk("DynamicVars.CalculationBase.UpgradeValueBy(4)" in mb, "升级 +4 -> 20")
chk("ModifyDamageMultiplicative" not in mb, "旧的「每点活力 +10%/20%」已删除")
chk("VigorMultiplierPatch.cs" in mb, "注释指向补丁")
chk("cardSource is not MomentumBreak momentum" in vig, "破势专属补丁")
chk("__result *= momentum.IsUpgraded ? 5m : 4m;" in vig, "活力 ×4 / 升级 ×5")
chk("nameof(VigorPower.ModifyDamageAdditive)" in vig, "挂在 VigorPower.ModifyDamageAdditive")
chk("RegisterPatch<Patches.VigorMultiplierPatch>()" in code("Entry.cs"), "已注册补丁")
z = Z["STS2_MOMOI_CARD_MOMENTUM_BREAK.description"]
want_z = ('造成{CalculatedDamage:diff()}点伤害。\n[gold]活力[/gold]在这张牌上发挥{IfUpgraded:show:5|4}倍的效果。\n'
          '若目标的意图为攻击，且这张牌造成的伤害大于目标即将对你造成的伤害，[gold]击晕[/gold]该敌人并将这张牌的耗能增加'
          '{CostIncrease:energyIcons()}。')   # 「击晕」批次23 补金色
chk(z == want_z, "zhs 文本与要求一致（击晕已补金色）", z)
e = E["STS2_MOMOI_CARD_MOMENTUM_BREAK.description"]
chk("{IfUpgraded:show:5|4} times on this card" in e, "eng 文本", e)

print("== 7. 费用 ==")
chk("public Focus() : base(1, CardType.Power" in rc3, "专注 1 费（批次30 最终口径）")
chk("EnergyCost.UpgradeBy(-1)" in body(rc3, "Focus"), "专注升级 -1 -> 0 费")
chk("public ExperienceCombo() : base(1, CardType.Attack" in ca, "博览群游 0 -> 1 费")
chk("升级前后都是 1" in ca, "博览群游注释同步")
chk("public SystemAbishu() : base(1, CardType.Attack" in code(os.path.join("Cards", "AssistCards2.cs")),
    "系统：阿比舒 1 费（上一批）")

print("== 8. 侧栏（靠文本自动附加）==")
patch = code(os.path.join("Patches", "MinigameSidebarPatch.cs"))
chk('Has("活力", "Vigor")' in patch, "活力侧栏：文本含活力自动加")
chk('Has("虚弱", "Weak")' in patch, "虚弱侧栏：文本含虚弱自动加")
chk("ModCardTemplate" in patch, "补丁覆盖所有模组卡")

print("== 9. 标签闭合 ==")
bad = []
for lang in ("zhs", "eng"):
    for f in os.listdir(os.path.join(LOC, lang)):
        if not f.endswith(".json"):
            continue
        d = load(lang, f[:-5])
        for k, v in d.items():
            if not isinstance(v, str):
                continue
            for tag in set(re.findall(r"\[([a-z]+)\]", v)):
                if v.count("[%s]" % tag) != v.count("[/%s]" % tag):
                    bad.append("%s/%s/%s[%s]" % (lang, f, k, tag))
chk(not bad, "标签全部闭合", bad[:6])

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
