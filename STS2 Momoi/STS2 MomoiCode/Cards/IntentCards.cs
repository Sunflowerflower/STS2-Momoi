using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.MonsterMoves.Intents;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 针锋相对：2 费攻击（罕见）。造成 1 点伤害 2 次；如果敌人的意图是攻击，伤害增加敌人即将对你造成的伤害数。
/// 消耗（升级：2 伤，不再消耗）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class TitForTat : ModCardTemplate
{
    public TitForTat() : base(2, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(1m),   // 升级 2
        new ExtraDamageVar(1m),
        // 若敌人意图为攻击，额外伤害 = 敌人即将对你造成的伤害（实时显示）。
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((card, target) =>
        {
            if (target?.Monster is not { IntendsToAttack: true } monster)
            {
                return 0m;
            }

            return monster.NextMove.Intents
                .OfType<AttackIntent>()
                .Sum(i => i.GetTotalDamage(new[] { card.Owner.Creature }, monster.Creature));
        })
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
            .WithHitCount(2)
            .WithHitFx("vfx/vfx_molten_fist", null, "blunt_attack.mp3")
            .Execute(choiceContext);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(1);
        LocalKeywords.Remove(CardKeyword.Exhaust);
    }
}

/// <summary>
/// 对策：1 费技能（普通）。获得 5 点活力、给予 1 层易伤；若目标的意图包含攻击，改为获得 6 点格挡、给予 1 层虚弱
/// （升级：7 活力/2 易伤 → 8 格挡/2 虚弱）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Countermeasure : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public Countermeasure() : base(1, CardType.Skill, CardRarity.Common, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Vigor", 4),    // 升级 5
        new DynamicVar("Vuln", 1),     // 升级 2
        new BlockVar(6m, ValueProp.Move),    // 升级 8
        new DynamicVar("Weak", 1)      // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        if (target.Monster is { IntendsToAttack: true })
        {
            await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);
            await PowerCmd.Apply<WeakPower>(choiceContext, target, DynamicVars["Weak"].BaseValue, Owner.Creature, this);
        }
        else
        {
            await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, DynamicVars["Vigor"].BaseValue, Owner.Creature, this);
            await PowerCmd.Apply<VulnerablePower>(choiceContext, target, DynamicVars["Vuln"].BaseValue, Owner.Creature, this);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Vigor"].UpgradeValueBy(1);   // 4 -> 5
        DynamicVars["Vuln"].UpgradeValueBy(1);
        DynamicVars["Block"].UpgradeValueBy(2);
        DynamicVars["Weak"].UpgradeValueBy(1);
    }
}
