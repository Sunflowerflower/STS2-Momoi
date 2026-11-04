using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Helpers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Enchantments;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.Nodes.Cards;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using MegaCrit.Sts2.Core.Nodes.Vfx;
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
/// 激战：0 费攻击（罕见）。随机造成 3 点伤害 2 次，在本回合随机化你手牌中所有牌的耗能（升级：3 次）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class ConfusedShot : ModCardTemplate
{
    public ConfusedShot() : base(0, CardType.Attack, CardRarity.Uncommon, TargetType.RandomEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");


    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(2m),
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new DynamicVar("Hits", 2)  // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .TargetingRandomOpponents(combatState)
            .WithHitCount(DynamicVars["Hits"].IntValue)
            .Execute(choiceContext);

        // 随机化手牌中所有牌的耗能（0～3），参考蛇眼药水。
        var player = Owner.Creature.Player;
        if (player != null)
        {
            foreach (var card in PileType.Hand.GetPile(player).Cards.Where(c => !c.EnergyCost.CostsX))
            {
                if (card.EnergyCost.GetWithModifiers(CostModifiers.None) >= 0)
                {
                    card.EnergyCost.SetThisTurnOrUntilPlayed(Owner.RunState.Rng.CombatEnergyCosts.NextInt(4));
                    NCard.FindOnTable(card)?.PlayRandomizeCostAnim();
                }
            }
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Hits"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 来自勇者的加护：0 费攻击（罕见·支援牌）。打出时对所有敌人造成伤害（机器人超能光束动画）；
/// 你每打出一张小游戏牌（含游戏牌），就将这张牌放入你的手牌（不在手牌时）并使其最终伤害翻倍，耗能+1。
/// 伤害翻倍为最终伤害倍数（参考亡灵契约师的吊杀），卡面显示即将造成的伤害。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class CourageBoon : ModCardTemplate
{
    // 每打出一张小游戏牌 ×2（最终伤害倍数）。
    private decimal _finalMultiplier = 1m;

    public CourageBoon() : base(0, CardType.Attack, CardRarity.Rare, TargetType.AllEnemies)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.SupportTag };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(6m),   // 升级 11
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new EnergyVar("CostIncrease", 1)  // 耗能+1（能量图标）
    ];

    // 最终伤害倍数（吊杀同款）：本卡自己的攻击在结算时乘以倍率；卡面预览也走同一管道。
    public override decimal ModifyDamageMultiplicative(Creature? target, decimal amount, ValueProp props,
        Creature? dealer, CardModel? cardSource, CardPlay? cardPlay)
    {
        if (cardSource != this)
        {
            return 1m;
        }

        return _finalMultiplier;
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 机器人超能光束动画（参考原版超能光束）。
        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .TargetingAllOpponents(combatState)
            .BeforeDamage(async () =>
            {
                var enemies = combatState.Enemies.Where(e => e.IsAlive).ToList();
                if (enemies.Count == 0)
                {
                    return;
                }

                var beam = NHyperbeamVfx.Create(Owner.Creature, enemies.Last());
                if (beam != null)
                {
                    NCombatRoom.Instance?.CombatVfxContainer.AddChildSafely(beam);
                    await Cmd.Wait(0.5f);
                }

                foreach (var enemy in enemies)
                {
                    var impact = NHyperbeamImpactVfx.Create(Owner.Creature, enemy);
                    if (impact != null)
                    {
                        NCombatRoom.Instance?.CombatVfxContainer.AddChildSafely(impact);
                    }
                }
            })
            .Execute(choiceContext);
    }

    // 每打出一张小游戏牌（含游戏牌）结算一次：不在手牌→放入手牌；最终伤害翻倍；耗能+1（两个效果独立，都触发）。
    public override async Task AfterCardPlayedLate(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner != Owner || !MinigameSupport.IsMinigameCard(cardPlay.Card))
        {
            return;
        }

        if (Pile != null && Pile.Type != PileType.Hand)
        {
            await CardPileCmd.Add(this, PileType.Hand);
        }

        _finalMultiplier *= 2;
        EnergyCost.AddThisCombat(1);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(3);   // 6 -> 9
    }
}





/// <summary>
/// 开发秘籍：3 费能力（稀有）。打出小游戏牌时使构想升级，数值+1（升级：+2，可叠加）；
/// 你每打出一张小游戏牌，这张牌的耗能就减少1（卡牌自带效果）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class DevSecrets : ModCardTemplate
{
    public DevSecrets() : base(3, CardType.Power, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar("CostReduce", 1)  // 每打出1张小游戏牌，此牌耗能-1（能量图标）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<DevSecretsPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    // 卡牌自带效果：每打出一张小游戏牌，这张牌的耗能减少 1。
    public override async Task AfterCardPlayedLate(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner != Owner || !MinigameSupport.IsMinigameCard(cardPlay.Card))
        {
            return;
        }

        EnergyCost.AddThisCombat(-1, reduceOnly: true);
    }

    protected override void OnUpgrade()
    {
    }
}

[RegisterPower]
public sealed class DevSecretsPower : ModPowerTemplate
{
    private class DevSecretsData
    {
        public int GainPerMinigame = 0;  // 叠加后的构想数值增加量
    }

    protected override object InitInternalData() => new DevSecretsData();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Gain", 0)
    ];

    // 右下角显示的是「每打出 1 张小游戏牌使构想增加的数值」（= Gain），不是叠加层数。
    public override int DisplayAmount => (int)DynamicVars["Gain"].BaseValue;

    public override PowerType Type => PowerType.Buff;

    // 构想数值 +1 可叠加（升级前 +1、升级后 +2）。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/dev_secrets_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/dev_secrets_power.png");

    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        var data = GetInternalData<DevSecretsData>();
        data.GainPerMinigame += (int)amount * (cardSource?.IsUpgraded == true ? 2 : 1);
        DynamicVars["Gain"].BaseValue = data.GainPerMinigame;
        InvokeDisplayAmountChanged();
        await Task.CompletedTask;
    }

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || !MinigameSupport.IsMinigameCard(cardPlay.Card))
        {
            return;
        }

        if (CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        // 打出小游戏牌：使构想升级，数值 +叠加值。
        var player = Owner.Player;
        if (player != null)
        {
            foreach (var card in PileType.Hand.GetPile(player).Cards.ToList())
            {
                if (card is ConceptCard concept)
                {
                    CardCmd.Upgrade(concept);
                    concept.GetOrCreateCapability<ConceptCounterCapability>().AddCount(GetInternalData<DevSecretsData>().GainPerMinigame);
                    NCombatRoom.Instance?.Ui.Hand?.GetCard(card)?.UpdateVisuals(PileType.Hand, CardPreviewMode.Normal);
                }
            }
        }
    }
}

/// <summary>
/// 日复一日，必有精进：4 费能力（罕见）。生成构想时，立即使其数值+1（可叠加）；
/// 你每打出过 1 次构想，这张牌的耗能-1（升级 -2，卡牌自带效果）。升级：保留。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class LearnByDoing : ModCardTemplate
{
    public LearnByDoing() : base(3, CardType.Power, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 保留升级前后都有（放进 CanonicalKeywords，升级时不再重复添加 → 不会出现两个「保留」）。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Retain };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar("CostReduce", 1)  // 每打出1次构想，此牌耗能-1（升级-2，能量图标）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<LearnByDoingPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    // 卡牌自带效果：每打出过 1 次构想，这张牌的耗能减 1（升级 2）。
    public override async Task AfterCardPlayedLate(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner != Owner || cardPlay.Card is not ConceptCard)
        {
            return;
        }

        EnergyCost.AddThisCombat(-(IsUpgraded ? 2 : 1), reduceOnly: true);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["CostReduce"].UpgradeValueBy(1);
    }
}

[RegisterPower]
public sealed class LearnByDoingPower : ModPowerTemplate
{
    private class LearnData
    {
        public int GainOnGenerate = 0;  // 叠加后的生成构想数值增加量
    }

    protected override object InitInternalData() => new LearnData();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Gain", 0)
    ];

    public override PowerType Type => PowerType.Buff;

    // 生成构想时数值 +1 可叠加。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/learn_by_doing_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/learn_by_doing_power.png");

    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        var data = GetInternalData<LearnData>();
        data.GainOnGenerate += (int)amount;
        DynamicVars["Gain"].BaseValue = data.GainOnGenerate;
        await Task.CompletedTask;
    }

    // 生成构想时立即使其数值加 1：新生成的构想（从战斗外直接进手牌）计数 +叠加值。
    public override async Task AfterCardChangedPiles(CardModel card, PileType oldPileType, AbstractModel? clonedBy)
    {
        if (card is not ConceptCard concept || card.Owner?.Creature != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        if (oldPileType != PileType.None || card.Pile?.Type != PileType.Hand)
        {
            return;
        }

        concept.GetOrCreateCapability<ConceptCounterCapability>().AddCount(GetInternalData<LearnData>().GainOnGenerate);
        NCombatRoom.Instance?.Ui.Hand?.GetCard(card)?.UpdateVisuals(PileType.Hand, CardPreviewMode.Normal);
    }
}

/// <summary>
/// 相遇：2 费技能（稀有）。获得 9 点格挡，将 1 张随机小游戏牌加入手牌；
/// 本场战斗中所有相遇共享解锁进度，每打出一次解锁一个新效果（墨影小刀→铸造→随机充能球+充能球栏位），最多 3 次。
/// 升级：12 格挡、升级过的小游戏牌、2 墨影小刀、铸造11、2 充能球+2 栏位。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Encounter : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public Encounter() : base(1, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(6m, ValueProp.Move)  // 升级 7
    ];

    // 侧栏：生成（充能球）/铸造（参考原版电击、战火铸就）+ 墨影（参考原版墨之刃）
    //      + 衍生牌预览：小刀、君王之剑。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.Static(StaticHoverTip.Channeling),
        .. HoverTipFactory.FromForge(),
        .. HoverTipFactory.FromEnchantment<Inky>(),
        HoverTipFactory.FromCard<Shiv>(),
        HoverTipFactory.FromCard<SovereignBlade>()
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 所有相遇（无论升级与否）共享解锁进度。
        var stage = CombatStats.RecordEncounterPlay();

        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);

        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 第 1 个新效果：墨影小刀（小刀+墨影附魔；升级 2 张）。
        if (stage >= 2)
        {
            var count = IsUpgraded ? 2 : 1;
            foreach (var shiv in await Shiv.CreateInHand(Owner, count, combatState))
            {
                CardCmd.Enchant<Inky>(shiv, 1m);
            }
        }

        // 第 2 个新效果：铸造 7（升级 11）。
        if (stage >= 3)
        {
            await ForgeCmd.Forge(IsUpgraded ? 11 : 7, Owner, this);
        }

        // 第 3 个新效果：生成 1 个随机充能球并获得 1 个充能球栏位（升级 2 个/2 栏位）。
        if (stage >= 4)
        {
            var orbs = IsUpgraded ? 2 : 1;
            await OrbCmd.AddSlots(Owner, orbs);
            for (int i = 0; i < orbs; i++)
            {
                await OrbCmd.Channel(choiceContext,
                    OrbModel.GetRandomOrb(Owner.RunState.Rng.CombatOrbGeneration).ToMutable(), Owner);
            }
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Block"].UpgradeValueBy(1);   // 6 -> 7
    }
}

/// <summary>
/// 友谊对决：1 费技能（罕见·游戏牌）。从 2 张特定牌（WIN！/LOSE！）中随机获得 1 张；
/// 活力越接近 7，赢面越大（活力=7 时 100% 获得 WIN！，每相差 1 点降低 10%，最低 0%）。
/// 升级：获得升级过的特定牌。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class FriendlyDuel : ModCardTemplate
{
    public FriendlyDuel() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.FullGameTag };

    // 衍生牌预览：WIN！/LOSE！。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<WinCard>(IsUpgraded),
        HoverTipFactory.FromCard<LoseCard>(IsUpgraded),
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 赢面 = 100% - |活力-7|×10%，最低 0%。
        var vigor = Owner.Creature.GetPower<VigorPower>()?.Amount ?? 0;
        var chance = Math.Clamp(100 - Math.Abs(vigor - 7) * 10, 0, 100);
        var roll = Owner.RunState.Rng.CombatCardSelection.NextInt(100);

        var rewardType = roll < chance ? typeof(WinCard) : typeof(LoseCard);
        var reward = combatState.CreateCard((CardModel)ModelDb.Get(rewardType), Owner);
        if (IsUpgraded)
        {
            CardCmd.Upgrade(reward);
        }

        await CardPileCmd.AddGeneratedCardToCombat(reward, PileType.Hand, Owner);
    }

    protected override void OnUpgrade()
    {
    }
}

/// <summary>
/// WIN！：0 费技能（衍生）。获得 4c，本回合剩余的能量可以留到下一回合。消耗（升级：6c）。
/// </summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class WinCard : ModCardTemplate
{
    public WinCard() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar(3)  // 升级 4
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PlayerCmd.GainEnergy(DynamicVars["Energy"].IntValue, Owner);
        // 本回合剩余的能量可以留到下一回合。
        await PowerCmd.Apply<WinEnergyPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Energy"].UpgradeValueBy(1);   // 3 -> 4
    }
}

/// <summary>
/// WIN！的能量保留：接下来 Amount 个回合，剩余能量留到下一回合。
/// 可叠加（叠层数 = 剩余生效回合数），右下角显示剩余回合数。
/// 实现细节：
///   * 真正“保留”靠的是 ShouldPlayerResetEnergy 拦住下个回合开始时的能量重置；
///   * 层数在**己方回合结束时** -1（无论有没有剩余能量）；
///   * 但 0 层时**不能立刻移除** —— 还要让它挡住下个回合开始的重置，
///     所以移除放在 AfterSideTurnStart（先拦截、后移除）。
/// </summary>
[RegisterPower]
public sealed class WinEnergyPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 可叠加：层数 = 剩余生效回合数。
    public override PowerStackType StackType => PowerStackType.Counter;

    // 右下角显示剩余生效回合数。
    public override int DisplayAmount => Amount;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/win_energy_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/win_energy_power.png");

    // 阻止能量重置（剩余能量留到下一回合）。
    public override bool ShouldPlayerResetEnergy(Player player) => player != Owner.Player;

    public override async Task AfterSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        // 回合结束计数 -1。用 SetAmount 而不是 TickDownDuration：
        // 0 层时不能立刻移除（还要挡住下个回合开始的重置）。
        SetAmount(Math.Max(0, Amount - 1));
    }

    public override Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants,
        ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner))
        {
            return Task.CompletedTask;
        }

        // 这一次能量重置已经被拦下了 → 没剩下回合数就移除。
        if (Amount <= 0)
        {
            return RemoveSelf();
        }

        return Task.CompletedTask;
    }

    private async Task RemoveSelf() => await PowerCmd.Remove(this);
}

/// <summary>
/// LOSE！：0 费技能（衍生）。获得 3 点活力，将一张创作的痛苦加入你的手牌。消耗（升级：5 活力、创作的痛苦+）。
/// </summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class LoseCard : ModCardTemplate
{
    public LoseCard() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    // 衍生牌预览：创作的痛苦。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<CreativePain>(IsUpgraded)
    ];

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Vigor", 2)  // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, DynamicVars["Vigor"].BaseValue, Owner.Creature, this);

        var combatState = Owner.Creature.CombatState;
        if (combatState != null)
        {
            var pain = combatState.CreateCard(ModelDb.Card<CreativePain>(), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(pain);
            }

            await CardPileCmd.AddGeneratedCardToCombat(pain, PileType.Hand, Owner);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Vigor"].UpgradeValueBy(1);   // 2 -> 3
    }
}





/// <summary>
/// 白与黑：1 费技能（稀有）。从两张牌中选择一张加入你的手牌；选择后将删去另一个选项，
/// 后续所有相同牌名的牌改为直接将选择的牌放入手牌（整局游戏继承）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class WhiteAndBlack : ModCardTemplate
{
    private static readonly Type[] Options = [typeof(ShowMyStrength), typeof(BigSister)];

    public WhiteAndBlack() : base(1, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：见识下我的实力吧、大姐头。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<ShowMyStrength>(IsUpgraded),
        HoverTipFactory.FromCard<BigSister>(IsUpgraded)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 若本场战斗已选择过，直接生成所选牌（战斗结束恢复两个选项）。
        if (CombatStats.WhiteBlackChoice != null)
        {
            var chosenType = CombatStats.WhiteBlackChoice == nameof(ShowMyStrength) ? typeof(ShowMyStrength) : typeof(BigSister);
            var chosen = combatState.CreateCard((CardModel)ModelDb.Get(chosenType), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(chosen);
            }

            await CardPileCmd.AddGeneratedCardToCombat(chosen, PileType.Hand, Owner);
            return;
        }

        var cards = Options
            .Select(t => combatState.CreateCard((CardModel)ModelDb.Get(t), Owner))
            .ToList();
        if (IsUpgraded)
        {
            foreach (var c in cards)
            {
                CardCmd.Upgrade(c);
            }
        }

        var picked = await CardSelectCmd.FromChooseACardScreen(choiceContext, cards, Owner);
        if (picked != null)
        {
            // 本场战斗内继承：后续同名牌直接给所选。
            CombatStats.WhiteBlackChoice = picked is ShowMyStrength ? nameof(ShowMyStrength) : nameof(BigSister);
            await CardPileCmd.AddGeneratedCardToCombat(picked, PileType.Hand, Owner);
        }
    }

    protected override void OnUpgrade()
    {
    }
}

/// <summary>见识下我的实力吧：1 费能力（衍生，升级 0 费）。获得 1 点力量；每打出 10 张牌，获得 1c（升级 2c）。
/// 多次打出时力量叠加，每打出 10 张牌获得能量各自独立（参考自动化显示倒计时）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class ShowMyStrength : ModCardTemplate
{
    public ShowMyStrength() : base(0, CardType.Power, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Strength", 1),  // 升级 2
        new EnergyVar(1)     // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<StrengthPower>(choiceContext, Owner.Creature, DynamicVars["Strength"].BaseValue, Owner.Creature, this);
        await PowerCmd.Apply<ShowMyStrengthPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Strength"].UpgradeValueBy(1);
        DynamicVars["Energy"].UpgradeValueBy(1);
        // 费用升级前后都是 0。
    }
}

[RegisterPower]
public sealed class ShowMyStrengthPower : ModPowerTemplate
{
    private class ShowData
    {
        public int CardsLeft = 10;  // 再打出几张牌就获得能量（自动化同款倒计时）
        public int Energy = 1;      // 升级 2
    }

    public override PowerType Type => PowerType.Buff;

    // 每张独立生效（各自计算 10 张倒计时）。Counter + Instanced：图标数字显示倒计时（参考原版神气制胜）。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/show_my_strength_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/show_my_strength_power.png");

    // 图标数字显示倒计时（参考自动化）。
    public override int DisplayAmount => GetInternalData<ShowData>().CardsLeft;

    protected override object InitInternalData() => new ShowData();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar("EnergyPer", 1),
        new DynamicVar("Countdown", 10)
    ];

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        var data = GetInternalData<ShowData>();
        data.Energy = cardSource?.IsUpgraded == true ? 2 : 1;
        DynamicVars["EnergyPer"].BaseValue = data.Energy;
        DynamicVars["Countdown"].BaseValue = data.CardsLeft;
        return Task.CompletedTask;
    }

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        // 每打出 10 张牌，获得 1c。
        var data = GetInternalData<ShowData>();
        data.CardsLeft--;
        DynamicVars["Countdown"].BaseValue = data.CardsLeft;
        InvokeDisplayAmountChanged();
        if (data.CardsLeft <= 0)
        {
            data.CardsLeft = 10;
            DynamicVars["Countdown"].BaseValue = data.CardsLeft;
            await PlayerCmd.GainEnergy(data.Energy, Owner.Player);
            InvokeDisplayAmountChanged();
        }
    }
}

/// <summary>大姐头：1 费技能（衍生）。选择 1 张手牌复制；复制出的牌本回合耗能减少 1（升级：免费）。保留、消耗。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class BigSister : ModCardTemplate
{
    public BigSister() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 保留（升级前后都有）+ 消耗。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Retain, CardKeyword.Exhaust };

    // 复制品本回合的减费数值（仅用于文本显示：未升级 1，升级改为免费）。
    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar("CostReduce", 1)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        if (player == null)
        {
            return;
        }

        var picked = (await CardSelectCmd.FromHand(choiceContext, player,
            new CardSelectorPrefs(new LocString("card_selection", "TO_CLONE"), 1, 1), null, this)).FirstOrDefault();
        if (picked != null)
        {
            // 保留升级状态的复制品。
            var clone = picked.CreateClone();

            if (IsUpgraded)
            {
                // 升级：复制出的牌本回合可以免费打出。
                clone.SetToFreeThisTurn();
            }
            else
            {
                // 未升级：复制出的牌本回合耗能减少 1。
                clone.EnergyCost.AddUntilPlayed(-1);
            }

            await CardPileCmd.AddGeneratedCardToCombat(clone, PileType.Hand, player);
        }
    }

    protected override void OnUpgrade()
    {
    }
}

/// <summary>
/// 开发者协同：绿：0 费能力（罕见·支援牌）。注能：每场战斗开始时自动打出。
/// 获得 1 点敏捷；回合开始时获得 1 点活力（升级：2 敏捷、2 活力）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class DevGreen : ModCardTemplate, IImbuedCard
{
    public DevGreen() : base(0, CardType.Power, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.SupportTag };

    // 侧栏：「注能」的解释（和循环叙事共用同一条词条）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [ImbuedSupport.ImbuedTip];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Dex", 1),   // 升级 2
        new DynamicVar("Vigor", 1)  // 升级 2
    ];

    // 注能是否已经打出过（每张牌每场战斗只算一次；同名牌各自一次）。
    private bool _imbuedApplied;

    // 「注能」：第 1 回合开局自动打出（和原版 Imbued 附魔一样走 CardCmd.AutoPlay）。
    // 置底由 Patches/MomoiImbuedDrawPilePatch.cs 在第 1 回合抽牌前处理，
    // 所以不会出现「开局抽到这张牌 = 少抽一张」。
    // 注：曾经为了绕开「抓两张时开局卡 30 秒」改成直接结算，但在能稳定复现前先回退成正常的自动打出。
    public override async Task AfterAutoPrePlayPhaseEntered(PlayerChoiceContext choiceContext, Player player)
    {
        if (_imbuedApplied || !ImbuedSupport.CanAutoPlayNow(player, this))
        {
            return;
        }

        _imbuedApplied = true;
        await ImbuedSupport.TryAutoPlayAsync(choiceContext, this, nameof(DevGreen));
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<DexterityPower>(choiceContext, Owner.Creature, DynamicVars["Dex"].BaseValue, Owner.Creature, this);
        // 回合开始时获得 1 点活力（升级 2），可叠加。
        await PowerCmd.Apply<DevGreenPower>(choiceContext, Owner.Creature,
            IsUpgraded ? 2 : 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Dex"].UpgradeValueBy(1);
        DynamicVars["Vigor"].UpgradeValueBy(1);
    }
}

[RegisterPower]
public sealed class DevGreenPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 叠加：每打出一张开发者协同：绿，回合开始多获得 1 点活力。
    public override PowerStackType StackType => PowerStackType.Counter;

    // 右下角显示的就是「回合开始时获得的活力」（= Amount；叠加层数与获得量本来就是同一个数）。
    public override int DisplayAmount => Amount;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/dev_green_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/dev_green_power.png");

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        await PowerCmd.Apply<VigorPower>(new ThrowingPlayerChoiceContext(), Owner, Amount, Owner, null);
    }
}
