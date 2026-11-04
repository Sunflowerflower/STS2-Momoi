using System;
using Godot;
using MegaCrit.Sts2.Core.Nodes.Cards;
using STS2_Momoi.Characters;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 直接对已经生成好的 NCard 覆盖 %Frame.Material。
/// 卡牌模型属性可能被 RitsuLib/原版的其他 prefix 再覆盖，这个补丁在 Reload 之后兜底。
/// </summary>
public class MomoiCardFrameVisualPatch : IPatchMethod
{
    private static ShaderMaterial? _source;

    // 同一张图集区域（稀有度卡框）只复制一份材质：以前每次 Reload 都 Duplicate 一份，
    // 既分配新的 ShaderMaterial，又让 frame.Material 变了，Godot 会把卡的渲染状态重建一遍 —— 出牌卡顿的主因之一。
    private static readonly Dictionary<(Vector2 Offset, Vector2 Scale), ShaderMaterial> Variants = new();

    private static ShaderMaterial? Source
    {
        get
        {
            _source ??= ResourceLoader.Load<ShaderMaterial>(
                $"{Entry.ResPath}/materials/momoi_card_frame_gradient.tres");
            return _source;
        }
    }

    public static string PatchId => "momoi_card_frame_visual";
    public static string Description => "NCard.Reload 后直接给王小桃卡牌换上渐变卡框材质。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(NCard), "Reload")];

    public static void Postfix(NCard __instance)
    {
        var model = __instance.Model;
        if (model is null)
        {
            return;
        }

        var frame = __instance.GetNodeOrNull<TextureRect>("%Frame");
        var isMomoi = model.Id.Entry.StartsWith("STS2_MOMOI_", StringComparison.Ordinal)
            || model.Pool is STS2_MomoiCardPool;
        if (!isMomoi || frame is null)
        {
            return;
        }

        // 只改 %Frame；%PortraitBorder 的稀有度材质必须保持原版。
        // Frame 的 Texture 是 AtlasTexture，shader 里的 UV 是整张图集坐标；
        // 必须按 Region/Atlas 尺寸写入归一化参数，否则正文遮罩会覆盖整张卡。
        var source = Source;
        if (source is null)
        {
            return;
        }

        var offset = Vector2.Zero;
        var scale = Vector2.One;
        if (frame.Texture is AtlasTexture atlas && atlas.Atlas is not null)
        {
            var size = atlas.Atlas.GetSize();
            if (size.X > 0 && size.Y > 0)
            {
                offset = atlas.Region.Position / size;
                scale = atlas.Region.Size / size;
            }
        }

        var key = (offset, scale);
        if (!Variants.TryGetValue(key, out var material))
        {
            material = (ShaderMaterial)source.Duplicate();
            material.SetShaderParameter("uv_offset", offset);
            material.SetShaderParameter("uv_scale", scale);
            Variants[key] = material;
        }

        // 已经是这一份材质就不用再赋值（重新赋值会让 Godot 重建一次渲染状态）。
        if (!ReferenceEquals(frame.Material, material))
        {
            frame.Material = material;
        }
    }
}
