using Godot;
using MegaCrit.Sts2.Core.Nodes.Screens.CharacterSelect;
using STS2_Momoi.Audio;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 选人背景场景自带 AudioStreamPlayer（白天/夜间各一首）；这里每帧把模组「音乐音量」写到它身上。
/// 选人界面是缓存子菜单，离开时只隐藏不释放；隐藏时暂停，显示时恢复，避免 BGM 跟到游戏里。
/// </summary>
public class MomoiSelectBgmPatch : IPatchMethod
{
    public static string PatchId => "momoi_select_bgm";
    public static string Description => "选人背景 BGM 跟随模组音乐音量，并在界面隐藏时暂停。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(NCharacterSelectScreen), nameof(NCharacterSelectScreen._Process))];

    public static void Postfix(NCharacterSelectScreen __instance)
    {
        var tree = __instance.GetTree();
        if (tree is null)
        {
            return;
        }

        var visible = __instance.Visible && __instance.IsVisibleInTree();

        foreach (var node in tree.GetNodesInGroup("momoi_select_bgm"))
        {
            if (node is not AudioStreamPlayer player || !GodotObject.IsInstanceValid(player))
            {
                continue;
            }

            if (player.Stream is AudioStreamOggVorbis ogg)
            {
                ogg.Loop = true;
            }

            player.VolumeDb = MomoiAudio.MusicVolumeDb;

            if (!visible)
            {
                if (player.Playing)
                {
                    player.StreamPaused = true;
                }

                continue;
            }

            player.StreamPaused = false;
            if (!player.Playing)
            {
                player.Play();
            }
        }
    }
}
