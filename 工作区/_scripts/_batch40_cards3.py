# -*- coding: utf-8 -*-
"""批次40（续2）：瓶颈突破用变量、博览群游随机敌人、日复一日 3/2 费+保留。"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

CODE = r"C:\Users\asus\RiderProjects\STS2 Momoi\STS2 Momoi\STS2 MomoiCode"


def read(rel):
    return io.open(CODE + "\\" + rel.replace("/", "\\"), encoding="utf-8").read()


def write(rel, txt):
    io.open(CODE + "\\" + rel.replace("/", "\\"), "w", encoding="utf-8").write(txt)


def rep(rel, old, new, label):
    d = read(rel)
    assert old in d, "没找到：" + label
    assert d.count(old) == 1, "多处：" + label
    write(rel, d.replace(old, new))
    print("  OK " + label)


# 1) 瓶颈突破：构想用 ConceptGain 变量
rep("Cards/ConceptFlowCards.cs",
    """        await ConceptCounterCapability.AddCountToAllInHand(choiceContext, Owner.Creature, 1);""",
    """        await ConceptCounterCapability.AddCountToAllInHand(choiceContext, Owner.Creature,
            DynamicVars["ConceptGain"].IntValue);""",
    "瓶颈突破 构想用变量")

# 2) 博览群游：随机敌人（参考原版散射炮 FlakCannon：TargetingRandomOpponents）
d = read("Cards/CommonAttackCards.cs")
m = re.search(r"\bclass\s+ExperienceCombo\b", d)
brace = d.find("{", m.end())
depth = 0
for j in range(brace, len(d)):
    if d[j] == "{":
        depth += 1
    elif d[j] == "}":
        depth -= 1
        if depth == 0:
            break
seg = d[m.start():j + 1]
old = """    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        var hits = Convert.ToInt32(DynamicVars["CalculatedHits"]);
        if (hits > 0)
        {
            await DamageCmd.Attack(DynamicVars.CalculatedDamage)
                .FromCard(this, cardPlay)
                .Targeting(target)
                .WithHitCount(hits)
                .Execute(choiceContext);
        }
    }"""
new = """    // 随机敌人：每一击各自随机挑目标（参考原版散射炮 FlakCannon 的 TargetingRandomOpponents）。
    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var hits = Convert.ToInt32(DynamicVars["CalculatedHits"]);
        if (hits > 0)
        {
            await DamageCmd.Attack(DynamicVars.CalculatedDamage)
                .FromCard(this, cardPlay)
                .TargetingRandomOpponents(combatState)
                .WithHitCount(hits)
                .Execute(choiceContext);
        }
    }"""
assert old in seg, "博览群游 OnPlay 没找到"
write("Cards/CommonAttackCards.cs", d[:m.start()] + seg.replace(old, new) + d[j + 1:])
print("  OK 博览群游 随机敌人")

# 3) 日复一日：3 费（升级 2），保留升级前后都有（放进 CanonicalKeywords，避免重复）
d = read("Cards/RemainingSpecialCards.cs")
m = re.search(r"\bclass\s+LearnByDoing\b", d)
brace = d.find("{", m.end())
depth = 0
for j in range(brace, len(d)):
    if d[j] == "{":
        depth += 1
    elif d[j] == "}":
        depth -= 1
        if depth == 0:
            break
seg = d[m.start():j + 1]
seg = seg.replace(
    "public LearnByDoing() : base(4, CardType.Power, CardRarity.Uncommon, TargetType.Self)",
    "public LearnByDoing() : base(3, CardType.Power, CardRarity.Uncommon, TargetType.Self)")
seg = seg.replace("""    protected override IEnumerable<DynamicVar> CanonicalVars =>""",
                  """    // 保留升级前后都有（放在 CanonicalKeywords 里，升级时不会再被加一遍 → 不会出现两个「保留」）。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Retain };

    protected override IEnumerable<DynamicVar> CanonicalVars =>""")
seg = seg.replace("""    protected override void OnUpgrade()
    {
        LocalKeywords.Add(CardKeyword.Retain);
        DynamicVars["CostReduce"].UpgradeValueBy(1);
    }""",
                  """    protected override void OnUpgrade()
    {
        // 升级：耗能 3 -> 2（保留已在 CanonicalKeywords 里，不重复添加）。
        EnergyCost.UpgradeBy(-1);
        DynamicVars["CostReduce"].UpgradeValueBy(1);
    }""")
write("Cards/RemainingSpecialCards.cs", d[:m.start()] + seg + d[j + 1:])
print("  OK 日复一日 3/2 费 + 保留")
