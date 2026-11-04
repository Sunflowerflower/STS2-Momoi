using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Hooks;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Patches;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 来自工程部的援助：1 费技能（普通）。获得 1 层火力；从 3 张牌中选择一张放入你的手牌。
/// 无法连续选择相同的选项（升级：2 火力、升级版选项）。选项：来自歌原/响/琴里的援助。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class EngineeringDeptAid : ModCardTemplate
{
    private static readonly Type[] Options = [typeof(MomoiSupportYoshimi), typeof(MomoiSupportHibiki), typeof(MomoiSupportKotori)];

    public EngineeringDeptAid() : base(1, CardType.Skill, CardRarity.Common, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：来自歌原/响/琴里的援助。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<MomoiSupportYoshimi>(IsUpgraded),
        HoverTipFactory.FromCard<MomoiSupportHibiki>(IsUpgraded),
        HoverTipFactory.FromCard<MomoiSupportKotori>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Firepower", 1)  // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature, DynamicVars["Firepower"].BaseValue, Owner.Creature, this);
        await AssistSupport.PickAssist(choiceContext, Owner, this, IsUpgraded, Options, typeof(EngineeringDeptAidPower));
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Firepower"].UpgradeValueBy(1);
    }
}

[RegisterPower]
public sealed class EngineeringDeptAidPower : AssistTrackerPowerBase
{
    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/engineering_dept_aid_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/engineering_dept_aid_power.png");
}

/// <summary>来自歌原的援助：1 费攻击（衍生）。获得 2 点格挡、1 层火力，对随机敌人造成 3 点伤害；
/// 接下来的 3 个回合结束时，重复此效果（升级：3 格挡、5 伤、4 回合）。消耗。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportYoshimi : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public MomoiSupportYoshimi() : base(1, CardType.Attack, CardRarity.Token, TargetType.RandomEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(3m, ValueProp.Move),  // 升级 4（BlockVar：卡面会实时显示计入敏捷/脆弱后的值）
        new CalculationBaseVar(4m),  // 升级 6
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new DynamicVar("Turns", 3)    // 升级 4
    ];

    /// <summary>卡面当前的格挡值（已计入敏捷等修正）——“雷酱”炮台支援的快照来源。</summary>
    public int FaceBlock => Math.Max(0, (int)DynamicVars.Block.PreviewValue);

    /// <summary>
    /// 卡面当前的伤害值（已计入力量/活力这类无目标修正，**不含目标易伤**）。
    /// 不能直接用 <c>CalculatedDamage.PreviewValue</c>：那是给玩家看的展示值，
    /// 而它由 <c>Hook.ModifyDamage</c> 带 **目标** 算出来 —— 如果卡面最后一次重绘时带着一个易伤目标，
    /// 它就已经乘过 1.5 了，而本 power 自己还会再补一次易伤 → 变成 1.5×1.5。
    /// 所以这里重算一遍：同一条管道，但 target 传 null（易伤/弱化这类需要目标的修正就不会介入）。
    /// </summary>
    public int FaceDamage
    {
        get
        {
            var owner = Owner;
            var combatState = owner?.Creature?.CombatState;
            var baseValue = DynamicVars.CalculatedDamage.Calculate(null);
            if (owner == null || combatState == null)
            {
                return Math.Max(0, (int)baseValue);
            }

            var modified = Hook.ModifyDamage(owner.RunState, combatState, null, owner.Creature, baseValue,
                ValueProp.Move, this, null, ModifyDamageHookType.All, CardPreviewMode.Normal, out _);
            return Math.Max(0, (int)modified);
        }
    }

    /// <summary>卡面当前的重复回合数。</summary>
    public int FaceTurns => DynamicVars["Turns"].IntValue;

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);
        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);

        var combatState = Owner.Creature.CombatState;
        if (combatState != null)
        {
            await DamageCmd.Attack(DynamicVars.CalculatedDamage)
                .FromCard(this, cardPlay)
                .TargetingRandomOpponents(combatState)
                .Execute(choiceContext);
        }

        // 叠层数 = 剩余重复回合数；具体数值由 AfterApplied 从本卡卡面快照。
        await PowerCmd.Apply<YoshimiRepeatPower>(choiceContext, Owner.Creature, FaceTurns, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.Block.UpgradeValueBy(1);
        DynamicVars.CalculationBase.UpgradeValueBy(2);
        DynamicVars["Turns"].UpgradeValueBy(1);
    }
}

/// <summary>
/// “雷酱”炮台支援：每张「来自歌原的援助」一个独立实例，叠层数 = 剩余重复回合数。
/// 数值在施加时从卡面快照（卡面值已计入敏捷/力量，但之后不再被力量/敏捷/虚弱/脆弱重复修正）。
/// 伤害仍会吃活力（加算，并在结算后扣除）和目标的易伤（×1.5）——这两项原版都以 IsPoweredAttack() 为门槛，
/// 所以这里把攻击标记为 Unpowered（跳过原版所有修正），再由本能力自己补上。
/// </summary>
[RegisterPower]
public sealed class YoshimiRepeatPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    // 多张「来自歌原的援助」各自独立存在。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    // 叠层数就是剩余回合数。
    public override PowerStackType StackType => PowerStackType.Counter;

    // 右下角显示剩余回合数（而不是默认的 Amount 语义重定义）。
    public override int DisplayAmount => Amount;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/yoshimi_repeat_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/yoshimi_repeat_power.png");

    private class Data
    {
        public int Block;
        public int Damage;
        public CardModel? SourceCard;
    }

    protected override object InitInternalData() => new Data();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Block", 0),
        new DynamicVar("Damage", 0)
    ];

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        var data = GetInternalData<Data>();
        // 快照来源必须是本卡自己的卡面值，而不是实际打在敌人身上造成的伤害。
        if (cardSource is MomoiSupportYoshimi yoshimi)
        {
            data.Block = yoshimi.FaceBlock;
            data.Damage = yoshimi.FaceDamage;
        }

        data.SourceCard = cardSource;
        DynamicVars["Block"].BaseValue = data.Block;
        DynamicVars["Damage"].BaseValue = data.Damage;
        return Task.CompletedTask;
    }

    public override async Task AfterSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var data = GetInternalData<Data>();

        // 格挡：Unpowered，不受敏捷/脆弱影响。
        if (data.Block > 0)
        {
            await CreatureCmd.GainBlock(Owner, new BlockVar(data.Block, ValueProp.Unpowered | ValueProp.Move), null);
        }

        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner, 1, Owner, null);

        var combatState = Owner.CombatState;
        if (combatState != null && data.Damage > 0 && data.SourceCard != null)
        {
            // 能力伤害走原版形状（同 Panache / Juggernaut）：直接 CreatureCmd.Damage + ValueProp.Unpowered，
            // 随机一个敌人。不吃力量/活力/虚弱/易伤，也不播攻击动画（所以也不需要再自己补活力/易伤）。
            var enemies = combatState.HittableEnemies;
            var target = enemies.Count > 0 ? Owner.Player?.RunState.Rng.CombatTargets.NextItem(enemies) : null;
            if (target != null)
            {
                await CreatureCmd.Damage(choiceContext, target, data.Damage, ValueProp.Unpowered,
                    Owner, data.SourceCard, null);
            }
        }

        // 结算完再扣剩余回合数，扣到 0 自动消失。
        await PowerCmd.TickDownDuration(this);
    }
}

/// <summary>来自响的援助：2 费攻击（衍生）。对所有敌人造成 14 点伤害；仅存活一名敌人时，将这张牌额外打出 2 次。
/// 消耗（升级：18 伤）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportHibiki : ModCardTemplate
{
    public MomoiSupportHibiki() : base(2, CardType.Attack, CardRarity.Token, TargetType.AllEnemies)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(14m),  // 升级 18
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

        var hits = combatState.HittableEnemies.Count == 1 ? 3 : 1;

        await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .TargetingAllOpponents(combatState)
            .WithHitCount(hits)
            .Execute(choiceContext);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(4);
    }
}

/// <summary>来自琴里的援助：1 费技能（衍生）。使所有友方单位获得 12 点格挡。消耗（升级：16）。</summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class MomoiSupportKotori : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public MomoiSupportKotori() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(12m, ValueProp.Move)  // 升级 16
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        foreach (var ally in combatState.Allies)
        {
            await CreatureCmd.GainBlock(ally, DynamicVars.Block, cardPlay);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Block"].UpgradeValueBy(4);
    }
}

/// <summary>支援牌公共逻辑：选择衍生牌（不可连续选择同一选项）。</summary>
public static class AssistSupport
{
    /// <summary>
    /// 从选项牌中选择一张加入手牌；记录上次选择（同源牌共享），避免连续选择相同选项。
    /// </summary>
    public static async Task PickAssist(PlayerChoiceContext choiceContext, Player owner, CardModel source,
        bool upgraded, Type[] options, Type trackerPowerType)
    {
        var combatState = owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var tracker = owner.Creature.GetPower(ModelDb.Get(trackerPowerType).Id);
        var lastChoice = tracker is AssistTrackerPowerBase assistTracker
            ? assistTracker.GetChoiceData().LastChoice
            : string.Empty;

        var available = options
            .Where(t => !string.Equals(((CardModel)ModelDb.Get(t)).Id.Entry, lastChoice, StringComparison.Ordinal))
            .ToList();
        if (available.Count == 0)
        {
            available = options.ToList();
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

        var picked = await CardSelectCmd.FromChooseACardScreen(choiceContext, cards, owner);
        if (picked != null)
        {
            // 记录本次选择（写回 tracker）。
            var power = owner.Creature.GetPower(ModelDb.Get(trackerPowerType).Id);
            if (power == null)
            {
                var trackerModel = ModelDb.Get(trackerPowerType) as PowerModel;
                if (trackerModel != null)
                {
                    await PowerCmd.Apply(choiceContext, trackerModel.ToMutable(),
                        owner.Creature, 1, owner.Creature, source);
                }
                power = owner.Creature.GetPower(ModelDb.Get(trackerPowerType).Id);
            }

            if (power is AssistTrackerPowerBase assistTracker2)
            {
                assistTracker2.GetChoiceData().SetLastChoice(picked.Id.Entry);
            }
            await CardPileCmd.AddGeneratedCardToCombat(picked, PileType.Hand, owner);
        }
    }
}

/// <summary>援助选择记录（挂在 tracker power 上）。</summary>
public class AssistChoiceData
{
    public string LastChoice { get; private set; } = string.Empty;

    public void SetLastChoice(string entry) => LastChoice = entry;
}

/// <summary>援助选择 tracker 基类：记录上次选择的选项（同源牌共享，战斗内有效）。</summary>
public abstract class AssistTrackerPowerBase : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;

    // 纯记录用，不给玩家看（原版 AmbergrisPower 同款做法）。
    protected override bool IsVisibleInternal => false;

    protected override object InitInternalData() => new AssistChoiceData();

    public AssistChoiceData GetChoiceData() => GetInternalData<AssistChoiceData>();
}
