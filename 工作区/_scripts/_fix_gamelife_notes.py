# -*- coding: utf-8 -*-
"""2026-10-11（追加）：游戏人生 的「游戏牌」标签改为「只在本场战斗生效、不写回牌组本尊」，
同步表格/ dump 里的备注。用法：py -3 _fix_gamelife_notes.py"""
import os, re
import openpyxl

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
XL = os.path.join(ROOT, "工作区", "STS2Momoi.xlsx")
DUMPF = os.path.join(ROOT, "工作区", "_design_dump.txt")

OLD_NOTE_XL = ("已经是游戏牌或小游戏牌的牌不会进入选择界面；本牌自己不是游戏牌/小游戏牌，也可以被自己添加。"
               "标签同时写在牌组本尊上（本局后续战斗仍算游戏牌）；描述顶行的金色「游戏牌。」由 CardKeywordLabelPatch 按标签自动显示。")
NEW_NOTE_XL = ("已经是游戏牌或小游戏牌的牌不会进入选择界面；本牌自己不是游戏牌/小游戏牌，也可以被自己添加。"
               "标签**只作用于本场战斗的这张牌**（不写回牌组本尊，战斗结束即失效）；"
               "描述顶行的金色「游戏牌。」由 CardKeywordLabelPatch 按标签自动显示。")

OLD_NOTE_DUMP = "已是游戏牌/小游戏牌的牌不进选择界面；标签同时写在牌组本尊上；描述顶行金色「游戏牌。」由补丁按标签显示。"
NEW_NOTE_DUMP = "已是游戏牌/小游戏牌的牌不进选择界面；标签只作用于本场战斗的这张牌（不写回牌组本尊）；描述顶行金色「游戏牌。」由补丁按标签显示。"

wb = openpyxl.load_workbook(XL)
ws = wb["卡牌"]
row = next((r for r in range(3, ws.max_row + 1) if ws.cell(row=r, column=2).value == "游戏人生"), None)
if row:
    cur = ws.cell(row=row, column=10).value
    if cur == OLD_NOTE_XL:
        ws.cell(row=row, column=10).value = NEW_NOTE_XL
        print("xlsx 行%d 备注已更新" % row)
    else:
        print("xlsx 行%d 备注与预期不同，实际：" % row, repr(cur)[:200])
    wb.save(XL)
else:
    print("xlsx 未找到 游戏人生")

t = open(DUMPF, encoding="utf-8").read()
if OLD_NOTE_DUMP in t:
    t = t.replace(OLD_NOTE_DUMP, NEW_NOTE_DUMP)
    open(DUMPF, "w", encoding="utf-8").write(t)
    print("dump [57] 备注已更新")
else:
    print("dump 备注与预期不同")
