using MegaCrit.Sts2.Core.Nodes.Screens.CharacterSelect;
using STS2_Momoi.Characters;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 每次重新进入选角界面时清空随机变体，保证背景和音效重新成对随机。
/// </summary>
public class MomoiSelectScreenResetPatch : IPatchMethod
{
    public static string PatchId => "momoi_select_variant_reset";
    public static string Description => "进入选角界面时重置随机背景/音效变体。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(NCharacterSelectScreen), nameof(NCharacterSelectScreen._Ready))];

    public static void Prefix()
    {
        STS2_MomoiCharacter.ResetSelectVariant();
    }
}
