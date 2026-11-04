# -*- coding: utf-8 -*-
"""2026-10-08：同步 xlsx + design dump
  * 火焰附加：耗能 2→1（含升级）
  * 天马行空（dump 里还叫「弹雨」）：伤害 4/6 → 5/7
  * 独特点子：耗能 2→1（含升级）、伤害 6/8 → 4/6；顺手修正备注/描述里遗留的「稀有牌/罕见牌」→ 小游戏牌
  * 打游戏！：表里本来就是 1→0（代码本次才对齐，无需改表）
  * 改名：节奏大师 → 节奏游戏！；还施彼身 → 针锋相对
用法：python _update_batch6_tables.py [--dry]
"""
import os, re, sys, shutil, datetime
import openpyxl

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
XL = os.path.join(ROOT, "工作区", "STS2Momoi.xlsx")
DUMP = os.path.join(ROOT, "工作区", "_design_dump.txt")
BAKDIR = os.path.join(ROOT, "工作区", "_backup", "_xlsx_backup")
NL, AR = chr(10), " ⏎ "

# 列：2 名称 / 3 类型 / 4 稀有度 / 5 耗费 / 6 升级耗费 / 7 描述 / 8 升级后描述 / 9 标签 / 10 备注 / 11 流派
XLSX = [
    ("火焰附加", dict(cost=1, costUp=1)),
    ("天马行空", dict(desc="对所有敌人造成5点伤害。" + NL + "额外攻击等同构想数值次。" + NL + "（额外攻击0次）",
                   descUp="对所有敌人造成7点伤害。" + NL + "额外攻击等同构想数值次。" + NL + "（额外攻击1次）")),
    ("独特点子", dict(cost=1, costUp=1,
                   desc="造成4点伤害2次。" + NL + "将这张牌变化为一张随机小游戏牌。",
                   descUp="造成6点伤害2次。" + NL + "将这张牌变化为一张升级过的随机小游戏牌。",
                   note="无论是否升级，变化目标都是小游戏牌（升级后为升级版）；变化在打出完成进入弃牌堆后进行（不使用弹出式变化UI）。")),
    ("节奏大师", dict(name="节奏游戏！")),
    ("还施彼身", dict(name="针锋相对")),
]
COLS = ["name", "type", "rarity", "cost", "costUp", "desc", "descUp", "tag", "note", "flow"]

DUMP_ENTRIES = {
    "弹雨": dict(head="天马行空 | 攻击 | 普通 | 费用 1 -> 1 | flow: 构想流",
               desc="对所有敌人造成5点伤害。" + AR + "额外攻击等同构想数值次。" + AR + "（额外攻击0次）",
               descUp="对所有敌人造成7点伤害。" + AR + "额外攻击等同构想数值次。" + AR + "（额外攻击1次）"),
    "独特点子": dict(head="独特点子 | 攻击 | 罕见 | 费用 1 -> 1 | flow: ",
                 desc="造成4点伤害2次。" + AR + "将这张牌变化为一张随机小游戏牌。",
                 descUp="造成6点伤害2次。" + AR + "将这张牌变化为一张升级过的随机小游戏牌。"),
    "火焰附加": dict(head="火焰附加 | 能力 | 稀有 | 费用 1 -> 1 | flow: 灼烧流"),
    "节奏大师": dict(head="节奏游戏！ | 能力 | 衍生 | 费用 0 -> 0 | flow: "),
}


def main():
    dry = "--dry" in sys.argv
    os.makedirs(BAKDIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

    # ---------- xlsx ----------
    if not dry:
        shutil.copy2(XL, os.path.join(BAKDIR, "STS2Momoi_%s_pre_batch6.xlsx" % ts))
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

    # ---------- design dump ----------
    text = open(DUMP, encoding="utf-8").read()
    for old_name, e in DUMP_ENTRIES.items():
        pat = re.compile(r"### \[(\d+)\] " + re.escape(old_name) + r" \|.*?\n(?:desc:.*?\n)?(?:descUp:.*?\n)?(?:note:.*?\n)?")
        m = pat.search(text)
        if not m:
            print("dump 未找到:", old_name)
            continue
        lines = ["### [%s] %s" % (m.group(1), e["head"])]
        for key in ("desc", "descUp", "note"):
            if e.get(key):
                lines.append(key + ": " + e[key])
            else:
                # 保留原行（改名的卡：desc/descUp/note 不动）
                mm = re.search(r"^" + key + r": .*$", m.group(0), re.M)
                if mm:
                    lines.append(mm.group(0))
        text = text[:m.start()] + NL.join(lines) + NL + text[m.end():]
        print("dump [%s] %s -> 已改写" % (m.group(1), old_name))
    if not dry:
        open(DUMP, "w", encoding="utf-8").write(text)
    print("[dry-run]" if dry else "已写入")


if __name__ == "__main__":
    main()
