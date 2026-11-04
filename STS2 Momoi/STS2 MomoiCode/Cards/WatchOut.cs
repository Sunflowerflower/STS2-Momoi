using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Entities.Powers;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.Powers;
using STS2_Momoi.Characters;
using STS2_Momoi.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 当心误射！：2 费技能（罕见）。
/// 获得 2 层火力（升级 3）；下 1 张攻击牌变为 0 费；
/// 下 3 次打出攻击牌后，随机将抽牌堆的 1 张攻击牌加入手牌（升级后为升级版）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class WatchOut : ModCardTemplate
{
    public WatchOut() : base(2, CardType.Power, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new DynamicVar("Firepower", 2),  // 火力层数（升级 3）
        new EnergyVar("NextCost", 0)     // 下一张攻击牌耗能变为 0（能量图标）
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        Audio.MomoiAudio.PlayVoice(Audio.MomoiSfx.WatchOutVoice);
        // 获得火力。
        await PowerCmd.Apply<FirepowerPower>(choiceContext, Owner.Creature,
            DynamicVars["Firepower"].BaseValue, Owner.Creature, this);

        // 下 1 张攻击牌变为 0 费（原版 FreeAttackPower 机制）。
        await PowerCmd.Apply<FreeAttackPower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);

        // 下 3 次打出攻击牌后，随机抽一张抽牌堆的攻击牌入手。
        await PowerCmd.Apply<WatchOutPower>(choiceContext, Owner.Creature, 3, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        // 升级后费用 2 -> 1。
        EnergyCost.UpgradeBy(-1);
        DynamicVars["Firepower"].UpgradeValueBy(1);
    }
}

/// <summary>
/// 当心误射的计数效果：每次打出攻击牌时，随机将抽牌堆的 1 张攻击牌加入手牌（升级后为升级版），
/// 然后层数 -1；层数归零后效果结束。
/// </summary>
[RegisterPower]
public sealed class WatchOutPower : ModPowerTemplate
{
    private class Data
    {
        public bool UpgradeGenerated;
    }

    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;

    protected override object InitInternalData() => new Data();

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/watch_out_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/watch_out_power.png");

    // 记录来源卡是否升级（决定抽到的攻击牌是否升级）。
    public override Task AfterApplied(Creature? applier, CardModel? cardSource)
    {
        GetInternalData<Data>().UpgradeGenerated = cardSource?.IsUpgraded == true;
        return Task.CompletedTask;
    }

    public override async Task AfterCardPlayed(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        if (cardPlay.Card.Owner?.Creature != Owner || cardPlay.Card.Type != CardType.Attack)
        {
            return;
        }

        if (CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        // 每次打出攻击牌：随机将抽牌堆的 1 张攻击牌加入手牌。
        var player = Owner.Player;
        if (player != null)
        {
            var attacks = PileType.Draw.GetPile(player).Cards
                .Where(c => c.Type == CardType.Attack)
                .ToList();
            var card = attacks.Count > 0
                ? player.RunState.Rng.CombatCardSelection.NextItem(attacks)
                : null;
            if (card != null)
            {
                if (GetInternalData<Data>().UpgradeGenerated)
                {
                    CardCmd.Upgrade(card);
                }

                await CardPileCmd.Add(card, PileType.Hand, CardPilePosition.Random, this, false);
            }
        }

        await PowerCmd.Decrement(this);
    }
}
