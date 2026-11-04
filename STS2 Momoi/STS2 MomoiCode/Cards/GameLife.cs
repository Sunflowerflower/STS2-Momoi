using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Nodes.CommonUi;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using MegaCrit.Sts2.Core.ValueProps;
using STS2_Momoi.Characters;
using STS2RitsuLib.CardTags;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;
using STS2_Momoi.Diagnostics;

namespace STS2_Momoi.Cards;

/// <summary>
/// 游戏人生：1 费攻击（罕见）。造成 9 点伤害；为一张手牌添加「游戏牌」标签
/// （升级：12 点伤害，且连同它的所有同名牌一起添加）。
/// 只给**本场战斗里的这张牌**加标签（不写回牌组本尊），因此效果只持续这一场战斗。
/// 「已经是游戏牌或小游戏牌的牌不会进入选择界面」；本牌自己不是游戏牌/小游戏牌，也可以被自己添加。
/// 描述顶行的金色「游戏牌。」由 Patches.CardKeywordLabelPatch 按标签自动带上。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class GameLife : ModCardTemplate
{
    public GameLife() : base(1, CardType.Attack, CardRarity.Uncommon, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new CalculationBaseVar(9m),   // 升级 12
        new ExtraDamageVar(0m),
        new CalculatedDamageVar(ValueProp.Move).WithMultiplier((_, _) => 0m)
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var target = cardPlay.Target;
        if (target != null)
        {
            await DamageCmd.Attack(DynamicVars.CalculatedDamage)
                .FromCard(this, cardPlay)
                .Targeting(target)
                .Execute(choiceContext);
        }

        var hand = CardPile.Get(PileType.Hand, Owner);
        if (hand == null)
        {
            return;
        }

        // 已经是游戏牌 / 小游戏牌的牌不进入选择界面；没有可选牌就直接跳过（伤害已结算）。
        var options = hand.Cards.Where(c => !MinigameSupport.IsMinigameCard(c)).ToList();
        if (options.Count == 0)
        {
            return;
        }

        var picked = await SelectHandCard(choiceContext);
        if (picked == null)
        {
            return;
        }

        // 给选中的牌加标记（升级：连同它的所有同名牌）。
        ApplyGameCardLabel(picked);
        if (IsUpgraded)
        {
            ApplyToSameNameCards(picked);
        }
    }

    /// <summary>
    /// 选手牌。异常只能在这里兜：
    /// 若选牌界面开着时场景被拆掉（QuickRestart / 读档 / 退出到主菜单），
    /// 原版 <c>CardSelectCmd.FromHand</c> 会把“空选择”发给 <c>PlayerChoiceSynchronizer.SyncLocalChoice</c>，
    /// 而那时 <c>NetCombatCard.FromModel</c> 已经找不到那张牌 → 招 <c>ArgumentOutOfRangeException</c>（日志 20261020-152615）。
    /// 这不是本卡特有的，但本卡用了手牌选择，所以自己兜住：战斗都没了，标签也不需要加。
    /// </summary>
    private async Task<CardModel?> SelectHandCard(PlayerChoiceContext choiceContext)
    {
        IEnumerable<CardModel> selection;
        try
        {
            selection = await CardSelectCmd.FromHand(choiceContext, Owner,
                new CardSelectorPrefs(new LocString("gameplay_ui", "CHOOSE_CARD_HEADER"), 1) { Cancelable = true },
                c => !MinigameSupport.IsMinigameCard(c), this);
        }
        catch (Exception ex) when (ex is ArgumentOutOfRangeException or InvalidOperationException)
        {
            MomoiDiag.Log($"[GameLife] selection aborted (scene teardown?): {ex.GetType().Name}");
            return null;
        }

        return selection.FirstOrDefault();
    }

    /// <summary>给一张牌打上「游戏牌」标记（**只作用于本场战斗**，不写卡的标签集合），并刷新手牌卡面让顶行文本立刻出现。</summary>
    private void ApplyGameCardLabel(CardModel card)
    {
        // 注意：不要用 AddModCardTag —— 战斗克隆体的 _tags 与牌组本尊共用，会污染存档（见 MinigameSupport 里的注释）。
        MinigameSupport.MarkTemporaryGameCard(card);
        NCombatRoom.Instance?.Ui.Hand?.GetCard(card)?.UpdateVisuals(PileType.Hand, CardPreviewMode.Normal);
    }

    /// <summary>升级版：本场战斗中同名牌（手牌 / 抽牌堆 / 弃牌堆）一起加标签（不涉及牌组本尊）。</summary>
    private void ApplyToSameNameCards(CardModel picked)
    {
        var entry = picked.Id.Entry;

        foreach (var pileType in new[] { PileType.Hand, PileType.Draw, PileType.Discard })
        {
            var pile = CardPile.Get(pileType, Owner);
            if (pile == null)
            {
                continue;
            }

            foreach (var card in pile.Cards.Where(c => c != picked && c.Id.Entry == entry).ToList())
            {
                ApplyGameCardLabel(card);
            }
        }
    }

    protected override void OnUpgrade()
    {
        DynamicVars.CalculationBase.UpgradeValueBy(3);   // 9 -> 12
    }
}
