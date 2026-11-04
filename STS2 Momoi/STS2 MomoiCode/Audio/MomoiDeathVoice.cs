using MegaCrit.Sts2.Core.Context;
using STS2RitsuLib;
using STS2_Momoi.Characters;

namespace STS2_Momoi.Audio;

/// <summary>
/// 所有死亡路径（战斗内、事件死亡、主动放弃）最终都会发 CreatureDiedEvent。
/// 只在 WasRemovalPrevented=false 时播放，避免免死效果先响一次死亡音；只让本地玩家播自己的。
/// </summary>
public static class MomoiDeathVoice
{
    public static void Register()
    {
        RitsuLibFramework.SubscribeLifecycle<CreatureDiedEvent>(OnCreatureDied);
    }

    private static void OnCreatureDied(CreatureDiedEvent ev)
    {
        if (ev.WasRemovalPrevented)
        {
            return;
        }

        var creature = ev.Creature;
        if (creature.Player?.Character is not STS2_MomoiCharacter || !LocalContext.IsMe(creature))
        {
            return;
        }

        Entry.Logger.Info("[DeathVoice] CreatureDiedEvent");
        MomoiAudio.PlayDirectDeathVoice(MomoiSfx.DeathVoice);
    }
}
