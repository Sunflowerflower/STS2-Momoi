using System;
using System.IO;
using System.Reflection;
using Godot;
using MegaCrit.Sts2.Core.Debug;
using STS2RitsuLib;
using STS2RitsuLib.Data;
using STS2RitsuLib.Settings;
using STS2RitsuLib.Utils.Persistence;

namespace STS2_Momoi.Settings;

/// <summary>
/// 王小桃模组的持久化设置。
/// 以后新增选项（卡牌数值微调、新事件、只在选王小桃时触发等）都加到这里，
/// 然后在 <see cref="MomoiSettingsStore.Init"/> 的页面上加对应控件。
/// </summary>
public sealed class MomoiModSettings
{
    // 色彩哲学家事件是否追加王小桃卡池。
    public bool PhilosopherPool { get; set; } = true;

    // 奥罗巴斯「海玻璃」是否出现王小桃这一项。
    public bool SeaGlassPool { get; set; } = true;

    // 跨角色随机来源是否出现本模组卡牌：飞溅 / 万花筒 / 棱彩宝石。
    // 关闭后其他角色遇不到小桃的牌，也不影响别人自己的卡池。
    public bool SplashPool { get; set; } = true;
    public bool KaleidoscopePool { get; set; } = true;
    public bool PrismaticGemPool { get; set; } = true;

    // 角色战斗贴图大小倍率（0.5~1.5，默认 1.0）。作用于玩家角色，怪物不受影响。
    // 王小桃自己的 0.7 是写死在补丁里的（相当于「素材比例」），不经过这个设置。
    public double CharacterTextureScale { get; set; } = 1.0;

    // 排查用详细日志（出牌动画、活力/火力消耗等热路径）。默认关闭：那几条日志在每回合会被写几十次盘。
    public bool VerboseLogging { get; set; }

    // 六档音量：前五档 0-100，死亡 0-700；总音量再乘到其余各档上。
    public int MasterVolume { get; set; } = 100;
    public int MusicVolume { get; set; } = 100;
    public int VoiceVolume { get; set; } = 100;
    public int SfxVolume { get; set; } = 100;
    public int HurtVoiceVolume { get; set; } = 100;
    // 死亡语音单独放大；默认 500%，最高 700%。素材本身很小，避免被受击/其他语音淹没。
    public int DeathVoiceVolume { get; set; } = 500;

    // 旧版默认 180% 的一次性迁移标记；迁移后用户仍可自由调低。
    public bool DeathVoiceVolumeMigrated { get; set; } = false;
}

/// <summary>设置页「诊断」用到的版本与日志路径。</summary>
public static class MomoiModInfo
{
    /// <summary>模组版本（来自程序集版本，csproj 里的 &lt;Version&gt;）。</summary>
    public static string ModVersion { get; } = ReadModVersion();

    /// <summary>游戏版本（v0.111.0 这种）。</summary>
    public static string GameVersion
    {
        get
        {
            try
            {
                return ReleaseInfoManager.Instance.ReleaseInfo?.Version ?? "未知";
            }
            catch
            {
                return "未知";
            }
        }
    }

    /// <summary>报错时要发给作者的日志目录（游戏 user:// 目录下的 logs，按当前账号解析）。</summary>
    public static string LogsDirectory => Path.Combine(OS.GetUserDataDir(), "logs");

    /// <summary>在文件管理器里打开日志目录（目录不存在就退回到用户数据目录）。</summary>
    public static void OpenLogsFolder()
    {
        try
        {
            var dir = LogsDirectory;
            if (!Directory.Exists(dir))
            {
                dir = OS.GetUserDataDir();
            }

            OS.ShellShowInFileManager(dir);
        }
        catch (Exception e)
        {
            Entry.Logger.Warn($"[Settings] open logs folder failed: {e.Message}");
        }
    }

    private static string ReadModVersion()
    {
        try
        {
            var v = Assembly.GetExecutingAssembly().GetName().Version;
            if (v != null)
            {
                // 1.0.0.0 -> 1.0.0
                return v.Revision > 0 ? v.ToString() : $"{v.Major}.{v.Minor}.{v.Build}";
            }
        }
        catch
        {
            // ignore
        }

        return "1.0.0";
    }
}

public static class MomoiSettingsStore
{
    private const string Key = "settings";

    public static readonly ModSettingsValueBinding<MomoiModSettings, bool> PhilosopherPool =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.PhilosopherPool,
            static (s, v) => s.PhilosopherPool = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, bool> SeaGlassPool =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.SeaGlassPool,
            static (s, v) => s.SeaGlassPool = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, bool> SplashPool =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.SplashPool,
            static (s, v) => s.SplashPool = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, bool> KaleidoscopePool =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.KaleidoscopePool,
            static (s, v) => s.KaleidoscopePool = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, bool> PrismaticGemPool =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.PrismaticGemPool,
            static (s, v) => s.PrismaticGemPool = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, double> CharacterTextureScale =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.CharacterTextureScale,
            static (s, v) => s.CharacterTextureScale = v);

    /// <summary>角色贴图倍率（读出来就钳到 0.5~1.5，防止手改 settings.json 写坏数值）。</summary>
    public static float TextureScaleFactor
        => (float)Math.Clamp(CharacterTextureScale.Read(), 0.5, 1.5);

    /// <summary>排查用详细日志开关（热路径上的日志只在它打开时输出）。</summary>
    public static readonly ModSettingsValueBinding<MomoiModSettings, bool> VerboseLogging =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.VerboseLogging,
            static (s, v) => s.VerboseLogging = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, int> MasterVolume =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.MasterVolume,
            static (s, v) => s.MasterVolume = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, int> MusicVolume =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.MusicVolume,
            static (s, v) => s.MusicVolume = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, int> VoiceVolume =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.VoiceVolume,
            static (s, v) => s.VoiceVolume = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, int> SfxVolume =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.SfxVolume,
            static (s, v) => s.SfxVolume = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, int> HurtVoiceVolume =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.HurtVoiceVolume,
            static (s, v) => s.HurtVoiceVolume = v);

    public static readonly ModSettingsValueBinding<MomoiModSettings, int> DeathVoiceVolume =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.DeathVoiceVolume,
            static (s, v) => s.DeathVoiceVolume = v);

    private static readonly ModSettingsValueBinding<MomoiModSettings, bool> DeathVoiceVolumeMigrated =
        new(Entry.ModId, Key, SaveScope.Global,
            static s => s.DeathVoiceVolumeMigrated,
            static (s, v) => s.DeathVoiceVolumeMigrated = v);

    public static void Init()
    {
        ModDataStore.For(Entry.ModId).Register<MomoiModSettings>(
            key: Key,
            fileName: "settings.json",
            scope: SaveScope.Global,
            defaultFactory: static () => new MomoiModSettings(),
            autoCreateIfMissing: true);

        // 旧版 180%（旧默认）/200%（旧上限）一次性提升到 500%；不碰 0/100 等主动设置。
        if (!DeathVoiceVolumeMigrated.Read())
        {
            var oldDeathVolume = DeathVoiceVolume.Read();
            if (oldDeathVolume is >= 180 and <= 200)
            {
                DeathVoiceVolume.Write(500);
                DeathVoiceVolume.Save();
            }

            DeathVoiceVolumeMigrated.Write(true);
            DeathVoiceVolumeMigrated.Save();
        }

        RitsuLibFramework.RegisterModSettings(Entry.ModId, page => page
            .WithTitle(ModSettingsText.Literal("游戏王小桃"))
            // 暂时不显示模组简介（默认会把清单里的 description 显示在页面顶部）。
            .WithDescriptionHidden(true)
            .AddSection("general", section => section
                .WithTitle(ModSettingsText.Literal("通用"))
                .AddToggle(
                    "philosopher_pool",
                    ModSettingsText.Literal("色彩哲学家出现该角色卡池"),
                    PhilosopherPool)
                .AddToggle(
                    "seaglass_pool",
                    ModSettingsText.Literal("海玻璃出现该角色"),
                    SeaGlassPool)
                .AddToggle(
                    "splash_pool",
                    ModSettingsText.Literal("飞溅出现该角色卡牌"),
                    SplashPool)
                .AddToggle(
                    "kaleidoscope_pool",
                    ModSettingsText.Literal("万花筒出现该角色卡牌"),
                    KaleidoscopePool)
                .AddToggle(
                    "prismatic_gem_pool",
                    ModSettingsText.Literal("棱彩宝石出现该角色卡牌"),
                    PrismaticGemPool)
                .AddSlider(
                    "character_texture_scale",
                    ModSettingsText.Literal("角色贴图大小"),
                    CharacterTextureScale,
                    0.5,
                    1.5,
                    0.05,
                    static v => $"{v:0.00}x"))
            .AddSection("audio", section => section
                .WithTitle(ModSettingsText.Literal("音量"))
                .AddIntSlider("master_volume", ModSettingsText.Literal("总音量"), MasterVolume, 0, 100, 5, static v => $"{v}%")
                .AddIntSlider("music_volume", ModSettingsText.Literal("音乐音量"), MusicVolume, 0, 100, 5, static v => $"{v}%")
                .AddIntSlider("voice_volume", ModSettingsText.Literal("语音音量"), VoiceVolume, 0, 100, 5, static v => $"{v}%")
                .AddIntSlider("sfx_volume", ModSettingsText.Literal("音效音量"), SfxVolume, 0, 100, 5, static v => $"{v}%")
                .AddIntSlider("hurt_voice_volume", ModSettingsText.Literal("受击语音音量"), HurtVoiceVolume, 0, 100, 5, static v => $"{v}%")
                .AddIntSlider("death_voice_volume", ModSettingsText.Literal("死亡语音音量"), DeathVoiceVolume, 0, 700, 5, static v => $"{v}%"))
            .AddSection("progress", section => section
                .WithTitle(ModSettingsText.Literal("其他"))
                .AddButton(
                    "unlock_compendium",
                    ModSettingsText.Literal("解锁全部图鉴"),
                    ModSettingsText.Literal("把本模组的卡牌 / 遗物 / 药水标记为已发现，卡牌图鉴不再显示问号"),
                    () => Patches.MomoiCompendiumUnlock.MarkAll(),
                    ModSettingsButtonTone.Normal,
                    ModSettingsText.Literal("解锁"))
                .AddButton(
                    "reset_settings",
                    ModSettingsText.Literal("重置本模组设置"),
                    ModSettingsText.Literal("把上面的开关与全部音量恢复默认值"),
                    ResetToDefaults,
                    ModSettingsButtonTone.Danger,
                    ModSettingsText.Literal("重置")))
            .AddSection("diagnostics", section => section
                .WithTitle(ModSettingsText.Literal("诊断"))
                .AddToggle(
                    "verbose_logging",
                    ModSettingsText.Literal("输出详细日志"),
                    VerboseLogging,
                    ModSettingsText.Literal("排查用：把出牌动画、活力/火力消耗等细节写进 godot.log。平时请关着，开着头会很卡。"))
                .AddInfoCard(
                    "version_info",
                    ModSettingsText.Dynamic(() => $"游戏王小桃 {MomoiModInfo.ModVersion}"),
                    ModSettingsText.Dynamic(() => $"游戏 {MomoiModInfo.GameVersion}"),
                    ModSettingsText.Dynamic(() =>
                        "报错请截图这一页，并点下面的按钮打开日志目录，把最新的 [gold]godot.log[/gold] 一起发出来。\n"
                        + $"日志目录：[gold]{MomoiModInfo.LogsDirectory}[/gold]\n"
                        + "依赖：RitsuLib 0.6.7+"))
                .AddButton(
                    "open_logs",
                    ModSettingsText.Literal("打开日志目录"),
                    ModSettingsText.Literal("在文件管理器里打开游戏日志所在的文件夹（跨平台，按当前账号的 user:// 目录解析）"),
                    MomoiModInfo.OpenLogsFolder,
                    ModSettingsButtonTone.Normal,
                    ModSettingsText.Literal("打开"))));
    }

    /// <summary>把本模组的全部设置恢复默认值（只动 mod 自己的 settings.json）。</summary>
    public static void ResetToDefaults()
    {
        var defaults = new MomoiModSettings();

        PhilosopherPool.Write(defaults.PhilosopherPool);
        SeaGlassPool.Write(defaults.SeaGlassPool);
        SplashPool.Write(defaults.SplashPool);
        KaleidoscopePool.Write(defaults.KaleidoscopePool);
        PrismaticGemPool.Write(defaults.PrismaticGemPool);
        CharacterTextureScale.Write(defaults.CharacterTextureScale);
        VerboseLogging.Write(defaults.VerboseLogging);
        MasterVolume.Write(defaults.MasterVolume);
        MusicVolume.Write(defaults.MusicVolume);
        VoiceVolume.Write(defaults.VoiceVolume);
        SfxVolume.Write(defaults.SfxVolume);
        HurtVoiceVolume.Write(defaults.HurtVoiceVolume);
        DeathVoiceVolume.Write(defaults.DeathVoiceVolume);
        DeathVoiceVolumeMigrated.Write(true);

        PhilosopherPool.Save();
        SeaGlassPool.Save();
        SplashPool.Save();
        KaleidoscopePool.Save();
        PrismaticGemPool.Save();
        CharacterTextureScale.Save();
        VerboseLogging.Save();
        MasterVolume.Save();
        MusicVolume.Save();
        VoiceVolume.Save();
        SfxVolume.Save();
        HurtVoiceVolume.Save();
        DeathVoiceVolume.Save();
        DeathVoiceVolumeMigrated.Save();

        Entry.Logger.Info("[Settings] reset to defaults");
    }
}
