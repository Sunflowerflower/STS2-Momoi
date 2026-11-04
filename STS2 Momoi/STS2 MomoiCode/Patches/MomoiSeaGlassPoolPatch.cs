using System.Collections.Generic;
using System.Linq;
using MegaCrit.Sts2.Core.Events;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Events;
using MegaCrit.Sts2.Core.Models.Relics;
using STS2_Momoi.Characters;
using STS2_Momoi.Settings;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 奥罗巴斯「海玻璃」选项：设置关闭时过滤掉王小桃那一项。
/// 设置开启时，SeaGlass 会自动从 ModelDb.AllCharacters 里拿到本角色。
/// </summary>
public class MomoiSeaGlassPoolPatch : IPatchMethod
{
    public static string PatchId => "momoi_seaglass_pool";
    public static string Description => "海玻璃选项按设置出现/隐藏王小桃。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Orobas), "get_SeaGlassOptions")];

    public static void Postfix(ref IEnumerable<EventOption> __result)
    {
        if (__result is null || MomoiSettingsStore.SeaGlassPool.Read())
        {
            return;
        }

        var momoiId = ModelDb.Character<STS2_MomoiCharacter>().Id;
        __result = __result.Where(option =>
            option.Relic is not SeaGlass seaGlass || seaGlass.CharacterId != momoiId);
    }
}
