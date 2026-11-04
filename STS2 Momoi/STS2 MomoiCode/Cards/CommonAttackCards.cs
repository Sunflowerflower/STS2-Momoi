using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 翻滚射击：1 费攻击（普通）。获得 7 点格挡，造成 1 点伤害 3 次（升级：9 格挡、2 伤）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class RollAndShoot : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public RollAndShoot() : base(1, CardType.Attack, CardRarity.Common, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(1m),  // 升级 2
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new BlockVar(6m, ValueProp.Move)   // 升级 8
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);

        var target = cardPlay.Target;
        if (target != null)
        {
            await MomoiGunStyle.Apply(
                    DamageCmd.Attack(DynamicVars.CalculatedDamage)
                        .FromCard(this, cardPlay)
                        .Targeting(target)
                        .WithHitCount(3),
                    Owner.Creature)
                .Execute(choiceContext);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Block"].UpgradeValueBy(2);
        DynamicVars.CalculationBase.UpgradeValueBy(1);
    }
}

/// <summary>
/// 复盘：1 费技能（普通）。将消耗牌堆中的一张随机小游戏牌放入你的手牌（升级：放入升级过的）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class GameReview : ModCardTemplate
{
    public GameReview() : base(1, CardType.Skill, CardRarity.Common, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 消耗（升级后删去），只保留「消耗牌堆里的随机小游戏牌回手」这一个效果。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        if (player == null)
        {
            return;
        }

        var minigames = PileType.Exhaust.GetPile(player).Cards
            .Where(MinigameSupport.IsMinigameCard)
            .ToList();
        if (minigames.Count > 0)
        {
            var card = player.RunState.Rng.CombatCardSelection.NextItem(minigames);
            if (card != null)
            {
                if (IsUpgraded)
                {
                    CardCmd.Upgrade(card);
                }

                await CardPileCmd.Add(card, PileType.Hand, CardPilePosition.Random, this);
            }
        }
    }

    protected override void OnUpgrade()
    {
        // 升级：删去消耗（另外放入的那张牌是升级过的，见 OnPlay 的 IsUpgraded 分支）。
        RemoveKeyword(CardKeyword.Exhaust);
    }

    protected override void AfterDowngraded()
    {
        base.AfterDowngraded();
        AddKeyword(CardKeyword.Exhaust);
    }
}

/// <summary>
/// 独特点子：1 费攻击（普通）。造成 4 点伤害 2 次，将这张牌变化为一张随机小游戏牌（升级：6 伤、升级后的小游戏牌）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class UniqueIdea : ModCardTemplate
{
    public UniqueIdea() : base(1, CardType.Attack, CardRarity.Common, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(4m),  // 升级 6
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target != null)
        {
            await DamageCmd.Attack(DynamicVars.CalculatedDamage)
                .FromCard(this, cardPlay)
                .Targeting(target)
                .WithHitCount(2)
                .Execute(choiceContext);
        }
    }

    // 打出完成、进入弃牌堆后：替换为随机稀有牌（不用弹出式变化 UI，避免卡在屏幕中间）。
    public override async Task AfterCardChangedPiles(CardModel card, PileType oldPileType, AbstractModel? clonedBy)
    {
        if (card != this || oldPileType != PileType.Play || card.Pile?.Type != PileType.Discard)
        {
            return;
        }

        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        await CardPileCmd.RemoveFromCombat(this);

        // 变化为随机小游戏牌（升级：升级过的随机小游戏牌）。
        var replacement = MinigameSupport.CreateRandomMinigameCard(combatState, Owner, IsUpgraded);
        CombatStats.RecordMinigameObtained(replacement);
        await CardPileCmd.AddGeneratedCardToCombat(replacement, PileType.Discard, Owner);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(2);
    }
}



/// <summary>
/// 博览群游：1 费攻击（罕见）。本场战斗中每打出过一张小游戏牌，就造成 8 点伤害一次（升级：11 点）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class ExperienceCombo : ModCardTemplate
{
    public ExperienceCombo() : base(1, CardType.Attack, CardRarity.Uncommon, TargetType.RandomEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars
    {
        get
        {
            var hitsBase = new DynamicVar("HitsBase", 0m);
            var hitsExtra = new DynamicVar("HitsExtra", 1m);
            return
            [
                new CalculationBaseVar(5m),  // 升级 7
                new ExtraDamageVar(0m),
                new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
                hitsBase,
                hitsExtra,
                // 攻击次数 = 本场打出过的小游戏牌数（实时显示，参考猎人终结技）。
                new IndependentCalculatedVar("CalculatedHits", hitsBase, hitsExtra)
                    .WithMultiplier((_, _) => CombatStats.MinigamesPlayed)
            ];
        }
    }

    // 随机敌人：每一击各自随机挑目标（参考原版散射炮 FlakCannon 的 TargetingRandomOpponents）。
    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var hits = Convert.ToInt32(DynamicVars["CalculatedHits"]);
        if (hits > 0)
        {
            await MomoiGunStyle.Apply(
                    DamageCmd.Attack(DynamicVars.CalculatedDamage)
                        .FromCard(this, cardPlay)
                        .TargetingRandomOpponents(combatState)
                        .WithHitCount(hits),
                    Owner.Creature)
                .Execute(choiceContext);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(2);   // 5 -> 7
        // 升级不改耗能（升级前后都是 1）。
    }
}

/// <summary>
/// 结果好就没问题！：3 费攻击（稀有）。造成 45 点伤害，获得 15 点格挡；失去所有能量、丢弃所有手牌、
/// 清空活力与火力层数；给予自身 2 层虚弱与 2 层脆弱（升级：53 伤、16 格挡）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class AllsWellThatEndsWell : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public AllsWellThatEndsWell() : base(3, CardType.Attack, CardRarity.Rare, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(44m),  // 升级 50
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new BlockVar(16m, ValueProp.Move),   // 升级 19
        new EnergyVar("CostIncrease", 1)  // 下回合卡牌耗能增加（能量图标）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target != null)
        {
            await DamageCmd.Attack(DynamicVars.CalculatedDamage)
                .FromCard(this, cardPlay)
                .Targeting(target)
                .Execute(choiceContext);
        }

        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);

        // 所有卡牌在下回合耗能增加（可叠加），然后结束你的回合（参考亡灵契约师「预借时间」）。
        await PowerCmd.Apply<NoProblemPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        PlayerCmd.EndTurn(Owner, canBackOut: false);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(6);
        DynamicVars["Block"].UpgradeValueBy(3);
    }
}

/// <summary>
/// 来自邮箱的关爱：2 费技能（普通）。获得 12 点格挡，将一张下砸加入你的手牌，这张牌本回合可以免费打出（升级：15 格挡、下砸+）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class MailCare : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public MailCare() : base(2, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：下砸。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<CrushUnder>(IsUpgraded)
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new BlockVar(12m, ValueProp.Move)  // 升级 15
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);

        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var crush = combatState.CreateCard(ModelDb.Card<CrushUnder>(), Owner);
        if (IsUpgraded)
        {
            CardCmd.Upgrade(crush);
        }

        crush.SetToFreeThisTurn();
        await CardPileCmd.AddGeneratedCardToCombat(crush, PileType.Hand, Owner);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Block"].UpgradeValueBy(3);
    }
}

/// <summary>没问题……吗？（结果好就没问题！）：你的所有卡牌在下回合耗能增加（可叠加），
/// 结束你的回合时施加；持续到下回合结束（参考亡灵契约师「预借时间」BorrowedTimePower）。</summary>
[RegisterPower]
public sealed class NoProblemPower : ModPowerTemplate
{
    private bool _skipFirstTurnEnd;

    public override PowerType Type => PowerType.Debuff;

    // 可叠加：层数 = 增加的耗能。
    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/no_problem_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/no_problem_power.png");

    public override bool TryModifyEnergyCostInCombat(CardModel card, decimal originalCost, out decimal modifiedCost)
    {
        modifiedCost = originalCost;
        if (card.Owner.Creature != Owner)
        {
            return false;
        }

        modifiedCost = originalCost + Amount;
        return true;
    }

    public override async Task AfterSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (!participants.Contains(Owner))
        {
            return;
        }

        // 施加回合（当前回合）结束时跳过；下回合结束时移除。
        if (!_skipFirstTurnEnd)
        {
            _skipFirstTurnEnd = true;
            return;
        }

        await PowerCmd.Remove(this);
    }
}
