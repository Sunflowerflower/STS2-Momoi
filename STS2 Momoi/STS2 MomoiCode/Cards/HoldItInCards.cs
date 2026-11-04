using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 「绷住」链：把下一张衍生牌加入手牌。
/// 来源牌升级时加入升级版，否则加入基础版。
/// </summary>
internal static class HoldItInChain
{
    public static async Task AddNext<T>(Player owner, bool upgraded) where T : CardModel
    {
        var combatState = owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var card = combatState.CreateCard(ModelDb.Card<T>(), owner);
        if (upgraded)
        {
            CardCmd.Upgrade(card);
        }

        await CardPileCmd.AddGeneratedCardToCombat(card, PileType.Hand, owner);
    }
}

/// <summary>
/// 严肃绷住：0 费技能（普通）。获得 4 点格挡，将一张「绷到我了」加入你的手牌。
/// 升级：6 点格挡，改为加入「绷到我了+」。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class SeriousFace : ModCardTemplate
{
    public SeriousFace() : base(0, CardType.Skill, CardRarity.Common, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override bool GainsBlock => true;

    // 侧栏预览被加入的衍生牌（按本牌是否升级显示对应版本）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<ItCrackedMe>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(4, ValueProp.Move)   // 升级 6
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);
        await HoldItInChain.AddNext<ItCrackedMe>(Owner, IsUpgraded);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.Block.UpgradeValueBy(2);
    }
}

/// <summary>
/// 绷到我了：0 费技能（衍生）。失去 1 点生命，获得 5 点格挡，将一张「轻松绷住」加入你的手牌。
/// 升级：7 点格挡，改为加入「轻松绷住+」。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class ItCrackedMe : ModCardTemplate
{
    public ItCrackedMe() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override bool GainsBlock => true;

    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<HoldingItEasy>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new HpLossVar(2m),
        new BlockVar(6, ValueProp.Move)   // 升级 8
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 失去生命：与原版放血一致（不可格挡、不受能力修正）。
        await CreatureCmd.Damage(choiceContext, Owner.Creature, DynamicVars.HpLoss.BaseValue,
            ValueProp.Unblockable | ValueProp.Unpowered | ValueProp.Move, this, cardPlay);
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);
        await HoldItInChain.AddNext<HoldingItEasy>(Owner, IsUpgraded);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.Block.UpgradeValueBy(2);
    }
}

/// <summary>
/// 轻松绷住：0 费技能（衍生）。获得 2 点格挡，抽 1 张牌，本回合内不能再抽牌，
/// 将一张「我还能绷五万年呢」加入你的手牌。升级：3 点格挡，改为加入「我还能绷五万年呢+」。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class HoldingItEasy : ModCardTemplate
{
    public HoldingItEasy() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override bool GainsBlock => true;

    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<FiftyThousandYears>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(2, ValueProp.Move),   // 升级 3
        new CardsVar(1)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);
        await CardPileCmd.Draw(choiceContext, DynamicVars.Cards.BaseValue, Owner);
        // 本回合内不能再抽牌：与原版战斗专注一致（抽完再上限制）。
        await PowerCmd.Apply<NoDrawPower>(choiceContext, Owner.Creature, 1m, Owner.Creature, this);
        await HoldItInChain.AddNext<FiftyThousandYears>(Owner, IsUpgraded);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.Block.UpgradeValueBy(1);
    }
}

/// <summary>
/// 我还能绷五万年呢：1 费技能（衍生·虚无）。获得 5 点格挡，在下个回合获得 5 点格挡，结束你的回合。
/// 升级：7 点格挡（下个回合同样 7 点）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class FiftyThousandYears : ModCardTemplate
{
    public FiftyThousandYears() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override bool GainsBlock => true;

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Ethereal };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(4, ValueProp.Move)   // 升级 6
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var amount = await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);
        // 下个回合的格挡：与原版闪躲翻滚一致（BlockNextTurnPower 可叠加）。
        await PowerCmd.Apply<BlockNextTurnPower>(choiceContext, Owner.Creature, amount, Owner.Creature, this);
        PlayerCmd.EndTurn(Owner, canBackOut: false);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.Block.UpgradeValueBy(2);
    }
}
