# -*- coding: utf-8 -*-
import os
BASE = os.path.dirname(os.path.abspath(__file__))

def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    ok = True
    for old, new in pairs:
        if old not in s:
            print('MISS:', path, '->', old[:70].replace('\n', '\\n'))
            ok = False
            continue
        s = s.replace(old, new, 1)
    open(path, 'w', encoding='utf-8').write(s)
    return ok

C = os.path.join(BASE, 'STS2 MomoiCode')

# ============ 4. 创作的痛苦 ============
patch(os.path.join(C, 'Cards', 'CreativePain.cs'), [
    ('''    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(6m),  // 升级 8
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new DynamicVar("Burn", 2)    // 升级 3
    ];''',
     '''    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(7m),  // 升级 8
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new DynamicVar("Burn", 3),   // 升级 5
        new EnergyVar("CostReduce", 1)  // 打出构想后下一次打出前耗能-1（能量图标）
    ];'''),
    ('''    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(2);   // 6 -> 8
        DynamicVars["Burn"].UpgradeValueBy(1);  // 灼烧 2 -> 3
    }''',
     '''    // 每当你打出构想时，此牌的耗能将在下一次打出前减少1c。\n    public override async Task AfterCardPlayedLate(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner != Owner || cardPlay.Card is not ConceptCard)
        {
            return;
        }

        EnergyCost.AddUntilPlayed(-1, reduceOnly: true);
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(1);   // 7 -> 8
        DynamicVars["Burn"].UpgradeValueBy(2);  // 灼烧 3 -> 5
    }'''),
])

# ============ 5. 毁灭与新生：耗能1、升级固有 ============
patch(os.path.join(C, 'Cards', 'MinigameFlowCards.cs'), [
    ('''public sealed class DestructionAndRebirth : ModCardTemplate
{
    public DestructionAndRebirth() : base(2, CardType.Skill, CardRarity.Rare, TargetType.Self)''',
     '''public sealed class DestructionAndRebirth : ModCardTemplate
{
    public DestructionAndRebirth() : base(1, CardType.Skill, CardRarity.Rare, TargetType.Self)'''),
    ('''    protected override void OnUpgrade()
    {
        LocalKeywords.Add(CardKeyword.Retain);
    }
}

/// <summary>
/// 战胜心魔：1 费能力（罕见）。''',
     '''    protected override void OnUpgrade()
    {
        // 升级：获得固有。
        LocalKeywords.Add(CardKeyword.Innate);
    }
}

/// <summary>
/// 战胜心魔：1 费能力（罕见）。'''),
])

# ============ 15. 战胜心魔重制：立即抽牌 + 打出诅咒牌消耗 ============
patch(os.path.join(C, 'Cards', 'MinigameFlowCards.cs'), [
    ('''    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        var data = GetInternalData<Data>();
        data.BlockPer += (int)amount * (cardSource?.IsUpgraded == true ? 7 : 4);
        data.DrawNextTurn += (int)amount;
        DynamicVars["BlockPer"].BaseValue = data.BlockPer;
        await Task.CompletedTask;
    }

    public override async Task AfterCardExhausted(PlayerChoiceContext choiceContext, CardModel card, bool causedByEthereal)
    {
        if (card.Type != CardType.Curse || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        await CreatureCmd.GainBlock(Owner, new BlockVar(GetInternalData<Data>().BlockPer, ValueProp.Move), null);
    }

    // 下回合开始时额外抽牌（按层数），抽完重置。
    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var data = GetInternalData<Data>();
        if (data.DrawNextTurn <= 0)
        {
            return;
        }

        var draws = data.DrawNextTurn;
        data.DrawNextTurn = 0;
        await CardPileCmd.Draw(new ThrowingPlayerChoiceContext(), draws, Owner.Player);
    }
}''',
     '''    public override async Task AfterPowerAmountChanged(PlayerChoiceContext choiceContext, PowerModel power,
        decimal amount, Creature? applier, CardModel? cardSource)
    {
        if (power != this || amount <= 0)
        {
            return;
        }

        var data = GetInternalData<Data>();
        // 升级后格挡降低 1 点：升级前 4、升级后 6（原 7 降低 1）。\n        data.BlockPer += (int)amount * (cardSource?.IsUpgraded == true ? 6 : 4);
        data.DrawPerCurse += (int)amount;
        DynamicVars["BlockPer"].BaseValue = data.BlockPer;
        DynamicVars["DrawPer"].BaseValue = data.DrawPerCurse;
        await Task.CompletedTask;
    }

    // 诅咒牌被消耗：立即获得格挡并抽牌（叠加）。\n    public override async Task AfterCardExhausted(PlayerChoiceContext choiceContext, CardModel card, bool causedByEthereal)
    {
        if (card.Type != CardType.Curse || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var data = GetInternalData<Data>();
        await CreatureCmd.GainBlock(Owner, new BlockVar(data.BlockPer, ValueProp.Move), null);
        if (data.DrawPerCurse > 0)
        {
            await CardPileCmd.Draw(choiceContext, data.DrawPerCurse, Owner.Player);
        }
    }

    // 打出的诅咒牌直接消耗。\n    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card.Type != CardType.Curse || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        await CardCmd.Exhaust(choiceContext, cardPlay.Card);
    }
}'''),
    ('''    private class Data
    {
        public int BlockPer = 0;   // 叠加后的每诅咒格挡（升级 4/7）
        public int DrawNextTurn = 0; // 叠加后的下回合额外抽牌数
    }''',
     '''    private class Data
    {
        public int BlockPer = 0;      // 叠加后的每诅咒格挡（升级前 4/升级后 6）
        public int DrawPerCurse = 0;  // 叠加后的每诅咒抽牌数
    }'''),
    ('''    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("BlockPer", 0)
    ];

    public override async Task AfterPowerAmountChanged''',
     '''    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("BlockPer", 0),
        new DynamicVar("DrawPer", 0)
    ];

    public override async Task AfterPowerAmountChanged'''),
])

# ============ 8. 构想回合开始被动改到构想自身 ============
patch(os.path.join(C, 'Cards', 'ConceptCard.cs'), [
    ('''    // 打出：摸 {计数} 张牌、获得 {计数} 点能量、获得 {计数} 点活力。''',
     '''    // 回合开始时：数值 +1（升级 +2），并按自身数值添加特定诅咒（构想的被动是自身效果）。\n    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner.Creature) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        if (Pile?.Type != PileType.Hand)
        {
            return;
        }

        var cap = this.GetOrCreateCapability<ConceptCounterCapability>();
        cap.AddCount(IsUpgraded ? 2 : 1);

        var curseType = cap.Count switch
        {
            >= 6 => typeof(Enthralled),
            5 => typeof(Doubt),
            4 => typeof(PoorSleep),
            3 => typeof(Writhe),
            _ => null
        };

        if (curseType != null)
        {
            var curse = Owner.Creature.CombatState?.CreateCard((CardModel)ModelDb.Get(curseType), Owner);
            if (curse != null)
            {
                await CardPileCmd.AddGeneratedCardToCombat(curse, PileType.Hand, Owner);
            }
        }

        NCombatRoom.Instance?.Ui.Hand?.GetCard(this)?.UpdateVisuals(PileType.Hand, CardPreviewMode.Normal);
    }

    // 打出：摸 {计数} 张牌、获得 {计数} 点能量、获得 {计数} 点活力。'''),
])

# ============ 遗物只负责添加构想 ============
patch(os.path.join(C, 'Relics', 'DriedInspiration.cs'), [
    ('''        CardModel? newConcept = null;
        CardModel? curseModel = null;

        var concept = hand.Cards.FirstOrDefault(c => c is ConceptCard);
        if (concept == null)
        {
            // 手上没有构想：生成一张（最后放到最左边）。
            newConcept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), player);
        }
        else
        {
            // 已有构想：计数 +1（升级后 +2），并按计数选诅咒。
            var cap = concept.GetOrCreateCapability<ConceptCounterCapability>();
            cap.AddCount(concept.CurrentUpgradeLevel >= 1 ? 2 : 1);

            // 计数已变，强制刷新卡面让数值实时显示。
            NCombatRoom.Instance?.Ui.Hand?.GetCard(concept)?.UpdateVisuals(PileType.Hand, CardPreviewMode.Normal);

            curseModel = cap.Count switch
            {
                >= 6 => ModelDb.Card<Enthralled>(),
                5 => ModelDb.Card<Doubt>(),
                4 => ModelDb.Card<PoorSleep>(),
                3 => ModelDb.Card<Writhe>(),
                _ => null
            };
        }

        // 诅咒先放（最右边），构想最后放（最左边）。
        if (curseModel != null)
        {
            var curse = combatState.CreateCard(curseModel, player);
            await CardPileCmd.AddGeneratedCardToCombat(curse, PileType.Hand, player, CardPilePosition.Bottom);
        }

        if (newConcept != null)
        {
            await CardPileCmd.AddGeneratedCardToCombat(newConcept, PileType.Hand, player, CardPilePosition.Top);
        }''',
     '''        // 初始遗物只负责添加构想（数值增长与诅咒添加为构想自身效果）。\n        if (!hand.Cards.Any(c => c is ConceptCard))
        {
            var newConcept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), player);
            await CardPileCmd.AddGeneratedCardToCombat(newConcept, PileType.Hand, player, CardPilePosition.Top);
        }'''),
])

# ============ 9. 双线叙事：复制所有构想 ============
patch(os.path.join(C, 'Cards', 'RemainingCards3.cs'), [
    ('''        // 使构想的数值加 2。
        await ConceptCounterCapability.AddCountToAllInHand(choiceContext, Owner.Creature, 2);

        // 构想复制品（继承当前数值，附魔灵魂之力：失去消耗）。
        var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), Owner);
        concept.GetOrCreateCapability<ConceptCounterCapability>().SetCount(
            ConceptCounterCapability.GetMaxCountInHand(Owner.Creature));
        CardCmd.Enchant<SoulsPower>(concept, 1);
        await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, Owner);''',
     '''        // 使构想的数值加 2。
        await ConceptCounterCapability.AddCountToAllInHand(choiceContext, Owner.Creature, 2);

        // 复制手牌中的所有构想，全部复制品附魔灵魂之力（失去消耗）。
        foreach (var original in PileType.Hand.GetPile(player).Cards.Where(c => c is ConceptCard).ToList())
        {
            var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), Owner);
            concept.GetOrCreateCapability<ConceptCounterCapability>().SetCount(
                original.GetOrCreateCapability<ConceptCounterCapability>().Count);
            CardCmd.Enchant<SoulsPower>(concept, 1);
            await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, Owner);
        }'''),
])

# ============ 10. 重振旗鼓：Instanced + 低血自动打出 ============
patch(os.path.join(C, 'Cards', 'RemainingCards3.cs'), [
    ('''    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/rally_again_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/rally_again_power.png");''',
     '''    public override PowerType Type => PowerType.Buff;

    // 无法叠加：每张重振旗鼓独立存在，打出构想后依次触发。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/rally_again_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/rally_again_power.png");'''),
    ('''    // 生命低于 20% 时立即打出（每回合一次）。
    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        if (Owner.CurrentHp >= Owner.MaxHp / 5)
        {
            return;
        }

        var source = GetInternalData<Data>().SourceCard;
        if (source != null && source.Pile != null)
        {
            await PowerCmd.Apply<IntangiblePower>(new ThrowingPlayerChoiceContext(), Owner, 1, Owner, null);
            await CardCmd.AutoPlay(new ThrowingPlayerChoiceContext(), source, null);
        }
    }
}''',
     '''    // 生命降低后低于 20% 时立即打出（可插入敌人多段攻击之间）。\n    public override async Task AfterDamageReceived(PlayerChoiceContext choiceContext, Creature target, DamageResult result,
        ValueProp props, Creature? dealer, CardModel? cardSource)
    {
        if (target != Owner || CombatManager.Instance.IsOverOrEnding || GetInternalData<Data>().Triggered)
        {
            return;
        }

        if (Owner.CurrentHp * 5 >= Owner.MaxHp)
        {
            return;
        }

        GetInternalData<Data>().Triggered = true;
        var source = GetInternalData<Data>().SourceCard;
        if (source != null && source.Pile != null)
        {
            await PowerCmd.Apply<IntangiblePower>(new ThrowingPlayerChoiceContext(), Owner, 1, Owner, null);
            await CardCmd.AutoPlay(new ThrowingPlayerChoiceContext(), source, null);
        }
    }
}'''),
    ('''    private class Data
    {
        public RallyAgain? SourceCard;
    }''',
     '''    private class Data
    {
        public RallyAgain? SourceCard;
        public bool Triggered;
    }'''),
])

# ============ 11. 轮回 ============
patch(os.path.join(C, 'Cards', 'RemainingCards2.cs'), [
    ('''public sealed class Reincarnation : ModCardTemplate
{
    public Reincarnation() : base(4, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }''',
     '''public sealed class Reincarnation : ModCardTemplate
{
    public Reincarnation() : base(3, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }'''),
    ('''    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Retain };

    protected override async Task OnPlay''',
     '''    protected override async Task OnPlay'''),
    ('''    protected override void OnUpgrade()
    {
        EnergyCost.UpgradeBy(-1);
    }
}

[RegisterPower]
public sealed class ReincarnationDrainPower''',
     '''    protected override void OnUpgrade()
    {
        // 升级：获得保留。
        LocalKeywords.Add(CardKeyword.Retain);
    }
}

[RegisterPower]
public sealed class ReincarnationDrainPower'''),
    ('''            await CardPileCmd.AddGeneratedCardToCombat(clone, PileType.Hand, player);
            await CardCmd.AutoPlay(choiceContext, clone, null);
            await CardCmd.Exhaust(choiceContext, clone);
        }
    }''',
     '''            await CardPileCmd.AddGeneratedCardToCombat(clone, PileType.Hand, player);
            await CardCmd.AutoPlay(choiceContext, clone, null);
            // 能力牌打出后自动消耗（不在任何牌堆）；其余复制品打出后进入弃牌堆，再消耗。\n            if (clone.Pile != null && clone.Pile.Type is not PileType.None)
            {
                await CardCmd.Exhaust(choiceContext, clone);
            }
        }
    }'''),
    ('''        if (_isLoopCopy)
        {
            await PowerCmd.Apply<ReincarnationDrainPower>(choiceContext, Owner.Creature,
                IsUpgraded ? 1 : 2, Owner.Creature, this);
            return;
        }''',
     '''        if (_isLoopCopy)
        {
            // 轮回代价：升级前后都只失去 1 点最大生命值（可叠加）。
            await PowerCmd.Apply<ReincarnationDrainPower>(choiceContext, Owner.Creature,
                1, Owner.Creature, this);
            return;
        }'''),
])

# ============ 12. 得道多助：队列不清空（每回合都触发） ============
patch(os.path.join(C, 'Cards', 'RemainingCards3.cs'), [
    ('''        data.GenerationQueue.Clear();
    }
}''',
     '''        // 不清空队列：之后的每个回合开始都会按打出顺序重新生成。\n    }
}'''),
])

# ============ 19. 创造性品味：队列不清空 ============
patch(os.path.join(C, 'Cards', 'MinigameFlowCards.cs'), [
    ('''        data.GenerationQueue.Clear();
    }
}''',
     '''        // 不清空队列：之后的每个回合开始都会按打出顺序重新生成。\n    }
}'''),
])

# ============ 20. 白与黑：本场战斗内生效 ============
patch(os.path.join(C, 'Cards', 'RemainingSpecialCards.cs'), [
    ('''        // 若已选择过，直接生成所选牌。
        if (RunStats.WhiteBlackChoice != null)
        {
            var chosenType = RunStats.WhiteBlackChoice == nameof(ShowMyStrength) ? typeof(ShowMyStrength) : typeof(BigSister);''',
     '''        // 若本场战斗已选择过，直接生成所选牌（战斗结束恢复两个选项）。
        if (CombatStats.WhiteBlackChoice != null)
        {
            var chosenType = CombatStats.WhiteBlackChoice == nameof(ShowMyStrength) ? typeof(ShowMyStrength) : typeof(BigSister);'''),
    ('''            // 整局游戏继承：后续同名牌直接给所选。
            RunStats.WhiteBlackChoice = picked is ShowMyStrength ? nameof(ShowMyStrength) : nameof(BigSister);''',
     '''            // 本场战斗内继承：后续同名牌直接给所选。
            CombatStats.WhiteBlackChoice = picked is ShowMyStrength ? nameof(ShowMyStrength) : nameof(BigSister);'''),
])

patch(os.path.join(C, 'CombatStats.cs'), [
    ('''    /// <summary>本场战斗打出过的相遇次数（所有相遇共享解锁进度）。</summary>
    public static int EncounterPlays { get; private set; }''',
     '''    /// <summary>本场战斗打出过的相遇次数（所有相遇共享解锁进度）。</summary>
    public static int EncounterPlays { get; private set; }

    /// <summary>白与黑本场战斗的选择（战斗结束恢复两个选项）。</summary>
    public static string? WhiteBlackChoice { get; set; }'''),
    ('''        EncounterPlays = 0;
        Cards.GrindingState.Reduction = 0;''',
     '''        EncounterPlays = 0;
        WhiteBlackChoice = null;
        Cards.GrindingState.Reduction = 0;'''),
])

# ============ 17. 俄罗斯方块：结算时清除所有满手牌效果 ============
patch(os.path.join(C, 'Cards', 'RemainingCards5.cs'), [
    ('''        await PowerCmd.Remove(this);
        return true;
    }''',
     '''        // 触发一次满手牌结算后，清除所有其它的满手牌结算效果。
        foreach (var other in Owner.GetPowerInstances(ModelDb.Get(typeof(TetrisFullHandPower)).Id).ToList())
        {
            if (other != this)
            {
                await PowerCmd.Remove(other);
            }
        }

        await PowerCmd.Remove(this);
        return true;
    }'''),
])

# ============ 22. 活力显示修复：火力拦截时清除绑定 ============
patch(os.path.join(C, 'Patches', 'VigorFirepowerPatch.cs'), [
    ('''        if (firepower != null && firepower.Amount > 0)
        {
            Entry.Logger.Info($"[Firepower] AfterAttack intercepted: vigor={__instance.Amount} firepower={firepower.Amount}");
            __result = FirepowerHooks.ConsumeFirepowerAsync(choiceContext, firepower);
            return false; // 跳过原方法：活力不消耗。
        }''',
     '''        if (firepower != null && firepower.Amount > 0)
        {
            Entry.Logger.Info($"[Firepower] AfterAttack intercepted: vigor={__instance.Amount} firepower={firepower.Amount}");
            // 清除攻击绑定：否则手牌中攻击牌伤害预览不会显示活力加成。
            __instance.GetInternalData<VigorPower.Data>().commandToModify = null;
            __result = FirepowerHooks.ConsumeFirepowerAsync(choiceContext, firepower);
            return false; // 跳过原方法：活力不消耗。
        }'''),
])

# ============ 24. 破势：卡自身最终伤害倍数 + 加费修复 ============
patch(os.path.join(C, 'Cards', 'RemainingCards2.cs'), [
    ('''    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(20m),
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];''',
     '''    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(20m),
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new EnergyVar("CostIncrease", 1)
    ];

    // 每点活力最终伤害增加 10%/20%（卡自身倍数：卡面预览与打出都走同一管道）。
    public override decimal ModifyDamageMultiplicative(Creature? target, decimal amount, ValueProp props,
        Creature? dealer, CardModel? cardSource, CardPlay? cardPlay)
    {
        if (cardSource != this)
        {
            return 1m;
        }

        var vigor = Owner.Creature.GetPower<VigorPower>();
        return 1m + (vigor?.Amount ?? 0) * (IsUpgraded ? 0.2m : 0.1m);
    }'''),
    ('''        // 挂上最终伤害倍数（每点活力 +10%/+20%，参考超巨化药水的 ModifyDamageMultiplicative）。
        var power = await PowerCmd.Apply<MomentumBreakPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);

        // 估算最终伤害（用于眩晕判断）。
        var vigor = Owner.Creature.GetPower<VigorPower>();
        var multiplier = 1m + (vigor?.Amount ?? 0) * (IsUpgraded ? 0.2m : 0.1m);
        var finalDamage = (int)(Convert.ToDecimal(DynamicVars.CalculatedDamage) * multiplier);

        var attack = await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .Targeting(target)
            .Execute(choiceContext);

        // 眩晕判断：目标意图攻击且造成伤害大于其将造成的伤害。
        var monster = target.Monster;
        if (monster is { IntendsToAttack: true })
        {
            var incoming = monster.NextMove.Intents
                .OfType<AttackIntent>()
                .Sum(i => i.GetTotalDamage(new[] { Owner.Creature }, monster.Creature));
            if (finalDamage > incoming)
            {
                await CreatureCmd.Stun(target);
                EnergyCost.AddUntilPlayed(1);
            }
        }

        if (power != null)
        {
            await PowerCmd.Remove(power);
        }
    }''',
     '''        var attack = await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .Targeting(target)
            .Execute(choiceContext);

        // 眩晕判断：目标意图攻击且造成的伤害大于其将造成的伤害。
        var monster = target.Monster;
        if (monster is { IntendsToAttack: true })
        {
            var dealt = attack.Results.SelectMany(r => r).Sum(r => r.TotalDamage);
            var incoming = monster.NextMove.Intents
                .OfType<AttackIntent>()
                .Sum(i => i.GetTotalDamage(new[] { Owner.Creature }, monster.Creature));
            if (dealt > incoming)
            {
                await CreatureCmd.Stun(target);
                // 这张牌的耗能增加1（本场战斗）。
                EnergyCost.AddThisCombat(1);
            }
        }
    }'''),
])

# ============ 27. 稀有度：勇气加护→稀有、严守截稿日→罕见 ============
patch(os.path.join(C, 'Cards', 'RemainingSpecialCards.cs'), [
    ("public CourageBoon() : base(0, CardType.Attack, CardRarity.Uncommon, TargetType.AllEnemies)",
     "public CourageBoon() : base(0, CardType.Attack, CardRarity.Rare, TargetType.AllEnemies)"),
])
patch(os.path.join(C, 'Cards', 'ConceptFlowCards.cs'), [
    ("public MeetDeadline() : base(3, CardType.Skill, CardRarity.Rare, TargetType.Self)",
     "public MeetDeadline() : base(3, CardType.Skill, CardRarity.Uncommon, TargetType.Self)"),
])

# ============ 28. 红色牌：Plot(谋划) 换 Stratagem(计策) ============
patch(os.path.join(C, 'Cards', 'PickRed.cs'), [
    ("        typeof(Volley), typeof(Plot), typeof(Rend), typeof(Calamity),",
     "        typeof(Volley), typeof(Stratagem), typeof(Rend), typeof(Calamity),"),
])

# ============ 29. 捕鱼达人：渔获加入牌组用 Deck 堆的 Add ============
patch(os.path.join(C, 'Cards', 'RemainingCards2.cs'), [
    ('''                    var catchCard = Owner.Creature.CombatState.CreateCard(ModelDb.Card<Catch>(), Owner);
                    if (IsUpgraded)
                    {
                        CardCmd.Upgrade(catchCard);
                    }

                    await CardPileCmd.AddGeneratedCardToCombat(catchCard, PileType.Deck, Owner);''',
     '''                    var catchCard = Owner.Creature.CombatState.CreateCard(ModelDb.Card<Catch>(), Owner);
                    if (IsUpgraded)
                    {
                        CardCmd.Upgrade(catchCard);
                    }

                    // 加入牌组（Deck 是局级牌堆，不能用战斗生成 API）。
                    await CardPileCmd.Add(catchCard, PileType.Deck);'''),
])

# ============ 33. 旅行异蛙→游戏牌 + 全部游戏牌侧栏 ============
patch(os.path.join(C, 'Cards', 'RemainingCards3.cs'), [
    ('''public sealed class TravelFrog : ModCardTemplate
{
    public TravelFrog() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");''',
     '''public sealed class TravelFrog : ModCardTemplate
{
    public TravelFrog() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 游戏牌：不可被临时添加，但被视为小游戏牌。
    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.FullGameTag };'''),
])

print('patch A done')
