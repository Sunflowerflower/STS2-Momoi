using Godot;
using MegaCrit.Sts2.Core.Commands.Builders;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Nodes.Vfx;
using STS2_Momoi.Audio;

namespace STS2_Momoi.Cards;

/// <summary>王小桃枪械类攻击：单体每次命中一发，对群每次命中一组弹幕；枪声按卡牌选择。</summary>
public static class MomoiGunStyle
{
    private static readonly Color SingleTint = new("FFD0A0");
    private static readonly Color BarrageFlurryTint = new("F5A9C9");
    private static readonly Color BarrageImpactTint = new("FFE08A");

    /// <summary>单体枪械：每次命中一发飞刀。</summary>
    public static AttackCommand Apply(AttackCommand attack, Creature owner)
    {
        return attack.WithHitVfxNode(target =>
        {
            MomoiAudio.PlaySfx(MomoiSfx.Gunshot);
            // NShivThrowVfx 是单发飞刀 + 命中，不是 NDaggerSprayFlurry 的整组弹幕。
            return NShivThrowVfx.Create(owner, target, SingleTint);
        });
    }

    /// <summary>
    /// 对群枪械/弹幕：每一段命中在攻击者侧生成一组弹幕（粉），并在每个目标身上生成命中特效（黄）。
    /// AttackCommand 默认每段都触发 WithAttackerFx，所以 3 段就是 3 组，间隔由调用方的停顿控制。
    /// </summary>
    public static AttackCommand ApplyBarrage(AttackCommand attack, Creature owner, bool playGunshot)
    {
        return attack
            .WithAttackerFx(() =>
            {
                if (playGunshot)
                {
                    MomoiAudio.PlaySfx(MomoiSfx.Gunshot);
                }

                return NDaggerSprayFlurryVfx.Create(owner, BarrageFlurryTint, goingRight: true);
            })
            .WithHitVfxNode(target =>
                NDaggerSprayImpactVfx.Create(target, BarrageImpactTint, goingRight: true));
    }
}
