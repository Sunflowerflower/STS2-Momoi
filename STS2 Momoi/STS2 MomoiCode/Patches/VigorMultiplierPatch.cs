using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using STS2_Momoi.Cards;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 「活力在这张牌上发挥 n 倍的效果」：把原版 <see cref="VigorPower.ModifyDamageAdditive"/> 的返回值乘 n。
///
/// 为什么只能补丁、不能改卡：
/// * 原版结算时 <c>Hook.ModifyDamageInternal</c> 做的是 <c>num += 各 power 的 ModifyDamageAdditive 返回值</c>，
///   力量与活力走的是同一条加伤通道 —— 在卡里手动再加一次就成了 1+n 倍（而不是 n 倍）。
///   劫持返回值只改「加多少」，不影响「吃不吃」（活力那堆 dealer / cardSource 判定原样保留）。
/// * <see cref="VigorPower"/> 是 <c>sealed</c>，没法继承出子类。
/// * 多段牌每段都会走这个钩子，所以 n 倍天然按段生效。
///
/// 目前只有「破势」在用：活力 ×4（升级 ×5）。
/// </summary>
public class VigorMultiplierPatch : IPatchMethod
{
    public static string PatchId => "momoi_vigor_multiplier";

    public static string Description => "破势：活力在这张牌上发挥 4/5 倍效果（乘在 VigorPower 的加伤返回值上）。";

    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(VigorPower), nameof(VigorPower.ModifyDamageAdditive))];

    public static void Postfix(CardModel? cardSource, ref decimal __result)
    {
        if (__result == 0m || cardSource is not MomentumBreak momentum)
        {
            return;
        }

        __result *= momentum.IsUpgraded ? 5m : 4m;
    }
}
