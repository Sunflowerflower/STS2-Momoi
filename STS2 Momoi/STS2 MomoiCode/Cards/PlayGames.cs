using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Nodes.CommonUi;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 打游戏！：第二张初始牌。1 费技能（普通，升级后 0 费）。
/// 将一张随机小游戏牌添加到手牌（升级后为升级版），失去 1 点活力。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class PlayGames : ModCardTemplate
{
    public PlayGames() : base(1, CardType.Skill, CardRarity.Basic, TargetType.None)
    {
    }

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 随机选一张小游戏牌并在战斗中生成。
        var type = MinigameSupport.PickRandomMinigame(Owner.RunState.Rng.CombatCardGeneration);
        var model = ModelDb.AllCards.First(c => c.GetType() == type);
        var card = combatState.CreateCard(model, Owner);

        // 升级后：生成升级版。
        if (IsUpgraded)
        {
            CardCmd.Upgrade(card, CardPreviewStyle.None);
        }

        // 记录获得（游戏王形态/拾遗的去重依据）。
        CombatStats.RecordMinigameObtained(card);
        await CardPileCmd.AddGeneratedCardToCombat(card, PileType.Hand, Owner, CardPilePosition.Top);

        // 失去 1 点活力（活力为 0 时保持 0）。
        await MinigameSupport.LoseVigor(choiceContext, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        // 升级：耗能 1 -> 0（其余效果不变：加入的小游戏牌为升级版，见 OnPlay）。
        base.EnergyCost.UpgradeBy(-1);
    }
}
