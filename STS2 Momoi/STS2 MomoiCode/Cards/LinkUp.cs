using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models.CardPools;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 连连看！：小游戏牌（Token 稀有度，图鉴杂项栏）。
/// 0 费技能，消耗 2 张手牌；若名称相同（升级不影响名称），摸 2 张牌并获得 1 点能量（升级 3 张 / 2 能量）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class LinkUp : ModCardTemplate
{
    public LinkUp() : base(0, CardType.Skill, CardRarity.Token, TargetType.None)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CardsVar(2),
        new EnergyVar(1)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 选择 2 张手牌消耗。
        var selected = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("card_selection", "STS2_MOMOI_LINKUP_HEADER"), 2),
            static _ => true, this)).ToList();

        if (selected.Count < 2)
        {
            return; // 取消选择：无事发生。
        }

        foreach (var card in selected)
        {
            await CardCmd.Exhaust(choiceContext, card);
        }

        // 名称相同（按卡牌 Id 比较，升级前后 Id 不变）→ 摸牌 + 能量。
        if (selected[0].Id == selected[1].Id)
        {
            await CardPileCmd.Draw(choiceContext, DynamicVars.Cards.IntValue, Owner);
            await PlayerCmd.GainEnergy(DynamicVars.Energy.IntValue, Owner);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.Cards.UpgradeValueBy(1);   // 摸 2 -> 3
        DynamicVars.Energy.UpgradeValueBy(1);  // 能量 1 -> 2
    }
}
