using System.Linq;
using System.Reflection;
using MegaCrit.Sts2.Core.Entities.Ancients;
using MegaCrit.Sts2.Core.Models.Events;
using STS2_Momoi.Characters;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 建筑师房「与建筑师对打」的演出。
///
/// 原版 <see cref="TheArchitect"/> 的攻击演出是**纯特效**（`AnimPlayerAttackIfNecessary`）：
/// 它按对话配置里的 <see cref="AncientDialogue.StartAttackers"/> / <see cref="AncientDialogue.EndAttackers"/>
/// 决定谁打谁，然后用角色自己的 `GetArchitectAttackVfx()` 播 vfx（我们已经在 `STS2_MomoiCharacter` 里返回了 5 条路径）。
///
/// 但这两个字段是 **C# 侧的对话配置**，不是本地化文本 —— RitsuLib 只会从 `ancients.json` 给模组角色
/// 生成对话（我们的 4 段台词就是那么来的），生成出来的对话 `EndAttackers` 全是默认的 `None`，
/// 于是玩家在建筑师房**一句台词都不打**，看不到任何演出。
///
/// 这个补丁在 <see cref="TheArchitect"/> 解析出对话之后（`LoadDialogue` 之后）按拜访次数补上攻击者配置：
/// 前几次「嘴硬」→ 玩家打 + 建筑师还手（Both），最后一次带了饮料 → 不打（None）。
/// 数值本身只是演出（`WinRun` 直接结算这一局，不会真的扣建筑师的血）。
/// </summary>
public class MomoiArchitectCutscenePatch : IPatchMethod
{
    public static string PatchId => "momoi_architect_cutscene";

    public static string Description => "建筑师房：给王小桃的 THE_ARCHITECT 对话补上 StartAttackers/EndAttackers，播放对打演出。";

    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(TheArchitect), "LoadDialogue")];

    public static void Postfix(TheArchitect __instance)
    {
        if (__instance.Owner?.Character is not STS2_MomoiCharacter)
        {
            return;
        }

        var dialogue = __instance.Dialogue;
        if (dialogue == null)
        {
            return;
        }

        // 最后一次拜访（带饮料那段）是友好收场，不打；之前几次嘴硬 → 玩家出手、建筑师还手。
        var friendly = dialogue.VisitIndex is >= 3;
        SetAutoProperty(dialogue, nameof(AncientDialogue.StartAttackers),
            friendly ? ArchitectAttackers.None : ArchitectAttackers.Player);
        SetAutoProperty(dialogue, nameof(AncientDialogue.EndAttackers),
            friendly ? ArchitectAttackers.None : ArchitectAttackers.Both);
    }

    /// <summary>这两个属性是 <c>init</c> 的，运行期只能通过自动属性的后备字段改（字段由 Publicizer 暴露/反射可写）。</summary>
    private static void SetAutoProperty(object target, string propertyName, ArchitectAttackers value)
    {
        var field = target.GetType().GetField($"<{propertyName}>k__BackingField",
            BindingFlags.Instance | BindingFlags.NonPublic);
        field?.SetValue(target, value);
    }
}
