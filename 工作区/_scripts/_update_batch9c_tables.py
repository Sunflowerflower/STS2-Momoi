# -*- coding: utf-8 -*-
"""2026-10-12 批次9c：同步 xlsx（序章 / 吃豆人 / 构想）

用法：py -3 _update_batch9c_tables.py [--dry]
"""
import os, re, sys, shutil, datetime
import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
XL = os.path.join(ROOT, "工作区", "STS2Momoi.xlsx")
DUMPF = os.path.join(ROOT, "工作区", "_design_dump.txt")
BAKDIR = os.path.join(ROOT, "工作区", "_backup", "_xlsx_backup")
NL, AR = chr(10), " ⏎ "

FULL = [
    # 序章：固有升级前后都有；升级改为删去消耗
    ("序章", 7, "固有。" + NL + "当前每有一名敌人，就使构想数值+1。" + NL + "消耗。"),
    ("序章", 8, "固有。" + NL + "当前每有一名敌人，就使构想数值+1。"),
    ("序章", 10, "固有升级前后都有（写在 CanonicalKeywords 里）；消耗只有未升级时有 —— "
     "升级效果改为 **删去消耗**（OnUpgrade 里 LocalKeywords.Remove(CardKeyword.Exhaust)），"
     "不再是「升级获得固有」。"),

    # 吃豆人：补注绿色卡名
    ("吃豆人！", 10, "4张诅咒：苦恼、睡眠不佳、羞耻、贪婪。" + NL +
     "先检测有没有诅咒牌：有才打出疯狂进食并消耗1张诅咒牌；没有就不打疯狂进食，直接给富足。" + NL +
     "疯狂进食用复制品（CreateDupe）打出：不进弃牌堆、也不进消耗堆，打完直接消失（机制同原版历史课 HistoryCourse）。" + NL +
     "能力侧栏里的「疯狂进食」卡名取自 ModelDb.Card<FeedingFrenzy>()（写成 Maul 会显示成「撕咬」，批次9b 已修）。" + NL +
     "升级后的描述里「疯狂进食+」「富足+」**整个卡名是绿的**：把整个名字放进 {IfUpgraded:show:...|} 的第一个分支"
     "（ShowIfUpgradedFormatter 在 UpgradePreview 模式下只给分支内容套 [green]；名字留在外面就只有那个 + 号变绿），"
     "并且第一个分支自己写 [green]…[/green]，保证正常显示升级版时也绿。" + NL +
     "（设计理念：经典吃豆人有4个幽灵，颜色分别为红粉蓝橙，正好对应战骨机储，也对应这4张诅咒）"),

    # 构想：补注「局内不显示当前数值」
    ("构想", 10, "构想回合开始的效果为构想自身效果（每张构想各自+1/+2并按自身数值添加诅咒）；初始遗物只负责添加构想。"
     "特定诅咒：3苦恼/4睡眠不佳/5疑虑/6+执迷。构想机制：多张构想时取最大值。" + NL +
     "描述里**不要**再写 {InCombat:…（当前数值…）}：局内会多出一行「（当前数值0）」很难看（批次9c 已删）。"),
]


def main():
    dry = "--dry" in sys.argv
    os.makedirs(BAKDIR, exist_ok=True)
    if not dry:
        shutil.copy2(XL, os.path.join(BAKDIR, "STS2Momoi_%s_pre_batch9c.xlsx"
                                      % datetime.datetime.now().strftime("%Y-%m-%d_%H%M")))
    wb = openpyxl.load_workbook(XL)
    ws = wb["卡牌"]
    row_of = {}
    for r in range(3, ws.max_row + 1):
        v = ws.cell(row=r, column=2).value
        if v:
            row_of.setdefault(str(v), r)
    n = 0
    for name, col, txt in FULL:
        r = row_of.get(name)
        if r is None:
            print("  !! xlsx 未找到:", name); continue
        ws.cell(row=r, column=col).value = txt
        n += 1
    if not dry:
        wb.save(XL)
    print("xlsx 改动 %d 处" % n)

    text = open(DUMPF, encoding="utf-8").read()
    m = 0
    for name in sorted(set(x[0] for x in FULL)):
        r = row_of.get(name)
        if r is None:
            continue
        desc = ws.cell(row=r, column=7).value or ""
        descUp = ws.cell(row=r, column=8).value or ""
        note = ws.cell(row=r, column=10).value
        pat = re.compile(r"### \[(\d+)\] " + re.escape(name) + r" \|.*?\n(?:(?:desc|descUp|note):.*\n?)*")
        mm = pat.search(text)
        if not mm:
            print("  -- dump 无此条（跳过）:", name); continue
        lines = [mm.group(0).splitlines()[0],
                 "desc: " + desc.replace(NL, AR),
                 "descUp: " + descUp.replace(NL, AR)]
        if note:
            lines.append("note: " + str(note).replace(NL, AR))
        text = text[:mm.start()] + NL.join(lines) + NL + NL + text[mm.end():]
        m += 1
    if not dry:
        open(DUMPF, "w", encoding="utf-8").write(text)
    print("dump 改写 %d 条" % m, "[dry-run]" if dry else "已写入")


if __name__ == "__main__":
    main()
