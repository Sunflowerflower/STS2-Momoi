# -*- coding: utf-8 -*-
"""2026-10-11：同步 xlsx + design dump
  * 局势升温（dump 里叫「玩火」）：分别将 2 张灼烧 → 1 张灼伤
  * 双线叙事：使构想的数值加2。→ 使构想数值+2。
  * 火焰附加：稀有 → 罕见
  * 金色传说！→ 游戏人生（顶替）
  * 趁热打铁（dump 里叫「夜以继日」）→ 暗黑心理学（顶替）
用法：py -3 _update_batch8_tables.py [--dry]
"""
import os, re, sys, shutil, datetime
import openpyxl

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
XL = os.path.join(ROOT, "工作区", "STS2Momoi.xlsx")
DUMPF = os.path.join(ROOT, "工作区", "_design_dump.txt")
BAKDIR = os.path.join(ROOT, "工作区", "_backup", "_xlsx_backup")
NL, AR = chr(10), " ⏎ "

BURN_FIX = ("分别将2张灼烧加入你的弃牌堆和抽牌堆。", "分别将1张灼伤加入你的弃牌堆和抽牌堆。")
CONCEPT_FIX = ("使构想的数值加2。", "使构想数值+2。")

GAMELIFE_DESC = "造成9点伤害。" + NL + "为一张手牌添加游戏牌标签。"
GAMELIFE_DESCUP = "造成12点伤害。" + NL + "为一张手牌和它的所有同名牌添加游戏牌标签。"
GAMELIFE_NOTE = ("已经是游戏牌或小游戏牌的牌不会进入选择界面；本牌自己不是游戏牌/小游戏牌，也可以被自己添加。"
                 "标签同时写在牌组本尊上（本局后续战斗仍算游戏牌）；描述顶行的金色「游戏牌。」由 CardKeywordLabelPatch 按标签自动显示。")

DARK_DESC = "使一名敌人在下次获得力量时将不再获得，改为使构想数值+1。" + NL + "消耗。"
DARK_DESCUP = "使一名敌人在下次获得力量时将不再获得，改为使构想数值+1。"
DARK_NOTE = ("可叠加次数（每层抵消一次力量获得）。用原版修饰器钩子拦截力量**增加**"
             "（TryModifyPowerAmountReceived + AfterModifyingPowerAmountReceived，写法同原版神器 ArtifactPower）；"
             "力量减少不拦，但「临时减力量」回合结束的补回属于力量增加，会被拦。触发拦截时使所有玩家手牌中的构想数值+1。")

# 列：2 名称 / 3 类型 / 4 稀有度 / 5 耗费 / 6 升级耗费 / 7 描述 / 8 升级后描述 / 9 标签 / 10 备注 / 11 流派
XLSX = [
    ("局势升温", dict(desc="造成10点伤害。" + NL + "给予一半所造成伤害的灼烧。（向下取整）" + NL + "分别将1张灼伤加入你的弃牌堆和抽牌堆。",
                   descUp="造成13点伤害。" + NL + "给予一半所造成伤害的灼烧。（向上取整）" + NL + "分别将1张灼伤加入你的弃牌堆和抽牌堆。")),
    ("双线叙事", dict(desc="固有。" + NL + "使构想数值+2。" + NL + "将构想的一张复制品加入你的手牌，然后为其附魔灵魂之力。" + NL + "消耗。",
                  descUp="固有。" + NL + "使构想数值+2。" + NL + "将构想的一张复制品加入你的手牌，然后为其附魔灵魂之力。" + NL + "消耗。")),
    ("火焰附加", dict(rarity="罕见")),
    ("金色传说！", dict(name="游戏人生", type="攻击", rarity="罕见", cost=1, costUp=1,
                   desc=GAMELIFE_DESC, descUp=GAMELIFE_DESCUP, tag=None, note=GAMELIFE_NOTE, flow=None)),
    ("趁热打铁", dict(name="暗黑心理学", type="技能", rarity="稀有", cost=2, costUp=2,
                  desc=DARK_DESC, descUp=DARK_DESCUP, tag=None, note=DARK_NOTE, flow="构想流")),
]
COLS = ["name", "type", "rarity", "cost", "costUp", "desc", "descUp", "tag", "note", "flow"]

DUMP_ENTRIES = {
    "玩火": dict(head="局势升温 | 攻击 | 罕见 | 费用 1 -> 1 | flow: 灼烧流",
               desc="造成10点伤害。" + AR + "给予一半所造成伤害的灼烧。（向下取整）" + AR + "分别将1张灼伤加入你的弃牌堆和抽牌堆。",
               descUp="造成13点伤害。" + AR + "给予一半所造成伤害的灼烧。（向上取整）" + AR + "分别将1张灼伤加入你的弃牌堆和抽牌堆。"),
    "双线叙事": dict(desc="固有。" + AR + "使构想数值+2。" + AR + "将构想的一张复制品加入你的手牌，然后为其附魔灵魂之力。" + AR + "消耗。",
                 descUp="固有。" + AR + "使构想数值+2。" + AR + "将构想的一张复制品加入你的手牌，然后为其附魔灵魂之力。" + AR + "消耗。"),
    "火焰附加": dict(head="火焰附加 | 能力 | 罕见 | 费用 1 -> 1 | flow: 灼烧流"),
    "金色传说！": dict(head="游戏人生 | 攻击 | 罕见 | 费用 1 -> 1 | flow: ",
                  desc="造成9点伤害。" + AR + "为一张手牌添加游戏牌标签。",
                  descUp="造成12点伤害。" + AR + "为一张手牌和它的所有同名牌添加游戏牌标签。",
                  note="已是游戏牌/小游戏牌的牌不进选择界面；标签同时写在牌组本尊上；描述顶行金色「游戏牌。」由补丁按标签显示。"),
    "夜以继日": dict(head="暗黑心理学 | 技能 | 稀有 | 费用 2 -> 2 | flow: 构想流",
                 desc="使一名敌人在下次获得力量时将不再获得，改为使构想数值+1。" + AR + "消耗。",
                 descUp="使一名敌人在下次获得力量时将不再获得，改为使构想数值+1。",
                 note="可叠加次数；拦截力量增加（原版修饰器钩子）；触发时使所有玩家手牌中的构想数值+1。"),
}


def main():
    dry = "--dry" in sys.argv
    os.makedirs(BAKDIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    if not dry:
        shutil.copy2(XL, os.path.join(BAKDIR, "STS2Momoi_%s_pre_batch8.xlsx" % ts))
    wb = openpyxl.load_workbook(XL)
    ws = wb["卡牌"]
    for old_name, row in XLSX:
        target = next((r for r in range(3, ws.max_row + 1) if ws.cell(row=r, column=2).value == old_name), None)
        if target is None:
            print("xlsx 未找到:", old_name)
            continue
        for i, key in enumerate(COLS):
            if row.get(key) is not None:
                ws.cell(row=target, column=2 + i).value = row[key]
        print("xlsx 行%-4d %s -> %s" % (target, old_name, row.get("name", old_name)))
    if not dry:
        wb.save(XL)

    text = open(DUMPF, encoding="utf-8").read()
    # 先做纯文本修正（两处）
    for old, new in (BURN_FIX, CONCEPT_FIX):
        if old in text:
            text = text.replace(old, new)
            print("dump 文案修正:", old, "→", new)
    for old_name, e in DUMP_ENTRIES.items():
        pat = re.compile(r"### \[(\d+)\] " + re.escape(old_name) + r" \|.*?\n(?:desc:.*?\n)?(?:descUp:.*?\n)?(?:note:.*?\n)?")
        m = pat.search(text)
        if not m:
            print("dump 未找到:", old_name)
            continue
        lines = ["### [%s] %s" % (m.group(1), e.get("head") or m.group(0).splitlines()[0])]
        for key in ("desc", "descUp", "note"):
            if e.get(key):
                lines.append(key + ": " + e[key])
            else:
                mm = re.search(r"^" + key + r": .*$", m.group(0), re.M)
                if mm:
                    lines.append(mm.group(0))
        text = text[:m.start()] + NL.join(lines) + NL + text[m.end():]
        print("dump [%s] %s -> 已改写" % (m.group(1), old_name))
    if not dry:
        open(DUMPF, "w", encoding="utf-8").write(text)
    print("[dry-run]" if dry else "已写入")


if __name__ == "__main__":
    main()
