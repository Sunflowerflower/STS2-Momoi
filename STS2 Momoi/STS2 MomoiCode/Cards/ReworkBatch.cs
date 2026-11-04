using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Hooks;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.Nodes.CommonUi;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Models.Capabilities;
using STS2RitsuLib.Scaffolding.Content;
using STS2_Momoi.Diagnostics;

namespace STS2_Momoi.Cards;

// ===================================================================
// 1) 双刀王小桃：1 费技能（稀有）。添加 2 张小刀到你的手牌；
//    本回合每打出一张不为小刀的攻击牌，就重复此效果。
// ===================================================================
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class DualBladeMomoi : ModCardTemplate
{
    public DualBladeMomoi() : base(1, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：小刀。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<Shiv>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Shivs", 2)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 添加 2 张小刀（升级版为小刀+）。
        for (int i = 0; i < DynamicVars["Shivs"].IntValue; i++)
        {
            var shiv = combatState.CreateCard(ModelDb.Card<Shiv>(), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(shiv);
            }

            await CardPileCmd.AddGeneratedCardToCombat(shiv, PileType.Hand, Owner);
        }

        // 本回合的重复效果（升级前/升级后各自独立的能力）。
        if (IsUpgraded)
        {
            await PowerCmd.Apply<DualBladeMomoiUpgradedPower>(choiceContext, Owner.Creature,
                DynamicVars["Shivs"].IntValue, Owner.Creature, this);
        }
        else
        {
            await PowerCmd.Apply<DualBladeMomoiPower>(choiceContext, Owner.Creature,
                DynamicVars["Shivs"].IntValue, Owner.Creature, this);
        }
    }

    protected override void OnUpgrade()
    {
    }
}

/// <summary>双刀王小桃（未升级）：本回合你打出不为小刀的攻击牌后，添加 2 张小刀到你的手牌。</summary>
[RegisterPower]
public class DualBladeMomoiPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 每个实例独立存在：Amount = 实例数，每次触发叠加 2×Amount 张小刀。
    public override PowerStackType StackType => PowerStackType.Counter;

    // 右下角显示的就是「每次触发添加的小刀张数」（= Amount；叠加层数与添加张数本来就是同一个数）。
    public override int DisplayAmount => Amount;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/dual_blade_momoi_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/dual_blade_momoi_power.png");

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (!ShouldTrigger(cardPlay))
        {
            return;
        }

        await AddShivs(choiceContext);
    }

    protected bool ShouldTrigger(CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return false;
        }

        // 只对「不为小刀的攻击牌」触发。
        return cardPlay.Card.Type == CardType.Attack && cardPlay.Card is not Shiv;
    }

    // 本回合当你打出一张不为小刀的攻击牌后，添加 Amount 张小刀到你的手牌。
    protected async Task AddShivs(PlayerChoiceContext choiceContext)
    {
        var combatState = Owner.CombatState;
        var player = Owner.Player;
        if (combatState == null || player == null)
        {
            return;
        }

        for (int i = 0; i < Amount; i++)
        {
            var shiv = combatState.CreateCard(ModelDb.Card<Shiv>(), player);
            if (UpgradedShivs)
            {
                CardCmd.Upgrade(shiv);
            }

            await CardPileCmd.AddGeneratedCardToCombat(shiv, PileType.Hand, player);
        }
    }

    protected virtual bool UpgradedShivs => false;

    // 只在本回合有效。
    public override async Task BeforeSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side == CombatSide.Player && participants.Contains(Owner))
        {
            await PowerCmd.Remove(this);
        }
    }
}

/// <summary>双刀王小桃（升级）：本回合你打出不为小刀的攻击牌后，添加 2 张小刀+ 到你的手牌。</summary>
[RegisterPower]
public sealed class DualBladeMomoiUpgradedPower : DualBladeMomoiPower
{
    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/dual_blade_momoi_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/dual_blade_momoi_power.png");

    protected override bool UpgradedShivs => true;
}

// ===================================================================
// 2) 虚拟女仆武器：3 费技能（稀有）。将 1 张当心误射！添加到你的手牌并打出；
//    下 2（升级 3）次打出攻击牌时，重复此效果。
// ===================================================================
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class MaidWeapon : ModCardTemplate
{
    public MaidWeapon() : base(3, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：当心误射！。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<WatchOut>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Times", 2)   // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        Audio.MomoiAudio.PlayVoice(Audio.MomoiSfx.MaidWeaponVoice);
        await PlayWatchOut(choiceContext, IsUpgraded);

        if (IsUpgraded)
        {
            await PowerCmd.Apply<MaidWeaponUpgradedPower>(choiceContext, Owner.Creature,
                DynamicVars["Times"].IntValue, Owner.Creature, this);
        }
        else
        {
            await PowerCmd.Apply<MaidWeaponPower>(choiceContext, Owner.Creature,
                DynamicVars["Times"].IntValue, Owner.Creature, this);
        }
    }

    private async Task PlayWatchOut(PlayerChoiceContext choiceContext, bool upgraded)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var watchOut = combatState.CreateCard(ModelDb.Card<WatchOut>(), Owner);
        if (upgraded)
        {
            CardCmd.Upgrade(watchOut);
        }

        await CardPileCmd.AddGeneratedCardToCombat(watchOut, PileType.Hand, Owner);
        await CardCmd.AutoPlay(choiceContext, watchOut, null);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Times"].UpgradeValueBy(1);
    }
}

/// <summary>虚拟女仆武器（未升级）：下 N 次打出攻击牌时，将一张当心误射！添加到你的手牌并打出。</summary>
[RegisterPower]
public class MaidWeaponPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 叠加：仅同类叠加，Amount = 剩余触发次数。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/maid_weapon_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/maid_weapon_power.png");

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        if (cardPlay.Card.Type != CardType.Attack)
        {
            return;
        }

        var combatState = Owner.CombatState;
        var player = Owner.Player;
        if (combatState == null || player == null)
        {
            return;
        }

        var watchOut = combatState.CreateCard(ModelDb.Card<WatchOut>(), player);
        if (UpgradedWatchOut)
        {
            CardCmd.Upgrade(watchOut);
        }

        await CardPileCmd.AddGeneratedCardToCombat(watchOut, PileType.Hand, player);
        await CardCmd.AutoPlay(choiceContext, watchOut, null);

        await PowerCmd.Decrement(this);
    }

    protected virtual bool UpgradedWatchOut => false;
}

/// <summary>虚拟女仆武器（升级）：下 N 次打出攻击牌时，将一张当心误射！+ 添加到你的手牌并打出。</summary>
[RegisterPower]
public sealed class MaidWeaponUpgradedPower : MaidWeaponPower
{
    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/maid_weapon_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/maid_weapon_power.png");

    protected override bool UpgradedWatchOut => true;
}

// ===================================================================
// 4) 赖招复读：2 费能力（稀有，升级 1 费）。选择一张攻击牌或小游戏牌；
//    在你的回合开始时，将这张牌的复制品加入手牌。
// ===================================================================
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class RepeatMove : ModCardTemplate
{
    public RepeatMove() : base(2, CardType.Power, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var picked = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 1, 1),
            c => c.Type == CardType.Attack || MinigameSupport.IsMinigameCard(c), this)).FirstOrDefault();
        if (picked == null)
        {
            return;
        }

        var power = await PowerCmd.Apply<RepeatMovePower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        power?.SetSelectedCard(picked);
    }

    protected override void OnUpgrade()
    {
        EnergyCost.UpgradeBy(-1);
    }
}

/// <summary>赖招复读：回合开始时，将所选牌的复制品加入手牌（照抄夜魇的存牌方式，实例独立）。</summary>
[RegisterPower]
public sealed class RepeatMovePower : ModPowerTemplate
{
    private class Data
    {
        public CardModel? SelectedCard;
    }

    public override PowerType Type => PowerType.Buff;

    // 每次打出都是独立实例，各存一张牌。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/repeat_move_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/repeat_move_power.png");

    // 只有真正挂在角色身上的实例才走 smartDescription（{Card} 才有值）。
    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new StringVar("Card")
    ];

    protected override object InitInternalData() => new Data();

    /// <summary>记录所选牌（存克隆体；含当前实际费用状态）。</summary>
    public void SetSelectedCard(CardModel card)
    {
        var clone = card.CreateClone();
        CardCmd.ClearAffliction(clone);

        // 保留当前实际耗能（例如本回合变为 0 费，则复制品也保持 0 费）。
        var resolved = card.EnergyCost.GetResolved();
        if (resolved != clone.EnergyCost.Canonical)
        {
            clone.EnergyCost.SetThisCombat(resolved, reduceOnly: true);
        }

        GetInternalData<Data>().SelectedCard = clone;
        ((StringVar)DynamicVars["Card"]).StringValue = clone.Title;
    }

    public override async Task BeforeHandDraw(Player player, PlayerChoiceContext choiceContext, ICombatState combatState)
    {
        if (player != Owner.Player || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var data = GetInternalData<Data>();
        if (data.SelectedCard == null)
        {
            return;
        }

        var copy = data.SelectedCard.CreateClone();
        await CardPileCmd.AddGeneratedCardToCombat(copy, PileType.Hand, player);
    }
}

// ===================================================================
// 5) 蒙太奇：3 费能力（稀有，升级 2 费）。回合结束时从抽牌堆选一张牌打出；
//    与该牌类型相同 → 将 1 张构想加入手牌；不同 → 使构想数值 +1（所有构想）。
// ===================================================================
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Montage : ModCardTemplate
{
    public Montage() : base(3, CardType.Power, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：构想。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<ConceptCard>()
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<MontagePower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        EnergyCost.UpgradeBy(-1);
    }
}

/// <summary>蒙太奇：回合结束时从抽牌堆选择一张牌打出，并按类型相同/不同给出构想奖励。</summary>
[RegisterPower]
public sealed class MontagePower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 不可叠加层数，但多个实例独立存在：Amount = 实例数，回合结束时依次触发。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/montage_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/montage_power.png");

    public override async Task BeforeSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var player = Owner.Player;
        var combatState = Owner.CombatState;
        if (player == null || combatState == null)
        {
            return;
        }

        for (int i = 0; i < Amount; i++)
        {
            if (CombatManager.Instance.IsOverOrEnding)
            {
                break;
            }

            var drawPile = PileType.Draw.GetPile(player);
            if (drawPile.Cards.Count == 0)
            {
                break;
            }

            var picked = (await CardSelectCmd.FromCombatPile(choiceContext, drawPile, player,
                new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 1, 1))).FirstOrDefault();
            if (picked == null)
            {
                break;
            }

            // 比较「上一张打出的牌」的类型。
            var lastPlayed = CombatStats.ThisTurnPlayed.Count > 0
                ? CombatStats.ThisTurnPlayed[^1]
                : (CombatStats.LastTurnPlayed.Count > 0 ? CombatStats.LastTurnPlayed[^1] : null);
            var sameType = lastPlayed != null && lastPlayed.Type == picked.Type;

            // 先判断 AutoPlay 是否真的会打出这张牌：被阻止时不发奖励（见 AutoPlayProbe）。
            var willPlay = AutoPlayProbe.WillActuallyPlay(combatState, picked);
            await CardCmd.AutoPlay(choiceContext, picked, null);
            if (!willPlay)
            {
                continue;
            }

            if (sameType)
            {
                var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), player);
                await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, player);
            }
            else
            {
                await ConceptCounterCapability.AddCountToAllInHand(choiceContext, Owner, 1);
            }
        }
    }
}

/// <summary>
/// 判断 <see cref="CardCmd.AutoPlay"/> 是否真的会把这张牌打出去。
/// AutoPlay 有几条**静默不打出、只把牌挪到结果堆**的分支：
///   * 带 <see cref="CardKeyword.Unplayable"/> 关键字；
///   * <see cref="Hook.ShouldPlay"/> 被某个模型阻止（如「凡庸」类限制）；
///   * 需要目标但场上有合法目标（AnyEnemy 没有可击敌人 / AnyAlly 没有存活队友）。
/// 蒙太奇的奖励必须以此为准 —— 否则牌根本没打出去，却照样发构想。
/// （这段逻辑是照抄 <c>CardCmd.AutoPlay</c> 的前置分支，它改了这里也要跟着对。）
/// </summary>
internal static class AutoPlayProbe
{
    public static bool WillActuallyPlay(ICombatState combatState, CardModel card)
    {
        if (card.Keywords.Contains(CardKeyword.Unplayable))
        {
            return false;
        }

        if (!Hook.ShouldPlay(combatState, card, out _, AutoPlayType.Default))
        {
            return false;
        }

        return card.TargetType switch
        {
            TargetType.AnyEnemy => combatState.HittableEnemies.Any(),
            TargetType.AnyAlly => combatState.Allies.Any(c =>
                c != null && c.IsAlive && c.IsPlayer && c != card.Owner?.Creature),
            _ => true
        };
    }
}

// ===================================================================
// 6) 严守截稿日！：0 费攻击（罕见）。保留；仅当构想数值 ≥3 时才能打出；
//    造成 24（升级 30）点伤害；立即打出手牌中的所有构想。
// ===================================================================
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class MeetDeadline : ModCardTemplate
{
    public MeetDeadline() : base(0, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Retain };

    // 条件打出（参考华丽收场）：构想数值不低于 3 时才能打出。
    protected override bool IsPlayable => ConceptCounterCapability.GetMaxCountInHand(Owner.Creature) >= 3;

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(24m),  // 升级 30
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target != null)
        {
            await DamageCmd.Attack(DynamicVars.CalculatedDamage)
                .FromCard(this, cardPlay)
                .Targeting(target)
                .Execute(choiceContext);
        }

        // 立即打出手牌中的所有构想。
        var player = Owner.Creature.Player;
        if (player == null)
        {
            return;
        }

        foreach (var card in PileType.Hand.GetPile(player).Cards.ToList())
        {
            if (card is ConceptCard)
            {
                await CardCmd.AutoPlay(choiceContext, card, null);
            }
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(6);
    }
}

// ===================================================================
// 10) 心流：3 费技能（罕见）。获得 16（升级 19）点格挡；
//     每打出 3 张小游戏牌，就将这张牌放入手牌，其耗能在下次打出前 -2（升级 -3）。
// ===================================================================
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class FlowState : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public FlowState() : base(3, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(16m, ValueProp.Move),           // 升级 19
        new EnergyVar("CostReduce", 2)         // 升级 3（能量图标）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);

    }

    // 照抄原版《如此甚好》(MakeItSo)：AfterCardPlayedLate 时刚打出的牌已记入战斗历史，计数包含当前这张。
    // 心流为「本场战斗累计」：统计全场已完成的小游戏牌出牌次数。
    public override async Task AfterCardPlayedLate(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        if (!MinigameSupport.IsMinigameCard(cardPlay.Card))
        {
            return;
        }

        var count = CombatManager.Instance.History.CardPlaysFinished
            .Count(e => e.CardPlay.Player == Owner && MinigameSupport.IsMinigameCard(e.CardPlay.Card));

        MomoiDiag.Log($"[FlowState] minigame played: count={count} ({cardPlay.Card.Id.Entry})");

        if (count <= 0 || count % 3 != 0)
        {
            return;
        }

        var reduce = IsUpgraded ? 3 : 2;

        // 已在手牌：仍然触发减费（不重复塞入手牌，避免重复动画）。
        // AddUntilPlayed 是**可叠加**的追加型相对修正 —— 这是设计意图：
        // 每 3 张小游戏牌再 -2，触发两次就是 -4（3 费基础直接减到 0），
        // 与原版火箭飞拳同款。不要改成 SetUntilPlayed。
        if (Pile?.Type == PileType.Hand)
        {
            EnergyCost.AddUntilPlayed(-reduce);
            return;
        }

        // 在其它牌堆（弃牌堆/抽牌堆）：放入手牌并减费。
        await CardPileCmd.Add(this, PileType.Hand);
        EnergyCost.AddUntilPlayed(-reduce);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Block"].UpgradeValueBy(3);
        DynamicVars["CostReduce"].UpgradeValueBy(1);
    }
}


