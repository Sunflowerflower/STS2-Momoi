# -*- coding: utf-8 -*-
"""批次40：一批卡牌改动（费用/稀有度/关键词/数值/新效果）。"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

CODE = r"C:\Users\asus\RiderProjects\STS2 Momoi\STS2 Momoi\STS2 MomoiCode"


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
    raise SystemExit("unclosed " + cls)


def patch_class(rel, cls, pairs, label):
    p = CODE + "\\" + rel.replace("/", "\\")
    d = io.open(p, encoding="utf-8").read()
    s, e = span(d, cls)
    seg = d[s:e]
    for old, new in pairs:
        assert old in seg, "没找到 [%s/%s]：%s" % (label, cls, old[:80])
        assert seg.count(old) == 1, "多处 [%s/%s]：%s" % (label, cls, old[:80])
        seg = seg.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(d[:s] + seg + d[e:])
    print("  OK %-22s %s" % (label, cls))


# 1) 复盘：升级前消耗，升级后删去
patch_class("Cards/CommonAttackCards.cs", "GameReview", [
 ("""    // 只保留「消耗牌堆里的随机小游戏牌回手」这一个效果（升级前后只差是否升级那张牌）。""",
  """    // 消耗（升级后删去），只保留「消耗牌堆里的随机小游戏牌回手」这一个效果。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };
"""),
 ("""    protected override void OnUpgrade()
    {
        // 升级效果只有「放入的那张牌是升级过的」，见 OnPlay 的 IsUpgraded 分支。
    }""",
  """    protected override void OnUpgrade()
    {
        // 升级：删去消耗（另外放入的那张牌是升级过的，见 OnPlay 的 IsUpgraded 分支）。
        RemoveKeyword(CardKeyword.Exhaust);
    }

    protected override void AfterDowngraded()
    {
        base.AfterDowngraded();
        AddKeyword(CardKeyword.Exhaust);
    }"""),
], "复盘 消耗")

# 2) 伏笔回收 稀有 -> 罕见；100连抽 罕见 -> 稀有
patch_class("Cards/ConceptFlowCards.cs", "ForeshadowRecovery", [
 ("public ForeshadowRecovery() : base(2, CardType.Skill, CardRarity.Rare, TargetType.Self)",
  "public ForeshadowRecovery() : base(2, CardType.Skill, CardRarity.Uncommon, TargetType.Self)"),
], "伏笔回收 罕见")
patch_class("Cards/HundredPull.cs", "HundredPull", [
 ("public HundredPull() : base(4, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)",
  "public HundredPull() : base(4, CardType.Attack, CardRarity.Rare, TargetType.AnyEnemy)"),
], "100连抽 稀有")

# 3) 循环叙事：0 费，升级加保留
p = CODE + r"\Cards\NewCardsBatch.cs"
d = io.open(p, encoding="utf-8").read()
s, e = span(d, "CyclicNarrative")
seg = d[s:e]
seg = seg.replace("public CyclicNarrative() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)",
                  "public CyclicNarrative() : base(0, CardType.Skill, CardRarity.Uncommon, TargetType.Self)")
seg = seg.replace("""    protected override void OnUpgrade()
    {
        EnergyCost.UpgradeBy(-1);
    }""",
                  """    protected override void OnUpgrade()
    {
        // 升级：获得保留（费用升级前后都是 0）。
        AddKeyword(CardKeyword.Retain);
    }

    protected override void AfterDowngraded()
    {
        base.AfterDowngraded();
        RemoveKeyword(CardKeyword.Retain);
    }""")
io.open(p, "w", encoding="utf-8").write(d[:s] + seg + d[e:])
print("  OK 循环叙事 0 费 + 升级保留")

# 4) 再启新篇：有构想时不再加自身费用
patch_class("Cards/ConceptFlowCards.cs", "NewChapter", [
 ("""        var player = Owner.Creature.Player;
        var hasConcept = player != null && PileType.Hand.GetPile(player).Cards.Any(c => c is ConceptCard);
        if (!hasConcept)
        {
            var combatState = Owner.Creature.CombatState;
            if (combatState != null)
            {
                var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), Owner);
                await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, Owner);
            }
        }

        // 这张牌的耗费+1（本场战斗）。
        EnergyCost.SetThisCombat(EnergyCost.GetResolved() + 1, reduceOnly: false);""",
  """        var player = Owner.Creature.Player;
        var hasConcept = player != null && PileType.Hand.GetPile(player).Cards.Any(c => c is ConceptCard);
        if (!hasConcept)
        {
            var combatState = Owner.Creature.CombatState;
            if (combatState != null)
            {
                var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), Owner);
                await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, Owner);
            }

            // 只有「手牌里没有构想、于是补了一张」这一支才让这张牌的耗费+1（本场战斗）。
            EnergyCost.SetThisCombat(EnergyCost.GetResolved() + 1, reduceOnly: false);
        }"""),
], "再启新篇 费用条件")

# 5) 创作的痛苦：新增「获得 2/3 层火力」
patch_class("Cards/CreativePain.cs", "CreativePain", [
 ("""        new DynamicVar("Burn", 3),   // 升级 5""",
  """        new DynamicVar("Firepower", 2),  // 升级 3
        new DynamicVar("Burn", 3),   // 升级 5"""),
 ("""        DynamicVars["Burn"].UpgradeValueBy(2);  // 灼烧 3 -> 5""",
  """        DynamicVars["Burn"].UpgradeValueBy(2);  // 灼烧 3 -> 5
        DynamicVars["Firepower"].UpgradeValueBy(1);  // 火力 2 -> 3"""),
], "创作的痛苦 火力数值")

# 6) 扫雷：炸弹洗到抽牌堆随机位置
patch_class("Cards/RemainingCards4.cs", "Minesweeper", [
 ("""        await CardPileCmd.AddGeneratedCardToCombat(bomb, PileType.Draw, Owner, CardPilePosition.Top);""",
  """        // 洗入抽牌堆的随机位置（与卡面「加入抽牌堆」一致；参考原版守墓人 GraveWarden 的 CardPilePosition.Random）。
        await CardPileCmd.AddGeneratedCardToCombat(bomb, PileType.Draw, Owner, CardPilePosition.Random);"""),
], "扫雷 随机位置")

# 7) 构想之矛 11/15
patch_class("Cards/ConceptFlowCards.cs", "ConceptSpear", [
 ("""        new DynamicVar("Damage", 10)  // 升级 14""",
  """        new DynamicVar("Damage", 11)  // 升级 15"""),
 ("""        DynamicVars["Damage"].UpgradeValueBy(4);   // 10 -> 14""",
  """        DynamicVars["Damage"].UpgradeValueBy(4);   // 11 -> 15"""),
], "构想之矛 11/15")

# 8) 矛与盾 伤害 8/11 -> 11/15（Power 里的叠加常数）
patch_class("Cards/ConceptFlowCards.cs", "SpearShieldPower", [
 ("""        public int DamagePer = 0;  // 叠加后的每张构想伤害（基础 8、升级 11）""",
  """        public int DamagePer = 0;  // 叠加后的每张构想伤害（基础 11、升级 15）"""),
 ("""        data.DamagePer += (int)amount * (upgraded ? 11 : 8);""",
  """        data.DamagePer += (int)amount * (upgraded ? 15 : 11);"""),
], "矛与盾 11/15")

# 9) 发布委托：2 费，格挡 11/14
patch_class("Cards/MinigameFlowCards.cs", "PostQuest", [
 ("public PostQuest() : base(1, CardType.Skill, CardRarity.Common, TargetType.Self)",
  "public PostQuest() : base(2, CardType.Skill, CardRarity.Common, TargetType.Self)"),
 ("""        new BlockVar(7m, ValueProp.Move)  // 升级 10""",
  """        new BlockVar(11m, ValueProp.Move)  // 升级 14"""),
 ("""        DynamicVars["Block"].UpgradeValueBy(3);""",
  """        DynamicVars["Block"].UpgradeValueBy(3);   // 11 -> 14"""),
], "发布委托 2 费 11/14")

# 10) 整装待发：格挡 6/8，活力/火力 2/3
patch_class("Cards/FirepowerFlowCards.cs", "GearUp", [
 ("""        new BlockVar(8m, ValueProp.Move),    // 升级 10""",
  """        new BlockVar(6m, ValueProp.Move),    // 升级 8"""),
 ("""        new DynamicVar("Vigor", 1),    // 升级 2""",
  """        new DynamicVar("Vigor", 2),    // 升级 3"""),
 ("""        new DynamicVar("Firepower", 1) // 升级 2""",
  """        new DynamicVar("Firepower", 2) // 升级 3"""),
], "整装待发 6/8 + 2/3")

# 11) 局势升温：2 费，12/16
patch_class("Cards/BurnFlowCards.cs", "PlayWithFire", [
 ("public PlayWithFire() : base(1, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)",
  "public PlayWithFire() : base(2, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)"),
 ("""        new CalculationBaseVar(10m),  // 升级 13""",
  """        new CalculationBaseVar(12m),  // 升级 16"""),
 ("""        DynamicVars.CalculationBase.UpgradeValueBy(3);""",
  """        DynamicVars.CalculationBase.UpgradeValueBy(4);   // 12 -> 16"""),
], "局势升温 2 费 12/16")

# 12) 王不见王：1/1 费，升级前消耗、升级后删去
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

# 13) 瓶颈突破：构想 +1/2
patch_class("Cards/ConceptFlowCards.cs", "BottleneckBreak", [
 ("""        new DynamicVar("Hits", 3)  // 升级 4""",
  """        new DynamicVar("Hits", 3),  // 升级 4
        new DynamicVar("ConceptGain", 1)  // 构想 +1，升级 +2"""),
 ("""        DynamicVars["Hits"].UpgradeValueBy(1);""",
  """        DynamicVars["Hits"].UpgradeValueBy(1);
        DynamicVars["ConceptGain"].UpgradeValueBy(1);   // 构想 +1 -> +2"""),
], "瓶颈突破 构想 1/2")

# 14) 黄金矿工 1/0 费
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

# 15) 愤怒的小鸟 1/1 费
patch_class("Cards/RemainingCards4.cs", "AngryBirds", [
 ("public AngryBirds() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)",
  "public AngryBirds() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)"),
], "愤怒的小鸟 1 费")

# 16) 博览群游：随机敌人
patch_class("Cards/CommonAttackCards.cs", "ExperienceCombo", [
 ("public ExperienceCombo() : base(1, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)",
  "public ExperienceCombo() : base(1, CardType.Attack, CardRarity.Uncommon, TargetType.RandomEnemy)"),
], "博览群游 随机目标")

print("全部完成")
