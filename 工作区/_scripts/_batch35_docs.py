# -*- coding: utf-8 -*-
"""批次35 文档：根文档 §21.40 + 数字/套件表同步；工作区文档批次表 + 数字同步。
批次号说明：24~26 动画、27 卡牌、28 动画、29~30 卡牌、31~34 动画/美术（10-22~23）、本批 = 35（2026-10-24）。"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
P_MAIN = ROOT + r"\STS2_Momoi_迁移文档.md"
P_WS = ROOT + r"\工作区\_docs\STS2_Momoi_迁移文档.md"

SUITES = "9 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 35"
TOTAL = 1020
COUNT = 24


def rep(path, old, new, label):
    d = io.open(path, encoding="utf-8").read()
    assert old in d, "没找到：" + label
    assert d.count(old) == 1, "多处(%d)：%s" % (d.count(old), label)
    io.open(path, "w", encoding="utf-8").write(d.replace(old, new))
    print("  OK " + label)


# ---------------- 根文档 ----------------
rep(P_MAIN, "> **本次状态（2026-10-23 批次34）**",
 """> **本次状态（2026-10-24 批次35）**：卡牌调整小批。**剧本打击**的括号数改为跟着升级走 —— 和「天马行空」的（额外攻击 0 次 / 1 次）一致，现在局内外都显示（**抽0张牌 / 抽1张牌**）；做法是把升级的 +1 从 `ConceptCards` 的 multiplier 挪到 `CardsBase`（`CalculatedVar` 局外 multiplier 记 0，原来局外一律显示「抽0张牌」），并去掉文本里的 `{InCombat:…}` 包装。**重整旗鼓**自动打出的血量阈值 **20% → 25%**（卡与 power 两处判定 + 中英文本 + 注释，升级前后都是 25%，其他效果没动）。
> ⚠ 又一次自检脚本覆盖：新建 `_verify_batch31.py` 与 10-22 动画批同名，已把本批脚本改名 `_verify_batch35.py`，并按 §21.35 重建 `_verify_batch31.py`（死亡 50 帧 / 能量图标 24·256 / 多人手臂 422×1200，24 条）。
> `dotnet build` **0 错误**，DLL **476,672 B** / PCK **127,960,540 B**；二十四套自检 **1020 条断言全绿**。详见 §21.40。
> **上一轮（2026-10-23 批次34）**""",
 "顶部状态块")

# 数据来源行（加在本批前一条之前）
rep(P_MAIN, "> - **2026-10-22 会话（批次30）**：专注 1 费 + 卡面/power 文本合成一句、天马行空升级版补「+1」（见 §21.34）。",
 "> - **2026-10-22 会话（批次30）**：专注 1 费 + 卡面/power 文本合成一句、天马行空升级版补「+1」（见 §21.34）。\n"
 "> - **2026-10-24 会话（批次35）**：剧本打击括号数跟升级（0/1）、重整旗鼓阈值 20%→25%（见 §21.40）。",
 "数据来源行")

rep(P_MAIN, "| **当前部署版本** | `STS2_Momoi.dll` **454,656 B**（**10-22 04:29**）、`STS2_Momoi.pck` **115,635,008 B**（**10-22 04:29**）、`STS2_Momoi.json` 409 B |",
 "| **当前部署版本** | `STS2_Momoi.dll` **476,672 B**（**10-24 03:17**）、`STS2_Momoi.pck` **127,960,540 B**（**10-24 03:17**）、`STS2_Momoi.json` 409 B |",
 "§1 部署版本")

# §10 命令（用当前全部套件列表 + 脚本逐个跑更稳）
d = io.open(P_MAIN, encoding="utf-8").read()
d = re.sub(r'for v in [0-9 ]+; do "\$PY" "工作区/_scripts/_verify_batch\$v\.py" \| tail -1; done',
           'for f in 工作区/_scripts/_verify_batch*.py; do "$PY" "$f" | tail -1; done   # 全部 %d 套 / %d 条' % (COUNT, TOTAL),
           d)
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK §10 命令（改成通配遍历）")

# §10 套件表：整段替换（旧表已被多份会话改乱）
old_tail = "| **合计** | **889** | 任一失败都要先查清是脚本过期还是代码回归，再继续 |"
new_table = """| `_verify_batch28.py` | 92 | 死亡节奏 / relaxed 商店 / 休息处新图 / 像素头像 / 选人背景 / PCK |
| `_verify_batch29.py` | 36 | 跑酷删 power + 七张数值 + 两个稀有度 + 专注重做 |
| `_verify_batch30.py` | 21 | 专注 1 费 + 卡面/power 单句文本 + 天马行空升级版「+1」 |
| `_verify_batch31.py` | 24 | **死亡动画 50 帧 / 能量图标 24·256 / 多人手臂 422×1200**（2026-10-24 重建） |
| `_verify_batch32.py` | 76 | 角色身份/头像/能量/多人手势/镜像 + 文本参考 |
| `_verify_batch35.py` | **21** | **剧本打击括号数跟升级（0/1）+ 重整旗鼓阈值 25%** |
| **合计** | **1020**（24 套） | 任一失败都要先查清是脚本过期还是代码回归，再继续 |"""
rep(P_MAIN, old_tail, new_table, "§10 套件表尾部")

# §0 里的旧套件数
d = io.open(P_MAIN, encoding="utf-8").read()
d = d.replace("（21 套 / **889** 条断言）", "（%d 套 / **%d** 条断言）" % (COUNT, TOTAL))
d = d.replace("`_verify_batch9~30`", "`_verify_batch*.py`")
d = d.replace("# 全量 21 套 / 889 条", "# 全量 %d 套 / %d 条" % (COUNT, TOTAL))
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK §0 套件数字")

tail = """
### 21.40 批次35：剧本打击括号数跟升级、重整旗鼓阈值 25%（2026-10-24）

#### 1. 剧本打击：括号里的抽牌数改成跟着升级走（0 张 / 1 张）

**现象**：卡面第二句已经写了「抽等同构想数值{IfUpgraded:show:+1|}张牌」，但括号里那句被 `{InCombat:…}` 包着，
**局外**（牌组/奖励/商店里看）固定走 else 分支，升级版也显示「（抽0张牌）」。

**修法**（与「天马行空」完全一致：升级的 +1 放在 base 变量上，而不是写在 multiplier 里）：

```csharp
// 之前：multiplier 里自算 +1 → 局外 multiplier 记 0，升级版也显示 0
new IndependentCalculatedVar("ConceptCards", cardsBase, cardsExtra)
    .WithMultiplier((card, _) => ConceptCounterCapability.GetMaxCountInHand(card.Owner.Creature) + (card.IsUpgraded ? 1 : 0));

// 现在：照着天马行空（HitsBase 0 → 升级 +1）的写法
.WithMultiplier((card, _) => ConceptCounterCapability.GetMaxCountInHand(card.Owner.Creature));

protected override void OnUpgrade()
{
    DynamicVars.CalculationBase.UpgradeValueBy(2);
    DynamicVars["CardsBase"].UpgradeValueBy(1);   // 抽牌数 +1（局内外都显示）
}
```

- 局外：`CardsBase` = **0 / 1** → 显示「（抽0张牌）/（抽1张牌）」✓
- 局内：`CardsBase + 1 × 构想数值` = 构想数值（+1 升级）✓ 与实际抽牌一致（`OnPlay` 仍读 `ConceptCards`）
- 文本去掉 `{InCombat:…}`：`……张牌。\\n（抽{ConceptCards:diff()}张牌）`

#### 2. 重整旗鼓：自动打出阈值 20% → 25%

两处判定（升级前后都是同一段代码，所以两版一起变；其它效果一律没动）：

| 位置 | 旧 | 新 |
|---|---|---|
| 卡 `RallyAgain.TryAutoPlayIfLowHp` | `if (me.CurrentHp > me.MaxHp / 5) return;` | `if (me.CurrentHp > me.MaxHp / 4) return;` |
| power `RallyAgainPower.AfterDamageReceived` | `if (Owner.CurrentHp * 5 >= Owner.MaxHp) return;` | `if (Owner.CurrentHp * 4 >= Owner.MaxHp) return;` |

中文文本「当生命值低于20%时…」→「低于25%时」，英文 `below 20%` → `below 25%`，注释同步。

#### 3. ⚠ 又一次自检脚本覆盖（第三次）

本批新建自检时又用了已存在的号：`_verify_batch31.py`（10-22 动画批：死亡 50 帧 / 能量图标 / 多人手臂）。
处理：

1. 本批脚本改名 **`_verify_batch35.py`**（批次号对齐当前最新 §21.38 / 批次34）。
2. 按 §21.35 与磁盘实测**重建** `_verify_batch31.py`（24 条：dead 50 帧 1400×1250 / `DeadFrameCount=50` / `DeadSpeed` / 不循环 / energy_text 24×24 / energy_big 256×256 / 4 张手臂 422×1200 / 审阅图 / AEP 不在 PCK 源目录）。

**新规矩（写进流程）**：新建自检前先 `ls 工作区/_scripts/_verify_batch*.py` **并**看根文档最新 `### 21.x 批次NN`，取 `NN+1` 命名；已发生 3 次同名覆盖（24、28、31）。

#### 4. 产物

- `dotnet build` **0 错误** → DLL **476,672 B**、PCK **127,960,540 B**（10-24 03:17）。
- `_verify_batch35.py` **21 条全绿**；**二十四套合计 1020 条断言全绿**（实测，逐个跑）。
- 文档 §10 的套件表/命令改为「按通配遍历全部脚本」，避免再出现表内数字与实际脚本数量对不上的情况。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.40")

# ---------------- 工作区文档 ----------------
d = io.open(P_WS, encoding="utf-8").read()
d = re.sub(r"\| 部署 \|.*\|", "| 部署 | `STS2_Momoi.dll` **476,672 B**（10-24 03:17）、`STS2_Momoi.pck` **127,960,540 B**（10-24 03:17） |", d, count=1)
d = re.sub(r"\| 自检 \|.*\|", "| 自检 | **24 套 / 1020 条断言全绿**（`_verify_batch*.py`；含动画批 24~26/28/31/32） |", d, count=1)
d = d.replace("# 21 套自检（889 条断言；任一套失败先查清是脚本过期还是代码回归）",
              "# 全部自检（24 套 / 1020 条；任一套失败先查清是脚本过期还是代码回归）")
d = re.sub(r'for v in [0-9 ]+; do "\$PY" "工作区/_scripts/_verify_batch\$v\.py" \| tail -1; done',
           'for f in 工作区/_scripts/_verify_batch*.py; do "$PY" "$f" | tail -1; done', d)
d = d.replace("跑自检 21 套（889 条断言）", "跑全部自检（24 套 / 1020 条断言）")
row35 = ("| 35 | 10-24 | **剧本打击**括号数跟着升级（0 张 / 1 张，+1 从 multiplier 挪到 `CardsBase`，去掉 `{InCombat:…}`）；"
         "**重整旗鼓**自动打出阈值 **20% → 25%**（卡 + power 两处判定、中英文本、注释）；自检脚本第三次同名覆盖已恢复（重建 batch31） |")
anchor = "> 批次 24~26 是**角色动画**"
if anchor in d:
    d = d.replace(anchor, row35 + "\n\n" + anchor, 1)
else:
    d = d.rstrip("\n") + "\n" + row35 + "\n"
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
