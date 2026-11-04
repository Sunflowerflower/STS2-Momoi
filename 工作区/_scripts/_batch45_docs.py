# -*- coding: utf-8 -*-
"""批次45 文档：§21.52 + 数字同步 + 发布清单 1.0.2。"""
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


rep(P_MAIN, "> **本次状态（2026-10-28 批次44）**",
 """> **本次状态（2026-10-28 批次45）**：两处收尾，版本 **1.0.2**。
> ① **注能（开发者协同：绿）回退成正常的 `CardCmd.AutoPlay` 自动打出** —— 上一批为了绕开局卡 30 秒改成直接结算，
> 但那个 bug 目前无法稳定复现，先改回原版行为（保留「第 1 回合抽牌前置底」的修复、单次打出标记和日志兜底）。
> ② **衍生牌图鉴问号修好了**：`MomoiCompendiumUnlock` 之前只按 `STS2_MomoiCardPool` 过滤，而**小游戏牌 / 构想 / 支援 / 绷住链 / 传送门悖论其一其二都在 `TokenCardPool`**，
> 所以它们仍是问号 → 改成按 **id 前缀 `STS2_MOMOI_`** 遍历（卡牌 / 遗物 / 药水都改），图鉴里全部可见。
> `dotnet build` **0 错误**，DLL **507,904 B** / PCK **131,853,648 B**；三十一套自检 **1349 条断言全绿**。
> **发布包**：`工作区\\发布包\\STS2_Momoi_v1.0.2.zip`（125.0 MB，顶层 `STS2_Momoi/`）。详见 §21.52。
> **上一轮（2026-10-28 批次44）**""",
 "顶部状态块")

rep(P_MAIN, "> - **2026-10-28 会话（批次44）**：22 项平衡调整、注能置底与直接结算（修开局卡顿）、图鉴全解锁、版本 1.0.1 发布包（见 §21.51）。",
 "> - **2026-10-28 会话（批次44）**：22 项平衡调整、注能置底与直接结算（修开局卡顿）、图鉴全解锁、版本 1.0.1 发布包（见 §21.51）。\n"
 "> - **2026-10-28 会话（批次45）**：注能回退成 AutoPlay、衍生牌图鉴问号修复、版本 1.0.2 发布包（见 §21.52）。",
 "数据来源行")

d = io.open(P_MAIN, encoding="utf-8").read()
d = re.sub(r"\| \*\*当前部署版本\*\* \|.*\|",
           "| **当前部署版本** | `STS2_Momoi.dll` **507,904 B**（**10-28 07:09**）、`STS2_Momoi.pck` **131,853,648 B**（**10-28 07:09**）、`STS2_Momoi.json` 729 B（**游戏王小桃 1.0.2**） |",
           d, count=1)
d = d.replace("31 套 / **1347** 条", "31 套 / **1349** 条")
d = d.replace("全部 31 套 / 1347 条", "全部 31 套 / 1349 条")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 部署版本 + 套件数字")

rep(P_MAIN, """| `_verify_batch44.py` | **56** | **22 项平衡 + 注能置底/直接结算 + 图鉴全解锁 + 1.0.1 包** |
| **合计** | **1347**（31 套） |""",
 """| `_verify_batch44.py` | **58** | 22 项平衡 + 注能置底/AutoPlay + 图鉴全解锁（含衍生牌）+ 发布包版本 |
| **合计** | **1349**（31 套） |""",
 "§10 套件表")

tail = """
### 21.52 批次45：注能回退 + 衍生牌图鉴解锁（1.0.2，2026-10-28）

#### 1. 注能（开发者协同：绿）回退成 `CardCmd.AutoPlay`

上一批为绕「抓两张时打沙漏开局卡 30 秒」把注能改成**直接结算**（挂能力 + `RemoveFromCombat`）。
既然那条卡顿暂时无法稳定复现，先**回退成原版行为**：

```csharp
public override async Task AfterAutoPrePlayPhaseEntered(PlayerChoiceContext choiceContext, Player player)
{
    if (player != Owner || Owner.PlayerCombatState is not { TurnNumber: <= 1 }) return;
    if (_imbuedApplied || Pile is null || !Pile.Type.IsCombatPile()) return;   // 每张牌每场只打一次
    _imbuedApplied = true;
    try { await CardCmd.AutoPlay(choiceContext, this, null); }                 // ← 正常的自动打出
    catch (Exception e) { Entry.Logger.Warn($"[Imbued] DevGreen auto-play failed: {e.Message}"); }
}
```

**保留的修复**：`MomoiImbuedDrawPilePatch` —— 第 1 回合抽牌前把这张牌挪到抽牌堆底部（等价原版 `ShouldStartAtBottomOfDrawPile`），
所以「开局抽到 = 少抽一张」的问题仍然是修好的。
**保留的兜底**：`_imbuedApplied` 单次标记 + `Pile` 校验 + try/catch 日志（`[Imbued] ...`），下次复现时按日志时间戳排查。

#### 2. 衍生牌图鉴还是问号 —— 原因与修复

`MomoiCompendiumUnlock.MarkAll()` 原来只遍历 `ModelDb.AllCards.Where(c => c.Pool is STS2_MomoiCardPool)`。
但**衍生牌全在 `TokenCardPool`**：小游戏牌（连连看 / 消消乐 / 俄罗斯方块 / 扫雷 / 吃豆人 / PvZ …）、构想、支援牌、绷住链、传送门悖论其一/其二…
→ 它们永远不会被标记，图鉴里就一直是问号。

改成按 **id 前缀**过滤（本模组所有内容 id 都是 `STS2_MOMOI_` 开头）：

```csharp
private const string ModIdPrefix = "STS2_MOMOI_";

foreach (var card in ModelDb.AllCards.Where(c => c.Id.Entry.StartsWith(ModIdPrefix, StringComparison.Ordinal)))
    if (!progress.DiscoveredCards.Contains(card.Id)) { progress.MarkCardAsSeen(card.Id); marked++; }
// 遗物 / 药水同样改成 id 前缀
```

设置页「其他 → 解锁全部图鉴」按钮走的也是这个函数，所以手动点一次同样会把衍生牌补齐（已进过游戏的玩家不用重开档）。

#### 3. 版本 1.0.2 + 发布包

- csproj `<Version>1.0.2</Version>` + 清单 `version: 1.0.2`。
- `工作区\\发布包\\STS2_Momoi_v1.0.2.zip`（125.0 MB，顶层 `STS2_Momoi/`：README.txt + dll + json + pck），旧的 v1.0.1 包已删。

#### 4. 产物 / 验证

- `dotnet build` **0 错误** → DLL **507,904 B**、PCK **131,853,648 B**（10-28 07:09）。
- 同步修正断言：`batch15`（注能恢复 AutoPlay）、`batch44`（回退 + id 前缀 + 1.0.2）、`batch42`（版本号）。
- **三十一套合计 1349 条断言全绿**。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.52")

# 发布清单 -> 1.0.2
d = io.open(P_REL, encoding="utf-8").read()
d = d.replace("version 1.0.1", "version 1.0.2").replace("STS2_Momoi_v1.0.1.zip", "STS2_Momoi_v1.0.2.zip")
d = d.replace("`<Version>1.0.1</Version>`", "`<Version>1.0.2</Version>`")
d = d.replace('"latest_version": "1.0.1"', '"latest_version": "1.0.2"').replace('"title": "游戏王小桃 1.0.1"', '"title": "游戏王小桃 1.0.2"')
io.open(P_REL, "w", encoding="utf-8").write(d)
print("  OK 发布清单 -> 1.0.2")

# 工作区文档
d = io.open(P_WS, encoding="utf-8").read()
d = re.sub(r"\| 部署 \|.*\|", "| 部署 | `STS2_Momoi.dll` **507,904 B**（10-28 07:09）、`STS2_Momoi.pck` **131,853,648 B**（10-28 07:09）、清单 **游戏王小桃 1.0.2** |", d, count=1)
d = re.sub(r"\| 自检 \|.*\|", "| 自检 | **31 套 / 1349 条断言全绿**（`_verify_batch*.py` 通配逐个跑） |", d, count=1)
d = d.replace("跑全部自检（31 套 / 1347 条断言）", "跑全部自检（31 套 / 1349 条断言）")
row = ("| 45 | 10-28 | **注能回退**成正常的 `CardCmd.AutoPlay`（保留置底修复 + 单次标记 + 日志兜底，卡顿待复现再修）；"
       "**衍生牌图鉴问号修复**：`MarkAll` 从「只按 STS2_MomoiCardPool」改成 **id 前缀 `STS2_MOMOI_`**（衍生牌都在 TokenCardPool）；"
       "版本 **1.0.2** + 发布包 `STS2_Momoi_v1.0.2.zip` |")
anchor = "> 批次 24~26 是**角色动画**"
if anchor in d:
    d = d.replace(anchor, row + "\n\n" + anchor, 1)
else:
    d = d.rstrip("\n") + "\n" + row + "\n"
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
