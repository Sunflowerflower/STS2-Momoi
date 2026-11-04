using Godot;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Characters;

public sealed class STS2_MomoiCardPool : TypeListCardPoolModel
{
    // 左粉右蓝的浅色渐变卡框（只改颜色/描边，不加元素）。
    private static Material? PoolFrameGradientMaterial =>
        ResourceLoader.Load<Material>($"{Entry.ResPath}/materials/momoi_card_frame_gradient.tres");

    // Title 和 EnergyColorName 是池子的稳定标识，不是玩家看到的角色名。
    // 自定义角色卡、遗物、药水池保持同一个 EnergyColorName，方便实验室和文本统一读取能量图标。
    public override string Title => "STS2_Momoi";
    public override string EnergyColorName => "STS2_Momoi";

    // 这里指定卡牌文本和大图使用的能量图标路径。
    // res://STS2_Momoi/... 里的 STS2_Momoi 是 PCK 资源目录，不是 C# namespace。
    public override string? BigEnergyIconPath => $"{Entry.ResPath}/images/characters/energy_big.png";
    public override string? TextEnergyIconPath => $"{Entry.ResPath}/images/characters/energy_text.png";

    public override Color DeckEntryCardColor => STS2_MomoiCharacter.ThemeColor;
    public override Color EnergyOutlineColor => STS2_MomoiCharacter.MomoiPink;
    public override Material? PoolFrameMaterial => PoolFrameGradientMaterial;

    // false 表示这是角色专属卡池，不是事件/状态那类无色卡池。
    public override bool IsColorless => false;
}