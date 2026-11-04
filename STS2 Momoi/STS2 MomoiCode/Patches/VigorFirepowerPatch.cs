using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Commands.Builders;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Models.Powers;
using STS2RitsuLib.Patching.Models;
using STS2_Momoi.Diagnostics;

namespace STS2_Momoi.Patches;

/// <summary>
/// 活力消耗拦截钩子：有火力时扣 1 层火力并保留活力；由 VigorConsumePatch 的 Prefix 调用。
/// 注意：不能 Transpiler 修改 async 方法体（逻辑在 MoveNext 状态机里），所以用 Prefix 跳过原方法。
/// </summary>
public static class FirepowerHooks
{
    public static async Task ConsumeFirepowerAsync(PlayerChoiceContext choiceContext,
        Powers.FirepowerPower firepower)
    {
        MomoiDiag.Log($"[Firepower] ConsumeVigor: skip original, firepower={firepower.Amount} -> -1");
        await PowerCmd.ModifyAmount(choiceContext, firepower, -1, null, null, false);
    }

    /// <summary>
    /// “有火力就扣 1 层火力、没火力才扣活力”的统一入口。
    /// 必须用它代替直接 <c>PowerCmd.ModifyAmount(vigor, -n)</c>：
    /// 原版的拦截挂在 <see cref="VigorPower.AfterAttack"/> 上，**只有走 AttackCommand 的消耗才会经过那里**。
    /// 凡是不经 AttackCommand 的伤害来源（如「雷酱」炮台支援的回合结束攻击），
    /// 自己扣活力就会绕过火力把活力白白吃掉，必须把本条规则自己复现一遍。
    /// </summary>
    public static async Task SpendVigorAsync(PlayerChoiceContext choiceContext, Creature owner, int vigorAmount)
    {
        if (owner.GetPower<Powers.FirepowerPower>() is { Amount: > 0 } firepower)
        {
            MomoiDiag.Log($"[Firepower] SpendVigor(manual): firepower={firepower.Amount} -> -1 (vigor kept)");
            await PowerCmd.ModifyAmount(choiceContext, firepower, -1, null, null, false);
            return;
        }

        if (vigorAmount > 0 && owner.GetPower<VigorPower>() is { } vigor)
        {
            MomoiDiag.Log($"[Firepower] SpendVigor(manual): vigor={vigor.Amount} -> -{vigorAmount}");
            await PowerCmd.ModifyAmount(choiceContext, vigor, -vigorAmount, null, null);
        }
    }
}

/// <summary>
/// 让活力每次攻击都重新绑定加伤目标。
/// 原版 BeforeAttack 只在 commandToModify 为 null 时绑定一次；活力被火力保留后，
/// 若不重新绑定，后续攻击既不加伤也不消耗。Prefix 清空旧绑定即可。
/// </summary>
public class VigorRebindPatch : IPatchMethod
{
    public static string PatchId => "momoi_vigor_rebind";
    public static string Description => "活力每次攻击重新绑定加伤目标（配合火力保留活力）。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(VigorPower), nameof(VigorPower.BeforeAttack))];

    public static void Prefix(VigorPower __instance, AttackCommand command)
    {
        // 只处理玩家自己发起的攻击（敌人在攻击开始前清空绑定也无害，但保持干净）。
        if (command.Attacker != __instance.Owner)
        {
            return;
        }

        MomoiDiag.Log($"[Firepower] VigorRebind.BeforeAttack: vigor={__instance.Amount}");
        // Publicizer 已将 VigorPower.Data 及其私有字段公开。
        __instance.GetInternalData<VigorPower.Data>().commandToModify = null;
    }
}

/// <summary>
/// VigorPower.AfterAttack 是 async 方法（Transpiler 无法修改其状态机逻辑），
/// 因此用 Prefix：玩家攻击且有火力时跳过原方法（活力保留）并异步扣 1 层火力；否则走原逻辑。
/// </summary>
public class VigorConsumePatch : IPatchMethod
{
    public static string PatchId => "momoi_vigor_consume";
    public static string Description => "活力被全部消耗时，若有火力则改为消耗 1 层火力并保留活力。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(VigorPower), nameof(VigorPower.AfterAttack))];

    public static bool Prefix(VigorPower __instance, PlayerChoiceContext choiceContext,
        AttackCommand command, ref Task __result)
    {
        // 只有玩家自己发起的攻击才会消耗玩家活力；敌人攻击直接走原逻辑（不会匹配消耗）。
        if (command.Attacker != __instance.Owner)
        {
            return true;
        }

        var firepower = __instance.Owner?.GetPower<Powers.FirepowerPower>();
        if (firepower != null && firepower.Amount > 0)
        {
            MomoiDiag.Log($"[Firepower] AfterAttack intercepted: vigor={__instance.Amount} firepower={firepower.Amount}");
            // 清除攻击绑定：否则手牌中攻击牌伤害预览不会显示活力加成。
            __instance.GetInternalData<VigorPower.Data>().commandToModify = null;
            __result = FirepowerHooks.ConsumeFirepowerAsync(choiceContext, firepower);
            return false; // 跳过原方法：活力不消耗。
        }

        MomoiDiag.Log($"[Firepower] AfterAttack normal: vigor={__instance.Amount} firepower=0");
        return true; // 无火力：原版逻辑（活力正常消耗）。
    }
}
