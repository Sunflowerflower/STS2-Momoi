using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Enchantments;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.Nodes.CommonUi;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Models.Capabilities;
using STS2RitsuLib.Patching.Models;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 专注：1 费能力（罕见，升级 0 费）。**回合结束时**判定**本回合**：
/// 没打出过小游戏牌 → 构想数值 +1；没打出过构想 → 可选择最多构想数值张牌保留。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Focus : ModCardTemplate
{
    public Focus() : base(1, CardType.Power, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");


    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<FocusPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        // 升级：耗能 1 -> 0。
        EnergyCost.UpgradeBy(-1);
    }
}

[RegisterPower]
public sealed class FocusPower : ModPowerTemplate
{
    private class Data
    {
        /// <summary>本回合是否打出过小游戏牌 / 构想（回合结束时判定，回合结束后重置）。</summary>
        public bool PlayedMinigameThisTurn;
        public bool PlayedConceptThisTurn;
        public List<CardModel> Retained = new();
    }

    public override PowerType Type => PowerType.Buff;

    // 构想 +1 的效果可叠加（保留选择不叠加）。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/focus_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/focus_power.png");

    protected override object InitInternalData() => new Data();

    // 描述中的「可选择保留张数」实时显示（始终为当前构想数值最大值）。
    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("RetainCount", 0)
    ];

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner)
        {
            return;
        }

        var data = GetInternalData<Data>();
        if (MinigameSupport.IsMinigameCard(cardPlay.Card))
        {
            data.PlayedMinigameThisTurn = true;
        }

        if (cardPlay.Card is ConceptCard)
        {
            data.PlayedConceptThisTurn = true;
        }

        DynamicVars["RetainCount"].BaseValue = ConceptCounterCapability.GetMaxCountInHand(Owner);
    }

    // 保留选择必须在弃牌前（BeforeSideTurnEnd 在手牌弃置之前触发）。
    public override async Task BeforeSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var data = GetInternalData<Data>();
        var player = Owner.Player;

        // 本回合没打过构想：可选择最多构想数值张手牌保留（已有保留词条的牌不进入选项，默认保留）。
        if (!data.PlayedConceptThisTurn && player != null)
        {
            var concept = ConceptCounterCapability.GetMaxCountInHand(Owner);
            DynamicVars["RetainCount"].BaseValue = concept;
            if (concept > 0)
            {
                var picked = (await CardSelectCmd.FromHand(choiceContext, player,
                    new CardSelectorPrefs(new LocString("card_selection", "TO_RETAIN"), 0, concept)
                    {
                        Cancelable = true,
                        RequireManualConfirmation = true
                    },
                    c => !c.Keywords.Contains(CardKeyword.Retain), this)).ToList();
                foreach (var card in picked)
                {
                    card.LocalKeywords.Add(CardKeyword.Retain);
                    data.Retained.Add(card);
                }
            }
        }
    }

    public override async Task AfterSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var data = GetInternalData<Data>();
        var player = Owner.Player;

        // 本回合没打过小游戏牌：构想 +1（叠加：每层 +1）。
        if (!data.PlayedMinigameThisTurn && player != null)
        {
            for (int i = 0; i < Amount; i++)
            {
                await ConceptCounterCapability.AddCountToAllInHand(choiceContext, Owner, 1);
            }
        }

        // 回合结束，重置「本回合打出过」。
        data.PlayedMinigameThisTurn = false;
        data.PlayedConceptThisTurn = false;
    }

    public override Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner))
        {
            return Task.CompletedTask;
        }

        // 移除上一回合手动加的保留。
        var data = GetInternalData<Data>();
        foreach (var card in data.Retained)
        {
            if (card.Pile != null)
            {
                card.LocalKeywords.Remove(CardKeyword.Retain);
            }
        }

        data.Retained.Clear();
        return Task.CompletedTask;
    }
}

/// <summary>
/// 灵感爆发：1 费能力（罕见）。当你打出数值不低于 6 的构想后，于该回合结束后进行一个额外回合（升级：5）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Inspiration : ModCardTemplate
{
    public Inspiration() : base(1, CardType.Power, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Threshold", 6)  // 升级 5
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 升级前/升级后是两个独立能力：各自叠加添加「我的回合！」的张数，可同时触发。
        if (IsUpgraded)
        {
            await PowerCmd.Apply<InspirationUpgradedPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }
        else
        {
            await PowerCmd.Apply<InspirationPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }
    }

    // 侧栏：我的回合！。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<MyTurn>(IsUpgraded)
    ];

    protected override void OnUpgrade()
    {
        DynamicVars["Threshold"].UpgradeValueBy(-1);
        // 升级：耗能 1 -> 0。
        EnergyCost.UpgradeBy(-1);
    }
}

[RegisterPower]
public sealed class InspirationPower : ModPowerTemplate
{
    private class Data
    {
        public int PendingExtraTurns;  // 待进行的额外回合
    }

    public override PowerType Type => PowerType.Buff;

    // 叠加：每打出一张升级前的灵感爆发，多 1 个额外回合。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/inspiration_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/inspiration_power.png");

    protected override object InitInternalData() => new Data();

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card is not ConceptCard concept)
        {
            return;
        }

        // 升级前：数值不低于 6 → 添加我的回合！（叠加张数）。
        if (concept.GetOrCreateCapability<ConceptCounterCapability>().Count >= 6)
        {
            var combatState = Owner.CombatState;
            if (combatState != null)
            {
                for (int i = 0; i < Amount; i++)
                {
                    var myTurn = combatState.CreateCard(ModelDb.Card<MyTurn>(), Owner.Player);
                    await CardPileCmd.AddGeneratedCardToCombat(myTurn, PileType.Hand, Owner.Player);
                }
            }
        }
    }
}

/// <summary>灵感爆发（升级后）：数值不低于 5 的构想触发额外回合；与升级前能力独立叠加。</summary>
[RegisterPower]
public sealed class InspirationUpgradedPower : ModPowerTemplate
{
    private class Data
    {
        public int PendingExtraTurns;
    }

    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/inspiration_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/inspiration_power.png");

    protected override object InitInternalData() => new Data();

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card is not ConceptCard concept)
        {
            return;
        }

        // 升级后：数值不低于 5 → 添加我的回合！+（叠加张数）。
        if (concept.GetOrCreateCapability<ConceptCounterCapability>().Count >= 5)
        {
            var combatState = Owner.CombatState;
            if (combatState != null)
            {
                for (int i = 0; i < Amount; i++)
                {
                    var myTurn = combatState.CreateCard(ModelDb.Card<MyTurn>(), Owner.Player);
                    CardCmd.Upgrade(myTurn);
                    await CardPileCmd.AddGeneratedCardToCombat(myTurn, PileType.Hand, Owner.Player);
                }
            }
        }
    }
}

/// <summary>
/// 游戏王形态。：3 费能力（稀有）。回合开始时，将 1 张本场战斗中未获得过的随机小游戏牌加入你的手牌；
/// 获得全部后不再获得。本场战斗中首次打出一个牌名的小游戏牌后，获得 1 层缓冲（升级：2 层）。
/// 重复打出游戏王形态仅叠加每回合获得的未获得的数量以及首次打出获得的缓冲数。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class GameKingForm : ModCardTemplate
{
    public GameKingForm() : base(3, CardType.Power, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Buffer", 1)  // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 叠加：每张游戏王形态每回合获得 1 张未获得过的小游戏牌。
        await PowerCmd.Apply<GameKingFormPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Buffer"].UpgradeValueBy(1);
        // 升级：获得固有。
        LocalKeywords.Add(CardKeyword.Innate);
    }
}

[RegisterPower]
public sealed class GameKingFormPower : ModPowerTemplate
{
    private class Data
    {
        public HashSet<string> FirstPlayed = new();  // 已首次打出的牌名（含游戏牌，升级前后同一牌名）
        public int BufferOnFirst = 0;                // 每张牌首次打出获得的缓冲（叠加）
    }

    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/game_king_form_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/game_king_form_power.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("BufferPer", 0)  // 描述中显示叠加后的缓冲数
    ];

    // 右下角显示的是「实际获得的缓冲层数」（= BufferPer），不是叠加层数。
    public override int DisplayAmount => (int)DynamicVars["BufferPer"].BaseValue;

    protected override object InitInternalData() => new Data();

    // 叠加缓冲数（升级前 +1、升级后 +2）。
    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        var data = GetInternalData<Data>();
        data.BufferOnFirst += (int)amount * (cardSource?.IsUpgraded == true ? 2 : 1);
        DynamicVars["BufferPer"].BaseValue = data.BufferOnFirst;
        InvokeDisplayAmountChanged();
        await Task.CompletedTask;
    }

    // ===== 附魔池（按牌类型筛选；数值为 Amount，未列出的传 1）=====
    private static readonly Type[] EnchantAll =
        [typeof(Sown), typeof(Glam), typeof(Steady), typeof(PerfectFit), typeof(Slither), typeof(Spiral), typeof(Swift)];
    private static readonly Type[] EnchantAttack =
        [typeof(Instinct), typeof(Inky), typeof(Vigorous), typeof(Sharp), typeof(Corrupted)];
    private static readonly Type[] EnchantSkill =
        [typeof(Adroit), typeof(SoulsPower)];
    private static readonly Type[] EnchantPower =
        [typeof(SlumberingEssence)];

    private static readonly Dictionary<Type, int> EnchantAmounts = new()
    {
        [typeof(Vigorous)] = 3,  // 活力 3
        [typeof(Sharp)] = 3,     // 锋利 3
        [typeof(Adroit)] = 3,    // 伶俐 3
        [typeof(Swift)] = 2      // 迅速 2
    };

    // 生成的小游戏牌（含局内临时生成的游戏牌）→ 添加 1 个随机附魔。
    public override async Task AfterCardGeneratedForCombat(CardModel card, Player? creator)
    {
        await TryEnchantGenerated(card);
    }

    // 复制品进入战斗（轮回复制等）也算被生成：无附魔的复制品获得随机附魔，有附魔的继承不添加。
    public override async Task AfterCardEnteredCombat(CardModel card)
    {
        await TryEnchantGenerated(card);
    }

    private async Task TryEnchantGenerated(CardModel card)
    {
        if (CombatManager.Instance.IsOverOrEnding || Owner?.Player == null)
        {
            return;
        }

        if (card.Owner?.Creature != Owner)
        {
            return;  // 只处理自己生成/进入的牌
        }

        if (!MinigameSupport.IsMinigameCard(card))
        {
            return;  // 只处理小游戏牌（含游戏牌）
        }

        if (card.Enchantment != null)
        {
            return;  // 已有附魔（含复制品继承）：不再添加
        }

        var pool = card.Type switch
        {
            CardType.Attack => EnchantAll.Concat(EnchantAttack).ToArray(),
            CardType.Skill => EnchantAll.Concat(EnchantSkill).ToArray(),
            CardType.Power => EnchantAll.Concat(EnchantPower).ToArray(),
            _ => EnchantAll
        };

        // 先按 CanEnchant 过滤（如涡旋仅基础打击/防御、灵魂之力需要消耗），再从可用的里随机。
        var candidates = pool
            .Where(t => ((EnchantmentModel)ModelDb.Get(t)).CanEnchant(card))
            .ToList();
        if (candidates.Count == 0)
        {
            return;
        }

        var rng = Owner.Player.RunState.Rng.CombatCardSelection;
        var chosen = candidates[rng.NextInt(candidates.Count)];
        var amount = EnchantAmounts.TryGetValue(chosen, out var a) ? a : 1;
        CardCmd.Enchant(((EnchantmentModel)ModelDb.Get(chosen)).ToMutable(), card, amount);
    }

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || !MinigameSupport.IsMinigameCard(cardPlay.Card))
        {
            return;
        }

        if (CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        // 首次打出该牌名（含游戏牌）：获得缓冲。
        var data = GetInternalData<Data>();
        if (data.FirstPlayed.Add(cardPlay.Card.Id.Entry))
        {
            await PowerCmd.Apply<BufferPower>(choiceContext, Owner, data.BufferOnFirst, Owner, null);
        }
    }
}

/// <summary>
/// 得道多助：1 费能力（稀有）。回合开始时，将一张随机支援牌洗入你的抽牌堆（升级：固有 + 升级版）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class HelpFromMany : ModCardTemplate
{
    public HelpFromMany() : base(1, CardType.Power, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 升级前后都获得固有。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Innate };

    // 侧栏：支援牌清单（与集结同款）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_RALLY.sidebar2"))
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 升级前/升级后能力独立：升级后只与升级后叠加。
        if (IsUpgraded)
        {
            await PowerCmd.Apply<HelpFromManyUpgradedPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }
        else
        {
            await PowerCmd.Apply<HelpFromManyPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }
    }

    protected override void OnUpgrade()
    {
        // 升级：耗能 1 -> 0（固有升级前后都有）。
        EnergyCost.UpgradeBy(-1);
    }
}

[RegisterPower]
public sealed class HelpFromManyPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 升级前的能力独立叠加：只生成未升级的支援牌。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/help_from_many_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/help_from_many_power.png");

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        for (int i = 0; i < Amount; i++)
        {
            await GenerateSupport(combatState, false);
        }
    }

    protected async Task GenerateSupport(ICombatState combatState, bool upgraded)
    {
        // 支援牌池：柚子护航、开发者协同：绿、来自勇者的加护、来自算术使的关爱 + 工程部/真理部/C&C 基础选项。
        // 额外选项（千寻/时）在解锁后才进入支援池。
        var pool = new List<Type>(MinigameSupport.AllSupportCards);
        if (RunStats.VeritasPicked.Count >= 3)
        {
            pool.Add(typeof(MomoiSupportChihiro));
        }

        if (RunStats.CnCPicked.Count >= 4)
        {
            pool.Add(typeof(MomoiSupportToki));
        }

        // 每次生成前检测当前卡组（抽牌堆+手牌+弃牌堆）已有的支援牌，从剩下的里随机；全都有则完全随机。
        // 用 CardPile.Get 而不是 GetPile：GetPile 在“没在战斗里”时会抛 InvalidOperationException。
        var player = Owner.Player;
        if (player == null)
        {
            return;
        }

        var owned = new HashSet<string>();
        foreach (var pileType in new[] { PileType.Draw, PileType.Hand, PileType.Discard })
        {
            foreach (var card in CardPile.Get(pileType, player)?.Cards ?? Enumerable.Empty<CardModel>())
            {
                if (MinigameSupport.IsSupportCard(card))
                {
                    owned.Add(card.Id.Entry);
                }
            }
        }

        var remaining = pool
            .Where(t => !owned.Contains(((CardModel)ModelDb.Get(t)).Id.Entry))
            .ToList();
        var source = remaining.Count > 0 ? remaining : pool;

        var type = player.RunState.Rng.CombatCardSelection.NextItem(source) ?? source[0];
        var supportCard = combatState.CreateCard((CardModel)ModelDb.Get(type), player);
        if (upgraded)
        {
            CardCmd.Upgrade(supportCard);
        }

        await CardPileCmd.AddGeneratedCardToCombat(supportCard, PileType.Draw, Owner.Player, CardPilePosition.Random);
    }
}

/// <summary>得道多助（升级）：只生成升级过的支援牌，与升级前的能力独立叠加。</summary>
[RegisterPower]
public sealed class HelpFromManyUpgradedPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 升级后的能力独立叠加：只生成升级过的支援牌。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/help_from_many_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/help_from_many_power.png");

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        for (int i = 0; i < Amount; i++)
        {
            await GenerateSupport(combatState, true);
        }
    }

    protected async Task GenerateSupport(ICombatState combatState, bool upgraded)
    {
        var pool = new List<Type>(MinigameSupport.AllSupportCards);
        if (RunStats.VeritasPicked.Count >= 3)
        {
            pool.Add(typeof(MomoiSupportChihiro));
        }

        if (RunStats.CnCPicked.Count >= 4)
        {
            pool.Add(typeof(MomoiSupportToki));
        }

        // CardPile.Get：非战斗时返回 null 而不是抛异常。
        var player = Owner.Player;
        if (player == null)
        {
            return;
        }

        var owned = new HashSet<string>();
        foreach (var pileType in new[] { PileType.Draw, PileType.Hand, PileType.Discard })
        {
            foreach (var card in CardPile.Get(pileType, player)?.Cards ?? Enumerable.Empty<CardModel>())
            {
                if (MinigameSupport.IsSupportCard(card))
                {
                    owned.Add(card.Id.Entry);
                }
            }
        }

        var remaining = pool
            .Where(t => !owned.Contains(((CardModel)ModelDb.Get(t)).Id.Entry))
            .ToList();
        var source = remaining.Count > 0 ? remaining : pool;

        var type = player.RunState.Rng.CombatCardSelection.NextItem(source) ?? source[0];
        var supportCard = combatState.CreateCard((CardModel)ModelDb.Get(type), player);
        if (upgraded)
        {
            CardCmd.Upgrade(supportCard);
        }

        await CardPileCmd.AddGeneratedCardToCombat(supportCard, PileType.Draw, Owner.Player, CardPilePosition.Random);
    }
}

/// <summary>
/// 重整旗鼓：4 费能力（先古）。恢复已损生命的 10% 的生命并获得等量的活力。
/// 当你打出构想后，重复此效果。当生命值低于 25% 时，立即将此牌打出，并额外获得 1 层无实体。
/// （升级：3 费；获得时默认为升级过的。）
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
[RegisterDustyTomeCard(typeof(STS2_MomoiCharacter))]
public sealed class RallyAgain : ModCardTemplate
{
    public RallyAgain() : base(4, CardType.Power, CardRarity.Ancient, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 低生命自动打出：游戏开始时或生命值发生变化（掉血）后，若生命低于最大生命的 25% 就立即自动打出
    // （不限敌方回合，包括自己的回合；并额外获得 1 层无实体）。
    // 该效果可多次触发：每张未打出过的重整旗鼓都会触发一次（打出后即消耗，不会重复触发）。
    // 只处理战斗内的牌实例（手牌/抽牌堆/弃牌堆/打出堆）——牌组中的对应卡不应被打出。
    private async Task TryAutoPlayIfLowHp(PlayerChoiceContext choiceContext)
    {
        var me = Owner.Creature;
        var combat = me.CombatState;
        if (combat == null)
        {
            return;
        }

        if (Pile == null || Pile.Type is PileType.Deck or PileType.None)
        {
            return;  // 牌组中的卡不应被打出；已打出（PileType.None）的也不再触发。
        }

        if (CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        if (me.CurrentHp > me.MaxHp / 4)
        {
            return;  // 低于最大生命的 25% 才触发
        }

        await PowerCmd.Apply<IntangiblePower>(choiceContext, me, 1, me, this);
        await CardCmd.AutoPlay(choiceContext, this, null);  // 目标 null 会随机合法目标
    }

    // 游戏开始时：生命已低于 25% 则立即自动打出。
    public override async Task BeforeCombatStart()
    {
        await TryAutoPlayIfLowHp(new ThrowingPlayerChoiceContext());
    }

    // 生命值发生变化（受到伤害）后：掉血且生命低于 25% 时自动打出（不限敌方回合）。
    public override async Task AfterDamageReceived(
        PlayerChoiceContext choiceContext,
        Creature target,
        DamageResult result,
        ValueProp props,
        Creature? dealer,
        CardModel? cardSource)
    {
        var me = Owner.Creature;
        if (target != me)
        {
            return;
        }

        if (result.UnblockedDamage <= 0)
        {
            return;  // 生命值实际发生变化（掉血）才检查
        }

        await TryAutoPlayIfLowHp(choiceContext);
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await Restore(choiceContext);
        await PowerCmd.Apply<RallyAgainPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    /// <summary>恢复已损生命 10% 并获得等量活力。</summary>
    public async Task Restore(PlayerChoiceContext choiceContext)
    {
        var creature = Owner.Creature;
        var missing = creature.MaxHp - creature.CurrentHp;
        if (missing <= 0)
        {
            return;
        }

        var heal = Math.Max(1, (int)(missing * 0.1m));
        await CreatureCmd.Heal(creature, heal);
        await PowerCmd.Apply<VigorPower>(choiceContext, creature, heal, creature, this);
    }

    protected override void OnUpgrade()
    {
        EnergyCost.UpgradeBy(-1);
    }
}

[RegisterPower]
public sealed class RallyAgainPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 无法叠加：每张重整旗鼓独立存在，打出构想后依次触发。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/rally_again_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/rally_again_power.png");

    private class Data
    {
        public RallyAgain? SourceCard;
        public bool Triggered;
    }

    protected override object InitInternalData() => new Data();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("HealPer", 0),
        new DynamicVar("VigorPer", 0)
    ];

    /// <summary>即将回复的生命值（= 即将获得的活力），每次读取都按当前生命现算。</summary>
    public int PendingHeal
    {
        get
        {
            var missing = Owner.MaxHp - Owner.CurrentHp;
            return missing <= 0 ? 0 : Math.Max(1, (int)(missing * 0.1m));
        }
    }

    // 右下角计数器：实时显示“即将回复的生命值”，而不是上一次回复的量。
    // 原版 UI 只在 InvokeDisplayAmountChanged 时重读 DisplayAmount，所以委托/属性变化不会自动刷新。
    public override int DisplayAmount => PendingHeal;

    private void RefreshDisplayVars()
    {
        var heal = PendingHeal;
        DynamicVars["HealPer"].BaseValue = heal;
        DynamicVars["VigorPer"].BaseValue = heal;
        InvokeDisplayAmountChanged();
    }

    // 挨打 / 回血都会改当前生命 → 立刻刷新数字（原版 HardenedShellPower / FeralPower 同款）。
    public override Task AfterCurrentHpChanged(Creature creature, decimal delta)
    {
        if (creature == Owner)
        {
            RefreshDisplayVars();
        }

        return Task.CompletedTask;
    }

    // 最大生命变化（加最大生命的遗物/药水）也会改期望值；事件没有退订口，只能在移除时退。
    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        GetInternalData<Data>().SourceCard = cardSource as RallyAgain;
        if (Owner != null)
        {
            Owner.MaxHpChanged += OnOwnerMaxHpChanged;
        }

        RefreshDisplayVars();
        return Task.CompletedTask;
    }

    public override Task AfterRemoved(Creature oldOwner)
    {
        oldOwner.MaxHpChanged -= OnOwnerMaxHpChanged;
        return Task.CompletedTask;
    }

    private void OnOwnerMaxHpChanged(int oldValue, int newValue) => RefreshDisplayVars();

    // 打出构想后重复回复效果。
    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card is not ConceptCard)
        {
            return;
        }

        if (CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var source = GetInternalData<Data>().SourceCard;
        if (source != null)
        {
            await source.Restore(choiceContext);
        }

        RefreshDisplayVars();
    }

    // 生命降低后低于 25% 时立即打出（可插入敌人多段攻击之间）。
    public override async Task AfterDamageReceived(PlayerChoiceContext choiceContext, Creature target, DamageResult result,
        ValueProp props, Creature? dealer, CardModel? cardSource)
    {
        if (target != Owner || CombatManager.Instance.IsOverOrEnding || GetInternalData<Data>().Triggered)
        {
            return;
        }

        if (Owner.CurrentHp * 4 >= Owner.MaxHp)   // 25%（原 20%）
        {
            return;
        }

        GetInternalData<Data>().Triggered = true;
        var source = GetInternalData<Data>().SourceCard;
        if (source != null && source.Pile != null)
        {
            // 用真实的 choiceContext（同上：Throwing 版在需要选择时会抛）。
            await PowerCmd.Apply<IntangiblePower>(choiceContext, Owner, 1, Owner, null);
            await CardCmd.AutoPlay(choiceContext, source, null);
        }
    }
}

/// <summary>
/// 双线叙事：1 费技能（先古）。固有；使构想的数值加 2；选择 1 张构想复制，
/// 给被复制的那张原构想添加 1 层重放（已有重放则次数 +1，写法同原版重构 Transfigure 的 BaseReplayCount++），
/// 然后为复制品附魔灵魂之力。消耗（升级：0 费）。「剧情推进！」变为的先古牌。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class DualNarrative : ModCardTemplate
{
    public DualNarrative() : base(1, CardType.Skill, CardRarity.Ancient, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：构想 + 重放说明。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<ConceptCard>(),
        HoverTipFactory.Static(StaticHoverTip.ReplayStatic)
    ];

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Innate, CardKeyword.Exhaust };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        var combatState = Owner.Creature.CombatState;
        if (player == null || combatState == null)
        {
            return;
        }

        // 使构想的数值加 2。
        await ConceptCounterCapability.AddCountToAllInHand(choiceContext, Owner.Creature, 2);

        // 选择 1 张手牌中的构想复制（没有构想就什么都不做）。
        var picked = (await CardSelectCmd.FromHand(choiceContext, player,
            new CardSelectorPrefs(new LocString("card_selection", "TO_CLONE_CONCEPT"), 1, 1),
            c => c is ConceptCard, this)).FirstOrDefault();
        if (picked == null)
        {
            return;
        }

        // 复制的目标 = 被选中的那张**原构想**：加 1 层重放（已有重放则次数 +1）。
        picked.BaseReplayCount++;

        // 复制品：沿用原构想的数值，附魔灵魂之力，**不加**重放。
        var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), Owner);
        concept.GetOrCreateCapability<ConceptCounterCapability>().SetCount(
            picked.GetOrCreateCapability<ConceptCounterCapability>().Count);
        CardCmd.Enchant<SoulsPower>(concept, 1);
        await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, Owner);
    }

    protected override void OnUpgrade()
    {
        EnergyCost.UpgradeBy(-1);
    }
}

/// <summary>
/// 旅行异蛙：1 费技能（罕见）。获得 6 点格挡；这张牌的数值-2；
/// 这张牌每进入过一次弃牌堆或抽牌堆，数值+2（升级：7 格挡、+3）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class TravelFrog : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public TravelFrog() : base(1, CardType.Skill, CardRarity.Common, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 游戏牌：不可被临时添加，但被视为小游戏牌。
    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.FullGameTag };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(6m, ValueProp.Move),    // 升级 6（升级只加每堆数值）
        new DynamicVar("PerPile", 2)   // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);
        // 这张牌的数值-2。
        DynamicVars["Block"].BaseValue -= 2;
    }

    protected override void OnUpgrade()
    {
        DynamicVars["PerPile"].UpgradeValueBy(1);
    }

    // 每进入一次弃牌堆或抽牌堆，格挡数值 +2（升级 +3）。
    public override async Task AfterCardChangedPiles(CardModel card, PileType oldPileType, AbstractModel? clonedBy)
    {
        if (card != this || card.Pile?.Type is not (PileType.Discard or PileType.Draw))
        {
            return;
        }

        DynamicVars["Block"].BaseValue += DynamicVars["PerPile"].BaseValue;
        await Task.CompletedTask;
    }
}

/// <summary>
/// 传送门悖论其一：1 费技能（罕见）。将弃牌堆的 1 张牌洗入抽牌堆；
/// 本场战斗中，当选择的这张牌进入弃牌堆时（无论以何种方式），立即将其洗入抽牌堆，持续 15 次。
/// 重复选择同一张牌会叠加次数。升级：0 费。与其二配合可无限循环（15 次限制防卡死）。
/// </summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class PortalParadoxOne : ModCardTemplate
{
    public PortalParadoxOne() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        if (player == null)
        {
            return;
        }

        // 选择弃牌堆的 1 张牌：给它挂上传送门标记（方向一），然后将其洗入抽牌堆。
        var discardPile = PileType.Discard.GetPile(player);
        if (discardPile.Cards.Count > 0)
        {
            var picked = (await CardSelectCmd.FromCombatPile(choiceContext, discardPile, player,
                new CardSelectorPrefs(new LocString("card_selection", "TO_TRANSFORM"), 1, 1))).FirstOrDefault();
            if (picked != null)
            {
                picked.GetOrCreateCapability<PortalCapability>().AddOne(15);
                await CardPileCmd.Add(picked, PileType.Draw, CardPilePosition.Random, this);
            }
        }
    }

    protected override void OnUpgrade()
    {
        // 升级：获得保留。
        LocalKeywords.Add(CardKeyword.Retain);
    }
}

/// <summary>
/// 传送门悖论其二：将抽牌堆的 1 张牌放入弃牌堆；本场战斗中，当选择的这张牌进入抽牌堆时（无论以何种方式），
/// 立即将其放入弃牌堆，持续 15 次。重复选择同一张牌会叠加次数。升级：0 费。
/// </summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class PortalParadoxTwo : ModCardTemplate
{
    public PortalParadoxTwo() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        if (player == null)
        {
            return;
        }

        // 选择抽牌堆的 1 张牌：给它挂上传送门标记（方向二），然后将其放入弃牌堆。
        var drawPile = PileType.Draw.GetPile(player);
        if (drawPile.Cards.Count > 0)
        {
            var picked = (await CardSelectCmd.FromCombatPile(choiceContext, drawPile, player,
                new CardSelectorPrefs(new LocString("card_selection", "TO_DISCARD"), 1, 1))).FirstOrDefault();
            if (picked != null)
            {
                picked.GetOrCreateCapability<PortalCapability>().AddTwo(15);
                await CardCmd.Discard(choiceContext, picked);
            }
        }
    }

    protected override void OnUpgrade()
    {
        // 升级：获得保留。
        LocalKeywords.Add(CardKeyword.Retain);
    }
}

/// <summary>传送门标记（挂在被选择的牌上）：两个方向独立计数，重复选择叠加次数。</summary>
public enum PortalDirection
{
    One,  // 进入弃牌堆 → 洗入抽牌堆（随机位置）
    Two   // 进入抽牌堆 → 放入弃牌堆
}

[RegisterModelCapability]
public sealed class PortalCapability : CardCapability
{
    public int OneMoves;
    public int TwoMoves;

    public void AddOne(int moves) => OneMoves += moves;

    public void AddTwo(int moves) => TwoMoves += moves;

    // 被选择的牌以任何方式进入弃牌堆/抽牌堆时触发（含手动打出、洗牌、另一张悖论移动等）。
    // 两个方向同时存在时形成循环：弃牌堆→抽牌堆→弃牌堆→…（每方向 15 次上限，防卡死）。
    // 不加防递归标记：计数上限本身就能终止循环（否则嵌套移动会被跳过，循环无法形成）。
    public override async Task AfterCardChangedPiles(CardModel card, PileType oldPileType, AbstractModel? clonedBy)
    {
        if (card != Owner)
        {
            return;
        }

        var pileType = card.Pile?.Type;
        if (pileType == PileType.Discard && OneMoves > 0)
        {
            OneMoves--;
            await CardPileCmd.Add(card, PileType.Draw, CardPilePosition.Random, this);
        }
        else if (pileType == PileType.Draw && TwoMoves > 0)
        {
            TwoMoves--;
            await CardPileCmd.Add(card, PileType.Discard, CardPilePosition.Random, this);
        }
    }
}


/// <summary>
/// 我的回合！：1 费技能（衍生）。选择 1 张牌添加保留（升级 2 张），本回合结束后额外获得一回合，结束你的回合。消耗。
/// </summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class MyTurn : ModCardTemplate
{
    public MyTurn() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Cards", 1)  // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        if (player != null)
        {
            // 先选择牌添加保留（已有保留词条的牌不进入选项）。
            var picked = (await CardSelectCmd.FromHand(choiceContext, player,
                new CardSelectorPrefs(new LocString("card_selection", "TO_RETAIN"), 0, DynamicVars["Cards"].IntValue)
                {
                    Cancelable = true,
                    RequireManualConfirmation = true
                },
                c => !c.Keywords.Contains(CardKeyword.Retain), this)).ToList();
            foreach (var card in picked)
            {
                card.LocalKeywords.Add(CardKeyword.Retain);
            }
        }

        // 获得额外回合的效果。
        await PowerCmd.Apply<MyTurnPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);

        // 最后结束回合。
        PlayerCmd.EndTurn(Owner, canBackOut: false);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Cards"].UpgradeValueBy(1);
    }
}

/// <summary>我的回合！的额外回合：本回合结束后获得一回合。该效果无法叠加。</summary>
[RegisterPower]
public sealed class MyTurnPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 原版额外回合叠层（参考 AmbergrisPower）：
    // 层数 = 还能拿几次额外回合；每次结算（含重放）叠 1 层，每个额外回合结束扣 1 层。
    public override PowerStackType StackType => PowerStackType.Counter;

    // 右下角显示剩余额外回合数（= Amount）。
    public override int DisplayAmount => Amount;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/my_turn_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/my_turn_power.png");

    public override bool ShouldTakeExtraTurn(Player player)
    {
        return Amount > 0 && player == Owner.Player;
    }

    public override async Task AfterTakingExtraTurn(Player player)
    {
        if (player == Owner.Player)
        {
            await PowerCmd.Decrement(this);
        }
    }
}
