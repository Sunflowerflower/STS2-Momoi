using MegaCrit.Sts2.Core.CardSelection;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Cards;
using STS2_Momoi.Characters;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 机会难得，选红色！：1 费技能（稀有）。从 3 张其他角色的红色牌中选择 1 张加入你的手牌，
/// 这张牌在本场战斗中可以被免费打出。消耗（升级：升级过的红色牌）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class PickRed : ModCardTemplate
{
    /// <summary>其他角色的红色牌（侧栏说明中的完整列表）。</summary>
    private static readonly Type[] RedCards =
    [
        // 铁甲战士
        typeof(MoltenFist), typeof(TwinStrike), typeof(Cinder), typeof(BloodWall), typeof(InfernalBlade),
        typeof(EvilEye), typeof(FlameBarrier), typeof(Conflagration), typeof(CrimsonMantle), typeof(Pyre), typeof(DemonForm),
        // 静默猎手
        typeof(Suppress), typeof(FanOfKnives), typeof(BulletTime), typeof(Murder),
        // 储君
        typeof(Bombardment), typeof(CrashLanding),
        // 亡灵契约师
        typeof(EndOfDays), typeof(Deathbringer), typeof(Corruption), typeof(Fear),
        // 故障机器人
        typeof(CreativeAi), typeof(Overclock), typeof(Shatter), typeof(Refract), typeof(Sunder),
        typeof(Synthesis), typeof(Null), typeof(BeamCell),
        // 无色牌
        typeof(Volley), typeof(Stratagem), typeof(Rend), typeof(Calamity),
        // 先古牌
        typeof(BrightestFlame), typeof(Whistle), typeof(Relax), typeof(Break)
    ];

    public PickRed() : base(1, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Exhaust };

    // 侧栏：解释红色牌。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_PICK_RED.sidebar"))
    ];

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var combatState = Owner.Creature.CombatState;
        if (combatState == null)
        {
            return;
        }

        // 从 2 张随机红色牌中选择 1 张。
        var options = new List<CardModel>();
        var used = new HashSet<string>();
        while (options.Count < 2 && used.Count < RedCards.Length)
        {
            var type = Owner.RunState.Rng.CombatCardSelection.NextItem(RedCards) ?? RedCards[0];
            if (!used.Add(((CardModel)ModelDb.Get(type)).Id.Entry))
            {
                continue;
            }

            var card = combatState.CreateCard((CardModel)ModelDb.Get(type), Owner);
            if (IsUpgraded)
            {
                CardCmd.Upgrade(card);
            }

            options.Add(card);
        }

        var picked = await CardSelectCmd.FromChooseACardScreen(choiceContext, options, Owner);
        if (picked != null)
        {
            // 本场战斗免费打出（打出一次后恢复原耗费）。
            picked.EnergyCost.SetUntilPlayed(0);
            await CardPileCmd.AddGeneratedCardToCombat(picked, PileType.Hand, Owner);
        }
    }

    protected override void OnUpgrade()
    {
    }
}
