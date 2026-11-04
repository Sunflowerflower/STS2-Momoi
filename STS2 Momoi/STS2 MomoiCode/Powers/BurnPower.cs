using Godot;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Commands.Builders;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Helpers;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using MegaCrit.Sts2.Core.Nodes.Vfx;
using MegaCrit.Sts2.Core.ValueProps;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2_Momoi.Cards;
using STS2RitsuLib.Combat.HealthBars;
using STS2RitsuLib.Scaffolding.Content;
using STS2RitsuLib.Utils;

namespace STS2_Momoi.Powers;

/// <summary>
/// 灼烧（层数图标）：负面效果（作用于敌人或我方）。双图标机制：
/// - 本能力显示灼烧层数；配对的 <see cref="BurnTurnsPower"/> 显示剩余回合数；
/// - 拥有者在自己的回合开始受到等同层数的伤害（由回合数图标统一结算）；
/// - 剩余回合数归零时两个图标一起消失。
/// 施加规则：
/// - 首次施加：获得层数 + 剩余回合 2；
/// - 叠层：层数始终叠加；剩余回合 ≤1（即 1）时重置为 2；剩余回合 2 及以上保持不变；
/// - 火蛇怒咬在施加后额外 +1 回合（可叠出 3+ 回合）。
/// 拥有灼烧的敌人每次造成未被格挡的伤害时，对目标附 1 层灼烧（走同一叠层规则）。
/// </summary>
[RegisterPower]
public sealed class BurnPower : ModPowerTemplate, IHealthBarForecastSource
{
    public override PowerType Type => PowerType.Debuff;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/burn_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/burn_power.png");

    private static Material? _barMaterial;

    // 白/黄/橙相间的火焰条；沿用原版 doom_bar 的渐变质感，但不抢血字颜色。
    private static Material BarMaterial => _barMaterial ??= CreateBarMaterial();

    private static Material CreateBarMaterial()
    {
        var gradient = new Gradient();
        gradient.SetColor(0, new Color("FFF4D6"));
        gradient.SetOffset(0, 0f);
        gradient.SetColor(1, new Color("FFD45C"));
        gradient.SetOffset(1, 0.38f);
        gradient.SetColor(2, new Color("FFA518"));
        gradient.SetOffset(2, 0.72f);
        gradient.SetColor(3, new Color("FF6A00"));
        gradient.SetOffset(3, 1f);
        return MaterialUtils.CreateDoomBarShaderMaterial(new GradientTexture1D { Gradient = gradient });
    }

    public IEnumerable<HealthBarForecastSegment> GetHealthBarForecastSegments(HealthBarForecastContext context)
    {
        // FromRight 让这一段接在中毒伤害外侧；AffectsHpLabel=false 避免和毒/灾厄抢致命色。
        return HealthBarForecasts.Single(
            (int)Amount,
            new Color("FFA518"),
            HealthBarForecastGrowthDirection.FromRight,
            20,
            BarMaterial,
            null,
            false);
    }

    // 首次施加：同时挂上「灼烧剩余回合数」图标（2 回合）。
    public override async Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        if (Owner.GetPower<BurnTurnsPower>() == null)
        {
            await PowerCmd.Apply<BurnTurnsPower>(new ThrowingPlayerChoiceContext(), Owner, 2, applier, cardSource);
        }
    }

    // 叠层：层数由 Counter 自动叠加；剩余回合 ≤1 时重置为 2，≥2 时保持不变。
    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        if (Owner.Side == CombatSide.Enemy)
        {
            // 首次施加和后续叠层都触发一次地面火焰；新能力也会走这里。
            MomoiVfx.PlayGroundFire(Owner);
        }

        var turns = Owner.GetPower<BurnTurnsPower>();
        if (turns != null && turns.Amount <= 1)
        {
            await PowerCmd.Apply<BurnTurnsPower>(choiceContext, Owner, 2 - turns.Amount, Owner, cardSource);
        }
    }

    // 灼烧层数图标被清除（净化等）时，回合数图标一起消失。
    public override async Task AfterRemoved(Creature oldOwner)
    {
        var turns = oldOwner.GetPower<BurnTurnsPower>();
        if (turns != null)
        {
            await PowerCmd.Remove(turns);
        }
    }

    // 拥有灼烧的敌人每次造成未被格挡的伤害时，对目标附 1 层灼烧（玩家身上的灼烧不附带）。
    public override async Task AfterAttack(PlayerChoiceContext choiceContext, AttackCommand command)
    {
        if (Owner.Side != CombatSide.Enemy)
        {
            return;
        }

        if (command.Attacker != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        foreach (var hitResults in command.Results)
        {
            var receiver = hitResults.FirstOrDefault()?.Receiver;
            if (receiver != null && hitResults.Any(r => r.UnblockedDamage > 0))
            {
                await PowerCmd.Apply<BurnPower>(choiceContext, receiver, 1, Owner, null);
            }
        }
    }
}

/// <summary>
/// 灼烧（剩余回合数图标）：显示灼烧剩余回合数。
/// 每回合开始时：先结算灼烧伤害（等同层数），然后回合数 -1；归零时与灼烧层数图标一起消失。
/// </summary>
[RegisterPower]
public sealed class BurnTurnsPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Debuff;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/burn_turns_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/burn_turns_power.png");

    // 灼烧的每回合结算统一在此进行（层数图标只负责叠层/附灼）。
    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (!participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var owner = Owner;
        var burn = owner.GetPower<BurnPower>();
        if (burn == null)
        {
            // 层数图标被单独清除：回合数图标跟着消失。
            await PowerCmd.Remove(this);
            return;
        }

        // 灼烧伤害（无来源、不可格挡、不受加成）。
        if (burn.Amount > 0 && owner.IsAlive)
        {
            if (owner.Side == CombatSide.Enemy)
            {
                // 原版「焚烧」的地面火焰特效（只 VFX，不额外叠音效）。
                MomoiVfx.PlayGroundFire(owner);
            }

            await CreatureCmd.Damage(new ThrowingPlayerChoiceContext(), owner, burn.Amount,
                ValueProp.Unblockable | ValueProp.Unpowered, null, null);
        }

        await PowerCmd.ModifyAmount(new ThrowingPlayerChoiceContext(), this, -1, null, null);

        // 归零后 ModifyAmount 会自动移除本图标；再把灼烧层数图标一起移除。
        if (owner.GetPower<BurnTurnsPower>() == null && owner.GetPower<BurnPower>() != null)
        {
            await PowerCmd.Remove(burn);
        }
    }
}
