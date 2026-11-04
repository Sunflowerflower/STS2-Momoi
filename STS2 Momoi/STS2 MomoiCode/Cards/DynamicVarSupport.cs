using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;

namespace STS2_Momoi.Cards;

/// <summary>
/// 带独立 base/extra 的计算变量：允许同一张卡同时拥有多个 CalculatedVar / CalculatedDamageVar。
/// 原版 CalculatedVar 固定取 DynamicVars.CalculationBase / CalculationExtra，
/// 当一张卡需要同时显示两个计算值时（例如伤害 + 攻击次数）会互相冲突。
/// 值 = baseVar.BaseValue + extraVar.BaseValue × multiplier。
///
/// ⚠ <b>为什么按名字实时取、而不是记住构造时那两个实例</b>：
/// <c>DynamicVarSet.Clone()</c>（每次进战斗 / 降级都会跑）是逐个 <c>v.Clone()</c>，而
/// <c>DynamicVar.Clone()</c> 只是 <c>MemberwiseClone()</c> —— 于是克隆出来的本类对象里
/// <c>_base</c>/<c>_extra</c> 仍然指向**规范化实例**，而 <c>DynamicVars["BurnBase"].UpgradeValueBy(1)</c>
/// 升的是这张卡自己的那个克隆。结果就是「曳光弹」升级后灼烧层数怎么都不涨
/// （卡面与结算读的都是那个没被升级的原实例）。
/// 改成运行时按名字从持有者的 DynamicVars 里取，就永远是当前这张卡自己的值。
/// 取不到时（owner 还没接上等）退回构造时那个实例，保证不会崩。
/// </summary>
public sealed class IndependentCalculatedVar : CalculatedVar
{
    private readonly string _baseName;
    private readonly string _extraName;
    private readonly DynamicVar _baseFallback;
    private readonly DynamicVar _extraFallback;

    public IndependentCalculatedVar(string name, DynamicVar baseVar, DynamicVar extraVar)
        : base(name)
    {
        _baseName = baseVar.Name;
        _extraName = extraVar.Name;
        _baseFallback = baseVar;
        _extraFallback = extraVar;
    }

    protected override DynamicVar GetBaseVar() => Resolve(_baseName, _baseFallback);

    protected override DynamicVar GetExtraVar() => Resolve(_extraName, _extraFallback);

    private DynamicVar Resolve(string name, DynamicVar fallback)
    {
        if (_owner is CardModel card && card.DynamicVars is { } set && set.TryGetValue(name, out var v))
        {
            return v;
        }

        return fallback;
    }
}
