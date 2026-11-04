# -*- coding: utf-8 -*-
"""批次46 文档：§21.53 + 数字同步 + 发布清单 1.0.3。"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
P_MAIN = ROOT + r"\STS2_Momoi_迁移文档.md"
P_WS = ROOT + r"\工作区\_docs\STS2_Momoi_迁移文档.md"
P_REL = ROOT + r"\工作区\_docs\_发布清单.md"


def rep(path, old, new, label):
    d = io.open(path, encoding="utf-8").read()
    assert old in d, "没找到：" + label
    assert d.count(old) == 1, "多处(%d)：%s" % (d.count(old), label)
    io.open(path, "w", encoding="utf-8").write(d.replace(old, new))
    print("  OK " + label)


rep(P_MAIN, "> **本次状态（2026-10-28 批次45）**",
 """> **本次状态（2026-10-28 批次46）**：**黄金矿工修好 + 一批数值/文本，版本 1.0.3**。
> **黄金矿工！**：费用 **1/0 → 0/0**（升级只给保留）；**关键 bug 修复** —— 原来用 `EnergyCost.Canonical`（卡面印的费），
> 现在改用 **`EnergyCost.GetWithModifiers(CostModifiers.All)`** 读当前耗能，所以「剧情推进！+」（升级后 0 费）消耗时正确给「巨石+」。
> 数值/费用：瓶颈突破 **5/5 → 4/4**、见识下我的实力吧 **1/0 → 0/0**、日复一日 **3/2 → 3/3**、灵感爆发 **1/1 → 1/0**、来自勇者的加护 **8/10 → 6/9**。
> 文本：**火力爆发 / 剧本打击 / 天马行空 / 博览群游** 的括号内容一律套 `{InCombat:\\n（…）|}`，**图鉴里不显示、局内才显示**（照原版 BARRAGE/BODY_SLAM 的写法）；
> **构想之矛 power** 的每点伤害 8/11 → **11/15**；**矛与盾卡面伤害** 8/11 → **11/15**（power 早已是 11/15）；**开荒** 卡面「未获得过」→「未生成过」、侧栏改成「将依次生成以下诅咒：…」（诅咒仍红）；**相遇** 的「铸造 / 生成」按关键词染金（eng: Forge / Channel）。
> **卡牌统计（本批实测）**：角色卡池 **91** 张 + 衍生牌 **44** 张 = **135** 张；其中**小游戏牌 14**、游戏牌 6。
> `dotnet build` **0 错误**，DLL **508,416 B** / PCK **131,855,024 B**；三十二套自检 **1389 条断言全绿**。
> **发布包**：`工作区\\发布包\\STS2_Momoi_v1.0.3.zip`（125.0 MB）。详见 §21.53。
> **上一轮（2026-10-28 批次45）**""",
 "顶部状态块")

rep(P_MAIN, "> - **2026-10-28 会话（批次45）**：注能回退成 AutoPlay、衍生牌图鉴问号修复、版本 1.0.2 发布包（见 §21.52）。",
 "> - **2026-10-28 会话（批次45）**：注能回退成 AutoPlay、衍生牌图鉴问号修复、版本 1.0.2 发布包（见 §21.52）。\n"
 "> - **2026-10-28 会话（批次46）**：黄金矿工读当前耗能、费用/数值批、仅局内括号、卡牌统计、版本 1.0.3（见 §21.53）。",
 "数据来源行")

d = io.open(P_MAIN, encoding="utf-8").read()
d = re.sub(r"\| \*\*当前部署版本\*\* \|.*\|",
           "| **当前部署版本** | `STS2_Momoi.dll` **508,416 B** / `STS2_Momoi.pck` **131,855,024 B**（10-28 **1.0.3**） |",
           d, count=1)
d = d.replace("31 套 / **1349** 条", "32 套 / **1389** 条")
d = d.replace("全部 31 套 / 1349 条", "全部 32 套 / 1389 条")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 部署版本 + 套件数字")

rep(P_MAIN, """| `_verify_batch44.py` | **58** | 22 项平衡 + 注能置底/AutoPlay + 图鉴全解锁（含衍生牌）+ 发布包版本 |
| **合计** | **1349**（31 套） |""",
 """| `_verify_batch44.py` | 58 | 22 项平衡 + 注能置底/AutoPlay + 图鉴全解锁（含衍生牌）+ 发布包版本 |
| `_verify_batch46.py` | **40** | **黄金矿工当前耗能 + 费用/数值批 + 仅局内括号 + 卡牌统计 + 1.0.3 包** |
| **合计** | **1389**（32 套） |""",
 "§10 套件表")

tail = """
### 21.53 批次46：黄金矿工读当前耗能 + 数值/文本批 + 卡牌统计（1.0.3，2026-10-28）

#### 1. 黄金矿工！：读「当前耗能」，而不是卡面印的费

```csharp
// 旧（错）：卡面印的 Canonical —— 被减费/加费过的牌按印的费算
var cost = picked.EnergyCost.Canonical;

// 新（对）：含局部修正 + 全局钩子的当前费用
var cost = picked.EnergyCost.GetWithModifiers(CostModifiers.All);
```

所以「剧情推进！+」（3 → 升级后 0 费）被消耗时，现在会走 **0 费分支**给「巨石+」，而不是按 1 费发能量+抽牌。
费用同时改成 **0/0**（升级只给保留）。

> API 备忘：`GetWithModifiers(CostModifiers.All)` = 当前费用（最常用）；`GetResolved()` = 解析后费用（X 费返回 CapturedXValue）；
> `GetAmountToSpend()` = 实际花费（X 费返回剩余能量）；只想看「印的费 + 改费」用 `CostModifiers.None`。

#### 2. 费用 / 数值

| 卡 | 改动 |
|---|---|
| 黄金矿工！ | **1/0 → 0/0**（升级只给保留） |
| 瓶颈突破 | 伤害 **5/5 → 4/4** |
| 见识下我的实力吧 | **1/0 → 0/0** |
| 日复一日，必有精进 | **3/2 → 3/3**（升级不再减费，升级只加「每次构想减费」） |
| 灵感爆发 | **1/1 → 1/0** |
| 来自勇者的加护 | 伤害 **8/10 → 6/9**（升级 +3） |

#### 3. 文本

- **仅局内显示的括号**：火力爆发「（已获得过 N 层）」、剧本打击「（抽 N 张牌）」、天马行空「（额外攻击 N 次）」、博览群游「（攻击 N 次）」
  统一套 `{InCombat:\\n（…）|}`（空 else 分支 = 图鉴不显示），写法与原版 `BARRAGE` / `BODY_SLAM` / `COMPILE_DRIVER` 一致。
- **构想之矛 power**：每点构想的伤害常数 **8/11 → 11/15**（与卡面一致）。
- **矛与盾**：**卡面伤害** 8/11 → **11/15**（power 内部早就是 11/15，只是卡面没同步）。
- **开荒**：卡面「本场战斗中**未获得过**的特定诅咒」→「**未生成过**」；侧栏改成「**将依次生成以下诅咒**：苦恼，睡眠不佳，疑虑，执迷。」（诅咒名仍用红色）。
- **相遇**：「**铸造**」「**生成**」按关键词染金（eng：`Forge` / `Channel`）。

#### 4. 卡牌统计（本批实测）

| 分类 | 数量 |
|---|---|
| **角色卡池**（`[RegisterCard(typeof(STS2_MomoiCardPool))]`，可掉落 / 起始牌） | **91** |
| **衍生牌**（`TokenCardPool`：支援牌 12、构想、系统：阿比舒、绷住链 3、矛与盾、方块 4、渔获、传送门悖论其一/其二、我的回合！/WIN！/LOSE！/见识下我的实力吧/大姐姐、小游戏牌…） | **44** |
| **合计卡牌** | **135** |
| ↳ 其中 **小游戏牌**（minigame 标签） | **14** |
| ↳ 其中 **游戏牌**（fullgame 标签，在角色卡池里） | **6** |

> 顺带发现：`localization/zhs/cards.json` 里有一条 `STS2_MOMOI_CARD_FRIENDLY_DUEL_B.title`，但代码里**没有对应类**
> （是早期「友好的决斗」变体留下的孤儿词条），不影响运行，暂不处理。

#### 5. 版本 1.0.3 + 发布包

- csproj `<Version>1.0.3</Version>` + 清单 `version: 1.0.3`。
- `工作区\\发布包\\STS2_Momoi_v1.0.3.zip`（125.0 MB，顶层 `STS2_Momoi/`），旧的 v1.0.2 包已删。

#### 6. 产物 / 验证

- `dotnet build` **0 错误** → DLL **508,416 B**、PCK **131,855,024 B**。
- 新增 `_verify_batch46.py` **40 条**（含卡牌统计断言：91 / 44 / 135 / 14 / 6）；同步修正 `batch20/35/40/42/44` 的过期断言。
- **三十二套合计 1389 条断言全绿**。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.53")

d = io.open(P_REL, encoding="utf-8").read()
d = d.replace("version 1.0.2", "version 1.0.3").replace("STS2_Momoi_v1.0.2.zip", "STS2_Momoi_v1.0.3.zip")
d = d.replace("`<Version>1.0.2</Version>`", "`<Version>1.0.3</Version>`")
d = d.replace('"latest_version": "1.0.2"', '"latest_version": "1.0.3"').replace('"title": "游戏王小桃 1.0.2"', '"title": "游戏王小桃 1.0.3"')
io.open(P_REL, "w", encoding="utf-8").write(d)
print("  OK 发布清单 -> 1.0.3")

d = io.open(P_WS, encoding="utf-8").read()
d = re.sub(r"\| 自检 \|.*\|", "| 自检 | **32 套 / 1389 条断言全绿**（`_verify_batch*.py` 通配逐个跑） |", d, count=1)
d = d.replace("跑全部自检（31 套 / 1349 条断言）", "跑全部自检（32 套 / 1389 条断言）")
row = ("| 46 | 10-28 | **黄金矿工读当前耗能**（`GetWithModifiers(CostModifiers.All)`，修「剧情推进！+ 应给巨石+」）+ 0/0 费；"
       "瓶颈突破 4/4、见识实力 0/0、日复一日 3/3、灵感爆发 1/0、勇者加护 6/9；"
       "**火力爆发/剧本打击/天马行空/博览群游括号改「仅局内显示」**（`{InCombat:\\n（…）|}`）；"
       "构想之矛 power 11/15、矛与盾卡面伤害 11/15、开荒换「生成」措辞、相遇铸造/生成染金；"
       "卡牌统计 91 + 44 = 135（小游戏 14 / 游戏牌 6）；版本 **1.0.3** |")
anchor = "> 批次 24~26 是**角色动画**"
if anchor in d:
    d = d.replace(anchor, row + "\n\n" + anchor, 1)
else:
    d = d.rstrip("\n") + "\n" + row + "\n"
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
