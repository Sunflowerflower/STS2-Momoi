using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Models.Powers;

namespace STS2_Momoi.Tips;

/// <summary>
/// 描述里出现「关键词」时需要补的侧栏，统一从这里取。
/// 遗物 / 药水的描述不会走卡牌的自动关键词侧栏（<see cref="Patches.MinigameCardSidebarPatch"/> 只挂在 CardModel 上），
/// 所以这些要手动加，并且文案必须和卡牌那边完全一致。
/// </summary>
public static class MomoiSidebarTips
{
    /// <summary>
    /// 构造一条「标题 + 说明」侧栏：标题（如「小游戏牌」）由 hover_tip.tscn 主题渲染成金色（**不要写 [gold]**），
    /// 说明用富文本。与 <c>MinigameSidebarPatch.SidebarTip</c> 同一套键。
    /// </summary>
    public static IHoverTip SidebarTip(string key) =>
        new HoverTip(new LocString("cards", key + ".title"), new LocString("cards", key + ".description"));

    /// <summary>「小游戏牌：一种特殊的衍生牌。」——描述里提到小游戏牌、但不是「这张牌为小游戏牌」时用这条。</summary>
    public static IHoverTip MinigameKeyword => SidebarTip("STS2_MOMOI_MINIGAME_KEYWORD_SIDEBAR");

    /// <summary>消耗（原版关键词：打出后进消耗堆）。</summary>
    public static IHoverTip Exhaust => HoverTipFactory.FromKeyword(CardKeyword.Exhaust);

    /// <summary>保留（原版关键词：回合结束不弃掉）。</summary>
    public static IHoverTip Retain => HoverTipFactory.FromKeyword(CardKeyword.Retain);

    /// <summary>变化（原版静态侧栏：卡牌被变化时会变成任意稀有度的随机牌）。</summary>
    public static IHoverTip Transform => HoverTipFactory.Static(StaticHoverTip.Transform);

    /// <summary>力量（原版能力）。</summary>
    public static IHoverTip Strength => HoverTipFactory.FromPower<StrengthPower>();
}
