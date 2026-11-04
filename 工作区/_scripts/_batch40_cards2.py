# -*- coding: utf-8 -*-
"""批次40（续）：剩余卡牌改动 + 创作的痛苦 OnPlay 加火力。"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

CODE = r"C:\Users\asus\RiderProjects\STS2 Momoi\STS2 Momoi\STS2 MomoiCode"


def span(src, cls):
    m = re.search(r"\bclass\s+" + cls + r"\b", src)
    brace = src.find("{", m.end())
    depth = 0
    for j in range(brace, len(src)):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                return m.start(), j + 1


def patch_class(rel, cls, pairs, label):
    p = CODE + "\\" + rel.replace("/", "\\")
    d = io.open(p, encoding="utf-8").read()
    s, e = span(d, cls)
    seg = d[s:e]
    for old, new in pairs:
        if old not in seg:
            if new in seg:
                print("  -- 已应用，跳过:", label, cls)
                continue
            raise SystemExit("没找到 [%s/%s]：%s" % (label, cls, old[:80]))
        seg = seg.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(d[:s] + seg + d[e:])
    print("  OK %-22s %s" % (label, cls))


# 创作的痛苦：OnPlay 开头加「获得火力」
patch_class("Cards/CreativePain.cs", "CreativePain", [
 ("""        // 给予所有敌人灼烧。
        foreach (var enemy in combatState.HittableEnemies)""",
  """        // 第一行效果：获得火力。
        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature,
            DynamicVars["Firepower"].IntValue, Owner.Creature, this);

        // 给予所有敌人灼烧。
        foreach (var enemy in combatState.HittableEnemies)"""),
], "创作痛苦 加火力")

# 扫雷：随机位置
patch_class("Cards/RemainingCards4.cs", "Minesweeper", [
 ("""        await CardPileCmd.AddGeneratedCardToCombat(bomb, PileType.Draw, Owner, CardPilePosition.Top);""",
  """        // 洗入抽牌堆的随机位置（与卡面「加入抽牌堆」一致；参考原版守墓人 GraveWarden 的 CardPilePosition.Random）。
        await CardPileCmd.AddGeneratedCardToCombat(bomb, PileType.Draw, Owner, CardPilePosition.Random);"""),
], "扫雷 随机位置")

# 构想之矛 11/15
patch_class("Cards/ConceptFlowCards.cs", "ConceptSpear", [
 ("""        new DynamicVar("Damage", 10)  // 升级 14""",
  """        new DynamicVar("Damage", 11)  // 升级 15"""),
 ("""        DynamicVars["Damage"].UpgradeValueBy(4);   // 10 -> 14""",
  """        DynamicVars["Damage"].UpgradeValueBy(4);   // 11 -> 15"""),
], "构想之矛 11/15")

# 矛与盾 伤害 11/15
patch_class("Cards/ConceptFlowCards.cs", "SpearShieldPower", [
 ("""        public int DamagePer = 0;  // 叠加后的每张构想伤害（基础 8、升级 11）""",
  """        public int DamagePer = 0;  // 叠加后的每张构想伤害（基础 11、升级 15）"""),
 ("""        data.DamagePer += (int)amount * (upgraded ? 11 : 8);""",
  """        data.DamagePer += (int)amount * (upgraded ? 15 : 11);"""),
], "矛与盾 11/15")

# 发布委托 2 费 + 11/14
patch_class("Cards/MinigameFlowCards.cs", "PostQuest", [
 ("public PostQuest() : base(1, CardType.Skill, CardRarity.Common, TargetType.Self)",
  "public PostQuest() : base(2, CardType.Skill, CardRarity.Common, TargetType.Self)"),
 ("""        new BlockVar(7m, ValueProp.Move)  // 升级 10""",
  """        new BlockVar(11m, ValueProp.Move)  // 升级 14"""),
 ("""        DynamicVars["Block"].UpgradeValueBy(3);""",
  """        DynamicVars["Block"].UpgradeValueBy(3);   // 11 -> 14"""),
], "发布委托 2 费 11/14")

# 整装待发 6/8 + 2/3
patch_class("Cards/FirepowerFlowCards.cs", "GearUp", [
 ("""        new BlockVar(8m, ValueProp.Move),    // 升级 10""",
  """        new BlockVar(6m, ValueProp.Move),    // 升级 8"""),
 ("""        new DynamicVar("Vigor", 1),    // 升级 2""",
  """        new DynamicVar("Vigor", 2),    // 升级 3"""),
 ("""        new DynamicVar("Firepower", 1) // 升级 2""",
  """        new DynamicVar("Firepower", 2) // 升级 3"""),
], "整装待发 6/8 + 2/3")

# 局势升温 2 费 12/16
patch_class("Cards/BurnFlowCards.cs", "PlayWithFire", [
 ("public PlayWithFire() : base(1, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)",
  "public PlayWithFire() : base(2, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)"),
 ("""        new CalculationBaseVar(10m),  // 升级 13""",
  """        new CalculationBaseVar(12m),  // 升级 16"""),
 ("""        DynamicVars.CalculationBase.UpgradeValueBy(3);""",
  """        DynamicVars.CalculationBase.UpgradeValueBy(4);   // 12 -> 16"""),
], "局势升温 2 费 12/16")

# 王不见王：1/1 费，升级前消耗
patch_class("Cards/NewCardsBatch2.cs", "KingsNeverMeet", [
 ("""    protected override void OnUpgrade()
    {
        // 升级：耗能 1 -> 0。""",
  """    // 消耗（升级后删去）。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override void OnUpgrade()
    {
        // 升级：删去消耗（费用升级前后都是 1）。"""),
 ("""        base.EnergyCost.UpgradeBy(-1);""",
  """        RemoveKeyword(CardKeyword.Exhaust);"""),
], "王不见王 消耗")

# 瓶颈突破 构想 +1/2
patch_class("Cards/ConceptFlowCards.cs", "BottleneckBreak", [
 ("""        new DynamicVar("Hits", 3)  // 升级 4""",
  """        new DynamicVar("Hits", 3),  // 升级 4
        new DynamicVar("ConceptGain", 1)  // 构想 +1，升级 +2"""),
 ("""        DynamicVars["Hits"].UpgradeValueBy(1);""",
  """        DynamicVars["Hits"].UpgradeValueBy(1);
        DynamicVars["ConceptGain"].UpgradeValueBy(1);   // 构想 +1 -> +2"""),
], "瓶颈突破 构想 1/2")

# 黄金矿工 1/0 费
patch_class("Cards/RemainingCards2.cs", "GoldMiner", [
 ("public GoldMiner() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)",
  "public GoldMiner() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)"),
 ("""    protected override void OnUpgrade()
    {
        // 升级：获得保留。
        LocalKeywords.Add(CardKeyword.Retain);
    }""",
  """    protected override void OnUpgrade()
    {
        // 升级：耗能 1 -> 0，并获得保留。
        EnergyCost.UpgradeBy(-1);
        LocalKeywords.Add(CardKeyword.Retain);
    }"""),
], "黄金矿工 1/0 费")

# 愤怒的小鸟 1/1 费
patch_class("Cards/RemainingCards4.cs", "AngryBirds", [
 ("public AngryBirds() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)",
  "public AngryBirds() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)"),
], "愤怒的小鸟 1 费")

# 博览群游 随机目标
patch_class("Cards/CommonAttackCards.cs", "ExperienceCombo", [
 ("public ExperienceCombo() : base(1, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)",
  "public ExperienceCombo() : base(1, CardType.Attack, CardRarity.Uncommon, TargetType.RandomEnemy)"),
], "博览群游 随机目标")

print("done")
