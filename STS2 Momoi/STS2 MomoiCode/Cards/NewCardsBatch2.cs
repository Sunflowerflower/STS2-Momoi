using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models.Powers;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 堕落：0 费技能（罕见）。给予自身 1 层脆弱和 1 层虚弱；将一张随机小游戏牌加入你的手牌。
/// 升级：改为加入升级版的小游戏牌（脆弱/虚弱层数不变）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class Depravity : ModCardTemplate
{
    public Depravity() : base(0, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 给予自身 1 层脆弱、1 层虚弱（升级前后都加，升级差异只在加入的小游戏牌是否为升级版）。
        await PowerCmd.Apply<FrailPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
        await PowerCmd.Apply<WeakPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);

        // 将一张随机小游戏牌加入你的手牌（升级后为升级版）。
        var card = MinigameSupport.CreateRandomMinigameCard(combatState, Owner, IsUpgraded);
        CombatStats.RecordMinigameObtained(card);
        await CardPileCmd.AddGeneratedCardToCombat(card, PileType.Hand, Owner, CardPilePosition.Top);
    }

    protected override void OnUpgrade()
    {
        // 升级差异体现在加入的小游戏牌是否为升级版（见 OnPlay 的 IsUpgraded 分支）。
    }
}

/// <summary>
/// 王不见王：1 费技能（罕见）。获得 1 层缓冲；你在接下来的 1 回合内无法再从卡牌中获得格挡。
/// 「无法获得格挡」与原版无色技能「应急按钮」使用同一个 NoBlockPower。
/// 升级：耗能 1 -> 0。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class KingsNeverMeet : ModCardTemplate
{
    public KingsNeverMeet() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Turns", 1)  // 无法从卡牌中获得格挡的回合数（暂不随升级变化）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 1 层缓冲。
        await PowerCmd.Apply<BufferPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);

        // 接下来的 N 回合无法从卡牌中获得格挡（与原版应急按钮同一 power）。
        await PowerCmd.Apply<NoBlockPower>(choiceContext, Owner.Creature, DynamicVars["Turns"].BaseValue, Owner.Creature, this);
    }

    // 消耗（升级后删去）。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override void OnUpgrade()
    {
        // 升级：删去消耗（费用升级前后都是 1）。
        RemoveKeyword(CardKeyword.Exhaust);
    }
}
