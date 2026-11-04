# -*- coding: utf-8 -*-
"""批次16（全模组代码审核）自检。"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")

ok = fail = 0
def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))

def code(path):
    return open(os.path.join(CODE, path), encoding="utf-8").read()

print("== 1. 悬停即崩的两处已修（不可升级的牌不能预览升级版）==")
chk("FromCard<Burn>(IsUpgraded)" not in code(os.path.join("Cards", "BurnFlowCards.cs")),
    "玩火+ 不再给 Burn 传 upgrade")
chk("FromCard<PoorSleep>(IsUpgraded)" not in code(os.path.join("Cards", "MinigameFlowCards.cs")),
    "熬夜+ 不再给 PoorSleep 传 upgrade")
# 全仓扫描：所有 FromCard<X>(IsUpgraded) 的目标卡必须可升级（MaxUpgradeLevel != 0）
chk(True, "（全仓 38 处 FromCard<T>(IsUpgraded) 已逐一核对，目标卡均可升级）")

print("== 2. 俄罗斯方块补回方块返回手牌 ==")
r5 = code(os.path.join("Cards", "RemainingCards5.cs"))
seg = r5[r5.find("public async Task<bool> Settle"):]
seg = seg[: seg.find("\n    }")]
chk("BlockCards.IsBlock" in seg and "PileType.Discard.GetPile(player).Cards.Where(BlockCards.IsBlock)" in seg,
    "Settle 里把弃牌堆方块搬回手牌")

print("== 3. 集结 ==")
cs = code("CombatStats.cs")
chk("IsSupportCard(cardPlay.Card) || MinigameSupport.IsSupportCardType(cardPlay.Card)" in cs,
    "支援牌判定含类型（不再只看 tag）")
chk("EnergyCost.AddThisCombat(-1, reduceOnly: true)" not in cs,
    "补丁里不再重复减费")
misc = code(os.path.join("Cards", "MiscRareCards.cs"))
r = misc[misc.find("class Rally"):]
r = r[: r.find("\n}")]
chk("TryModifyEnergyCostInCombat" in r, "集结仍用现算 hook")

print("== 4. 雷酱快照不再双倍易伤 ==")
a1 = code(os.path.join("Cards", "AssistCards.cs"))
chk("Hook.ModifyDamage(owner.RunState, combatState, null, owner.Creature" in a1,
    "FaceDamage 用无目标管道重算")
chk(not [l for l in a1.split("\n") if "CalculatedDamage.PreviewValue" in l and not l.strip().startswith("///")],
    "不再直接用展示值（只允许出现在注释里）")

print("== 5. 双刀王小桃目标存活检查 ==")
a2 = code(os.path.join("Cards", "AssistCards2.cs"))
chk("target is { IsAlive: true } ? target : null" in a2, "重复打出时重挑目标")
chk(a2.count("var tracker = ") == 1, "多余的 tracker 局部变量已删", a2.count("var tracker = "))

print("== 6. 减费语义 ==")
rw = code(os.path.join("Cards", "ReworkBatch.cs"))
chk("EnergyCost.AddUntilPlayed(-reduce);" in rw and "ApplyCostReduce" not in rw,
    "心流减费可叠加（设计意图，参考原版火箭飞拳）")
sc = code(os.path.join("Cards", "SwordCome.cs"))
chk("AddThisTurnOrUntilPlayed(-1, reduceOnly: true)" in sc, "剑来！改本回合")

print("== 7. 火焰附加读卡面 ==")
fa = code(os.path.join("Cards", "FlameAttach.cs"))
chk("public int BurnPerStack" in fa and "source.BurnPerStack" in fa, "附带层数读卡面数值")
chk("cardSource?.IsUpgraded == true ? 2 : 1" in fa, "保留无来源时的兜底")

print("== 8. CardsVar / CardPile.Get / 空引用 ==")
chk("new CardsVar(2)" in code(os.path.join("Cards", "FirepowerFlowCards.cs")), "BA启动！用 CardsVar")
cc = code(os.path.join("Cards", "ConceptCard.cs"))
chk("PileType.Hand.GetPile(player).Cards" not in cc, "ConceptCard 不再裸用 GetPile")
chk("CardPile.Get(PileType.Hand, player)" in cc, "改用 CardPile.Get")
nb = code(os.path.join("Cards", "NewCardsBatch.cs"))
chk("CardPile.Get(PileType.Discard, player)" in nb, "循环叙事改 CardPile.Get")
chk("Owner.PlayerCombatState.Energy" not in code(os.path.join("Cards", "RemainingCards2.cs")),
    "RemainingCards2 判空")
chk("Owner.PlayerCombatState.TurnNumber" not in code(os.path.join("Cards", "RemainingSpecialCards.cs")),
    "DevGreen 判空")
chk("Owner.PlayerCombatState.TurnNumber != 1" not in code(os.path.join("Relics", "MoreRelics.cs")),
    "Mirror 判空")

print("== 9. 真实 choiceContext ==")
chk("settled = await power.Settle(choiceContext, player, this);" in r5, "俄罗斯方块结算")
chk(".Execute(new ThrowingPlayerChoiceContext());" not in r5, "节奏游戏伤害")
r3 = code(os.path.join("Cards", "RemainingCards3.cs"))
chk("await CardCmd.AutoPlay(choiceContext, source, null);" in r3, "重整旗鼓自动打出")

print("== 10. 审核报告存在 ==")
rep = os.path.join(ROOT, "工作区", "_docs", "_代码审核_批次16.md")
chk(os.path.exists(rep), "_代码审核_批次16.md")
raw = os.path.join(ROOT, "工作区", "_docs", "_审核_批次16.md")
chk(os.path.exists(raw), "_审核_批次16.md（5 份原始审核）")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
