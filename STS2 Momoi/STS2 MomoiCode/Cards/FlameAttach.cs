using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Commands.Builders;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 火焰附加：1 费能力（罕见）。每当你造成伤害时，附带 1 层灼烧（升级 2 层）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class FlameAttach : ModCardTemplate
{
    public FlameAttach() : base(1, CardType.Power, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Burn", 2)  // 附带灼烧层数（升级 3）
    ];

    /// <summary>每叠加 1 层本能力时附带多少灼烧（= 卡面数值）。供 FlameAttachPower 直接读取。</summary>
    public int BurnPerStack => DynamicVars["Burn"].IntValue;

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 挂载被动（升级决定附带灼烧层数）。
        await PowerCmd.Apply<FlameAttachPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Burn"].UpgradeValueBy(1);  // 灼烧 2 -> 3
    }
}

/// <summary>
/// 火焰附加被动：每当玩家造成未被格挡的伤害时，目标获得灼烧（升级后 2 层）。
/// </summary>
[RegisterPower]
public sealed class FlameAttachPower : ModPowerTemplate
{
    private class Data
    {
        public int BurnAmount = 0;  // 叠加后的附带灼烧（升级前 1、升级后 2）
    }

    public override PowerType Type => PowerType.Buff;

    // 叠加：每多打出一张火焰附加，附带灼烧叠加（升级前 +1、升级后 +2）。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/flame_attach_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/flame_attach_power.png");

    protected override object InitInternalData() => new Data();

    // 右下角显示“被击中的敌人实际获得的灼烧层数”而不是叠加层数。
    public override int DisplayAmount => GetInternalData<Data>().BurnAmount;

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("BurnTotal", 0)
    ];

    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        var data = GetInternalData<Data>();
        // 附带层数按来源卡的卡面数值算（「火焰附加」是 1、升级 2），不要在这里写死 ? 2 : 1 ——
        // 以后调卡面数值时两边就会脱节。
        var perStack = cardSource is FlameAttach source
            ? source.BurnPerStack
            : (cardSource?.IsUpgraded == true ? 2 : 1);
        data.BurnAmount += (int)amount * perStack;
        DynamicVars["BurnTotal"].BaseValue = data.BurnAmount;
        InvokeDisplayAmountChanged();
        await Task.CompletedTask;
    }

    // 每当玩家拥有火力并造成伤害时（含虚拟女仆武器的附带伤害），被击中的目标获得灼烧。无关格挡。
    public override async Task AfterAttack(PlayerChoiceContext choiceContext, AttackCommand command)
    {
        if (command.Attacker != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        // 设计：拥有火力时才附带灼烧。
        if (Owner.GetPower<FirepowerPower>() is not { Amount: > 0 })
        {
            return;
        }

        var amount = GetInternalData<Data>().BurnAmount;
        foreach (var hitResults in command.Results)
        {
            var receiver = hitResults.FirstOrDefault()?.Receiver;
            // 只要攻击造成了伤害（含被格挡的部分）就施加灼烧。
            if (receiver != null && hitResults.Any(r => r.TotalDamage > 0))
            {
                await PowerCmd.Apply<BurnPower>(choiceContext, receiver, amount, Owner, null);
            }
        }
    }
}
