# -*- coding: utf-8 -*-
"""
2026-10-04：STS2Momoi.xlsx 卡牌表同步
  * 第 9 行「天意侵蚀」→ 原地改为「严肃绷住」（保留行样式）
  * 末尾追加 3 张衍生牌：绷到我了 / 轻松绷住 / 我还能绷五万年呢
用法：python _xlsx_update_beng.py
"""
import os, shutil, datetime
import openpyxl

XL = r"C:\Users\asus\RiderProjects\STS2 Momoi\工作区\STS2Momoi.xlsx"
BAKDIR = r"C:\Users\asus\RiderProjects\STS2 Momoi\工作区\_xlsx_backup"
NL = chr(10)

# 列：2 名称 / 3 类型 / 4 稀有度 / 5 耗费 / 6 升级耗费 / 7 描述 / 8 升级后描述 / 9 标签 / 10 备注 / 11 流派
ROW9 = {
    "name": "严肃绷住",
    "type": "技能",
    "rarity": "普通",
    "cost": 0, "costUp": 0,
    "desc": "获得4点格挡。" + NL + "将一张绷到我了加入你的手牌。",
    "descUp": "获得6点格挡。" + NL + "将一张绷到我了+加入你的手牌。",
    "tag": None,
    "note": "「绷住」链第 1 张：绷到我了 → 轻松绷住 → 我还能绷五万年呢，逐级加入手牌；升级版加入的衍生牌同样是升级版。",
    "flow": None,
}

NEW_ROWS = [
    {
        "name": "绷到我了", "type": "技能", "rarity": "衍生",
        "cost": 0, "costUp": 0,
        "desc": "失去1点生命。" + NL + "获得5点格挡。" + NL + "将一张轻松绷住加入你的手牌。",
        "descUp": "失去1点生命。" + NL + "获得7点格挡。" + NL + "将一张轻松绷住+加入你的手牌。",
        "tag": None,
        "note": "「绷住」链第 2 张（严肃绷住衍生）。失去生命同原版放血（不可格挡、不受能力修正）。",
        "flow": None,
    },
    {
        "name": "轻松绷住", "type": "技能", "rarity": "衍生",
        "cost": 0, "costUp": 0,
        "desc": "获得2点格挡。" + NL + "抽1张牌。" + NL + "你在本回合内不能再抽牌。" + NL + "将一张我还能绷五万年呢加入你的手牌。",
        "descUp": "获得3点格挡。" + NL + "抽1张牌。" + NL + "你在本回合内不能再抽牌。" + NL + "将一张我还能绷五万年呢+加入你的手牌。",
        "tag": None,
        "note": "「绷住」链第 3 张（绷到我了衍生）。本回合禁止抽牌参考原版战斗专注（抽完 1 张后再上限制）。",
        "flow": None,
    },
    {
        "name": "我还能绷五万年呢", "type": "技能", "rarity": "衍生",
        "cost": 1, "costUp": 1,
        "desc": "虚无。" + NL + "获得5点格挡。" + NL + "在下个回合获得5点格挡。" + NL + "结束你的回合。",
        "descUp": "虚无。" + NL + "获得7点格挡。" + NL + "在下个回合获得7点格挡。" + NL + "结束你的回合。",
        "tag": None,
        "note": "「绷住」链第 4 张（轻松绷住衍生）。虚无。下回合格挡参考闪躲翻滚（BlockNextTurnPower，可叠加）。",
        "flow": None,
    },
]

COLS = ["name", "type", "rarity", "cost", "costUp", "desc", "descUp", "tag", "note", "flow"]


def main():
    os.makedirs(BAKDIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    bak = os.path.join(BAKDIR, "STS2Momoi_%s_pre_beng.xlsx" % ts)
    shutil.copy2(XL, bak)
    print("备份 ->", bak)

    wb = openpyxl.load_workbook(XL)
    ws = wb["卡牌"]

    # 1) 第 9 行原地替换
    for i, key in enumerate(COLS):
        ws.cell(row=9, column=2 + i).value = ROW9[key]
    print("行9:", ws.cell(row=9, column=2).value)

    # 2) 追加 3 行（样式抄最后一行）
    template_row = ws.max_row
    start = template_row + 1
    for n, row in enumerate(NEW_ROWS):
        r = start + n
        for i, key in enumerate(COLS):
            c = 2 + i
            src = ws.cell(row=template_row, column=c)
            dst = ws.cell(row=r, column=c)
            dst.value = row[key]
            if src.has_style:
                dst._style = src._style
        print("行%d: %s [%s]" % (r, row["name"], row["rarity"]))

    wb.save(XL)
    print("已保存。卡牌表总行数:", ws.max_row)


if __name__ == "__main__":
    main()
