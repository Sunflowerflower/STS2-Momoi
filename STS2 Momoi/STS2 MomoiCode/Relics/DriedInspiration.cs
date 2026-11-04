using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Entities.Relics;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Nodes.Combat;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using STS2_Momoi.Cards;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Models.Capabilities;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Relics;

/// <summary>
/// 枯竭灵感：回合开始时，若手上没有构想，将一张构想加入手牌（最左边）；
/// 若已有构想，则使其计数 +1（升级后 +2），并按计数将 1 张原版诅咒加入手牌（最右边）：
/// 3 苦恼(Writhe) / 4 睡眠不佳(PoorSleep) / 5 疑虑(Doubt) / 6+ 执迷(Enthralled)。
/// </summary>
[RegisterRelic(typeof(STS2_MomoiRelicPool))]
[RegisterCharacterStarterRelic(typeof(STS2_MomoiCharacter))]
[RegisterTouchOfOrobasRefinement(typeof(Relics.OverflowingInspiration))]
public sealed class DriedInspiration : ModRelicTemplate
{
    public override RelicRarity Rarity => RelicRarity.Starter;

    public override RelicAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png",
        IconOutlinePath: $"{Entry.ResPath}/images/relics/{GetType().Name}_outline.png",
        BigIconPath: $"{Entry.ResPath}/images/relics/{GetType().Name}.png");

    // 侧栏：预览「构想」这张衍生牌。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [HoverTipFactory.FromCard<ConceptCard>()];

    // 局内生成小游戏牌（不含 fullgame 游戏牌）时播放。
    public override Task AfterCardGeneratedForCombat(CardModel card, Player? creator)
    {
        if (creator == Owner && MinigameSupport.CanBeTemporarilyAdded(card))
        {
            Audio.MomoiAudio.PlayVoice(Audio.MomoiSfx.MinigameGenerated);
        }

        return Task.CompletedTask;
    }

    public override async Task AfterPlayerTurnStart(PlayerChoiceContext choiceContext, Player player)
    {
        // 多人模式：这个钩子会对所有玩家的回合开始都触发一次，遗物只服务它自己的主人。
        // 没有这一行的话，队友的回合开始也会给他塞一张构想（Bug：小桃的初始遗物会服务所有玩家）。
        if (player != Owner)
        {
            return;
        }

        // 战斗中生成卡必须走 CombatState，否则卡无法进入战斗牌堆/打出。
        var combatState = player.Creature.CombatState;
        var hand = player.PlayerCombatState?.Hand;
        if (combatState == null || hand == null)
        {
            return;
        }

        // 初始遗物只负责添加构想（数值增长与诅咒添加为构想自身效果）。
        if (!hand.Cards.Any(c => c is ConceptCard))
        {
            var newConcept = combatState.CreateCard(ModelDb.Card<ConceptCard>(), player);
            await CardPileCmd.AddGeneratedCardToCombat(newConcept, PileType.Hand, player, CardPilePosition.Top);
        }
    }
}
