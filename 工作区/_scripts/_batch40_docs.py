# -*- coding: utf-8 -*-
"""批次40 文档：§21.47 + 数字/套件表同步（根文档 & 工作区文档）。"""
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


rep(P_MAIN, "> **本次状态（2026-10-25 批次39）**",
 """> **本次状态（2026-10-25 批次40）**：**一大批卡牌改动 + 两张新卡 + 建筑师打斗演出**。
> 消耗/费用：复盘与王不见王「升级前消耗、升级后删去」；循环叙事 0 费且升级给保留；日复一日 3/2 费且保留升级前后都有；发布委托 2/2 费；局势升温 2/2 费；黄金矿工 1/0 费；愤怒的小鸟 1/1 费。
> 数值：瓶颈突破构想 1/2、构想之矛 11/15、矛与盾伤害 11/15、整装待发 6/8 + 活力火力 2/3、局势升温 12/16、发布委托格挡 11/14、伏笔回收→罕见、100连抽→稀有。
> 机制：创作的痛苦新增「获得 2/3 层火力」；扫雷炸弹改成**洗入抽牌堆随机位置**（同原版守墓人）；再启新篇**只有手牌没构想时才加自己费用**；博览群游改**随机敌人**（同原版散射炮）。
> 新卡：**传送门悖论**（0c 技能，从两张衍生牌选一张入手；升级给升级版并删去消耗）+ **过载**（1c 能力，2/3 火力，火力减少时按能力层数获得活力）。
> **建筑师房对打演出**：RitsuLib 只从 `ancients.json` 生成对话，`StartAttackers/EndAttackers` 是 C# 字段 → 我们补了 `MomoiArchitectCutscenePatch` 在 `TheArchitect.LoadDialogue` 之后按拜访次数补上攻击者配置。
> `dotnet build` **0 错误**，DLL **501,760 B** / PCK **131,852,476 B**；二十七套自检 **1201 条断言全绿**。详见 §21.47。
> **上一轮（2026-10-25 批次39）**""",
 "顶部状态块")

rep(P_MAIN, "> - **2026-10-25 会话（批次39）**：九张卡数值/费用、自助指南附魔（GainsBlock）、? 事件全面体检（见 §21.46）。",
 "> - **2026-10-25 会话（批次39）**：九张卡数值/费用、自助指南附魔（GainsBlock）、? 事件全面体检（见 §21.46）。\n"
 "> - **2026-10-25 会话（批次40）**：一批卡牌费用/数值/机制、新卡「传送门悖论」与「过载」、建筑师打斗演出（见 §21.47）。",
 "数据来源行")

d = io.open(P_MAIN, encoding="utf-8").read()
d = re.sub(r"\| \*\*当前部署版本\*\* \|.*\|",
           "| **当前部署版本** | `STS2_Momoi.dll` **501,760 B**（**10-25 21:44**）、`STS2_Momoi.pck` **131,852,476 B**（**10-25 21:45**）、`STS2_Momoi.json` 409 B |",
           d, count=1)
d = d.replace("26 套 / **1139** 条", "27 套 / **1201** 条")
d = d.replace("全部 26 套 / 1139 条", "全部 27 套 / 1201 条")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 部署版本 + 套件数字")

rep(P_MAIN, """| `_verify_batch37.py` | **55** | **九张卡数值/费用 + GainsBlock 全覆盖 + 事件/角色文本兜底** |
| **合计** | **1139**（26 套） |""",
 """| `_verify_batch37.py` | 55 | 九张卡数值/费用 + GainsBlock 全覆盖 + 事件/角色文本兜底 |
| `_verify_batch40.py` | **62** | **本批全部卡牌改动 + 传送门悖论 + 过载 + 建筑师打斗补丁** |
| **合计** | **1201**（27 套） |""",
 "§10 套件表")

tail = """
### 21.47 批次40：一批卡牌改动 + 传送门悖论 / 过载 + 建筑师打斗演出（2026-10-25）

#### 1. 消耗 / 费用 / 关键词

| 卡 | 改动 |
|---|---|
| **复盘** `GameReview` | **升级前有「消耗」，升级后删去**（`OnUpgrade → RemoveKeyword(Exhaust)`，`AfterDowngraded` 加回） |
| **王不见王** `KingsNeverMeet` | 费 **1/0 → 1/1**；**升级前消耗、升级后删去**（同上写法） |
| **循环叙事** `CyclicNarrative` | 费 **1/0 → 0/0**；升级改为**获得保留** |
| **日复一日，必有精进** `LearnByDoing` | 费 **4/4 → 3/2**；**保留升级前后都有** —— 放进 `CanonicalKeywords`（升级里不再 `AddKeyword`，所以不会出现两个「保留」） |
| **发布委托** `PostQuest` | 费 **1/1 → 2/2** |
| **局势升温** `PlayWithFire` | 费 **1/1 → 2/2** |
| **黄金矿工** `GoldMiner` | 费 **0/0 → 1/0** |
| **愤怒的小鸟** `AngryBirds` | 费 **0/0 → 1/1** |

#### 2. 数值

| 卡 | 改动 |
|---|---|
| **伏笔回收** | 稀有 → **罕见** |
| **100连抽！** | 罕见 → **稀有** |
| **瓶颈突破** | 构想 +1/1 → **+1/2**（新增 `ConceptGain` 变量，实际结算也读它） |
| **构想之矛** | 伤害 10/14 → **11/15** |
| **矛与盾** | 伤害 8/11 → **11/15**（在 `SpearShieldPower` 的叠加常数里） |
| **整装待发** | 格挡 8/10 → **6/8**；活力/火力 1/2 → **2/3** |
| **局势升温** | 伤害 10/13 → **12/16**（升级 +4） |
| **发布委托** | 格挡 7/10 → **11/14** |
| **创作的痛苦！** | **第一行新增「获得 2/3 层火力」**（`DynamicVar("Firepower", 2)`，OnPlay 开头 `PowerCmd.Apply<FirepowerPower>`） |

#### 3. 机制修正

- **再启新篇**：以前无论手牌有没有构想都会 `EnergyCost.SetThisCombat(+1)`；现在把加费挪进「手牌没有构想 → 补一张构想」那一支里面，
  有构想时打出**不再增加自身费用**。
- **扫雷**：炸弹原本 `CardPilePosition.Top`（放抽牌堆顶），与卡面「加入你的抽牌堆」不符 →
  改成 **`CardPilePosition.Random`**（与卡面一致，参考原版守墓人 `GraveWarden` 把灵魂洗入抽牌堆的写法）。
- **博览群游**：`TargetType.AnyEnemy` → **`TargetType.RandomEnemy`**，结算改 `TargetingRandomOpponents(combatState)`
  （参考原版散射炮 `FlakCannon`：每一击各自随机挑目标）；文本改成「就**随机对敌人**造成……」。

#### 4. 新卡

**传送门悖论** `PortalParadox`（0 费技能·罕见）

```
从两张牌中选择一张加入你的手牌。
（消耗。升级：给的是升级过的版本，并删去消耗。）
```

- 「传送门悖论其一 / 其二」从角色池改成 **Token 衍生牌**（`CardRarity.Token` + `TokenCardPool`），只能由这张牌生成。
- 侧栏用 `HoverTipFactory.FromCard<PortalParadoxOne>(IsUpgraded)` + `...Two` —— 悬停就能看到两张衍生牌（升级时预览升级版）。
- 卡面直接复制「其一」的图（`PortalParadox.png`），与需求一致。
- 升级：`RemoveKeyword(Exhaust)` + `OnPlay` 里 `CardCmd.Upgrade(card)` 给升级过的衍生牌。

**过载** `Overload`（1 费能力·罕见）+ `OverloadPower`

```
获得 2（升级 3）层火力。
每当你的火力层数减少时，获得 3（升级 4）点活力。
```

- power 用 `PowerStackType.Counter`：**层数 = 每次触发获得的活力点数**，重复打出过载会把数值叠上去（3+3=6 …）。
- 触发靠 `OverloadPower.AfterPowerAmountChanged` 监听 `power is FirepowerPower && amount < 0`（火力消耗都走 `PowerCmd.ModifyAmount`）。
- 卡面 `工作区\\美术成品区\\过载.png` → `images/cards/Overload.png`；图标 `过载power.png` → `images/powers/overload_power.png`（尺寸刚好 1000×760 / 256×256）。

#### 5. 建筑师房「与建筑师对打」的演出

按用户给的 QA 复盘到了真正的原因：

- 演出全在 `TheArchitect` 事件里，是**纯特效**；打几下、谁打谁由**对话配置**的 `StartAttackers/EndAttackers` 决定；
  实际播放用角色自己的 `GetArchitectAttackVfx()`（我们角色早就返回了 Ironclad 那 5 条 vfx 路径 ✓，5 个场景文件都存在 ✓）。
- **问题**：`StartAttackers/EndAttackers` 是 **C# 字段**，而 mod 的对话是 **RitsuLib 从 `ancients.json` 里生成的**
  （`THE_ARCHITECT.talk.<角色>.N-…` 台词我们写好了 4 段），生成出来的对话这两个字段全是默认 `None` →
  台词照常播，但**一下都不打**。
- **修法**：新增 `MomoiArchitectCutscenePatch`，挂在 `TheArchitect.LoadDialogue` 的 Postfix：
  解析出对话后按 `VisitIndex` 补上攻击者 —— 前几次（嘴硬）`Player` 起手 / `Both` 收场，最后一次（带饮料）`None`。
  这两个属性是 `init` 的，运行期通过自动属性后备字段反射写入。

> 数值只是演出：`WinRun` 直接结算这一局，不会真的扣建筑师的血（QA 里也这么说）。

#### 6. 产物 / 验证

- `dotnet build` **0 错误** → DLL **501,760 B**、PCK **131,852,476 B**（10-25 21:45）。
- 新增 `_verify_batch40.py` **62 条**（本批全部改动 + 两张新卡 + 建筑师补丁 + 标签闭合）；
  同步修正过期断言：`batch27`（100连抽又回到稀有）、`batch29`（构想之矛 11/15）。
- **二十七套合计 1201 条断言全绿**。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.47")

# ---------------- 工作区文档 ----------------
d = io.open(P_WS, encoding="utf-8").read()
d = re.sub(r"\| 部署 \|.*\|", "| 部署 | `STS2_Momoi.dll` **501,760 B**（10-25 21:44）、`STS2_Momoi.pck` **131,852,476 B**（10-25 21:45） |", d, count=1)
d = re.sub(r"\| 自检 \|.*\|", "| 自检 | **27 套 / 1201 条断言全绿**（`_verify_batch*.py` 通配逐个跑） |", d, count=1)
d = d.replace("跑全部自检（26 套 / 1139 条断言）", "跑全部自检（27 套 / 1201 条断言）")
row = ("| 40 | 10-25 | 复盘/王不见王「升级前消耗、升级后删去」；循环叙事 0 费+升级保留；日复一日 3/2 费且保留常驻；"
       "发布委托 2/2 费·格挡 11/14；局势升温 2/2 费·12/16；黄金矿工 1/0；愤怒的小鸟 1/1；瓶颈突破构想 1/2；"
       "构想之矛 11/15；矛与盾 11/15；整装待发 6/8+2/3；伏笔回收→罕见、100连抽→稀有；创作的痛苦加火力 2/3；"
       "扫雷炸弹改随机位置；再启新篇只在无构想时加费；博览群游改随机敌人；**新卡传送门悖论 / 过载**；"
       "**建筑师对打演出**（LoadDialogue 后补 Start/EndAttackers） |")
anchor = "> 批次 24~26 是**角色动画**"
if anchor in d:
    d = d.replace(anchor, row + "\n\n" + anchor, 1)
else:
    d = d.rstrip("\n") + "\n" + row + "\n"
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
