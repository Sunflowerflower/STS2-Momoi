# -*- coding: utf-8 -*-
"""批次44：平衡性调整（22 项）。"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

CODE = r"C:\Users\asus\RiderProjects\STS2 Momoi\STS2 Momoi\STS2 MomoiCode"
FILES = {}


def load(rel):
    if rel not in FILES:
        FILES[rel] = io.open(CODE + "\\" + rel.replace("/", "\\"), encoding="utf-8").read()
    return FILES[rel]


def save(rel):
    io.open(CODE + "\\" + rel.replace("/", "\\"), "w", encoding="utf-8").write(FILES[rel])


def span(src, cls):
    m = re.search(r"\bclass\s+" + cls + r"\b", src)
    if not m:
        raise SystemExit("no class " + cls)
    brace = src.find("{", m.end())
    depth = 0
    for j in range(brace, len(src)):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                return m.start(), j + 1


def patch(rel, cls, pairs, label):
    d = load(rel)
    s, e = span(d, cls)
    seg = d[s:e]
    for old, new in pairs:
        if old not in seg:
            if new and new in seg:
                print("  -- 已应用:", label)
                continue
            raise SystemExit("no match [%s/%s]: %s" % (label, cls, old[:80]))
        seg = seg.replace(old, new, 1)
    FILES[rel] = d[:s] + seg + d[e:]
    save(rel)
    print("  OK %-26s %s" % (label, cls))


# 1) 过载：费 1 -> 2；活力 3/4 -> 2/3
patch("Cards/PortalParadoxAndOverload.cs", "Overload", [
 ("public Overload() : base(1, CardType.Power", "public Overload() : base(2, CardType.Power"),
 ('new DynamicVar("Vigor", 3)       // 升级 4', 'new DynamicVar("Vigor", 2)       // 升级 3'),
 ("DynamicVars[\"Vigor\"].UpgradeValueBy(1);       // 3 -> 4", "DynamicVars[\"Vigor\"].UpgradeValueBy(1);       // 2 -> 3"),
], "过载 2 费/活力 2-3")

# 2) 修行：费 1 -> 2
patch("Cards/NewCardsBatch.cs", "AsceticTraining", [
 ("public AsceticTraining() : base(1, CardType.Power", "public AsceticTraining() : base(2, CardType.Power"),
], "修行 2 费")

# 3) BA启动：活力 3/4 -> 2/3
patch("Cards/FirepowerFlowCards.cs", "BaBoot", [
 ('new DynamicVar("Vigor", 3),  // 升级 4', 'new DynamicVar("Vigor", 2),  // 升级 3'),
], "BA启动 活力 2-3")

# 4) 整装待发：格挡 6/8 -> 4/6
patch("Cards/FirepowerFlowCards.cs", "GearUp", [
 ("new BlockVar(6m, ValueProp.Move),    // 升级 8", "new BlockVar(4m, ValueProp.Move),    // 升级 6"),
], "整装待发 格挡 4-6")

# 5) 天马行空：伤害 5/7 -> 4/4（升级不再加伤害，只加一击）
patch("Cards/ConceptFlowCards.cs", "BulletRain", [
 ("new CalculationBaseVar(5m),   // 升级 7", "new CalculationBaseVar(4m),   // 升级 4（升级只加 1 次额外攻击）"),
 ("        DynamicVars.CalculationBase.UpgradeValueBy(2);\n", ""),
], "天马行空 4-4")

# 6) 博览群游：7/9 -> 5/7
patch("Cards/CommonAttackCards.cs", "ExperienceCombo", [
 ("new CalculationBaseVar(7m),  // 升级 9", "new CalculationBaseVar(5m),  // 升级 7"),
 ("DynamicVars.CalculationBase.UpgradeValueBy(2);   // 7 -> 9", "DynamicVars.CalculationBase.UpgradeValueBy(2);   // 5 -> 7"),
], "博览群游 5-7")

# 8) 植物大战僵尸：升级不再减费（1/1）
patch("Cards/RemainingCards5.cs", "PlantsVsZombies", [
 ("""        // 升级：耗能 1 -> 0。
        EnergyCost.UpgradeBy(-1);""",
  """        // 升级不再减费（费用升级前后都是 1）。"""),
], "PvZ 1-1 费")

# 9) 传送门悖论：费 0 -> 1
patch("Cards/PortalParadoxAndOverload.cs", "PortalParadox", [
 ("public PortalParadox() : base(0, CardType.Skill", "public PortalParadox() : base(1, CardType.Skill"),
], "传送门悖论 1 费")

# 10) 激战：伤害 3/3 -> 2/2
patch("Cards/RemainingSpecialCards.cs", "ConfusedShot", [
 ("new CalculationBaseVar(3m),", "new CalculationBaseVar(2m),"),
], "激战 2-2")

# 11) 翻滚射击：格挡 7/9 -> 6/8
patch("Cards/CommonAttackCards.cs", "RollAndShoot", [
 ("new BlockVar(7m, ValueProp.Move)   // 升级 9", "new BlockVar(6m, ValueProp.Move)   // 升级 8"),
], "翻滚射击 6-8")

# 12) 对策：活力 5/7 -> 4/5
patch("Cards/IntentCards.cs", "Countermeasure", [
 ('new DynamicVar("Vigor", 5),    // 升级 7', 'new DynamicVar("Vigor", 4),    // 升级 5'),
 ('DynamicVars["Vigor"].UpgradeValueBy(2);', 'DynamicVars["Vigor"].UpgradeValueBy(1);   // 4 -> 5'),
], "对策 活力 4-5")

# 13) 我复活啦：活力 3/5 -> 2/3
patch("Cards/ImBack.cs", "ImBack", [
 ('new DynamicVar("Vigor", 3),        // 升级 5', 'new DynamicVar("Vigor", 2),        // 升级 3'),
 ('DynamicVars["Vigor"].UpgradeValueBy(2);   // 3 -> 5', 'DynamicVars["Vigor"].UpgradeValueBy(1);   // 2 -> 3'),
], "我复活啦 活力 2-3")

# 14) 捕鱼达人：伤害 11/11 -> 8/8
patch("Cards/RemainingCards2.cs", "FishingMaster", [
 ("new CalculationBaseVar(11m),", "new CalculationBaseVar(8m),"),
], "捕鱼达人 8-8")

# 15) 旅行异蛙：格挡 6/7 -> 6/6（升级不再加格挡）
patch("Cards/RemainingCards3.cs", "TravelFrog", [
 ("new BlockVar(6m, ValueProp.Move),    // 升级 7", "new BlockVar(6m, ValueProp.Move),    // 升级 6（升级只加每堆数值）"),
 ("        DynamicVars[\"Block\"].UpgradeValueBy(1);\n", ""),
], "旅行异蛙 6-6")

# 16) 相遇：格挡 8/10 -> 6/7
patch("Cards/RemainingSpecialCards.cs", "Encounter", [
 ("new BlockVar(8m, ValueProp.Move)  // 升级 10", "new BlockVar(6m, ValueProp.Move)  // 升级 7"),
 ("DynamicVars[\"Block\"].UpgradeValueBy(2);", "DynamicVars[\"Block\"].UpgradeValueBy(1);   // 6 -> 7"),
], "相遇 6-7")

# 17) 构想之盾：升级不再给固有
patch("Cards/ConceptFlowCards.cs", "ConceptShield", [
 ("        LocalKeywords.Add(CardKeyword.Innate);\n", ""),
], "构想之盾 升级不给固有")

# 18) 来自时的援护：火力 3/4 -> 2/3
patch("Cards/AssistCards2.cs", "MomoiSupportToki", [
 ('new DynamicVar("Firepower", 3)  // 升级 4', 'new DynamicVar("Firepower", 2)  // 升级 3'),
], "时 火力 2-3")

# 19) LOSE！：活力 3/5 -> 2/3
patch("Cards/RemainingSpecialCards.cs", "LoseCard", [
 ('new DynamicVar("Vigor", 3)  // 升级 5', 'new DynamicVar("Vigor", 2)  // 升级 3'),
 ('DynamicVars["Vigor"].UpgradeValueBy(2);', 'DynamicVars["Vigor"].UpgradeValueBy(1);   // 2 -> 3'),
], "LOSE！活力 2-3")

# 20) 节奏游戏：伤害 18/20、每方块 6/5、费 1/1
patch("Cards/RemainingCards5.cs", "RhythmGame", [
 ("public RhythmGame() : base(0, CardType.Power", "public RhythmGame() : base(1, CardType.Power"),
 ('new DynamicVar("Damage", 18),  // 升级 24', 'new DynamicVar("Damage", 18),  // 升级 20'),
 ('new DynamicVar("PerBlock", 6)  // 升级 4', 'new DynamicVar("PerBlock", 6)  // 升级 5'),
 ('DynamicVars["Damage"].UpgradeValueBy(6);    // 18 -> 24', 'DynamicVars["Damage"].UpgradeValueBy(2);    // 18 -> 20'),
 ('DynamicVars["PerBlock"].UpgradeValueBy(-2); // 6 -> 4', 'DynamicVars["PerBlock"].UpgradeValueBy(-1); // 6 -> 5'),
 ('data.Damage += cardSource?.IsUpgraded == true ? 24 : 18;', 'data.Damage += cardSource?.IsUpgraded == true ? 20 : 18;'),
 ('data.PerBlock += cardSource?.IsUpgraded == true ? 4 : 6;', 'data.PerBlock += cardSource?.IsUpgraded == true ? 5 : 6;'),
], "节奏游戏 18-20 / 6-5 / 1 费")

# 21) 绷到我了：失去生命 1/1 -> 2/2，格挡 5/7 -> 6/8
patch("Cards/HoldItInCards.cs", "ItCrackedMe", [
 ("new HpLossVar(1m),", "new HpLossVar(2m),"),
 ("new BlockVar(5, ValueProp.Move)   // 升级 7", "new BlockVar(6, ValueProp.Move)   // 升级 8"),
], "绷到我了 2 血 / 6-8 格挡")

# 22) 我还能绷五万年呢：格挡 5/7 -> 4/6
patch("Cards/HoldItInCards.cs", "FiftyThousandYears", [
 ("new BlockVar(5, ValueProp.Move)   // 升级 7", "new BlockVar(4, ValueProp.Move)   // 升级 6"),
], "五万年 4-6 格挡")

print("done")
