using System.Text.Json;
using System.Text.Json.Nodes;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Models.Capabilities;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 剧情推进！：1 费技能（升级后 0 费），使手牌中构想卡的计数 +1，消耗。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
[RegisterArchaicToothTranscendence(typeof(Cards.DualNarrative))]
public sealed class PlotAdvance : ModCardTemplate
{
    // 注意：初始卡组由 STS2_MomoiCharacter.LocalStartingDeck 提供（含 1 张剧情推进！），
    // 不要再加 [RegisterCharacterStarterCard]，否则会重复。
    public PlotAdvance() : base(1, CardType.Skill, CardRarity.Basic, TargetType.None)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");
    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 构想机制：若手牌中有多张构想，它们的数值将同时变动。
        var hand = Owner.PlayerCombatState?.Hand;
        if (hand != null)
        {
            foreach (var card in hand.Cards.ToList())
            {
                if (card is ConceptCard concept)
                {
                    concept.GetOrCreateCapability<ConceptCounterCapability>().AddCount(1);
                }
            }
        }

        await Task.CompletedTask;
    }

    protected override void OnUpgrade()
    {
        // 升级：费用 1 -> 0。
        base.EnergyCost.UpgradeBy(-1);
    }
}
