# -*- coding: utf-8 -*-
"""从 xlsx（权威）重建 _design_dump.txt

背景：dump 是给后续会话读的「设计快照」，但它早已与 xlsx 脱节 ——
索引停在旧编号（重整旗鼓 dump 里是 [101]、xlsx 实际是第 94 项），
还有 36 张卡在 xlsx 里、dump 里没有；dump 里另有 25 条是 xlsx 已改名的旧卡。
本脚本以 xlsx 为唯一来源整份重建，并把旧 dump 备份到 _session_export 边上的 _backup 目录。

用法：py -3 _sync_design_dump.py [--dry]
"""
import os, sys, shutil, datetime, re
import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
XL = os.path.join(ROOT, "工作区", "STS2Momoi.xlsx")
OUT = os.path.join(ROOT, "工作区", "_design_dump.txt")
BAKDIR = os.path.join(ROOT, "工作区", "_backup", "_dump_backup")
NL, AR = chr(10), " ⏎ "


def cell(ws, r, c, default=""):
    v = ws.cell(row=r, column=c).value
    if v is None:
        return default
    return str(v).strip()


def main():
    dry = "--dry" in sys.argv
    wb = openpyxl.load_workbook(XL)
    ws = wb["卡牌"]
    entries = []
    for r in range(3, ws.max_row + 1):
        name = ws.cell(row=r, column=2).value
        if not name:
            continue
        idx = r - 3
        head = "### [%d] %s | %s | %s | 费用 %s -> %s | flow: %s" % (
            idx, str(name).strip(), cell(ws, r, 3), cell(ws, r, 4),
            cell(ws, r, 5), cell(ws, r, 6), cell(ws, r, 11))
        body = ["desc: " + cell(ws, r, 7).replace(NL, AR),
                "descUp: " + cell(ws, r, 8).replace(NL, AR),
                "note: " + cell(ws, r, 10).replace(NL, AR)]
        entries.append(head + NL + NL.join(body))
    text = (NL + NL).join(entries) + NL

    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    old_names = set(re.findall(r"^### \[\d+\] (.+?) \|", old, re.M))
    new_names = set(re.findall(r"^### \[\d+\] (.+?) \|", text, re.M))
    print("xlsx 卡数 %d；新 dump 条目 %d" % (len(entries), len(new_names)))
    print("旧 dump 有、新 dump 没有（已改名/已删）:", sorted(old_names - new_names))
    print("新 dump 新增:", len(new_names - old_names))
    if dry:
        print("[dry-run] 不写入")
        return
    os.makedirs(BAKDIR, exist_ok=True)
    if old:
        shutil.copy2(OUT, os.path.join(BAKDIR, "_design_dump_%s.txt"
                                       % datetime.datetime.now().strftime("%Y-%m-%d_%H%M")))
    open(OUT, "w", encoding="utf-8").write(text)
    print("已重建 ->", OUT)


if __name__ == "__main__":
    main()
