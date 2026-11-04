using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Powers;
using MegaCrit.Sts2.Core.Models.Relics;
using MegaCrit.Sts2.Core.Nodes.CommonUi;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Models.Capabilities;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

// ===================================================================
// 序章：0 费技能（罕见）。固有；当前每有一名敌人，就使构想数值 +1。消耗（升级：删去消耗）。
// ===================================================================
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Prologue : ModCardTemplate
{
    public Prologue() : base(0, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 固有升级前后都有；消耗只有未升级时有（升级后删掉）。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Innate, CardKeyword.Exhaust };

    // 衍生牌预览：构想。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<ConceptCard>()
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        var enemies = combatState.HittableEnemies.Count();
        if (enemies <= 0)
        {
            return;
        }

        // 每有一名敌人，手牌中所有构想数值 +1。
        await ConceptCounterCapability.AddCountToAllInHand(choiceContext, Owner.Creature, enemies);
    }

    protected override void OnUpgrade()
    {
        // 升级：删去消耗（固有升级前后都有）。
        LocalKeywords.Remove(CardKeyword.Exhaust);
    }
}

// ===================================================================
// 整活：1 费技能（罕见）。抽 2（升级 3）张牌；选择其中 1 张，将其变化为随机小游戏牌（升级后为升级版）。
// ===================================================================
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Slapstick : ModCardTemplate
{
    public Slapstick() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Cards", 2)  // 升级 3
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var drawn = (await CardPileCmd.Draw(choiceContext, DynamicVars["Cards"].IntValue, Owner)).ToList();
        var combatState = Owner.Creature.CombatState;
        if (combatState == null || drawn.Count == 0)
        {
            return;
        }

        // 只能选择本次抽到的牌。
        var picked = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 1, 1),
            c => drawn.Contains(c), this)).FirstOrDefault();
        if (picked == null)
        {
            return;
        }

        var replacement = MinigameSupport.CreateRandomMinigameCard(combatState, Owner, IsUpgraded);
        CombatStats.RecordMinigameObtained(replacement);
        await CardCmd.Transform(picked, replacement);
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Cards"].UpgradeValueBy(1);
    }
}

// ===================================================================
// 超级玛丽：0 费技能（衍生·小游戏）。将一张随机「蘑菇」加入手牌，本回合可以免费打出；
// 有 1/256 的概率改为获得遗物「大蘑菇」。消耗。
// ===================================================================
[RegisterCard(typeof(TokenCardPool))]
public sealed class SuperMario : ModCardTemplate
{
    /// <summary>「蘑菇」卡池（原版各职业的强力卡）。</summary>
    private static readonly Type[] Mushrooms =
    [
        typeof(Mangle), typeof(DaggerSpray), typeof(GrandFinale), typeof(PhotonCut), typeof(GuidingStar),
        typeof(DyingStar), typeof(CaptureSpirit), typeof(Chill), typeof(HelixDrill), typeof(Hyperbeam)
    ];

    public SuperMario() : base(0, CardType.Skill, CardRarity.Token, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    // 侧栏：蘑菇卡池说明。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_SUPER_MARIO.sidebar"))
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 1/256：不获得卡牌，改为获得遗物「大蘑菇」。
        if (Owner.RunState.Rng.CombatCardGeneration.NextInt(256) == 0)
        {
            await RelicCmd.Obtain<BigMushroom>(Owner);
            return;
        }

        var type = Owner.RunState.Rng.CombatCardSelection.NextItem(Mushrooms) ?? Mushrooms[0];
        var mushroom = combatState.CreateCard((CardModel)ModelDb.Get(type), Owner);
        if (IsUpgraded)
        {
            CardCmd.Upgrade(mushroom);
        }

        await CardPileCmd.AddGeneratedCardToCombat(mushroom, PileType.Hand, Owner);

        // 本回合可以免费打出（SetToFreeThisTurn 内部同时清零能量与辉星费用）。
        mushroom.SetToFreeThisTurn();
    }

    protected override void OnUpgrade()
    {
    }
}
