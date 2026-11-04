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
/// 打击（战士版）：数值与卡图与原版一致，注册在本角色池（图鉴显示在本角色栏）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class STS2_MomoiStrike : ModCardTemplate
{
    public STS2_MomoiStrike() : base(1, CardType.Attack, CardRarity.Basic, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { CardTag.Strike };

    // 伤害显示完整预览（力量/活力/易伤等，Hook.ModifyDamage 管道）。
    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(6m),   // 升级 9
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        ArgumentNullException.ThrowIfNull(cardPlay.Target);

        await MomoiGunStyle.Apply(
                DamageCmd.Attack(DynamicVars.CalculatedDamage)
                    .FromCard(this, cardPlay)
                    .Targeting(cardPlay.Target),
                Owner.Creature)
            .Execute(choiceContext);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(3);
    }
}
