# -*- coding: utf-8 -*-
import os
BASE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(BASE, 'STS2 MomoiCode')

SIDEBAR = '''
    // 游戏牌侧栏。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_GAME_CARD_SIDEBAR"))
    ];'''

def fix(path, wrong_cls_list, insert_map):
    s = open(path, encoding='utf-8').read()
    # 1) 删除误插（若该类本不该有侧栏）
    for cls in wrong_cls_list:
        anchor = 'public sealed class %s : ModCardTemplate' % cls
        i = s.find(anchor)
        if i < 0:
            continue
        j = s.find(SIDEBAR, i)
        if j < 0:
            continue
        # 删除这段侧栏
        s = s[:j] + s[j + len(SIDEBAR):]
    # 2) 正确插入
    for cls, unique_anchor in insert_map.items():
        anchor = unique_anchor
        if anchor not in s:
            print('MISS anchor', path, cls)
            continue
        s = s.replace(anchor, anchor + SIDEBAR, 1)
    open(path, 'w', encoding='utf-8').write(s)

fix(os.path.join(C, 'Cards', 'RemainingCards2.cs'),
    ['MomentumBreak'],
    {
        'FishingMaster': '''public sealed class FishingMaster : ModCardTemplate
{
    protected override bool HasEnergyCostX => true;

    public FishingMaster() : base(0, CardType.Attack, CardRarity.Rare, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：渔获。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<Catch>(IsUpgraded)
    ];''',
        'FightingGame': '''public sealed class FightingGame : ModCardTemplate
{
    protected override bool HasEnergyCostX => true;

    public FightingGame() : base(0, CardType.Attack, CardRarity.Rare, TargetType.AnyEnemy)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    protected override HashSet<CardTag> CanonicalTags => new() { MinigameSupport.FullGameTag };''',
        'GoldMiner': '''public sealed class GoldMiner : ModCardTemplate
{
    public GoldMiner() : base(0, CardType.Skill, CardRarity.Rare, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");

    // 衍生牌预览：巨石。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<GiantRock>(IsUpgraded)
    ];''',
    })

fix(os.path.join(C, 'Cards', 'RemainingCards5.cs'),
    ['RighteousIndignation'],
    {
        'OldMaid': '''public sealed class OldMaid : ModCardTemplate
{
    public OldMaid() : base(0, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");''',
        'PlayThisOne': '''public sealed class PlayThisOne : ModCardTemplate
{
    public PlayThisOne() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");''',
    })

# RolePlay：把重复的侧栏删除（已有飞溅侧栏，改为合并游戏牌侧栏）
s = open(os.path.join(C, 'Cards', 'MultiplayerCards.cs'), encoding='utf-8').read()
old_role = '''    // 衍生牌预览：飞溅。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<Splash>(IsUpgraded)
    ];'''
new_role = '''    // 衍生牌预览：飞溅 + 游戏牌侧栏。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<Splash>(IsUpgraded),
        new HoverTip(new LocString("cards", "STS2_MOMOI_GAME_CARD_SIDEBAR"))
    ];'''
s = s.replace(old_role, new_role, 1)
# 删除角色扮演类里误插的重复游戏牌侧栏（可能插入在 OnPlay 前）
dup = '''    // 游戏牌侧栏。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        new HoverTip(new LocString("cards", "STS2_MOMOI_GAME_CARD_SIDEBAR"))
    ];'''
s = s.replace(dup, '', 1)
open(os.path.join(C, 'Cards', 'MultiplayerCards.cs'), 'w', encoding='utf-8').write(s)

# TravelFrog（RemainingCards3）：TravelFrog 类内加侧栏
s = open(os.path.join(C, 'Cards', 'RemainingCards3.cs'), encoding='utf-8').read()
anchor = '''public sealed class TravelFrog : ModCardTemplate
{
    public TravelFrog() : base(1, CardType.Skill, CardRarity.Uncommon, TargetType.Self)
    {
    }

    public override CardAssetProfile AssetProfile => new(
        PortraitPath: $"{Entry.ResPath}/images/cards/{GetType().Name}.png");'''
s = s.replace(anchor, anchor + SIDEBAR, 1)
open(os.path.join(C, 'Cards', 'RemainingCards3.cs'), 'w', encoding='utf-8').write(s)

# FriendlyDuel（RemainingSpecialCards）：合并游戏牌侧栏
s = open(os.path.join(C, 'Cards', 'RemainingSpecialCards.cs'), encoding='utf-8').read()
old_fd = '''    // 衍生牌预览：WIN！/LOSE！。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<WinCard>(IsUpgraded),
        HoverTipFactory.FromCard<LoseCard>(IsUpgraded)
    ];'''
new_fd = '''    // 衍生牌预览：WIN！/LOSE！ + 游戏牌侧栏。
    protected override IEnumerable<IHoverTip> AdditionalHoverTips =>
    [
        HoverTipFactory.FromCard<WinCard>(IsUpgraded),
        HoverTipFactory.FromCard<LoseCard>(IsUpgraded),
        new HoverTip(new LocString("cards", "STS2_MOMOI_GAME_CARD_SIDEBAR"))
    ];'''
s = s.replace(old_fd, new_fd, 1)
open(os.path.join(C, 'Cards', 'RemainingSpecialCards.cs'), 'w', encoding='utf-8').write(s)

# MiscRareCards / Match3 缺 HoverTips using
for p2 in ['MiscRareCards.cs', 'Match3.cs']:
    p2 = os.path.join(C, 'Cards', p2)
    s = open(p2, encoding='utf-8').read()
    if 'using MegaCrit.Sts2.Core.HoverTips;' not in s:
        s = s.replace('using MegaCrit.Sts2.Core.GameActions.Multiplayer;',
                      'using MegaCrit.Sts2.Core.GameActions.Multiplayer;\nusing MegaCrit.Sts2.Core.HoverTips;', 1)
    open(p2, 'w', encoding='utf-8').write(s)

print('sidebar fix done')
