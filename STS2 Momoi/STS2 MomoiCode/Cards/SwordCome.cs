using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 剑来！：1 费技能（普通）。获得 1 层火力；将弃牌堆中的一张攻击牌放入你的手牌并使其本回合耗能-1。消耗
/// （升级：2 火力、不再消耗）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class SwordCome : ModCardTemplate
{
    public SwordCome() : base(1, CardType.Skill, CardRarity.Common, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar("Firepower", 1),      // 升级 2
        new EnergyVar("CostReduce", 1)      // 回收的攻击牌本回合耗能-1（能量图标）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature, DynamicVars["Firepower"].IntValue, Owner.Creature, this);

        var player = Owner.Creature.Player;
        if (player == null)
        {
            return;
        }

        // 将弃牌堆中的一张攻击牌放入手牌并使其本回合耗能-1（升级：先升级该牌）。
        var discard = PileType.Discard.GetPile(player);
        if (discard.Cards.Count > 0)
        {
            var picked = (await CardSelectCmd.FromCombatPile(choiceContext, discard, player,
                new CardSelectorPrefs(new LocString("card_selection", "TO_ADD_TO_HAND"), 1, 1),
                c => c.Type == CardType.Attack)).FirstOrDefault();
            if (picked != null)
            {
                if (IsUpgraded)
                {
                    CardCmd.Upgrade(picked);
                }

                await CardPileCmd.Add(picked, PileType.Hand, CardPilePosition.Random, this);
                // 文案是「使其本回合耗能减少 1c」→ 用 AddThisTurnOrUntilPlayed：
                // AddUntilPlayed 只在“被打出”时清理，没打出去会留到下一回合。
                picked.EnergyCost.AddThisTurnOrUntilPlayed(-1, reduceOnly: true);
            }
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars["Firepower"].UpgradeValueBy(1);
        LocalKeywords.Remove(CardKeyword.Exhaust);
    }
}
