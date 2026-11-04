using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Random;
using STS2RitsuLib.CardTags;
using STS2_Momoi.Diagnostics;

namespace STS2_Momoi.Cards;

/// <summary>
/// 小游戏牌公共支持：
/// - minigame 标签：可被临时加入对局的小游戏牌（连连看/消消乐等）。
/// - fullgame 标签：游戏牌——可作为奖励掉落，但不可被临时加入对局；仍享受小游戏牌的所有增益（计数/回手/触发）。
/// - 支援牌支持：support 标签 + 支援牌清单（得道多助 / 集结）。
/// </summary>
public static class MinigameSupport
{
    /// <summary>小游戏标签（可临时加入对局）。</summary>
    public static CardTag Tag { get; } = ModCardTagRegistry.GetCardTag("minigame");

    /// <summary>游戏牌标签（不可临时加入，但享受小游戏牌增益）。</summary>
    public static CardTag FullGameTag { get; } = ModCardTagRegistry.GetCardTag("fullgame");

    /// <summary>支援牌标签。</summary>
    public static CardTag SupportTag { get; } = ModCardTagRegistry.GetCardTag("support");

    /// <summary>「打游戏！」等可随机临时加入对局的小游戏牌（全部小游戏 Token 牌）。</summary>
    public static readonly IReadOnlyList<Type> AllMinigameCards =
    [
        typeof(LinkUp), typeof(Match3), typeof(SnakeGame), typeof(AngryBirds), typeof(Minesweeper),
        typeof(BattleRoyale), typeof(Parkour), typeof(Tetris), typeof(Shmup), typeof(PacMan),
        typeof(PlantsVsZombies), typeof(RhythmGame), typeof(GoldMiner), typeof(SuperMario)
    ];

    /// <summary>支援牌基础池（得道多助）。不含额外选项（千寻/时），解锁后由得道多助动态加入。</summary>
    public static readonly IReadOnlyList<Type> AllSupportCards =
    [
        typeof(YuzuEscort),
        typeof(DevGreen),
        typeof(CourageBoon),
        typeof(MailCare),
        typeof(MomoiSupportYoshimi),
        typeof(MomoiSupportHibiki),
        typeof(MomoiSupportKotori),
        typeof(MomoiSupportMaki),
        typeof(MomoiSupportHare),
        typeof(MomoiSupportKotama),
        typeof(MomoiSupportNeru),
        typeof(MomoiSupportAsuna),
        typeof(MomoiSupportKarin),
        typeof(MomoiSupportAkira)
    ];

    /// <summary>是否是「小游戏牌」（含游戏牌：游戏牌享受小游戏牌的所有增益）。</summary>
    public static bool IsMinigameCard(CardModel card) =>
        card.Tags.Contains(Tag) || card.Tags.Contains(FullGameTag) || IsTemporaryGameCard(card);

    // ===================================================================
    // 「游戏人生」给的游戏牌标签：**只在本场战斗生效**。
    //
    // 为什么不能直接 AddModCardTag：
    //   战斗克隆体的 _tags 与**牌组本尊共用同一个 HashSet**（CardModel.CloneForCombat 不重建 _tags），
    //   所以往手牌那张牌里写标签，实际会写进牌组本尊 —— 打完这场还在，甚至随存档进到下一局
    //   （用户实测：上一把给打击加的“游戏牌”标签，新开局还在）。
    // 所以改成一张按**实例引用**记录的「本场战斗临时游戏牌」表：
    //   * 读标签的地方统一走 IsMinigameCard / IsTemporaryGameCard，不碰卡的持久状态；
    //   * 战斗开始时清空（见 CombatStats.CombatStartResetPatch）；
    //   * 战斗结束/新局自然失效。
    // ===================================================================
    private static readonly HashSet<CardModel> TemporaryGameCards = new(ReferenceEqualityComparer.Instance);

    /// <summary>把这张牌标记为本场战斗的游戏牌（不修改卡的标签集合）。</summary>
    public static void MarkTemporaryGameCard(CardModel card) => TemporaryGameCards.Add(card);

    /// <summary>这张牌是否被「游戏人生」在本场战斗标为游戏牌。</summary>
    public static bool IsTemporaryGameCard(CardModel card) => TemporaryGameCards.Contains(card);

    /// <summary>战斗开始 / 新局时清空临时标记。</summary>
    public static void ClearTemporaryGameCards() => TemporaryGameCards.Clear();

    /// <summary>
    /// 清理旧版遗留：老版本用 AddModCardTag 写进牌组本尊的 fullgame 标签会随存档跨局保存。
    /// 这里把「本来就不是游戏牌」的牌上的这个标签去掉（真正的游戏牌看规范模型的标签）。
    /// </summary>
    public static void StripLeakedGameCardTags(IEnumerable<CardModel> deckCards)
    {
        foreach (var card in deckCards)
        {
            if (!card.Tags.Contains(FullGameTag))
            {
                continue;
            }

            var canonical = ModelDb.GetById<CardModel>(card.Id);
            if (canonical != null && canonical.Tags.Contains(FullGameTag))
            {
                continue;   // 本来就是游戏牌（如 游戏人生 / 小游戏牌），不动
            }

            card.RemoveModCardTag(FullGameTag);
            MomoiDiag.Log($"[GameLife] Stripped leaked fullgame tag from {card.Id.Entry}");
        }
    }

    /// <summary>全部支援牌类型（支援池 14 种 + 解锁后的千寻 / 时）——用于「支援牌」标记与侧栏判定。</summary>
    public static readonly IReadOnlySet<Type> AllSupportCardTypes = new HashSet<Type>(
        AllSupportCards.Concat(new[] { typeof(MomoiSupportChihiro), typeof(MomoiSupportToki) }));

    /// <summary>是否是支援牌（按类型判定：这些卡大部分没有 tag，只有 勇者的加护 / 开发者协同：绿 带 support tag）。</summary>
    public static bool IsSupportCardType(CardModel card) => AllSupportCardTypes.Contains(card.GetType());

    /// <summary>是否是可临时加入对局的小游戏牌（不含游戏牌）。</summary>
    public static bool CanBeTemporarilyAdded(CardModel card) => card.Tags.Contains(Tag);

    /// <summary>是否是支援牌。</summary>
    public static bool IsSupportCard(CardModel card) => card.Tags.Contains(SupportTag);

    public static Type PickRandomMinigame(Rng rng) =>
        rng.NextItem(AllMinigameCards) ?? AllMinigameCards[0];

    /// <summary>创建一张随机小游戏牌实例（可指定升级版）。</summary>
    public static CardModel CreateRandomMinigameCard(ICombatState combatState, Player? owner, bool upgraded)
    {
        var type = PickRandomMinigame(owner?.RunState?.Rng?.CombatCardSelection ?? Rng.Chaotic);
        var card = combatState.CreateCard(ModelDb.Get(type) as CardModel ?? ModelDb.Card<LinkUp>(), owner);
        if (upgraded)
        {
            CardCmd.Upgrade(card);
        }

        return card;
    }

    /// <summary>失去 X 点活力；活力为 0 时不再扣减（保持 0，不产生负值）。</summary>
    public static async Task LoseVigor(PlayerChoiceContext ctx, Creature creature, CardModel source, int amount = 1)
    {
        var vigor = creature.GetPower<VigorPower>();
        if (vigor != null && vigor.Amount > 0)
        {
            await PowerCmd.Apply<VigorPower>(ctx, creature, -amount, creature, source);
        }
    }
}
