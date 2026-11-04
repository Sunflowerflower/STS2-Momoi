# -*- coding: utf-8 -*-
"""批次30 文档：根文档 §21.34 + 数字同步；工作区文档批次表 + 数字同步。"""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
P_MAIN = ROOT + r"\STS2_Momoi_迁移文档.md"
P_WS = ROOT + r"\工作区\_docs\STS2_Momoi_迁移文档.md"


def rep(path, old, new, label):
    d = io.open(path, encoding="utf-8").read()
    assert old in d, "没找到：" + label
    assert d.count(old) == 1, "多处(%d)：%s" % (d.count(old), label)
    io.open(path, "w", encoding="utf-8").write(d.replace(old, new))
    print("  OK " + label)


# ---------------- 根文档 ----------------
rep(P_MAIN, "> **本次跟进（2026-10-22 批次28b）**",
 """> **本次状态（2026-10-22 批次30）**：**专注**最终定稿 —— 耗能**回到 1 费（升级 0 费）**；卡面与 power 文本都**并成一句**（照「蒙太奇」那种「A/B，X/Y」的写法，不再重复两遍「在你的回合结束时」）：
> `在你的回合结束时，若你本回合没有打出过小游戏牌/构想，使构想数值+1/选择最多构想数值张牌保留。`（power 侧的构想加值用 `{Amount}`、保留张数仍用 `{RetainCount}` 显示实际数值）。
> **天马行空**升级版卡面补上「+1」：`额外攻击等同构想数值{IfUpgraded:show:+1|}次`（升级前不带，实际效果本来就是升级 +1 次，未改代码）。
> `dotnet build` **0 错误**，DLL **454,656 B** / PCK **115,635,008 B**；二十一套自检 **888 条断言全绿**。详见 §21.34。
> **上一轮（2026-10-22 批次28b）**""",
 "顶部状态块")

rep(P_MAIN, "> - **2026-10-22 会话（批次29）**：跑酷删 power、六张数值卡、两个稀有度、专注重做（见 §21.32）。",
 "> - **2026-10-22 会话（批次29）**：跑酷删 power、六张数值卡、两个稀有度、专注重做（见 §21.32）。\n"
 "> - **2026-10-22 会话（批次30）**：专注 1 费 + 卡面/power 文本合成一句、天马行空升级版补「+1」（见 §21.34）。",
 "数据来源行")

rep(P_MAIN, "| **当前部署版本** | `STS2_Momoi.dll` **454,656 B**（**10-22 02:16**）、`STS2_Momoi.pck` **115,402,920 B**（**10-22 02:20**）、`STS2_Momoi.json` 409 B |",
 "| **当前部署版本** | `STS2_Momoi.dll` **454,656 B**（**10-22 04:29**）、`STS2_Momoi.pck` **115,635,008 B**（**10-22 04:29**）、`STS2_Momoi.json` 409 B |",
 "§1 部署版本")

# 全量数字：867 -> 888、20 套 -> 21 套
d = io.open(P_MAIN, encoding="utf-8").read()
d = d.replace("（20 套 / **867** 条断言）", "（21 套 / **888** 条断言）")
d = d.replace("`_verify_batch9~29`", "`_verify_batch9~30`")
d = d.replace("# 全量 20 套 / 867 条", "# 全量 21 套 / 888 条")
d = d.replace("```", "```")  # no-op
d = d.replace("for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29; do",
              "for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 867 -> 888 数字")

rep(P_MAIN, '''"$PY" 工作区/_scripts/_verify_batch29.py         # 批次29：跑酷删 power / 七张数值 / 专注重做（35 条）''',
 '''"$PY" 工作区/_scripts/_verify_batch29.py         # 批次29：跑酷删 power / 七张数值 / 专注重做（35 条）
"$PY" 工作区/_scripts/_verify_batch30.py         # 批次30：专注 1 费 + 单句文本 / 天马行空升级 +1（21 条）''',
 "§0.3 命令")

# §10 套件表：在 batch29 行后补 batch30，并改合计
rep(P_MAIN, """| `_verify_batch29.py` | **35** | **跑酷删 power + 七张数值 + 两个稀有度 + 专注重做**（含标签闭合） |
| **合计** | **831** | 任一失败都要先查清是脚本过期还是代码回归，再继续 |""",
 """| `_verify_batch29.py` | 35 | 跑酷删 power + 七张数值 + 两个稀有度 + 专注重做（含标签闭合） |
| `_verify_batch30.py` | **21** | **专注 1 费 + 卡面/power 单句文本 + 天马行空升级版「+1」** |
| **合计** | **888** | 任一失败都要先查清是脚本过期还是代码回归，再继续 |""",
 "§10 套件表")

tail = """
### 21.34 批次30：专注 1 费 + 文本并成一句、天马行空升级版补「+1」（2026-10-22）

#### 1. 专注：耗能改回 1 费（升级 0 费）

上一批我按「升级前后都 0 费」改过头了，用户更正为 **1 费 / 升级 0 费**：
`base(1, …)` + `OnUpgrade → EnergyCost.UpgradeBy(-1)`。

#### 2. 专注：卡面 / power 文本并成一句

旧写法把「在你的回合结束时」说了两遍，字数过多。照**蒙太奇**那种「A/B，X/Y」的写法合成一句：

```
在你的回合结束时，若你本回合没有打出过[gold]小游戏牌[/gold]/[gold]构想[/gold]，使[gold]构想[/gold]数值+1/选择最多[gold]构想[/gold]数值张牌[gold]保留[/gold]。
```

**power 侧**同句式，只把两个数字换成变量（**保留张数仍显示实际数值** —— 用户一开始就要求「最多构思数值张」的数值要实时显示）：

```
在你的回合结束时，若你本回合没有打出过[gold]小游戏牌[/gold]/[gold]构想[/gold]，使[gold]构想[/gold]数值+[blue]{Amount}[/blue]/选择最多[blue]{RetainCount}[/blue]张牌[gold]保留[/gold]。
```

- `{RetainCount}` 的刷新逻辑没动（`AfterCardPlayed` 与 `BeforeSideTurnEnd` 各写一次当前构想数值）。
- 效果判定仍是「**本回合**」两个 bool（批次29 的改法），只改文案。
- 按新措辞去掉了旧文本里的「[gold]手牌[/gold]」（用户写的是「张牌」）。

#### 3. 天马行空：升级版卡面补「+1」

实际效果本来就是「构想数值 + 升级 +1 次」（`HitsBase` 0 → 升级 +1），只是升级版卡面漏了这个 +1：

```
对所有敌人造成{CalculatedDamage:diff()}点伤害。
额外攻击等同[gold]构想[/gold]数值{IfUpgraded:show:+1|}次。（额外攻击{ExtraHits:diff()}次）
```

升级前不显示（`{IfUpgraded:show:+1|}` 的空分支），代码未改。

#### 4. 产物

- `dotnet build` **0 错误** → DLL **454,656 B**、PCK **115,635,008 B**（10-22 04:29）。
- `_verify_batch30.py` **21 条全绿**；二十一套合计 **888 条断言全绿**。
- 同步修正旧断言：`batch22`（专注 1 费 + 升级 -1）、`batch29`（专注费用与「单句」结构、power 关键词不再含「手牌」）。

> 注：`_verify_batch28.py` 已由 10-22 的动画会话改写为 82 条的「死亡节奏/商店 relaxed/休息处新图」版本，本批未动它。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.34")

# ---------------- 工作区文档 ----------------
d = io.open(P_WS, encoding="utf-8").read()
d = d.replace("| 部署 | `STS2_Momoi.dll` **454,656 B**（10-22 02:16）、`STS2_Momoi.pck` **115,402,920 B**（10-22 02:20） |",
              "| 部署 | `STS2_Momoi.dll` **454,656 B**（10-22 04:29）、`STS2_Momoi.pck` **115,635,008 B**（10-22 04:29） |")
d = d.replace("| 自检 | 20 套 / **831 条断言全绿**", "| 自检 | 21 套 / **888 条断言全绿**")
d = d.replace("for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29; do",
              "for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do")
d = d.replace("# 20 套自检（831 条断言", "# 21 套自检（888 条断言")
d = d.replace("跑自检 20 套（831 条断言）", "跑自检 21 套（888 条断言）")
row30 = ("| 30 | 10-22 | **专注**回到 1 费（升级 0），卡面与 power 文本**并成一句**（`小游戏牌/构想，+1/选择最多…`，"
         "power 侧 `{Amount}` + `{RetainCount}` 仍显示实际数值）；**天马行空**升级版卡面补「等同构想数值**+1**次」 |")
anchor = "> 批次 24~26 是**角色动画**"
assert anchor in d
d = d.replace(anchor, row30 + "\n\n" + anchor, 1)
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
