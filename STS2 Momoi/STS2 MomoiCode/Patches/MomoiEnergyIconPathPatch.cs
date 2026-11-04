using MegaCrit.Sts2.Core.Helpers;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 能量图标兜底：原版 <see cref="EnergyIconHelper.GetPath(string)"/> 是按
/// <c>atlases/ui_atlas.sprites/card/energy_{池子的 EnergyColorName}.tres</c> 拼出来的，
/// 我们卡池的 <c>EnergyColorName = "STS2_Momoi"</c> 在游戏自带图集里没有对应条目 →
/// 预加载会报 “Asset not cached”，多人界面左上角的能量图标也会是空的。
///
/// 这里只在自己的池子上把它替换成 mod 内的文本能量图标（24×24，与
/// <c>CardPoolModel.TextEnergyIconPath</c> 同一个文件）；其他池子原样放行。
/// </summary>
public class MomoiEnergyIconPathPatch : IPatchMethod
{
    public static string PatchId => "momoi_energy_icon_path";

    public static string Description => "王小桃卡池的 EnergyIconPath 指到 mod 自己的能量图标。";

    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(EnergyIconHelper), nameof(EnergyIconHelper.GetPath), new[] { typeof(string) })];

    public static void Postfix(string prefix, ref string __result)
    {
        if (!string.Equals(prefix, "STS2_Momoi", System.StringComparison.OrdinalIgnoreCase))
        {
            return;
        }

        __result = $"{Entry.ResPath}/images/characters/energy_text.png";
    }
}
