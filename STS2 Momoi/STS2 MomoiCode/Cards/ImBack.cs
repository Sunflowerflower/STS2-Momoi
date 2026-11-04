using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 我复活啦！：0 费技能（稀有）。获得 3 点活力；
/// 当你的生命值将被减少至 0 或以下时（局内/局外都会触发）：
/// 局内 —— 先消耗战斗中的副本、再从牌组移除本尊（参考 DeprecatedCard 的 DeckVersion 写法），
/// 然后回复到你最大生命值的 10% 并获得 5 层再生（升级：5 活力 / 6 再生）；
/// 局外 —— 没有战斗牌堆与能力系统，因此不消耗、不给再生，只从牌组移除并回复到 10%。
/// 免死部分照抄原版「蜥蜴尾巴」LizardTail 的 ShouldDieLate + AfterPreventingDeath。
/// 注意：局外取战斗牌堆会抛 InvalidOperationException，必须用 CardPile.Get（返回 null）而不是 GetPile。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class ImBack : ModCardTemplate
{
    /// <summary>
    /// 是否已经用掉这次的免死。
    /// 关键：牌组里的本体与局内副本是**两个不同实例**，而 <c>RunState.IterateHookListeners</c>
    /// 会先遍历牌组卡、再遍历战斗卡（CombatState.IterateHookListeners），
    /// 两边都会问 ShouldDieLate。若各自记自己的标记，就会分别挡一次死亡（就是“能挡两次、第三次才死”的原因）。
    /// 所以标记统一存在牌组本体上，副本通过 <see cref="CardModel.DeckVersion"/> 读写同一份。
    /// </summary>
    private bool _used;

    /// <summary>牌组本体（副本的 DeckVersion 指向本体；本体自己就是根）。</summary>
    private ImBack Root => DeckVersion as ImBack ?? this;

    /// <summary>本体与它的所有局内副本共用的“已用掉”标记。</summary>
    private bool Used
    {
        get => Root._used;
        set => Root._used = value;
    }

    public ImBack() : base(0, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Vigor", 2),        // 升级 3
        new DynamicVar("Regen", 5),        // 升级 6
        new DynamicVar("HealPercent", 10)  // 复活后回复到最大生命值的百分比（固定 10%）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, DynamicVars["Vigor"].IntValue, Owner.Creature, this);
    }

    // 免死判定：只对玩家自己生效，且用掉后不再拦（返回 true = 允许死亡）。局外（combatState 为 null）同样会走到这里。
    public override bool ShouldDieLate(Creature creature) => creature != Owner.Creature || Used;

    public override async Task AfterPreventingDeath(Creature creature)
    {
        Used = true;

        var player = Owner;
        var inCombat = player?.Creature.CombatState != null;

        // 1) 先回血。
        //    ⚠ 顺序很重要：触发免死时玩家 CurrentHp == 0，而 `Creature.IsDead => CurrentHp <= 0`，
        //    而 CardPileCmd.Add 里有 `card.Owner.Creature.IsDead` 的守卫（直接返回 success=false）。
        //    所以在回血之前做任何牌堆搬动都会被静默丢掉 —— 这正是“从牌组移除了、但没进消耗牌堆、还能再打”的原因。
        var target = Math.Max(1m, creature.MaxHp * DynamicVars["HealPercent"].BaseValue / 100m);
        await CreatureCmd.Heal(creature, Math.Max(1m, target - creature.CurrentHp));

        // 2) 局内：把战斗中的副本送进消耗牌堆（局外没有战斗牌堆，跳过）。
        if (inCombat && player != null)
        {
            var clone = DeckVersion != null ? this : FindCombatClone(player);
            if (clone?.Pile?.Type is PileType.Hand or PileType.Draw or PileType.Discard or PileType.Play)
            {
                await CardCmd.Exhaust(new ThrowingPlayerChoiceContext(), clone);
            }
        }

        // 3) 从牌组中移除本尊。
        var original = DeckVersion ?? (Pile?.Type == PileType.Deck ? this : null);
        if (original?.Pile?.Type == PileType.Deck)
        {
            await CardPileCmd.RemoveFromDeck(original);
        }

        if (DeckVersion != null && DeckVersion == original)
        {
            DeckVersion = null;
        }

        // 4) 局内：获得再生（局外没有能力系统，跳过）。
        if (inCombat && player != null)
        {
            await PowerCmd.Apply<RegenPower>(new ThrowingPlayerChoiceContext(), creature,
                DynamicVars["Regen"].IntValue, player.Creature, this);
        }
    }

    /// <summary>
    /// 找出战斗中的同名副本（本尊触发时用；副本触发时直接用 this）。
    /// 用 <see cref="CardPile.Get"/>（局外返回 null）而不是 GetPile（局外直接抛异常）。
    /// </summary>
    private CardModel? FindCombatClone(Player player)
    {
        foreach (var pileType in new[] { PileType.Hand, PileType.Draw, PileType.Discard, PileType.Play })
        {
            var pile = CardPile.Get(pileType, player);
            var found = pile?.Cards.FirstOrDefault(c => c.DeckVersion == this);
            if (found != null)
            {
                return found;
            }
        }

        return null;
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Vigor"].UpgradeValueBy(1);   // 2 -> 3
        DynamicVars["Regen"].UpgradeValueBy(1);   // 5 -> 6
    }
}
