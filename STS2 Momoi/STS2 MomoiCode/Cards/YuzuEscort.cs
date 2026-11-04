using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 柚子护航！：2 费能力（罕见）。虚无。
/// 每回合第 1 张小游戏牌将打出 2 次，然后失去 1 点活力。
/// 升级：移除虚无。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class YuzuEscort : ModCardTemplate
{
    public YuzuEscort() : base(2, CardType.Power, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Ethereal };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("YuzuEscort", 1)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<YuzuEscortPower>(choiceContext, Owner.Creature,
            DynamicVars["YuzuEscort"].BaseValue, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        // 移除虚无。
        RemoveKeyword(CardKeyword.Ethereal);
    }
}

/// <summary>
/// 柚子护航能力：每回合第 1 张小游戏牌打出次数 +1（打出 2 次），随后失去 1 点活力。
/// </summary>
[RegisterPower]
public sealed class YuzuEscortPower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/yuzu_escort_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/yuzu_escort_power.png");

    private int _minigamesPlayedThisTurn;

    // 回合开始时重置本回合小游戏牌计数。
    public override Task BeforeSideTurnStart(PlayerChoiceContext choiceContext, CombatSide side,
        IReadOnlyList<Creature> participants, ICombatState combatState)
    {
        if (participants.Contains(Owner))
        {
            _minigamesPlayedThisTurn = 0;
        }

        return Task.CompletedTask;
    }

    // 每回合第 1 张小游戏牌打出次数 +1（打出 2 次）。
    public override int ModifyCardPlayCount(CardModel card, Creature? target, int playCount)
    {
        if (card.Owner?.Creature == Owner && MinigameSupport.IsMinigameCard(card) && _minigamesPlayedThisTurn < Amount)
        {
            return playCount + 1;
        }

        return playCount;
    }

    // 小游戏牌打出后：计数；前 Amount 张小游戏牌都会失去 1 点活力。
    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature == Owner && MinigameSupport.IsMinigameCard(cardPlay.Card)
            && _minigamesPlayedThisTurn < Amount)
        {
            _minigamesPlayedThisTurn++;
            await MinigameSupport.LoseVigor(choiceContext, Owner, cardPlay.Card);
        }
    }
}
