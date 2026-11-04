# -*- coding: utf-8 -*-
"""批次41 文档：§21.48 + 数字/套件表同步。"""
import io
import re
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


rep(P_MAIN, "> **本次状态（2026-10-25 批次40）**",
 """> **本次状态（2026-10-25 批次41）**：**多段攻击的活力/火力重复消耗修好了**。真因是把多段拆成了多条 `AttackCommand`：
> `VigorPower.BeforeAttack` 只给第一条命令记快照，`AfterAttack` 一次把层数扣光，后面几条命令只能吃残值。
> **创作的痛苦**：删去上一批加的「获得 2/3 层火力」；三段合成**一条命令**（`WithHitCount(3)` + `WithWaitBeforeHit(0.5f, 0.5f)`），
> 段间 0.5s 间隔与每段弹幕/命中特效都保持原样（故意**不**加 `OnlyPlayAnimOnce`，否则每段弹幕也只会播一次）。
> **100连抽！**：100 次伤害也是 100 条命令（同样的活力 bug + 每条命令都播一次攻击动画，卡顿）→ 合成 `WithHitCount(Repeat)` + `OnlyPlayAnimOnce()`。
> 顺手把全部模组卡扫了一遍：其余多段牌（来自妮露的援护 / 捕鱼达人 / 激战 / 街啪6 各分支）本来就是 `WithHitCount` 单命令 ✓。
> `dotnet build` **0 错误**，DLL **500,736 B** / PCK **131,853,468 B**；二十八套自检 **1222 条断言全绿**。详见 §21.48。
> **上一轮（2026-10-25 批次40）**""",
 "顶部状态块")

rep(P_MAIN, "> - **2026-10-25 会话（批次40）**：一批卡牌费用/数值/机制、新卡「传送门悖论」与「过载」、建筑师打斗演出（见 §21.47）。",
 "> - **2026-10-25 会话（批次40）**：一批卡牌费用/数值/机制、新卡「传送门悖论」与「过载」、建筑师打斗演出（见 §21.47）。\n"
 "> - **2026-10-25 会话（批次41）**：创作的痛苦删火力、多段攻击合成单条命令（活力只扣一次）、100连抽同修（见 §21.48）。",
 "数据来源行")

d = io.open(P_MAIN, encoding="utf-8").read()
d = re.sub(r"\| \*\*当前部署版本\*\* \|.*\|",
           "| **当前部署版本** | `STS2_Momoi.dll` **500,736 B**（**10-25 22:29**）、`STS2_Momoi.pck` **131,853,468 B**（**10-25 22:30**）、`STS2_Momoi.json` 409 B |",
           d, count=1)
d = d.replace("27 套 / **1201** 条", "28 套 / **1222** 条")
d = d.replace("全部 27 套 / 1201 条", "全部 28 套 / 1222 条")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 部署版本 + 套件数字")

rep(P_MAIN, """| `_verify_batch40.py` | **62** | **本批全部卡牌改动 + 传送门悖论 + 过载 + 建筑师打斗补丁** |
| **合计** | **1201**（27 套） |""",
 """| `_verify_batch40.py` | 62 | 批次40 全部卡牌改动 + 传送门悖论 + 过载 + 建筑师打斗补丁 |
| `_verify_batch41.py` | **21** | **创作痛苦删火力 + 多段合成单命令 + 全卡多命令扫描** |
| **合计** | **1222**（28 套） |""",
 "§10 套件表")

tail = """
### 21.48 批次41：多段攻击的活力/火力重复消耗（创作的痛苦 / 100连抽）（2026-10-25）

#### 1. 根本原因

把一张多段攻击**拆成多条 `AttackCommand`** 时：

- `VigorPower.BeforeAttack` 只在**第一条**命令上记下 `commandToModify` 与 `amountWhenAttackStarted`；
- 这条命令执行完进入 `AfterAttack` 时，**一次把全部层数扣光**；
- 后面几条命令里 `base.Amount` 已经是 0 → 它们只能吃残值。

所以玩家看到的是「活力/火力只作用在第 1 段，而且被扣了多次/一次扣光」。正确写法是 **一条命令 + `WithHitCount(n)`**，
段间间隔用 `WithWaitBeforeHit(fast, standard)`，动画只播一次用 `OnlyPlayAnimOnce()`。

#### 2. 创作的痛苦！`CreativePain`

| 项 | 处理 |
|---|---|
| 上一批加的「获得 2/3 层火力」 | **删掉**（变量、升级、OnPlay 施加、卡面 `Firepower` 行、中英文本） |
| 三段攻击 | `for` 循环发 3 条命令 → **一条命令** `.WithHitCount(3)` |
| 段间 0.5s | `Cmd.CustomScaledWait(0.5f, 0.5f)` + 拆分 → **`.WithWaitBeforeHit(0.5f, 0.5f)`**（间隔不变） |
| 每段弹幕 / 命中特效 | 仍走 `MomoiGunStyle.ApplyBarrage` 的 `WithAttackerFx` / `WithHitVfxNode`（每段各一次） |
| ⚠ 注意 | **故意不加 `OnlyPlayAnimOnce()`** —— 原版那个开关只控制「攻击者侧特效/动画」是否每段播放，加了会把每段弹幕也一起关掉 |

> 细微差别：`WithWaitBeforeHit` 在**每一段（含第一段）** 的命中特效/伤害前等待，所以第一段伤害比原来晚 0.5s；
> 但「段间隔 0.5s」和「第一段弹幕立刻出现」都保持不变。

#### 3. 100连抽！`HundredPull`

100 次伤害原本是 `for` 循环发 **100 条** `AttackCommand`：
同样的活力 bug（只有第 1 次吃到）+ 每条命令都播一次攻击动画（卡顿）。

改成一条命令：`.WithHitCount(DynamicVars.Repeat.IntValue)` + `.OnlyPlayAnimOnce()`（命中特效 `vfx_giant_horizontal_slash` 每段照常）。

> ⚠ **平衡变化提示**：合成一条命令后，活力按「多段攻击」的正常规则**对每一段都生效**（活力 5 → 100 段共 +500 伤害）。
> 这是原版多段牌的语义；如果觉得过强，可以把这张牌改成 `WithHitCount(1)` 的固定伤害或限制段数。

#### 4. 全模组扫描（其余多段牌）

| 卡 | 现状 |
|---|---|
| 来自妮露的援护 | `WithHitCount(Hits)` ✓ 本来就对 |
| 捕鱼达人！ | `WithHitCount(hits)` ✓ |
| 激战 | `WithHitCount(Hits)` ✓ |
| 街啪6 | 每个能量分支各一条命令（一次打出只走一个分支）✓ |
| 来自晴 / 来自茜的援护 | 只是「对群一条命令」，不是多命令 ✓ |
| 节奏游戏！power 的回合末攻击 | 一条命令 ✓ |
| 来自勇者的加护 / 我复活啦 / 后续任务 等 | 单命令 ✓ |

扫描脚本（写进 `_verify_batch41.py` 第 4 节）：遍历所有 `ModCardTemplate` 的类体，
若一次 `OnPlay` 里出现「>1 条 `DamageCmd.Attack(`」或「循环体里发攻击命令」就报错 —— 目前**零告警**。

#### 5. 产物

- `dotnet build` **0 错误** → DLL **500,736 B**、PCK **131,853,468 B**（10-25 22:30）。
- 新增 `_verify_batch41.py` **21 条**；同步修正过期断言：`batch32`（创作痛苦由循环改成 `WithHitCount`+`WithWaitBeforeHit`）、`batch40`（创作痛苦已删火力）。
- **二十八套合计 1222 条断言全绿**。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.48")

# 工作区文档
d = io.open(P_WS, encoding="utf-8").read()
d = re.sub(r"\| 部署 \|.*\|", "| 部署 | `STS2_Momoi.dll` **500,736 B**（10-25 22:29）、`STS2_Momoi.pck` **131,853,468 B**（10-25 22:30） |", d, count=1)
d = re.sub(r"\| 自检 \|.*\|", "| 自检 | **28 套 / 1222 条断言全绿**（`_verify_batch*.py` 通配逐个跑） |", d, count=1)
d = d.replace("跑全部自检（27 套 / 1201 条断言）", "跑全部自检（28 套 / 1222 条断言）")
row = ("| 41 | 10-25 | **多段攻击的活力/火力重复消耗修好**（拆多条 `AttackCommand` → `VigorPower.BeforeAttack` 只记第一条、"
       "`AfterAttack` 一次扣光）；创作的痛苦删去火力、三段改 `WithHitCount(3)`+`WithWaitBeforeHit(0.5,0.5)`（间隔不变、"
       "不加 OnlyPlayAnimOnce 保住每段弹幕）；100连抽 100 段同样合并 + OnlyPlayAnimOnce；全卡扫描零告警 |")
anchor = "> 批次 24~26 是**角色动画**"
if anchor in d:
    d = d.replace(anchor, row + "\n\n" + anchor, 1)
else:
    d = d.rstrip("\n") + "\n" + row + "\n"
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
