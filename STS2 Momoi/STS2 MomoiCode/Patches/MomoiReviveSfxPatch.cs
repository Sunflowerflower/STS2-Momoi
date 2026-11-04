using MegaCrit.Sts2.Core.Context;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Hooks;
using STS2_Momoi.Audio;
using STS2_Momoi.Characters;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>瓶中精灵/蜥蜴尾巴/自制免死效果统一走 AfterPreventingDeath。</summary>
public class MomoiReviveSfxPatch : IPatchMethod
{
    public static string PatchId => "momoi_revive_sfx";
    public static string Description => "王小桃触发免死时播放复活音效。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Hook), nameof(Hook.AfterPreventingDeath))];

    public static void Prefix(Creature creature)
    {
        if (creature.Player?.Character is STS2_MomoiCharacter && LocalContext.IsMe(creature))
        {
            // 免死发生时战斗往往已经进入 ending 状态，绕过 SfxCmd 的静默检查。
            MomoiAudio.PlayDirectVoice(MomoiSfx.Revive);
        }
    }
}
