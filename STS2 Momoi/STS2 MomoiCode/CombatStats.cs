using System.Collections.Generic;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Runs;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Hooks;
using MegaCrit.Sts2.Core.Models;
using STS2_Momoi.Cards;
using STS2_Momoi.Powers;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi;

/// <summary>
/// 本场战斗的跨卡共享统计（战斗开始由 Patch 重置）。
/// </summary>
public static class CombatStats
{
    /// <summary>本场战斗打出过的小游戏牌次数（阅历连击 / 集结 / 游戏学习）。</summary>
    public static int MinigamesPlayed { get; private set; }

    /// <summary>本场战斗获得过的火力层数总和（火力打击）。</summary>
    public static int TotalFirepowerGained { get; private set; }

    /// <summary>本场战斗获得过的小游戏牌名（拾遗 / 游戏王形态的去重依据）。</summary>
    public static readonly HashSet<string> ObtainedMinigames = new();

    /// <summary>上一张打出的小游戏牌（来自真纪的协助）。</summary>
    public static CardModel? LastPlayedMinigame { get; private set; }

    /// <summary>本场战斗打出过的支援牌次数（集结费用减免）。</summary>
    public static int SupportCardsPlayed { get; private set; }

    /// <summary>本场战斗打出过的相遇次数（所有相遇共享解锁进度）。</summary>
    public static int EncounterPlays { get; private set; }

    /// <summary>白与黑本场战斗的选择（战斗结束恢复两个选项）。</summary>
    public static string? WhiteBlackChoice { get; set; }

    /// <summary>本回合打出过的牌（不含复制品，轮回用）。</summary>
    public static readonly List<CardModel> ThisTurnPlayed = new();

    /// <summary>上一回合打出过的牌（不含复制品，轮回用）。</summary>
    public static readonly List<CardModel> LastTurnPlayed = new();

    /// <summary>本回合进入过弃牌堆的牌（循环叙事用）。</summary>
    public static readonly List<CardModel> ThisTurnDiscarded = new();


    public static int RecordEncounterPlay() => ++EncounterPlays;

    public static void RecordPlayedThisTurn(CardModel card)
    {
        // 上回合通过轮回打出的复制品也要能被下一回合的轮回重放，因此不排除 IsDupe。
        if (card != null && !ThisTurnPlayed.Contains(card))
        {
            ThisTurnPlayed.Add(card);
        }
    }

    public static void OnPlayerTurnEnd()
    {
        LastTurnPlayed.Clear();
        LastTurnPlayed.AddRange(ThisTurnPlayed);
        ThisTurnPlayed.Clear();
    }

    public static void RecordSupportPlayed() => SupportCardsPlayed++;

    /// <summary>记录一张牌进入弃牌堆（循环叙事）。</summary>
    public static void RecordDiscardedThisTurn(CardModel card)
    {
        if (card != null && !ThisTurnDiscarded.Contains(card))
        {
            ThisTurnDiscarded.Add(card);
        }
    }

    public static void ClearDiscardedThisTurn() => ThisTurnDiscarded.Clear();

    public static void Reset()
    {
        MinigamesPlayed = 0;
        TotalFirepowerGained = 0;
        ObtainedMinigames.Clear();
        LastPlayedMinigame = null;
        SupportCardsPlayed = 0;
        EncounterPlays = 0;
        WhiteBlackChoice = null;
        ThisTurnPlayed.Clear();
        LastTurnPlayed.Clear();
        ThisTurnDiscarded.Clear();
        Cards.GrindingCursePool.Reset();
    }

    public static void RecordMinigamePlayed(CardModel card)
    {
        MinigamesPlayed++;
        LastPlayedMinigame = card;
    }

    public static void RecordFirepowerGained(int amount) => TotalFirepowerGained += amount;


    public static void RecordMinigameObtained(CardModel card)
    {
        if (MinigameSupport.IsMinigameCard(card))
        {
            ObtainedMinigames.Add(card.Id.Entry);
        }
    }
}

/// <summary>任意牌堆变化后：记录本回合进入过弃牌堆的牌（循环叙事）。</summary>
public class DiscardTrackingPatch : IPatchMethod
{
    public static string PatchId => "momoi_discard_tracking";
    public static string Description => "记录本回合进入过弃牌堆的牌（循环叙事）。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Hook), nameof(Hook.AfterCardChangedPiles))];

    public static void Prefix(CardModel card, PileType oldPile)
    {
        if (card?.Pile?.Type == PileType.Discard && oldPile != PileType.Discard)
        {
            CombatStats.RecordDiscardedThisTurn(card);
        }
    }
}

/// <summary>玩家回合开始时：清空「本回合进入过弃牌堆」记录。</summary>
public class TurnDiscardResetPatch : IPatchMethod
{
    public static string PatchId => "momoi_turn_discard_reset";
    public static string Description => "玩家回合开始时清空循环叙事的弃牌记录。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Hook), nameof(Hook.BeforeSideTurnStart))];

    public static void Prefix(CombatSide side)
    {
        if (side == CombatSide.Player)
        {
            CombatStats.ClearDiscardedThisTurn();
        }
    }
}

/// <summary>战斗开始时重置跨卡统计。</summary>
public class CombatStartResetPatch : IPatchMethod
{
    public static string PatchId => "momoi_combat_start_reset";
    public static string Description => "战斗开始时重置本 mod 的跨卡统计。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Hook), nameof(Hook.BeforeCombatStart))];

    public static void Prefix(IRunState runState, ICombatState? combatState)
    {
        CombatStats.Reset();
        // 「游戏人生」的游戏牌标记只在本场战斗生效，新战斗一律清空。
        MinigameSupport.ClearTemporaryGameCards();
    }
}

/// <summary>玩家回合结束时：把本回合打出的牌快照为"上回合打出的牌"（轮回）。</summary>
public class PlayerTurnEndSnapshotPatch : IPatchMethod
{
    public static string PatchId => "momoi_player_turn_end_snapshot";
    public static string Description => "玩家回合结束时快照上回合打出的牌（轮回复制依据）。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Hook), nameof(Hook.BeforeSideTurnEnd))];

    public static void Prefix(CombatSide side, IEnumerable<Creature> participants)
    {
        if (side == CombatSide.Player)
        {
            CombatStats.OnPlayerTurnEnd();
        }
    }
}

/// <summary>本场战斗中生成卡牌时：记录开荒的「特定诅咒」池。</summary>
public class GrindingCurseTrackPatch : IPatchMethod
{
    public static string PatchId => "momoi_grinding_curse_track";
    public static string Description => "记录本场战斗中生成过的特定诅咒（开荒的诅咒池）。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Hook), nameof(Hook.AfterCardGeneratedForCombat))];

    public static void Prefix(ICombatState combatState, CardModel card, Player? creator)
    {
        if (card != null)
        {
            Cards.GrindingCursePool.Record(card);
        }
    }
}

/// <summary>任意卡打出后：小游戏牌计数 +1（阅历连击等）。</summary>
public class MinigamePlayedPatch : IPatchMethod
{
    public static string PatchId => "momoi_minigame_played";
    public static string Description => "记录本场战斗打出过的小游戏牌次数。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Hook), nameof(Hook.AfterCardPlayed))];

    public static void Prefix(ICombatState combatState, PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        CombatStats.RecordPlayedThisTurn(cardPlay.Card);

        if (MinigameSupport.IsMinigameCard(cardPlay.Card))
        {
            CombatStats.RecordMinigamePlayed(cardPlay.Card);
        }

        // 支援牌要按「tag 或类型」两边判：大部分支援牌没有 support tag，只有 IsSupportCardType 认得。
        if (MinigameSupport.IsSupportCard(cardPlay.Card) || MinigameSupport.IsSupportCardType(cardPlay.Card))
        {
            CombatStats.RecordSupportPlayed();
            // 集结的减费改由 Rally.TryModifyEnergyCostInCombat 每次读取时现算（见 MiscRareCards.cs），
            // 这里不再追加 EnergyCost.AddThisCombat —— 否则会和那个 hook 叠一次，变成减 2 倍。
        }
    }
}

/// <summary>火力层数变化时累计本场获得总量（火力打击）。</summary>
public class FirepowerGainedPatch : IPatchMethod
{
    public static string PatchId => "momoi_firepower_gained";
    public static string Description => "累计本场战斗获得过的火力层数。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Hook), nameof(Hook.BeforePowerAmountChanged))];

    public static void Prefix(ICombatState combatState, PowerModel power, decimal amount,
        Creature target, Creature? applier, CardModel? cardSource)
    {
        if (power is FirepowerPower && amount > 0)
        {
            CombatStats.RecordFirepowerGained((int)amount);
        }
    }
}
