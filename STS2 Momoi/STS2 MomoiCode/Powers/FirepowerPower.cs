using MegaCrit.Sts2.Core.Entities.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Powers;

/// <summary>
/// 火力：当活力因原版消耗逻辑要被全部消耗时，改为消耗 1 层火力并保留活力。
/// </summary>
[RegisterPower]
public sealed class FirepowerPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/firepower_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/firepower_power.png");
}
