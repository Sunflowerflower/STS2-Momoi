using System;
using System.Threading.Tasks;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Models;
using STS2_Momoi.Diagnostics;

namespace STS2_Momoi.Cards;

/// <summary>
/// 「注能」卡牌的标记接口：第 1 回合抽牌前沉到抽牌堆底（<c>Patches/MomoiImbuedDrawPilePatch</c>），
/// 开场自动打出一次（各牌自己的 <c>AfterAutoPrePlayPhaseEntered</c>）。
/// 本模组把原版 Imbued 附魔当成关键词用，所以是**卡牌**实现这个接口，而不是附魔模型。
/// </summary>
public interface IImbuedCard
{
}

/// <summary>「注能」的共用逻辑与侧栏词条。</summary>
public static class ImbuedSupport
{
    /// <summary>侧栏：「注能」的解释（原版附魔那份词条，现在只当关键词用）。</summary>
    public static IHoverTip ImbuedTip => new HoverTip(
        new LocString("enchantments", "MOMOI_IMBUED.title"),
        new LocString("enchantments", "MOMOI_IMBUED.description"));

    /// <summary>现在是不是「第 1 回合开局自动打出」该生效的时机。</summary>
    public static bool CanAutoPlayNow(Player player, CardModel card)
    {
        return player == card.Owner
               && card.Owner?.PlayerCombatState is { TurnNumber: <= 1 }
               && card.Pile is { } pile
               && pile.Type.IsCombatPile();
    }

    /// <summary>
    /// 注能：开局自动打出。和原版 Imbued 附魔一样走 <c>CardCmd.AutoPlay</c>（免费、不需要能量）。
    /// 任何异常都只记日志，绝不能让战斗开场中断。
    /// </summary>
    public static async Task TryAutoPlayAsync(PlayerChoiceContext choiceContext, CardModel card, string tag)
    {
        try
        {
            await CardCmd.AutoPlay(choiceContext, card, null);
            MomoiDiag.Log($"[Imbued] {tag} auto-played at combat start (upgraded={card.IsUpgraded})");
        }
        catch (Exception e)
        {
            Entry.Logger.Warn($"[Imbued] {tag} auto-play failed: {e.Message}");
        }
    }
}
