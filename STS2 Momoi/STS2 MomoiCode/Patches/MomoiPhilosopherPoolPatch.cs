using System.Collections.Generic;
using System.Linq;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Events;
using STS2_Momoi.Characters;
using STS2_Momoi.Settings;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 色彩哲学家：在设置开启时，把王小桃卡池追加到原版颜色池顺序里。
/// 用 Postfix 而不是 IModColorfulPhilosophersCardPool，保证设置可以随时关掉。
/// </summary>
public class MomoiPhilosopherPoolPatch : IPatchMethod
{
    public static string PatchId => "momoi_philosopher_pool";
    public static string Description => "色彩哲学家事件追加王小桃卡池（受设置控制）。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(ColorfulPhilosophers), "get_CardPoolColorOrder")];

    public static void Postfix(ref IEnumerable<CardPoolModel> __result)
    {
        if (__result is null || !MomoiSettingsStore.PhilosopherPool.Read())
        {
            return;
        }

        __result = __result
            .Concat([ModelDb.CardPool<STS2_MomoiCardPool>()])
            .DistinctBy(pool => pool.Id);
    }
}
