using Godot;
using MegaCrit.Sts2.Core.Entities.Characters;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Helpers;
using MegaCrit.Sts2.Core.Nodes.Combat;
using MegaCrit.Sts2.Core.Nodes.Vfx;
using MegaCrit.Sts2.Core.Random;
using STS2_Momoi.Cards;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Characters;
using STS2RitsuLib.Scaffolding.Content;
using STS2RitsuLib.Scaffolding.Godot;
using STS2RitsuLib.Scaffolding.Visuals;
using STS2RitsuLib.Scaffolding.Visuals.Definition;
using STS2RitsuLib.Scaffolding.Visuals.StateMachine;

namespace STS2_Momoi.Characters;

[RegisterCharacter]
public sealed class
    STS2_MomoiCharacter : ModCharacterTemplate<STS2_MomoiCardPool, STS2_MomoiRelicPool, STS2_MomoiPotionPool>
{
    public static readonly Color ThemeColor = new(0.42f, 0.65f, 0.72f);
    // 王小桃的桃红色（能量数字描边 / 名字 / 事件文本统一使用）。
    public static readonly Color MomoiPink = new("D95C97");

    private const string SceneRoot = $"{Entry.ResPath}/scenes/characters";
    private const string ImageRoot = $"{Entry.ResPath}/images/characters";
    private const string RelicRoot = $"{Entry.ResPath}/images/relics";
    private const string CueRoot = $"{ImageRoot}/cue";
    // 战斗模型：走 RitsuLib 的非 Spine 方案（VisualCueSet + Sprite2D）。
    // 以前这里指向原版 `res://scenes/creature_visuals/ironclad.tscn`，所以进战斗站着的是铁甲战士。
    private const string CharacterScenePath = $"{SceneRoot}/STS2_Momoi_character.tscn";
    private const string EnergyCounterScenePath = $"{SceneRoot}/STS2_Momoi_energy_counter.tscn";
    private const string MerchantScenePath = $"{SceneRoot}/STS2_Momoi_merchant.tscn";
    private const string RestSiteScenePath = $"{SceneRoot}/STS2_Momoi_rest_site.tscn";
    public const string SelectBg1ScenePath = $"{SceneRoot}/STS2_Momoi_character_select_bg_1.tscn";
    public const string SelectBg2ScenePath = $"{SceneRoot}/STS2_Momoi_character_select_bg_2.tscn";
    private const string CharacterSelectBgScenePath = SelectBg1ScenePath;

    // 待机：来自 `工作区/编辑区/人物/待机动画.aep` 的 comp「待机」。
    // 932x720 / 24fps / 193 帧 = 3 × 46 帧循环 + 55 帧“坐下-站起”收尾；
    // AEP 里 4×/2× 慢放造成同一张图连续出现多帧，Hold 表示保持的帧数。
    private const int IdleLoopReps = 3;
    private const float CueFps = 24f;

    // 调速倍率：1 = 原始 24fps；>1 更快，<1 更慢。
    // IdleLoopSpeed  = 站立循环（前 46 帧 × 3 轮）
    // IdleOutroSpeed = 整段收尾（坐下-站起）
    // IdleCrouchSpeed = 只作用在蹲下/站起帧（16-19 / 24-28 / 33-37），叠加在 IdleOutroSpeed 上
    private const float IdleLoopSpeed = 0.9f;
    private const float IdleOutroSpeed = 1.3f;
    private const float IdleCrouchSpeed = 1.6f;

    // 各动作速度倍率：1 = 原始 24fps；>1 更快，<1 更慢。
    private const float Attack1Speed = 1f;
    private const float Attack2Speed = 1f;
    private const float Attack3Speed = 1f;
    private const float Cast1Speed = 1f;
    private const float Cast2Speed = 1f;
    private const float Taunt1Speed = 1f;
    private const float HitSpeed = 1f;
    private const float DeadSpeed = 1f;
    private const int DeadFrameCount = 50; // 2.0833s @ 24fps

    // relaxed：参考 AEP comp「12交替频率」总时长 2.291571s；两张底图各占半个循环。
    private const float RelaxedHalfCycleSeconds = 1.1457856f;
    private const float RelaxedSpeed = 1f;

    // 选人界面随机二选一：背景场景自带对应 BGM（白天 bg1 / 夜间 bg2）。
    // 不再使用战士的选人/转场音效占位；两个 override 返回 null，避免回退铁甲战士音频。
    private static int? _selectVariant;

    public static int SelectVariant => _selectVariant ??= Rng.Chaotic.NextInt(2);
    public static void ResetSelectVariant() => _selectVariant = null;

    public override string? CustomCharacterSelectBgPath =>
        SelectVariant == 0 ? SelectBg1ScenePath : SelectBg2ScenePath;

    public override string? CustomCharacterSelectSfx => null;
    public override string? CustomCharacterTransitionSfx => null;

    private static readonly (int Frame, int Hold)[] IdleLoop =
    [
        (0, 4),
        (1, 2),
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 4),
        (6, 3),
        (7, 1),
        (8, 3),
        (9, 5),
        (10, 3),
        (11, 1),
        (12, 8),
    ];

    private static readonly (int Frame, int Hold)[] IdleOutro =
    [
        (13, 6),
        (14, 1),
        (15, 1),
        (16, 2),
        (17, 4),
        (18, 1),
        (19, 1),
        (20, 2),
        (21, 3),
        (22, 3),
        (23, 2),
        (24, 1),
        (25, 1),
        (26, 1),
        (27, 3),
        (28, 2),
        (29, 2),
        (30, 2),
        (31, 2),
        (32, 2),
        (33, 1),
        (34, 1),
        (35, 2),
        (36, 1),
        (37, 3),
        (38, 1),
        (39, 1),
        (40, 2),
        (41, 1),
    ];

    // 残血 idle：仍使用 idle 的 3 轮站立循环 + 收尾里去掉三次蹲起后的剩余帧。
    // 下标是原 idle 帧号；-1 = 被删掉的蹲起帧 16-19 / 24-28 / 33-37。
    private static readonly int[] LowHpFrameMap =
    [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1, -1, -1,
        16, 17, 18, 19, -1, -1, -1, -1, -1, 20, 21, 22, 23, -1, -1, -1, -1, -1,
        24, 25, 26, 27
    ];

    private static readonly (int Frame, int Hold)[] Attack1Frames =
    [
        (0, 2),
        (1, 1),
        (2, 2),
        (3, 1),
        (4, 1),
        (5, 9),
        (6, 1),
        (7, 4),
    ];

    private static readonly (int Frame, int Hold)[] Attack2Frames =
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 1),
        (4, 1),
        (5, 2),
        (6, 1),
        (7, 1),
        (8, 2),
        (9, 1),
        (10, 1),
        (11, 2),
        (12, 1),
        (13, 1),
        (14, 2),
        (15, 1),
        (16, 1),
        (17, 2),
        (18, 1),
        (19, 1),
        (20, 2),
        (21, 1),
        (22, 1),
        (23, 1),
    ];

    private static readonly (int Frame, int Hold)[] Attack3Frames =
    [
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (5, 2),
        (6, 2),
        (7, 2),
        (8, 2),
        (9, 2),
        (10, 2),
        (11, 2),
        (12, 2),
        (13, 2),
        (14, 2),
        (15, 1),
    ];

    private static readonly (int Frame, int Hold)[] Taunt1Frames =
    [
        (0, 3),
        (1, 1),
        (2, 1),
        (3, 3),
        (4, 1),
        (5, 3),
        (6, 1),
        (7, 1),
        (8, 3),
        (9, 1),
        (10, 3),
        (11, 1),
        (12, 1),
        (13, 3),
        (14, 1),
        (15, 3),
        (16, 1),
        (17, 1),
        (18, 3),
        (19, 1),
        (20, 2),
    ];

    private static readonly (int Frame, int Hold)[] Cast1Frames =
    [
        (0, 3),
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 1),
        (5, 1),
        (6, 1),
        (7, 1),
        (8, 1),
        (9, 1),
        (10, 1),
        (11, 1),
        (12, 1),
        (13, 1),
        (14, 1),
        (15, 1),
        (16, 1),
        (17, 1),
        (18, 1),
        (19, 1),
        (20, 1),
        (21, 1),
        (22, 1),
        (23, 23),
    ];

    private static readonly (int Frame, int Hold)[] Cast2Frames =
    [
        (0, 4),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 4),
        (5, 4),
        (6, 4),
        (7, 2),
        (8, 2),
        (9, 2),
        (10, 4),
        (11, 14),
    ];

    private static readonly (int Frame, int Hold)[] HitFrames =
    [
        (0, 1),
        (2, 1),
        (4, 1),
        (6, 1),
        (7, 1),
        (8, 1),
        (7, 1),
        (6, 17),
    ];

    private static string IdleFramePath(int frame) =>
        frame == 0 ? $"{CueRoot}/idle.png" : $"{CueRoot}/idle_{frame:00}.png";

    private static string LowHpFramePath(int frame)
    {
        var index = LowHpFrameMap[frame];
        return index == 0 ? $"{CueRoot}/low_hp.png" : $"{CueRoot}/low_hp_{index:00}.png";
    }

    private static bool IsIdleCrouch(int frame) =>
        frame is (>= 16 and <= 19) or (>= 24 and <= 28) or (>= 33 and <= 37);

    private static float IdleOutroSpeedFor(int frame) =>
        IdleOutroSpeed * (IsIdleCrouch(frame) ? IdleCrouchSpeed : 1f);

    private static string AnimFramePath(string cue, int frame) =>
        frame == 0 ? $"{CueRoot}/{cue}.png" : $"{CueRoot}/{cue}_{frame:00}.png";

    private static void AddFrames(VisualFrameSequenceBuilder seq, string cue,
        (int Frame, int Hold)[] frames, float speed)
    {
        foreach (var (frame, hold) in frames)
        {
            seq.Frame(AnimFramePath(cue, frame), hold / (CueFps * speed));
        }
    }

    // 角色名称颜色。
    public override Color NameColor => MomoiPink;

    // 能量图标轮廓颜色。
    public override Color EnergyLabelOutlineColor => MomoiPink;

    // 地图绘制颜色。
    public override Color MapDrawingColor => ThemeColor;

    // 人物性别（男女中立）。
    public override CharacterGender Gender => CharacterGender.Neutral;

    // 初始血量和金币。
    public override int StartingHp => 72;
    public override int StartingGold => 99;

    // CharacterAssetProfile 按类别拆分。你只写需要替换的部分，其他字段会保留回退。
    // AssetProfile 只指定模板自带的静态占位资源；没有复制的音频、拖尾、转场等资源继续从占位角色回退。
    public override CharacterAssetProfile AssetProfile => new(
        Scenes: new CharacterSceneAssetSet(
            // 人物模型 tscn 路径。
            VisualsPath: CharacterScenePath,
            // 能量表盘 tscn 路径。
            EnergyCounterPath: EnergyCounterScenePath,
            // 商店人物场景。
            MerchantAnimPath: MerchantScenePath,
            // 篝火休息场景。
            RestSiteAnimPath: RestSiteScenePath),
        Ui: new CharacterUiAssetSet(
            // 人物头像路径。
            IconTexturePath: $"{ImageRoot}/STS2_Momoi_character_icon.png",
            // 人物头像轮廓。
            IconOutlineTexturePath: $"{ImageRoot}/STS2_Momoi_character_icon_outline.png",
            // 左上角头像场景（像素小桃）。
            IconPath: $"{SceneRoot}/STS2_Momoi_icon.tscn",
            // 人物选择背景。
            CharacterSelectBgPath: CharacterSelectBgScenePath,
            // 人物选择图标。
            CharacterSelectIconPath: $"{ImageRoot}/STS2_Momoi_character_select.png",
            // 人物选择图标-锁定状态。
            CharacterSelectLockedIconPath: $"{ImageRoot}/STS2_Momoi_character_select_locked.png",
            // 地图上的角色标记图标、表情轮盘上的角色头像。
            MapMarkerPath: $"{ImageRoot}/STS2_Momoi_map_marker.png"),
        // 多人模式手势：4 张 422×1200。
        Multiplayer: new CharacterMultiplayerAssetSet(
            ArmPointingTexturePath: $"{ImageRoot}/STS2_Momoi_arm_point.png",
            ArmRockTexturePath: $"{ImageRoot}/STS2_Momoi_arm_rock.png",
            ArmPaperTexturePath: $"{ImageRoot}/STS2_Momoi_arm_paper.png",
            ArmScissorsTexturePath: $"{ImageRoot}/STS2_Momoi_arm_scissors.png"),
        // 卡牌拖尾：沿用原版铁甲战士拖尾场景，只把内外轨迹和火花改为粉蓝。
        Vfx: new CharacterVfxAssetSet(
            TrailPath: "res://scenes/vfx/card_trail_ironclad.tscn",
            TrailStyle: new CharacterTrailStyle(
                OuterTrailModulate: new Color("8FB8FF"),
                InnerTrailModulate: new Color("F5A9C9"),
                BigSparksColor: new Color("8FB8FF"),
                LittleSparksColor: new Color("F5A9C9"),
                PrimarySpriteModulate: new Color("8FB8FF"),
                SecondarySpriteModulate: new Color("F5A9C9"))),
        // 战斗/世界场景动画：非 Spine 的静态图或帧动画（RitsuLib VisualCueSet）。
        // 图片放 images/characters/cue/；idle 是 AEP 待机动画拆出的帧序列，
        // 其余动作仍是单张图，要改多帧把 .Single 换成 .Sequence。
        VisualCues: ModVisualCues.CueSet()
            .Sequence("idle", seq =>
            {
                for (var rep = 0; rep < IdleLoopReps; rep++)
                {
                    foreach (var (frame, hold) in IdleLoop)
                    {
                        seq.Frame(IdleFramePath(frame), hold / (CueFps * IdleLoopSpeed));
                    }
                }

                foreach (var (frame, hold) in IdleOutro)
                {
                    seq.Frame(IdleFramePath(frame), hold / (CueFps * IdleOutroSpeedFor(frame)));
                }

                seq.Loop();
            })
            .Sequence("low_hp", seq =>
            {
                // 和 idle 同一套 timing；去掉 16-19 / 24-28 / 33-37 三组蹲起。
                for (var rep = 0; rep < IdleLoopReps; rep++)
                {
                    foreach (var (frame, hold) in IdleLoop)
                    {
                        seq.Frame(LowHpFramePath(frame), hold / (CueFps * IdleLoopSpeed));
                    }
                }

                foreach (var (frame, hold) in IdleOutro)
                {
                    if (IsIdleCrouch(frame))
                    {
                        continue;
                    }

                    seq.Frame(LowHpFramePath(frame), hold / (CueFps * IdleOutroSpeedFor(frame)));
                }

                seq.Loop();
            })
            .Sequence("attack1", seq => AddFrames(seq, "attack1", Attack1Frames, Attack1Speed))
            .Sequence("attack2", seq => AddFrames(seq, "attack2", Attack2Frames, Attack2Speed))
            .Sequence("attack3", seq => AddFrames(seq, "attack3", Attack3Frames, Attack3Speed))
            .Sequence("cast1", seq => AddFrames(seq, "cast1", Cast1Frames, Cast1Speed))
            .Sequence("cast2", seq => AddFrames(seq, "cast2", Cast2Frames, Cast2Speed))
            .Sequence("taunt1", seq => AddFrames(seq, "taunt1", Taunt1Frames, Taunt1Speed))
            .Sequence("hit", seq => AddFrames(seq, "hit", HitFrames, HitSpeed))
            .Sequence("dead", seq =>
            {
                // AEP 死亡动画：50 帧 @ 24fps = 2.0833s；最后一张保持。
                for (var i = 0; i < DeadFrameCount; i++)
                {
                    seq.Frame(AnimFramePath("dead", i), 1f / CueFps / DeadSpeed);
                }
            })
            .Sequence("relaxed", seq =>
            {
                seq.Frame($"{CueRoot}/relaxed.png", RelaxedHalfCycleSeconds / RelaxedSpeed);
                seq.Frame($"{CueRoot}/relaxed_2.png", RelaxedHalfCycleSeconds / RelaxedSpeed);
                seq.Loop();
            })
            .Build(),
        // 原版遗物「美味饼干」的角色专属贴图。
        // 原版 YummyCookie 本身就是按角色出图的（yummy_cookie_ironclad/silent/regent/necro/defect），
        // 小桃不在其中会回退成铁甲战士那版，所以在这里补上小桃那一版。
        VanillaRelicVisualOverrides:
        [
            new(CharacterOwnedVanillaRelicModelId.YummyCookie, new RelicAssetProfile(
                IconPath: $"{RelicRoot}/YummyCookie_Momoi.png",
                IconOutlinePath: $"{RelicRoot}/YummyCookie_Momoi_outline.png",
                BigIconPath: $"{RelicRoot}/YummyCookie_Momoi.png"))
        ]);

    // 把模组用的原版 VFX 场景加入本角色 run 资源预载；
    // 否则 NGroundFireVfx.Create 这类 PreloadManager.Cache.GetScene 可能拿不到场景。
    protected override IEnumerable<string> ExtraAssetPaths =>
    [
        .. NGroundFireVfx.AssetPaths,
        .. NHorizontalLinesVfx.AssetPaths,
        .. NSmokyVignetteVfx.AssetPaths,
        NShivThrowVfx.scenePath,
        NDaggerSprayFlurryVfx.scenePath,
        NDaggerSprayImpactVfx.scenePath,
        NBigSlashVfx.scenePath,
        NBigSlashImpactVfx.scenePath,
        SceneHelper.GetScenePath("vfx/vfx_bite"),
        SceneHelper.GetScenePath("vfx/vfx_adrenaline"),
        SceneHelper.GetScenePath("vfx/vfx_molten_fist"),
        SceneHelper.GetScenePath("vfx/vfx_thrash"),
        SceneHelper.GetScenePath("vfx/vfx_giant_horizontal_slash"),
    ];

    // 某个字段没写时，RitsuLib 会从占位角色配置里补齐。
    public override string? PlaceholderCharacterId => "ironclad";

    // 如果你的人物不需要时间线小故事，加上这句。
    public override bool RequiresEpochAndTimeline => false;

    // 攻击和施法动画延迟，以对齐动画。静态占位资源不需要延迟。
    public override float AttackAnimDelay => 0f;
    public override float CastAnimDelay => 0f;

    // 起始卡组：4 打击 + 4 防御（战士版贴图/音效/数值），外加初始牌 剧情推进！和 打游戏！。
    // 注意：LocalStartingDeck 之后还会追加通过 [RegisterCharacterStarterCard] 注册的卡。
    protected override IEnumerable<CardModel> LocalStartingDeck =>
        Enumerable.Repeat<CardModel>(ModelDb.Card<STS2_MomoiStrike>(), 4)
            .Concat(Enumerable.Repeat<CardModel>(ModelDb.Card<STS2_MomoiDefend>(), 4))
            .Append(ModelDb.Card<PlotAdvance>())
            .Append(ModelDb.Card<PlayGames>());

    // 让 RitsuLib 把普通 Godot 场景转换成游戏需要的 NCreatureVisuals。
    // 自动转换人物场景，让你不需要手动挂脚本。复制即可。
    protected override NCreatureVisuals? TryCreateCreatureVisuals()
    {
        return RitsuGodotNodeFactories.CreateFromScenePath<NCreatureVisuals>(
            CharacterScenePath);
    }

    // 战斗动画状态机（非 Spine）：
    //   idle 循环
    //   attack1/2/3、cast1/2、taunt1 单次播放后回 idle
    //   hit 单次后回 idle；dead 终止；relaxed 循环
    // 关键：RitsuLib 的 NCreatureCombatAnimationInitialBootstrapPatch 只有在角色返回了状态机时，
    // 才会在 NCreature._Ready 主动播 idle。不重写这里，战斗开场只会显示场景默认的 idle.png（第 0 帧）。
    protected override ModAnimStateMachine? SetupCustomCombatAnimationStateMachine(
        Node visualsRoot, CharacterModel character)
    {
        Entry.Logger.Info($"[Visual] state machine: idle/low_hp + attack1/2/3 + cast1/2 + taunt1; " +
                          $"speeds a1={Attack1Speed} a2={Attack2Speed} a3={Attack3Speed} " +
                          $"c1={Cast1Speed} c2={Cast2Speed} t1={Taunt1Speed} h={HitSpeed} d={DeadSpeed}");

        var b = ModAnimStateMachineBuilder.Create();
        b.AddState("idle", true).AsInitial().Done();
        b.AddState("low_hp", true).Done();
        b.AddState("attack1").WithNext("idle").Done();
        b.AddState("attack2").WithNext("idle").Done();
        b.AddState("attack3").WithNext("idle").Done();
        b.AddState("cast1").WithNext("idle").Done();
        b.AddState("cast2").WithNext("idle").Done();
        b.AddState("taunt1").WithNext("idle").Done();
        b.AddState("hit").WithNext("idle").Done();
        b.AddState("dead").Done();
        b.AddState("relaxed", true).Done();
        b.AddBranch("relaxed", "Idle", "idle");

        b.AddAnyState("Idle", "idle");
        b.AddAnyState("LowHp", "low_hp");
        b.AddAnyState("Attack1", "attack1");
        b.AddAnyState("Attack2", "attack2");
        b.AddAnyState("Attack3", "attack3");
        b.AddAnyState("Cast1", "cast1");
        b.AddAnyState("Cast2", "cast2");
        b.AddAnyState("Taunt1", "taunt1");
        // 非卡牌来源（能力/遗物/宠物）的默认动作
        b.AddAnyState("Attack", "attack1");
        b.AddAnyState("Cast", "cast1");
        b.AddAnyState("PowerUp", "cast1");
        b.AddAnyState("Hit", "hit");
        b.AddAnyState("Dead", "dead");
        b.AddAnyState("Relaxed", "relaxed");

        return b.BuildForVisualsRoot(visualsRoot, character);
    }

    // 攻击建筑师的攻击特效列表。
    public override List<string> GetArchitectAttackVfx()
    {
        return
        [
            "vfx/vfx_attack_blunt",
            "vfx/vfx_heavy_blunt",
            "vfx/vfx_attack_slash",
            "vfx/vfx_bloody_impact",
            "vfx/vfx_rock_shatter"
        ];
    }
}