# -*- coding: utf-8 -*-
"""导出 xlsx 卡牌 sheet 中指定卡名的行（用于比对/更新）"""
import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
wb = openpyxl.load_workbook(ROOT + r"\工作区\STS2Momoi.xlsx")
ws = wb["卡牌"]
hdr = [ws.cell(row=2, column=c).value for c in range(1, 16)]
print("表头:", hdr)
NAMES = sys.argv[1:] or None
for r in range(3, ws.max_row + 1):
    n = ws.cell(row=r, column=2).value
    if not n:
        continue
    if NAMES and str(n) not in NAMES:
        continue
    print("=" * 70)
    print("row", r)
    for c in range(1, 16):
        v = ws.cell(row=r, column=c).value
        if v not in (None, ""):
            print("  C%-2d %-12s %s" % (c, hdr[c - 1], repr(v)))
