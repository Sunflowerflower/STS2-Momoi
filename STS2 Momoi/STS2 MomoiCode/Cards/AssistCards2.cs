using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Commands.Builders;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Helpers;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.MonsterMoves.Intents;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using MegaCrit.Sts2.Core.Nodes.Vfx;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;
using STS2RitsuLib.Scaffolding.Content.Patches;

namespace STS2_Momoi.Cards;

/// <summary>
/// 来自真理部的协助：1 费技能（罕见）。抽 1 张牌；从 3 张牌中选择一张放入你的手牌；无法连续选择相同的选项。
/// 本局游戏中，3 张牌各选择一次后，这张牌将解锁新的选项（升级：抽 2、升级版选项）。
/// 选项：来自真纪/晴/小玉的协助；额外选项：来自千寻的协助。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class VeritasDeptAid : ModCardTemplate
{
    private static readonly Type[] Options = [typeof(MomoiSupportMaki), typeof(MomoiSupportHare), typeof(MomoiSupportKotama)];
    private static readonly Type[] ExtraOption = [typeof(MomoiSupportChihiro)];

    public VeritasDeptAid() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：来自真纪/晴/小玉的协助。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<MomoiSupportMaki>(IsUpgraded),
        HoverTipFactory.FromCard<MomoiSupportHare>(IsUpgraded),
        HoverTipFactory.FromCard<MomoiSupportKotama>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Cards", 1)  // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CardPileCmd.Draw(choiceContext, DynamicVars["Cards"].IntValue, Owner);

        var options = Options.ToList();
        // 解锁进度为整局游戏全局继承：3 个基础选项各选过至少一次后，永久解锁新选项。
        if (RunStats.VeritasPicked.Count >= Options.Length)
        {
            options.AddRange(ExtraOption);
        }

        await AssistSupport2.PickAssist(choiceContext, Owner, this, IsUpgraded, options,
            typeof(VeritasTrackerPower), RunStats.VeritasPicked);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Cards"].UpgradeValueBy(1);
    }
}

[RegisterPower]
public sealed class VeritasTrackerPower : AssistTrackerPowerBase2
{
    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/veritas_tracker_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/veritas_tracker_power.png");
}

/// <summary>来自真纪的协助：1 费攻击（衍生）。获得 1 点力量，造成 10 点伤害；将上一张打出的小游戏牌放入你的手牌。
/// 消耗（升级：2 力量、11 伤、升级后放入）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportMaki : ModCardTemplate
{
    public MomoiSupportMaki() : base(1, CardType.Attack, CardRarity.Token, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Strength", 1),   // 升级 2
        new CalculationBaseVar(10m),  // 升级 11
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<StrengthPower>(choiceContext, Owner.Creature, DynamicVars["Strength"].BaseValue, Owner.Creature, this);

        var target = cardPlay.Target;
        if (target != null)
        {
            await DamageCmd.Attack(DynamicVars.CalculatedDamage)
                .FromCard(this, cardPlay)
                .Targeting(target)
                .Execute(choiceContext);
        }

        var last = CombatStats.LastPlayedMinigame;
        if (last != null)
        {
            if (IsUpgraded)
            {
                CardCmd.Upgrade(last);
            }

            await CardPileCmd.Add(last, PileType.Hand, CardPilePosition.Random, this);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Strength"].UpgradeValueBy(1);
        DynamicVars.CalculationBase.UpgradeValueBy(1);
    }
}

/// <summary>来自晴的协助：3 费攻击（衍生）。对所有敌人造成 4 点伤害，将它们 1 回合内的意图改为眩晕。消耗（升级：6 伤）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportHare : ModCardTemplate
{
    public MomoiSupportHare() : base(3, CardType.Attack, CardRarity.Token, TargetType.AllEnemies)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(6m),  // 升级 9
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .TargetingAllOpponents(combatState)
            .Execute(choiceContext);

        foreach (var enemy in combatState.HittableEnemies)
        {
            await CreatureCmd.Stun(enemy);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(3);   // 6 -> 9
    }
}

/// <summary>来自小玉的协助：0 费技能（衍生）。使所有友方单位在本回合获得 2 点力量；
/// 选择最多 1 张牌，在本回合随机化其耗能（0～3）（升级：3 力量）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportKotama : ModCardTemplate
{
    public MomoiSupportKotama() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Strength", 3)  // 升级 4
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 友方单位 = 单人模式包含玩家角色与奥斯提；多人模式包含所有玩家。
        foreach (var ally in combatState.GetTeammatesOf(Owner.Creature))
        {
            if (ally != null && ally.IsAlive)
            {
                await PowerCmd.Apply<KotamaStrengthPower>(choiceContext, ally,
                    DynamicVars["Strength"].BaseValue, Owner.Creature, this);
            }
        }

        // 选择最多 1 张手牌，随机化耗能（可跳过）。
        var picked = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("card_selection", "TO_RANDOMIZE_COST"), 0, 1) { Cancelable = true, RequireManualConfirmation = true },
            null, this)).FirstOrDefault();
        if (picked != null)
        {
            var cost = Owner.RunState.Rng.CombatEnergyCosts.NextInt(4);
            picked.EnergyCost.SetThisTurnOrUntilPlayed(cost);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Strength"].UpgradeValueBy(1);
    }
}

/// <summary>小玉的临时力量：本回合获得力量（回合结束移除）。原版 TemporaryStrengthPower 是抽象基类不能直接使用。
/// 因为继承的是原版类，拿不到 ModPowerTemplate.AssetProfile，所以用 RitsuLib 的
/// IModPowerAssetOverrides 把图标路径补上（否则会去原版 power_atlas 找 sts2_momoi_power_kotama_strength_power 而落空）。</summary>
[RegisterPower]
public sealed class KotamaStrengthPower : TemporaryStrengthPower, IModPowerAssetOverrides
{
    // 原版临时力量逻辑：施加时静默给真实 StrengthPower；己方回合结束时移除临时能力并扣回等量力量。
    // 临时能力本身只是计数标记，真正生效的是底下那层真实力量（参考原版 CoordinatePower）。
    public override AbstractModel OriginModel => ModelDb.Card<MomoiSupportKotama>();

    public PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/kotama_strength_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/kotama_strength_power.png");

    public string? CustomIconPath => AssetProfile.IconPath;

    public string? CustomBigIconPath => AssetProfile.BigIconPath;
}

/// <summary>来自千寻的协助：2 费攻击（衍生）。造成 6 点伤害；若目标的意图包含强化或者守势，将其 1 回合内的意图改为眩晕。
/// 消耗（升级：8 伤）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportChihiro : ModCardTemplate
{
    public MomoiSupportChihiro() : base(2, CardType.Attack, CardRarity.Token, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(7m),  // 升级 10
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .Targeting(target)
            .Execute(choiceContext);

        var monster = target.Monster;
        if (monster != null && monster.NextMove.Intents.Any(i =>
                i.IntentType is IntentType.Buff or IntentType.Defend or IntentType.Debuff or IntentType.Heal))
        {
            await CreatureCmd.Stun(target);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(3);   // 7 -> 10
    }
}

/// <summary>
/// 来自C&C的援护：1 费技能（稀有）。获得 1 点活力；从 4 张牌中选择一张放入你的手牌；无法连续选择相同的选项。
/// 本局游戏中，4 张牌各选择一次后，这张牌将解锁新的选项（升级：2 活力、升级版选项）。
/// 选项：来自妮露/明日奈/花凛/茜的援护；额外选项：来自时的援护。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class CnCAid : ModCardTemplate
{
    private static readonly Type[] Options = [typeof(MomoiSupportNeru), typeof(MomoiSupportAsuna), typeof(MomoiSupportKarin), typeof(MomoiSupportAkira)];
    private static readonly Type[] ExtraOption = [typeof(MomoiSupportToki)];

    public CnCAid() : base(1, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：来自妮露/明日奈/花凛/茜的援护。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<MomoiSupportNeru>(IsUpgraded),
        HoverTipFactory.FromCard<MomoiSupportAsuna>(IsUpgraded),
        HoverTipFactory.FromCard<MomoiSupportKarin>(IsUpgraded),
        HoverTipFactory.FromCard<MomoiSupportAkira>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Vigor", 1)  // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, DynamicVars["Vigor"].BaseValue, Owner.Creature, this);

        var options = Options.ToList();
        // 解锁进度为整局游戏全局继承。
        if (RunStats.CnCPicked.Count >= Options.Length)
        {
            options.AddRange(ExtraOption);
        }

        await AssistSupport2.PickAssist(choiceContext, Owner, this, IsUpgraded, options,
            typeof(CnCTrackerPower), RunStats.CnCPicked);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Vigor"].UpgradeValueBy(1);
    }
}

[RegisterPower]
public sealed class CnCTrackerPower : AssistTrackerPowerBase2
{
    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/cnc_tracker_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/cnc_tracker_power.png");
}

/// <summary>来自妮露的援护：1 费攻击（衍生）。造成 5 点伤害 2 次；消耗所有火力，每消耗 1 层火力，
/// 就将此牌额外打出一次。消耗（升级：7 点伤害 2 次）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportNeru : ModCardTemplate
{
    public MomoiSupportNeru() : base(1, CardType.Attack, CardRarity.Token, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(5m),  // 升级 7
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new DynamicVar("Hits", 2)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .Targeting(target)
            .WithHitCount(DynamicVars["Hits"].IntValue)
            .Execute(choiceContext);

        // 消耗所有火力：每消耗 1 层，就将此牌额外打出一次（火力已清空，重复打出不会再次追加）。
        var firepower = Owner.Creature.GetPower<FirepowerPower>();
        var stacks = (int)(firepower?.Amount ?? 0);
        if (stacks <= 0 || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature, -stacks, Owner.Creature, this);

        var player = Owner.Creature.Player;
        if (player == null)
        {
            return;
        }

        for (int i = 0; i < stacks; i++)
        {
            if (CombatManager.Instance.IsOverOrEnding)
            {
                break;
            }

            var dupe = CreateDupe(player);
            // 不要复用 OnPlay 开头抓的 target：前几次重复很可能已经把它打死了，
            // 而 AutoPlay 对非 null 目标不做存活检查 → 后续重复会静默空放（卡被消耗、无伤害）。
            // 传 null 让 AutoPlay 每次自己随机挑一个还活着的敌人。
            await CardCmd.AutoPlay(choiceContext, dupe, target is { IsAlive: true } ? target : null);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(2);
    }
}



/// <summary>来自明日奈的援护：1 费技能（衍生）。获得 4 点活力、1 点敏捷；本回合受到的所有伤害降低 25%。
/// 消耗（升级：6 活力、2 敏捷、40%）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportAsuna : ModCardTemplate
{
    public MomoiSupportAsuna() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Vigor", 4),   // 升级 6
        new DynamicVar("Dex", 1)      // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, DynamicVars["Vigor"].BaseValue, Owner.Creature, this);
        await PowerCmd.Apply<DexterityPower>(choiceContext, Owner.Creature, DynamicVars["Dex"].BaseValue, Owner.Creature, this);

        // 幸运儿的祝福：可叠加（叠层数 = 持续回合数）；减伤百分比不叠加，
        // 升级过的 40% 覆盖升级前的 25%，反之不覆盖（规则在 AsunaGuardPower.ApplySource 里）。
        await PowerCmd.Apply<AsunaGuardPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Vigor"].UpgradeValueBy(2);
        DynamicVars["Dex"].UpgradeValueBy(1);
    }
}

/// <summary>明日奈援护的减伤：叠层数 = 剩余回合数；减伤百分比不叠加（升级 40% 覆盖 25%，反之不覆盖）。</summary>
[RegisterPower]
public sealed class AsunaGuardPower : ModPowerTemplate
{
    private class Data
    {
        public decimal ReductionPct = 25m;  // 升级 40
        public bool Upgraded;
    }

    /// <summary>该实例是否来自升级后的牌（升级版覆盖升级前）。</summary>
    public bool IsUpgradedVersion => GetInternalData<Data>().Upgraded;

    public override PowerType Type => PowerType.Buff;

    // 可叠加：叠层数 = 剩余回合数（右下角计数器直接显示 Amount）。
    public override PowerStackType StackType => PowerStackType.Counter;

    // 右下角显示剩余回合数。
    public override int DisplayAmount => Amount;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/asuna_guard_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/asuna_guard_power.png");

    protected override object InitInternalData() => new Data();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("ReductionPct", 25)  // 升级 40（显示用百分数）
    ];

    // 减伤百分比只在“升级版”或“当前还没有升级版”时更新：
    // 升级过的 40% 覆盖升级前的 25%；反之 25% 不能覆盖 40%。
    private void ApplySource(CardModel? cardSource)
    {
        var data = GetInternalData<Data>();
        var upgraded = cardSource?.IsUpgraded == true;
        if (upgraded || !data.Upgraded)
        {
            data.Upgraded = upgraded;
            data.ReductionPct = upgraded ? 40m : 25m;
        }

        DynamicVars["ReductionPct"].BaseValue = data.ReductionPct;
    }

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        ApplySource(cardSource);
        return Task.CompletedTask;
    }

    // 叠加时（再打一张）也会走这里。
    public override Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power == this && amount > 0)
        {
            ApplySource(cardSource);
        }

        return Task.CompletedTask;
    }

    /// <summary>本回合受到的所有伤害降低 25%/40%（最终伤害倍数）；百分比取当前持有的最高档。</summary>
    public override decimal ModifyDamageMultiplicative(Creature? target, decimal amount, ValueProp props,
        Creature? dealer, CardModel? cardSource, CardPlay? cardPlay)
    {
        if (target != Owner)
        {
            return 1m;
        }

        return 1m - GetInternalData<Data>().ReductionPct / 100m;
    }

    // 效果持续到「你的下回合开始前」：己方回合**开始**时扣持续时间，归零自动消失（TickDownDuration）。
    // 所以打出当回合 + 之后的敌方回合都还在，到下一次自己的回合开始时才失效。
    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants,
        ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        await PowerCmd.TickDownDuration(this);
    }
}

/// <summary>
/// 来自花凛的援护：2 费攻击（衍生·支援牌）。造成 36 点伤害；对 Boss 造成的伤害增加 50%。消耗。
/// 升级：44 伤、+75%。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportKarin : ModCardTemplate
{
    public MomoiSupportKarin() : base(2, CardType.Attack, CardRarity.Token, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    // 支援牌。
    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.SupportTag };

    // 衍生牌预览：易伤（Boss 增伤那段的说明用）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromKeyword(CardKeyword.Exhaust)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(32m),  // 升级 40
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new DynamicVar("BossPct", 50) // 升级 75（显示用百分数）
    ];

    /// <summary>
    /// 本场战斗是否为 Boss 战。
    /// 注意：游戏里**没有**“Boss”这个怪物标记（搜 IsBoss / IsElite 都没结果），
    /// 只能用房间层级（`RunState.CurrentRoom.RoomType`，原版 Pantograph 就是这么写的）。
    /// </summary>
    private bool InBossRoom()
        => Owner.RunState.CurrentRoom?.RoomType == MegaCrit.Sts2.Core.Rooms.RoomType.Boss;

    /// <summary>
    /// 对 Boss 造成的伤害增加 50%（升级 75%）。
    /// 同族小队那种体面会把“爪牙”也放进 Boss 房间，但爪牙不属于 Boss，
    /// 所以再加一条 <c>target.IsPrimaryEnemy</c>（爪牙挂的是 MinionPower，IsPrimaryEnemy 为 false）→ 挡住爪牙。
    /// 像帝皇蟹这种多部位 Boss（Crusher / Rocket 都没挂 MinionPower）两个部位都是 primary enemy，照常吃增伤，不需要白名单。
    /// </summary>
    public override decimal ModifyDamageMultiplicative(Creature? target, decimal amount, ValueProp props,
        Creature? dealer, CardModel? cardSource, CardPlay? cardPlay)
    {
        if (cardSource != this || target == null || !InBossRoom() || !target.IsPrimaryEnemy)
        {
            return 1m;
        }

        return 1m + DynamicVars["BossPct"].BaseValue / 100m;
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .Targeting(target)
            .Execute(choiceContext);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(8);   // 32 -> 40
        DynamicVars["BossPct"].UpgradeValueBy(25);       // 50 -> 75
    }
}

/// <summary>来自茜的援护：1 费攻击（衍生）。对所有敌人造成 10 点伤害，给予所有敌人 1 层虚弱。消耗（升级：11 伤、2 虚弱）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportAkira : ModCardTemplate
{
    public MomoiSupportAkira() : base(1, CardType.Attack, CardRarity.Token, TargetType.AllEnemies)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(12m),  // 升级 15
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new DynamicVar("Weak", 2)     // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .TargetingAllOpponents(combatState)
            .Execute(choiceContext);

        foreach (var enemy in combatState.HittableEnemies)
        {
            await PowerCmd.Apply<WeakPower>(choiceContext, enemy, DynamicVars["Weak"].BaseValue, Owner.Creature, this);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(3);   // 12 -> 15
        DynamicVars["Weak"].UpgradeValueBy(1);
    }
}

/// <summary>来自时的援护：1 费技能（衍生）。获得 1 点活力、3 层火力；将 3 张系统：阿比舒分别放入你的手牌、弃牌堆、抽牌堆。
/// 消耗（升级：2 活力、4 火力、阿比舒+）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportToki : ModCardTemplate
{
    public MomoiSupportToki() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    // 衍生牌预览：系统：阿比舒（升级版预览升级后的衍生牌）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<SystemAbishu>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Vigor", 1),     // 升级 2
        new DynamicVar("Firepower", 2)  // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, DynamicVars["Vigor"].BaseValue, Owner.Creature, this);
        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature, DynamicVars["Firepower"].BaseValue, Owner.Creature, this);

        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        foreach (var pile in new[] { PileType.Hand, PileType.Discard, PileType.Draw })
        {
            var abishu = combatState.CreateCard(ModelDb.Card<SystemAbishu>(), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(abishu);
            }

            await CardPileCmd.AddGeneratedCardToCombat(abishu, pile, Owner);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Vigor"].UpgradeValueBy(1);
        DynamicVars["Firepower"].UpgradeValueBy(1);
    }
}

/// <summary>系统：阿比舒：1 费攻击（衍生）。对所有敌人造成 1 点伤害 3 次；最后一次攻击造成 4 倍伤害；
/// 使所有系统：阿比舒在本场战斗中造成的伤害+1。消耗（升级：2 伤）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class SystemAbishu : ModCardTemplate
{
    /// <summary>累计从「其它阿比舒被打出」中获得的加伤（降级时要补回 BaseValue）。</summary>
    private decimal _extraDamageFromAbishuPlays;

    /// <summary>只在最后一段（4 倍）伤害期间置真，用来把 ×4 限定在那一段上。</summary>
    private bool _finalHit;

    private decimal ExtraDamageFromAbishuPlays
    {
        get => _extraDamageFromAbishuPlays;
        set
        {
            AssertMutable();
            _extraDamageFromAbishuPlays = value;
        }
    }

    public SystemAbishu() : base(1, CardType.Attack, CardRarity.Token, TargetType.AllEnemies)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    // 用原版爪击 / 撕咬的写法：加伤直接累加到 Damage.BaseValue 上，
    // 这样卡面 {Damage:diff()} 与真正打出的数值天然是同一个数。
    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DamageVar(1m, ValueProp.Move),  // 升级 2
        new DynamicVar("Growth", 1m)        // 每打出一次后续阿比舒 +1（不随升级变化）
    ];

    /// <summary>
    /// 最后一段的 ×4 用**乘法修正**而不是把面板数值乘 4（参考「来自勇者的加护」的伤害翻倍）：
    ///   * 力量 / 活力 / 同类型阿比舒累积的加伤都会一起被 ×4（力量为负也会被 ×4）；
    ///   * 易伤、脆弱这类需要目标的修正各自只乘一次 —— 如果把 4 提前乘进面板，
    ///     面板再走一遍管道就会变成「吃好几次易伤」；
    ///   * 虚弱按原版就是最终伤害 -25%，和这里的 ×4 各自乘一次
    ///     （= 翻倍的是不吃虚弱的那份伤害，然后再吃一次虚弱）。
    /// </summary>
    public override decimal ModifyDamageMultiplicative(Creature? target, decimal amount, ValueProp props,
        Creature? dealer, CardModel? cardSource, CardPlay? cardPlay)
        => cardSource == this && _finalHit ? 4m : 1m;

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var targets = combatState.HittableEnemies.ToList();
        if (targets.Count == 0)
        {
            return;
        }

        var baseDamage = DynamicVars.Damage.BaseValue;

        // 整张牌算「一次攻击」：BeforeAttack / AfterAttack 各只跑一次。
        // （不用它的话每一段都会各跑一遍 → 活力会被消耗两次，而不是被最后一段的 4 倍放大。）
        await using var attackContext = await AttackCommand.CreateContextAsync(combatState, choiceContext, cardPlay);

        // 第 1 段：基础伤害 2 次。
        // ⚠ CreatureCmd.Damage 每次只结算**一次**伤害（它不是 AttackCommand 的 WithHitCount），
        //   所以 2 次要调两次 —— 只调一次就会变成“只有 2 段”而不是卡面写的 3 次。
        for (int i = 0; i < 2; i++)
        {
            attackContext.AddHit(await CreatureCmd.Damage(choiceContext, targets, baseDamage, ValueProp.Move,
                Owner.Creature, this, cardPlay));
        }

        // 第 2 段：4 倍伤害 1 次，只给这一段加超能光束特效。
        await PlayHyperbeamVfx(combatState);
        _finalHit = true;
        try
        {
            attackContext.AddHit(await CreatureCmd.Damage(choiceContext, targets, baseDamage, ValueProp.Move,
                Owner.Creature, this, cardPlay));
        }
        finally
        {
            _finalHit = false;
        }

        // 本场战斗里所有「系统：阿比舒」一起变强（按 C# 类型取，复制品/升级版/其它来源都命中）。
        var owner = Owner;
        if (owner?.PlayerCombatState == null)
        {
            return;
        }

        var increase = DynamicVars["Growth"].BaseValue;
        foreach (var card in owner.PlayerCombatState.AllCards.OfType<SystemAbishu>().ToList())
        {
            card.BuffFromAbishuPlay(increase);
        }
    }

    /// <summary>原版超能光束的攻击特效（只给最后一段用）。</summary>
    private async Task PlayHyperbeamVfx(ICombatState combatState)
    {
        var enemies = combatState.Enemies.Where(e => e.IsAlive).ToList();
        if (enemies.Count == 0)
        {
            return;
        }

        var beam = NHyperbeamVfx.Create(Owner.Creature, enemies.Last());
        if (beam != null)
        {
            NCombatRoom.Instance?.CombatVfxContainer.AddChildSafely(beam);
            await Cmd.Wait(0.5f);
        }

        foreach (var enemy in enemies)
        {
            var impact = NHyperbeamImpactVfx.Create(Owner.Creature, enemy);
            if (impact != null)
            {
                NCombatRoom.Instance?.CombatVfxContainer.AddChildSafely(impact);
            }
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.Damage.UpgradeValueBy(1m);        // 1 -> 2
    }

    // 降级 / 移除加成后要把已累计的加伤补回来（原版爪击同款）。
    protected override void AfterDowngraded()
    {
        base.AfterDowngraded();
        DynamicVars.Damage.BaseValue += ExtraDamageFromAbishuPlays;
    }

    private void BuffFromAbishuPlay(decimal extraDamage)
    {
        DynamicVars.Damage.BaseValue += extraDamage;
        ExtraDamageFromAbishuPlays += extraDamage;
    }
}

/// <summary>援助选择支持（真理部 / C&C 共用）：记录已选过的选项（解锁进度）。</summary>
public static class AssistSupport2
{
    public static async Task PickAssist(PlayerChoiceContext choiceContext, Player owner, CardModel source,
        bool upgraded, List<Type> options, Type trackerPowerType, HashSet<string>? runPicked = null)
    {
        var combatState = owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var tracker = owner.Creature.GetPower(ModelDb.Get(trackerPowerType).Id) as AssistTrackerPowerBase2;

        // 排除上次选项（同源牌共享）。
        var lastChoice = tracker?.GetChoiceData().LastChoice ?? string.Empty;
        var available = options
            .Where(t => !string.Equals(((CardModel)ModelDb.Get(t)).Id.Entry, lastChoice, StringComparison.Ordinal))
            .ToList();
        if (available.Count == 0)
        {
            available = options;
        }

        var cards = available
            .Select(t => combatState.CreateCard((CardModel)ModelDb.Get(t), owner))
            .ToList();
        foreach (var c in cards)
        {
            if (upgraded)
            {
                CardCmd.Upgrade(c);
            }
        }

        // C&C 解锁后最多 4 个选项：用网格选择（FromChooseACardScreen 最多 3 张）。
        var picked = (await CardSelectCmd.FromSimpleGrid(choiceContext, cards, owner,
            new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 1, 1))).FirstOrDefault();
        if (picked != null)
        {
            // 首次选择时 tracker 不存在：先挂上记录能力，否则「无法连续选择相同选项」失效。
            if (tracker == null)
            {
                var trackerModel = ModelDb.Get(trackerPowerType) as PowerModel;
                if (trackerModel != null)
                {
                    await PowerCmd.Apply(choiceContext, trackerModel.ToMutable(),
                        owner.Creature, 1, owner.Creature, source);
                }

                tracker = owner.Creature.GetPower(ModelDb.Get(trackerPowerType).Id) as AssistTrackerPowerBase2;
            }

            tracker?.GetChoiceData().RecordChoice(picked.Id.Entry);
            runPicked?.Add(picked.Id.Entry);
            CombatStats.RecordMinigameObtained(picked);
            await CardPileCmd.AddGeneratedCardToCombat(picked, PileType.Hand, owner);
        }
    }
}

/// <summary>援助选择 tracker 基类（真理部 / C&C）：记录上次选择与全部已选选项。</summary>
public abstract class AssistTrackerPowerBase2 : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;

    // 纯记录用，不给玩家看（原版 AmbergrisPower 同款做法）。
    protected override bool IsVisibleInternal => false;

    protected override object InitInternalData() => new AssistChoiceData2();

    public AssistChoiceData2 GetChoiceData() => GetInternalData<AssistChoiceData2>();
}

public class AssistChoiceData2
{
    public string LastChoice { get; private set; } = string.Empty;

    public HashSet<string> PickedNames { get; } = new();

    public void RecordChoice(string entry)
    {
        LastChoice = entry;
        PickedNames.Add(entry);
    }
}
