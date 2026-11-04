using System.Linq;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Models;
using STS2_Momoi.Cards;
using STS2_Momoi.Keywords;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 按卡牌标签补上「游戏牌 / 小游戏牌 / 支援牌」关键词，
/// 让这三类牌的卡牌描述最上方出现金色的「游戏牌。」「小游戏牌。」「支援牌。」文本。
///
/// 为什么挂在 <see cref="CardModel.GetKeywordsWithSources"/>：
/// * <c>CanonicalKeywords</c> 是虚属性，各卡自己都 override 过 —— 挂基类/模板类的 getter 都会被派生类绕过
///   （项目里额外提示文本那个补丁就踩过这个坑）；而 <c>GetKeywordsWithSources</c> 是**非虚公共方法**，所有卡都走它。
/// * 它同时把「局内临时加上的标签」也算进来（<c>Tags</c> 会包含 AddModCardTag 写入的可变标签），
///   所以「游戏人生」给手牌加游戏牌标签后，文本会立刻显示「游戏牌。」。
/// * 返回值是只读接口，这里返回**新的集合**（不修改卡牌自己的 LocalKeywords，避免污染存档状态）。
/// </summary>
public class CardKeywordLabelPatch : IPatchMethod
{
    public static string PatchId => "momoi_card_keyword_label";

    public static string Description =>
        "按标签/类型为卡牌关键字集合补上 游戏牌/小游戏牌/支援牌 模组关键词（描述顶行金色文本）。";

    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(CardModel), nameof(CardModel.GetKeywordsWithSources))];

    public static void Postfix(CardModel __instance, ref IReadOnlySet<CardKeyword> __result)
    {
        var extra = LabelFor(__instance);
        if (extra == null || __result.Contains(extra.Value))
        {
            return;
        }

        __result = new HashSet<CardKeyword>(__result) { extra.Value };
    }

    /// <summary>按标签/类型决定这张卡该带哪个标签关键词（优先级：游戏牌 &gt; 小游戏牌 &gt; 支援牌）。</summary>
    private static CardKeyword? LabelFor(CardModel card)
    {
        var tags = card.Tags;
        // 「游戏人生」本场战斗临时标成游戏牌的牌（不写标签集合）也要显示金色顶行文本。
        if (tags.Contains(MinigameSupport.FullGameTag) || MinigameSupport.IsTemporaryGameCard(card))
        {
            return MomoiKeywords.GameCard;
        }

        if (tags.Contains(MinigameSupport.Tag))
        {
            return MomoiKeywords.MinigameCard;
        }

        return MinigameSupport.IsSupportCardType(card) ? MomoiKeywords.SupportCard : null;
    }
}
