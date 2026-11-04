using System;
using Godot;
using MegaCrit.Sts2.Core.Models;
using STS2_Momoi.Characters;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 所有王小桃卡牌（不论在主卡池还是 TokenCardPool）统一使用粉蓝渐变卡框材质。
/// 只替换 FrameMaterial，不动 BannerMaterial / PortraitBorder，稀有度表现保持原版。
/// </summary>
public class MomoiCardFrameMaterialPatch : IPatchMethod
{
    // 卡牌每刷新一次（NCard.Reload / 换牌 / 文字刷新）都会读一次 FrameMaterial，
    // 以前每次都要走一遍 ResourceLoader.Load，这里只读一次就缓存住。
    private static Material? _cached;
    private static bool _loadAttempted;

    private static Material? FrameMaterial
    {
        get
        {
            if (!_loadAttempted)
            {
                _loadAttempted = true;
                _cached = ResourceLoader.Load<Material>(
                    $"{Entry.ResPath}/materials/momoi_card_frame_gradient.tres");
            }

            return _cached;
        }
    }

    public static string PatchId => "momoi_card_frame_material";
    public static string Description => "王小桃卡牌统一使用粉蓝渐变卡框材质。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(CardModel), "get_FrameMaterial")];

    public static void Postfix(CardModel __instance, ref Material __result)
    {
        if (!__instance.Id.Entry.StartsWith("STS2_MOMOI_", StringComparison.Ordinal)
            && __instance.Pool is not STS2_MomoiCardPool)
        {
            return;
        }

        var material = FrameMaterial;
        if (material != null)
        {
            __result = material;
        }
    }
}
