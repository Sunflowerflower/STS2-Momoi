using System.Collections.Generic;
using System.Linq;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.MonsterMoves.Intents;
using STS2_Momoi.Cards;
using STS2_Momoi.Powers;
using STS2RitsuLib.Patching.Models;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Patches;

/// <summary>
/// 小游戏牌侧栏 + 关键词（活力/火力/灼烧/格挡/消耗/保留/变化/斩杀/脆弱）侧栏：
/// 用全局 Postfix 挂在 ExtraHoverTips 上，无需逐卡添加。
///   * 小游戏牌（tag=minigame）→「小游戏牌：这张牌为小游戏牌。」
///   * 游戏牌（tag=fullgame）  →「游戏牌：这张牌视为小游戏牌，但不会作为小游戏牌局内添加。」
///   * 描述里提到小游戏牌但不是上述两类 →「小游戏牌：一种特殊的衍生牌。」
/// 卡牌描述文本（当前语言）包含对应关键词时，附加原版解释侧栏；
/// 「消耗/保留」只在卡本身没有该关键词时才加（否则会与自动徐章重复）。
/// </summary>
public class MinigameCardSidebarPatch : IPatchMethod
{
    public static string PatchId => "momoi_minigame_sidebar";
    public static string Description => "小游戏牌与关键词（活力/火力/灼烧）的解释侧栏。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        // 注意：ModCardTemplate 将 ExtraHoverTips 声明为 sealed override（不走基类实现），
        // 必须挂派生类的 getter，否则对我们的卡永远不会触发。
        [new(typeof(ModCardTemplate), "get_ExtraHoverTips")];

    public static void Postfix(CardModel __instance, ref IEnumerable<IHoverTip> __result)
    {
        var tips = __result.ToList();

        // 小游戏牌 / 游戏牌：靠 tag 判定（小游戏牌池里的牌、以及不掉落但视为小游戏牌的游戏牌）。
        bool isMinigame = __instance.Tags.Contains(MinigameSupport.Tag);
        bool isGame = __instance.Tags.Contains(MinigameSupport.FullGameTag)
                      || MinigameSupport.IsTemporaryGameCard(__instance);
        if (isMinigame)
        {
            tips.Add(SidebarTip("STS2_MOMOI_MINIGAME_CARD_SIDEBAR"));
        }
        else if (isGame)
        {
            tips.Add(SidebarTip("STS2_MOMOI_GAME_CARD_SIDEBAR"));
        }
        else if (MinigameSupport.IsSupportCardType(__instance))
        {
            // 支援牌（支援池里的牌；这些卡大多没有 tag，按类型判定）。
            tips.Add(SidebarTip("STS2_MOMOI_SUPPORT_CARD_SIDEBAR"));
        }

        // 关键词侧栏：按原始卡面文本（当前语言）包含的关键词自动附加原版解释。
        string raw;
        try
        {
            raw = __instance.Description.GetRawText();
        }
        catch
        {
            __result = tips;
            return;
        }

        bool Has(string zh, string en) => raw.Contains(zh) || raw.Contains(en);

        // 描述里点到了「小游戏牌」但卡本身既不是小游戏牌也不是游戏牌（如 打游戏！/拾遗/堕落）：
        // 给「小游戏牌」这个关键词本身的解释（不是“这张牌为小游戏牌”）。
        if (!isMinigame && !isGame && Has("小游戏牌", "Minigame"))
        {
            tips.Add(SidebarTip("STS2_MOMOI_MINIGAME_KEYWORD_SIDEBAR"));
        }

        if (Has("活力", "Vigor"))
        {
            tips.Add(HoverTipFactory.FromPower<VigorPower>());  // 原版活力（图标+标题+解释）
        }

        if (Has("火力", "Firepower"))
        {
            // 火力：图标+标题 + 自定义解释侧栏（先用现有火力图标代替）。
            tips.Add(new HoverTip(ModelDb.Power<FirepowerPower>(),
                new LocString("cards", "STS2_MOMOI_KEYWORD_FIREPOWER_SIDEBAR").GetFormattedText(), isSmart: false));
        }

        if (Has("灼烧", "Burn"))
        {
            // 灼烧：图标+标题 + 自定义解释侧栏（先用现有灼烧图标代替）。
            tips.Add(new HoverTip(ModelDb.Power<BurnPower>(),
                new LocString("cards", "STS2_MOMOI_KEYWORD_BURN_SIDEBAR").GetFormattedText(), isSmart: false));
        }

        if (Has("无实体", "Intangible"))
        {
            tips.Add(HoverTipFactory.FromPower<IntangiblePower>());
        }

        if (Has("脆弱", "Frail"))
        {
            tips.Add(HoverTipFactory.FromPower<FrailPower>());
        }

        if (Has("再生", "Regen"))
        {
            tips.Add(HoverTipFactory.FromPower<RegenPower>());
        }

        if (Has("易伤", "Vulnerable"))
        {
            tips.Add(HoverTipFactory.FromPower<VulnerablePower>());
        }

        if (Has("缓冲", "Buffer"))
        {
            tips.Add(HoverTipFactory.FromPower<BufferPower>());
        }

        if (Has("虚弱", "Weak"))
        {
            tips.Add(HoverTipFactory.FromPower<WeakPower>());
        }

        if (Has("力量", "Strength"))
        {
            tips.Add(HoverTipFactory.FromPower<StrengthPower>());
        }

        if (Has("敏捷", "Dexterity"))
        {
            tips.Add(HoverTipFactory.FromPower<DexterityPower>());
        }

        if (Has("格挡", "Block"))
        {
            tips.Add(HoverTipFactory.Static(StaticHoverTip.Block));
        }

        // 描述里提到「消耗 / 保留」但卡本身没有该关键词时，补上关键词的提示文本
        // （卡自己有该关键词时，游戏会自动附上，不能重复加）。
        // 原则同「格挡」：模组把「消耗/保留」当关键词染色，提示文本要跟上。
        if (Has("消耗", "Exhaust") && !__instance.Keywords.Contains(CardKeyword.Exhaust))
        {
            tips.Add(HoverTipFactory.FromKeyword(CardKeyword.Exhaust));
        }

        if (Has("保留", "Retain") && !__instance.Keywords.Contains(CardKeyword.Retain))
        {
            tips.Add(HoverTipFactory.FromKeyword(CardKeyword.Retain));
        }

        if (Has("变化", "Transform"))
        {
            tips.Add(HoverTipFactory.Static(StaticHoverTip.Transform));
        }

        if (Has("斩杀", "Fatal"))
        {
            tips.Add(HoverTipFactory.Static(StaticHoverTip.Fatal));
        }

        if (raw.Contains("energyIcons") || Has("能量图标", "Energy"))
        {
            tips.Add(HoverTipFactory.ForEnergy(__instance));
        }

        if (Has("击晕", "Stun") || Has("眩晕", "Stun"))
        {
            tips.Add(StunIntent.GetStaticHoverTip());
        }

        __result = tips;
    }

    /// <summary>
    /// 构造一条「标题 + 说明」侧栏：标题（如「小游戏牌」）由 hover_tip.tscn 主题渲染成金色（**不要写 [gold]**），
    /// 说明用富文本。
    /// </summary>
    private static IHoverTip SidebarTip(string key) =>
        new HoverTip(new LocString("cards", key + ".title"), new LocString("cards", key + ".description"));
}
