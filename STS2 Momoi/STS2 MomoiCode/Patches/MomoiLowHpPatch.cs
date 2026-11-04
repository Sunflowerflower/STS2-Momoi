using Godot;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Context;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Nodes.Combat;
using MegaCrit.Sts2.Core.Nodes.Screens;
using MegaCrit.Sts2.Core.Nodes.Screens.Overlays;
using MegaCrit.Sts2.Core.Models.Encounters;
using STS2_Momoi.Audio;
using STS2_Momoi.Characters;
using STS2_Momoi.Settings;
using STS2RitsuLib.Patching.Models;
using STS2RitsuLib.Scaffolding.Visuals.StateMachine;

namespace STS2_Momoi.Patches;

/// <summary>记录每个战斗形象根当前使用的 RitsuLib 状态机，供残血控制器读取 Current.Id。</summary>
public static class MomoiAnimMachineRegistry
{
    private static readonly System.Runtime.CompilerServices.ConditionalWeakTable<Node, ModAnimStateMachine>
        Machines = new();

    public static void Register(Node owner, ModAnimStateMachine machine)
    {
        if (owner is not null && GodotObject.IsInstanceValid(owner))
        {
            Machines.AddOrUpdate(owner, machine);
        }
    }

    public static ModAnimStateMachine? TryGet(Node? owner)
    {
        return owner is not null
               && GodotObject.IsInstanceValid(owner)
               && Machines.TryGetValue(owner, out var machine)
            ? machine
            : null;
    }
}

/// <summary>状态机 Start / SetTrigger 后登记，避免反射 internal RitsuLib 补丁类。</summary>
public class MomoiAnimMachineTrackPatch : IPatchMethod
{
    public static string PatchId => "momoi_anim_machine_track";
    public static string Description => "缓存王小桃战斗状态机，供残血动画读取当前状态。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
    [
        new(typeof(ModAnimStateMachine), nameof(ModAnimStateMachine.Start)),
    ];

    public static void Postfix(ModAnimStateMachine __instance)
    {
        if (__instance.Backend?.OwnerNode is { } owner)
        {
            MomoiAnimMachineRegistry.Register(owner, __instance);
        }
    }
}

/// <summary>
/// 王小桃的残血表现：
/// - 战斗内 HP / MaxHP &lt;= 25% 时切到 low_hp 残血待机；
/// - 播放一次残血 BGM，播完仍残血就重复，离开残血不打断当前这一遍；
/// - 战斗结束（CombatState 消失）停止音频。
/// 用挂在 NCreature 上的节点轮询，避免给角色额外加一个会显示在 UI 上的 Power/Relic。
/// </summary>
public partial class MomoiLowHpController : Node
{
    private const double LowHpThreshold = 0.25;
    private const string LowHpBgmPath = "res://STS2_Momoi/audio/low_hp_bgm.ogg";

    private NCreature? _creature;
    private AudioStreamPlayer? _audio;
    private ICombatState? _combatState;
    private bool _low;
    private bool _streamTried;
    private bool _isLocal;
    private ulong _lastHurtAtMs;
    private Creature? _hpHookedEntity;
    private bool _audioSuppressed;
    private bool _fadingOut;
    private float _fadeElapsed;
    private float _fadeStartDb;
    private bool _loggedLowState;
    private bool _lowTriggerFallback;
    private const float StopFadeSeconds = 2.0f;

    public override void _Ready()
    {
        _creature = GetParent<NCreature>();
        _isLocal = _creature.Entity is not null && LocalContext.IsMe(_creature.Entity);
        if (_creature.Entity is not null)
        {
            _hpHookedEntity = _creature.Entity;
            _hpHookedEntity.CurrentHpChanged += OnCurrentHpChanged;
        }

        _audio = new AudioStreamPlayer
        {
            Name = "LowHpBgm",
            Bus = "SFX",
        };
        AddChild(_audio);
        _audio.Finished += OnAudioFinished;
    }

    public override void _Process(double delta)
    {
        if (_creature is null || !GodotObject.IsInstanceValid(_creature))
        {
            return;
        }

        var entity = _creature.Entity;
        if (entity is null)
        {
            return;
        }

        // NCreature 可能被复用；Entity 变化时把受伤事件挂到当前实体上。
        if (!ReferenceEquals(entity, _hpHookedEntity))
        {
            if (_hpHookedEntity is not null)
            {
                _hpHookedEntity.CurrentHpChanged -= OnCurrentHpChanged;
            }

            _hpHookedEntity = entity;
            _isLocal = LocalContext.IsMe(entity);
            _hpHookedEntity.CurrentHpChanged += OnCurrentHpChanged;
        }

        var state = entity.CombatState;
        if (!ReferenceEquals(state, _combatState))
        {
            _combatState = state;
            _low = false;
            _audioSuppressed = false;
            _loggedLowState = false;
            _lowTriggerFallback = false;
            // 新战斗开始时硬复位；战斗结束不在这里 Stop，也不打断正在进行的淡出。
            // 进入最终建筑师对话场景时保留当前声音，让下面的 2s 淡出负责收尾。
            if (state is not null)
            {
                _fadingOut = false;
                _fadeElapsed = 0f;
                if (state.Encounter is not TheArchitectEventEncounter)
                {
                    StopAudio();
                }
            }
        }

        // 奖励界面出现时开始 2s 淡出；不要等 CombatState 清空。
        if (IsRewardScreenVisible())
        {
            _low = false;
            _audioSuppressed = true;
            BeginStopFade();
            UpdateStopFade(delta);
            return;
        }

        if (state is not null && state.Encounter is TheArchitectEventEncounter)
        {
            // 最终建筑师的对话场景里不要响残血 BGM；如果在响，做 2s 淡出。
            _low = false;
            _audioSuppressed = true;
            BeginStopFade();
            UpdateStopFade(delta);
            return;
        }

        // 死亡 / 战斗结束也走 2s 淡出，避免突然截断两分钟的 BGM。
        // 死亡语音由全局 CreatureDiedEvent 处理，覆盖战斗内、事件死亡和主动放弃。
        if (state is null || entity.IsDead)
        {
            _low = false;
            _audioSuppressed = true;
            BeginStopFade();
            UpdateStopFade(delta);
            return;
        }

        if (_fadingOut)
        {
            // 奖励界面可能在淡出途中关闭；仍然把这一遍淡完，不再重新拉起。
            UpdateStopFade(delta);
            return;
        }

        ApplyConfiguredVolume();

        var isLow = entity.GetHpPercentRemaining() <= LowHpThreshold;
        if (isLow != _low)
        {
            _low = isLow;
            if (isLow)
            {
                // 如果上一遍还在播，不重新叠一层；播完后 OnAudioFinished 会按当前
                // 残血状态决定是否续播。
                StartAudioIfNeeded();
            }
            // 离开残血时不调用 Stop：让这一遍自然播完，播完再根据 _low 决定不续播。
        }

        if (isLow)
        {
            ShowLowHpIdle();
        }
        else
        {
            ShowNormalIdle();
        }
    }

    private void OnCurrentHpChanged(int oldHp, int newHp)
    {
        if (!_isLocal || newHp >= oldHp
            || _creature is null
            || !GodotObject.IsInstanceValid(_creature)
            || _creature.Entity?.CombatState is null)
        {
            return;
        }

        // 死亡音由 CreatureDiedEvent 统一处理，避免事件死亡/主动放弃漏掉或与免死音重叠。
        if (newHp <= 0)
        {
            return;
        }

        var now = Time.GetTicksMsec();
        if (now - _lastHurtAtMs < 120)
        {
            return;
        }

        _lastHurtAtMs = now;
        MomoiAudio.PlayHurtVoice(MomoiSfx.Hurt);
    }

    private void ShowLowHpIdle()
    {
        if (_creature is null)
        {
            return;
        }

        var machine = TryGetMachine(_creature);
        var current = machine?.Current?.Id;
        if (!_loggedLowState)
        {
            _loggedLowState = true;
            Entry.Logger.Info(
                $"[LowHp] machine={machine is not null} current={current ?? "null"} " +
                $"hasTrigger={machine?.HasTrigger("LowHp")} hasAnim={machine?.Backend?.HasAnimation("low_hp")}");
        }

        if (current is null or "idle")
        {
            if (machine is null)
            {
                // 反射拿不到状态机时，至少跨入残血时直接触发一次；不每帧重触发，
                // 避免把 low_hp 反复重启。
                if (!_lowTriggerFallback)
                {
                    _lowTriggerFallback = true;
                    _creature.SetAnimationTrigger("LowHp");
                }
            }
            else
            {
                _creature.SetAnimationTrigger("LowHp");
            }
        }
    }

    private void ShowNormalIdle()
    {
        if (_creature is null)
        {
            return;
        }

        var machine = TryGetMachine(_creature);
        if (machine?.Current?.Id == "low_hp")
        {
            _creature.SetAnimationTrigger("Idle");
        }

        _loggedLowState = false;
        _lowTriggerFallback = false;
    }

    private static ModAnimStateMachine? TryGetMachine(NCreature creature)
    {
        // 由下方 MomoiAnimMachineTrackPatch 在 Start/SetTrigger 后记录；
        // 这样不依赖 RitsuLib 内部补丁类的反射，版本兼容性更好。
        return MomoiAnimMachineRegistry.TryGet(creature.Visuals) ?? MomoiAnimMachineRegistry.TryGet(creature);
    }

    private void StartAudioIfNeeded()
    {
        // 多人模式只让本地玩家播自己的残血 BGM；远端小桃仍然会切 low_hp。
        if (!_isLocal || _audio is null)
        {
            return;
        }

        if (!_streamTried)
        {
            _streamTried = true;
            var stream = ResourceLoader.Load<AudioStream>(LowHpBgmPath);
            if (stream is null)
            {
                Entry.Logger.Info($"[LowHp] audio missing: {LowHpBgmPath}");
                return;
            }

            // OGG 导入默认 loop=false；这里再兜底一次，保证 Finished 能触发。
            if (stream is AudioStreamOggVorbis ogg)
            {
                ogg.Loop = false;
            }

            _audio.Stream = stream;
        }

        if (_audio.Stream is not null && !_audio.Playing && !_audioSuppressed)
        {
            _audio.VolumeDb = GetConfiguredVolumeDb();
            _audio.Play();
        }
    }

    private void OnAudioFinished()
    {
        if (_low
            && _creature is not null
            && GodotObject.IsInstanceValid(_creature)
            && _creature.Entity?.CombatState is not null
            && _creature.Entity.IsAlive)
        {
            StartAudioIfNeeded();
        }
    }

    private static bool IsRewardScreenVisible()
    {
        return NOverlayStack.Instance?.Peek() is NRewardsScreen;
    }

    private static float GetConfiguredVolumeDb()
    {
        // 音乐音量 × 总音量；0% 用 -80 dB 静音。
        return MomoiAudio.MusicVolumeDb;
    }

    private void ApplyConfiguredVolume()
    {
        if (_audio is null)
        {
            return;
        }

        var db = GetConfiguredVolumeDb();
        if (!Mathf.IsEqualApprox(_audio.VolumeDb, db))
        {
            _audio.VolumeDb = db;
        }
    }

    private void BeginStopFade()
    {
        if (_audio is null || !_audio.Playing || _fadingOut)
        {
            return;
        }

        _fadingOut = true;
        _fadeElapsed = 0f;
        _fadeStartDb = _audio.VolumeDb;
    }

    private void UpdateStopFade(double delta)
    {
        if (!_fadingOut || _audio is null)
        {
            return;
        }

        if (!_audio.Playing)
        {
            _fadingOut = false;
            return;
        }

        _fadeElapsed += (float)delta;
        var t = Mathf.Clamp(_fadeElapsed / StopFadeSeconds, 0f, 1f);
        _audio.VolumeDb = Mathf.Lerp(_fadeStartDb, -80f, t);
        if (t >= 1f)
        {
            _audio.Stop();
            _fadingOut = false;
            _audio.VolumeDb = GetConfiguredVolumeDb();
        }
    }

    private void StopAudio()
    {
        _fadingOut = false;
        _fadeElapsed = 0f;
        if (_audio is not null && _audio.Playing)
        {
            _audio.Stop();
        }

        if (_audio is not null)
        {
            _audio.VolumeDb = GetConfiguredVolumeDb();
        }
    }

    public override void _ExitTree()
    {
        if (_hpHookedEntity is not null)
        {
            _hpHookedEntity.CurrentHpChanged -= OnCurrentHpChanged;
            _hpHookedEntity = null;
        }

        if (_audio is not null)
        {
            _audio.Finished -= OnAudioFinished;
            _audio.Stop();
        }

        base._ExitTree();
    }
}

/// <summary>战斗角色节点就绪时，只给王小桃本体挂一个残血控制器。</summary>
public class MomoiLowHpPatch : IPatchMethod
{
    public static string PatchId => "momoi_low_hp";
    public static string Description => "王小桃残血待机与残血 BGM。";
    public static bool IsCritical => false;

    public static ModPatchTarget[] GetTargets() =>
        [new(typeof(NCreature), "_Ready")];

    public static void Postfix(NCreature __instance)
    {
        if (__instance.Entity?.Player?.Character is not STS2_MomoiCharacter)
        {
            return;
        }

        if (__instance.GetNodeOrNull<MomoiLowHpController>(MomoiLowHpControllerName) is not null)
        {
            return;
        }

        __instance.AddChild(new MomoiLowHpController { Name = MomoiLowHpControllerName });
    }

    private const string MomoiLowHpControllerName = "MomoiLowHpController";
}
