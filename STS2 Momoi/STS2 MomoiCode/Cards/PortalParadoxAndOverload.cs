using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.ValueProps;
using MegaCrit.Sts2.Core.Combat;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 传送门悖论：0 费技能（罕见）。从「传送门悖论其一 / 其二」中选择一张加入手牌，消耗。
/// 升级：给的是升级过的版本，并删去消耗。
/// （两张衍生牌本体是 Token 牌，只能由这张牌生成。）
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class PortalParadox : ModCardTemplate
{
    public PortalParadox() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 消耗（升级后删去）。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    // 侧栏：两张衍生牌（升级时预览升级过的版本）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<PortalParadoxOne>(IsUpgraded),
        HoverTipFactory.FromCard<PortalParadoxTwo>(IsUpgraded)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var options = new List<CardModel>();
        foreach (var type in new[] { typeof(PortalParadoxOne), typeof(PortalParadoxTwo) })
        {
            var card = combatState.CreateCard((CardModel)ModelDb.Get(type), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(card);
            }

            options.Add(card);
        }

        var picked = (await CardSelectCmd.FromSimpleGrid(choiceContext, options, Owner,
            new CardSelectorPrefs(new LocString("card_selection", "TO_ADD_TO_HAND"), 1, 1))).FirstOrDefault();
        if (picked != null)
        {
            await CardPileCmd.AddGeneratedCardToCombat(picked, PileType.Hand, Owner);
        }
    }

    protected override void OnUpgrade()
    {
        // 升级：删去消耗（另外给的是升级过的衍生牌，见 OnPlay）。
        RemoveKeyword(CardKeyword.Exhaust);
    }

    protected override void AfterDowngraded()
    {
        base.AfterDowngraded();
        AddKeyword(CardKeyword.Exhaust);
    }
}

/// <summary>
/// 过载：1 费能力（罕见）。获得 2（升级 3）层火力；每当你的火力层数减少时，获得 3（升级 4）点活力。
/// 过载 power 的层数 = 每次触发实际获得的活力点数，重复获得会叠加这个数值。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Overload : ModCardTemplate
{
    public Overload() : base(2, CardType.Power, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Firepower", 2),  // 升级 3
        new DynamicVar("Vigor", 2)       // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature,
            DynamicVars["Firepower"].IntValue, Owner.Creature, this);
        await PowerCmd.Apply<OverloadPower>(choiceContext, Owner.Creature,
            DynamicVars["Vigor"].IntValue, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Firepower"].UpgradeValueBy(1);   // 2 -> 3
        DynamicVars["Vigor"].UpgradeValueBy(1);       // 2 -> 3
    }
}

/// <summary>
/// 过载 power：层数 = 每次火力减少时获得的活力点数（重复施加叠加）。
/// </summary>
[RegisterPower]
public sealed class OverloadPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 叠加：重复获得会把「每次触发的活力点数」加上去。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/overload_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/overload_power.png");

    // 右下角数字就是 Amount（每次触发获得的活力点数），不需要额外定义。

    // 火力层数减少时（原版/模组的消耗都走 PowerCmd.ModifyAmount → 这里能收到）。
    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != null && power is FirepowerPower && power.Owner == Owner && amount < 0)
        {
            if (CombatManager.Instance.IsOverOrEnding)
            {
                return;
            }

            var gain = (int)(Amount * -amount);
            if (gain > 0)
            {
                await PowerCmd.Apply<VigorPower>(choiceContext, Owner, gain, Owner, null);
            }
        }
    }
}
