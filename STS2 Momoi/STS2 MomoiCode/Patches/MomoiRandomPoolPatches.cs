using System;
using System.Collections.Generic;
using System.Linq;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Relics;
using MegaCrit.Sts2.Core.Unlocks;
using STS2_Momoi.Characters;
using STS2_Momoi.Settings;
using STS2RitsuLib.Patching.Models;

namespace STS2_Momoi.Patches;

/// <summary>
/// 跨角色随机来源（飞溅 / 万花筒 / 棱彩宝石）的角色隔离。
///
/// 原版这三条途径最后都只读 <see cref="UnlockState.CharacterCardPools"/>
/// （= <c>Characters.Select(c =&gt; c.CardPool)</c>，UnlockState.cs:111）：
/// 飞溅 Splash.cs:25、万花筒 Kaleidoscope.cs:40、棱彩宝石 PrismaticGem.cs:46。
/// 所以我们**不**去改每张牌的 <c>CanBeGeneratedInCombat</c>（那会连自己角色在战斗内的随机生成一起挡掉），
/// 而是在这三个入口各打一个「作用域」标记：标记期间 <see cref="HideOurPoolNow"/> 为真，
/// 由 <see cref="MomoiCharacterCardPoolsPatch"/> 在读取角色池集合时把本模组的角色池摘掉。
///
/// 作用域只覆盖入口方法里**同步**的那一段（这三个入口都是在第一次 await 之前就把集合读完的），
/// 前缀置位、后缀复位，用 [ThreadStatic] 计数防重入。
/// 因此「自己玩王小桃」时完全不受影响：飞溅/万花筒本来就会排除自己的角色池，棱彩宝石的
/// <c>options.CardPools</c> 里也还有自己的池兜底，摘掉集合里的重复项不会让候选变成空的。
/// </summary>
public static class MomoiPoolIsolation
{
    [ThreadStatic] private static int _splashDepth;
    [ThreadStatic] private static int _kaleidoscopeDepth;
    [ThreadStatic] private static int _prismaticGemDepth;

    /// <summary>当前这次读取角色池集合要不要隐藏本模组卡池（只在三个入口的作用域内可能为真）。</summary>
    public static bool HideOurPoolNow =>
        (_splashDepth > 0 && !MomoiSettingsStore.SplashPool.Read())
        || (_kaleidoscopeDepth > 0 && !MomoiSettingsStore.KaleidoscopePool.Read())
        || (_prismaticGemDepth > 0 && !MomoiSettingsStore.PrismaticGemPool.Read());

    /// <summary>是不是本模组的角色卡池（衍生牌 TokenCardPool 不在角色池集合里，不用管）。</summary>
    public static bool IsOurPool(CardPoolModel? pool) => pool is STS2_MomoiCardPool;

    public static void EnterSplash() => _splashDepth++;
    public static void ExitSplash() => _splashDepth = Math.Max(0, _splashDepth - 1);

    public static void EnterKaleidoscope() => _kaleidoscopeDepth++;
    public static void ExitKaleidoscope() => _kaleidoscopeDepth = Math.Max(0, _kaleidoscopeDepth - 1);

    public static void EnterPrismaticGem() => _prismaticGemDepth++;
    public static void ExitPrismaticGem() => _prismaticGemDepth = Math.Max(0, _prismaticGemDepth - 1);
}

/// <summary>
/// 角色池集合的唯一收口：作用域内把本模组角色池摘掉。
/// 只影响飞溅 / 万花筒 / 棱彩宝石三处的候选，色彩哲学家有自己的开关（<see cref="MomoiPhilosopherPoolPatch"/>）。
/// </summary>
public class MomoiCharacterCardPoolsPatch : IPatchMethod
{
    public static string PatchId => "momoi_character_card_pools";
    public static string Description => "跨角色随机来源（飞溅/万花筒/棱彩宝石）按设置隐藏本模组角色池。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(UnlockState), "get_CharacterCardPools")];

    public static void Postfix(ref IEnumerable<CardPoolModel> __result)
    {
        if (__result is null || !MomoiPoolIsolation.HideOurPoolNow)
        {
            return;
        }

        __result = __result.Where(pool => !MomoiPoolIsolation.IsOurPool(pool));
    }
}

/// <summary>
/// 飞溅：从「其他角色」卡池里随机 3 张攻击牌选 1 张。
/// 标记只包住 <c>OnPlay</c> 里同步的那一段（第一次 await 在 <c>FromChooseACardScreen</c>）。
/// </summary>
public class MomoiSplashPoolPatch : IPatchMethod
{
    public static string PatchId => "momoi_splash_pool";
    public static string Description => "飞溅按设置隐藏本模组卡牌。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Splash), "OnPlay", new[] { typeof(PlayerChoiceContext), typeof(CardPlay) })];

    public static void Prefix() => MomoiPoolIsolation.EnterSplash();

    public static void Postfix() => MomoiPoolIsolation.ExitSplash();
}

/// <summary>
/// 万花筒：每份奖励从其他角色池里随机取 3 个池各 1 张。
/// 注意不能走 <c>CardCreationOptions.WithFilter</c>：单池被过滤空之后
/// <c>CardFactory.CreateForReward</c> 会抛 InvalidOperationException（Kaleidoscope.cs:44 的 <c>.First()</c> 也拿不到东西）。
/// 所以这里只把「我们的池」从候选池列表里摘掉，剩下的池照原样随机，Take(3) 自然少一个。
/// </summary>
public class MomoiKaleidoscopePoolPatch : IPatchMethod
{
    public static string PatchId => "momoi_kaleidoscope_pool";
    public static string Description => "万花筒按设置隐藏本模组卡牌。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(Kaleidoscope), "AfterObtained")];

    public static void Prefix() => MomoiPoolIsolation.EnterKaleidoscope();

    public static void Postfix() => MomoiPoolIsolation.ExitKaleidoscope();
}

/// <summary>
/// 棱彩宝石：把玩家的角色卡池 union 进奖励候选池。
/// 摘掉我们的池是安全的——union 里原本就有玩家自己的角色池，不会变空。
/// </summary>
public class MomoiPrismaticGemPoolPatch : IPatchMethod
{
    public static string PatchId => "momoi_prismatic_gem_pool";
    public static string Description => "棱彩宝石按设置隐藏本模组卡牌。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(PrismaticGem), nameof(PrismaticGem.ModifyCardRewardCreationOptions))];

    public static void Prefix() => MomoiPoolIsolation.EnterPrismaticGem();

    public static void Postfix() => MomoiPoolIsolation.ExitPrismaticGem();
}
