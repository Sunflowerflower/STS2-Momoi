# -*- coding: utf-8 -*-
import os
BASE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(BASE, 'STS2 MomoiCode')

def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    ok = True
    for old, new in pairs:
        if old not in s:
            print('MISS:', path, '->', old[:60].replace('\n', '\\n'))
            ok = False
            continue
        s = s.replace(old, new, 1)
    open(path, 'w', encoding='utf-8').write(s)

# ============ 13. 灵感爆发重做：我的回合！衍生牌 ============
p = os.path.join(C, 'Cards', 'RemainingCards3.cs')
s = open(p, encoding='utf-8').read()
# 卡牌 OnPlay 改：加我的回合
old = '''    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 升级前/升级后是两个独立能力：各自叠加额外回合数，可同时触发。
        if (IsUpgraded)
        {
            await PowerCmd.Apply<InspirationUpgradedPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }
        else
        {
            await PowerCmd.Apply<InspirationPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }
    }'''
new = '''    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 升级前/升级后是两个独立能力：各自叠加添加「我的回合！」的张数，可同时触发。
        if (IsUpgraded)
        {
            await PowerCmd.Apply<InspirationUpgradedPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }
        else
        {
            await PowerCmd.Apply<InspirationPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }
    }

    // 侧栏：我的回合！。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<MyTurn>(IsUpgraded)
    ];'''
if old in s:
    s = s.replace(old, new, 1)
else:
    print('MISS inspiration OnPlay')

# 两个能力的触发逻辑改为发牌
old = '''    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card is not ConceptCard concept)
        {
            return;
        }

        // 升级前：数值不低于 6。
        if (concept.GetOrCreateCapability<ConceptCounterCapability>().Count >= 6)
        {
            GetInternalData<Data>().PendingExtraTurns += Amount;
        }
    }

    // 触发额外回合（原版 ShouldTakeExtraTurn 机制）。
    public override bool ShouldTakeExtraTurn(Player player)
    {
        if (player != Owner.Player)
        {
            return false;
        }

        var data = GetInternalData<Data>();
        if (data.PendingExtraTurns > 0)
        {
            data.PendingExtraTurns--;
            return true;
        }

        return false;
    }

    public override Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (participants.Contains(Owner))
        {
            GetInternalData<Data>().PendingExtraTurns = 0;
        }

        return Task.CompletedTask;
    }
}'''
new = '''    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card is not ConceptCard concept)
        {
            return;
        }

        // 升级前：数值不低于 6 → 添加我的回合！（叠加张数）。
        if (concept.GetOrCreateCapability<ConceptCounterCapability>().Count >= 6)
        {
            var combatState = Owner.CombatState;
            if (combatState != null)
            {
                for (int i = 0; i < Amount; i++)
                {
                    var myTurn = combatState.CreateCard(ModelDb.Card<MyTurn>(), Owner.Player);
                    await CardPileCmd.AddGeneratedCardToCombat(myTurn, PileType.Hand, Owner.Player);
                }
            }
        }
    }
}'''
if old in s:
    s = s.replace(old, new, 1)
else:
    print('MISS inspiration base power')

old = '''    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card is not ConceptCard concept)
        {
            return;
        }

        if (concept.GetOrCreateCapability<ConceptCounterCapability>().Count >= 5)
        {
            GetInternalData<Data>().PendingExtraTurns += Amount;
        }
    }

    public override bool ShouldTakeExtraTurn(Player player)
    {
        if (player != Owner.Player)
        {
            return false;
        }

        var data = GetInternalData<Data>();
        if (data.PendingExtraTurns > 0)
        {
            data.PendingExtraTurns--;
            return true;
        }

        return false;
    }

    public override Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (participants.Contains(Owner))
        {
            GetInternalData<Data>().PendingExtraTurns = 0;
        }

        return Task.CompletedTask;
    }
}'''
new = '''    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card is not ConceptCard concept)
        {
            return;
        }

        // 升级后：数值不低于 5 → 添加我的回合！+（叠加张数）。
        if (concept.GetOrCreateCapability<ConceptCounterCapability>().Count >= 5)
        {
            var combatState = Owner.CombatState;
            if (combatState != null)
            {
                for (int i = 0; i < Amount; i++)
                {
                    var myTurn = combatState.CreateCard(ModelDb.Card<MyTurn>(), Owner.Player);
                    CardCmd.Upgrade(myTurn);
                    await CardPileCmd.AddGeneratedCardToCombat(myTurn, PileType.Hand, Owner.Player);
                }
            }
        }
    }
}'''
if old in s:
    s = s.replace(old, new, 1)
else:
    print('MISS inspiration upgraded power')

# 新增我的回合！卡与能力（追加到文件末尾）
s += '''

/// <summary>
/// 我的回合！：1 费技能（衍生）。选择 1 张牌添加保留（升级 2 张），本回合结束后额外获得一回合，结束你的回合。消耗。
/// </summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class MyTurn : ModCardTemplate
{
    public MyTurn() : base(1, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Cards", 1)  // 升级 2
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        if (player != null)
        {
            // 先选择牌添加保留（已有保留词条的牌不进入选项）。
            var picked = (await CardSelectCmd.FromHand(choiceContext, player,
                new CardSelectorPrefs(new LocString("card_selection", "TO_RETAIN"), 0, DynamicVars["Cards"].IntValue)
                {
                    Cancelable = true,
                    RequireManualConfirmation = true
                },
                c => !c.Keywords.Contains(CardKeyword.Retain), this)).ToList();
            foreach (var card in picked)
            {
                card.LocalKeywords.Add(CardKeyword.Retain);
            }
        }

        // 获得额外回合的效果。
        await PowerCmd.Apply<MyTurnPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);

        // 最后结束回合。
        PlayerCmd.EndTurn(Owner, canBackOut: false);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Cards"].UpgradeValueBy(1);
    }
}

/// <summary>我的回合！的额外回合：本回合结束后获得一回合。该效果无法叠加。</summary>
[RegisterPower]
public sealed class MyTurnPower : ModPowerTemplate
{
    private class Data
    {
        public bool Used;
    }

    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/inspiration_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/inspiration_power.png");

    protected override object InitInternalData() => new Data();

    // 无法叠加：多张也只获得一回合（打出后立即结束回合，因此同一回合通常只有一张）。\n    public override bool ShouldTakeExtraTurn(Player player)
    {
        if (player != Owner.Player)
        {
            return false;
        }

        var data = GetInternalData<Data>();
        if (data.Used)
        {
            return false;
        }

        data.Used = true;
        return true;
    }
}
'''
open(p, 'w', encoding='utf-8').write(s)

# ============ 36. 集结：文本、侧栏、隐藏 5%、实时减费已在 patch 中 ============
patch(os.path.join(C, 'Cards', 'MiscRareCards.cs'), [
    ('''public sealed class Rally : ModCardTemplate
{
    private static readonly Type[] ForeignCards =
    [
        typeof(Unmovable), typeof(BladeOfInk), typeof(ForegoneConclusion), typeof(Transfigure), typeof(Hyperbeam)
    ];''',
     '''public sealed class Rally : ModCardTemplate
{
    private static readonly Type[] ForeignCards =
    [
        typeof(Unmovable), typeof(BladeOfInk), typeof(ForegoneConclusion), typeof(Transfigure), typeof(Hyperbeam)
    ];

    // 隐藏效果（5%）：改为获得 5 张形态牌。
    private static readonly Type[] HiddenForms =
    [
        typeof(DemonForm), typeof(SerpentForm), typeof(VoidForm), typeof(ReaperForm), typeof(EchoForm)
    ];'''),
    ('''    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };''',
     '''    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    // 侧栏1：特定牌；侧栏2：支援牌。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_RALLY.sidebar1")),
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_RALLY.sidebar2"))
    ];'''),
    ('''        // 本场战斗中每打出过一张支援牌，这张牌的耗费-1（打出时结算，不封顶）。
        EnergyCost.AddThisCombat(-CombatStats.SupportCardsPlayed, reduceOnly: true);

        foreach (var type in ForeignCards)
        {''',
     '''        // 本场战斗中每打出过一张支援牌，这张牌的耗费-1（打出时结算，不封顶）。
        EnergyCost.AddThisCombat(-CombatStats.SupportCardsPlayed, reduceOnly: true);

        // 隐藏效果：5% 概率改为获得 5 张形态牌。
        var pool = Owner.RunState.Rng.CombatCardSelection.NextInt(100) < 5 ? HiddenForms : ForeignCards;

        foreach (var type in pool)
        {'''),
])

# ============ 37. 消消乐重做 ============
patch(os.path.join(C, 'Cards', 'Match3.cs'), [
    ('''    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(4m),  // 攻击：每张 4 伤（升级 5）
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new BlockVar(5, ValueProp.Move)  // 技能：每张 5 格挡（升级 7）
    ];''',
     '''    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(4m),  // 攻击：每张 4 伤（升级 6）
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new BlockVar(5, ValueProp.Move),  // 技能：每张 5 格挡（升级 7）
        new EnergyVar(1)                 // 超过阈值每张 1 能量
    ];

    // 侧栏：按消耗牌类型触发的额外效果。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_MATCH3.sidebar"))
    ];'''),
    ('''    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 第一段：选择 1 张手牌（必消耗，并作为类型基准）。
        var first = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 1),
            null, this)).FirstOrDefault();
        if (first == null)
        {
            return;
        }

        var cardType = first.Type;
        await CardCmd.Exhaust(choiceContext, first);

        // 第二段：选择任意数量与其类型相同的牌（0 张起，手动确认），选完立即消耗。
        var rest = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 0, 99),
            (CardModel c) => c.Type == cardType, this)).ToList();
        foreach (var card in rest)
        {
            await CardCmd.Exhaust(choiceContext, card);
        }

        var count = 1 + rest.Count;''',
     '''    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 第一段：选择 1 张牌（作为类型基准，选择后返回手牌区）。
        var first = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 1),
            null, this)).FirstOrDefault();
        if (first == null)
        {
            return;
        }

        var cardType = first.Type;

        // 第二段：选择手牌区所有与第一次选择类型相同的牌消耗（包括第一次选择的牌）。
        var rest = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 0, 99),
            (CardModel c) => c.Type == cardType, this)).ToList();
        foreach (var card in rest)
        {
            await CardCmd.Exhaust(choiceContext, card);
        }

        var count = rest.Count;'''),
    ('''                case CardType.Attack:
                    // 每消耗 1 张就对所有敌人造成 4 点伤害；只有 1 名敌人时双倍。
                    // 用多段攻击（WithHitCount）一次结算：活力增伤对每一段都生效。
                    var damage = Convert.ToInt32(DynamicVars.CalculatedDamage);
                    if (combatState.HittableEnemies.Count() <= 1)
                    {
                        damage *= 2;
                    }

                    await DamageCmd.Attack(damage)
                        .FromCard(this, cardPlay)
                        .TargetingAllOpponents(combatState)
                        .WithHitCount(count)
                        .Execute(choiceContext);

                    break;''',
     '''                case CardType.Attack:
                    // 每消耗 1 张就对所有敌人造成 4 点伤害；只有 1 名敌人时双倍。
                    // 用多段攻击（WithHitCount）一次结算：活力增伤对每一段都生效。
                    var damage = Convert.ToInt32(DynamicVars.CalculatedDamage);
                    if (combatState.HittableEnemies.Count() <= 1)
                    {
                        damage *= 2;
                    }

                    await DamageCmd.Attack(damage)
                        .FromCard(this, cardPlay)
                        .TargetingAllOpponents(combatState)
                        .WithHitCount(count)
                        .Execute(choiceContext);

                    break;'''),
    ('''        if (count > 3)
        {
            // 每超过 1 张摸 1 张牌并获得 1 点能量。
            var extra = count - 3;
            await CardPileCmd.Draw(choiceContext, extra, Owner);
            await PlayerCmd.GainEnergy(extra, Owner);
        }
    }''',
     '''        if (count >= 3)
        {
            // 每超出 1 张抽 1 张牌并获得 1c。
            var extra = count - 2;
            if (extra > 0)
            {
                await CardPileCmd.Draw(choiceContext, extra, Owner);
                await PlayerCmd.GainEnergy(extra, Owner);
            }
        }
    }'''),
    ('''    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(1);  // 攻击 4 -> 5
        DynamicVars.Block.UpgradeValueBy(2);            // 技能 5 -> 7
    }''',
     '''    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(2);  // 攻击 4 -> 6
        DynamicVars.Block.UpgradeValueBy(2);            // 技能 5 -> 7
    }'''),
])

# ============ 33. 游戏牌侧栏统一注入 ============
# 为没有自定义 AdditionalHoverTips 的游戏牌加侧栏；已有侧栏的合并。
def add_game_sidebar(path, cls, existing=''):
    p2 = os.path.join(C, 'Cards', path)
    s = open(p2, encoding='utf-8').read()
    mark = 'public sealed class %s : ModCardTemplate' % cls
    if existing:
        old = existing
        new = existing.rstrip()[:-2] + ',\n        new HoverTip(new LocString("cards", "STS2_MOMOI_GAME_CARD_SIDEBAR"))\n    ];'
        if old in s:
            s = s.replace(old, new, 1)
        else:
            print('MISS sidebar merge', cls)
    else:
        # 在 AssetProfile 后插入
        anchor = '''    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");'''
        if anchor in s:
            s = s.replace(anchor, anchor + '''

    // 游戏牌侧栏。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_GAME_CARD_SIDEBAR"))
    ];''', 1)
        else:
            print('MISS sidebar anchor', cls)
    open(p2, 'w', encoding='utf-8').write(s)

# FishingMaster / FightingGame / GoldMiner / OldMaid / RolePlay / TravelFrog / FriendlyDuel / PlayThisOne
add_game_sidebar('RemainingCards2.cs', 'FishingMaster')
add_game_sidebar('RemainingCards2.cs', 'FightingGame')
add_game_sidebar('RemainingCards2.cs', 'GoldMiner')
add_game_sidebar('RemainingCards5.cs', 'OldMaid')
add_game_sidebar('RemainingCards5.cs', 'PlayThisOne')
add_game_sidebar('MultiplayerCards.cs', 'RolePlay')
add_game_sidebar('RemainingCards3.cs', 'TravelFrog')
add_game_sidebar('RemainingSpecialCards.cs', 'FriendlyDuel')

print('patch B done')
