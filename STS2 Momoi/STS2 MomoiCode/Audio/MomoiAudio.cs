using System.Collections.Concurrent;
using Godot;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Nodes;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using STS2_Momoi.Diagnostics;
using STS2_Momoi.Settings;
using STS2RitsuLib.Audio;

namespace STS2_Momoi.Audio;

/// <summary>六档音量：总音量 × 音乐/语音/音效/受击/死亡。低频音效直接走 AudioStreamPlayer 时也走这里。</summary>
public static class MomoiAudio
{
    // 直放音效（免死/死亡）以前每次都 ResourceLoader.Load 一次音频，现在读一次就缓存。
    private static readonly ConcurrentDictionary<string, AudioStream> StreamCache = new();

    public static float MasterGain => Mathf.Clamp(MomoiSettingsStore.MasterVolume.Read(), 0, 100) / 100f;
    public static float MusicGain => MasterGain * Mathf.Clamp(MomoiSettingsStore.MusicVolume.Read(), 0, 100) / 100f;
    public static float VoiceGain => MasterGain * Mathf.Clamp(MomoiSettingsStore.VoiceVolume.Read(), 0, 100) / 100f;
    public static float SfxGain => MasterGain * Mathf.Clamp(MomoiSettingsStore.SfxVolume.Read(), 0, 100) / 100f;
    public static float HurtGain => MasterGain * Mathf.Clamp(MomoiSettingsStore.HurtVoiceVolume.Read(), 0, 100) / 100f;
    public static float DeathGain => MasterGain * Mathf.Clamp(MomoiSettingsStore.DeathVoiceVolume.Read(), 0, 700) / 100f;

    public static float MusicVolumeDb => Mathf.LinearToDb(Mathf.Max(0.0001f, MusicGain));

    public static void PlayVoice(string eventPath) => Play(eventPath, VoiceGain);
    public static void PlaySfx(string eventPath) => Play(eventPath, SfxGain);
    public static void PlayHurtVoice(string eventPath) => Play(eventPath, HurtGain);

    /// <summary>Flash/其他必须由 SfxCmd 自己播放的事件先刷新注册音量。</summary>
    public static void PrepareVoice(string eventPath) => Prepare(eventPath, VoiceGain);
    public static void PrepareSfx(string eventPath) => Prepare(eventPath, SfxGain);

    private static void Play(string eventPath, float gain)
    {
        if (!MomoiSfx.Paths.TryGetValue(eventPath, out _))
        {
            SfxCmd.Play(eventPath);
            return;
        }

        Prepare(eventPath, gain);
        SfxCmd.Play(eventPath);
    }

    private static void Prepare(string eventPath, float gain)
    {
        if (MomoiSfx.Paths.TryGetValue(eventPath, out var resourcePath))
        {
            VirtualFmodEventRegistry.RegisterOneShot(eventPath, resourcePath, volume: Mathf.Max(0.0001f, gain));
        }
    }

    /// <summary>
    /// 免死/死亡等战斗结束边界用：绕过 SfxCmd 的 combat-ending 静默检查，直接 AudioStreamPlayer。
    /// </summary>
    public static void PlayDirectVoice(string eventPath) => PlayDirect(eventPath, VoiceGain);
    public static void PlayDirectSfx(string eventPath) => PlayDirect(eventPath, SfxGain);
    public static void PlayDirectDeathVoice(string eventPath) => PlayDirect(eventPath, DeathGain);

    private static void PlayDirect(string eventPath, float gain)
    {
        if (!MomoiSfx.Paths.TryGetValue(eventPath, out var resourcePath))
        {
            SfxCmd.Play(eventPath);
            return;
        }

        var stream = StreamCache.GetOrAdd(resourcePath,
            static path => ResourceLoader.Load<AudioStream>(path));
        if (stream is null)
        {
            Entry.Logger.Info($"[Audio] direct missing {resourcePath}");
            return;
        }

        if (stream is AudioStreamOggVorbis ogg)
        {
            ogg.Loop = false;
        }

        Node? parent = NRun.Instance?.GlobalUi;
        parent ??= NRun.Instance;
        parent ??= NCombatRoom.Instance?.CombatVfxContainer;
        parent ??= NCombatRoom.Instance;
        // 事件死亡/主动放弃时 NRun 可能已在切换；NGame 是更稳定的兜底父节点。
        parent ??= NGame.Instance;
        if (parent is null)
        {
            Entry.Logger.Info($"[Audio] direct no parent {eventPath}");
            return;
        }

        var player = new AudioStreamPlayer
        {
            Stream = stream,
            Bus = "SFX",
            VolumeDb = Mathf.LinearToDb(Mathf.Max(0.0001f, gain)),
        };
        parent.AddChild(player);
        player.Finished += player.QueueFree;
        player.Play();
        if (MomoiDiag.Enabled)
        {
            MomoiDiag.Log($"[Audio] direct {eventPath} gain={gain:0.00} parent={parent.GetType().Name}");
        }
    }
}
