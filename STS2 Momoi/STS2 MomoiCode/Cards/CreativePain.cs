using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 创作的痛苦！：3 费攻击（罕见）。对所有敌人造成 6 点伤害 3 次，给予所有敌人 2 层灼烧。
/// 升级：6→8、灼烧 2→3。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class CreativePain : ModCardTemplate
{
    public CreativePain() : base(3, CardType.Attack, CardRarity.Uncommon, TargetType.AllEnemies)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(6m),  // 升级 7
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new DynamicVar("Burn", 3),   // 升级 5
        new EnergyVar("CostReduce", 1)  // 打出构想后下一次打出前耗能-1（能量图标）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        Audio.MomoiAudio.PlayVoice(Audio.MomoiSfx.CreativePain);
        Audio.MomoiAudio.PlaySfx(Audio.MomoiSfx.CreativePainImpact);
        using var whirlwind = MomoiVfx.PlayWhirlwind(3, persistent: true);
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 三段必须是**同一条** AttackCommand（WithHitCount(3)）：
        // 拆成 3 条命令的话，VigorPower.BeforeAttack 只给第一条命令记快照、AfterAttack 就把全部层数扣光，
        // 后两段只能吃残值（= 活力/火力被消耗多次且数值不对）。段间间隔用 WithWaitBeforeHit 表达。
        // 弹幕/命中特效走 MomoiGunStyle.ApplyBarrage 的 WithAttackerFx / WithHitVfxNode —— 每段各一次，
        // 所以不要加 OnlyPlayAnimOnce（那会把每段的弹幕也一起关掉）。
        await MomoiGunStyle.ApplyBarrage(
                DamageCmd.Attack(DynamicVars.CalculatedDamage)
                    .FromCard(this, cardPlay)
                    .TargetingAllOpponents(combatState)
                    .WithHitCount(3)
                    .WithWaitBeforeHit(0.5f, 0.5f),
                Owner.Creature,
                playGunshot: false)
            .Execute(choiceContext);

        // 给予所有敌人灼烧。
        foreach (var enemy in combatState.HittableEnemies)
        {
            await PowerCmd.Apply<BurnPower>(choiceContext, enemy,
                DynamicVars["Burn"].BaseValue, Owner.Creature, this);
        }
    }

    // 每当你打出构想时，此牌的耗能将在下一次打出前减少1c。
    public override async Task AfterCardPlayedLate(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner != Owner || cardPlay.Card is not ConceptCard)
        {
            return;
        }

        EnergyCost.AddUntilPlayed(-1, reduceOnly: true);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(1);   // 6 -> 7
        DynamicVars["Burn"].UpgradeValueBy(2);  // 灼烧 3 -> 5
    }
}
