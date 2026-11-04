using Godot;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Helpers;
using MegaCrit.Sts2.Core.Nodes;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using MegaCrit.Sts2.Core.Nodes.Vfx;

namespace STS2_Momoi.Cards;

/// <summary>复用的原版 VFX 组合。</summary>
public static class MomoiVfx
{
    /// <summary>原版焚烧地面火焰，不附带音效。</summary>
    public static void PlayGroundFire(Creature target)
    {
        var fire = NGroundFireVfx.Create(target);
        if (fire is not null)
        {
            NCombatRoom.Instance?.CombatVfxContainer.AddChildSafely(fire);
        }
    }

    /// <summary>恶魔之焰：目标脚下地面火焰 + 火焰攻击音效。</summary>
    public static void PlayFiendFire(Creature target)
    {
        PlayGroundFire(target);
        SfxCmd.Play("event:/sfx/characters/attack_fire");
    }

    public sealed class WhirlwindHandle : IDisposable
    {
        private readonly Node? _lines;
        private readonly Node? _vignette;

        public WhirlwindHandle(Node? lines, Node? vignette)
        {
            _lines = lines;
            _vignette = vignette;
        }

        public void Dispose()
        {
            if (_lines is not null && GodotObject.IsInstanceValid(_lines))
            {
                _lines.QueueFree();
            }

            if (_vignette is not null && GodotObject.IsInstanceValid(_vignette))
            {
                _vignette.QueueFree();
            }
        }
    }

    /// <summary>旋风斩：全屏横线 + 烟雾暗角；persistent=true 时由调用方在攻击结束后 Dispose。</summary>
    public static WhirlwindHandle PlayWhirlwind(int hitCount, bool persistent = false)
    {
        var color = new Color("FFFFFF80");
        var seconds = persistent ? 120.0 : 0.8 + Mathf.Min(8, hitCount) * 0.3;
        var lines = NHorizontalLinesVfx.Create(color, seconds);
        NCombatRoom.Instance?.CombatVfxContainer.AddChildSafely(lines);
        var vignette = NSmokyVignetteVfx.Create(color, color);
        NRun.Instance?.GlobalUi.AddChildSafely(vignette);
        return new WhirlwindHandle(lines, vignette);
    }
}
