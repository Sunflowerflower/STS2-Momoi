using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 暗黑心理学：2 费技能（稀有）。使一名敌人在下次获得力量时将不再获得，改为使构想数值 +1。消耗。
/// 升级：不再消耗（效果不变）。
/// 拦截力量结算用的是原版「修饰器钩子」TryModifyPowerAmountReceived + AfterModifyingPowerAmountReceived
/// （与原版神器 ArtifactPower 同款写法）；只拦力量**增加**，不拦减少。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class DarkPsychology : ModCardTemplate
{
    public DarkPsychology() : base(2, CardType.Skill, CardRarity.Rare, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        await PowerCmd.Apply<DarkPsychologyPower>(choiceContext, target, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        // 升级：不再消耗（效果不变）。
        LocalKeywords.Remove(CardKeyword.Exhaust);
    }
}

/// <summary>
/// 暗黑心理学（敌方减益，可叠加次数）：下 <c>Amount</c> 次获得力量时将不再获得，改为使构想数值 +1。
/// 触发后消耗 1 层（减到 0 自动移除）。
/// </summary>
[RegisterPower]
public sealed class DarkPsychologyPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Debuff;

    // 只叠次数：每层抵消一次力量获得。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/dark_psychology_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/dark_psychology_power.png");

    public override bool TryModifyPowerAmountReceived(PowerModel canonicalPower, Creature target,
        decimal amount, Creature? applier, out decimal modifiedAmount)
    {
        modifiedAmount = amount;

        // 只拦「力量」的「增加」；力量减少（例如临时减力量的结算）照常通过。
        if (canonicalPower is not StrengthPower || target != Owner || amount <= 0m)
        {
            return false;
        }

        modifiedAmount = 0m;
        return true;
    }

    public override async Task AfterModifyingPowerAmountReceived(PowerModel power)
    {
        // 拦截成功：使所有玩家手牌中的构想数值 +1（没有构想的玩家不受影响）。
        var combatState = Owner.CombatState;
        if (combatState != null)
        {
            foreach (var player in combatState.Players)
            {
                // AddCountToAllInHand 本身不做选择，但保留真实上下文更安全（Throwing 版需要选择时会抛）。
                await ConceptCounterCapability.AddCountToAllInHand(new ThrowingPlayerChoiceContext(), player.Creature, 1);
            }
        }

        // 消耗 1 层（减到 0 自动移除）。
        await PowerCmd.Decrement(this);
    }
}
