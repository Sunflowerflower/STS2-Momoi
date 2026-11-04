using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Godot;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using STS2_Momoi.Characters;
using STS2_Momoi.Diagnostics;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 战斗开始时把王小桃的动作帧贴图预热进 Godot 的资源缓存。
///
/// 为什么需要：RitsuLib 的 cue 动画是按「路径」声明然后用 <c>CueFrameSequencePlayer</c> 逐帧换图的，
/// 帧贴图是第一次播到那一帧才 <c>ResourceLoader.Load</c>。而游戏切场景时 <c>PreloadManager</c> 会清资源缓存，
/// 模组的 <c>res://</c> 图又不在原版预载表里 —— 于是每次战斗的第一次出牌都要现场解码十几张图，就是那个卡顿。
/// 这里在角色节点进入战斗房间后，把 <c>images/characters/cue/*.png</c> 全部过一遍
/// （<see cref="ResourceLoader.CacheMode.Reuse"/>），之后 RitsuLib 再读就是缓存命中。
///
/// 每帧只读几张，铺开在开局那一两秒里，避免变成一次性的长卡死。
/// </summary>
public class MomoiCueWarmupPatch : IPatchMethod
{
    public static string PatchId => "momoi_cue_warmup";

    public static string Description => "战斗开始时预热王小桃的动作帧贴图，消除出牌首帧卡顿。";

    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(NCombatRoom), nameof(NCombatRoom.AddCreature))];

    public static void Postfix(NCombatRoom __instance, Creature creature)
    {
        if (__instance is null || creature is not { IsPlayer: true })
        {
            return;
        }

        if (creature.Player?.Character is not STS2_MomoiCharacter)
        {
            return;
        }

        MomoiCueWarmup.Schedule(__instance);
    }
}

/// <summary>动作帧贴图预热（每个战斗房间只跑一次）。</summary>
public static class MomoiCueWarmup
{
    private const string NodeName = "MomoiCueWarmup";
    private static readonly List<string> Paths = new();
    private static bool _enumerated;

    /// <summary>cue 目录里全部 png 的 res:// 路径（只在第一次调用时枚举）。</summary>
    public static IReadOnlyList<string> CuePaths()
    {
        if (_enumerated)
        {
            return Paths;
        }

        _enumerated = true;
        try
        {
            using var dir = DirAccess.Open($"{Entry.ResPath}/images/characters/cue");
            if (dir is null)
            {
                MomoiDiag.Warn("[Warmup] cue dir not found");
                return Paths;
            }

            foreach (var name in dir.GetFiles())
            {
                if (name.EndsWith(".png", StringComparison.OrdinalIgnoreCase))
                {
                    Paths.Add($"{Entry.ResPath}/images/characters/cue/{name}");
                }
            }

            Paths.Sort(StringComparer.Ordinal);
            Entry.Logger.Info($"[Warmup] {Paths.Count} cue frames queued");
        }
        catch (Exception e)
        {
            MomoiDiag.Warn($"[Warmup] enumerate failed: {e.Message}");
        }

        return Paths;
    }

    public static void Schedule(Node room)
    {
        if (room is null || !GodotObject.IsInstanceValid(room))
        {
            return;
        }

        if (room.GetNodeOrNull(NodeName) is not null)
        {
            return;
        }

        var node = new MomoiCueWarmupNode { Name = NodeName };
        room.AddChild(node);
    }
}

/// <summary>分帧把 cue 贴图读进资源缓存，读完自己 QueueFree。</summary>
public partial class MomoiCueWarmupNode : Node
{
    private const int PerFrame = 4;

    public override void _Ready()
    {
        SetProcess(false);
        _ = WarmAsync();
    }

    private async Task WarmAsync()
    {
        try
        {
            var paths = MomoiCueWarmup.CuePaths();
            var tree = GetTree();
            var index = 0;
            while (index < paths.Count)
            {
                if (tree is null || !GodotObject.IsInstanceValid(this))
                {
                    return;
                }

                var end = Math.Min(index + PerFrame, paths.Count);
                for (; index < end; index++)
                {
                    ResourceLoader.Load<Texture2D>(paths[index], cacheMode: ResourceLoader.CacheMode.Reuse);
                }

                await ToSignal(tree, SceneTree.SignalName.ProcessFrame);
            }
        }
        catch (Exception e)
        {
            MomoiDiag.Warn($"[Warmup] failed: {e.Message}");
        }
        finally
        {
            if (GodotObject.IsInstanceValid(this))
            {
                QueueFree();
            }
        }
    }
}
