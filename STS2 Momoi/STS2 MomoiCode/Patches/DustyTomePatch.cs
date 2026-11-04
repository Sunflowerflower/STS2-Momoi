using System.Threading.Tasks;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Relics;
using STS2_Momoi.Cards;
using STS2_Momoi.Characters;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 尘封魔典修复：
/// 第三方模组（如 FreeLoadout 遗物页）直接获得遗物而不调用 SetupForPlayer 时，
/// AncientCard 为空会崩溃；桃井玩家兜底为重整旗鼓。
/// 其余情况（包括先古卡默认升级）完全走原版逻辑。
/// </summary>
public class DustyTomeAfterObtainedPatch : IPatchMethod
{
    public static string PatchId => "momoi_dusty_tome_fix";
    public static string Description => "尘封魔典：AncientCard 为空时兜底不崩溃（先古卡默认升级，与原版一致）。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(DustyTome), nameof(DustyTome.AfterObtained))];

    public static bool Prefix(DustyTome __instance, ref Task __result)
    {
        var player = __instance.Owner;
        var isMomoi = player?.Character is STS2_MomoiCharacter;
        var ancientCard = __instance.AncientCard;

        // 正常流程（先古卡已确定）与其他角色：走原版逻辑，先古卡默认升级。
        if (ancientCard != null || !isMomoi)
        {
            return true;
        }

        // FreeLoadout 等直接领取导致未 SetupForPlayer：桃井兜底为重整旗鼓（与原版一样默认升级）。
        var rallyId = ModelDb.Card<RallyAgain>().Id;
        Entry.Logger.Info($"[DustyTome] AncientCard null, fallback to RallyAgain");
        __result = ReplaceAsync(player, rallyId);
        return false;
    }

    private static async Task ReplaceAsync(Player player, ModelId cardId)
    {
        var card = player.RunState.CreateCard(ModelDb.GetById<CardModel>(cardId), player);
        CardCmd.Upgrade(card);
        CardCmd.PreviewCardPileAdd(await CardPileCmd.Add(card, PileType.Deck), 2f);
    }
}
