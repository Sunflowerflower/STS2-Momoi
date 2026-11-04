# -*- coding: utf-8 -*-
"""2026-10-12 批次9b：同步 xlsx + 设计 dump（在批次9 的基础上修正）

  * 双线叙事：删「1层」；备注说明「固有。/消耗。 由关键词自动追加，描述里不要手写」
  * 吃豆人！：按用户原文（不加「直接打出」）
  * 秒人斧 / 渔获：删「打出时，」
  * 绝地求生：主行显示最大值（已在上批），本次备注补充
  * 植物大战僵尸：0c（不是 0+图标 两次）
用法：py -3 _update_batch9b_tables.py [--dry]
"""
import os, re, sys, shutil, datetime
import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
XL = os.path.join(ROOT, "工作区", "STS2Momoi.xlsx")
DUMPF = os.path.join(ROOT, "工作区", "_design_dump.txt")
BAKDIR = os.path.join(ROOT, "工作区", "_backup", "_xlsx_backup")
NL, AR = chr(10), " ⏎ "

KW_NOTE = ("描述里**不要**手写「固有。」「消耗。」—— 这两个词由关键词自动追加"
           "（原版 CardModel 的 CardKeywordOrder：beforeDescription 插在最前、afterDescription 接在最后），"
           "写了会在卡面上重复显示两次（本批修过这个 bug）。")

FULL = [
    ("双线叙事", 7, "固有。" + NL + "使构想数值+2。" + NL +
     "选择1张构想复制，并为被复制的构想添加重放，然后为复制品附魔灵魂之力。" + NL + "消耗。"),
    ("双线叙事", 8, "固有。" + NL + "使构想数值+2。" + NL +
     "选择1张构想复制，并为被复制的构想添加重放，然后为复制品附魔灵魂之力。" + NL + "消耗。"),
    ("双线叙事", 10, "只复制**选中的那一张**构想（不再复制手牌里所有构想）。"
     "被复制的**原构想**获得**重放**（已有重放则次数+1，写法同原版重构 Transfigure 的 BaseReplayCount++）；"
     "复制品不加任何重放，只附魔灵魂之力。初始牌「剧情推进！」通过先古遗物古老牙齿变化为此牌。升级：耗费1c→0c。" + NL + KW_NOTE),

    ("吃豆人！", 7, "将4张特定诅咒加入你的手牌。" + NL +
     "在你的回合开始时，若你有诅咒牌，则打出1张疯狂进食并随机消耗你的1张诅咒牌；"
     "若你没有诅咒牌则改为将1张富足加入你的手牌。"),
    ("吃豆人！", 8, "将4张特定诅咒加入你的手牌。" + NL +
     "在你的回合开始时，若你有诅咒牌，则打出1张疯狂进食+并随机消耗你的1张诅咒牌；"
     "若你没有诅咒牌则改为将1张富足+加入你的手牌。"),
    ("吃豆人！", 10, "4张诅咒：苦恼、睡眠不佳、羞耻、贪婪。" + NL +
     "先检测有没有诅咒牌：有才打出疯狂进食并消耗1张诅咒牌；没有就不打疯狂进食，直接给富足。" + NL +
     "疯狂进食用复制品（CreateDupe）打出：不进弃牌堆、也不进消耗堆，打完直接消失（机制同原版历史课 HistoryCourse）。" + NL +
     "能力侧栏里的「疯狂进食」卡名取自 ModelDb.Card<FeedingFrenzy>()（写成 Maul 会显示成「撕咬」，本批已修）。" + NL +
     "（设计理念：经典吃豆人有4个幽灵，颜色分别为红粉蓝橙，正好对应战骨机储，也对应这4张诅咒）"),

    ("秒人斧", 7, "造成999点伤害。" + NL + "从你的牌组中移除这张牌。"),
    ("秒人斧", 8, "造成999点伤害。" + NL + "从你的牌组中移除这张牌。" + NL + "保留。"),
    ("秒人斧", 10, "移除自身：打出时**立即**移除牌组中的本尊（复制品 IsClone 不移除）。"
     "在 OnPlay 里 await 掉 CardPileCmd.RemoveFromDeck，而不是在 GetResultLocationForCardPlay 里 fire-and-forget —— "
     "这样即使这一斧直接把敌人砍死、战斗立刻结束，移除也已经结算完。" + NL +
     "DeckVersion 为空时（控制台 / FreeLoadout 直接塞手牌的实例）退化为按卡 ID 在牌组里找一张同名牌移除。"),

    ("渔获", 10, "移除自身同秒人斧：打出时立即移除牌组中的本尊；复制品 IsClone 不移除；"
     "DeckVersion 为空时按卡 ID 兜底。注意描述里不写「打出时，」。"),

    ("绝地求生", 7, "抽4张牌，获得3c。" + NL +
     "你的手牌中每有一张其他牌，此牌的数值就降低1点。（抽0张牌，获得0c）" + NL + "消耗。"),
    ("绝地求生", 8, "抽5张牌，获得4c。" + NL +
     "你的手牌中每有一张其他牌，此牌的数值就降低1点。（抽0张牌，获得0c）" + NL + "消耗。"),
    ("绝地求生", 10, "主行显示的是**最大值**（图鉴里也显示最大值）；括号里是实时数值。"
     "实现：静态 DynamicVar Cards=4 / EnergyVar Energy=3 当主行（升级各 +1），"
     "CalculatedVar 的 Calculate() 在非战斗状态恒返回 0，所以只能放括号里。" + NL + KW_NOTE),

    ("植物大战僵尸", 7, "从随机两张特定牌中选择一张放入你的手牌，下回合将另一张牌放入你的手牌。"
     "它们的耗能在下次打出前变为0c。"),
    ("植物大战僵尸", 8, "从随机两张升级过的特定牌中选择一张放入你的手牌，下回合将另一张牌放入你的手牌。"
     "它们的耗能在下次打出前变为0c。"),
    ("植物大战僵尸", 10, "描述里的 {Energy:energyIcons()} 需要卡上有 Energy 变量才能解析，"
     "所以 CanonicalVars 里加了 new EnergyVar(0)；写成「0{Energy:energyIcons()}」会渲染成 00c。"),
]


def main():
    dry = "--dry" in sys.argv
    os.makedirs(BAKDIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    if not dry:
        shutil.copy2(XL, os.path.join(BAKDIR, "STS2Momoi_%s_pre_batch9b.xlsx" % ts))
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
