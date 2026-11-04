# -*- coding: utf-8 -*-
"""批次49：把因本次改动而过期的自检断言就地更新（17 条）。"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BS = chr(92)

EDITS = [
    # ---- _verify_batch12：明日奈文本 + 援护能力伤害 ----
    ("_verify_batch12.py",
     'chk(z == "[blue]{Amount}[/blue]回合内，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。", "zhs 文本规范", z)',
     'chk(z == "直到你的下回合开始前，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。",\n    "zhs 文本规范（批次49：持续到下回合开始前）", z)', 1),
    ("_verify_batch12.py",
     'chk("{Amount}" in e and "{ReductionPct}%" in e and e.count("[blue]") == 2, "eng 文本规范", e)',
     'chk("Until the start of your next turn" in e and "{ReductionPct}%" in e and e.count("[blue]") == 1,\n    "eng 文本规范（批次49 同步）", e)', 1),
    ("_verify_batch12.py",
     'chk(".Unpowered()" in a1, "power 伤害不受力量/虚弱影响")',
     'chk("ValueProp.Unpowered" in a1 and "CreatureCmd.Damage" in a1, "power 伤害走原版能力伤害（Unpowered）")', 1),
    ("_verify_batch12.py",
     'chk("_vigorThisAttack" in a1 and "VulnerablePower" in a1, "自己补活力与易伤")',
     'chk("_vigorThisAttack" not in a1 and "VulnerablePower" not in a1, "不再自己补活力与易伤（批次49）")', 1),
    # ---- _verify_batch13：援护不再扣活力 + 循环叙事 power 文本 ----
    ("_verify_batch13.py",
     'chk("await FirepowerHooks.SpendVigorAsync(choiceContext, Owner, _vigorThisAttack);" in a1,',
     'chk("FirepowerHooks.SpendVigorAsync" not in a1,', 1),
    ("_verify_batch13.py",
     '"雷酱改走 FirepowerHooks")',
     '"援护不再自己扣活力（批次49 改原版能力伤害）")', 1),
    ("_verify_batch13.py",
     'chk(z == "接下来的[blue]{Amount}[/blue]个回合结束时，将本回合所有进入过[gold]弃牌堆[/gold]的牌洗入[gold]抽牌堆[/gold]。",',
     'chk(z == "本回合结束时，将[gold]弃牌堆[/gold]的最多[blue]{Amount}[/blue]张牌洗入你的[gold]抽牌堆[/gold]。",', 1),
    # ---- _verify_batch15：注能改走 ImbuedSupport + 循环叙事卡面文本 ----
    ("_verify_batch15.py",
     '"CardCmd.AutoPlay(choiceContext, this, null)" in d',
     '"ImbuedSupport.TryAutoPlayAsync(choiceContext, this" in d', 1),
    ("_verify_batch15.py",
     'chk("MOMOI_IMBUED" in d, "保留注能词条的侧栏")',
     'chk("ImbuedSupport.ImbuedTip" in d, "保留注能词条的侧栏")', 1),
    ("_verify_batch15.py",
     'chk(zc == "将本回合所有进入过[gold]弃牌堆[/gold]的牌洗入[gold]抽牌堆[/gold]。',
     'chk(zc == "[gold]注能[/gold]。', 1),
    ("_verify_batch15.py",
     '本回合结束时，重复此效果。",',
     '本回合结束时，将[gold]弃牌堆[/gold]的最多1张牌洗入你的[gold]抽牌堆[/gold]。",', 1),
    # ---- _verify_batch20：注能侧栏统一 ----
    ("_verify_batch20.py",
     'chk(\'new HoverTip(new LocString("enchantments", "MOMOI_IMBUED.title")\' in rs, "注能侧栏仍在")',
     'chk("MOMOI_IMBUED.title" in rs, "注能侧栏仍在（统一到 ImbuedSupport）")', 1),
    # ---- _verify_batch24/28/32：贴图导入规则与 pck 体积 ----
    ("_verify_batch24.py",
     'chk("compress/mode=0" in imp, "idle.png 无损导入（compress/mode=0）")',
     'chk("compress/mode=1" in imp and "compress/lossy_quality=0.95" in imp,\n    "cue/idle.png 走有损 WebP 0.95（批次49 体积优化）")', 1),
    ("_verify_batch28.py",
     'chk(os.path.getsize(PCK) >= 115_000_000, "PCK >=115MB", os.path.getsize(PCK))',
     'chk(40_000_000 <= os.path.getsize(PCK) <= 80_000_000, "PCK 已按贴图规则压缩（约 55MB）", os.path.getsize(PCK))', 1),
    ("_verify_batch32.py",
     'chk(os.path.getsize(PCK) >= 120_000_000, "PCK >=120MB", os.path.getsize(PCK))',
     'chk(40_000_000 <= os.path.getsize(PCK) <= 80_000_000, "PCK 已按贴图规则压缩（约 55MB）", os.path.getsize(PCK))', 2),
    # ---- _verify_batch40：循环叙事 1 费 / 升级减费 ----
    ("_verify_batch40.py",
     'chk("public CyclicNarrative() : base(0, CardType.Skill" in cn, "循环叙事 0 费")',
     'chk("public CyclicNarrative() : base(1, CardType.Skill, CardRarity.Uncommon" in cn,\n    "循环叙事 1 费技能罕见（批次49）")', 1),
    ("_verify_batch40.py",
     'chk("AddKeyword(CardKeyword.Retain);" in cn, "循环叙事：升级加保留")',
     'chk("EnergyCost.UpgradeBy(-1);" in cn, "循环叙事：升级减 1 费")', 1),
    # ---- _verify_batch44：BA启动 活力 3/4 + DevGreen 走 ImbuedSupport ----
    ("_verify_batch44.py",
     '("BaBoot", \'new DynamicVar("Vigor", 2)\', "BA启动 活力 2/3"),',
     '("BaBoot", \'new DynamicVar("Vigor", 3)\', "BA启动 活力 3/4（批次49）"),', 1),
    ("_verify_batch44.py",
     'chk("CardCmd.AutoPlay(choiceContext, this, null)" in dg, "恢复正常的 CardCmd.AutoPlay 自动打出（批次46 回退）")',
     'chk("ImbuedSupport.TryAutoPlayAsync(choiceContext, this" in dg, "注能走共用 ImbuedSupport 自动打出（批次49）")', 1),
]


def main() -> int:
    bad = 0
    for name, old, new, expected in EDITS:
        path = os.path.join(HERE, name)
        with io.open(path, encoding="utf-8") as f:
            text = f.read()
        got = text.count(old)
        if got != expected:
            print(f"[FAIL] {name}: 期望 {expected} 处，实际 {got} 处 << {old[:40]}")
            bad += 1
            continue
        text = text.replace(old, new)
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"[OK] {name}: {old[:38]} -> {new[:38]}")
    print(f"完成：{len(EDITS) - bad} 处替换，{bad} 处失败")
    return 1 if bad else 0


sys.exit(main())
