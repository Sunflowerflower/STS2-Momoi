using System.Collections.Generic;
using System.Linq;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Saves;
using STS2_Momoi.Cards;
using STS2_Momoi.Characters;
using STS2RitsuLib.Patching.Models;
using STS2_Momoi.Diagnostics;

namespace STS2_Momoi.Patches;

/// <summary>
/// 「开发者协同：绿」的注能：第 1 回合抽牌前把这张牌挪到抽牌堆**底部**。
///
/// 原版 Imbued 附魔是靠 <c>EnchantmentModel.ShouldStartAtBottomOfDrawPile</c> 让
/// <c>CombatManager.SetupPlayerTurn</c> 在开局抽牌前自己把牌挪到底部；我们这张注能是**卡牌**、没有附魔模型，
/// 所以在这里复现同一件事（仍然交给原版的抽牌流程，不自己改抽牌数）：
/// 抽 5 张时够不到堆底 → 不会像以前那样「开局抽到这张牌，等于少抽一张」。
/// </summary>
public class MomoiImbuedDrawPilePatch : IPatchMethod
{
    public static string PatchId => "momoi_imbued_draw_pile";

    public static string Description => "开发者协同：绿 在第 1 回合抽牌前沉到抽牌堆底部（等价原版注能）。";

    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(CombatManager), "SetupPlayerTurn")];

    public static void Prefix(Player player)
    {
        if (player?.PlayerCombatState is not { TurnNumber: 1 })
        {
            return;
        }

        var player_ = player;
        var pile = CardPile.Get(PileType.Draw, player_);
        if (pile is null)
        {
            return;
        }

        var cards = pile.Cards.Where(c => c is IImbuedCard).ToList();
        if (cards.Count == 0)
        {
            return;
        }

        foreach (var card in cards)
        {
            pile.MoveToBottomInternal(card);
        }

        MomoiDiag.Log($"[Imbued] moved {cards.Count} imbued card(s) to bottom of draw pile (turn 1)");
    }
}

/// <summary>
/// 图鉴默认全解锁：模组卡在 <c>Progress.DiscoveredCards</c> 里没有记录时，卡牌图鉴会显示问号（NotSeen）。
/// 在档案进度加载完之后批量补上本模组卡牌 / 遗物 / 药水的「已发现」记录并落盘。
/// （用 <c>Progress.MarkXxxAsSeen</c>，不要用 <c>SaveManager.MarkCardAsSeen(card)</c> —— 后者要求 LocalContext.IsMine。）
/// </summary>
public static class MomoiCompendiumUnlock
{
    private const string ModIdPrefix = "STS2_MOMOI_";

    /// <summary>把本模组的卡牌 / 遗物 / 药水标记为已发现；返回新标记的数量。</summary>
    public static int MarkAll()
    {
        var save = SaveManager.Instance;
        if (save?.Progress is not { } progress)
        {
            return 0;
        }

        var marked = 0;
        // 用 id 前缀而不是卡池：衍生牌（小游戏牌 / 构想 / 支援 / 绷住链 / 传送门悖论其一其二…）都在 TokenCardPool 里，
        // 只按 STS2_MomoiCardPool 过滤会漏掉它们，图鉴里仍然是问号。
        foreach (var card in ModelDb.AllCards.Where(c => c.Id.Entry.StartsWith(ModIdPrefix, System.StringComparison.Ordinal)))
        {
            if (!progress.DiscoveredCards.Contains(card.Id))
            {
                progress.MarkCardAsSeen(card.Id);
                marked++;
            }
        }

        foreach (var relic in ModelDb.AllRelics.Where(r => r.Id.Entry.StartsWith(ModIdPrefix, System.StringComparison.Ordinal)))
        {
            if (!progress.DiscoveredRelics.Contains(relic.Id))
            {
                progress.MarkRelicAsSeen(relic.Id);
                marked++;
            }
        }

        foreach (var potion in ModelDb.AllPotions.Where(p => p.Id.Entry.StartsWith(ModIdPrefix, System.StringComparison.Ordinal)))
        {
            if (!progress.DiscoveredPotions.Contains(potion.Id))
            {
                progress.MarkPotionAsSeen(potion.Id);
                marked++;
            }
        }

        if (marked > 0)
        {
            save.SaveProgressFile();
            Entry.Logger.Info($"[Compendium] marked {marked} entry(ies) as discovered");
        }

        return marked;
    }
}

/// <summary>档案进度加载完成之后补图鉴记录。</summary>
public class MomoiCompendiumUnlockPatch : IPatchMethod
{
    public static string PatchId => "momoi_compendium_unlock";

    public static string Description => "加载档案后把本模组卡牌/遗物/药水标记为已发现（图鉴不再问号）。";

    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(SaveManager), nameof(SaveManager.InitProgressData))];

    public static void Postfix()
    {
        try
        {
            MomoiCompendiumUnlock.MarkAll();
        }
        catch (System.Exception e)
        {
            Entry.Logger.Warn($"[Compendium] unlock failed: {e.Message}");
        }
    }
}
