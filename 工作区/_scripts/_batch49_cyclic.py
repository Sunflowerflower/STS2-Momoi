# -*- coding: utf-8 -*-
"""批次49：把 CyclicNarrative / CyclicNarrativePower 整块替换成「注能 + 回合结束选牌洗回」版本。"""
import io

P = "C:/Users/asus/RiderProjects/STS2 Momoi/STS2 Momoi/STS2 MomoiCode/Cards/NewCardsBatch.cs"
START = "/// <summary>\n/// 循环叙事：1 费技能"
END = "/// <summary>\n/// 王道减费组件"

NEW = '''/// <summary>
/// 循环叙事：1 费技能（罕见）。注能：将这张牌置于你的抽牌堆底，在你的回合开始时自动打出。
/// 打出时：本回合结束时，将弃牌堆的最多 1 张牌洗入你的抽牌堆（升级：0 费）。
/// </summary>
[RegisterCard(typeof(STS2_MomoiCardPool))]
public sealed class CyclicNarrative : ModCardTemplate, IImbuedCard
{
    public CyclicNarrative() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 侧栏：「注能」的解释（和开发者协同：绿 共用同一条词条）。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips => [ImbuedSupport.ImbuedTip];

    // 注能是否已经打出过（同一张牌每场战斗只算一次）。
    private bool _imbuedApplied;

    public override async Task AfterAutoPrePlayPhaseEntered(PlayerChoiceContext choiceContext, Player player)
    {
        if (_imbuedApplied || !ImbuedSupport.CanAutoPlayNow(player, this))
        {
            return;
        }

        _imbuedApplied = true;
        await ImbuedSupport.TryAutoPlayAsync(choiceContext, this, nameof(CyclicNarrative));
    }

    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        // 洗回效果：可叠加，叠层数 = 之后每个回合结束时最多能选的张数。
        await PowerCmd.Apply<CyclicNarrativePower>(choiceContext, Owner.Creature, 1, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
        // 升级：1 费 → 0 费。
        EnergyCost.UpgradeBy(-1);
    }
}

/// <summary>
/// 循环叙事：本回合结束时，将弃牌堆的最多 Amount 张牌洗入你的抽牌堆。
/// 可叠加：叠层数既是剩余回合数，也是每次最多能选的张数（右下角计数器显示的就是它）。
/// </summary>
[RegisterPower]
public sealed class CyclicNarrativePower : ModPowerTemplate
{
    public override PowerType Type => PowerType.Buff;

    public override PowerStackType StackType => PowerStackType.Counter;

    // 右下角计数器 = 每次最多能洗回几张（也就是层数）。
    public override int DisplayAmount => Amount;

    public override PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/cyclic_narrative_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/cyclic_narrative_power.png");

    public override async Task AfterSideTurnEnd(PlayerChoiceContext choiceContext, CombatSide side,
        IEnumerable<Creature> participants)
    {
        if (side != CombatSide.Player || !participants.Contains(Owner) || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        var player = Owner.Player;
        if (player == null)
        {
            return;
        }

        var discard = CardPile.Get(PileType.Discard, player);
        if (discard != null && discard.Cards.Count > 0)
        {
            var amount = (int)Amount;
            var max = amount < discard.Cards.Count ? amount : discard.Cards.Count;
            if (max > 0)
            {
                // 「最多 max 张」：可以跳过不选。MinSelect(0) != MaxSelect 时 CardSelectorPrefs 会强制弹选择界面，
                // 所以即使弃牌堆只有 1 张牌，也会让玩家自己决定要不要洗回去。
                var prefs = new CardSelectorPrefs(
                    new LocString("card_selection", "STS2_MOMOI_CYCLIC_NARRATIVE_HEADER"), 0, max)
                {
                    Cancelable = true
                };

                var selected = (await CardSelectCmd.FromCombatPile(choiceContext, discard, player, prefs)).ToList();
                if (selected.Count > 0)
                {
                    await CardPileCmd.Add(selected, PileType.Draw, CardPilePosition.Random);
                }
            }
        }

        // 结算完再扣剩余回合数，扣到 0 自动消失。
        await PowerCmd.TickDownDuration(this);
    }
}


'''

s = io.open(P, encoding="utf-8").read()
assert s.count(START) == 1, ("START count", s.count(START))
assert s.count(END) == 1, ("END count", s.count(END))
i = s.index(START)
j = s.index(END)
old = s[i:j]
assert "CyclicNarrative" in old and "ShuffleDiscardsEnteredThisTurn" in old, "unexpected block"

s2 = s[:i] + NEW + s[j:]
io.open(P, "w", encoding="utf-8").write(s2)

# 结构自检：花括号平衡 + 旧符号已消失
print("braces", s2.count("{") - s2.count("}"))
print("old helper gone:", "ShuffleDiscardsEnteredThisTurn" not in s2)
print("class count:", s2.count("public sealed class CyclicNarrative"))
print("power refs:", s2.count("CyclicNarrativePower"))
print("lines", len(s2.splitlines()), "was", len(s.splitlines()))
