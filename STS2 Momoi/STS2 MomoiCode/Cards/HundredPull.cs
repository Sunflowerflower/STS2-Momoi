using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 100连抽！：4 费攻击（罕见）。给予目标 1 层无实体 + 1 层虚弱，造成 1 点伤害 100 次，消耗，固有。
/// 升级：耗能 4 -> 3（固有升级前后都有）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class HundredPull : ModCardTemplate
{
    public HundredPull() : base(4, CardType.Attack, CardRarity.Rare, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 消耗 + 固有（升级前后都有固有）。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust, CardKeyword.Innate };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(1m),
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new RepeatVar(100)
    ];

    // 给予 1 层无实体、1 层虚弱，然后造成 1 点伤害 100 次。
    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        ArgumentNullException.ThrowIfNull(cardPlay.Target);

        await PowerCmd.Apply<IntangiblePower>(choiceContext, cardPlay.Target, 1, Owner.Creature, this);
        await PowerCmd.Apply<WeakPower>(choiceContext, cardPlay.Target, 1, Owner.Creature, this);

        using var whirlwind = MomoiVfx.PlayWhirlwind(DynamicVars.Repeat.IntValue, persistent: true);

        // 100 次伤害必须是**同一条** AttackCommand：拆成 100 条命令的话，
        // 活力/火力只会在第 1 条命令上生效（BeforeAttack 只记一次快照、AfterAttack 一次扣光），
        // 而且每条命令都会播一次攻击动画（卡到不能看）。用 WithHitCount + OnlyPlayAnimOnce 一次打完。
        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .Targeting(cardPlay.Target)
            .WithHitFx("vfx/vfx_giant_horizontal_slash")
            .WithHitCount(DynamicVars.Repeat.IntValue)
            .OnlyPlayAnimOnce()
            .Execute(choiceContext);
    }

    protected override void OnUpgrade()
    {
        // 升级：耗能 4 -> 3。
        EnergyCost.UpgradeBy(-1);
    }
}
