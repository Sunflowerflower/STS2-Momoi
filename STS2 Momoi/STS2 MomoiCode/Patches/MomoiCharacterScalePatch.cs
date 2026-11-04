using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Nodes.Combat;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using STS2_Momoi.Characters;
using STS2_Momoi.Settings;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 「角色贴图大小」设置（0.5~1.5，默认 1.0）。
///
/// 做法（等价于原版 <c>NCombatRoom.AddCreature</c> 之后补一次缩放）：
/// 1. <see cref="NCreature.ScaleTo"/> 的 Prefix 只对**玩家角色**乘上倍率 —— 原版自己也会调
///    ScaleTo（缩小药水、大蘑菇等），乘上去之后这些相对缩放依然成立；怪物（<c>Entity.IsPlayer == false</c>）不受影响。
/// 2. 战斗房间里角色节点创建出来时（<c>NCombatRoom.AddCreature</c>）补一次 <c>ScaleTo(1, 0)</c>，
///    让倍率立刻生效（Prefix 会把它乘成实际倍率）。
/// 3. 王小桃本人额外乘一个写死的 <see cref="MomoiDefaultScale"/>=0.7（她的素材是按这个比例画的），
///    所以设置里 1.0 时她就是 0.7 —— 设置界面不暴露这个值。
/// </summary>
public class MomoiCreatureScaleToPatch : IPatchMethod
{
    /// <summary>王小桃素材自身的比例（写死，不进设置）。</summary>
    public const float MomoiDefaultScale = 0.7f;

    public static string PatchId => "momoi_creature_scale_to";

    public static string Description => "玩家角色贴图按设置倍率缩放（怪物不受影响）。";

    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(NCreature), nameof(NCreature.ScaleTo))];

    public static void Prefix(NCreature __instance, ref float size)
    {
        if (__instance?.Entity is not { IsPlayer: true })
        {
            return;
        }

        size *= MomoiSettingsStore.TextureScaleFactor;

        // 小桃的素材按 0.7 绘制：设置 1.0 时她就是 0.7，其他角色是 1.0。
        if (__instance.Entity.Player?.Character is STS2_MomoiCharacter)
        {
            size *= MomoiDefaultScale;
        }
    }
}

/// <summary>战斗房间创建角色节点时补一次缩放，让「角色贴图大小」立刻生效。</summary>
public class MomoiCombatRoomAddCreaturePatch : IPatchMethod
{
    public static string PatchId => "momoi_combat_room_add_creature";

    public static string Description => "角色节点加入战斗房间时按设置补一次缩放。";

    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(NCombatRoom), nameof(NCombatRoom.AddCreature))];

    public static void Postfix(NCombatRoom __instance, Creature creature)
    {
        // 只处理玩家角色；宠物（Osty）与怪物保持原样。
        if (__instance is null || creature is not { IsPlayer: true })
        {
            return;
        }

        // 传 1 而不是倍率：MomoiCreatureScaleToPatch.Prefix 会把它乘成实际倍率。
        __instance.GetCreatureNode(creature)?.ScaleTo(1f, 0.0);
    }
}
