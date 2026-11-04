# -*- coding: utf-8 -*-
"""批次23 文档：根文档 + 工作区文档 追加记录，更新自检套件数字。"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
P_MAIN = ROOT + r"\STS2_Momoi_迁移文档.md"
P_WS = ROOT + r"\工作区\_docs\STS2_Momoi_迁移文档.md"


def rep(path, old, new, label):
    d = open(path, encoding="utf-8").read()
    assert old in d, "没找到：" + label
    assert d.count(old) == 1, "多处匹配：" + label
    open(path, "w", encoding="utf-8").write(d.replace(old, new))
    print("  OK " + label)


# ---------------- 根文档 ----------------
rep(P_MAIN, "> **本次状态（2026-10-16 批次22）**",
    """> **本次状态（2026-10-16 批次23）**：文本收尾两处 —— **「击晕」补成金色关键词**（3 张：来自哈雷的援护、来自千寻的援护、破势；侧栏本来就有，是 `StunIntent.GetStaticHoverTip()`）；**「终于上一档了！」的金币补金色**（`{IfUpgraded:show:25|20}[gold]金币[/gold]`，两处），**金币不加侧栏**（补丁的关键词扫描表里本来就没有金币/Gold，与原版一致）。`dotnet build` **0 错误**，DLL **442,880 B** / PCK **75,402,280 B**；十四套自检 **549 条断言全绿**。详见 §21.26。
> **上一轮（2026-10-16 批次22）**""",
    "顶部状态块")

rep(P_MAIN, "| 自检 | `工作区\\_scripts\\_verify_batch{9,11..22}.py`（13 套 / 524 条断言） |",
    "| 自检 | `工作区\\_scripts\\_verify_batch{9,11..23}.py`（14 套 / 549 条断言） |",
    "§1 自检行（若存在）")

# 自检套件表
rep(P_MAIN, "| `_verify_batch20~22.py` | 28 / 17 / 43 | 阿比舒（4 倍倍率 + 3 段）、曳光弹与费用、批次 22 全项 + 标签闭合 |\n| **合计** | **524** | 任一失败都要先查清是脚本过期还是代码回归，再继续 |",
    "| `_verify_batch20~23.py` | 28 / 17 / 43 / 25 | 阿比舒（4 倍倍率 + 3 段）、曳光弹与费用、批次 22 全项、**金色关键词收尾（击晕 / 金币）** + 标签闭合 |\n| **合计** | **549** | 任一失败都要先查清是脚本过期还是代码回归，再继续 |",
    "§10 套件表")

rep(P_MAIN, "for v in 9 11 12 13 14 15 16 17 18 19 20 21 22; do \"$PY\" \"工作区/_scripts/_verify_batch$v.py\" | tail -1; done",
    "for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23; do \"$PY\" \"工作区/_scripts/_verify_batch$v.py\" | tail -1; done",
    "§10 命令")

# §0 里的数字
d = open(P_MAIN, encoding="utf-8").read()
d = d.replace("（13 套 / 524 条断言）", "（14 套 / 549 条断言）")
d = d.replace("DLL **442,880 B** / PCK **75,402,024 B**", "DLL **442,880 B** / PCK **75,402,280 B**")
open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK §0 数字同步")

# 追加 §21.26
tail = """
### 21.26 批次23：金色关键词收尾（击晕 / 金币）（2026-10-16）

| 卡 | 改动 |
|---|---|
| 来自哈雷的援护 `MomoiSupportHare` | `[gold]击晕[/gold]所有敌人。` |
| 来自千寻的援护 `MomoiSupportChihiro` | `…[gold]击晕[/gold]该敌人。` |
| 破势 `MomentumBreak` | `…[gold]击晕[/gold]该敌人并将…`（承接批次 22 的文本） |
| 终于上一档了！ `RankUp` | `战斗结束后额外获得{IfUpgraded:show:25|20}[gold]金币[/gold]与一组卡牌奖励。\\n如果下个回合结束前未能结束战斗，则只能额外获得{IfUpgraded:show:15|10}[gold]金币[/gold]。` |

- 英文同步 `[gold]Stun[/gold]` / `[gold]Gold[/gold]`（与 `RANK_UP_POWER` 里已有的写法一致）。
- **击晕的侧栏是现成的**：`Patches\\MinigameSidebarPatch.cs` 里 `Has("击晕", "Stun") || Has("眩晕", "Stun")` → `StunIntent.GetStaticHoverTip()`，本次没有动它。
- **金币不加侧栏**：补丁的关键词扫描表里本来就没有「金币 / Gold」，所以上色纯粹是显示效果，符合原版（原版金币也没有侧栏）。
- 全表复核：`cards` 里已无裸的「击晕 / Stun / 金币 / Gold」正文（`GOLD_MINER.title` = "Gold Miner!" 是卡名，不动；`GOLD_MINER.sidebar2` 里还有一处「25金币/25 gold」属于**该卡侧栏**，**按「不擅自修改」原则未动**，见下方备注）。

**产物**：`dotnet build` 0 错误 → DLL **442,880 B**、PCK **75,402,280 B**（10-16 17:15）；`_verify_batch23.py` **25 条全绿**，十四套合计 **549 条**。

> 备注（待用户裁决，未自行修改）：`STS2_MOMOI_CARD_GOLD_MINER.sidebar2`（金币矿工·升级后说明）里有「每有1点耗能，战斗结束就额外获得25金币。」，
> 其中的「金币」与同段落的「能量 / 手牌」都没有 `[gold]`；如果要统一，可以一并补上（属于该卡侧栏文本，只影响显示）。
"""
d = open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.26")

# ---------------- 工作区文档 ----------------
rep(P_WS, "| 部署 | `STS2_Momoi.dll` **442,880 B**（10-16 16:01）、`STS2_Momoi.pck` **75,402,024 B**（10-16 16:02） |",
    "| 部署 | `STS2_Momoi.dll` **442,880 B**（10-16 17:15）、`STS2_Momoi.pck` **75,402,280 B**（10-16 17:15） |",
    "工作区文档 部署行")

rep(P_WS, "| 自检 | 13 套 / **524 条断言全绿**（`_verify_batch9.py`、`11~22`） |",
    "| 自检 | 14 套 / **549 条断言全绿**（`_verify_batch9.py`、`11~23`） |",
    "工作区文档 自检行")

rep(P_WS, "for v in 9 11 12 13 14 15 16 17 18 19 20 21 22; do \"$PY\" \"工作区/_scripts/_verify_batch$v.py\" | tail -1; done",
    "for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23; do \"$PY\" \"工作区/_scripts/_verify_batch$v.py\" | tail -1; done",
    "工作区文档 命令")

rep(P_WS, "（13 套 / 524 条断言）", "（14 套 / 549 条断言）", "工作区文档 §2.2 数字")

open(P_WS, "a", encoding="utf-8").write("""
---

## 6. 最近三批（卡牌调整期）

| 批次 | 日期 | 内容 |
|---|---|---|
| 20 | 10-15 | 阿比舒最后一段的 4 倍改成真乘法（`ModifyDamageMultiplicative` 门控 `_finalHit`）、勇者加护 11→10 伤、消消乐首句缩短；期间一次文件截断事故已从 `_backup/batch15_pre` 完整恢复 |
| 21 | 10-15 | 阿比舒 3 段修复（`CreatureCmd.Damage` 一次只结算一次）、曳光弹数值（6/8 伤、3/4 灼烧、每 1 点活力 +1 层）、来自时的援助 2→0 费、阿比舒 0→1 费 |
| 22 | 10-16 | 曳光弹升级灼烧真因（`DynamicVar.Clone()` 浅拷贝 → `IndependentCalculatedVar` 改为按名字实时解析）、破势重做（2 费、16/20、活力 4/5 倍走新补丁 `VigorMultiplierPatch`）、整活补「升级过的」、吃豆人诅咒查三堆、堕落改罕见+1 层虚弱、独特点子改普通、专注 1→0 费、博览群游 0→1 费 |
| 23 | 10-16 | 「击晕」补金色（3 张，侧栏已有）、「终于上一档了！」金币补金色（**不加侧栏**，与原版一致） |

> 文档同步：本文件写「现状 + 后续重心」，逐批细节在仓库根 `STS2_Momoi_迁移文档.md` §21。
""")
print("  OK 工作区文档追加批次表")
