using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Cards;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 集结：5 费技能（稀有）。将 5 张来自其他角色的特定牌放入你的手牌，这些牌本回合可以免费打出。
/// 本场战斗中每打出过一张支援牌，这张牌的耗费-1。消耗（升级：4 费、升级版）。
/// 5 张牌：坚定不移（战士）、墨之刃（静默）、既定事项（君主）、重构（死灵法师）、超能光束（机器人）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Rally : ModCardTemplate
{
    private static readonly Type[] ForeignCards =
    [
        typeof(Unmovable), typeof(BladeOfInk), typeof(ForegoneConclusion), typeof(Transfigure), typeof(Hyperbeam)
    ];

    // 隐藏效果（5%）：改为获得 5 张形态牌。
    private static readonly Type[] HiddenForms =
    [
        typeof(DemonForm), typeof(SerpentForm), typeof(VoidForm), typeof(ReaperForm), typeof(EchoForm)
    ];

    public Rally() : base(5, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar("CostReduce", 1)  // 每打出1张支援牌，此牌耗能-1（能量图标）
    ];

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    // 侧栏1：特定牌；侧栏2：支援牌。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_RALLY.sidebar1")),
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_RALLY.sidebar2"))
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 隐藏效果：5% 概率改为获得 5 张形态牌。
        var pool = Owner.RunState.Rng.CombatCardSelection.NextInt(100) < 5 ? HiddenForms : ForeignCards;

        foreach (var type in pool)
        {
            var card = combatState.CreateCard((CardModel)ModelDb.Get(type), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(card);
            }

            card.SetToFreeThisTurn();
            await CardPileCmd.AddGeneratedCardToCombat(card, PileType.Hand, Owner);
        }
    }

    // 本场战斗中每打出过一张支援牌，这张牌的耗能 -1（卡面实时显示）。
    //
    // 为什么不用 EnergyCost.AddThisCombat：
    //   它是往 _localModifiers 里**追加**一条相对修正，只在“进手牌/打出”那一刻算一次；
    //   之后又打出支援牌时卡面不会重算（就是“减费只生效一次”），而且进手牌 + 打出时会追加两次。
    //   用 TryModifyEnergyCostInCombat 每次读取时现算：无需状态、不会重复叠加，也不会在
    //   牌堆搬动过程中改模型状态（那个会引发换牌/刷新导致 Match3 里“already has a parent”的 UI 报错）。
    public override bool TryModifyEnergyCostInCombat(CardModel card, decimal originalCost, out decimal modifiedCost)
    {
        modifiedCost = originalCost;
        if (card != this || originalCost < 0m)
        {
            return false;
        }

        var reduction = CombatStats.SupportCardsPlayed;
        if (reduction <= 0)
        {
            return false;
        }

        modifiedCost = Math.Max(0m, originalCost - reduction);
        return modifiedCost != originalCost;
    }

    protected override void OnUpgrade()
    {
        EnergyCost.UpgradeBy(-1);
    }
}
