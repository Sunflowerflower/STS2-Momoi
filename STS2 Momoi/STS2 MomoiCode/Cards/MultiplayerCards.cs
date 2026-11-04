using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Powers;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Models.Capabilities;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 角色扮演！：2 费能力（稀有·多人·游戏牌）。回合开始时，将一张飞溅加入所有玩家的手牌，这张飞溅获得消耗。
/// 升级：固有 + 升级过的飞溅。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class RolePlay : ModCardTemplate
{
    public override CardMultiplayerConstraint MultiplayerConstraint => CardMultiplayerConstraint.MultiplayerOnly;

    public RolePlay() : base(2, CardType.Power, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");



    // 衍生牌预览：原版消耗侧栏（文本带“消耗”但牌本身不消耗）+ 飞溅。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromKeyword(CardKeyword.Exhaust),
        HoverTipFactory.FromCard<Splash>(IsUpgraded),
    ];

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.FullGameTag };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<RolePlayPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        LocalKeywords.Add(CardKeyword.Innate);
    }
}

[RegisterPower]
public sealed class RolePlayPower : ModPowerTemplate
{
    private class Data
    {
        public bool Upgraded;
    }

    public override PowerType Type => PowerType.Buff;

    // 不能叠加：每张角色扮演（无论是否升级）独立存在。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/role_play_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/role_play_power.png");

    protected override object InitInternalData() => new Data();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new StringVar("SplashName")
    ];

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        var upgraded = cardSource?.IsUpgraded == true;
        GetInternalData<Data>().Upgraded = upgraded;
        // 描述中的卡名随升级变化：飞溅 / 飞溅+。
        ((StringVar)DynamicVars["SplashName"]).StringValue = upgraded
            ? ModelDb.Card<Splash>().Title + "+"
            : ModelDb.Card<Splash>().Title;
        return Task.CompletedTask;
    }

    // 回合开始时，将 1 张飞溅（消耗）放入所有玩家的手牌。
    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var upgraded = GetInternalData<Data>().Upgraded;
        foreach (var player in combatState.Players)
        {
            var splash = combatState.CreateCard(ModelDb.Card<Splash>(), player);
            if (upgraded)
            {
                CardCmd.Upgrade(splash);
            }

            splash.LocalKeywords.Add(CardKeyword.Exhaust);
            await CardPileCmd.AddGeneratedCardToCombat(splash, PileType.Hand, player);
        }
    }
}

/// <summary>
/// 集思广益：1 费技能（稀有·多人）。保留；将 1 张构想加入所有盟友的手牌，
/// 这些构想的数值增加你当前构想的数值。消耗。升级：0 费。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class CollectiveWisdom : ModCardTemplate
{
    public override CardMultiplayerConstraint MultiplayerConstraint => CardMultiplayerConstraint.MultiplayerOnly;

    public CollectiveWisdom() : base(1, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Retain, CardKeyword.Exhaust };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 你当前构想数值（多张取最大值）。
        var myConcept = ConceptCounterCapability.GetMaxCountInHand(Owner.Creature);

        foreach (var ally in combatState.Players.Where(p => p != Owner))
        {
            var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), ally);
            concept.GetOrCreateCapability<ConceptCounterCapability>().SetCount(myConcept);
            await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, ally);
        }
    }

    protected override void OnUpgrade()
    {
        EnergyCost.UpgradeBy(-1);
    }
}
