using MegaCrit.Sts2.Core.Entities.Cards;
using STS2RitsuLib.Content;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Keywords;

namespace STS2_Momoi.Keywords;

/// <summary>
/// 模组自定义卡牌关键词：游戏牌 / 小游戏牌 / 支援牌。
/// 三个关键词都用 <see cref="ModKeywordCardDescriptionPlacement.BeforeCardDescription"/>：
/// 卡牌描述最上方会直接出现金色的「游戏牌。」「小游戏牌。」「支援牌。」文本。
/// 哪些卡带这些关键词由 <c>Patches.CardKeywordLabelPatch</c> 按标签/类型判定
/// （所以局内被「游戏人生」临时加上游戏牌标签的卡，也会立刻显示「游戏牌。」）。
/// 本地化在 localization\{zhs,eng}\card_keywords.json。
/// 注意：按 RitsuLib 约定，这里**不能用 static 类**（特性要挂在可实例化的类上）。
/// </summary>
// 注意：RitsuLib 的本地化键按「限定 ID」生成（= 卡牌惯例的 SNAKE_UPPER），
// 所以每个词条在 card_keywords.json 里都写了两种拼法（GAME_CARD / GAMECARD）以防万一；
// 多余键不会被引用，不影响。
[RegisterOwnedCardKeyword("GameCard",
    CardDescriptionPlacement = ModKeywordCardDescriptionPlacement.BeforeCardDescription,
    IncludeInCardHoverTip = false)]
[RegisterOwnedCardKeyword("MinigameCard",
    CardDescriptionPlacement = ModKeywordCardDescriptionPlacement.BeforeCardDescription,
    IncludeInCardHoverTip = false)]
[RegisterOwnedCardKeyword("SupportCard",
    CardDescriptionPlacement = ModKeywordCardDescriptionPlacement.BeforeCardDescription,
    IncludeInCardHoverTip = false)]
public class MomoiKeywords
{
    /// <summary>游戏牌（tag=fullgame）：视为小游戏牌，但不会被小游戏牌局内随机添加。</summary>
    public static readonly CardKeyword GameCard =
        ModContentRegistry.GetQualifiedKeywordId(Entry.ModId, "GameCard").GetModCardKeyword();

    /// <summary>小游戏牌（tag=minigame）：可被局内随机添加的小游戏 Token 牌。</summary>
    public static readonly CardKeyword MinigameCard =
        ModContentRegistry.GetQualifiedKeywordId(Entry.ModId, "MinigameCard").GetModCardKeyword();

    /// <summary>支援牌：得道多助 / 集结的支援池里的牌。</summary>
    public static readonly CardKeyword SupportCard =
        ModContentRegistry.GetQualifiedKeywordId(Entry.ModId, "SupportCard").GetModCardKeyword();
}
