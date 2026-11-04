using System.Collections.Generic;
using System.Linq;
using MegaCrit.Sts2.Core.Models;
using STS2_Momoi.Characters;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 把两个选人背景场景都塞进 AssetPathsCharacterSelect，避免随机到未预载的那个时同步加载卡顿。
/// </summary>
public class MomoiSelectBgPreloadPatch : IPatchMethod
{
    public static string PatchId => "momoi_select_bg_preload";
    public static string Description => "预载选人界面的两个随机背景变体。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(CharacterModel), "get_AssetPathsCharacterSelect")];

    public static void Postfix(CharacterModel __instance, ref IEnumerable<string> __result)
    {
        if (__instance is not STS2_MomoiCharacter)
        {
            return;
        }

        if (__result is null)
        {
            return;
        }

        __result = __result.Concat(new[]
        {
            STS2_MomoiCharacter.SelectBg1ScenePath,
            STS2_MomoiCharacter.SelectBg2ScenePath,
        });
    }
}
