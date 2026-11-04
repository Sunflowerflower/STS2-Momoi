# -*- coding: utf-8 -*-
"""2026-10-09：同步 xlsx + design dump
  * 针锋相对（xlsx 行23 / dump [21]，dump 里还叫「借力打力」）：删掉「保留」行
  * 对策（xlsx 行45 / dump [44]，dump 里还叫「对症下药」）：仅改名
  * 我复活啦！（xlsx 行68 / dump [68]，顶替「轮回」）：整行/整条替换（轮回已备份）
  * 白与黑（xlsx 行69 / dump [70]）：文本加「在本场战斗中」
  * 修行（xlsx 行127 / dump [91]，dump 里还叫「活学活用」）：desc 也加「保留。」
用法：python _update_batch7_tables.py [--dry]
"""
import os, re, sys, shutil, datetime
import openpyxl

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
XL = os.path.join(ROOT, "工作区", "STS2Momoi.xlsx")
DUMPF = os.path.join(ROOT, "工作区", "_design_dump.txt")
BAKDIR = os.path.join(ROOT, "工作区", "_backup", "_xlsx_backup")
NL, AR = chr(10), " ⏎ "

IMBACK_DESC = ("获得3点活力。" + NL +
               "当你的生命值将被减少至0或以下时，改为消耗并从牌组中移除这张牌，然后将你回复到你最大生命值的10%并获得5层再生。")
IMBACK_DESCUP = ("获得5点活力。" + NL +
                 "当你的生命值将被减少至0或以下时，改为消耗并从牌组中移除这张牌，然后将你回复到你最大生命值的10%并获得6层再生。")
IMBACK_NOTE = ("免死参考原版蜥蜴尾巴（ShouldDieLate + AfterPreventingDeath）；发动时先消耗战斗内副本、再从牌组移除本尊"
               "（DeprecatedCard 的 DeckVersion 写法）；牌在牌组/抽牌堆/手牌/弃牌堆都会生效，已在消耗牌堆的副本不会二次触发。")

# 列：2 名称 / 3 类型 / 4 稀有度 / 5 耗费 / 6 升级耗费 / 7 描述 / 8 升级后描述 / 9 标签 / 10 备注 / 11 流派
XLSX = [
    ("针锋相对", dict(desc="造成1点伤害2次。" + NL + "如果敌人的意图是攻击，伤害增加敌人即将对你造成的伤害数。" + NL + "消耗。",
                   descUp="造成2点伤害2次。" + NL + "如果敌人的意图是攻击，伤害增加敌人即将对你造成的伤害数。")),
    ("见招拆招", dict(name="对策")),
    ("轮回", dict(name="我复活啦！", cost=0, costUp=0, desc=IMBACK_DESC, descUp=IMBACK_DESCUP, note=IMBACK_NOTE)),
    ("白与黑", dict(desc="从两张牌中选择一张加入你的手牌。" + NL + "选择后将在本场战斗中删去另一个选项。",
                  descUp="从两张升级过的牌中选择一张加入你的手牌。" + NL + "选择后将在本场战斗中删去另一个选项。")),
    ("修行", dict(desc="保留。" + NL + "选择一张构想消耗。" + NL + "该构想每有1点数值，你就获得2点力量，2点敏捷。")),
]
COLS = ["name", "type", "rarity", "cost", "costUp", "desc", "descUp", "tag", "note", "flow"]

DUMP_ENTRIES = {
    "借力打力": dict(head="针锋相对 | 攻击 | 罕见 | 费用 2 -> 2 | flow: ",
                 desc="造成1点伤害2次。" + AR + "如果敌人的意图是攻击，伤害增加敌人即将对你造成的伤害数。" + AR + "消耗。",
                 descUp="造成2点伤害2次。" + AR + "如果敌人的意图是攻击，伤害增加敌人即将对你造成的伤害数。"),
    "对症下药": dict(head="对策 | 技能 | 普通 | 费用 1 -> 1 | flow: 活力/火力流"),
    "轮回": dict(head="我复活啦！ | 技能 | 稀有 | 费用 0 -> 0 | flow: ",
               desc="获得3点活力。" + AR + "当你的生命值将被减少至0或以下时，改为消耗并从牌组中移除这张牌，然后将你回复到你最大生命值的10%并获得5层再生。",
               descUp="获得5点活力。" + AR + "当你的生命值将被减少至0或以下时，改为消耗并从牌组中移除这张牌，然后将你回复到你最大生命值的10%并获得6层再生。",
               note="免死参考原版蜥蜴尾巴；发动时先消耗战斗内副本、再从牌组移除本尊；牌在牌组/抽牌堆/手牌/弃牌堆都会生效，已在消耗牌堆的副本不会二次触发。"),
    "白与黑": dict(desc="从两张牌中选择一张加入你的手牌。" + AR + "选择后将在本场战斗中删去另一个选项。",
                descUp="从两张升级后的牌中选择一张加入你的手牌。" + AR + "选择后将在本场战斗中删去另一个选项。"),
    "活学活用": dict(head="修行 | 能力 | 罕见 | 费用 1 -> 1 | flow: 构想流",
                 desc="保留。" + AR + "选择一张构想消耗。" + AR + "该构想每有1点数值，你就获得2点力量，2点敏捷。",
                 descUp="保留。" + AR + "选择一张构想消耗。" + AR + "该构想每有1点数值，你就获得3点力量，3点敏捷。",
                 note="保留升级前后都有（2026-10-09 起）。"),
}


def main():
    dry = "--dry" in sys.argv
    os.makedirs(BAKDIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    if not dry:
        shutil.copy2(XL, os.path.join(BAKDIR, "STS2Momoi_%s_pre_batch7.xlsx" % ts))
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
    for old_name, e in DUMP_ENTRIES.items():
        pat = re.compile(r"### \[(\d+)\] " + re.escape(old_name) + r" \|.*?\n(?:desc:.*?\n)?(?:descUp:.*?\n)?(?:note:.*?\n)?")
        m = pat.search(text)
        if not m:
            print("dump 未找到:", old_name)
            continue
        orig_head = m.group(0).splitlines()[0]
        lines = [orig_head if not e.get("head") else "### [%s] %s" % (m.group(1), e["head"])]
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
