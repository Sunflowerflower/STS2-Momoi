using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Commands.Builders;
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
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.MonsterMoves.Intents;
using MegaCrit.Sts2.Core.Rewards;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using MegaCrit.Sts2.Core.Nodes.Vfx;
using MegaCrit.Sts2.Core.Rooms;
using MegaCrit.Sts2.Core.Runs;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;
using STS2_Momoi.Diagnostics;

namespace STS2_Momoi.Cards;

/// <summary>战斗房间辅助（获取当前战斗的 CombatRoom 模型）。</summary>
public static class CombatRoomHelper
{
    public static CombatRoom? GetCombatRoom(Player? player = null)
    {
        var runState = player?.RunState ?? MegaCrit.Sts2.Core.Runs.RunManager.Instance?.State;
        return runState?.CurrentRoom as CombatRoom;
    }
}

/// <summary>
/// 破势：2 费攻击（稀有）。造成 16 点伤害；活力在这张牌上发挥 4 倍的效果（升级：20 伤、5 倍）。
/// 若目标的意图为攻击，且这张牌造成的伤害大于目标即将对你造成的伤害，将其 1 回合内的意图改为眩晕，
/// 并将这张牌的耗费增加 1c（升级不再减费，升级前后都是 2 费）。
/// 「活力发挥 n 倍」由 Patches/VigorMultiplierPatch.cs 乘在 VigorPower 的加伤返回值上。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class MomentumBreak : ModCardTemplate
{
    public MomentumBreak() : base(2, CardType.Attack, CardRarity.Rare, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");


    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(16m),   // 升级 20
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m),
        new EnergyVar("CostIncrease", 1)
    ];

    // 「活力在这张牌上发挥 4 倍（升级 5 倍）的效果」不在卡里做，而在 Modifier：
    // 见 Patches/VigorMultiplierPatch.cs —— 原版力量与活力走同一条加伤通道（Hook.ModifyDamageInternal
    // 做 num += 返回值），在卡里手动再加一次会变成 1+n 倍。

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target == null)
        {
            return;
        }

        var attack = await MomoiSovereignStyle.Apply(
                DamageCmd.Attack(DynamicVars.CalculatedDamage)
                    .FromCard(this, cardPlay)
                    .Targeting(target))
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
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(4);   // 16 -> 20（耗能不再随升级变化）
    }
}

/// <summary>
/// 捕鱼达人！：X 费攻击（稀有·游戏牌）。对 1 名敌人造成 11 点伤害 X 次（升级 X+1），并将其 1 回合内的意图改为眩晕。
/// 若此牌直接斩杀了敌人，战斗结束时将 1 张渔获加入牌组（精英 2 张，Boss 3 张）。消耗。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class FishingMaster : ModCardTemplate
{
    protected override bool HasEnergyCostX => true;

    public FishingMaster() : base(0, CardType.Attack, CardRarity.Rare, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：渔获 + 斩杀提示（参考原版 Feed）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.Static(StaticHoverTip.Fatal),
        HoverTipFactory.FromCard<Catch>(IsUpgraded),
    ];

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.FullGameTag };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(8m),
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

        var hits = ResolveEnergyXValue() + (IsUpgraded ? 1 : 0);

        var attack = await DamageCmd.Attack(DynamicVars.CalculatedDamage)
            .FromCard(this, cardPlay)
            .Targeting(target)
            .WithHitCount(Math.Max(1, hits))
            .Execute(choiceContext);

        // 斩杀判定（参考原版 Feed）：攻击前目标所有能力的 ShouldOwnerDeathTriggerFatal 都为 true，
        // 且攻击后 WasTargetKilled == true。哪怕这一击直接结束战斗（转阶段/胜利），斩杀仍然成立，
        // 渔获照常加入永久牌组——不要用 IsOverOrEnding 拦截。
        bool shouldTriggerFatal = target.Powers.All(p => p.ShouldOwnerDeathTriggerFatal());
        if (shouldTriggerFatal && attack.Results.SelectMany(r => r).Any(r => r.WasTargetKilled))
        {
            var room = CombatRoomHelper.GetCombatRoom(Owner);
            if (room != null)
            {
                var count = room.RoomType switch
                {
                    MegaCrit.Sts2.Core.Rooms.RoomType.Boss => 3,
                    MegaCrit.Sts2.Core.Rooms.RoomType.Elite => 2,
                    _ => 1
                };
                for (int i = 0; i < count; i++)
                {
                    // 永久牌组：必须由 RunState 创建（Deck 是局级牌堆），再 CardPileCmd.Add 进 Deck。
                    var catchCard = Owner.RunState.CreateCard<Catch>(Owner);
                    if (IsUpgraded)
                    {
                        // 斩杀直接结束战斗时 IsEnding 为 true，CardCmd.Upgrade 会静默跳过升级；
                        // 这里直接调用升级内部方法（与 CardCmd.Upgrade 相同的核心逻辑）。
                        catchCard.UpgradeInternal();
                        catchCard.FinalizeUpgradeInternal();
                    }

                    CardCmd.PreviewCardPileAdd(await CardPileCmd.Add(catchCard, PileType.Deck));
                }
            }
        }
    }

    protected override void OnUpgrade()
    {
    }
}

/// <summary>渔获：0 费技能（衍生）。固有、保留、消耗。抽 1 张牌，获得 1c，获得 1 点活力（升级：抽 2、2c、2 活力）。</summary>
[RegisterCard(typeof(MegaCrit.Sts2.Core.Models.CardPools.TokenCardPool))]
public sealed class Catch : ModCardTemplate
{
    public Catch() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Innate, CardKeyword.Retain, CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Cards", 1),   // 升级 2
        new EnergyVar(1),  // 升级后仍为 1c
        new DynamicVar("Vigor", 1),   // 升级 2
        new DynamicVar("Heal", 4)     // 升级 6
    ];

    // 移除自身：打出时**立即**把牌组中的本尊移除（复制品不移除）。
    // 放在 OnPlay 里 await 掉，而不是在 GetResultLocationForCardPlay 里 fire-and-forget：
    // 这样即使打出后立刻结束战斗，移除也已经结算完。
    private async Task RemoveSelfFromDeck()
    {
        // 复制品不移除：IsClone（CloneOf != null）同时盖住两种复制方式 ——
        // 「大姐头」/「赖招复读」走 CreateClone，而「轮回」/「援护」走 CreateDupe。
        if (IsClone)
        {
            MomoiDiag.Log("[Catch] 这张是复制品(IsClone)，不移除牌组");
            return;
        }

        // 优先用 DeckVersion（战斗开始时从牌组克隆出来的那张所对应的牌组本尊）。
        var deckCard = DeckVersion;
        if (deckCard == null)
        {
            // 兜底：控制台 / FreeLoadout 这类直接塞到手牌的实例不会挂 DeckVersion，
            // 这时按卡 ID 在牌组里找一张同名牌移除，保证「打出即从牌组移除」始终生效。
            deckCard = Owner.Deck.Cards.FirstOrDefault(c => c.Id == Id);
        }

        if (deckCard == null)
        {
            MomoiDiag.Log("[Catch] 牌组里没有同名牌，跳过移除");
            return;
        }

        if (deckCard.Pile?.Type != PileType.Deck)
        {
            MomoiDiag.Log($"[Catch] 牌组卡不在 Deck 堆（Pile={deckCard.Pile?.Type}），跳过移除");
            return;
        }

        MomoiDiag.Log($"[Catch] 打出时从牌组移除本尊（DeckVersion={(DeckVersion != null ? "有" : "无")}）");
        await CardPileCmd.RemoveFromDeck(deckCard);
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await RemoveSelfFromDeck();

        await CardPileCmd.Draw(choiceContext, DynamicVars["Cards"].BaseValue, Owner);
        await PlayerCmd.GainEnergy(DynamicVars["Energy"].IntValue, Owner);
        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, DynamicVars["Vigor"].BaseValue, Owner.Creature, this);
        await CreatureCmd.Heal(Owner.Creature, DynamicVars["Heal"].BaseValue);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Cards"].UpgradeValueBy(1);
        // 设计：升级后能量仍为 1c。
        DynamicVars["Vigor"].UpgradeValueBy(1);
        DynamicVars["Heal"].UpgradeValueBy(2);
    }
}


/// <summary>
/// 格斗游戏：X 费攻击（稀有·游戏牌）。根据消耗的能量触发对应效果：
/// 0c：造成 4 点伤害，获得 1c。1c：造成 2 点伤害 5 次（有火力改为 8 次）。2c：造成 20 点伤害；
/// 选择最多 1 张手牌变化为王者之踢且本回合免费打出；若伤害突破格挡改为最多 6 张变化为异鸟扑击。
/// 3c+：造成 48 点伤害，获得 1c；生命低于 25% 时改为：获得 7 层火力、造成 53 点伤害、获得 1c。
/// 升级：先给予 1 层易伤。
/// 隐藏彩蛋：回合结束时此牌仍在手牌且能量≥3 且血量<25%：自动打出，对所有敌人造成 47 点伤害。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class FightingGame : ModCardTemplate
{
    protected override bool HasEnergyCostX => true;

    public FightingGame() : base(0, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.FullGameTag };
    // 四个侧边栏：描述消耗不同能量触发的效果。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_FIGHTING_GAME.sidebar0")),
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_FIGHTING_GAME.sidebar1")),
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_FIGHTING_GAME.sidebar2")),
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_FIGHTING_GAME.sidebar3")),
    ];

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DamageVar(4, ValueProp.Move),
        new EnergyVar(1),
        new EnergyVar("Tier0", 0),  // 侧栏能量档位图标
        new EnergyVar("Tier1", 1),
        new EnergyVar("Tier2", 2),
        new EnergyVar("Tier3", 3)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        var combatState = Owner.Creature.CombatState;
        if (target == null || combatState == null)
        {
            return;
        }

        if (!IsUpgraded)
        {
            // 升级前：先给予自身 1 层虚弱（升级后删去此效果）。
            await PowerCmd.Apply<WeakPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        }

        var x = ResolveEnergyXValue();
        var lowHp = Owner.Creature.CurrentHp * 4 < Owner.Creature.MaxHp;

        if (x == 0)
        {
            // 0c：造成 6 点伤害。
            await DamageCmd.Attack(6).FromCard(this, cardPlay).Targeting(target).Execute(choiceContext);
        }
        else if (x == 1)
        {
            // 1c：造成 1 点伤害 5 次（有火力改为 8 次）。
            var firepower = Owner.Creature.GetPower<FirepowerPower>();
            var hits = firepower is { Amount: > 0 } ? 8 : 5;
            await DamageCmd.Attack(1).FromCard(this, cardPlay).Targeting(target).WithHitCount(hits).Execute(choiceContext);
        }
        else if (x == 2)
        {
            // 2c：造成 12 点伤害（战士完美打击同款攻击特效）。
            var attack = await DamageCmd.Attack(12).FromCard(this, cardPlay).Targeting(target)
                .WithHitFx(null, null, "heavy_attack.mp3")
                .WithHitVfxNode((Creature t) => NBigSlashVfx.Create(t))
                .WithHitVfxNode((Creature t) => NBigSlashImpactVfx.Create(t))
                .Execute(choiceContext);
            var brokeBlock = attack.Results.SelectMany(r => r).Any(r => r.Receiver == target && r.BlockedDamage > 0 && r.UnblockedDamage > 0);

            // 选择手牌变化。
            var player = Owner.Creature.Player;
            if (player != null)
            {
                var max = brokeBlock ? 6 : 1;
                var picked = (await CardSelectCmd.FromHand(choiceContext, player,
                    new CardSelectorPrefs(new LocString("card_selection", "TO_TRANSFORM"), 0, max) { Cancelable = true, RequireManualConfirmation = true }, null, this)).ToList();
                foreach (var card in picked)
                {
                    var replacementType = brokeBlock ? typeof(ByrdSwoop) : typeof(KinglyKick);
                    var replacement = combatState.CreateCard((CardModel)ModelDb.Get(replacementType), Owner);
                    replacement.SetToFreeThisTurn();
                    await CardCmd.Transform(card, replacement);
                }
            }
        }
        else
        {
            // 3c+：储君轰击同款攻击特效。
            if (lowHp)
            {
                await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature, 7, Owner.Creature, this);
                var nCreature = NCombatRoom.Instance?.GetCreatureNode(target);
                if (nCreature != null)
                {
                    var missile = NLargeMagicMissileVfx.Create(nCreature.GetBottomOfHitbox(), new Godot.Color("50b598"));
                    NCombatRoom.Instance?.CombatVfxContainer.AddChildSafely(missile);
                    if (missile != null)
                    {
                        await Cmd.Wait(missile.WaitTime);
                    }
                }

                await DamageCmd.Attack(53).FromCard(this, cardPlay).Targeting(target)
                    .WithHitFx("vfx/vfx_attack_blunt", null, "blunt_attack.mp3")
                    .Execute(choiceContext);
            }
            else
            {
                var nCreature = NCombatRoom.Instance?.GetCreatureNode(target);
                if (nCreature != null)
                {
                    var missile = NLargeMagicMissileVfx.Create(nCreature.GetBottomOfHitbox(), new Godot.Color("50b598"));
                    NCombatRoom.Instance?.CombatVfxContainer.AddChildSafely(missile);
                    if (missile != null)
                    {
                        await Cmd.Wait(missile.WaitTime);
                    }
                }

                await DamageCmd.Attack(48).FromCard(this, cardPlay).Targeting(target)
                    .WithHitFx("vfx/vfx_attack_blunt", null, "blunt_attack.mp3")
                    .Execute(choiceContext);
            }
        }
    }

    // 隐藏彩蛋：回合结束时此牌仍在手牌、剩余能量≥3 且血量<25% → 自动打出：全体 47 伤（华丽收场特效）。
    public override async Task BeforeSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner.Creature) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        if (Pile?.Type != PileType.Hand)
        {
            return;
        }

        // PlayerCombatState 只在战斗里存在；这里虽然已经是战斗钩子，仍用 ? 兜一层。
        if (Owner.PlayerCombatState?.Energy is not >= 3 || Owner.Creature.CurrentHp * 4 >= Owner.Creature.MaxHp)
        {
            return;
        }

        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        if (IsUpgraded)
        {
            foreach (var enemy in combatState.HittableEnemies)
            {
                await PowerCmd.Apply<VulnerablePower>(choiceContext, enemy, 1, Owner.Creature, this);
            }
        }

        var finale = NGrandFinaleVfx.Create(Owner.Creature);
        if (finale != null)
        {
            NCombatRoom.Instance?.CombatVfxContainer.AddChildSafely(finale);
            await Cmd.Wait(NGrandFinaleVfx.totalAnticipationDuration);
        }

        await DamageCmd.Attack(47).FromCard(this, null).TargetingAllOpponents(combatState)
            .WithHitVfxNode(NGrandFinaleImpactVfx.Create)
            .WithHitFx(null, null, "blunt_attack.mp3")
            .Execute(choiceContext);

        // 视为自动打出：从手牌进入弃牌堆。
        await CardPileCmd.Add(this, PileType.Discard, CardPilePosition.Random, this);
    }

    protected override void OnUpgrade()
    {
    }
}

/// <summary>
/// 黄金矿工！：0 费技能（稀有·小游戏牌）。消耗弃牌堆中的 1 张牌，并根据其当前耗能触发对应效果：
/// 没有耗能：消耗弃牌堆中与其相邻的牌，如果消耗了没有耗能的牌将再次触发此效果。
/// 0 费牌或 X 费牌：将 1 张巨石+加入你的手牌。
/// 有耗能的牌：获得与其耗能相等的能量并抽等量张牌。消耗（升级：获得保留）。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class GoldMiner : ModCardTemplate
{
    public GoldMiner() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：巨石+ 与效果侧栏（升级前后合并为一条）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_GOLD_MINER.sidebar1")),
        HoverTipFactory.FromCard<GiantRock>(true)
    ];

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    // 小游戏牌（享受小游戏牌增益，侧栏改用小游戏牌侧栏）。
    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var player = Owner.Creature.Player;
        var combatState = Owner.Creature.CombatState;
        if (player == null || combatState == null)
        {
            return;
        }

        var discard = PileType.Discard.GetPile(player);
        var discardCards = discard.Cards.ToList();
        var picked = (await CardSelectCmd.FromCombatPile(choiceContext, discard, player,
            new CardSelectorPrefs(new LocString("card_selection", "TO_EXHAUST"), 1, 1))).FirstOrDefault();
        if (picked == null)
        {
            return;
        }

        var idx = discardCards.IndexOf(picked);
        await CardCmd.Exhaust(choiceContext, picked);

        // 根据**当前**耗能分支（不是卡面印的 Canonical —— 被减费/加费过的牌要按当前值算，
        // 例如「剧情推进！+」升到 0 费就该给巨石+）。
        var cost = picked.EnergyCost.GetWithModifiers(CostModifiers.All);
        var costsX = picked.EnergyCost.CostsX;
        if (picked.Keywords.Contains(CardKeyword.Unplayable))
        {
            // 没有耗费：消耗弃牌堆中与其相邻的牌；若消耗了没有费用的牌则连续触发。
            var exhausted = new HashSet<CardModel> { picked };
            var queue = new Queue<int>();
            if (idx > 0)
            {
                queue.Enqueue(idx - 1);
            }

            if (idx >= 0 && idx < discardCards.Count - 1)
            {
                queue.Enqueue(idx + 1);
            }

            while (queue.Count > 0)
            {
                var i = queue.Dequeue();
                if (i < 0 || i >= discardCards.Count)
                {
                    continue;
                }

                var neighbor = discardCards[i];
                if (exhausted.Contains(neighbor) || neighbor.Pile?.Type != PileType.Discard)
                {
                    continue;
                }

                var wasUnplayable = neighbor.Keywords.Contains(CardKeyword.Unplayable);
                await CardCmd.Exhaust(choiceContext, neighbor);
                exhausted.Add(neighbor);
                if (wasUnplayable)
                {
                    if (i > 0)
                    {
                        queue.Enqueue(i - 1);
                    }

                    if (i < discardCards.Count - 1)
                    {
                        queue.Enqueue(i + 1);
                    }
                }
            }
        }
        else if (costsX || cost <= 0)
        {
            // 0 费牌或 X 费牌：将 1 张巨石+ 加入手牌。
            var rock = combatState.CreateCard(ModelDb.Card<GiantRock>(), Owner);
            CardCmd.Upgrade(rock);
            await CardPileCmd.AddGeneratedCardToCombat(rock, PileType.Hand, Owner);
        }
        else
        {
            // 有耗能的牌：获得与其耗能相等的能量并抽等量张牌。
            await PlayerCmd.GainEnergy(cost, Owner);
            await CardPileCmd.Draw(choiceContext, cost, Owner);
        }
    }

    protected override void OnUpgrade()
    {
        // 升级：获得保留（费用升级前后都是 0）。
        LocalKeywords.Add(CardKeyword.Retain);
    }
}

/// <summary>
/// 终于上一档了！：1 费技能（稀有）。战斗结束后额外获得 20 金币与一组卡牌奖励；
/// 如果下个回合结束前未能结束战斗，则只能额外获得 10 金币。消耗（升级：25 金币 + 卡牌奖励 / 15 金币）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class RankUp : ModCardTemplate
{
    public RankUp() : base(1, CardType.Power, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("GoldFull", 20),    // 升级 25
        new DynamicVar("GoldPartial", 10)  // 升级 15
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 初始 2 层：可维持本回合与下一回合结束（之后掉到二档）。
        await PowerCmd.Apply<RankUpPower>(choiceContext, Owner.Creature, 2, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        EnergyCost.UpgradeBy(-1);
        DynamicVars["GoldFull"].UpgradeValueBy(5);
        DynamicVars["GoldPartial"].UpgradeValueBy(5);
    }
}

[RegisterPower]
public sealed class RankUpPower : ModPowerTemplate
{
    private class Data
    {
        public int GoldFull = 20;     // 升级 25
        public int GoldPartial = 10;  // 升级 15
    }

    public override PowerType Type => PowerType.Buff;

    // 每个实例独立存在（层数 = 剩余可维持回合数，初始 2）。
    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/rank_up_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/rank_up_power.png");

    protected override object InitInternalData() => new Data();

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("GoldFull", 20)
    ];

    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        var upgraded = cardSource?.IsUpgraded == true;
        var data = GetInternalData<Data>();
        data.GoldFull = upgraded ? 25 : 20;
        data.GoldPartial = upgraded ? 15 : 10;
        DynamicVars["GoldFull"].BaseValue = data.GoldFull;
        return Task.CompletedTask;
    }

    // 回合结束时层数 -1；归零时由 AfterRemoved 换成「掉到二档了」。
    public override async Task BeforeSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        await PowerCmd.Decrement(this);
    }

    public override async Task AfterRemoved(Creature oldOwner)
    {
        // 层数归零（或提前移除）→ 换成「掉到二档了」（无层数，只给小量金币）。
        if (oldOwner.CombatState == null)
        {
            return;
        }

        var data = GetInternalData<Data>();
        var weak = await PowerCmd.Apply<FellToSecondTierPower>(new BlockingPlayerChoiceContext(), oldOwner,
            1m, oldOwner, null);
        weak?.SetGold(data.GoldPartial);
    }

    public override Task AfterCombatEnd(CombatRoom room)
    {
        var player = Owner.Player;
        if (player == null)
        {
            return Task.CompletedTask;
        }

        var data = GetInternalData<Data>();
        room.AddExtraReward(player, new GoldReward(data.GoldFull, player));
        room.AddExtraReward(player, new CardReward(
            CardCreationOptions.ForRoom(player, MegaCrit.Sts2.Core.Rooms.RoomType.Monster), 3, player));
        return Task.CompletedTask;
    }
}

/// <summary>掉到二档了：无层数，战斗结束时获得少量金币。</summary>
[RegisterPower]
public sealed class FellToSecondTierPower : ModPowerTemplate
{
    private class Data
    {
        public int Gold = 10;  // 升级 15
    }

    public override PowerType Type => PowerType.Buff;

    public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;

    public override PowerStackType StackType => PowerStackType.Single;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/fell_to_second_tier_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/fell_to_second_tier_power.png");

    protected override object InitInternalData() => new Data();

    // 右下角显示的是「这次实际会给多少金币」，不是层数。
    public override int DisplayAmount => GetInternalData<Data>().Gold;

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Gold", 10)
    ];

    public void SetGold(int gold)
    {
        GetInternalData<Data>().Gold = gold;
        DynamicVars["Gold"].BaseValue = gold;
    }

    public override Task AfterCombatEnd(CombatRoom room)
    {
        var player = Owner.Player;
        if (player != null)
        {
            room.AddExtraReward(player, new GoldReward(GetInternalData<Data>().Gold, player));
        }

        return Task.CompletedTask;
    }
}


