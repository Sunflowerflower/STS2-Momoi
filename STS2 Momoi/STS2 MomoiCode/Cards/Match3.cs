using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 消消乐！：0 费技能（衍生·小游戏牌）。消耗。
/// 选择 1 张牌，再选择任意张与其类型相同的牌：
///   * 不足 3 张 —— 直接消耗；
///   * 不低于 3 张 —— 改为「打出并消耗」（无法打出的牌就直接消耗；能力牌打出后进 Limbo、本来就带消耗的已进消耗堆，
///     这两种都不需要也不能再补一次消耗）；
///   * 超过 3 张 —— 每超出 1 张抽 1 张牌并获得 1 能量。
/// 升级：添加「保留」。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class Match3 : ModCardTemplate
{
    public Match3() : base(1, CardType.Skill, CardRarity.Token, TargetType.None)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.Tag };

    // 消耗：打出后进消耗堆（卡面自动补「消耗。」）。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new EnergyVar(1)  // 超过 3 张时，每超出一张获得的能量
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 第一段：选择 1 张牌作为类型基准（不消耗，仍留在手牌）。
        //
        // ⚠ source 传 null（而不是 this）：NPlayerHand.SelectCards 在选牌结束时会在
        // `AfterCardsSelected(source)` 里把选中的卡从 _selectedHandCardContainer 搬回手牌，
        // 但如果传了 source，这一步会被推后到 **source.ExecutionFinished**（= 本卡整段 OnPlay 结束）才做；
        // 那样在 OnPlay 里紧接着消耗这些卡时：
        //   * 不跳过动画 → 在 MoveCardNodeToNewPileBeforeTween 里撞 "already has a parent"；
        //   * 跳过动画   → 节点永远没被搬走，ExecutionFinished 时又被搬回手牌，变成一张“幽灵牌”。
        // 传 null 会让每次选牌的收尾（OnSelectModeSourceFinished）当场完成，两种问题都没了。
        // （source 在 NPlayerHand 里只用于这个 ExecutionFinished 订阅，传 null 没有其它副作用。）
        var first = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 1),
            null, null)).FirstOrDefault();
        if (first == null)
        {
            return;
        }

        var cardType = first.Type;

        // 第二段：选择任意张同类型牌；第一次选择的牌会一起被处理。
        var rest = (await CardSelectCmd.FromHand(choiceContext, Owner,
            new CardSelectorPrefs(new LocString("cards", "STS2_MOMOI_CARD_MATCH3.pickAny"), 0, 999),
            (CardModel c) => c.Type == cardType, null)).ToList();
        var all = rest.Contains(first) ? rest : rest.Prepend(first).ToList();
        var count = all.Count;

        if (count >= 3)
        {
            // 三消成立：改为「打出并消耗」。
            foreach (var card in all)
            {
                if (CombatManager.Instance.IsOverOrEnding)
                {
                    break;
                }

                // 能打出的先打出（被阻止 / Unplayable 的会走进下面的「直接消耗」）。
                if (AutoPlayProbe.WillActuallyPlay(combatState, card))
                {
                    await CardCmd.AutoPlay(choiceContext, card, null);
                }

                // 只对「还在战斗牌堆里」的牌补一次消耗：
                //   * 本来就是消耗牌 → 打出后已在消耗堆，再消耗一次会找不到对象；
                //   * 能力牌 → 打出后进 Limbo（Pile 为 None），不会也不该被消耗。
                if (card.Pile?.Type is PileType.Hand or PileType.Draw or PileType.Discard or PileType.Play)
                {
                    await CardCmd.Exhaust(choiceContext, card);
                }
            }
        }
        else
        {
            // 不足三消：直接消耗。
            foreach (var card in all)
            {
                await CardCmd.Exhaust(choiceContext, card);
            }
        }

        // 超过 3 张：每超出 1 张抽 1 张牌并获得 1 能量。
        var extra = count - 3;
        if (extra > 0)
        {
            await CardPileCmd.Draw(choiceContext, extra, Owner);
            await PlayerCmd.GainEnergy(extra, Owner);
        }
    }

    // 升级：添加「保留」（卡面会自动补「保留。」）。
    protected override void OnUpgrade()
    {
        // 升级：耗能 1 -> 0（以前升级还给「保留」，2026-10-25 按用户要求去掉）。
        EnergyCost.UpgradeBy(-1);
    }
}
