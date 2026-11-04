using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Factories;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Entities.Relics;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.Nodes.CommonUi;
using MegaCrit.Sts2.Core.Rooms;
using STS2_Momoi.Cards;
using STS2_Momoi.Characters;
using STS2_Momoi.Tips;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Models.Capabilities;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Relics;

/// <summary>
/// 满溢灵感（先古）：枯竭灵感的先古版本（与先古遗物欧洛巴斯之触绑定）。
/// 回合开始时，若手牌中没有构想，将一张构想+加入你的手牌并使其数值+1。
/// </summary>
[RegisterRelic(typeof(STS2_MomoiRelicPool))]
public sealed class OverflowingInspiration : ModRelicTemplate
{
    public override RelicRarity Rarity => RelicRarity.Ancient;

    public override RelicAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png",
        IconOutlinePath: $"{Entry.ResPath}/images/relics/{GetType().Name}_outline.png",
        BigIconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png");

    // 侧栏：预览升级过的「构想+」（这个遗物给的是升级版）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [HoverTipFactory.FromCard<ConceptCard>(upgrade: true)];

    public override Task AfterCardGeneratedForCombat(CardModel card, Player? creator)
    {
        if (creator == Owner && MinigameSupport.CanBeTemporarilyAdded(card))
        {
            Audio.MomoiAudio.PlayVoice(Audio.MomoiSfx.MinigameGenerated);
        }

        return Task.CompletedTask;
    }

    public override async Task AfterPlayerTurnStart(PlayerChoiceContext choiceContext, Player player)
    {
        // 多人模式：这个钩子会对所有玩家的回合开始都触发一次，遗物只服务它自己的主人。
        if (player != Owner) { return; }

        var combatState = player.Creature.CombatState;
        var hand = player.PlayerCombatState?.Hand;
        if (combatState == null || hand == null)
        {
            return;
        }

        if (hand.Cards.Any(c => c is ConceptCard))
        {
            return;
        }

        var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), player);
        CardCmd.Upgrade(concept);
        await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, player, CardPilePosition.Top);
    }
}

/// <summary>没吃完的薯片（普通）：你每有50金币，当你进入商店房间和休息处时就将你的最大生命值提升1点。</summary>
[RegisterRelic(typeof(STS2_MomoiRelicPool))]
public sealed class UnfinishedChips : ModRelicTemplate
{
    public override RelicRarity Rarity => RelicRarity.Common;

    public override RelicAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png",
        IconOutlinePath: $"{Entry.ResPath}/images/relics/{GetType().Name}_outline.png",
        BigIconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png");

    // 商店房间 / 休息处都触发（商店的写法参考原版遗物餐券 MealTicket：AfterRoomEntered + room is MerchantRoom）。
    public override async Task AfterRoomEntered(AbstractRoom room)
    {
        var player = Owner;
        if (player == null || room is not (RestSiteRoom or MerchantRoom))
        {
            return;
        }

        var amount = player.Gold / 50;
        if (amount > 0)
        {
            Flash();
            await CreatureCmd.GainMaxHp(player.Creature, amount);
        }
    }
}

/// <summary>胜利的剧本（罕见）：打出构想时，升级手中所有牌。</summary>
[RegisterRelic(typeof(STS2_MomoiRelicPool))]
public sealed class WinningScript : ModRelicTemplate
{
    public override RelicRarity Rarity => RelicRarity.Uncommon;

    public override string FlashSfx => Audio.MomoiSfx.WinningScript;

    public override RelicAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png",
        IconOutlinePath: $"{Entry.ResPath}/images/relics/{GetType().Name}_outline.png",
        BigIconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png");

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner != Owner || cardPlay.Card is not ConceptCard)
        {
            return;
        }

        Audio.MomoiAudio.PrepareVoice(Audio.MomoiSfx.WinningScript);
        Flash();
        var hand = PileType.Hand.GetPile(Owner).Cards.ToList();
        foreach (var card in hand)
        {
            CardCmd.Upgrade(card);
        }
    }
}

/// <summary>收藏完好的旧游戏机（罕见）：战斗开始时，将一张随机小游戏牌加入你的手牌。</summary>
[RegisterRelic(typeof(STS2_MomoiRelicPool))]
public sealed class OldGameConsole : ModRelicTemplate
{
    public override RelicRarity Rarity => RelicRarity.Uncommon;

    public override RelicAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png",
        IconOutlinePath: $"{Entry.ResPath}/images/relics/{GetType().Name}_outline.png",
        BigIconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png");

    // 侧栏：描述里的「小游戏牌」。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [MomoiSidebarTips.MinigameKeyword];

    public override async Task BeforeCombatStart()
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var card = MinigameSupport.CreateRandomMinigameCard(combatState, Owner, false);
        CombatStats.RecordMinigameObtained(card);
        await CardPileCmd.AddGeneratedCardToCombat(card, PileType.Hand, Owner);
    }
}

/// <summary>绿色挂饰（稀有）：回合开始时，你可以消耗一张诅咒牌来使构想数值+1。</summary>
[RegisterRelic(typeof(STS2_MomoiRelicPool))]
public sealed class GreenCharm : ModRelicTemplate
{
    public override RelicRarity Rarity => RelicRarity.Rare;

    public override RelicAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png",
        IconOutlinePath: $"{Entry.ResPath}/images/relics/{GetType().Name}_outline.png",
        BigIconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png");

    // 侧栏：描述里的「消耗」。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [MomoiSidebarTips.Exhaust];

    public override async Task AfterPlayerTurnStart(PlayerChoiceContext choiceContext, Player player)
    {
        // 多人模式：这个钩子会对所有玩家的回合开始都触发一次，遗物只服务它自己的主人。
        if (player != Owner) { return; }

        var curses = PileType.Hand.GetPile(player).Cards.Where(c => c.Type == CardType.Curse).ToList();
        if (curses.Count == 0)
        {
            return;
        }

        var picked = (await CardSelectCmd.FromHand(choiceContext, player,
            new CardSelectorPrefs(new LocString("card_selection", "TO_EXHAUST"), 0, 1)
            {
                Cancelable = true,
                RequireManualConfirmation = true
            },
            c => c.Type == CardType.Curse, this)).FirstOrDefault();
        if (picked == null)
        {
            return;
        }

        await CardCmd.Exhaust(choiceContext, picked);
        await ConceptCounterCapability.AddCountToAllInHand(choiceContext, player.Creature, 1);
    }
}

/// <summary>桌游「The·人生」（稀有）：每当你打出一张小游戏牌时，将一张随机牌添加到你的手牌。</summary>
[RegisterRelic(typeof(STS2_MomoiRelicPool))]
public sealed class BoardGameOfLife : ModRelicTemplate
{
    public override RelicRarity Rarity => RelicRarity.Rare;

    public override RelicAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png",
        IconOutlinePath: $"{Entry.ResPath}/images/relics/{GetType().Name}_outline.png",
        BigIconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png");

    // 侧栏：描述里的「小游戏牌」。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [MomoiSidebarTips.MinigameKeyword];

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner != Owner || !MinigameSupport.IsMinigameCard(cardPlay.Card))
        {
            return;
        }

        // 原版添柴逻辑：从本角色已解锁、可战斗生成的卡池里有放回地抽 1 张加入手牌。
        var pool = Owner.Character.CardPool.GetUnlockedCards(Owner.UnlockState, Owner.RunState.CardMultiplayerConstraint);
        var cards = CardFactory.GetForCombat(Owner, pool, 1, Owner.RunState.Rng.CombatCardGeneration).ToList();
        await CardPileCmd.AddGeneratedCardsToCombat(cards, PileType.Hand, Owner);
    }
}

/// <summary>G.Bible（稀有）：你每打出5张小游戏牌，就回复6点生命。</summary>
[RegisterRelic(typeof(STS2_MomoiRelicPool))]
public sealed class GBible : ModRelicTemplate
{
    public override RelicRarity Rarity => RelicRarity.Rare;

    public override RelicAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png",
        IconOutlinePath: $"{Entry.ResPath}/images/relics/{GetType().Name}_outline.png",
        BigIconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png");

    // 侧栏：描述里的「小游戏牌」。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [MomoiSidebarTips.MinigameKeyword];

    private int _minigamesPlayed;

    // 计数角标（参考原版 Nunchaku/LetterOpener）：战斗中显示，数字 = 已打出的小游戏牌数。
    public override bool ShowCounter => CombatManager.Instance.IsInProgress;

    public override int DisplayAmount => _minigamesPlayed;

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner != Owner || !MinigameSupport.IsMinigameCard(cardPlay.Card))
        {
            return;
        }

        _minigamesPlayed++;
        if (_minigamesPlayed >= 5)
        {
            _minigamesPlayed = 0;
            Flash();
            await CreatureCmd.Heal(Owner.Creature, 6);
        }

        UpdateCounterDisplay();
    }

    private void UpdateCounterDisplay()
    {
        // 计数为 4/5 时高亮（RelicStatus.Active），触发后归 0。
        Status = _minigamesPlayed == 4 ? RelicStatus.Active : RelicStatus.Normal;
        InvokeDisplayAmountChanged();
    }
}

/// <summary>"镜子"（商店）：每场战斗的第1个回合结束时，可以选择一张牌复制并保留。原卡牌和复制品都将保留一回合。</summary>
[RegisterRelic(typeof(STS2_MomoiRelicPool))]
public sealed class Mirror : ModRelicTemplate
{
    public override RelicRarity Rarity => RelicRarity.Shop;

    public override RelicAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png",
        IconOutlinePath: $"{Entry.ResPath}/images/relics/{GetType().Name}_outline.png",
        BigIconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png");

    // 侧栏：描述里的「保留」。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [MomoiSidebarTips.Retain];

    private bool _usedThisCombat;

    public override Task BeforeCombatStart()
    {
        _usedThisCombat = false;
        return Task.CompletedTask;
    }

    public override async Task BeforeSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner.Creature) || _usedThisCombat)
        {
            return;
        }

        if (Owner.PlayerCombatState?.TurnNumber != 1)
        {
            return;
        }

        _usedThisCombat = true;
        var picked = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("card_selection", "TO_CLONE"), 0, 1)
            {
                Cancelable = true,
                RequireManualConfirmation = true
            }, null, this)).FirstOrDefault();
        if (picked == null)
        {
            return;
        }

        // 复制并只保留一回合（参考原版独门技术：单回合临时保留，不挂永久 Retain 关键词）。
        CardCmd.ApplySingleTurnRetain(picked);
        var clone = picked.CreateClone();
        CardCmd.ApplySingleTurnRetain(clone);
        await CardPileCmd.AddGeneratedCardToCombat(clone, PileType.Hand, Owner);
    }
}
