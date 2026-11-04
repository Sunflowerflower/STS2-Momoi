using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Hooks;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 火力打击：1 费攻击（普通）。造成 6 点伤害；本场战斗中你每获得过 1 层火力，伤害+3（升级：8 伤、+4）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class FirepowerStrike : ModCardTemplate
{
    public FirepowerStrike() : base(1, CardType.Attack, CardRarity.Common, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 原版「完美打击」同款：基础 6 + 每层火力累计 3；伤害由攻击命令统一结算（力量/活力/易伤只算一次），
    // 卡面 {CalculatedDamage:diff()} 自动显示完整加成后的预览值。
    protected override IEnumerable<DynamicVar> CanonicalVars
    {
        get
        {
            var gainedBase = new DynamicVar("FirepowerGainedBase", 0m);
            var gainedExtra = new DynamicVar("FirepowerGainedExtra", 1m);
            return
            [
                new CalculationBaseVar(6m),   // 升级 8
                new ExtraDamageVar(3m),       // 升级 4
                new CalculatedDamageVar(ValueProp.Move)
                    .WithMultiplier((_, _) => CombatStats.TotalFirepowerGained),
                gainedBase,
                gainedExtra,
                // 本场已获得过的火力层数（实时显示）。
                new IndependentCalculatedVar("FirepowerGained", gainedBase, gainedExtra)
                    .WithMultiplier((_, _) => CombatStats.TotalFirepowerGained)
            ];
        }
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        await MomoiGunStyle.Apply(
                DamageCmd.Attack(DynamicVars.CalculatedDamage)
                    .FromCard(this, cardPlay)
                    .Targeting(target),
                Owner.Creature)
            .Execute(choiceContext);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(2);
        DynamicVars.ExtraDamage.UpgradeValueBy(1);
    }
}

/// <summary>
/// 火焰子弹：1 费攻击（普通）。造成 7 点伤害，给予 2 层灼烧；每有 2 点活力，额外给予 1 层灼烧（升级：9 伤、3 层）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class FlameBullet : ModCardTemplate
{
    public FlameBullet() : base(1, CardType.Attack, CardRarity.Common, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars
    {
        get
        {
            var burnBase = new DynamicVar("BurnBase", 3m);   // 升级 4
            var burnExtra = new DynamicVar("BurnExtra", 1m);
            return
            [
                new CalculationBaseVar(6m),   // 升级 8
                new ExtraDamageVar(0m),
                new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
                burnBase,
                burnExtra,
                // 灼烧层数 = 基础 + 每 1 点活力 +1（实时显示）。
                new IndependentCalculatedVar("CalculatedBurn", burnBase, burnExtra).WithMultiplier((card, _) =>
                {
                    var vigor = card.Owner.Creature.GetPower<VigorPower>();
                    return vigor != null ? vigor.Amount : 0;
                })
            ];
        }
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        // 先读活力算灼烧（攻击后活力可能被消耗/保留，必须攻击前计算）。
        var burn = Convert.ToInt32(DynamicVars["CalculatedBurn"]);

        await MomoiGunStyle.Apply(
                DamageCmd.Attack(DynamicVars.CalculatedDamage)
                    .FromCard(this, cardPlay)
                    .Targeting(target)
                    .BeforeDamage(() =>
                    {
                        MomoiVfx.PlayFiendFire(target);
                        return Task.CompletedTask;
                    }),
                Owner.Creature)
            .Execute(choiceContext);

        if (burn > 0)
        {
            await PowerCmd.Apply<BurnPower>(choiceContext, target, burn, Owner.Creature, this);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(2);
        DynamicVars["BurnBase"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 活力打击：0 费攻击（普通）。对随机敌人造成 2 点伤害 2 次，获得 2 点活力（升级：3 伤、3 活力）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class VigorStrike : ModCardTemplate
{
    public VigorStrike() : base(0, CardType.Attack, CardRarity.Common, TargetType.RandomEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(2m),   // 升级 3
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new DynamicVar("Vigor", 2)  // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        await MomoiGunStyle.Apply(
                DamageCmd.Attack(DynamicVars.CalculatedDamage)
                    .FromCard(this, cardPlay)
                    .TargetingRandomOpponents(combatState)
                    .WithHitCount(2),
                Owner.Creature)
            .Execute(choiceContext);

        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature,
            DynamicVars["Vigor"].BaseValue, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(1);
        DynamicVars["Vigor"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 整装待发：1 费技能（普通）。获得 8 点格挡、1 点活力、1 层火力（升级：10 格挡、2 活力、2 火力）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class GearUp : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public GearUp() : base(1, CardType.Skill, CardRarity.Common, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(4m, ValueProp.Move),    // 升级 6
        new DynamicVar("Vigor", 2),    // 升级 3
        new DynamicVar("Firepower", 2) // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);
        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, DynamicVars["Vigor"].BaseValue, Owner.Creature, this);
        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature, DynamicVars["Firepower"].BaseValue, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Block"].UpgradeValueBy(2);
        DynamicVars["Vigor"].UpgradeValueBy(1);
        DynamicVars["Firepower"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 预热：0 费技能（普通）。获得 1 层火力，给予 1 层易伤（升级：2/2）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class WarmUp : ModCardTemplate
{
    public WarmUp() : base(0, CardType.Skill, CardRarity.Common, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Firepower", 2),  // 升级 3
        new DynamicVar("Vulnerable", 1)  // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature, DynamicVars["Firepower"].BaseValue, Owner.Creature, this);

        var target = cardPlay.Target;
        if (target != null)
        {
            await PowerCmd.Apply<VulnerablePower>(choiceContext, target, DynamicVars["Vulnerable"].BaseValue, Owner.Creature, this);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Firepower"].UpgradeValueBy(1);
        DynamicVars["Vulnerable"].UpgradeValueBy(1);
    }
}

/// <summary>
/// BA启动！：1 费技能（罕见）。获得 3 点活力，摸 2 张牌（升级：4 活力、3 牌）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class BaBoot : ModCardTemplate
{
    public BaBoot() : base(0, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Vigor", 3),  // 升级 4
        // 用原版强类型 CardsVar：「抽 N 张牌」的 "Cards" 槽位在原版是 CardsVar，
        // 普通 DynamicVar 只要有任何代码读 DynamicVars.Cards 就会 InvalidCastException。
        new CardsVar(2)              // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        Audio.MomoiAudio.PlayVoice(Audio.MomoiSfx.BaBoot);
        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, DynamicVars["Vigor"].BaseValue, Owner.Creature, this);
        await CardPileCmd.Draw(choiceContext, DynamicVars["Cards"].BaseValue, Owner);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Vigor"].UpgradeValueBy(1);
        DynamicVars["Cards"].UpgradeValueBy(1);
    }
}



/// <summary>
/// 嘲讽：0 费技能（罕见）。给予自身 1 层易伤与 1 层缓冲；使所有敌人获得 3 点活力，
/// 并给予所有敌人 1 层易伤与 4 层灼烧（升级：敌方 2 层易伤、5 层灼烧）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Taunt : ModCardTemplate
{
    public Taunt() : base(0, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Vulnerable", 1),  // 敌方易伤（升级 2）
        new DynamicVar("Burn", 4),        // 升级 5
        new DynamicVar("Vigor", 3)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        if (player == null)
        {
            return;
        }

        // 自身：1 层易伤 + 1 层缓冲。
        await PowerCmd.Apply<VulnerablePower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        await PowerCmd.Apply<BufferPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);

        var combatState = Owner.Creature.CombatState;
        if (combatState != null)
        {
            foreach (var enemy in combatState.HittableEnemies)
            {
                await PowerCmd.Apply<VigorPower>(choiceContext, enemy, DynamicVars["Vigor"].IntValue, Owner.Creature, this);
                await PowerCmd.Apply<VulnerablePower>(choiceContext, enemy, DynamicVars["Vulnerable"].IntValue, Owner.Creature, this);
                await PowerCmd.Apply<BurnPower>(choiceContext, enemy, DynamicVars["Burn"].IntValue, Owner.Creature, this);
            }
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Vulnerable"].UpgradeValueBy(1);
        DynamicVars["Burn"].UpgradeValueBy(1);
    }
}
