using MegaCrit.Sts2.Core.Commands.Builders;
using MegaCrit.Sts2.Core.Nodes.Vfx;

namespace STS2_Momoi.Cards;

/// <summary>君王之剑：大王斩击 VFX + 君王之剑斩击音效。</summary>
public static class MomoiSovereignStyle
{
    public static AttackCommand Apply(AttackCommand attack)
    {
        return attack
            .WithAttackerFx(null, "event:/sfx/characters/regent/regent_sovereign_blade")
            .WithHitVfxNode(NBigSlashVfx.Create)
            .WithHitVfxNode(NBigSlashImpactVfx.Create);
    }
}
