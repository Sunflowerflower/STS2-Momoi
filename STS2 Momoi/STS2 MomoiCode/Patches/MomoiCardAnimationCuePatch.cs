using System.Runtime.CompilerServices;
using Godot;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Hooks;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Nodes.Combat;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using STS2_Momoi.Cards;
using STS2_Momoi.Characters;
using STS2RitsuLib.Patching.Models;
using STS2RitsuLib.Scaffolding.Visuals.StateMachine;
using STS2_Momoi.Diagnostics;

namespace STS2_Momoi.Patches;

/// <summary>
/// 卡牌 -> 战斗动画的分流：
///   一般攻击 = attack1；支援牌里的攻击牌 = attack2；构想 = attack3（先只给它）
///   稀有 Power = cast2；其他 Power / 技能 = cast1
///   嘲讽 / WIN！ = taunt1
/// 卡牌出手时在 <see cref="Hook.BeforeCardPlayed"/> 主动播一次，并压制同一张牌后续的
/// Attack/Cast/PowerUp 触发器，避免攻击牌再触发一次通用 attack1。
/// </summary>
public static class MomoiCardAnimationCue
{
    private sealed class SuppressState
    {
        public bool Value;
        public string? AttackCue;
    }

    private static readonly ConditionalWeakTable<Node, SuppressState> Suppressed = new();

    public static void Suppress(Node visuals)
    {
        Suppressed.GetOrCreateValue(visuals).Value = true;
    }

    public static void ClearSuppress(Node visuals)
    {
        if (Suppressed.TryGetValue(visuals, out var state))
        {
            state.Value = false;
            state.AttackCue = null;
        }
    }

    public static void SetAttackCue(Node visuals, string cue)
    {
        Suppressed.GetOrCreateValue(visuals).AttackCue = cue;
    }

    public static string? GetAttackCue(Node? visuals)
    {
        return visuals != null && Suppressed.TryGetValue(visuals, out var state)
            ? state.AttackCue
            : null;
    }

    public static bool IsSuppressed(Node? visuals)
    {
        return visuals != null && Suppressed.TryGetValue(visuals, out var state) && state.Value;
    }

    public static string? Choose(CardModel card)
    {
        // 这两张牌点名用嘲讽动画。
        if (card is Taunt or WinCard)
        {
            return "Taunt1";
        }

        // 构想先单独用攻击动画3（它是技能牌，所以走 Cast 时也由这里决定）。
        if (card is ConceptCard)
        {
            return "Attack3";
        }

        if (card.Type == CardType.Attack)
        {
            // 支援牌里有攻击牌（大部分没有 support tag，按类型判定）。
            return MinigameSupport.IsSupportCardType(card) ? "Attack2" : "Attack1";
        }

        if (card.Type == CardType.Power)
        {
            // 稀有 = 能力动画2；其他（罕见/无稀有度/普通）= 能力动画1。
            return card.Rarity == CardRarity.Rare ? "Cast2" : "Cast1";
        }

        // 普通技能 / 状态 / 诅咒：技能动画还没做，先不播（保持 idle）。
        // 等技能动画做好后，在这里按卡牌返回 cast1/技能 cue。
        return null;
    }

    public static void Trigger(NCreature? node, CardModel card)
    {
        if (node?.Visuals == null)
        {
            return;
        }

        var cue = Choose(card);
        if (cue == null)
        {
            // 技能动画待补：压制这张牌后续的 Attack/Cast/PowerUp，保持 idle。
            Suppress(node.Visuals);
            MomoiDiag.Log($"[Visual] card cue (skill animation pending) for {card.Id.Entry}");
            return;
        }

        // 攻击牌交给 AttackCommand 的逐段 TriggerAnim：
        // 每次伤害前都会发 "Attack"，这里只记录本次卡牌要用的 attack1/2/3，
        // 由 SetTrigger 的 Prefix 把每段 "Attack" 改写成对应动画。
        // HundredPull 例外：100 连抽只播一次攻击动画。
        if (card.Type == CardType.Attack && card is not HundredPull)
        {
            SetAttackCue(node.Visuals, cue);
            MomoiDiag.Log($"[Visual] per-hit cue {cue} for {card.Id.Entry}");
            return;
        }

        node.SetAnimationTrigger(cue);
        Suppress(node.Visuals);
        MomoiDiag.Log($"[Visual] card cue {cue} for {card.Id.Entry}");
    }
}

/// <summary>卡牌开始结算时播该牌对应的动画（此时牌已进入出牌区，时机和原版 Cast/Attack 接近）。</summary>
public class MomoiBeforeCardPlayedCuePatch : IPatchMethod
{
    public static string PatchId => "momoi_before_card_played_cue";
    public static string Description => "按卡牌类型/稀有度选择 attack1/2/3、cast1/2、taunt1。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Hook), nameof(Hook.BeforeCardPlayed))];

    public static void Prefix(ICombatState combatState, CardPlay cardPlay)
    {
        var player = cardPlay.Player;
        if (player?.Character is not STS2_MomoiCharacter)
        {
            return;
        }

        var node = NCombatRoom.Instance?.GetCreatureNode(player.Creature);
        MomoiCardAnimationCue.Trigger(node, cardPlay.Card);
    }
}

/// <summary>卡牌结算结束后解除压制，避免影响能力/遗物等非卡牌触发的默认动画。</summary>
public class MomoiAfterCardPlayedCuePatch : IPatchMethod
{
    public static string PatchId => "momoi_after_card_played_cue";
    public static string Description => "卡牌结束后清掉本次卡牌的动画压制标记。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Hook), nameof(Hook.AfterCardPlayed))];

    public static void Prefix(ICombatState combatState, PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = cardPlay.Player;
        if (player?.Character is not STS2_MomoiCharacter)
        {
            return;
        }

        var node = NCombatRoom.Instance?.GetCreatureNode(player.Creature);
        if (node?.Visuals != null)
        {
            MomoiCardAnimationCue.ClearSuppress(node.Visuals);
        }
    }
}

/// <summary>
/// 压制同一张牌后续的标准触发器：卡牌已经主动播了 attack2/attack3/cast2/taunt1 等，
/// 不能让 AttackCommand / PowerCmd 再触发一次通用 Attack/Cast/PowerUp 把动画重置。
/// </summary>
public class MomoiStateMachineCueSuppressPatch : IPatchMethod
{
    public static string PatchId => "momoi_state_machine_cue_suppress";
    public static string Description => "卡牌播放期间压制标准 Attack/Cast/PowerUp 触发器。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(ModAnimStateMachine), nameof(ModAnimStateMachine.SetTrigger))];

    public static bool Prefix(ModAnimStateMachine __instance, string trigger)
    {
        // 攻击牌：把每一段标准 Attack 改写成这张牌对应的 attack1/2/3。
        if (trigger == "Attack")
        {
            var cue = MomoiCardAnimationCue.GetAttackCue(__instance.Backend.OwnerNode);
            if (cue != null)
            {
                __instance.SetTrigger(cue);
                return false;
            }
        }

        if (trigger is "Attack" or "Cast" or "PowerUp"
            && MomoiCardAnimationCue.IsSuppressed(__instance.Backend.OwnerNode))
        {
            return false;
        }

        return true;
    }
}
