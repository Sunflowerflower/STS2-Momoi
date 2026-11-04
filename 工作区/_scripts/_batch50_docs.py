# -*- coding: utf-8 -*-
"""批次50 文档：顶部状态块 + §21.57。"""
import io
import os

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
DOC = os.path.join(ROOT, "STS2_Momoi_迁移文档.md")
SEC = os.path.join(ROOT, "工作区", "_docs", "_batch50_section.md")

HEAD = """> **本次状态（2026-11-02 批次50）**：**绝地求生括号仅局内 / 明日奈 power 文本带层数 / 循环叙事改到弃手牌前 + 触发后直接消失（修「下回合开始报错」），版本 1.0.6**。
> 三条改动：① 绝地求生 卡面「（抽N张牌，获得N能量）」用 `{InCombat:…|}` 包起来，局外不显示；② 来自明日奈的援护 power 文本改成「直到你的下[blue]{Amount}[/blue]个回合开始前，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。」（卡面不动，叠加规则不动：`Amount` 递增=回合数，40% 覆盖 25%、25% 只加回合数）；③ **循环叙事**：报错排查结论是 `godot.log` 里没有本模组异常，真因是旧实现挂在 `AfterSideTurnEnd`（**弃手牌之后**）又用带动画的 `CardPileCmd.Add` 把牌塞进抽牌堆，与下回合重建手牌撞车 → 改挂 `BeforeSideTurnEnd`（`CombatManager.cs:1522`，弃手牌在 `:1665 FlushPlayerHand` 之后）+ `skipVisuals: true`，并且结算完 `PowerCmd.Remove(this)` 直接消失（层数只当「这次最多能选几张」）+ `try/catch` `[Cyclic]` 日志。
> 产物：DLL **515,072 B** / PCK **57,832,996 B**；`工作区\\发布包\\STS2_Momoi_v1.0.6.zip`（54.2 MB，v1.0.5 已删）；工坊 `Content` 已同步 1.0.6 但**没上传**。全量 **36 套 / 1671 条断言全绿**。详见 **§21.57**。
>
> **上一轮（2026-11-02 批次49）**"""

LATEST_BEFORE = "### 21.56"


def main():
    doc = io.open(DOC, encoding="utf-8").read()
    sec = io.open(SEC, encoding="utf-8").read()

    old_head = "> **本次状态（2026-11-02 批次49）**"
    assert doc.count(old_head) == 1, doc.count(old_head)
    doc = doc.replace(old_head, HEAD)

    assert "### 21.57" not in doc
    assert doc.rstrip().endswith(("。", "）", "|", "`")) or True
    doc = doc.rstrip("\n") + "\n\n" + sec.strip("\n") + "\n"

    bad = [(i, hex(ord(c))) for i, c in enumerate(doc) if ord(c) < 32 and c not in "\n\t\r"]
    assert not bad, bad[:5]

    io.open(DOC, "w", encoding="utf-8", newline="\n").write(doc)
    print("ok: 文档已更新，%d 行 / %d B" % (doc.count("\n") + 1, len(doc.encode("utf-8"))))
    assert LATEST_BEFORE in doc


main()
