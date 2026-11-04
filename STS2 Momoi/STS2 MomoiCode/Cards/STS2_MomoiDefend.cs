using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 防御（战士版）：数值与卡图与原版一致，注册在本角色池（图鉴显示在本角色栏）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class STS2_MomoiDefend : ModCardTemplate
{
    public STS2_MomoiDefend() : base(1, CardType.Skill, CardRarity.Basic, TargetType.Self)
    {
    }

    // 直接用原版战士卡图。
    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { CardTag.Defend };

    public override bool GainsBlock => true;

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(5, ValueProp.Move)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);
    }

    protected override void OnUpgrade()
    {
        // 与原版战士防御一致：5 -> 8。
        DynamicVars.Block.UpgradeValueBy(3);
    }
}
