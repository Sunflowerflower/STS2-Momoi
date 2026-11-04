# -*- coding: utf-8 -*-
"""批次29 文档：根文档 §21.32 + 数字同步；工作区文档批次表 + 数字同步。
批次号：24/25/26 = 角色动画（10-17/18）、27 = 卡牌调整（10-20）、28 = 死亡AE/relaxed/像素UI（10-21）、
本批 = 29（2026-10-22）。"""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
P_MAIN = ROOT + r"\STS2_Momoi_迁移文档.md"
P_WS = ROOT + r"\工作区\_docs\STS2_Momoi_迁移文档.md"


def rep(path, old, new, label, count=1):
    d = io.open(path, encoding="utf-8").read()
    assert old in d, "没找到：" + label
    assert d.count(old) == count, "匹配数异常(%d)：%s" % (d.count(old), label)
    io.open(path, "w", encoding="utf-8").write(d.replace(old, new))
    print("  OK " + label)


# ---------------- 根文档 ----------------
rep(P_MAIN, "> **本次状态（2026-10-21 批次28）**",
 """> **本次状态（2026-10-22 批次29）**：卡牌调整批。**跑酷！**去掉「回合开始时重复」，**两个 power（含基类）+ 死图标 + 本地化键一起删除**（现在是 0 费一次性「选最多一张特定牌」）；数值：**WIN！** 能量 3/4、**火焰附加** 灼烧 2/3、**热身** 火力 2/3、**构想之矛** 10/14、**博览群游** 7/9、**再起新篇** 活力 3/4；稀有度：**瓶颈突破→普通**、**玩玩新作！→罕见**；**专注小重做** —— 判定从「连续 2 回合」改成 **本回合**，0 费（升级前后都是 0），卡面与 power 文本按用户措辞重写。
> ⚠ 同批还修了自检脚本的一次覆盖事故：新建 `_verify_batch28.py` 时与本会话（10-21）同名文件冲突，把动画批的自检覆盖了；已把本批脚本改名为 `_verify_batch29.py`，并按 §21.27 / §21.31 与磁盘实测**重建** `_verify_batch24.py`（idle，26 条）与 `_verify_batch28.py`（死亡AE/relaxed/像素头像/选人背景，46 条）。另发现 `工作区\\编辑区\\人物\\死亡动画.aep` 本体已不在磁盘（只剩日志目录与 `_work` 预览）。
> `dotnet build` **0 错误**，DLL **454,656 B** / PCK **115,402,920 B**；二十套自检 **831 条断言全绿**。详见 §21.32。
> **上一轮（2026-10-21 批次28）**""",
 "顶部状态块")

# 数据来源：加一行本批
rep(P_MAIN, "> - **2026-10-21 会话（批次28）**",
 "> - **2026-10-22 会话（批次29）**：跑酷删 power、六张数值卡、两个稀有度、专注重做（见 §21.32）。\n> - **2026-10-21 会话（批次28）**",
 "数据来源行")

# §1 部署版本
rep(P_MAIN, "| **当前部署版本** | `STS2_Momoi.dll` **454,656 B**（**10-20 22:31**）、`STS2_Momoi.pck` **109,989,948 B**（**10-20 22:32**）、`STS2_Momoi.json` 409 B |",
 "| **当前部署版本** | `STS2_Momoi.dll` **454,656 B**（**10-22 02:16**）、`STS2_Momoi.pck` **115,402,920 B**（**10-22 02:20**）、`STS2_Momoi.json` 409 B |",
 "§1 部署版本")

# 全局数字：834 -> 831、18 套 -> 20 套
d = io.open(P_MAIN, encoding="utf-8").read()
d = d.replace("18 套 / 834 条", "20 套 / 831 条")
d = d.replace("`_verify_batch9~28`（20 套 / 831 条断言；本批 102）", "`_verify_batch9~29`（20 套 / 831 条断言）")
d = d.replace("`_verify_batch9~28`（20 套 / 831 条断言）", "`_verify_batch9~29`（20 套 / 831 条断言）")
d = d.replace("``_verify_batch9~28`（18 套 / 834 条断言）`", "")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 834 -> 831 数字")

# §0.3 命令块：补 27/29 两行
rep(P_MAIN, '''"$PY" 工作区/_scripts/_verify_batch28.py         # 死亡 AE / relaxed 休息点 / 像素头像 / 选人背景（102 条）''',
 '''"$PY" 工作区/_scripts/_verify_batch28.py         # 死亡 AE / relaxed 休息点 / 像素头像 / 选人背景（46 条·重建）
"$PY" 工作区/_scripts/_verify_batch27.py         # 批次27：游戏人生标签作用域 / 六张数值 / UI 文本（56 条）
"$PY" 工作区/_scripts/_verify_batch29.py         # 批次29：跑酷删 power / 七张数值 / 专注重做（35 条）''',
 "§0.3 命令")

# §10 命令 + 套件表
rep(P_MAIN, "for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23 25 26 27; do",
 "for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29; do", "§10 命令")

rep(P_MAIN, """| `_verify_batch27.py` | **58** | **游戏人生标签作用域 + 六张数值卡 + 三处 UI 文本**（含标签闭合） |
| **合计** | **732** | 任一失败都要先查清是脚本过期还是代码回归，再继续 |""",
 """| `_verify_batch24.py` | 26 | **idle 帧序列**（42 帧 / 600×820 / 无损 / 接线；2026-10-22 重建） |
| `_verify_batch27.py` | 56 | 游戏人生标签作用域 + 六张数值卡 + 三处 UI 文本（含标签闭合） |
| `_verify_batch28.py` | 46 | 死亡AE 未部署 / relaxed 交替 / 像素头像 5 张 / 选人视频背景（2026-10-22 重建） |
| `_verify_batch29.py` | **35** | **跑酷删 power + 七张数值 + 两个稀有度 + 专注重做**（含标签闭合） |
| **合计** | **831** | 任一失败都要先查清是脚本过期还是代码回归，再继续 |""",
 "§10 套件表")

tail = """
### 21.32 批次29：跑酷删 power、七张数值卡、专注重做（2026-10-22）

#### 1. 跑酷！：删掉「回合开始时重复」，power 一并删除

原效果 = 打出时选一张 + 挂一个 power，每回合开始重复到受伤为止。按需求只留前半段：

- **删代码**：`ParkourPower` / `ParkourUpgradedPower` / 抽象基类 `ParkourPowerBase`（含 `BeforeHandDraw` 重复逻辑与 `AfterDamageReceived` 停止逻辑）全删；
  `OnPlay` 只 `await PickOne(...)`。
- **删死资源**：`images/powers/parkour_power.png`（+`.import`）、`powers.json` 里 6 个 `PARKOUR_POWER*` / `PARKOUR_UPGRADED_POWER*` 键（中英各 6 条）。
- **删本地化文本**：卡面第二行「在你的回合开始时，重复此效果，直至你受到伤害或失去生命。」（中英同步）。
- 现在是 **0 费一次性**（`消耗` 由 `CanonicalKeywords` 自动追加）：从 5 张随机特定牌里**选最多一张**（`MinSelect=0` 可跳过），本{回合|场战斗}免费。

#### 2. 六张卡的数值

| 卡 | 改动 |
|---|---|
| **WIN！** `WinCard` | 能量 4/6 → **3（升级 4，+1）** |
| **火焰附加** `FlameAttach` | 灼烧 1/2 → **2（升级 3）** |
| **热身** `WarmUp` | 火力 1/2 → **2（升级 3）** |
| **构想之矛** `ConceptSpear` | 伤害 8/11 → **10（升级 14，+4）** |
| **博览群游** `ExperienceCombo` | 伤害 8/11 → **7（升级 9，+2）** |
| **再起新篇** `NewChapter` | 活力 2/3 → **3（升级 4）** |

#### 3. 稀有度

- **瓶颈突破** `BottleneckBreak`：罕见 → **普通**
- **玩玩新作！** `Salvage`：普通 → **罕见**

#### 4. 专注：连续 2 回合 → 本回合

**旧**：`TurnsNoMinigame` / `TurnsNoConcept` 两个计数器累加，要求「连续 2 个回合」都没打出；
**新**：两个 bool（`PlayedMinigameThisTurn` / `PlayedConceptThisTurn`），**每个回合结束时各判定一次**：

| 判定 | 效果 |
|---|---|
| 本回合没打出过**小游戏牌** | 构想数值 +1（按层数叠加 `Amount`） |
| 本回合没打出过**构想** | 可选择最多（构想数值）张手牌**保留** —— 在 `BeforeSideTurnEnd`（弃牌前）判定 |
| 回合结束 | 两个标记重置 |

耗能 **0**（升级前后都是 0，`OnUpgrade` 因此没有内容）。卡面文本按用户给的措辞：

```
在你的回合结束时，若你本回合没有打出过[gold]小游戏牌[/gold]，使[gold]构想[/gold]数值+1。
在你的回合结束时，若你本回合没有打出过[gold]构想[/gold]，可选择最多[gold]构想[/gold]数值张[gold]手牌[/gold][gold]保留[/gold]。
```

power 文本同步（`{Amount}` / `{RetainCount}` 保留，小游戏牌/构想/手牌/保留 都染金）。

#### 5. ⚠ 自检脚本覆盖事故与恢复

本批新建自检时用了 `_verify_batch28.py`，与 **10-21 会话（批次28：死亡AE/relaxed/像素头像/选人背景）** 的同名脚本冲突 → 原文件被覆盖。
处理：

1. 本批脚本改名为 **`_verify_batch29.py`**（批次号对齐）。
2. 按 §21.31 与磁盘实测**重建** `_verify_batch28.py`（46 条：AEP 未部署 / relaxed 交替 1.1457856s / 5 张像素头像尺寸 / 两段 ogv + 两个 tscn / 音效接口）。
3. 一并重建 10-17 会话丢失的 `_verify_batch24.py`（26 条：42 张 idle 帧 / 600×820 RGBA / 无损导入 / IdleLoop·IdleOutro·三个倍率 / 开场主动播 idle）。
4. **发现**：`工作区\\编辑区\\人物\\死亡动画.aep` 本体已不在磁盘（只剩 `死亡动画.aep 日志` 目录与 `_work\\death_*` 预览/分层图），
   所以重建版脚本改成断言「审阅产物在 + 没有误部署」，不再断言 AEP 本体。

**教训**：新建自检脚本前先 `ls 工作区/_scripts/_verify_batch*.py` 看号段；本项目批次号已跨会话交叉使用（24~26 动画 / 27 卡牌 / 28 动画 / 29 卡牌）。

#### 6. 产物

- `dotnet build` **0 错误** → DLL **454,656 B**、PCK **115,402,920 B**（10-22 02:20）。
- `_verify_batch29.py` **35 条全绿**；**二十套合计 831 条断言全绿**。
- 同步修正的旧断言：`batch9`（PARKOUR power 行 / 吃豆人文本）、`batch11`（孤儿图标）、`batch14`（跑酷拆 power 一节改「已删除」）、
  `batch22`（专注改 0 费）、`batch27`（跑酷 power 文本 → 已删除）；`_power总览.md` 重生成（**52 个 power**）。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.32")

# ---------------- 工作区文档 ----------------
rep(P_WS, "| 部署 | `STS2_Momoi.dll` **454,656 B**（10-20 22:31）、`STS2_Momoi.pck` **109,989,948 B**（10-20 22:32） |",
 "| 部署 | `STS2_Momoi.dll` **454,656 B**（10-22 02:16）、`STS2_Momoi.pck` **115,402,920 B**（10-22 02:20） |",
 "工作区 部署行")

d = io.open(P_WS, encoding="utf-8").read()
d = d.replace("| 自检 | 18 套 / **759 条断言全绿**", "| 自检 | 20 套 / **831 条断言全绿**")
d = d.replace("for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23 25 26 27; do",
              "for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29; do")
d = d.replace("# 18 套自检（759 条断言", "# 20 套自检（831 条断言")
d = d.replace("跑自检 18 套（759 条断言）", "跑自检 20 套（831 条断言）")
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区 数字同步")

row29 = ("| 29 | 10-22 | 跑酷删「回合开始时重复」+ **两个 power/基类/死图标/本地化键全删**；WIN！3/4、火焰附加灼烧 2/3、"
         "热火力 2/3、构想之矛 10/14、博览群游 7/9、再起新篇活力 3/4；瓶颈突破→普通、玩玩新作！→罕见；"
         "**专注小重做**（连续 2 回合 → 本回合，0 费，卡面/power 文本重写）；自检脚本覆盖事故已恢复（重建 24/28） |")
d = io.open(P_WS, encoding="utf-8").read()
anchor = "> 批次 24~26 是**角色动画**"
assert anchor in d
d = d.replace(anchor, row29 + "\n\n" + anchor, 1)
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区 批次表加一行")
