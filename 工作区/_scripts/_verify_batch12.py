# -*- coding: utf-8 -*-
"""批次12 自检：本轮所有改动的逐项核对。"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
LOC = os.path.join(MOD, "localization")

ok = fail = 0
def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))

def load(lang, table):
    return json.load(open(os.path.join(LOC, lang, table + ".json"), encoding="utf-8"))

def code(path):
    return open(os.path.join(CODE, path), encoding="utf-8").read()

Z = {t: load("zhs", t) for t in ("powers", "cards", "enchantments")}
E = {t: load("eng", t) for t in ("powers", "cards", "enchantments")}

print("== 1. 吃豆人「消耗」金色 ==")
for lang, d in (("zhs", Z), ("eng", E)):
    for suf in (".description", ".smartDescription"):
        s = d["cards"]["STS2_MOMOI_CARD_PAC_MAN" + suf]
        g = "[gold]消耗[/gold]" if lang == "zhs" else "[gold]Exhaust[/gold]"
        chk(g in s, "%s 卡牌 %s 含金色消耗" % (lang, suf))
    ps = d["powers"]["STS2_MOMOI_POWER_PAC_MAN_POWER.description"]
    g = "[gold]消耗[/gold]" if lang == "zhs" else "[gold]Exhaust[/gold]"
    chk(g in ps, "%s power 含金色消耗" % lang)

print("== 2. 构想局内数值绿色（专用 DynamicVar + UpdateCardPreview）==")
cc = code(os.path.join("Cards", "ConceptCard.cs"))
chk("class ConceptCountVar : DynamicVar" in cc and "override void UpdateCardPreview" in cc, "专用变量在 UpdateCardPreview 里现算")
chk("PreviewValue = ReadCount(card);" in cc, "写 PreviewValue")
chk('foreach (var name in new[] { "ConceptCount", "ConceptDraw", "Energy", "ConceptVigor" })' in cc,
    "四个变量都同步")
cd = Z["cards"]["STS2_MOMOI_CARD_CONCEPT_CARD.description"]
chk("{ConceptDraw:diff()}" in cd and "{Energy:energyIcons()}" in cd and "{ConceptVigor:diff()}" in cd,
    "描述用 diff()/energyIcons() 走高亮管道")

print("== 3. 记录型 power 隐藏 ==")
a1 = code(os.path.join("Cards", "AssistCards.cs"))
a2 = code(os.path.join("Cards", "AssistCards2.cs"))
chk(a1.count("protected override bool IsVisibleInternal => false;") == 1, "AssistTrackerPowerBase 隐藏")
chk(a2.count("protected override bool IsVisibleInternal => false;") == 1, "AssistTrackerPowerBase2 隐藏")

print("== 4. 幸运儿的祝福 ==")
chk("public override PowerStackType StackType => PowerStackType.Counter;" in a2, "改为可叠加")
chk("public override int DisplayAmount => Amount;" in a2, "右下角显示剩余回合数")
chk("if (upgraded || !data.Upgraded)" in a2, "升级覆盖、降级不覆盖")
chk("await PowerCmd.TickDownDuration(this);" in a2, "回合结束递减")
z = Z["powers"]["STS2_MOMOI_POWER_ASUNA_GUARD_POWER.description"]
chk(z == "直到你的下[blue]{Amount}[/blue]个回合开始前，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。",
    "zhs 文本规范（批次50：带剩余回合数）", z)
e = E["powers"]["STS2_MOMOI_POWER_ASUNA_GUARD_POWER.description"]
chk("Until the start of your next [blue]{Amount}[/blue] turn(s)" in e and "{ReductionPct}%" in e
    and e.count("[blue]") == 2,
    "eng 文本规范（批次50 同步）", e)
# 卡牌不再手动处理已有 power
chk("existingGuard" not in a2, "卡牌不再手动判重")

print("== 5. “雷酱”炮台支援 ==")
chk("public override PowerInstanceType InstanceType => PowerInstanceType.Instanced;" in a1, "独立实例")
chk("public override PowerStackType StackType => PowerStackType.Counter;" in a1, "层数=剩余回合")
chk("public override int DisplayAmount => Amount;" in a1, "计数=剩余回合")
chk("yoshimi.FaceBlock" in a1 and "yoshimi.FaceDamage" in a1, "从卡面快照数值")
chk("new BlockVar(3m, ValueProp.Move)" in a1, "大师卡格挡用 BlockVar（3/4，卡面受敏捷影响）")
chk("ValueProp.Unpowered" in a1 and "CreatureCmd.Damage" in a1, "power 伤害走原版能力伤害（Unpowered）")
chk("_vigorThisAttack" not in a1 and "VulnerablePower" not in a1, "不再自己补活力与易伤（批次49）")
chk("await PowerCmd.Apply<YoshimiRepeatPower>(choiceContext, Owner.Creature, FaceTurns," in a1,
    "施加层数=卡面回合数")
zy = Z["powers"]["STS2_MOMOI_POWER_YOSHIMI_REPEAT_POWER.description"]
chk("{Amount}" in zy and "[gold]格挡[/gold]" in zy and "[gold]火力[/gold]" in zy, "zhs 文本用实际回合数+金色关键词", zy)

print("== 6. 打灰机！格挡 ==")
r4 = code(os.path.join("Cards", "RemainingCards4.cs"))
chk("new BlockVar(6m, ValueProp.Move)" in r4, "打灰机用 BlockVar（6/8）")
chk("DynamicVars.Block, cardPlay" in r4, "GainBlock 用 DynamicVars.Block")

print("== 7. 来自花凛的援护（删 power，改 Boss 增伤牌）==")
chk("class KarinFinishPower" not in a2, "KarinFinishPower 已删")
chk("public MomoiSupportKarin() : base(2, CardType.Attack, CardRarity.Token, TargetType.AnyEnemy)" in a2,
    "2 费攻击·衍生·单体")
chk("new CalculationBaseVar(32m)" in a2, "基础 32 伤")
chk('DynamicVars["BossPct"].UpgradeValueBy(25)' in a2, "升级 50->75")
chk("MinigameSupport.SupportTag" in a2, "支援牌 tag")
zk = Z["cards"]["STS2_MOMOI_CARD_MOMOI_SUPPORT_KARIN.description"]
chk(re.sub(r"\[/?[a-z]+\]", "", zk).startswith("造成") and "对Boss造成的伤害增加" in zk, "zhs 文本", zk)

print("== 8. 注能已改为卡牌自带（不再有附魔与附魔图标）==")
chk(not os.path.exists(os.path.join(MOD, "images", "enchantments")), "附魔图标目录已删（不再有 nope）")
chk("AfterAutoPrePlayPhaseEntered" in code(os.path.join("Cards", "RemainingSpecialCards.cs")),
    "注能效果写在 DevGreen 卡里")

print("== 9. power 数字全蓝 / 关键词金 ==")
bad = []
for lang in ("zhs", "eng"):
    d = load(lang, "powers")
    for k, v in d.items():
        if not k.endswith(".description"):
            continue
        stripped = re.sub(r"\[blue\][^[]*?\[/blue\]|\[green\][^[]*?\[/green\]", "", v)
        stripped = re.sub(r"\{[^}]*\}", "", stripped)
        stripped = re.sub(r"\[[a-z/]+\]", "", stripped)
        if re.search(r"\d+%?", stripped):
            bad.append("%s/%s" % (lang, k))
chk(not bad, "无裸数字", bad[:8])
bad2 = []
for lang in ("zhs", "eng"):
    for f in os.listdir(os.path.join(LOC, lang)):
        if not f.endswith(".json"):
            continue
        d = load(lang, f[:-5])
        for k, v in d.items():
            if not isinstance(v, str):
                continue
            for tag in set(re.findall(r"\[([a-z]+)\]", v)):
                if v.count("[%s]" % tag) != v.count("[/%s]" % tag):
                    bad2.append("%s/%s/%s[%s]" % (lang, f, k, tag))
chk(not bad2, "标签全部闭合", bad2[:6])

print("== 10. 右下角计数语义 ==")
c5 = code(os.path.join("Cards", "ConceptFlowCards.cs"))
chk("public override int DisplayAmount => GetInternalData<Data>().DamagePer;" in c5, "构想之矛=伤害")
chk("public override int DisplayAmount => GetInternalData<Data>().BlockPer;" in c5, "构想之盾=格挡")
# 矛与盾不改：整个文件只有上面两条 DisplayAmount，且都不属于 SpearShieldPower。
ss_start = c5.find("class SpearShieldPower")
ss_body = c5[ss_start:] if ss_start >= 0 else ""
chk(c5.count("public override int DisplayAmount") == 2 and "public override int DisplayAmount" not in ss_body,
    "矛与盾未改（仍是叠加层数）", "count=%d" % c5.count("public override int DisplayAmount"))

print("== 11. 重整旗鼓：回复 + 实时数值 ==")
r3 = code(os.path.join("Cards", "RemainingCards3.cs"))
chk("public override int DisplayAmount => PendingHeal;" in r3, "右下角实时显示")
chk("public override Task AfterCurrentHpChanged(Creature creature, decimal delta)" in r3, "生命变化刷新")
chk("Owner.MaxHpChanged += OnOwnerMaxHpChanged" in r3 and "oldOwner.MaxHpChanged -= OnOwnerMaxHpChanged" in r3,
    "最大生命事件订阅/退订")
for lang, d in (("zhs", Z), ("eng", E)):
    s = d["powers"]["STS2_MOMOI_POWER_RALLY_AGAIN_POWER.description"]
    if lang == "zhs":
        chk("回复" in s and "恢复" not in s, "power 文本恢复→回复", s)
    else:
        chk("heal" in s.lower(), "eng power 文本", s)
zr = Z["cards"]["STS2_MOMOI_CARD_RALLY_AGAIN.description"]
chk("回复" in zr and "恢复" not in zr, "卡牌文本恢复→回复", zr)

print("== 12. 我复活啦！ ==")
ib = code(os.path.join("Cards", "ImBack.cs"))
chk("private ImBack Root => DeckVersion as ImBack ?? this;" in ib, "本体/副本共用标记")
chk("private bool Used" in ib and "get => Root._used;" in ib, "Used 读写根实例")
chk("creature != Owner.Creature || Used" in ib, "ShouldDieLate 用共用标记")

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
