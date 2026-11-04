# -*- coding: utf-8 -*-
"""批次27 文档：根文档 §21.30 + 数字同步；工作区文档批次表 + 数字同步。
注意：批次 24/25/26 已被角色动画会话（10-17/10-18）占用，本批编号为 27。"""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
P_MAIN = ROOT + r"\STS2_Momoi_迁移文档.md"
P_WS = ROOT + r"\工作区\_docs\STS2_Momoi_迁移文档.md"


def rep(path, old, new, label):
    d = io.open(path, encoding="utf-8").read()
    assert old in d, "没找到：" + label
    assert d.count(old) == 1, "多处：" + label
    io.open(path, "w", encoding="utf-8").write(d.replace(old, new))
    print("  OK " + label)


# ---------------- 根文档 ----------------
rep(P_MAIN, "> **本次状态（2026-10-18 批次26）**",
    """> **本次状态（2026-10-20 批次27）**：一次实操反馈批（角色动画期穿插的卡牌调整）。**游戏人生**跨局污染修好了 —— 真因是 `CardModel.CloneForCombat` **不重建 `_tags`**，战斗克隆体与牌组本尊共用同一个 `HashSet`，所以 `AddModCardTag` 写进去等于写进牌组、随存档跨局保留；改成按实例引用的「本场战斗临时游戏牌」表（`MinigameSupport.TemporaryGameCards`，战斗开始清空），并在开局清理旧版泄漏的标签；顺带给手牌选择加了拆场兜底（QuickRestart 时原版 `PlayerChoiceSynchronizer` 会抛 `ArgumentOutOfRangeException`，日志 20261020-152615）。数值/稀有度：**激战** 5→3 伤、费 1→0；**开发秘籍** → 稀有；**100连抽！** → 罕见 + **固有（升级前后都有）** + 升级改为费 4→3；**复盘** 攻击→**技能**、费 2→1、删掉伤害只留消耗堆回手。UI 文本：**连连看** 选牌文案 →「选择2张牌消耗」；**跑酷！**「选择一张」→「**选择最多一张**」（MinSelect=0 可以跳过，卡面+两个能力文本同步）；**节奏游戏！** power 右下角数字 → **将要造成的伤害**；**吃豆人** 没诅咒时给的 富足 → **WIN！**（升级 WIN！+），卡面+能力文本同步；**黄金矿工** 删掉已失效的死侧栏 `sidebar2`（不再给金币）。`dotnet build` **0 错误**，DLL **454,656 B** / PCK **109,989,948 B**；十七套自检 **732 条断言全绿**。详见 §21.30。
> **上一轮（2026-10-18 批次26）**""",
    "顶部状态块")

# 数据来源行
rep(P_MAIN, "> - **2026-10-18 会话（批次26）**",
    "> - **2026-10-20 会话（批次27）**：卡牌调整 + 游戏人生标签作用域修复 + 拆场兜底（见 §21.30）。\n> - **2026-10-18 会话（批次26）**",
    "数据来源行")

# 部署版本行
rep(P_MAIN, "| **当前部署版本** | `STS2_Momoi.dll` **453,120 B**（**10-18 13:51**）、`STS2_Momoi.pck` **109,990,924 B**（**10-18 13:51**）、`STS2_Momoi.json` 409 B |",
    "| **当前部署版本** | `STS2_Momoi.dll` **454,656 B**（**10-20 22:31**）、`STS2_Momoi.pck` **109,989,948 B**（**10-20 22:32**）、`STS2_Momoi.json` 409 B |",
    "§1 部署版本")

# §10 自检套件表
rep(P_MAIN, '''for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23; do "$PY" "工作区/_scripts/_verify_batch$v.py" | tail -1; done''',
    '''for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27; do "$PY" "工作区/_scripts/_verify_batch$v.py" | tail -1; done''',
    "§10 命令")

rep(P_MAIN, """| `_verify_batch20~23.py` | 28 / 17 / 43 / 25 | 阿比舒（4 倍倍率 + 3 段）、曳光弹与费用、批次 22 全项、**金色关键词收尾（击晕 / 金币）** + 标签闭合 |
| **合计** | **549** | 任一失败都要先查清是脚本过期还是代码回归，再继续 |""",
    """| `_verify_batch20~23.py` | 28 / 17 / 43 / 25 | 阿比舒（4 倍倍率 + 3 段）、曳光弹与费用、批次 22 全项、金色关键词收尾（击晕 / 金币） |
| `_verify_batch24~26.py` | 101 / 24 | **角色动画**：idle 帧序列与 `VisualCueSet`、攻击/能力/嘲讽分流、hit 回弹序列（帧数/尺寸/锚点/接线） |
| `_verify_batch27.py` | **58** | **游戏人生标签作用域 + 六张数值卡 + 三处 UI 文本**（含标签闭合） |
| **合计** | **732** | 任一失败都要先查清是脚本过期还是代码回归，再继续 |""",
    "§10 套件表")

d = io.open(P_MAIN, encoding="utf-8").read()
d = d.replace("# 跑自检（9/11/12/…/24 共 15 套）", "# 跑自检（9/11/12/…/27 共 17 套）")
d = d.replace("（15 套 / 607 条断言）", "（17 套 / 732 条断言）")
d = d.replace("（14 套 / 549 条断言）", "（17 套 / 732 条断言）")
d = d.replace("（13 套 / 524 条断言）", "（17 套 / 732 条断言）")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 根文档数字同步")

tail = """
### 21.30 批次27：游戏人生标签作用域、六张数值卡、三处 UI 文本（2026-10-20）

> 本批是**卡牌调整**穿插在角色动画期（批次 24~26）里的一次实操反馈批。

#### 1. 🔴 游戏人生：游戏牌标签跨战斗 / 跨局残留

**现象**：上一把用「游戏人生」给「打击」等牌加的「游戏牌」标签，新开一局还在（`MinigameSupport.IsMinigameCard` 仍为真）。

**真因**：`CardModel.CloneForCombat` **不重建 `_tags`** —— 战斗克隆体的 `_tags` 与牌组本尊**共用同一个 `HashSet`**。
所以 `AddModCardTag(手牌那张)` 实际上写进了**牌组本尊**，打完这场还在，并且随存档进到下一局。

**修法**（不再碰卡的持久状态）：

```csharp
// Cards\\MinigameSupport.cs
private static readonly HashSet<CardModel> TemporaryGameCards = new(ReferenceEqualityComparer.Instance);
public static void MarkTemporaryGameCard(CardModel card) => TemporaryGameCards.Add(card);
public static bool IsTemporaryGameCard(CardModel card) => TemporaryGameCards.Contains(card);
public static void ClearTemporaryGameCards() => TemporaryGameCards.Clear();

public static bool IsMinigameCard(CardModel card) =>
    card.Tags.Contains(Tag) || card.Tags.Contains(FullGameTag) || IsTemporaryGameCard(card);
```

- 读标签的地方统一走 `IsMinigameCard` / `IsTemporaryGameCard`：`Patches\\CardKeywordLabelPatch.cs`（金色顶行「游戏牌。」）
  与 `Patches\\MinigameSidebarPatch.cs` 都已补上。
- **战斗开始清空**（`CombatStats.CombatStartResetPatch.Prefix`）→ 天然「只本场战斗生效」。
- **旧存档清理**：`Entry.cs` 的 `RunStarted` 里遍历牌组，把「本来不是游戏牌」（规范模型没有该标签）的牌上的
  fullgame 标签 `RemoveModCardTag` 掉（`MinigameSupport.StripLeakedGameCardTags`）。
- 升级前后的差异保持原样：**升级前只给选中的那张**，**升级后给手牌/抽牌堆/弃牌堆里的所有同名牌**（都只在本场战斗）。

#### 2. 手牌选择的拆场兜底（日志 20261020-152615）

日志里唯一的报错：

```
System.ArgumentOutOfRangeException: Index was out of range.
   at PlayerChoiceSynchronizer.SyncLocalChoice_Patch3(...)
   at CardSelectCmd.FromHand(...)
   at STS2_Momoi.Cards.GameLife.OnPlay(...)
```

上下文是 **`[QuickRestart]`**（`Creating a new restart button` → `Cleaning up the current room` → `starting load now`）：
玩家在「游戏人生」的选牌界面开着时快速重开 → 房间被拆 → 原版把选择当成「空结果」同步，
而 `NetCombatCard.FromModel` 已找不到那张牌 → 抛异常。
**这是原版在「拆场时仍有待决选择」下的健壮性缺口**（任何用 `FromHand` 的卡都会中招），
既然接口是我们调的，就自己兜住：

```csharp
catch (Exception ex) when (ex is ArgumentOutOfRangeException or InvalidOperationException)
{
    Entry.Logger.Info($"[GameLife] selection aborted (scene teardown?): {ex.GetType().Name}");
    return null;
}
```

> 其它 `[WARN]`（`KitDevTools/mod_image.png`、`Asset not cached`、`RandomForeseer 推断`、Steam 学习版告警）均与本模组无关。

#### 3. 六张卡的数值 / 稀有度 / 类型

| 卡 | 改动 |
|---|---|
| **激战** `ConfusedShot` | 伤害 **5 → 3**；耗能 **1 → 0**（升级前后都是 0，升级只加次数 2→3） |
| **开发秘籍** `DevSecrets` | 稀有度 罕见 → **稀有** |
| **100连抽！** `HundredPull` | 稀有度 稀有 → **罕见**；**固有升级前后都有**；升级效果改为 **耗能 4 → 3** |
| **复盘** `GameReview` | 攻击 → **技能**（目标改 `Self`）；耗能 **2 → 1**；**删去伤害**，只留「消耗牌堆里的随机小游戏牌回手」；升级仍只让那张牌是升级版 |

#### 4. 四处 UI 文本 / 显示

| 卡 / 能力 | 改动 |
|---|---|
| **连连看** `LinkUp` | 选牌界面文案 → **「选择2张牌消耗」**（新键 `card_selection/STS2_MOMOI_LINKUP_HEADER`） |
| **跑酷！** `Parkour` | 「选择一张」→ **「选择最多一张」**：`CardSelectorPrefs(..., 0, 1)` + `Cancelable = true`（**可以跳过不选**）；卡面 + 两个能力文本 + 选牌界面文案（`STS2_MOMOI_PARKOUR_HEADER`）全部同步 |
| **节奏游戏！** `RhythmGamePower` | 右下角数字由「叠加层数」改为 **「将要造成的伤害」**：`DisplayAmount = max(0, 基础伤害 − 当前方块数 × 每方块降低)`（方块数取手牌 + 弃牌堆），并在施加 / 回合开始时刷 `InvokeDisplayAmountChanged()` |
| **吃豆人** `PacMan` | 没诅咒时给的 **富足 → WIN！**（升级 WIN！+）：`ModelDb.Card<WinCard>()`；`StringVar("AbundanceName")` → `StringVar("WinName")`；卡面与能力文本同步；其他效果不动 |
| **黄金矿工** `GoldMiner` | 删掉**已失效的死侧栏** `STS2_MOMOI_CARD_GOLD_MINER.sidebar2`（升级后早已不再给金币，且代码只引用 `sidebar1`） |

#### 5. 产物

- `dotnet build` **0 错误** → DLL **454,656 B**、PCK **109,989,948 B**（10-20 22:32）。
  PCK 约 110 MB 是**角色动图帧**（批次 24~26 的 100+ 张 600×820 帧）入库导致的，不是本批代码。
- `_verify_batch27.py` **58 条全绿**；十七套合计 **732 条断言全绿**。
- 过期的旧断言同步修正：`_verify_batch9.py`（吃豆人 富足→WIN！）、`_verify_batch14.py`（跑酷「最多一张」）。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.30")

# ---------------- 工作区文档 ----------------
rep(P_WS, "| 部署 | `STS2_Momoi.dll` **442,880 B**（10-16 17:15）、`STS2_Momoi.pck` **75,402,280 B**（10-16 17:15） |",
    "| 部署 | `STS2_Momoi.dll` **454,656 B**（10-20 22:31）、`STS2_Momoi.pck` **109,989,948 B**（10-20 22:32） |",
    "工作区 部署行")

rep(P_WS, "| 自检 | 14 套 / **549 条断言全绿**（`_verify_batch9.py`、`11~23`） |",
    "| 自检 | 17 套 / **732 条断言全绿**（`_verify_batch9.py`、`11~27`，含角色动画的 24~26） |",
    "工作区 自检行")

d = io.open(P_WS, encoding="utf-8").read()
d = d.replace("for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23; do",
              "for v in 9 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27; do")
d = d.replace("# 14 套自检（549 条断言", "# 17 套自检（732 条断言")
d = d.replace("跑自检 14 套（549 条断言）", "跑自检 17 套（732 条断言）")
d = d.replace("## 6. 最近四批（卡牌调整期）", "## 6. 最近的卡牌调整批")
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区 数字同步")

d = io.open(P_WS, encoding="utf-8").read()
old_tail = "| 23 | 10-16 | 「击晕」补金色（3 张，侧栏已有）、「终于上一档了！」金币补金色（**不加侧栏**，与原版一致） |"
row = "| 27 | 10-20 | 游戏人生标签改为**只本场战斗**（真因：`CloneForCombat` 不重建 `_tags`，克隆体与牌组本尊共用集合）+ 开局清理旧泄漏标签 + 手牌选择加拆场兜底；激战 5→3/0 费、开发秘籍→稀有、100连抽→罕见+固有+升级费 3、复盘→1 费技能去伤害；连连看选牌文案、跑酷「最多一张」可跳过、节奏游戏右下角显示伤害、吃豆人富足→WIN！、黄金矿工删死侧栏 |"
note = "> 批次 24~26 是**角色动画**（10-17/10-18，idle / 攻击·能力·嘲讽 / hit），细节见根文档 §21.27~§21.29。"
assert old_tail in d
io.open(P_WS, "w", encoding="utf-8").write(d.replace(old_tail, old_tail + "\n" + row + "\n\n" + note))
print("  OK 工作区 批次表加一行")
