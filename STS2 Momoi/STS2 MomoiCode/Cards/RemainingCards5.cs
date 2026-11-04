using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 义愤填膺：1 费技能（罕见·多人）。所有玩家获得 2 点活力、2 层火力（升级：3/3）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class RighteousIndignation : ModCardTemplate
{
    public override CardMultiplayerConstraint MultiplayerConstraint => CardMultiplayerConstraint.MultiplayerOnly;

    public RighteousIndignation() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");



    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Vigor", 2),     // 升级 3
        new DynamicVar("Firepower", 2)  // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        foreach (var player in combatState.Players)
        {
            await PowerCmd.Apply<VigorPower>(choiceContext, player.Creature, DynamicVars["Vigor"].BaseValue, Owner.Creature, this);
            await PowerCmd.Apply<FirepowerPower>(choiceContext, player.Creature, DynamicVars["Firepower"].BaseValue, Owner.Creature, this);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Vigor"].UpgradeValueBy(1);
        DynamicVars["Firepower"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 抽鬼牌！：0 费技能（罕见·多人·游戏牌）。每当你抽到这张牌时，将一张炸弹加入一名随机玩家的抽牌堆。
/// 打出时，使所有玩家的炸弹的耗费变为 0c。消耗（升级：炸弹+）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class OldMaid : ModCardTemplate
{
    public override CardMultiplayerConstraint MultiplayerConstraint => CardMultiplayerConstraint.MultiplayerOnly;

    public OldMaid() : base(0, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar("NoCost", 0)  // 描述中 0 费能量图标
    ];
    // 衍生牌预览：炸弹（原版 The Bomb）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<TheBomb>(IsUpgraded),
    ];

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.FullGameTag };

    // 抽到这张牌时：给一名随机玩家的抽牌堆加炸弹。
    public override async Task AfterCardDrawn(PlayerChoiceContext choiceContext, CardModel card, bool fromHandDraw)
    {
        if (card != this || Owner.Creature.CombatState == null)
        {
            return;
        }

        var combatState = Owner.Creature.CombatState;
        var player = Owner.RunState.Rng.CombatTargets.NextItem(combatState.Players);
        if (player == null)
        {
            return;
        }

        var bomb = combatState.CreateCard(ModelDb.Card<TheBomb>(), player);
        if (IsUpgraded)
        {
            CardCmd.Upgrade(bomb);
        }

        await CardPileCmd.AddGeneratedCardToCombat(bomb, PileType.Draw, player);
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 使所有玩家的炸弹耗费变为 0c。
        foreach (var player in combatState.Players)
        {
            foreach (var pileType in new[] { PileType.Hand, PileType.Draw, PileType.Discard })
            {
                foreach (var card in pileType.GetPile(player).Cards.Where(c => c is TheBomb))
                {
                    card.EnergyCost.SetThisCombat(0);
                }
            }
        }
    }

    protected override void OnUpgrade()
    {
    }
}

/// <summary>
/// 玩玩这款！：1 费技能（罕见·多人）。选择手牌中的 1 张小游戏牌，将其加入所有盟友的手牌（升级：升级版 + 保留）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class PlayThisOne : ModCardTemplate
{
    public override CardMultiplayerConstraint MultiplayerConstraint => CardMultiplayerConstraint.MultiplayerOnly;

    public PlayThisOne() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
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

        var picked = (await CardSelectCmd.FromHand(choiceContext, player,
            new CardSelectorPrefs(new LocString("card_selection", "CHOOSE_CARD_HEADER"), 1, 1),
            MinigameSupport.IsMinigameCard, this)).FirstOrDefault();
        if (picked == null)
        {
            return;
        }

        foreach (var ally in combatState.Players)
        {
            // 保留选中牌自身的升级状态。
            var clone = picked.CreateCloneForPlayer(ally);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(clone);
            }

            await CardPileCmd.AddGeneratedCardToCombat(clone, PileType.Hand, ally);
        }
    }

    protected override void OnUpgrade()
    {
        LocalKeywords.Add(CardKeyword.Retain);
    }
}

/// <summary>
/// 俄罗斯方块！：0 费技能（衍生·小游戏）。打出时随机将 1~4 张方块加入手牌，并将此牌返回你的手牌。
/// 本回合下一次手牌区满（10 张）时：消耗所有手牌、抽 3 张牌、获得 2c、将弃牌堆的所有方块返回手牌，并将此牌消耗
/// （升级：抽 4、3c）。该效果不可叠加（多张俄罗斯方块也只存在一个）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class Tetris : ModCardTemplate
{
    public Tetris() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    // 衍生牌预览：查看卡牌时显示四种方块。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => BlockCards.Tips();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Cards", 3),   // 升级 4（抽牌数）
        new EnergyVar(2),             // 升级 3
        new DynamicVar("NextBlocks", 0)  // 打出时加入的方块数（实时显示）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        var combatState = Owner.Creature.CombatState;
        if (player == null || combatState == null)
        {
            return;
        }

        // 覆盖规则：一张俄罗斯方块最多对应一个满手牌结算 buff（升级版连普通版一起顶掉）。
        await TetrisFullHandPower.RemoveOverridden(player, IsUpgraded);

        // 先挂上手牌达到上限时的消耗结算效果。
        var power = await PowerCmd.Apply<TetrisFullHandPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);

        // 随机 1~4 张方块：手牌未满→入手；溢出→先进入弃牌堆。
        var count = Owner.RunState.Rng.CombatCardSelection.NextInt(1, 5);
        DynamicVars["NextBlocks"].BaseValue = count;
        var hand = PileType.Hand.GetPile(player);
        for (int i = 0; i < count; i++)
        {
            var block = BlockCards.CreateRandom(combatState, Owner);
            var targetPile = hand.Cards.Count < CardPile.MaxCardsInHand ? PileType.Hand : PileType.Discard;
            await CardPileCmd.AddGeneratedCardToCombat(block, targetPile, Owner);
        }

        // 第 1 次塞方块就填满手牌：立即结算（溢出方块已在弃牌堆，随结算返回手牌）。
        var settled = false;
        if (power != null && hand.Cards.Count >= CardPile.MaxCardsInHand)
        {
            settled = await power.Settle(choiceContext, player, this);
        }

        if (!settled && Pile?.Type == PileType.Play)
        {
            // 未触发结算：将此牌返回手牌（后续本回合手牌满时由能力结算）。
            await CardPileCmd.Add(this, PileType.Hand, CardPilePosition.Random, this);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Cards"].UpgradeValueBy(1);
        DynamicVars["Energy"].UpgradeValueBy(1);
    }
}

/// <summary>俄罗斯方块的手牌满结算：消耗所有手牌 + 抽牌 + 能量 + 消耗自身 + 弃牌堆方块回手（不可叠加）。</summary>
[RegisterPower]
public sealed class TetrisFullHandPower : ModPowerTemplate
{
    private class Data
    {
        public int Cards = 3;
        public int Energy = 2;
        public bool Upgraded;
        public bool Triggered;
    }

    public override PowerType Type => PowerType.Buff;

    // 每张俄罗斯方块独立生效（多张时手牌满会同时触发各自的效果）。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/tetris_full_hand_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/tetris_full_hand_power.png");

    protected override object InitInternalData() => new Data();

    /// <summary>该实例是否来自升级后的俄罗斯方块。
    /// 本能力不做升级/非升级两个类，同档位靠这个标记区分。</summary>
    public bool Upgraded => GetInternalData<Data>().Upgraded;

    /// <summary>描述里显示实际抽几张、获得几能量。</summary>
    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Cards", 3),  // 升级 4
        new EnergyVar("Energy", 2)   // 升级 3
    ];

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        var data = GetInternalData<Data>();
        var upgraded = cardSource?.IsUpgraded == true;
        data.Upgraded = upgraded;
        data.Cards = upgraded ? 4 : 3;
        data.Energy = upgraded ? 3 : 2;
        DynamicVars["Cards"].BaseValue = data.Cards;
        DynamicVars["Energy"].BaseValue = data.Energy;
        return Task.CompletedTask;
    }

    /// <summary>
    /// 覆盖规则：一张俄罗斯方块最多对应一个满手牌结算 buff。
    ///   * 同档位互相覆盖（普通覆盖普通、升级覆盖升级）；
    ///   * **升级版额外覆盖非升级版**（反之不覆盖）——即升级后的俄罗斯方块总能把普通那层顶掉。
    /// </summary>
    public static async Task RemoveOverridden(Player player, bool upgraded)
    {
        var id = ModelDb.Get(typeof(TetrisFullHandPower)).Id;
        foreach (var existing in player.Creature.GetPowerInstances(id).OfType<TetrisFullHandPower>().ToList())
        {
            if (upgraded || !existing.Upgraded)
            {
                await PowerCmd.Remove(existing);
            }
        }
    }

    /// <summary>
    /// 手牌满时应由哪一个实例结算：升级版优先（无论两张俄罗斯方块的打出顺序），
    /// 没有升级版才用非升级版。两个实例都收到 hook，但只有被选中的那个会真的结算。
    /// </summary>
    public static TetrisFullHandPower? ResolveOneToSettle(Player player)
    {
        var id = ModelDb.Get(typeof(TetrisFullHandPower)).Id;
        var all = player.Creature.GetPowerInstances(id).OfType<TetrisFullHandPower>().ToList();
        return all.FirstOrDefault(p => p.Upgraded) ?? all.FirstOrDefault();
    }

    /// <summary>
    /// 结算：消耗所有手牌（含手中的俄罗斯方块）、抽牌、获得能量、
    /// 消耗俄罗斯方块本身（打出中→直接消耗；弃牌堆→直接消耗）、弃牌堆所有方块返回手牌。
    /// </summary>
    public async Task<bool> Settle(PlayerChoiceContext choiceContext, Player player, Tetris? tetrisCard)
    {
        var data = GetInternalData<Data>();
        if (data.Triggered)
        {
            return false;
        }

        data.Triggered = true;
        var hand = PileType.Hand.GetPile(player);

        // 消耗所有手牌（含手中的俄罗斯方块）。
        foreach (var c in hand.Cards.ToList())
        {
            await CardCmd.Exhaust(choiceContext, c);
        }

        await CardPileCmd.Draw(choiceContext, data.Cards, player);
        await PlayerCmd.GainEnergy(data.Energy, player);

        // 弃牌堆的所有方块返回手牌（含溢出方块）。
        // 溢出方块在 Tetris.OnPlay 里因为手牌已满被放进了弃牌堆（targetPile = Discard），
        // 卡面写的是「将弃牌堆的所有方块返回手牌」，所以这一趟不能省。
        foreach (var block in PileType.Discard.GetPile(player).Cards.Where(BlockCards.IsBlock).ToList())
        {
            await CardPileCmd.Add(block, PileType.Hand, CardPilePosition.Random, this);
        }

        // 本回合打出过的俄罗斯方块全部消耗（打出堆 + 弃牌堆；手中的已随“消耗所有手牌”一并带走）。
        var tetrisCards = PileType.Play.GetPile(player).Cards.OfType<Tetris>()
            .Concat(PileType.Discard.GetPile(player).Cards.OfType<Tetris>())
            .ToList();
        if (tetrisCard != null && tetrisCard.Pile?.Type is PileType.Play or PileType.Discard)
        {
            tetrisCards.Add(tetrisCard);
        }

        foreach (var tetris in tetrisCards.Distinct().ToList())
        {
            await CardCmd.Exhaust(choiceContext, tetris);
        }

        // 触发一次满手牌结算后，清除所有其它的满手牌结算效果（含另一个档位的）。
        foreach (var other in Owner.GetPowerInstances(ModelDb.Get(typeof(TetrisFullHandPower)).Id).ToList())
        {
            if (other != this)
            {
                await PowerCmd.Remove(other);
            }
        }

        await PowerCmd.Remove(this);
        return true;
    }

    // 打出完成后，本回合后续任意卡进入手牌使手牌达到上限时触发。
    public override async Task AfterCardChangedPiles(CardModel card, PileType oldPileType, AbstractModel? clonedBy)
    {
        if (CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var player = Owner.Player;
        if (player == null)
        {
            return;
        }

        var hand = PileType.Hand.GetPile(player);
        if (card.Pile != hand || oldPileType == PileType.Hand || hand.Cards.Count < CardPile.MaxCardsInHand)
        {
            return;
        }

        // 俄罗斯方块打出过程中（塞方块）不触发：由 OnPlay 统一结算，保证溢出方块先入弃牌堆。
        if (PileType.Play.GetPile(player).Cards.Any(c => c is Tetris))
        {
            return;
        }

        var tetrisCard = hand.Cards.OfType<Tetris>().FirstOrDefault();

        // 两个档位同时存在时，只让升级版结算（无论打出顺序）。
        if (ResolveOneToSettle(player) != this)
        {
            return;
        }

        await Settle(new ThrowingPlayerChoiceContext(), player, tetrisCard);
    }
    public override async Task AfterSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side, IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner))
        {
            return;
        }

        await PowerCmd.Remove(this);
    }
}

/// <summary>
/// 节奏游戏！：0 费能力（衍生·小游戏）。回合开始时，将随机 1~4 张方块加入你的手牌。
/// 回合结束时，消耗所有方块，并对所有敌人造成 24 点伤害；每以该法消耗一张方块，该伤害降低 6 点（升级：30 伤、-5）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class RhythmGame : ModCardTemplate
{
    public RhythmGame() : base(1, CardType.Power, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    // 衍生牌预览：四种方块。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => BlockCards.Tips();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Damage", 18),  // 升级 20
        new DynamicVar("PerBlock", 6)  // 升级 5
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<RhythmGamePower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Damage"].UpgradeValueBy(2);    // 18 -> 20
        DynamicVars["PerBlock"].UpgradeValueBy(-1); // 6 -> 5
    }
}

[RegisterPower]
public sealed class RhythmGamePower : ModPowerTemplate
{
    private class Data
    {
        public int Damage = 0;     // 叠加后的基础伤害
        public int PerBlock = 0;   // 叠加后的每方块降低
        public CardModel? SourceCard;
    }

    public override PowerType Type => PowerType.Buff;

    // 叠加：方块数不叠加（仍随机 1~4）；基础伤害与每方块降低伤害叠加（无论升级与否）。
    public override PowerStackType StackType => PowerStackType.Counter;

    // 右下角数字显示「这张能力这次回合结束将要造成的伤害」（= 基础总伤害 - 当前方块数 × 每方块降低），
    // 而不是叠加层数。层数仍然决定基础伤害（见 AfterPowerAmountChanged）。
    public override int DisplayAmount
    {
        get
        {
            var data = GetInternalData<Data>();
            if (data.Damage == 0)
            {
                return 0;
            }

            var player = Owner.Player;
            if (player == null)
            {
                return Math.Max(0, data.Damage);
            }

            var blocks = (CardPile.Get(PileType.Hand, player)?.Cards.Count(BlockCards.IsBlock) ?? 0)
                + (CardPile.Get(PileType.Discard, player)?.Cards.Count(BlockCards.IsBlock) ?? 0);
            return Math.Max(0, data.Damage - blocks * data.PerBlock);
        }
    }

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/rhythm_game_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/rhythm_game_power.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("DamageTotal", 0),
        new DynamicVar("PerBlockTotal", 0)
    ];

    protected override object InitInternalData() => new Data();

    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        var data = GetInternalData<Data>();
        for (int i = 0; i < (int)amount; i++)
        {
            data.Damage += cardSource?.IsUpgraded == true ? 20 : 18;
            data.PerBlock += cardSource?.IsUpgraded == true ? 5 : 6;
            data.SourceCard ??= cardSource;
        }

        DynamicVars["DamageTotal"].BaseValue = data.Damage;
        DynamicVars["PerBlockTotal"].BaseValue = data.PerBlock;
        InvokeDisplayAmountChanged();
        await Task.CompletedTask;
    }

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        // 随机 1~4 张方块。
        var player = Owner.Player;
        if (player == null)
        {
            return;
        }

        var count = player.RunState.Rng.CombatCardSelection.NextInt(1, 5);
        for (int i = 0; i < count; i++)
        {
            var block = BlockCards.CreateRandom(combatState, player);
            await CardPileCmd.AddGeneratedCardToCombat(block, PileType.Hand, player);
        }

        // 方块数变了 → 右下角“将要造成的伤害”要跟着变。
        InvokeDisplayAmountChanged();
    }

    public override async Task AfterSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var player = Owner.Player;
        if (player == null)
        {
            return;
        }

        // 回合末先弃牌后结算：方块可能已在弃牌堆（状态牌无法打出），从手牌+弃牌堆收集。
        var blocks = PileType.Hand.GetPile(player).Cards.Where(BlockCards.IsBlock).ToList();
        blocks.AddRange(PileType.Discard.GetPile(player).Cards.Where(BlockCards.IsBlock));
        foreach (var block in blocks)
        {
            await CardCmd.Exhaust(choiceContext, block);
        }

        // 全体伤害（每消耗一张方块降低）。
        var data = GetInternalData<Data>();
        var damage = Math.Max(0, data.Damage - blocks.Count * data.PerBlock);
        var combatState = Owner.CombatState;
        if (combatState != null && damage > 0 && data.SourceCard != null)
        {
            // 能力伤害走原版形状：直接 CreatureCmd.Damage + ValueProp.Unpowered（不吃力量/活力/虚弱/易伤）。
            await CreatureCmd.Damage(choiceContext, combatState.HittableEnemies, damage,
                ValueProp.Unpowered, Owner, data.SourceCard, null);
        }
    }
}

/// <summary>
/// 吃豆人！：0 费能力（衍生·小游戏）。将 4 张特定诅咒放入你的手牌（苦恼、睡眠不佳、羞耻、贪婪）。
/// 回合开始时，自动打出 1 张疯狂进食并将其消耗，然后随机消耗你的 1 张诅咒牌。
/// 若你没有诅咒牌，改为将一张富足加入你的手牌（升级：富足+）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class PacMan : ModCardTemplate
{
    public PacMan() : base(0, CardType.Power, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：苦恼、睡眠不佳、羞耻、贪婪。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<Writhe>(),
        HoverTipFactory.FromCard<PoorSleep>(),
        HoverTipFactory.FromCard<Shame>(),
        HoverTipFactory.FromCard<Greed>()
    ];

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 4 张特定诅咒放入手牌。
        foreach (var type in new[] { typeof(Writhe), typeof(PoorSleep), typeof(Shame), typeof(Greed) })
        {
            var curse = combatState.CreateCard((CardModel)ModelDb.Get(type), Owner);
            await CardPileCmd.AddGeneratedCardToCombat(curse, PileType.Hand, Owner);
        }

        await PowerCmd.Apply<PacManPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
    }
}

[RegisterPower]
public sealed class PacManPower : ModPowerTemplate
{
    private class PacData
    {
        public bool Upgraded;
    }

    // 多张吃豆人独立生效。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    protected override object InitInternalData() => new PacData();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new StringVar("FrenzyName"),
        new StringVar("WinName")
    ];

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        var upgraded = cardSource?.IsUpgraded == true;
        GetInternalData<PacData>().Upgraded = upgraded;
        // 描述中的卡名随升级变化：疯狂进食(+)、WIN！(+)。
        // 注意：疯狂进食的原版类是 FeedingFrenzy（Maul＝「撕咬」是另一张牌，写错会让侧栏显示成撕咬）。
        ((StringVar)DynamicVars["FrenzyName"]).StringValue = upgraded
            ? ModelDb.Card<FeedingFrenzy>().Title + "+"
            : ModelDb.Card<FeedingFrenzy>().Title;
        // 没诅咒时给的牌：WIN！（WinCard），升级给 WIN！+。
        ((StringVar)DynamicVars["WinName"]).StringValue = upgraded
            ? ModelDb.Card<WinCard>().Title + "+"
            : ModelDb.Card<WinCard>().Title;
        return Task.CompletedTask;
    }

    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/pac_man_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/pac_man_power.png");

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var player = Owner.Player;
        if (player == null)
        {
            return;
        }

        var upgraded = GetInternalData<PacData>().Upgraded;
        var ctx = new ThrowingPlayerChoiceContext();

        // 先检测诅咒牌：「没有诅咒」= 抽牌堆 + 手牌 + 弃牌堆**全都没有**诅咒，
        // 只要三堆里任意一张是诅咒就算有。
        // 注意用 CardPile.Get（PileType.X.GetPile 在非战斗时会抛异常，Get 会返回 null）。
        var curses = new List<CardModel>();
        foreach (var pileType in new[] { PileType.Draw, PileType.Hand, PileType.Discard })
        {
            var pile = CardPile.Get(pileType, player);
            if (pile == null)
            {
                continue;
            }

            curses.AddRange(pile.Cards.Where(c => c.Type == CardType.Curse));
        }

        // 三堆都没诅咒 → 不给疯狂进食，直接给 WIN！（升级版给 WIN！+）。
        if (curses.Count == 0)
        {
            var win = combatState.CreateCard(ModelDb.Card<WinCard>(), player);
            if (upgraded)
            {
                CardCmd.Upgrade(win);
            }

            await CardPileCmd.AddGeneratedCardToCombat(win, PileType.Hand, player);
            return;
        }

        // 有诅咒牌：直接打出 1 张疯狂进食（升级版吃豆人给升级版）。
        // 关键：用 CreateDupe 而不是原牌 —— 复制品的 IsDupe 会走
        // CardModel.GetResultLocationForCardPlay 的 PileType.None 分支，
        // 打完由 CardPileCmd.RemoveFromCombat 从战斗里删掉，
        // 既不进弃牌堆也不进消耗堆（机制同原版历史课 HistoryCourse）。
        var frenzy = combatState.CreateCard(ModelDb.Card<FeedingFrenzy>(), player);
        if (upgraded)
        {
            CardCmd.Upgrade(frenzy);
        }

        await CardCmd.AutoPlay(ctx, frenzy.CreateDupe(player), null);

        // 然后随机消耗 1 张诅咒牌（在手牌里的直接消耗，在抽牌堆/弃牌堆里的会被拉出来消耗）。
        var curse = player.RunState.Rng.CombatCardSelection.NextItem(curses);
        if (curse != null)
        {
            await CardCmd.Exhaust(ctx, curse);
        }
    }
}

/// <summary>
/// 植物大战僵尸：0 费技能（衍生·小游戏）。从随机两张特定牌中选择一张放入你的手牌，下回合将另一张牌放入你的手牌；
/// 它们在本场战斗中可以被免费打出一次。消耗（升级：升级版）。
/// 左侧：凌虐、添柴、播种、腐败、净化、你好世界、坚韧之环。
/// 右侧：疯狂进食、撕咬、扯碎、野性、不死、腐化、死者苏生。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class PlantsVsZombies : ModCardTemplate
{
    private static readonly Type[] Left =
    [
        typeof(Mangle), typeof(Stoke), typeof(Sow), typeof(Putrefy), typeof(Purity), typeof(HelloWorld), typeof(ToricToughness)
    ];

    private static readonly Type[] Right =
    [
        typeof(FeedingFrenzy), typeof(Maul), typeof(TearAsunder), typeof(Feral), typeof(Undeath), typeof(Corruption), typeof(Reanimate)
    ];

    public PlantsVsZombies() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    // 侧栏：说明左右两边分别会出现什么特定牌。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_PLANTS_VS_ZOMBIES.sidebar"))
    ];

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    // 描述里的「它们的耗能在下次打出前变为 {Energy:energyIcons()}」需要一个 Energy 变量才能解析
    // （否则 SmartFormat 报 “No source extension could handle the selector named Energy”）。
    // 这里给 0：EnergyIconsFormatter 对 0 会输出「0 + 能量图标」。
    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar(0),
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var left = Owner.RunState.Rng.CombatCardSelection.NextItem(Left) ?? Left[0];
        var right = Owner.RunState.Rng.CombatCardSelection.NextItem(Right) ?? Right[0];

        var leftCard = combatState.CreateCard((CardModel)ModelDb.Get(left), Owner);
        var rightCard = combatState.CreateCard((CardModel)ModelDb.Get(right), Owner);
        if (IsUpgraded)
        {
            CardCmd.Upgrade(leftCard);
            CardCmd.Upgrade(rightCard);
        }

        var picked = (await CardSelectCmd.FromSimpleGrid(choiceContext, new List<CardModel> { leftCard, rightCard }, Owner,
            new CardSelectorPrefs(new LocString("card_selection", "TO_ADD_TO_HAND"), 1, 1))).FirstOrDefault();
        if (picked != null)
        {
            // 设计：它们在本场战斗中可以被免费打出一次（打出一次后恢复原耗费）。
            picked.EnergyCost.SetUntilPlayed(0);
            await CardPileCmd.AddGeneratedCardToCombat(picked, PileType.Hand, Owner);

            // 下回合另一张入手（每张植物大战僵尸独立：Instanced）。
            var other = picked == leftCard ? rightCard : leftCard;
            other.EnergyCost.SetUntilPlayed(0);
            var power = await PowerCmd.Apply<PlantsNextTurnPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
            if (power != null)
            {
                power.SetOtherCard(other);
            }
        }
    }

    protected override void OnUpgrade()
    {
        // 升级不再减费（费用升级前后都是 1）。
    }
}

[RegisterPower]
public sealed class PlantsNextTurnPower : ModPowerTemplate
{
    private class Data
    {
        public CardModel? Other;
    }

    // 每张植物大战僵尸独立生效（多张各自给各自的另一张）。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/plants_next_turn_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/plants_next_turn_power.png");

    protected override object InitInternalData() => new Data();

    // 描述里的卡名：显示实际要加入手牌的那张牌（升级则为升级版卡名）。
    protected override IEnumerable<DynamicVar> CanonicalVars => [new StringVar("Card")];

    public void SetOtherCard(CardModel other)
    {
        GetInternalData<Data>().Other = other;
        if (other != null)
        {
            ((StringVar)DynamicVars["Card"]).StringValue = other.Title;
        }
    }

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var other = GetInternalData<Data>().Other;
        if (other != null)
        {
            other.EnergyCost.SetUntilPlayed(0);
            await CardPileCmd.AddGeneratedCardToCombat(other, PileType.Hand, Owner.Player);
        }

        await PowerCmd.Remove(this);
    }
}
