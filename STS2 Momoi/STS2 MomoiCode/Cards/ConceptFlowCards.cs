using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.Nodes.CommonUi;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Models.Capabilities;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 天马行空：1 费攻击（普通）。对所有敌人造成 5 点伤害，额外攻击等同构想数值次（升级：伤害 7）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class BulletRain : ModCardTemplate
{
    public BulletRain() : base(1, CardType.Attack, CardRarity.Common, TargetType.AllEnemies)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars
    {
        get
        {
            var hitsBase = new DynamicVar("HitsBase", 0m);  // 升级 +1 次额外攻击
            var hitsExtra = new DynamicVar("HitsExtra", 1m);
            return
            [
                new CalculationBaseVar(4m),   // 升级 4（升级只加 1 次额外攻击）
                new ExtraDamageVar(0m),
                new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
                hitsBase,
                hitsExtra,
                // 额外攻击次数 = 构想数值（升级 +1），实时显示，局外 0。
                new IndependentCalculatedVar("ExtraHits", hitsBase, hitsExtra)
                    .WithMultiplier((card, _) => ConceptCounterCapability.GetMaxCountInHand(card.Owner.Creature))
            ];
        }
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 总攻击次数 = 1 + 额外攻击（构想数值，升级 +1）。
        var hits = 1 + Convert.ToInt32(DynamicVars["ExtraHits"]);

        await MomoiGunStyle.ApplyBarrage(
                DamageCmd.Attack(DynamicVars.CalculatedDamage)
                    .FromCard(this, cardPlay)
                    .TargetingAllOpponents(combatState)
                    .WithHitCount(Math.Max(1, hits)),
                Owner.Creature,
                playGunshot: true)
            .Execute(choiceContext);
    }

    protected override void OnUpgrade()
    {
        // 升级：伤害 4→6，额外攻击 +1 次。
        DynamicVars["HitsBase"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 剧本打击：1 费攻击（普通）。造成 9 点伤害，抽等同构想数值张牌（升级：11 伤，数值+1）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class ScriptStrike : ModCardTemplate
{
    public ScriptStrike() : base(1, CardType.Attack, CardRarity.Common, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars
    {
        get
        {
            var cardsBase = new DynamicVar("CardsBase", 0m);
            var cardsExtra = new DynamicVar("CardsExtra", 1m);
            return
            [
                new CalculationBaseVar(9m),   // 升级 11
                new ExtraDamageVar(0m),
                new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
                cardsBase,
                cardsExtra,
                // 抽牌数 = 构想数值 + 升级的 +1，实时显示。
                // 升级的 +1 放在 CardsBase 上（而不是写在 multiplier 里）：这样**局外**也显示 0 / 1，
                // 与「天马行空」的（额外攻击 0 次 / 1 次）表现一致（CalculatedVar 局外 multiplier 记 0）。
                new IndependentCalculatedVar("ConceptCards", cardsBase, cardsExtra).WithMultiplier((card, _) =>
                    ConceptCounterCapability.GetMaxCountInHand(card.Owner.Creature))
            ];
        }
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .Targeting(target)
            .Execute(choiceContext);

        var concept = Convert.ToInt32(DynamicVars["ConceptCards"]);
        if (concept > 0)
        {
            await CardPileCmd.Draw(choiceContext, concept, Owner);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(2);
        DynamicVars["CardsBase"].UpgradeValueBy(1);   // 抽牌数 +1（局内外都显示）
    }
}

/// <summary>
/// 瓶颈突破：2 费攻击（罕见）。造成 5 点伤害 3 次，使所有构想数值+1（升级：4 次）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class BottleneckBreak : ModCardTemplate
{
    public BottleneckBreak() : base(2, CardType.Attack, CardRarity.Common, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(4m),
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new DynamicVar("Hits", 3),  // 升级 4
        new DynamicVar("ConceptGain", 1)  // 构想 +1，升级 +2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .Targeting(target)
            .WithHitCount(DynamicVars["Hits"].IntValue)
            .Execute(choiceContext);

        await ConceptCounterCapability.AddCountToAllInHand(choiceContext, Owner.Creature,
            DynamicVars["ConceptGain"].IntValue);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Hits"].UpgradeValueBy(1);
        DynamicVars["ConceptGain"].UpgradeValueBy(1);   // 构想 +1 -> +2
    }
}



/// <summary>
/// 伏笔回收：2 费技能（稀有）。将消耗牌堆的所有构想放入抽牌堆，消耗（升级：保留）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class ForeshadowRecovery : ModCardTemplate
{
    public ForeshadowRecovery() : base(2, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust, CardKeyword.Retain };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        if (player == null)
        {
            return;
        }

        var concepts = PileType.Exhaust.GetPile(player).Cards
            .Where(c => c is ConceptCard)
            .ToList();
        foreach (var card in concepts)
        {
            await CardPileCmd.Add(card, PileType.Draw, CardPilePosition.Top, this);
        }
    }

    protected override void OnUpgrade()
    {
        // 升级：费用 2 -> 1（保留升级前后都有，为关键词）。
        EnergyCost.UpgradeBy(-1);
    }
}

/// <summary>
/// 构想之矛：1 费能力（罕见）。当你打出构想时，该构想每有 1 点数值，就对所有敌人造成 8 点伤害 1 次（升级：11）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class ConceptSpear : ModCardTemplate
{
    public ConceptSpear() : base(1, CardType.Power, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：矛与盾（升级的构想之矛联动生成矛与盾+）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<SpearShield>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Damage", 11)  // 升级 15
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<ConceptSpearPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Damage"].UpgradeValueBy(4);   // 11 -> 15
    }
}

[RegisterPower]
public sealed class ConceptSpearPower : ModPowerTemplate
{
    private class Data
    {
        public int DamagePer = 0;  // 叠加后的每点构想伤害
        public bool Upgraded;       // 最近来源的升级状态（矛与盾的生成依据）
    }

    public override PowerType Type => PowerType.Buff;

    // 叠加：每多打出一张构想之矛，每点构想数值多造成对应伤害（升级 8/11）。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/concept_spear_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/concept_spear_power.png");

    protected override object InitInternalData() => new Data();

    // 右下角显示“实际造成的伤害”而不是叠加层数（本能力只有一个数值）。
    public override int DisplayAmount => GetInternalData<Data>().DamagePer;

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("DamagePer", 0)
    ];

    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        var data = GetInternalData<Data>();
        data.DamagePer += (int)amount * (cardSource?.IsUpgraded == true ? 15 : 11);
        data.Upgraded = cardSource?.IsUpgraded == true;
        DynamicVars["DamagePer"].BaseValue = data.DamagePer;
        InvokeDisplayAmountChanged();

        // 若已拥有构想之盾：立即生成并打出一张矛与盾（升级后的矛触发矛与盾+）。
        await MaybeSpawnSpearShield(choiceContext);
        await Task.CompletedTask;
    }

    // 拥有构想之盾时：生成并立即打出一张矛与盾（升级后的矛触发更强的：矛与盾+）。
    private async Task MaybeSpawnSpearShield(PlayerChoiceContext choiceContext)
    {
        if (!Owner.HasPower<ConceptShieldPower>())
        {
            return;
        }

        var combatState = Owner.CombatState;
        if (combatState == null || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var combo = combatState.CreateCard(ModelDb.Card<SpearShield>(), Owner.Player);
        if (GetInternalData<Data>().Upgraded)
        {
            CardCmd.Upgrade(combo, CardPreviewStyle.None);
        }

        await CardCmd.AutoPlay(choiceContext, combo, null);
    }

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card is not ConceptCard concept)
        {
            return;
        }

        if (CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var count = concept.GetOrCreateCapability<ConceptCounterCapability>().Count;
        if (count <= 0)
        {
            return;
        }

        var combatState = Owner.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 能力伤害走原版形状：直接 CreatureCmd.Damage + ValueProp.Unpowered。
        // （不吃力量/活力/虚弱/易伤，也不播攻击动画、不触发 BeforeAttack/AfterAttack —— 同原版 Panache/Juggernaut。）
        var damagePer = GetInternalData<Data>().DamagePer;
        for (var i = 0; i < count && !CombatManager.Instance.IsOverOrEnding; i++)
        {
            await CreatureCmd.Damage(choiceContext, combatState.HittableEnemies, damagePer,
                ValueProp.Unpowered, Owner, cardPlay.Card, null);
        }
    }
}

/// <summary>
/// 构想之盾：1 费能力（罕见）。回合结束时，手牌中每有一张构想就获得 6 点格挡（升级：8 + 固有）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class ConceptShield : ModCardTemplate
{
    public ConceptShield() : base(1, CardType.Power, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：矛与盾（升级的构想之盾联动生成矛与盾+）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<SpearShield>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Block", 6)  // 升级 8
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<ConceptShieldPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Block"].UpgradeValueBy(2);
    }
}

[RegisterPower]
public sealed class ConceptShieldPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 叠加：每多打出一张构想之盾，每张构想多获得对应格挡（升级 6/8）。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/concept_shield_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/concept_shield_power.png");

    private class Data
    {
        public int BlockPer = 0;  // 叠加后的每张构想格挡
        public bool Upgraded;       // 最近来源的升级状态（矛与盾的生成依据）
    }

    protected override object InitInternalData() => new Data();

    // 右下角显示“实际获得的格挡”而不是叠加层数（本能力只有一个数值）。
    public override int DisplayAmount => GetInternalData<Data>().BlockPer;

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("BlockPer", 0)
    ];

    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        var data = GetInternalData<Data>();
        data.BlockPer += (int)amount * (cardSource?.IsUpgraded == true ? 8 : 6);
        data.Upgraded = cardSource?.IsUpgraded == true;
        DynamicVars["BlockPer"].BaseValue = data.BlockPer;
        InvokeDisplayAmountChanged();

        // 若已拥有构想之矛：立即生成并打出一张矛与盾（升级后的盾触发矛与盾+）。
        await MaybeSpawnSpearShield(choiceContext);
        await Task.CompletedTask;
    }

    // 拥有构想之矛时：生成并立即打出一张矛与盾（升级后的盾触发更强的：矛与盾+）。
    private async Task MaybeSpawnSpearShield(PlayerChoiceContext choiceContext)
    {
        if (!Owner.HasPower<ConceptSpearPower>())
        {
            return;
        }

        var combatState = Owner.CombatState;
        if (combatState == null || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var combo = combatState.CreateCard(ModelDb.Card<SpearShield>(), Owner.Player);
        if (GetInternalData<Data>().Upgraded)
        {
            CardCmd.Upgrade(combo, CardPreviewStyle.None);
        }

        await CardCmd.AutoPlay(choiceContext, combo, null);
    }

    public override async Task AfterSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var player = Owner.Player;
        if (player == null)
        {
            return;
        }

        var conceptCount = PileType.Hand.GetPile(player).Cards.Count(c => c is ConceptCard);
        if (conceptCount <= 0)
        {
            return;
        }

        await CreatureCmd.GainBlock(Owner, new BlockVar(conceptCount * GetInternalData<Data>().BlockPer, ValueProp.Move), null);
    }
}

/// <summary>
/// 再启新篇：0 费技能（罕见）。虚无，获得 2 点活力；若手牌中没有构想，将 1 张构想加入手牌。这张牌的耗费+1（升级：3 活力、不再虚无）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class NewChapter : ModCardTemplate
{
    public NewChapter() : base(0, CardType.Skill, CardRarity.Common, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Vigor", 3),          // 升级 4
        new EnergyVar("CostIncrease", 1)     // 打出后本场战斗耗能+1（能量图标）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, DynamicVars["Vigor"].IntValue, Owner.Creature, this);

        var player = Owner.Creature.Player;
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
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Vigor"].UpgradeValueBy(1);
    }
}



/// <summary>
/// 矛与盾：0 费能力（衍生·Token）。构想之矛/构想之盾的联动衍生牌：
/// 打出构想时按数值获得格挡；回合结束时按手牌构想数对全体敌人造成伤害。升级数值提升。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class SpearShield : ModCardTemplate
{
    public SpearShield() : base(0, CardType.Power, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<SpearShieldPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
    }
}

[RegisterPower]
public sealed class SpearShieldPower : ModPowerTemplate
{
    private class Data
    {
        public int BlockPer = 0;   // 叠加后的每点构想格挡（基础 6、升级 8）
        public int DamagePer = 0;  // 叠加后的每张构想伤害（基础 11、升级 15）
        public CardModel? SourceCard;  // 攻击来源（FromCard 不能传 null）
    }

    public override PowerType Type => PowerType.Buff;

    // 无论升级前后都可叠加：叠加到获得的格挡量与造成的伤害量上。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/spear_shield_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/spear_shield_power.png");

    protected override object InitInternalData() => new Data();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("BlockPer", 0),
        new DynamicVar("DamagePer", 0)
    ];

    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        var data = GetInternalData<Data>();
        var upgraded = cardSource?.IsUpgraded == true;
        data.BlockPer += (int)amount * (upgraded ? 8 : 6);
        data.DamagePer += (int)amount * (upgraded ? 15 : 11);
        data.SourceCard ??= cardSource;
        DynamicVars["BlockPer"].BaseValue = data.BlockPer;
        DynamicVars["DamagePer"].BaseValue = data.DamagePer;
        await Task.CompletedTask;
    }

    // 当你打出构想时，该构想每有 1 点数值，就获得格挡。
    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card is not ConceptCard concept)
        {
            return;
        }

        if (CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var count = concept.GetOrCreateCapability<ConceptCounterCapability>().Count;
        if (count <= 0)
        {
            return;
        }

        await CreatureCmd.GainBlock(Owner, new BlockVar(count * GetInternalData<Data>().BlockPer, ValueProp.Move), null);
    }

    // 回合结束时，手牌中每有一张构想就对所有敌人造成伤害。
    public override async Task AfterSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var player = Owner.Player;
        var combatState = Owner.CombatState;
        if (player == null || combatState == null)
        {
            return;
        }

        var data = GetInternalData<Data>();
        var conceptCount = PileType.Hand.GetPile(player).Cards.Count(c => c is ConceptCard);
        var damagePer = data.DamagePer;
        if (conceptCount <= 0 || damagePer <= 0)
        {
            return;
        }

        var source = data.SourceCard;
        if (source == null)
        {
            return;  // 无来源卡时跳过（正常途径都会有矛与盾卡作为来源）
        }

        // 能力伤害走原版形状：直接 CreatureCmd.Damage + ValueProp.Unpowered。
        for (var i = 0; i < conceptCount && !CombatManager.Instance.IsOverOrEnding; i++)
        {
            await CreatureCmd.Damage(choiceContext, combatState.HittableEnemies, damagePer,
                ValueProp.Unpowered, Owner, source, null);
        }
    }
}
