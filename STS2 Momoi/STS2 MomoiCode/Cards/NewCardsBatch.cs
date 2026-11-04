using System;
using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2RitsuLib.Models.Capabilities;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;
using STS2_Momoi.Diagnostics;

namespace STS2_Momoi.Cards;

/// <summary>
/// 王道：3 费攻击（稀有）。造成 27 点伤害；若构想的数值不低于 1，使构想数值 -1 并将此牌返回你的手牌，
/// 此牌的耗能在下一次打出前减少 3（升级：34 点伤害）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class KinglyWay : ModCardTemplate
{
    public KinglyWay() : base(3, CardType.Attack, CardRarity.Rare, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：构想。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<ConceptCard>()
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(27m),  // 升级 34
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new EnergyVar("CostReduce", 3)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        ArgumentNullException.ThrowIfNull(cardPlay.Target);

        await MomoiSovereignStyle.Apply(
                DamageCmd.Attack(DynamicVars.CalculatedDamage)
                    .FromCard(this, cardPlay)
                    .Targeting(cardPlay.Target))
            .Execute(choiceContext);

        // 若构想的数值不低于 1：所有构想 -1，本牌回手并减费 3（直到下一次打出）。
        if (ConceptCounterCapability.SpendOneFromAllInHand(Owner.Creature))
        {
            await CardPileCmd.Add(this, PileType.Hand);

            // 注意：卡牌打出流程结尾会调用 EnergyCost.AfterCardPlayedCleanup() 清掉所有
            // "直到打出" 的修正，因此必须在 Played 事件（清理之后触发）里再挂上减费。
            var rebate = this.GetOrCreateCapability<KinglyWayRebateCapability>();
            rebate.Pending = DynamicVars["CostReduce"].IntValue;
            rebate.Attach(this);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(7);
    }
}

/// <summary>
/// 埋下伏笔：1 费技能（普通）。下 2 次抽到构想时，使构想数值 +1；
/// 分别将两张构想加入你的抽牌堆和弃牌堆。消耗（升级：不再消耗）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class PlantForeshadow : ModCardTemplate
{
    public PlantForeshadow() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    // 衍生牌预览：构想。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<ConceptCard>()
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Times", 2)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<PlantForeshadowPower>(choiceContext, Owner.Creature,
            DynamicVars["Times"].IntValue, Owner.Creature, this);

        var player = Owner.Creature.Player;
        var combatState = Owner.Creature.CombatState;
        if (player == null || combatState == null)
        {
            return;
        }

        // 分别加入抽牌堆和弃牌堆各 1 张构想。
        var toDraw = combatState.CreateCard(ModelDb.Card<ConceptCard>(), Owner);
        await CardPileCmd.AddGeneratedCardToCombat(toDraw, PileType.Draw, Owner, CardPilePosition.Random);

        var toDiscard = combatState.CreateCard(ModelDb.Card<ConceptCard>(), Owner);
        await CardPileCmd.AddGeneratedCardToCombat(toDiscard, PileType.Discard, Owner);
    }

    protected override void OnUpgrade()
    {
        LocalKeywords.Remove(CardKeyword.Exhaust);
    }
}

/// <summary>
/// 埋下伏笔能力：下 {Amount} 次抽到构想时，使构想数值 +1（可叠加次数）。
/// </summary>
[RegisterPower]
public sealed class PlantForeshadowPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/plant_foreshadow_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/plant_foreshadow_power.png");

    public override async Task AfterCardDrawn(PlayerChoiceContext choiceContext, CardModel card, bool fromHandDraw)
    {
        if (card is not ConceptCard || card.Owner?.Creature != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        // 使手牌中所有构想数值 +1（不只是抽到的那张）。
        var player = card.Owner;
        if (player != null)
        {
            foreach (var c in PileType.Hand.GetPile(player).Cards.ToList())
            {
                if (c is ConceptCard)
                {
                    c.GetOrCreateCapability<ConceptCounterCapability>().AddCount(1);
                    MegaCrit.Sts2.Core.Nodes.Rooms.NCombatRoom.Instance?.Ui.Hand?
                        .GetCard(c)?.UpdateVisuals(PileType.Hand, CardPreviewMode.Normal);
                }
            }
        }

        await PowerCmd.Decrement(this);
    }
}

/// <summary>
/// 修行：1 费技能（罕见）。选择一张构想消耗；该构想每有 1 点数值，你就获得 2 点力量和 2 点敏捷。
/// 升级：保留；每点数值改为 3 点力量和 3 点敏捷。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class AsceticTraining : ModCardTemplate
{
    public AsceticTraining() : base(2, CardType.Power, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：构想。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<ConceptCard>()
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Strength", 2),   // 升级 3
        new DynamicVar("Dexterity", 2)   // 升级 3
    ];

    // 保留：升级前后都有（原设计只在升级后获得，2026-10-10 按用户要求改为两版都有）。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Retain };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var picked = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("card_selection", "TO_EXHAUST"), 1, 1) { Cancelable = true, RequireManualConfirmation = true },
            c => c is ConceptCard, this)).FirstOrDefault();
        if (picked == null)
        {
            return;
        }

        var count = picked.GetOrCreateCapability<ConceptCounterCapability>().Count;
        await CardCmd.Exhaust(choiceContext, picked);

        if (count <= 0)
        {
            return;
        }

        await PowerCmd.Apply<StrengthPower>(choiceContext, Owner.Creature,
            count * DynamicVars["Strength"].IntValue, Owner.Creature, this);
        await PowerCmd.Apply<DexterityPower>(choiceContext, Owner.Creature,
            count * DynamicVars["Dexterity"].IntValue, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        // 升级：每点构想数值改为 3 点力量/敏捷（保留升级前后都有，不再单独添加）。
        DynamicVars["Strength"].UpgradeValueBy(1);
        DynamicVars["Dexterity"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 循环叙事：1 费技能（罕见）。注能：将这张牌置于你的抽牌堆底，在你的回合开始时自动打出。
/// 打出时：本回合结束时，将弃牌堆的最多 1 张牌洗入你的抽牌堆（升级：0 费）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class CyclicNarrative : ModCardTemplate, IImbuedCard
{
    public CyclicNarrative() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 侧栏：「注能」的解释（和开发者协同：绿 共用同一条词条）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [ImbuedSupport.ImbuedTip];

    // 注能是否已经打出过（同一张牌每场战斗只算一次）。
    private bool _imbuedApplied;

    public override async Task AfterAutoPrePlayPhaseEntered(PlayerChoiceContext choiceContext, Player player)
    {
        if (_imbuedApplied || !ImbuedSupport.CanAutoPlayNow(player, this))
        {
            return;
        }

        _imbuedApplied = true;
        await ImbuedSupport.TryAutoPlayAsync(choiceContext, this, nameof(CyclicNarrative));
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 洗回效果：可叠加，叠层数 = 之后每个回合结束时最多能选的张数。
        await PowerCmd.Apply<CyclicNarrativePower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        // 升级：1 费 → 0 费。
        EnergyCost.UpgradeBy(-1);
    }
}

/// <summary>
/// 循环叙事：本回合结束时，将弃牌堆的最多 Amount 张牌洗入你的抽牌堆，然后此能力消失（一次性）。
/// 可叠加：层数 = 这一次最多能选的张数（右下角计数器显示的就是它）。
/// </summary>
[RegisterPower]
public sealed class CyclicNarrativePower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;

    // 右下角计数器 = 每次最多能洗回几张（也就是层数）。
    public override int DisplayAmount => Amount;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/cyclic_narrative_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/cyclic_narrative_power.png");

    // 时机：弃手牌之前（同原版「炸弹」「惊逃」），这样弃牌堆里不会混进本回合的手牌，
    // 也不会和「弃手牌 / 下回合抽牌」的卡牌节点重建撞车（那种时序会让下回合抽牌时报错）。
    public override async Task BeforeSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        try
        {
            var player = Owner.Player;
            var discard = player == null ? null : CardPile.Get(PileType.Discard, player);
            if (discard != null && discard.Cards.Count > 0)
            {
                var amount = (int)Amount;
                var max = amount < discard.Cards.Count ? amount : discard.Cards.Count;
                if (max > 0)
                {
                    // 「最多 max 张」：可以跳过不选。MinSelect(0) != MaxSelect 时 CardSelectorPrefs 会强制弹选择界面，
                    // 所以即使弃牌堆只有 1 张牌，也会让玩家自己决定要不要洗回去。
                    var prefs = new CardSelectorPrefs(
                        new LocString("card_selection", "STS2_MOMOI_CYCLIC_NARRATIVE_HEADER"), 0, max)
                    {
                        Cancelable = true
                    };

                    var selected = (await CardSelectCmd.FromCombatPile(choiceContext, discard, player!, prefs))
                        .ToList();
                    if (selected.Count > 0)
                    {
                        // skipVisuals：回合结束阶段卡牌节点正在被回收，这里不做归位动画，
                        // 只改牌堆数据，避免下回合重建手牌时找不到节点。
                        await CardPileCmd.Add(selected, PileType.Draw, CardPilePosition.Random, skipVisuals: true);
                        MomoiDiag.Log($"[Cyclic] moved {selected.Count} card(s) from discard to draw pile");
                    }
                }
            }
        }
        catch (Exception e)
        {
            Entry.Logger.Warn($"[Cyclic] end-of-turn shuffle failed: {e.Message}");
        }

        // 一次性：结算完直接消失（不按回合数递减）。
        await PowerCmd.Remove(this);
    }
}


/// <summary>
/// 王道减费组件：卡牌打出流程末尾会清理所有「直到打出」的耗能修正，
/// 因此把减费挂到卡牌的 Played 事件（清理之后触发）上，确保回手后仍然生效。
/// </summary>
[RegisterModelCapability]
public sealed class KinglyWayRebateCapability : CardCapability
{
    /// <summary>待应用的减费量（打出后应用一次）。</summary>
    public int Pending { get; set; }

    private bool _attached;

    public void Attach(CardModel card)
    {
        if (_attached)
        {
            return;
        }

        _attached = true;
        card.Played += OnPlayed;
    }

    private void OnPlayed()
    {
        if (Pending <= 0)
        {
            return;
        }

        if (Owner is CardModel card && card.EnergyCost != null)
        {
            card.EnergyCost.AddUntilPlayed(-Pending);
        }

        Pending = 0;
    }
}
