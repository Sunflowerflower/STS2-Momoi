# -*- coding: utf-8 -*-
"""本批（第六批）代码核验。"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.abspath(__file__))

def read(p):
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''

src = {}
for dirpath, _, files in os.walk(os.path.join(BASE, 'STS2 MomoiCode')):
    for f in files:
        if f.endswith('.cs'):
            full = os.path.join(dirpath, f)
            src[os.path.relpath(full, BASE).replace('\\', '/')] = read(full)

mfc = src['STS2 MomoiCode/Cards/MinigameFlowCards.cs']
r5 = src['STS2 MomoiCode/Cards/RemainingCards5.cs']
rsp = src['STS2 MomoiCode/Cards/RemainingSpecialCards.cs']
cfc = src['STS2 MomoiCode/Cards/ConceptFlowCards.cs']
cs = src['STS2 MomoiCode/CombatStats.cs']
entry = src['STS2 MomoiCode/Entry.cs']
allc = '\n'.join(src.values())
ok = bad = 0
def check(label, cond):
    global ok, bad
    if cond:
        ok += 1
        print('  OK  ' + label)
    else:
        bad += 1
        print('  !!  ' + label)

print('【1 开荒】')
check('耗能/类型/稀有度不变', 'public Grinding() : base(0, CardType.Skill, CardRarity.Common' in mfc)
check('能量 2（升级 +1）', 'new EnergyVar(2)  // 升级 3' in mfc and 'DynamicVars["Energy"].UpgradeValueBy(1);' in mfc)
check('诅咒池顺序 苦恼→睡眠不佳→疑虑→执迷', 'Order = [typeof(Writhe), typeof(PoorSleep), typeof(Doubt), typeof(Enthralled)]' in mfc)
check('按序取未生成过的', 'Order.FirstOrDefault(t => !Generated.Contains(t))' in mfc)
check('1 张诅咒进弃牌堆', 'AddGeneratedCardToCombat(curse, PileType.Discard, Owner)' in mfc)
gseg = mfc.split('class Grinding :')[1].split('class GrindingCursePool')[0]
check('笨拙逻辑已移除', 'Clumsy' not in gseg)
check('侧栏 4 张诅咒预览', all(f'FromCard<{c}>()' in mfc for c in ['Writhe', 'PoorSleep', 'Doubt', 'Enthralled']))
check('战斗开始重置池', 'Cards.GrindingCursePool.Reset();' in cs)
check('补丁记录生成卡', 'nameof(Hook.AfterCardGeneratedForCombat)' in cs and 'GrindingCursePool.Record(card)' in cs)
check('补丁已注册', 'RegisterPatch<GrindingCurseTrackPatch>()' in entry)

print('【2 大姐头】')
bs = rsp[rsp.find('class BigSister'):rsp.find('class BigSister') + 2200]
check('保留+消耗（升级前后）', 'new() { CardKeyword.Retain, CardKeyword.Exhaust }' in bs)
check('升级前 -1 费', 'clone.EnergyCost.AddUntilPlayed(-1);' in bs)
check('升级后免费', 'clone.SetToFreeThisTurn();' in bs and 'if (IsUpgraded)' in bs)
check('OnUpgrade 不再加保留', 'LocalKeywords.Add(CardKeyword.Retain)' not in bs)
wc = rsp[rsp.find('class WinCard'):rsp.find('class WinCard') + 1600]
check('WinCard 未被误改（仅消耗）', 'new() { CardKeyword.Exhaust };' in wc and 'CostReduce' not in wc)

print('【3 构想之盾/矛 → 矛与盾 展示】')
sh = cfc[cfc.find('class ConceptShield'):cfc.find('class ConceptShieldPower')]
sp = cfc[cfc.find('class ConceptSpear'):cfc.find('class ConceptSpearPower')]
check('构想之盾 预览矛与盾', 'FromCard<SpearShield>(IsUpgraded)' in sh)
check('构想之矛 预览矛与盾', 'FromCard<SpearShield>(IsUpgraded)' in sp)

print('【4 方块 4 种】')
check('旧 TetrisBlock 已删除', 'TetrisBlock' not in allc)
for c, cn in [('YellowBlock', '黄方块'), ('BlueBlock', '蓝方块'), ('PurpleBlock', '紫方块'), ('GreenBlock', '绿方块')]:
    check(f'{cn} 已注册', f'public sealed class {c} : ModCardTemplate' in mfc)
check('BlockCards.All 四种', 'typeof(YellowBlock), typeof(BlueBlock), typeof(PurpleBlock), typeof(GreenBlock)' in mfc)
check('随机获得一种', 'owner.RunState.Rng.CombatCardSelection.NextInt(All.Length)' in mfc)
check('消耗获得 2 格挡 ×4', mfc.count('await CreatureCmd.GainBlock(Owner.Creature, new BlockVar(2, ValueProp.Move), null);') == 4)
check('相关牌展示 4 种（3 处）', mfc.count('BlockCards.Tips()') + r5.count('BlockCards.Tips()') == 3)
check('计数用 IsBlock（3 处）', r5.count('BlockCards.IsBlock') == 3)
check('生成用 CreateRandom（4 处）', (mfc + r5).count('BlockCards.CreateRandom') == 4)

print('【5 卡面应用】')
img = os.path.join(BASE, 'STS2_Momoi/images/cards')
files = [f for f in os.listdir(img) if f.endswith('.png')]
check(f'图片 {len(files)} 张', len(files) == 130)
for c in ['YellowBlock', 'BlueBlock', 'PurpleBlock', 'GreenBlock', 'LoseCard', 'WinCard', 'ConceptCard', 'Rally']:
    check(f'{c}.png 存在', f'{c}.png' in files)
check('旧 TetrisBlock.png 已删', 'TetrisBlock.png' not in files)

print('【本地化】')
zhs = json.load(open(os.path.join(BASE, 'STS2_Momoi/localization/zhs/cards.json'), encoding='utf-8'))
eng = json.load(open(os.path.join(BASE, 'STS2_Momoi/localization/eng/cards.json'), encoding='utf-8'))
for cls in ['GRINDING', 'BIG_SISTER', 'YELLOW_BLOCK', 'BLUE_BLOCK', 'PURPLE_BLOCK', 'GREEN_BLOCK']:
    for suf in ['.title', '.description']:
        check(f'{cls}{suf} zh/eng 存在', f'STS2_MOMOI_CARD_{cls}{suf}' in zhs and f'STS2_MOMOI_CARD_{cls}{suf}' in eng)
check('开荒侧栏文本', '特定诅咒：苦恼，睡眠不佳，疑虑，执迷。' in zhs.get('STS2_MOMOI_CARD_GRINDING.sidebar', ''))
check('旧方块键已删', 'STS2_MOMOI_CARD_TETRIS_BLOCK.title' not in zhs)
check('大姐头文本含 IfUpgraded 减费', 'IfUpgraded:show:可以免费打出|耗能减少{CostReduce:energyIcons()}' in zhs['STS2_MOMOI_CARD_BIG_SISTER.description'])

print(f'\n核验：通过 {ok}，未通过 {bad}')
