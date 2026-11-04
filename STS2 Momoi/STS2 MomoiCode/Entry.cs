using System.Reflection;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Logging;
using MegaCrit.Sts2.Core.Modding;
using STS2RitsuLib;
using STS2_Momoi.Settings;
using STS2RitsuLib.Interop;
using STS2RitsuLib.Patching.Core;
using Logger = MegaCrit.Sts2.Core.Logging.Logger;

namespace STS2_Momoi;

[ModInitializer(nameof(Initialize))]
public partial class Entry
{
    // ModId 需要和 STS2_Momoi.json 里的 id 保持一致。
    // res://STS2_Momoi/... 里的 STS2_Momoi 是 PCK 资源目录，不是 C# namespace。
    public const string ModId = "STS2_Momoi";
    public const string ResPath = $"res://{ModId}";

    public static Logger Logger { get; } = new(ModId, LogType.Generic);



    public static void Initialize()
    {
        var assembly = Assembly.GetExecutingAssembly();

        // 以下示例默认已经在 Entry.Initialize() 中调用了
        // RitsuLibFramework.EnsureGodotScriptsRegistered(...) 和
        // ModTypeDiscoveryHub.RegisterModAssembly(...)，否则自动注册不会生效。
        //
        // Godot C# 脚本注册只负责让 pck 中的脚本类型能被 Godot 找到。
        // 这一步和 RitsuLib 的内容自动注册不是同一件事，两个都需要保留。
        RitsuLibFramework.EnsureGodotScriptsRegistered(assembly, Logger);

        // 自动注册扫描会读取当前程序集里的 RegisterCard/RegisterRelic 等 attribute。
        // 新增内容类后，只要 attribute 写对，通常不需要在入口里手动逐个注册。
        ModTypeDiscoveryHub.RegisterModAssembly(ModId, assembly);

        // 小游戏标签（连连看/消消乐等小游戏牌共用，柚子护航用它识别小游戏牌）。
        // fullgame：游戏牌（可掉落、不可临时加入、享受小游戏牌增益）；support：支援牌。
        var tagRegistry = RitsuLibFramework.GetCardTagRegistry(ModId);
        tagRegistry.RegisterOwned("minigame");
        tagRegistry.RegisterOwned("fullgame");
        tagRegistry.RegisterOwned("support");

        // 自定义音效：注册为 RitsuLib virtual FMOD 事件，之后统一走 SfxCmd.Play。
        Audio.MomoiSfx.Register();

        // 设置页：色彩哲学家 / 海玻璃开关；以后更多视觉/数值选项也放这里。
        MomoiSettingsStore.Init();

        // 死亡语音走全局死亡事件，覆盖战斗死亡、事件死亡和主动放弃。
        // 放在设置初始化之后，保证事件触发时能读到死亡音量。
        Audio.MomoiDeathVoice.Register();

        // run 级统计（真理部/C&C 解锁进度等）：新局开始重置。
        MegaCrit.Sts2.Core.Runs.RunManager.Instance.RunStarted += run =>
        {
            RunStats.Reset();
            // 旧版「游戏人生」把 fullgame 标签写进了牌组本尊（克隆体与本体共用 _tags），会随存档跨局保留。
            // 这里在开局时清掉那些“本来不是游戏牌”的牌上的标签。
            foreach (var player in run.Players)
            {
                Cards.MinigameSupport.StripLeakedGameCardTags(player.Deck.Cards);
            }
        };

        // 火力机制：拦截活力消耗（有火力时改为消耗火力、保留活力）。
        var patcher = RitsuLibFramework.CreatePatcher(ModId, "core-patches");
        patcher.RegisterPatch<Patches.VigorRebindPatch>();
        patcher.RegisterPatch<Patches.VigorConsumePatch>();
        patcher.RegisterPatch<Patches.VigorMultiplierPatch>();
        patcher.RegisterPatch<CombatStartResetPatch>();
        patcher.RegisterPatch<MinigamePlayedPatch>();
        patcher.RegisterPatch<FirepowerGainedPatch>();
        patcher.RegisterPatch<PlayerTurnEndSnapshotPatch>();
        patcher.RegisterPatch<DiscardTrackingPatch>();
        patcher.RegisterPatch<TurnDiscardResetPatch>();
        patcher.RegisterPatch<Patches.DustyTomeAfterObtainedPatch>();
        patcher.RegisterPatch<Patches.MinigameCardSidebarPatch>();
        patcher.RegisterPatch<GrindingCurseTrackPatch>();
        patcher.RegisterPatch<Patches.CardKeywordLabelPatch>();
        patcher.RegisterPatch<Patches.MomoiBeforeCardPlayedCuePatch>();
        patcher.RegisterPatch<Patches.MomoiAfterCardPlayedCuePatch>();
        patcher.RegisterPatch<Patches.MomoiStateMachineCueSuppressPatch>();
        patcher.RegisterPatch<Patches.MomoiSelectScreenResetPatch>();
        patcher.RegisterPatch<Patches.MomoiSelectBgPreloadPatch>();
        patcher.RegisterPatch<Patches.MomoiSelectBgmPatch>();
        patcher.RegisterPatch<Patches.MomoiPhilosopherPoolPatch>();
        patcher.RegisterPatch<Patches.MomoiSeaGlassPoolPatch>();
        patcher.RegisterPatch<Patches.MomoiCharacterCardPoolsPatch>();
        patcher.RegisterPatch<Patches.MomoiSplashPoolPatch>();
        patcher.RegisterPatch<Patches.MomoiKaleidoscopePoolPatch>();
        patcher.RegisterPatch<Patches.MomoiPrismaticGemPoolPatch>();
        patcher.RegisterPatch<Patches.MomoiCardFrameMaterialPatch>();
        patcher.RegisterPatch<Patches.MomoiCardFrameVisualPatch>();
        patcher.RegisterPatch<Patches.MomoiLowHpPatch>();
        patcher.RegisterPatch<Patches.MomoiReviveSfxPatch>();
        patcher.RegisterPatch<Patches.MomoiAnimMachineTrackPatch>();
        patcher.RegisterPatch<Patches.MomoiEnergyIconPathPatch>();
        patcher.RegisterPatch<Patches.MomoiArchitectCutscenePatch>();
        patcher.RegisterPatch<Patches.MomoiImbuedDrawPilePatch>();
        patcher.RegisterPatch<Patches.MomoiCompendiumUnlockPatch>();
        patcher.RegisterPatch<Patches.MomoiCreatureScaleToPatch>();
        patcher.RegisterPatch<Patches.MomoiCombatRoomAddCreaturePatch>();
        patcher.RegisterPatch<Patches.MomoiCueWarmupPatch>();
        if (!patcher.PatchAll())
        {
            throw new InvalidOperationException("Critical patches failed.");
        }

        Logger.Info("STS2_Momoi initialized.");
    }
}