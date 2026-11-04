using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.Nodes.Cards;
using MegaCrit.Sts2.Core.Nodes.CommonUi;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 贪吃蛇：0 费技能（衍生·小游戏）。将一张疯狂进食、一张蛇咬、一张火蛇怒咬放入你的手牌；
/// 每当你打出一张牌时，随机化这三张牌的耗能（0～3）。消耗（升级：升级版）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class SnakeGame : ModCardTemplate
{
    public SnakeGame() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：疯狂进食、蛇咬、火蛇怒咬。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<Maul>(IsUpgraded),
        HoverTipFactory.FromCard<Snakebite>(IsUpgraded),
        HoverTipFactory.FromCard<FireSerpentBite>(IsUpgraded)
    ];

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var types = new[] { typeof(Maul), typeof(Snakebite), typeof(FireSerpentBite) };
        var created = new List<CardModel>();
        foreach (var type in types)
        {
            var card = combatState.CreateCard((CardModel)ModelDb.Get(type), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(card);
            }

            created.Add(card);
            await CardPileCmd.AddGeneratedCardToCombat(card, PileType.Hand, Owner);
        }

        // 升级前后是两个不同的 power：各自只管自己产生的那三张牌。
        SnakeGamePowerBase? power = IsUpgraded
            ? await PowerCmd.Apply<SnakeGameUpgradedPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this)
            : await PowerCmd.Apply<SnakeGamePower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        power?.Track(created);
    }

    protected override void OnUpgrade()
    {
    }
}

/// <summary>
/// 贪吃蛇（未升级）：每当你打出一张牌时，随机化你放出去的那三张牌（撕咬、蛇咬、火蛇怒咬）的耗能。
/// 不叠加：每次打出都是独立实例，每个实例只管自己产生的那三张牌。
/// </summary>
[RegisterPower]
public sealed class SnakeGamePower : SnakeGamePowerBase
{
    protected override bool CardsAreUpgraded => false;
}

/// <summary>
/// 贪吃蛇（升级）：同上，管的是升级版的那三张（撕咬+、蛇咬+、火蛇怒咬+）。
/// </summary>
[RegisterPower]
public sealed class SnakeGameUpgradedPower : SnakeGamePowerBase
{
    protected override bool CardsAreUpgraded => true;
}

/// <summary>贪吃蛇的公共逻辑。</summary>
public abstract class SnakeGamePowerBase : ModPowerTemplate
{
    /// <summary>本实例管的是不是升级版的那三张牌。</summary>
    protected abstract bool CardsAreUpgraded { get; }

    public override PowerType Type => PowerType.Buff;

    // 不叠加：每次打出都是独立实例。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/snake_game_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/snake_game_power.png");

    // 描述里显示实际卡名（升级版会带 +）。
    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new StringVar("MaulName"),
        new StringVar("SnakeName"),
        new StringVar("FireName")
    ];

    private class Data
    {
        public readonly List<CardModel> Owned = new();
    }

    protected override object InitInternalData() => new Data();

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        var plus = CardsAreUpgraded ? "+" : "";
        ((StringVar)DynamicVars["MaulName"]).StringValue = ModelDb.Card<Maul>().Title + plus;
        ((StringVar)DynamicVars["SnakeName"]).StringValue = ModelDb.Card<Snakebite>().Title + plus;
        ((StringVar)DynamicVars["FireName"]).StringValue = ModelDb.Card<FireSerpentBite>().Title + plus;
        return Task.CompletedTask;
    }

    /// <summary>由卡在生成那三张牌之后登记：本实例从此只管这三张。</summary>
    public void Track(IEnumerable<CardModel> cards) => GetInternalData<Data>().Owned.AddRange(cards);

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var player = Owner.Player;
        if (player == null)
        {
            return;
        }

        var hand = PileType.Hand.GetPile(player);

        // 只随机化「自己产生、且还在手牌里」的那三张（其他贪吃蛇放的牌不归本实例管）。
        foreach (var card in GetInternalData<Data>().Owned)
        {
            if (card.Pile != hand)
            {
                continue;
            }

            card.EnergyCost.SetThisTurnOrUntilPlayed(player.RunState.Rng.CombatEnergyCosts.NextInt(4));
            NCard.FindOnTable(card)?.PlayRandomizeCostAnim();
        }
    }
}

/// <summary>
/// 愤怒的小鸟：0 费技能（衍生·小游戏）。将一张愤怒和一张异鸟扑击放入你的手牌。消耗（升级：升级版）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class AngryBirds : ModCardTemplate
{
    public AngryBirds() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：愤怒、异鸟扑击。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<Anger>(IsUpgraded),
        HoverTipFactory.FromCard<ByrdSwoop>(IsUpgraded)
    ];

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        foreach (var type in new[] { typeof(Anger), typeof(ByrdSwoop) })
        {
            var card = combatState.CreateCard((CardModel)ModelDb.Get(type), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(card);
            }

            await CardPileCmd.AddGeneratedCardToCombat(card, PileType.Hand, Owner);
        }
    }

    protected override void OnUpgrade()
    {
    }
}

/// <summary>
/// 扫雷：0 费技能（衍生·小游戏）。当你下 1 次抽到炸弹时，直接打出这张牌；将一张炸弹加入你的抽牌堆（顶部）；抽 1 张牌。
/// 消耗（升级：炸弹+、抽 2）。触发效果每次获得叠加 1 次次数。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class Minesweeper : ModCardTemplate
{
    public Minesweeper() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：炸弹。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<TheBomb>(IsUpgraded)
    ];

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Cards", 1)  // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 效果顺序：先挂上「下次抽到炸弹直接打出」（可叠加次数），再把炸弹加入抽牌堆顶部，最后抽牌。
        await PowerCmd.Apply<MinesweeperPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);

        var bomb = combatState.CreateCard(ModelDb.Card<TheBomb>(), Owner);
        if (IsUpgraded)
        {
            CardCmd.Upgrade(bomb);
        }

        // 洗入抽牌堆的随机位置（与卡面「加入抽牌堆」一致；参考原版守墓人 GraveWarden 的 CardPilePosition.Random）。
        await CardPileCmd.AddGeneratedCardToCombat(bomb, PileType.Draw, Owner, CardPilePosition.Random);
        await CardPileCmd.Draw(choiceContext, DynamicVars["Cards"].BaseValue, Owner);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Cards"].UpgradeValueBy(1);
    }
}

[RegisterPower]
public sealed class MinesweeperPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;

    // 右下角显示的就是「还剩几次」（= Amount）；叠加会叠加这个次数。
    public override int DisplayAmount => Amount;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/minesweeper_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/minesweeper_power.png");

    // 每层 = 1 次「抽到炸弹直接打出」：触发一次减一层，归零移除；重复获得叠加次数。
    public override async Task AfterCardDrawn(PlayerChoiceContext choiceContext, CardModel card, bool fromHandDraw)
    {
        if (card is not TheBomb || card.Owner.Creature != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        await Cmd.Wait(0.25f);
        await CardCmd.AutoPlay(choiceContext, card, null);
        await PowerCmd.Decrement(this);
    }
}

/// <summary>
/// 绝地求生：0 费技能（衍生·小游戏）。抽 4 张牌，获得 3c；
/// 你的手牌中每有一张牌，此牌的数值就降低 1 点。消耗（升级：抽 5、4c）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class BattleRoyale : ModCardTemplate
{
    public BattleRoyale() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(0m),
        new CalculationExtraVar(1m),
        // 主行显示的是**最大值**（抽 4/5 张、获得 3/4 能量）——
        // 图鉴里没有战斗状态，CalculatedVar 会算成 0，所以不能拿它当主行显示。
        new DynamicVar("Cards", 4),     // 升级 5
        new EnergyVar("Energy", 3),     // 升级 4
        // 括号里显示实时值：抽牌数 = max(0, 4 - 其它手牌数)（升级 5），
        // 卡在手牌中时不把自己算进去，与打出时一致。
        new CalculatedVar("CalculatedCards").WithMultiplier((card, _) =>
            Math.Max(0, (card.IsUpgraded ? 5 : 4) - (PileType.Hand.GetPile(card.Owner).Cards.Count - (card.Pile?.Type == PileType.Hand ? 1 : 0)))),
        // 能量 = max(0, 3 - 其它手牌数)（升级 4），实时显示。
        new CalculatedVar("CalculatedEnergy").WithMultiplier((card, _) =>
            Math.Max(0, (card.IsUpgraded ? 4 : 3) - (PileType.Hand.GetPile(card.Owner).Cards.Count - (card.Pile?.Type == PileType.Hand ? 1 : 0))))
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 同一时刻的手牌快照：抽牌数与能量都按「其它手牌」数计算（打出时卡不在手牌中，天然一致）。
        var otherCount = PileType.Hand.GetPile(Owner).Cards.Count;
        var drawCount = Math.Max(0, (IsUpgraded ? 5 : 4) - otherCount);
        var energy = Math.Max(0, (IsUpgraded ? 4 : 3) - otherCount);

        if (drawCount > 0)
        {
            await CardPileCmd.Draw(choiceContext, drawCount, Owner);
        }

        if (energy > 0)
        {
            await PlayerCmd.GainEnergy(energy, Owner);
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Cards"].UpgradeValueBy(1);
        DynamicVars["Energy"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 跑酷！：0 费技能（衍生·小游戏）。从 5 张随机特定卡牌中选择一张放入你的手牌，这张牌在本回合可以被免费打出；
/// 回合开始时，重复此效果，直至你受到伤害或失去生命。消耗（升级：本场战斗免费 + 升级版）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class Parkour : ModCardTemplate
{
    private static readonly Type[] Pool =
    [
        typeof(Stomp), typeof(Stampede), typeof(FlickFlack), typeof(Backflip), typeof(Acrobatics),
        typeof(DodgeAndRoll), typeof(Dash), typeof(Blur), typeof(Speedster), typeof(ShadowStep),
        typeof(Footwork), typeof(CrushUnder), typeof(CrashLanding), typeof(Turbo), typeof(BoostAway), typeof(Leap)
    ];

    public Parkour() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    // 侧栏：说明各职业会出现什么特定牌。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_PARKOUR.sidebar"))
    ];

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    // 一次性效果（消耗）：选一张特定牌入手；升级版选升级牌且本场战斗免费。
    // 原先还挂了一个「回合开始时重复」的 power，已按需求整体删除。
    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PickOne(choiceContext, IsUpgraded, IsUpgraded);
    }

    public async Task PickOne(PlayerChoiceContext choiceContext, bool upgraded, bool freeThisCombat)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 随机 5 张不同卡牌中选择一张。
        var options = new List<CardModel>();
        var used = new HashSet<string>();
        while (options.Count < 5 && used.Count < Pool.Length)
        {
            var type = Owner.RunState.Rng.CombatCardSelection.NextItem(Pool) ?? Pool[0];
            if (used.Add(((CardModel)ModelDb.Get(type)).Id.Entry))
            {
                var card = combatState.CreateCard((CardModel)ModelDb.Get(type), Owner);
                if (upgraded)
                {
                    CardCmd.Upgrade(card);
                }

                options.Add(card);
            }
        }

        // 「最多一张」：MinSelect = 0 → 可以直接确认跳过（不选）。Cancelable 让 ESC 也能取消。
        var picked = (await CardSelectCmd.FromSimpleGrid(choiceContext, options, Owner,
            new CardSelectorPrefs(new LocString("card_selection", "STS2_MOMOI_PARKOUR_HEADER"), 0, 1)
            {
                Cancelable = true
            })).FirstOrDefault();
        if (picked != null)
        {
            // 升级：本场战斗免费；未升级：本回合免费。
            if (freeThisCombat)
            {
                picked.SetToFreeThisCombat();
            }
            else
            {
                picked.SetToFreeThisTurn();
            }

            await CardPileCmd.AddGeneratedCardToCombat(picked, PileType.Hand, Owner);
        }
    }

    protected override void OnUpgrade()
    {
    }
}


/// <summary>
/// 打灰机！：0 费能力（衍生·小游戏）。获得 3 点格挡；将 1 张燃料放入你的手牌；抽 1 张牌；
/// 当任何生物死亡时，重复此效果（升级：5 格挡、燃料+）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class Shmup : ModCardTemplate
{
    // 本卡会给格挡：Nimble（灵巧）附魔靠这个标志筛选目标（原版也用它自动挂「格挡」侧栏）。
    public override bool GainsBlock => true;

    public Shmup() : base(0, CardType.Power, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：燃料。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<Fuel>(IsUpgraded)
    ];

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        // BlockVar：卡面会实时显示计入敏捷/脆弱后的值（与获得格挡时用同一管道）。
        new BlockVar(6m, ValueProp.Move),  // 升级 8
        new CardsVar(1)                     // 抽牌数，升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);

        var combatState = Owner.Creature.CombatState;
        if (combatState != null)
        {
            var fuel = combatState.CreateCard(ModelDb.Card<Fuel>(), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(fuel);
            }

            await CardPileCmd.AddGeneratedCardToCombat(fuel, PileType.Hand, Owner);
        }

        await CardPileCmd.Draw(choiceContext, DynamicVars.Cards.IntValue, Owner);
        await PowerCmd.Apply<ShmupPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.Block.UpgradeValueBy(2);   // 6 -> 8
        DynamicVars.Cards.UpgradeValueBy(1);   // 1 -> 2
    }
}

[RegisterPower]
public sealed class ShmupPower : ModPowerTemplate
{
    private class Data
    {
        public bool Upgraded;
    }

    public override PowerType Type => PowerType.Buff;

    // 每张打灰机独立存在：升级前/升级后的能力各自独立触发（与吃豆人同款）。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/shmup_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/shmup_power.png");

    protected override object InitInternalData() => new Data();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Block", 0),
        new StringVar("FuelName")
    ];

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        var upgraded = cardSource?.IsUpgraded == true;
        GetInternalData<Data>().Upgraded = upgraded;
        // 描述中的格挡数与卡名随升级变化：燃料 / 燃料+。
        DynamicVars["Block"].BaseValue = upgraded ? 5 : 3;
        ((StringVar)DynamicVars["FuelName"]).StringValue = upgraded
            ? ModelDb.Card<Fuel>().Title + "+"
            : ModelDb.Card<Fuel>().Title;
        return Task.CompletedTask;
    }

    public override async Task AfterDeath(PlayerChoiceContext choiceContext, Creature creature, bool wasRemovalPrevented, float deathAnimLength)
    {
        if (CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var upgraded = GetInternalData<Data>().Upgraded;
        await CreatureCmd.GainBlock(Owner, new BlockVar(upgraded ? 5 : 3, ValueProp.Move), null);

        var combatState = Owner.CombatState;
        if (combatState != null)
        {
            var fuel = combatState.CreateCard(ModelDb.Card<Fuel>(), Owner.Player);
            if (upgraded)
            {
                CardCmd.Upgrade(fuel);
            }

            await CardPileCmd.AddGeneratedCardToCombat(fuel, PileType.Hand, Owner.Player);
        }

        await CardPileCmd.Draw(choiceContext, 1, Owner.Player);
    }
}
