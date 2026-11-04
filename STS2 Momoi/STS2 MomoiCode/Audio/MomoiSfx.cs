using System.Collections.Generic;
using STS2RitsuLib.Audio;

namespace STS2_Momoi.Audio;

/// <summary>王小桃模组自定义音效的 virtual FMOD 事件路径。</summary>
public static class MomoiSfx
{
    public const string Hurt = "event:/STS2_Momoi/sfx/hurt";
    public const string BaBoot = "event:/STS2_Momoi/sfx/ba_boot";
    public const string CreativePain = "event:/STS2_Momoi/sfx/creative_pain";
    public const string CreativePainImpact = "event:/STS2_Momoi/sfx/creative_pain_impact";
    public const string MinigameGenerated = "event:/STS2_Momoi/sfx/minigame_generated";
    public const string WinningScript = "event:/STS2_Momoi/sfx/winning_script";
    public const string Gunshot = "event:/STS2_Momoi/sfx/gunshot";
    public const string DeathVoice = "event:/STS2_Momoi/sfx/death_voice";
    public const string WatchOutVoice = "event:/STS2_Momoi/sfx/watch_out_voice";
    public const string MaidWeaponVoice = "event:/STS2_Momoi/sfx/maid_weapon_voice";
    public const string Revive = "event:/STS2_Momoi/sfx/revive";

    public static readonly IReadOnlyDictionary<string, string> Paths = new Dictionary<string, string>
    {
        [Hurt] = "res://STS2_Momoi/audio/hurt.ogg",
        [BaBoot] = "res://STS2_Momoi/audio/ba_boot.ogg",
        [CreativePain] = "res://STS2_Momoi/audio/creative_pain.ogg",
        [CreativePainImpact] = "res://STS2_Momoi/audio/creative_pain_impact.ogg",
        [MinigameGenerated] = "res://STS2_Momoi/audio/minigame_generated.ogg",
        [WinningScript] = "res://STS2_Momoi/audio/winning_script.ogg",
        [Gunshot] = "res://STS2_Momoi/audio/gunshot.wav",
        [DeathVoice] = "res://STS2_Momoi/audio/death_voice.ogg",
        [WatchOutVoice] = "res://STS2_Momoi/audio/watch_out_voice.ogg",
        [MaidWeaponVoice] = "res://STS2_Momoi/audio/maid_weapon_voice.ogg",
        [Revive] = "res://STS2_Momoi/audio/revive.ogg",
    };

    public static void Register()
    {
        VirtualFmodEventRegistry.RegisterOneShots(new Dictionary<string, string>(Paths));
    }
}
