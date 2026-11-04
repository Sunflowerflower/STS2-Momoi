# -*- coding: utf-8 -*-
import re

# ===== 4) 扫雷：抽到炸弹自动打出 =====
t = open('STS2 MomoiCode/Cards/RemainingCards4.cs', encoding='utf-8').read()
old = '''        await CardPileCmd.AddGeneratedCardToCombat(bomb, PileType.Draw, Owner);
        await CardPileCmd.Draw(choiceContext, DynamicVars["Cards"].BaseValue, Owner);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Cards"].UpgradeValueBy(1);
    }
}'''
new = '''        await CardPileCmd.AddGeneratedCardToCombat(bomb, PileType.Draw, Owner);
        await CardPileCmd.Draw(choiceContext, DynamicVars["Cards"].BaseValue, Owner);

        // 挂上"抽到炸弹直接打出"的监控（参考地狱狂徒/虚空的抽到触发）。
        await PowerCmd.Apply<MinesweeperPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
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

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/minesweeper_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/minesweeper_power.png");

    // 抽到炸弹时直接打出（本场战斗）。
    public override async Task AfterCardDrawn(PlayerChoiceContext choiceContext, CardModel card, bool fromHandDraw)
    {
        if (card is not TheBomb || card.Owner.Creature != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        await Cmd.Wait(0.25f);
        await CardCmd.AutoPlay(choiceContext, card, null);
    }
}'''
assert old in t, "minesweeper"
t = t.replace(old, new)
open('STS2 MomoiCode/Cards/RemainingCards4.cs', 'w', encoding='utf-8').write(t)
print("minesweeper ok")

# ===== 5) 植物大战僵尸：Instanced + Other 传递 =====
t = open('STS2 MomoiCode/Cards/RemainingCards5.cs', encoding='utf-8').read()
old = '''        var picked = await CardSelectCmd.FromChooseACardScreen(choiceContext, new List<CardModel> { leftCard, rightCard }, Owner);
        if (picked != null)
        {
            picked.SetToFreeThisTurn();
            await CardPileCmd.AddGeneratedCardToCombat(picked, PileType.Hand, Owner);

            // 下回合另一张入手。
            var other = picked == leftCard ? rightCard : leftCard;
            other.SetToFreeThisTurn();
            await PowerCmd.Apply<PlantsNextTurnPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
            _ = other;
        }'''
new = '''        var picked = (await CardSelectCmd.FromSimpleGrid(choiceContext, new List<CardModel> { leftCard, rightCard }, Owner,
            new CardSelectorPrefs(new LocString("card_selection", "TO_ADD_TO_HAND"), 1, 1))).FirstOrDefault();
        if (picked != null)
        {
            picked.SetToFreeThisTurn();
            await CardPileCmd.AddGeneratedCardToCombat(picked, PileType.Hand, Owner);

            // 下回合另一张入手（每张植物大战僵尸独立：Instanced）。
            var other = picked == leftCard ? rightCard : leftCard;
            other.SetToFreeThisTurn();
            var power = await PowerCmd.Apply<PlantsNextTurnPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
            if (power != null)
            {
                power.SetOtherCard(other);
            }
        }'''
assert old in t, "pvz"
t = t.replace(old, new)
old = '''[RegisterPower]
public sealed class PlantsNextTurnPower : ModPowerTemplate
{
    private class Data
    {
        public CardModel? Other;
    }

    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/plants_next_turn_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/plants_next_turn_power.png");

    protected override object InitInternalData() => new Data();

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)'''
new = '''[RegisterPower]
public sealed class PlantsNextTurnPower : ModPowerTemplate
{
    private class Data
    {
        public CardModel? Other;
    }

    // 每张植物大战僵尸独立生效（多张各自给各自的另一张）。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/plants_next_turn_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/plants_next_turn_power.png");

    protected override object InitInternalData() => new Data();

    public void SetOtherCard(CardModel other) => GetInternalData<Data>().Other = other;

    public override async Task AfterSideTurnStart(CombatSide side, IReadOnlyList<Creature> participants, ICombatState combatState)'''
assert old in t, "pvz power"
t = t.replace(old, new)
open('STS2 MomoiCode/Cards/RemainingCards5.cs', 'w', encoding='utf-8').write(t)
print("pvz ok")

# ===== 6) 吃豆人：升级版 + Instanced =====
t = open('STS2 MomoiCode/Cards/RemainingCards5.cs', encoding='utf-8').read()
old = '''        // 自动打出 1 张疯狂进食并消耗。
        var frenzy = combatState.CreateCard(ModelDb.Card<FeedingFrenzy>(), player);
        await CardCmd.AutoPlay(new ThrowingPlayerChoiceContext(), frenzy, null);
        await CardCmd.Exhaust(new ThrowingPlayerChoiceContext(), frenzy);

        // 随机消耗 1 张诅咒牌。
        var curses = PileType.Hand.GetPile(player).Cards.Where(c => c.Type == CardType.Curse).ToList();
        if (curses.Count > 0)
        {
            var curse = player.RunState.Rng.CombatCardSelection.NextItem(curses);
            if (curse != null)
            {
                await CardCmd.Exhaust(new ThrowingPlayerChoiceContext(), curse);
            }
        }
        else
        {
            // 无诅咒牌：富足入手。
            var abundance = combatState.CreateCard(ModelDb.Card<Abundance>(), player);
            if (Applier?.IsUpgraded == true)
            {
                CardCmd.Upgrade(abundance);
            }

            await CardPileCmd.AddGeneratedCardToCombat(abundance, PileType.Hand, player);
        }'''
new = '''        // 自动打出 1 张疯狂进食并消耗（升级版吃豆人给升级版）。
        var upgraded = GetInternalData<PacData>().Upgraded;
        var frenzy = combatState.CreateCard(ModelDb.Card<FeedingFrenzy>(), player);
        if (upgraded)
        {
            CardCmd.Upgrade(frenzy);
        }

        await CardCmd.AutoPlay(new ThrowingPlayerChoiceContext(), frenzy, null);
        await CardCmd.Exhaust(new ThrowingPlayerChoiceContext(), frenzy);

        // 随机消耗 1 张诅咒牌。
        var curses = PileType.Hand.GetPile(player).Cards.Where(c => c.Type == CardType.Curse).ToList();
        if (curses.Count > 0)
        {
            var curse = player.RunState.Rng.CombatCardSelection.NextItem(curses);
            if (curse != null)
            {
                await CardCmd.Exhaust(new ThrowingPlayerChoiceContext(), curse);
            }
        }
        else
        {
            // 无诅咒牌：富足入手（升级版）。
            var abundance = combatState.CreateCard(ModelDb.Card<Abundance>(), player);
            if (upgraded)
            {
                CardCmd.Upgrade(abundance);
            }

            await CardPileCmd.AddGeneratedCardToCombat(abundance, PileType.Hand, player);
        }'''
assert old in t, "pacman"
t = t.replace(old, new)
old = '''[RegisterPower]
public sealed class PacManPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;'''
new = '''[RegisterPower]
public sealed class PacManPower : ModPowerTemplate
{
    private class PacData
    {
        public bool Upgraded;
    }

    // 多张吃豆人独立生效。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    protected override object InitInternalData() => new PacData();

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        GetInternalData<PacData>().Upgraded = cardSource?.IsUpgraded == true;
        return Task.CompletedTask;
    }

    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;'''
assert old in t, "pacman power"
t = t.replace(old, new)
open('STS2 MomoiCode/Cards/RemainingCards5.cs', 'w', encoding='utf-8').write(t)
print("pacman ok")

# ===== 7) 夜以继日：Counter 叠加 =====
t = open('STS2 MomoiCode/Cards/ConceptFlowCards.cs', encoding='utf-8').read()
old = '''    // 多张夜以继日的效果应该叠加，叠加到失去活力的点数和增加构想的张数。
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;'''
if old in t:
    t = t.replace(old, '''    // 多张叠加：失去的活力与加入的构想数量按层数算。
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;''')
else:
    old = '''    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/day_and_night_power.png",'''
    new = '''    // 多张叠加：失去的活力与加入的构想数量按层数算。
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/day_and_night_power.png",'''
    assert old in t, "daynight power"
    t = t.replace(old, new)
old = '''        data.UsedThisTurn = true;

        // 失去 1 点活力。
        await MinigameSupport.LoseVigor(choiceContext, Owner, cardPlay.Card);

        // 将 1 张构想加入手牌。
        var combatState = Owner.CombatState;
        if (combatState != null)
        {
            var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), Owner.Player);
            await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, Owner.Player);
        }'''
new = '''        data.UsedThisTurn = true;

        // 按层数失去活力。
        for (int i = 0; i < Amount; i++)
        {
            await MinigameSupport.LoseVigor(choiceContext, Owner, cardPlay.Card);
        }

        // 按层数加入构想。
        var combatState = Owner.CombatState;
        if (combatState != null)
        {
            for (int i = 0; i < Amount; i++)
            {
                var concept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), Owner.Player);
                await CardPileCmd.AddGeneratedCardToCombat(concept, PileType.Hand, Owner.Player);
            }
        }'''
assert old in t, "daynight effect"
t = t.replace(old, new)
open('STS2 MomoiCode/Cards/ConceptFlowCards.cs', 'w', encoding='utf-8').write(t)
print("daynight ok")
