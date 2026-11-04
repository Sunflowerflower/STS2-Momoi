using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Potions;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.Models.Cards;
using STS2_Momoi.Cards;
using STS2_Momoi.Characters;
using STS2_Momoi.Tips;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Potions;

/// <summary>速溶咖啡（普通）：将一张构想与一张睡眠不佳加入你的手牌。</summary>
[RegisterPotion(typeof(STS2_MomoiPotionPool))]
public sealed class InstantCoffee : ModPotionTemplate
{
    public override PotionRarity Rarity => PotionRarity.Common;

    public override PotionUsage Usage => PotionUsage.CombatOnly;

    public override TargetType TargetType => TargetType.Self;

    public override PotionAssetProfile AssetProfile => new(
        ImagePath: $"{Entry.ResPath}/images/potions/{GetType().Name}.png",
        OutlinePath: $"{Entry.ResPath}/images/potions/{GetType().Name}_outline.png");

    // 侧栏：预览会加入手牌的那两张牌（构想 / 睡眠不佳）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<ConceptCard>(),
        HoverTipFactory.FromCard<PoorSleep>()
    ];

    protected override async Task OnUse(PlayerChoiceContext choiceContext, Creature? target)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), Owner);
        await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, Owner);
        var poorSleep = combatState.CreateCard(ModelDb.Card<PoorSleep>(), Owner);
        await CardPileCmd.AddGeneratedCardToCombat(poorSleep, PileType.Hand, Owner);
    }
}

/// <summary>草莓牛奶（罕见）：仅对玩家自己使用。清空所有能力与状态，然后获得 7 点最大生命值与 1 点力量。</summary>
[RegisterPotion(typeof(STS2_MomoiPotionPool))]
public sealed class StrawberryMilk : ModPotionTemplate
{
    public override PotionRarity Rarity => PotionRarity.Uncommon;

    public override PotionUsage Usage => PotionUsage.AnyTime;

    public override TargetType TargetType => TargetType.Self;

    public override PotionAssetProfile AssetProfile => new(
        ImagePath: $"{Entry.ResPath}/images/potions/{GetType().Name}.png",
        OutlinePath: $"{Entry.ResPath}/images/potions/{GetType().Name}_outline.png");

    // 侧栏：描述里的「力量」。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [MomoiSidebarTips.Strength];

    protected override async Task OnUse(PlayerChoiceContext choiceContext, Creature? target)
    {
        // 净化：清空玩家当前的所有能力与状态（正面/负面/临时能力都在 Creature.Powers 里；
        // 必须 ToList() 再逐个 PowerCmd.Remove，边卸边遍历会炸）。
        foreach (var power in Owner.Creature.Powers.ToList())
        {
            await PowerCmd.Remove(power);
        }

        // 净化之后的效果：+7 最大生命值，+1 力量。
        await CreatureCmd.GainMaxHp(Owner.Creature, 7);
        await PowerCmd.Apply<StrengthPower>(choiceContext, Owner.Creature, 1, Owner.Creature, null);
    }
}

/// <summary>桃味气泡水（稀有）：任意张手牌变化为小游戏牌。</summary>
[RegisterPotion(typeof(STS2_MomoiPotionPool))]
public sealed class PeachSoda : ModPotionTemplate
{
    public override PotionRarity Rarity => PotionRarity.Rare;

    public override PotionUsage Usage => PotionUsage.CombatOnly;

    public override TargetType TargetType => TargetType.Self;

    // 注意：这个属性以前漏写了，导致药水贴图回退成占位图（就是游戏里那个“nope”小图标）。
    public override PotionAssetProfile AssetProfile => new(
        ImagePath: $"{Entry.ResPath}/images/potions/{GetType().Name}.png",
        OutlinePath: $"{Entry.ResPath}/images/potions/{GetType().Name}_outline.png");

    // 侧栏：描述里的「小游戏牌」与「变化」。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        MomoiSidebarTips.MinigameKeyword,
        MomoiSidebarTips.Transform
    ];

    protected override async Task OnUse(PlayerChoiceContext choiceContext, Creature? target)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 「任意张」= 原版那种 0 ~ 999999999（护驾！！！/净化 都是这么写的），文案自己写一条不带 {Amount} 的。
        // ⚠ source 必须传 null：NPlayerHand.AfterCardsSelected(source) 在 source != null 时会把「手牌 holder 归位」
        //   挂到 source.ExecutionFinished 上；药水模型永远不会抛这个事件，于是选中的卡牌节点一直留在
        //   「已选卡牌容器」里 —— CardCmd.Transform 找不到手牌节点、变牌白光后卡面迟迟不恢复（就是那个“白很久”）。
        //   （消消乐在批次17/18 踩过同一个坑，同样用 source: null 解决。）
        var picked = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("card_selection", "STS2_MOMOI_ANY_TRANSFORM"), 0, 999999999)
            {
                Cancelable = true,
                RequireManualConfirmation = true
            }, null, null)).ToList();

        // 逐张变牌：和「整活」/ 原版「护驾！！！」完全同一条路径（CardCmd.Transform(单张)）。
        foreach (var card in picked)
        {
            var replacement = MinigameSupport.CreateRandomMinigameCard(combatState, Owner, false);
            CombatStats.RecordMinigameObtained(replacement);
            await CardCmd.Transform(card, replacement);
        }
    }
}
