using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Factories;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Helpers;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Nodes.CommonUi;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.Rooms;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;
using STS2_Momoi.Diagnostics;

namespace STS2_Momoi.Cards;

/// <summary>
/// 发布委托：1 费技能（普通）。获得 7 点格挡；下回合开始时，将一张随机小游戏牌放入你的手牌（升级：10 格挡、升级后）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class PostQuest : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public PostQuest() : base(2, CardType.Skill, CardRarity.Common, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(11m, ValueProp.Move)  // 升级 14
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);
        await PowerCmd.Apply<PostQuestPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Block"].UpgradeValueBy(3);   // 11 -> 14
    }
}

/// <summary>
/// 发布委托的延迟发牌：多张可叠加——每打出一张发布委托，下回合多获得 1 张小游戏牌；
/// 升级版独立计数（下回合多获得 1 张升级过的小游戏牌）。
/// </summary>
[RegisterPower]
public sealed class PostQuestPower : ModPowerTemplate
{
    private class Data
    {
        public bool Upgraded;
    }

    // 每张发布委托独立生效（Instanced：重复打出叠加张数）。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/post_quest_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/post_quest_power.png");

    protected override object InitInternalData() => new Data();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new StringVar("UpgradedMark")  // 描述中的卡牌状态：空 / 升级过的
    ];

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        var upgraded = cardSource?.IsUpgraded == true;
        GetInternalData<Data>().Upgraded = upgraded;
        // 描述随升级变化：升级后显示“升级过的”（值取自本地化键，随语言自动切换）。
        ((StringVar)DynamicVars["UpgradedMark"]).StringValue = upgraded
            ? new LocString("powers", "STS2_MOMOI_POWER_POST_QUEST_UPGRADED_MARK").GetFormattedText()
            : "";
        return Task.CompletedTask;
    }

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var card = MinigameSupport.CreateRandomMinigameCard(combatState, Owner.Player, GetInternalData<Data>().Upgraded);
        CombatStats.RecordMinigameObtained(card);
        await CardPileCmd.AddGeneratedCardToCombat(card, PileType.Hand, Owner.Player);

        await PowerCmd.Remove(this);
    }
}

/// <summary>
/// 拾遗：1 费技能（普通）。从随机 3 张小游戏牌中选择 1 张加入你的手牌；优先搜寻本场战斗中未获得过的。消耗
/// （升级：4 张升级版）。若均获得过则改为获得随机小游戏牌。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Salvage : ModCardTemplate
{
    public Salvage() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Options", 3)  // 升级 4
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 优先本场未获得过的小游戏牌。
        var unseen = MinigameSupport.AllMinigameCards
            .Where(t => !CombatStats.ObtainedMinigames.Contains(((CardModel)ModelDb.Get(t)).Id.Entry))
            .ToList();

        var options = new List<CardModel>();
        var source = unseen.Count > 0 ? unseen : MinigameSupport.AllMinigameCards.ToList();
        var used = new HashSet<string>();
        while (options.Count < DynamicVars["Options"].IntValue && used.Count < source.Count)
        {
            var type = Owner.RunState.Rng.CombatCardSelection.NextItem(source) ?? source[0];
            var entry = ((CardModel)ModelDb.Get(type)).Id.Entry;
            if (!used.Add(entry))
            {
                continue;
            }

            var card = combatState.CreateCard((CardModel)ModelDb.Get(type), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(card);
            }

            options.Add(card);
        }

        // 4 张以上选项用网格选择（FromChooseACardScreen 最多 3 张）。
        var picked = (await CardSelectCmd.FromSimpleGrid(choiceContext, options, Owner,
            new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 1, 1))).FirstOrDefault();
        if (picked != null)
        {
            CombatStats.RecordMinigameObtained(picked);
            await CardPileCmd.AddGeneratedCardToCombat(picked, PileType.Hand, Owner);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Options"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 熬夜：1 费技能（罕见）。选择抽牌堆的 1 张牌，将其变化为随机小游戏牌；将一张睡眠不佳放入你的手牌
/// （升级：升级版小游戏牌）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class StayUpLate : ModCardTemplate
{
    public StayUpLate() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    // 衍生牌预览：睡眠不佳。
    // ⚠ 必须恒传 upgrade:false —— PoorSleep 是诅咒牌，MaxUpgradeLevel == 0，
    // 而 HoverTipFactory.FromCard(card, upgrade:true) 内部会调 UpgradeInternal()，
    // 那里会抛 InvalidOperationException("cannot be upgraded past its MaxUpgradeLevel")，
    // 所以「熬夜+」一旦悬停就会直接抛。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<PoorSleep>()
    ];

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        var combatState = Owner.Creature.CombatState;
        if (player == null || combatState == null)
        {
            return;
        }

        // 选择抽牌堆的 1 张牌。
        var drawPile = PileType.Draw.GetPile(player);
        if (drawPile.Cards.Count > 0)
        {
            var picked = (await CardSelectCmd.FromCombatPile(choiceContext, drawPile, player,
                new CardSelectorPrefs(new LocString("card_selection", "TO_TRANSFORM"), 1, 1))).FirstOrDefault();
            if (picked != null)
            {
                // 变化为随机小游戏牌。
                var replacement = MinigameSupport.CreateRandomMinigameCard(combatState, Owner, IsUpgraded);
                CombatStats.RecordMinigameObtained(replacement);
                await CardCmd.Transform(picked, replacement);
            }
        }

        // 睡眠不佳入手。
        var poorSleep = combatState.CreateCard(ModelDb.Card<PoorSleep>(), Owner);
        await CardPileCmd.AddGeneratedCardToCombat(poorSleep, PileType.Hand, Owner);
    }

    protected override void OnUpgrade()
    {
    }
}

/// <summary>
/// 创造性品味：3 费能力（稀有）。回合开始时，将 1 张随机小游戏牌加入手牌（升级：2 费、升级版）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class CreativeTaste : ModCardTemplate
{
    public CreativeTaste() : base(3, CardType.Power, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 升级前/升级后能力独立：升级后只与升级后叠加。
        if (IsUpgraded)
        {
            await PowerCmd.Apply<CreativeTasteUpgradedPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }
        else
        {
            await PowerCmd.Apply<CreativeTastePower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }
    }

    protected override void OnUpgrade()
    {
        EnergyCost.UpgradeBy(-1);
    }
}

[RegisterPower]
public sealed class CreativeTastePower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 升级前的能力独立叠加：只生成未升级的小游戏牌。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/creative_taste_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/creative_taste_power.png");

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        for (int i = 0; i < Amount; i++)
        {
            var card = MinigameSupport.CreateRandomMinigameCard(combatState, Owner.Player, false);
            CombatStats.RecordMinigameObtained(card);
            await CardPileCmd.AddGeneratedCardToCombat(card, PileType.Hand, Owner.Player);
        }
    }
}

/// <summary>创造性品味（升级）：只生成升级过的小游戏牌，与升级前的能力独立叠加。</summary>
[RegisterPower]
public sealed class CreativeTasteUpgradedPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 升级后的能力独立叠加：只生成升级过的小游戏牌。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/creative_taste_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/creative_taste_power.png");

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        for (int i = 0; i < Amount; i++)
        {
            var card = MinigameSupport.CreateRandomMinigameCard(combatState, Owner.Player, true);
            CombatStats.RecordMinigameObtained(card);
            await CardPileCmd.AddGeneratedCardToCombat(card, PileType.Hand, Owner.Player);
        }
    }
}





/// <summary>
/// 方块（状态牌·衍生）的共享逻辑：当此牌被消耗时，获得 2 点格挡（受敏捷等加成）。
/// 黄 / 蓝 / 紫 / 绿四种方块效果与类型完全相同，仅卡面独立；相关效果随机获得其中一种。
/// </summary>
public static class BlockCards
{
    /// <summary>四种方块（黄、蓝、紫、绿）。</summary>
    public static readonly Type[] All =
    [
        typeof(YellowBlock), typeof(BlueBlock), typeof(PurpleBlock), typeof(GreenBlock)
    ];

    public static bool IsBlock(CardModel card) => card is YellowBlock or BlueBlock or PurpleBlock or GreenBlock;

    /// <summary>随机生成一种方块（本场战斗随机池）。</summary>
    public static CardModel CreateRandom(ICombatState combatState, Player owner)
    {
        var type = All[owner.RunState.Rng.CombatCardSelection.NextInt(All.Length)];
        return combatState.CreateCard((CardModel)ModelDb.Get(type), owner);
    }

    /// <summary>展示用：查看与方块有关的牌时同时显示四种方块。</summary>
    public static IEnumerable<IHoverTip> Tips() =>
        All.Select(t => HoverTipFactory.FromCard((CardModel)ModelDb.Get(t))).ToList();
}

/// <summary>黄方块：状态牌（衍生）。</summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class YellowBlock : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public YellowBlock() : base(-1, CardType.Status, CardRarity.Status, TargetType.None)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Unplayable };

    public override int MaxUpgradeLevel => 0;

    public override async Task AfterCardExhausted(PlayerChoiceContext choiceContext, CardModel card, bool causedByEthereal)
    {
        if (card != this)
        {
            return;
        }

        await CreatureCmd.GainBlock(Owner.Creature, new BlockVar(2, ValueProp.Move), null);
    }
}

/// <summary>蓝方块：状态牌（衍生）。</summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class BlueBlock : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public BlueBlock() : base(-1, CardType.Status, CardRarity.Status, TargetType.None)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Unplayable };

    public override int MaxUpgradeLevel => 0;

    public override async Task AfterCardExhausted(PlayerChoiceContext choiceContext, CardModel card, bool causedByEthereal)
    {
        if (card != this)
        {
            return;
        }

        await CreatureCmd.GainBlock(Owner.Creature, new BlockVar(2, ValueProp.Move), null);
    }
}

/// <summary>紫方块：状态牌（衍生）。</summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class PurpleBlock : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public PurpleBlock() : base(-1, CardType.Status, CardRarity.Status, TargetType.None)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Unplayable };

    public override int MaxUpgradeLevel => 0;

    public override async Task AfterCardExhausted(PlayerChoiceContext choiceContext, CardModel card, bool causedByEthereal)
    {
        if (card != this)
        {
            return;
        }

        await CreatureCmd.GainBlock(Owner.Creature, new BlockVar(2, ValueProp.Move), null);
    }
}

/// <summary>绿方块：状态牌（衍生）。</summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class GreenBlock : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public GreenBlock() : base(-1, CardType.Status, CardRarity.Status, TargetType.None)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Unplayable };

    public override int MaxUpgradeLevel => 0;

    public override async Task AfterCardExhausted(PlayerChoiceContext choiceContext, CardModel card, bool causedByEthereal)
    {
        if (card != this)
        {
            return;
        }

        await CreatureCmd.GainBlock(Owner.Creature, new BlockVar(2, ValueProp.Move), null);
    }
}

/// <summary>
/// 秒人斧：0 费攻击（稀有）。造成 999 点伤害；战斗结束时，从你的牌组中移除这张牌。消耗（升级：保留）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class OneShotAxe : ModCardTemplate
{
    public OneShotAxe() : base(0, CardType.Attack, CardRarity.Rare, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(999m),
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];

    // 移除自身：打出时**立即**把牌组中的本尊移除（复制品不移除）。
    // 放在 OnPlay 里 await 掉，而不是在 GetResultLocationForCardPlay 里 fire-and-forget：
    // 这样即使这一斧直接把敌人砍死、战斗立刻结束，移除也已经结算完。
    private async Task RemoveSelfFromDeck()
    {
        // 复制品不移除：IsClone（CloneOf != null）同时盖住两种复制方式 ——
        // 「大姐头」/「赖招复读」走 CreateClone，而「轮回」/「援护」走 CreateDupe。
        if (IsClone)
        {
            MomoiDiag.Log("[OneShotAxe] 这张是复制品(IsClone)，不移除牌组");
            return;
        }

        // 优先用 DeckVersion（战斗开始时从牌组克隆出来的那张所对应的牌组本尊）。
        var deckCard = DeckVersion;
        if (deckCard == null)
        {
            // 兜底：控制台 / FreeLoadout 这类直接塞到手牌的实例不会挂 DeckVersion，
            // 这时按卡 ID 在牌组里找一张同名牌移除。
            deckCard = Owner.Deck.Cards.FirstOrDefault(c => c.Id == Id);
        }

        if (deckCard == null)
        {
            MomoiDiag.Log("[OneShotAxe] 牌组里没有同名牌，跳过移除");
            return;
        }

        if (deckCard.Pile?.Type != PileType.Deck)
        {
            MomoiDiag.Log($"[OneShotAxe] 牌组卡不在 Deck 堆（Pile={deckCard.Pile?.Type}），跳过移除");
            return;
        }

        MomoiDiag.Log($"[OneShotAxe] 打出时从牌组移除本尊（DeckVersion={(DeckVersion != null ? "有" : "无")}）");
        await CardPileCmd.RemoveFromDeck(deckCard);
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 先移除再打伤害：击杀即结束战斗也不会漏掉移除。
        await RemoveSelfFromDeck();

        var target = cardPlay.Target;
        if (target != null)
        {
            await MomoiSovereignStyle.Apply(
                    DamageCmd.Attack(DynamicVars.CalculatedDamage)
                        .FromCard(this, cardPlay)
                        .Targeting(target))
                .Execute(choiceContext);
        }
    }

    protected override void OnUpgrade()
    {
        LocalKeywords.Add(CardKeyword.Retain);
    }
}

/// <summary>
/// 毁灭与新生：2 费技能（稀有）。消耗你所有的诅咒牌；每消耗一张牌，将一张随机牌加入你的手牌（升级：升级版 + 保留）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class DestructionAndRebirth : ModCardTemplate
{
    public DestructionAndRebirth() : base(1, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        var combatState = Owner.Creature.CombatState;
        if (player == null || combatState == null)
        {
            return;
        }

        var curses = new List<CardModel>();
        foreach (var pileType in new[] { PileType.Hand, PileType.Draw, PileType.Discard })
        {
            curses.AddRange(pileType.GetPile(player).Cards.Where(c => c.Type == CardType.Curse));
        }

        var count = curses.Count;
        foreach (var curse in curses.Distinct().ToList())
        {
            await CardCmd.Exhaust(choiceContext, curse);
        }

        // 每消耗 1 张诅咒牌，将 1 张随机小游戏牌加入手牌（升级：升级过的随机小游戏牌）。
        for (int i = 0; i < count; i++)
        {
            var minigame = MinigameSupport.CreateRandomMinigameCard(combatState, player, IsUpgraded);
            CombatStats.RecordMinigameObtained(minigame);
            await CardPileCmd.AddGeneratedCardToCombat(minigame, PileType.Hand, player);
        }
    }

    protected override void OnUpgrade()
    {
        // 升级：获得固有。
        LocalKeywords.Add(CardKeyword.Innate);
    }
}





/// <summary>
/// 开荒：0 费技能（普通）。获得 2 点能量，将 1 张本场战斗中尚未获得过的特定诅咒加入你的弃牌堆（升级：3 点能量）。
/// 特定诅咒池：苦恼 → 睡眠不佳 → 疑虑 → 执迷；本场战斗中生成过的诅咒会从池中移除，池空后不再获得。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Grinding : ModCardTemplate
{
    public Grinding() : base(0, CardType.Skill, CardRarity.Common, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 侧栏：4 张特定诅咒。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_GRINDING.sidebar")),
        HoverTipFactory.FromCard<Writhe>(),
        HoverTipFactory.FromCard<PoorSleep>(),
        HoverTipFactory.FromCard<Doubt>(),
        HoverTipFactory.FromCard<Enthralled>()
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar(2)  // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PlayerCmd.GainEnergy(DynamicVars["Energy"].IntValue, Owner);

        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 取池中下一个本场战斗中未生成过的特定诅咒（池空 → 不再获得）。
        var curseType = GrindingCursePool.Next();
        if (curseType == null)
        {
            MomoiDiag.Log("[Grinding] curse pool is empty, no curse added");
            return;
        }

        var curse = combatState.CreateCard((CardModel)ModelDb.Get(curseType), Owner);
        CardCmd.PreviewCardPileAdd(await CardPileCmd.AddGeneratedCardToCombat(curse, PileType.Discard, Owner));
        await Cmd.Wait(0.4f);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Energy"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 开荒的「特定诅咒」池（战斗级）：苦恼 → 睡眠不佳 → 疑虑 → 执迷。
/// 本场战斗中生成过某种诅咒（含熬夜、构想等其它来源）即从池中移除该种；战斗开始时重置。
/// </summary>
public static class GrindingCursePool
{
    private static readonly Type[] Order = [typeof(Writhe), typeof(PoorSleep), typeof(Doubt), typeof(Enthralled)];

    private static readonly HashSet<Type> Generated = [];

    public static void Reset() => Generated.Clear();

    /// <summary>记录本场战斗中生成过的特定诅咒（由 Hook.AfterCardGeneratedForCombat 调用）。</summary>
    public static void Record(CardModel card)
    {
        var type = card switch
        {
            Writhe => typeof(Writhe),
            PoorSleep => typeof(PoorSleep),
            Doubt => typeof(Doubt),
            Enthralled => typeof(Enthralled),
            _ => null
        };

        if (type != null && Generated.Add(type))
        {
            MomoiDiag.Log($"[Grinding] curse pool: {type.Name} used, {Order.Length - Generated.Count} left");
        }
    }

    /// <summary>按固定顺序取下一个未生成过的诅咒；池空返回 null。</summary>
    public static Type? Next() => Order.FirstOrDefault(t => !Generated.Contains(t));
}
