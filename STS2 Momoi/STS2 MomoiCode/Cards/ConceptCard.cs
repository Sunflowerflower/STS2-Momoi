using System.Text.Json;
using System.Text.Json.Nodes;
using MegaCrit.Sts2.Core.Commands;
using MegaCrit.Sts2.Core.Combat;
using MegaCrit.Sts2.Core.Context;
using MegaCrit.Sts2.Core.Entities.Creatures;
using MegaCrit.Sts2.Core.Nodes.Rooms;
using MegaCrit.Sts2.Core.Entities.Players;
using MegaCrit.Sts2.Core.Entities.Cards;
using MegaCrit.Sts2.Core.GameActions.Multiplayer;
using MegaCrit.Sts2.Core.HoverTips;
using MegaCrit.Sts2.Core.Localization;
using MegaCrit.Sts2.Core.Nodes.CommonUi;
using MegaCrit.Sts2.Core.Localization.DynamicVars;
using MegaCrit.Sts2.Core.Models;
using MegaCrit.Sts2.Core.Models.CardPools;
using MegaCrit.Sts2.Core.Models.Cards;
using MegaCrit.Sts2.Core.Models.Powers;
using STS2RitsuLib.Interop.AutoRegistration;
using STS2RitsuLib.Models.Capabilities;
using STS2RitsuLib.Scaffolding.Content;

namespace STS2_Momoi.Cards;

/// <summary>
/// 构想：0 费技能，保留 + 消耗。
/// 注册在原版 TokenCardPool（与巨石/小刀/君王之剑/灵魂/燃料同池）：
/// 不进任何卡牌奖励/商店掉落，只能由遗物或其他牌生成。
/// 计数由 <see cref="ConceptCounterCapability"/> 存储在卡实例上，并同步到卡面 DynamicVar 实时显示。
/// 遗物「枯竭灵感」在每回合开始时递增（升级后 +2）并依计数塞入原版诅咒。
/// 打出时按当前计数：摸牌、获得能量、获得活力。
/// </summary>
[RegisterCard(typeof(TokenCardPool))]
public sealed class ConceptCard : ModCardTemplate
{
    public ConceptCard() : base(0, CardType.Skill, CardRarity.Token, TargetType.None)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 侧栏：根据构想数值获得对应诅咒。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_CARD_CONCEPT_CARD.sidebarCurse"))
    ];

    // 保留：回合结束不弃掉；消耗：打出后进消耗堆。
    public override HashSet<CardKeyword> CanonicalKeywords => new() { CardKeyword.Retain, CardKeyword.Exhaust };

    // 升级后每回合计数 +2（由遗物按升级等级判断），卡本身没有其它数值变化。
    public override int MaxUpgradeLevel => 1;

    // 卡面实时显示的数值：计数 / 摸牌数 / 能量 / 活力（由 capability 同步更新）。
    // 用专用变量而不是普通 DynamicVar：普通 DynamicVar 的 PreviewValue 会被
    // NCard.UpdateText → DynamicVars.ClearPreview()（= ResetToBase）打回 BaseValue，
    // 所以必须像原版 BlockVar / CalculatedDamageVar 那样在 UpdateCardPreview 里现算。
    protected override IEnumerable<DynamicVar> CanonicalVars =>
    [
        new ConceptCountVar("ConceptCount"),
        new ConceptCountVar("ConceptDraw"),
        new ConceptEnergyVar(),
        new ConceptCountVar("ConceptVigor")
    ];

    // 回合开始（抽牌结束）后：数值 +1（升级 +2），并按自身数值添加特定诅咒（构想的被动是自身效果）。
    public override async Task AfterPlayerTurnStart(PlayerChoiceContext choiceContext, Player player)
    {
        if (player != Owner || CombatManager.Instance.IsOverOrEnding)
        {
            return;
        }

        if (Pile?.Type != PileType.Hand)
        {
            return;
        }

        var cap = this.GetOrCreateCapability<ConceptCounterCapability>();
        cap.AddCount(IsUpgraded ? 2 : 1);

        var curseType = cap.Count switch
        {
            >= 6 => typeof(Enthralled),
            5 => typeof(Doubt),
            4 => typeof(PoorSleep),
            3 => typeof(Writhe),
            _ => null
        };

        if (curseType != null)
        {
            var curse = Owner.Creature.CombatState?.CreateCard((CardModel)ModelDb.Get(curseType), Owner);
            if (curse != null)
            {
                await CardPileCmd.AddGeneratedCardToCombat(curse, PileType.Hand, Owner);
            }
        }

        NCombatRoom.Instance?.Ui.Hand?.GetCard(this)?.UpdateVisuals(PileType.Hand, CardPreviewMode.Normal);
    }

    // 打出：摸 {计数} 张牌、获得 {计数} 点能量、获得 {计数} 点活力。
    protected override async Task OnPlay(PlayerChoiceContext choiceContext, CardPlay cardPlay)
    {
        var count = this.GetOrCreateCapability<ConceptCounterCapability>().Count;
        if (count <= 0)
        {
            return;
        }

        if (LocalContext.IsMe(Owner))
        {
            VfxCmd.PlayFullScreenInCombat("vfx/vfx_adrenaline", Owner.Creature);
        }

        await CardPileCmd.Draw(choiceContext, count, Owner);
        await PlayerCmd.GainEnergy(count, Owner);
        await PowerCmd.Apply<VigorPower>(choiceContext, Owner.Creature, count, Owner.Creature, this);
    }

    protected override void OnUpgrade()
    {
    }

    // 创建实例时就把计数器挂上，保证遗物/其它牌随时可读写。
    public override void AfterCreated()
    {
        base.AfterCreated();
        this.GetOrCreateCapability<ConceptCounterCapability>();
    }
}

/// <summary>
/// 构想计数组件：持久化计数，并把计数同步到卡面 DynamicVar（{ConceptCount} 等）实时显示。
/// </summary>
[RegisterModelCapability]
public sealed class ConceptCounterCapability : CardCapability
{
    /// <summary>查询手牌中所有构想的最大数值（多张构想取最大值）。</summary>
    public static int GetMaxCountInHand(Creature creature)
    {
        var player = creature.Player;
        if (player == null)
        {
            return 0;
        }

        int max = 0;
        foreach (var card in CardPile.Get(PileType.Hand, player)?.Cards ?? Enumerable.Empty<CardModel>())
        {
            if (card is ConceptCard concept)
            {
                max = Math.Max(max, concept.GetOrCreateCapability<ConceptCounterCapability>().Count);
            }
        }

        return max;
    }

    /// <summary>手牌中所有构想计数 +1（瓶颈突破：全部+1）。</summary>
    public static async Task AddCountToAllInHand(PlayerChoiceContext ctx, Creature creature, int delta)
    {
        var player = creature.Player;
        if (player == null)
        {
            return;
        }

        foreach (var card in CardPile.Get(PileType.Hand, player)?.Cards ?? Enumerable.Empty<CardModel>().ToList())
        {
            if (card is ConceptCard concept)
            {
                concept.GetOrCreateCapability<ConceptCounterCapability>().AddCount(delta);
                NCombatRoom.Instance?.Ui.Hand?.GetCard(card)?.UpdateVisuals(PileType.Hand, CardPreviewMode.Normal);
            }
        }
    }

    /// <summary>手牌中所有构想计数 -1（王道）：任一构想数值 ≥1 即视为成功。</summary>
    public static bool SpendOneFromAllInHand(Creature creature)
    {
        var player = creature.Player;
        if (player == null)
        {
            return false;
        }

        bool any = false;
        foreach (var card in CardPile.Get(PileType.Hand, player)?.Cards ?? Enumerable.Empty<CardModel>().ToList())
        {
            if (card is not ConceptCard)
            {
                continue;
            }

            var cap = card.GetOrCreateCapability<ConceptCounterCapability>();
            if (cap.Count < 1)
            {
                continue;
            }

            cap.AddCount(-1);
            NCombatRoom.Instance?.Ui.Hand?.GetCard(card)?.UpdateVisuals(PileType.Hand, CardPreviewMode.Normal);
            any = true;
        }

        return any;
    }

    public int Count { get; private set; }

    /// <summary>手牌中数值最高的一张构想计数 -1（王道）；失败返回 false。会同步卡面显示。</summary>
    public static bool SpendOneFromHand(Creature creature)
    {
        var player = creature.Player;
        if (player == null)
        {
            return false;
        }

        ConceptCounterCapability? best = null;
        CardModel? bestCard = null;
        foreach (var card in CardPile.Get(PileType.Hand, player)?.Cards ?? Enumerable.Empty<CardModel>())
        {
            if (card is not ConceptCard)
            {
                continue;
            }

            var cap = card.GetOrCreateCapability<ConceptCounterCapability>();
            if (cap.Count < 1)
            {
                continue;
            }

            if (best == null || cap.Count > best.Count)
            {
                best = cap;
                bestCard = card;
            }
        }

        if (best == null)
        {
            return false;
        }

        best.AddCount(-1);
        if (bestCard != null)
        {
            NCombatRoom.Instance?.Ui.Hand?.GetCard(bestCard)?.UpdateVisuals(PileType.Hand, CardPreviewMode.Normal);
        }

        return true;
    }

    public void AddCount(int delta)
    {
        Count += delta;
        SyncDisplayVars();
    }
    /// <summary>直接把计数设为指定值（方案回退 / 严守截稿日）。</summary>
    public void SetCount(int value)
    {
        Count = Math.Max(0, value);
        SyncDisplayVars();
    }

    // 把当前计数同步到卡实例的 DynamicVar，卡面描述渲染时读取。颜色规则（对照原版）：
    //   * BaseValue 固定 0，真正的值在 ConceptCountVar.UpdateCardPreview 里写进 PreviewValue；
    //   * 原版 ToHighlightedString 比较 PreviewValue 与 EnchantedValue（= BaseValue = 0）
    //     → 数值 0 时白色、≥1 时绿色；
    //   * 能量走 EnergyIconsFormatter：1~3 直接堆叠图标（无数字），4 及以上才出数字并跟着变绿。
    private void SyncDisplayVars()
    {
        if (Owner is not CardModel card)
        {
            return;
        }

        foreach (var name in new[] { "ConceptCount", "ConceptDraw", "Energy", "ConceptVigor" })
        {
            card.DynamicVars[name].ResetToBase();
        }
    }

    protected override JsonNode? SaveAdditionalState() => JsonSerializer.SerializeToNode(Count);

    protected override void LoadAdditionalState(JsonNode? state, int schemaVersion)
    {
        Count = state?.Deserialize<int>() ?? 0;
        SyncDisplayVars();
    }
}

/// <summary>
/// 构想计数显示变量：<c>BaseValue</c> 固定 0，"当前计数"在卡面预览阶段现算进 <c>PreviewValue</c>。
/// 必须走 <see cref="DynamicVar.UpdateCardPreview"/>：NCard.UpdateText 每次渲染前都会先
/// <c>Model.DynamicVars.ClearPreview()</c>（= ResetToBase，把 PreviewValue 打回 BaseValue），
/// 在别处写 PreviewValue 会被冲掉（这就是"数值一直是 0"的原因）。
/// 原版 HighlightDifferencesFormatter（{X:diff()}）与 EnergyIconsFormatter 都是比较
/// PreviewValue 与 EnchantedValue 来决定染不染绿，所以 0 白、≥1 绿就自然成立。
/// </summary>
public sealed class ConceptCountVar : DynamicVar
{
    public ConceptCountVar(string name) : base(name, 0m)
    {
    }

    public override void UpdateCardPreview(CardModel card, CardPreviewMode previewMode, Creature? target,
        bool runGlobalHooks)
    {
        PreviewValue = ReadCount(card);
    }

    internal static int ReadCount(CardModel card)
        => card.TryGetCapability<ConceptCounterCapability>(out var capability) ? capability.Count : 0;
}

/// <summary>同上，供 <c>{Energy:energyIcons()}</c> 用（1~3 堆叠图标、4+ 才出绿数字）。</summary>
public sealed class ConceptEnergyVar : EnergyVar
{
    public ConceptEnergyVar() : base("Energy", 0)
    {
    }

    public override void UpdateCardPreview(CardModel card, CardPreviewMode previewMode, Creature? target,
        bool runGlobalHooks)
    {
        PreviewValue = ConceptCountVar.ReadCount(card);
    }
}
