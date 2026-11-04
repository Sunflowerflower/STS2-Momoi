using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 灼热打击：1 费攻击（罕见）。造成 9 点伤害；若目标有灼烧状态，则攻击 2 次（升级：10 伤、3 次）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class ScorchingStrike : ModCardTemplate
{
    public ScorchingStrike() : base(1, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(7m),  // 升级 11
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        var damage = Convert.ToInt32(DynamicVars.CalculatedDamage);
        var attack = await DamageCmd.Attack(damage)
            .FromCard(this, cardPlay)
            .Targeting(target)
            .BeforeDamage(() =>
            {
                MomoiVfx.PlayFiendFire(target);
                return Task.CompletedTask;
            })
            .Execute(choiceContext);

        // 如果该敌人拥有灼烧，则给予所有敌人等量层灼烧（等量 = 该目标拥有的灼烧层数）。
        var targetBurn = target.GetPower<BurnPower>();
        if (targetBurn is { Amount: > 0 } && !CombatManager.Instance.IsOverOrEnding)
        {
            var enemies = Owner.Creature.CombatState?.HittableEnemies;
            if (enemies != null)
            {
                await PowerCmd.Apply<BurnPower>(choiceContext, enemies, targetBurn.Amount, Owner.Creature, this);
            }
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(4);  // 7 -> 11
    }
}

/// <summary>
/// 局势升温（原「玩火」）：1 费攻击（罕见）。造成 10 点伤害，给予一半所造成伤害的灼烧（向下取整；升级向上）；
/// 分别将 2 张灼烧加入你的弃牌堆和抽牌堆（升级：13 伤）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class PlayWithFire : ModCardTemplate
{
    public PlayWithFire() : base(2, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(12m),  // 升级 16
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];

    // 衍生牌预览：灼烧（状态牌）。
    // ⚠ 必须恒传 upgrade:false —— Burn 是状态牌，MaxUpgradeLevel == 0，
    // 而 HoverTipFactory.FromCard(card, upgrade:true) 内部会调 UpgradeInternal()，
    // 那里 `if (value > MaxUpgradeLevel) throw new InvalidOperationException(...)`，
    // 所以「局势升温+」一旦悬停就会直接抛（升级版卡一定存在，因为玩火本体可升级）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<Burn>()
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        var attack = await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .Targeting(target)
            .BeforeDamage(() =>
            {
                MomoiVfx.PlayFiendFire(target);
                return Task.CompletedTask;
            })
            .Execute(choiceContext);

        // 一半所造成伤害的灼烧（未升级向下取整，升级向上取整）。
        var totalDealt = attack.Results.SelectMany(g => g).Sum(r => r.UnblockedDamage);
        var burn = IsUpgraded ? (totalDealt + 1) / 2 : totalDealt / 2;
        if (burn > 0)
        {
            await PowerCmd.Apply<BurnPower>(choiceContext, target, burn, Owner.Creature, this);
        }

        // 2 张灼烧状态牌分别加入弃牌堆与抽牌堆。
        var combatState = Owner.Creature.CombatState;
        if (combatState != null)
        {
            var burn1 = combatState.CreateCard(ModelDb.Card<Burn>(), Owner);
            await CardPileCmd.AddGeneratedCardToCombat(burn1, PileType.Discard, Owner);
            var burn2 = combatState.CreateCard(ModelDb.Card<Burn>(), Owner);
            await CardPileCmd.AddGeneratedCardToCombat(burn2, PileType.Draw, Owner);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(4);   // 12 -> 16
    }
}

/// <summary>
/// 火蛇怒咬：2 费技能（普通）。保留；给予 7 层灼烧；使灼烧持续回合数额外+1（升级：10 层）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class FireSerpentBite : ModCardTemplate
{
    public FireSerpentBite() : base(2, CardType.Skill, CardRarity.Common, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Retain };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Burn", 7)  // 升级 10
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        VfxCmd.PlayOnCreatureCenter(target, "vfx/vfx_bite");

        await PowerCmd.Apply<BurnPower>(choiceContext, target,
            DynamicVars["Burn"].BaseValue, Owner.Creature, this);

        // 火蛇怒咬：在叠层重置规则的基础上额外使剩余回合数 +1（可叠出 3+ 回合）。
        var turns = target.GetPower<BurnTurnsPower>();
        if (turns != null)
        {
            await PowerCmd.ModifyAmount(choiceContext, turns, 1, Owner.Creature, this);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Burn"].UpgradeValueBy(3);
    }
}
