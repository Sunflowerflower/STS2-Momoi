# -*- coding: utf-8 -*-
"""2026-10-05：同步 工作区\\STS2Momoi.xlsx 与 工作区\\_design_dump.txt
  * 私人订制 → 堕落（普通，0c）
  * 便携式掩体 → 王不见王（罕见，1c→0c）
  * 游戏学习 → 开发秘籍（仅改名，效果不变）
用法：python _update_batch5_tables.py [--dry]
"""
import os, shutil, sys, datetime, re
import openpyxl

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
XL = os.path.join(ROOT, "工作区", "STS2Momoi.xlsx")
DUMP = os.path.join(ROOT, "工作区", "_design_dump.txt")
BAKDIR = os.path.join(ROOT, "工作区", "_backup", "_xlsx_backup")
NL = chr(10)      # xlsx 内的换行
AR = " ⏎ "        # dump 内的换行符

# 列：2 名称 / 3 类型 / 4 稀有度 / 5 耗费 / 6 升级耗费 / 7 描述 / 8 升级后描述 / 9 标签 / 10 备注 / 11 流派
XLSX_ROWS = [
    ("私人订制", dict(name="堕落", type="技能", rarity="普通", cost=0, costUp=0,
                   desc="给予自身1层脆弱。" + NL + "将一张随机小游戏牌加入你的手牌。",
                   descUp="给予自身1层脆弱。" + NL + "将一张升级过的随机小游戏牌加入你的手牌。",
                   tag=None,
                   note="脆弱：从卡牌中获得的格挡值减少25%（原版同名状态）。随机小游戏牌为 12 种小游戏牌之一；升级后加入的是升级版。",
                   flow=None)),
    ("便携式掩体", dict(name="王不见王", type="技能", rarity="罕见", cost=1, costUp=0,
                    desc="获得1层缓冲。" + NL + "你在接下来的1回合内无法再从卡牌中获得格挡。",
                    descUp="（耗能 1c→0c，其余同基础效果）",
                    tag=None,
                    note="「无法从卡牌中获得格挡」参考原版无色技能「应急按钮」（同一 NoBlockPower，1 回合）。",
                    flow=None)),
    ("游戏学习", dict(name="开发秘籍", type=None, rarity=None, cost=None, costUp=None,
                   desc=None, descUp=None, tag=None, note=None, flow=None)),
]
COLS = ["name", "type", "rarity", "cost", "costUp", "desc", "descUp", "tag", "note", "flow"]

DUMP_ENTRIES = {
    "精挑细选": dict(head="堕落 | 技能 | 普通 | 费用 0 -> 0 | flow: ",
                  desc="给予自身1层脆弱。" + AR + "将一张随机小游戏牌加入你的手牌。",
                  descUp="给予自身1层脆弱。" + AR + "将一张升级过的随机小游戏牌加入你的手牌。",
                  note="脆弱：从卡牌中获得的格挡值减少25%（原版同名状态）。随机小游戏牌为 12 种小游戏牌之一。"),
    "快找掩体！": dict(head="王不见王 | 技能 | 罕见 | 费用 1 -> 0 | flow: ",
                  desc="获得1层缓冲。" + AR + "你在接下来的1回合内无法再从卡牌中获得格挡。",
                  descUp="（耗能 1c→0c，其余同基础效果）",
                  note="「无法从卡牌中获得格挡」参考原版无色技能「应急按钮」（同一 NoBlockPower，1 回合）。"),
    "游戏学习": dict(head="开发秘籍 | 能力 | 罕见 | 费用 3 -> 3 | flow: 游戏流" + NL + "构想流",
                  desc=None, descUp=None, note=None),
}


def main():
    dry = "--dry" in sys.argv
    os.makedirs(BAKDIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

    # ---------- xlsx ----------
    if not dry:
        shutil.copy2(XL, os.path.join(BAKDIR, "STS2Momoi_%s_pre_batch5.xlsx" % ts))
    wb = openpyxl.load_workbook(XL)
    ws = wb["卡牌"]
    for old_name, row in XLSX_ROWS:
        target = None
        for r in range(3, ws.max_row + 1):
            if ws.cell(row=r, column=2).value == old_name:
                target = r
                break
        if target is None:
            print("xlsx 未找到:", old_name)
            continue
        for i, key in enumerate(COLS):
            if row[key] is not None:
                ws.cell(row=target, column=2 + i).value = row[key]
        print("xlsx 行%-4d %s → %s" % (target, old_name, row["name"]))
    if not dry:
        wb.save(XL)

    # ---------- design dump ----------
    text = open(DUMP, encoding="utf-8").read()
    for old_name, e in DUMP_ENTRIES.items():
        pat = re.compile(r"### \[(\d+)\] " + re.escape(old_name) + r" \|.*?\n(?:desc:.*?\n)(?:descUp:.*?\n)(?:note:.*?\n)?")
        m = pat.search(text)
        if not m:
            print("dump 未找到:", old_name)
            continue
        lines = ["### [%s] %s" % (m.group(1), e["head"])]
        if e["desc"]:
            lines.append("desc: " + e["desc"])
        if e["descUp"]:
            lines.append("descUp: " + e["descUp"])
        if e["note"]:
            lines.append("note: " + e["note"])
        new_block = NL.join(lines) + NL
        # 保留原有的 desc/descUp/note（改名的卡）
        text = text[:m.start()] + new_block + text[m.end():]
        print("dump 条目[%s] %s → 已改写" % (m.group(1), old_name))
    if not dry:
        open(DUMP, "w", encoding="utf-8").write(text)
    print("[dry-run]" if dry else "已写入")


if __name__ == "__main__":
    main()
