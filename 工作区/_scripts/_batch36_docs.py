# -*- coding: utf-8 -*-
"""批次36 文档：§10 套件表整段重写 + §21.42 + 数字同步（根文档 & 工作区文档）。"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
P_MAIN = ROOT + r"\STS2_Momoi_迁移文档.md"
P_WS = ROOT + r"\工作区\_docs\STS2_Momoi_迁移文档.md"

NEW_TABLE = """| 套件 | 断言数 | 管什么 |
|---|---|---|
| `_verify_batch9.py` | 63 | 卡牌文本 / 代码特征（匹配前会剥掉 `[gold]` 等标签） |
| `_verify_batch11~19.py` | 102 / 52 / 32 / 37 / 50 / 27 / 28 / 26 / 13 | 遗物药水文本 → power 文本 → 机制 → 数值语义 → 颜色规范 |
| `_verify_batch20~23.py` | 28 / 17 / 43 / 25 | 阿比舒（4 倍倍率 + 3 段）、曳光弹与费用、批次 22 全项、金色关键词收尾 |
| `_verify_batch24.py` | 26 | idle 帧序列（42 帧 / 600×820 / 无损 / 接线） |
| `_verify_batch25~26.py` | 101 / 24 | 攻击/能力/嘲讽分流、hit 回弹序列 |
| `_verify_batch27.py` | 56 | 游戏人生标签作用域 + 六张数值卡 + 三处 UI 文本 |
| `_verify_batch28.py` | 92 | 死亡节奏 / relaxed 商店 / 休息处新图 / 像素头像 / 选人背景 / PCK |
| `_verify_batch29.py` | 36 | 跑酷删 power + 七张数值 + 两个稀有度 + 专注重做 |
| `_verify_batch30.py` | 21 | 专注 1 费 + 卡面/power 单句文本 + 天马行空升级版「+1」 |
| `_verify_batch31.py` | 24 | 死亡动画 50 帧 / 能量图标 24·256 / 多人手臂 422×1200 |
| `_verify_batch32.py` | 96 | 角色身份/头像/能量/多人手势/镜像 + 文本/特效参考 |
| `_verify_batch35.py` | 21 | 剧本打击括号数跟升级（0/1）+ 重整旗鼓阈值 25% |
| `_verify_batch36.py` | **19** | **桃味气泡水变牌（source:null + 逐张变换）+ 「任意张」选牌界面** |
| **合计** | **1062**（25 套） | 任一失败都要先查清是脚本过期还是代码回归，再继续 |"""


def rep(path, old, new, label):
    d = io.open(path, encoding="utf-8").read()
    assert old in d, "没找到：" + label
    assert d.count(old) == 1, "多处(%d)：%s" % (d.count(old), label)
    io.open(path, "w", encoding="utf-8").write(d.replace(old, new))
    print("  OK " + label)


# ---- §10 表整段替换（旧表已被多个会话重复追加成两份，重写一遍） ----
d = io.open(P_MAIN, encoding="utf-8").read()
start = d.find("| 套件 | 断言数 | 管什么 |")
end = d.find("### 10.2 其它验证手段")
assert start > 0 and end > start
d = d[:start] + NEW_TABLE + "\n\n" + d[end:]
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK §10 表整段重写")

# ---- 本次状态 ----
rep(P_MAIN, "> **本次状态（2026-10-24 批次35）**",
 """> **本次状态（2026-10-25 批次36）**：**桃味气泡水变牌修好了** —— 白光后卡面迟迟不恢复的真因是 `FromHand` 的 `source` 传了药水模型：
> `NPlayerHand.AfterCardsSelected(source)` 在 `source != null` 时把「手牌 holder 归位」挂到 `source.ExecutionFinished` 上，
> 而药水模型永远不抛这个事件 → 选中的卡牌节点一直留在「已选卡牌容器」里，`CardCmd.Transform` 也就找不到手牌节点、变牌白光后不刷新。
> 现在改成 **`source: null`**（与消消乐同一修法）+ **逐张 `CardCmd.Transform(单张)`**（与「整活」/原版「护驾！！！」完全同一条路径）。
> 选牌界面也从「99 张」改成 **任意张**（`0 ~ 999999999` 的原版写法 + 自带文案「选择任意张牌来变化。」）。
> `dotnet build` **0 错误**，DLL **488,960 B** / PCK **128,360,268 B**；二十五套自检 **1062 条断言全绿**。详见 §21.42。
> **上一轮（2026-10-24 批次35）**""",
 "顶部状态块")

rep(P_MAIN, "> - **2026-10-24 会话（批次35）**：剧本打击括号数跟升级（0/1）、重整旗鼓阈值 20%→25%（见 §21.40）。",
 "> - **2026-10-24 会话（批次35）**：剧本打击括号数跟升级（0/1）、重整旗鼓阈值 20%→25%（见 §21.40）。\n"
 "> - **2026-10-25 会话（批次36）**：桃味气泡水变牌修复（`source: null` + 逐张变换）、选牌界面改「任意张」（见 §21.42）。",
 "数据来源行")

# ---- 部署版本 ----
d = io.open(P_MAIN, encoding="utf-8").read()
d = re.sub(r"\| \*\*当前部署版本\*\* \|.*\|",
           "| **当前部署版本** | `STS2_Momoi.dll` **488,960 B**（**10-25 01:41**）、`STS2_Momoi.pck` **128,360,268 B**（**10-25 01:42**）、`STS2_Momoi.json` 409 B |",
           d, count=1)
d = d.replace("23 套 / **1043** 条", "25 套 / **1062** 条")
d = d.replace("全部 24 套 / 1020 条", "全部 25 套 / 1062 条")
d = d.replace("`_verify_batch9~32`", "`_verify_batch*.py`")
d = d.replace("# 全量 23 套 / 1043 条", "# 全量 25 套 / 1062 条")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 部署版本 + 套件数字")

tail = """
### 21.42 批次36：桃味气泡水变牌修复 + 选牌界面「任意张」（2026-10-25）

#### 1. 🔴 变牌后卡面「白很久」的真因

```csharp
// 旧写法（药水模型当 source）
CardSelectCmd.FromHand(ctx, Owner, prefs, null, this)   // ← source = 药水
```

`NPlayerHand.AfterCardsSelected(source)`（`NPlayerHand.cs:676`）：

```csharp
foreach (NHandCardHolder holder in Holders) { … }     // 恢复正常
if (source != null) source.ExecutionFinished += OnSelectModeSourceFinished;
else                OnSelectModeSourceFinished(null);   // ← 立刻把「已选卡牌」上的节点搬回手牌
```

`OnSelectModeSourceFinished` 才是把节点从 `_selectedHandCardContainer` 搬回手牌的那一步。
**药水模型永远不会抛 `ExecutionFinished`** → 归位永远不发生 → 选中的卡牌节点留在「已选容器」里，
`CardCmd.Transform` 里 `NCard.FindOnTable(original, PileType.Hand)` 也就拿不到手牌节点 → 变牌白光结束、卡面却迟迟不刷新
（玩家看到的就是「白很久」）。

> 这与批次 17/18 消消乐的「幽灵牌」是同一个坑，修法相同：**`source` 传 `null`**。

#### 2. 变牌写法改成和「整活」/原版「护驾！！！」一致

原版 `Guards`（护驾！！！）是逐张来：

```csharp
var list = (await CardSelectCmd.FromHand(..., source: this)).ToList();
foreach (var item in list) { var c = CombatState.CreateCard<MinionSacrifice>(Owner); … await CardCmd.Transform(item, c); }
```

本批照这个改成**逐张 `CardCmd.Transform(card, replacement)`**（不再自己拼 `CardTransformation` 批量提交）。

#### 3. 选牌界面：99 张 → 任意张

- `CardSelectorPrefs(..., 0, 999999999)`：原版「净化 / 护驾！！！」那种「任意张」写法。
- 文案不复用 `card_selection/TO_TRANSFORM`（那条带 `{Amount}`，会显示 999999999），新加一条：
  - `card_selection/STS2_MOMOI_ANY_TRANSFORM` = `选择任意张牌来[gold]变化[/gold]。` / `Choose any number of cards to [gold]Transform[/gold].`

#### 4. 顺手修了三条**过期断言**（不是本次改动引入的）

| 脚本 | 原断言 | 现状 | 处理 |
|---|---|---|---|
| `batch28` / `batch32` | `Entry` 正好 **24** 个补丁 | 后续批次已加到 **25** | 改成 `>= 24` 并打印实际数 |
| `batch32` | `LowHpVolume` + `AddIntSlider`（残血 BGM 音量） | 该设置项已被重构掉，改成 low_hp idle 帧 + `MomoiLowHpPatch` | 改成断言 `MomoiLowHpPatch.cs` + `cue/low_hp.png` |
| `batch32` | `vfx_thrash`（针锋相对）/ `vfx_giant_horizontal_slash`（秒人斧，在 MinigameFlowCards） | 特效路径被重排：针锋相对用 `vfx_molten_fist`（`IntentCards.cs`），秒人斧在 `HundredPull.cs` | 按现有实现改断言 |

> 这三条属于**别的批次的变量**，本次只是让套件重新全绿并把「为什么改」写进脚本注释；如果原负责人还想锁死具体数字/路径，请再改回去。

#### 5. 产物

- `dotnet build` **0 错误** → DLL **488,960 B**、PCK **128,360,268 B**（10-25 01:42）。
- `_verify_batch36.py` **19 条全绿**；**二十五套合计 1062 条断言全绿**（通配逐个跑）。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.42")

# ---- 工作区文档 ----
d = io.open(P_WS, encoding="utf-8").read()
d = re.sub(r"\| 部署 \|.*\|", "| 部署 | `STS2_Momoi.dll` **488,960 B**（10-25 01:41）、`STS2_Momoi.pck` **128,360,268 B**（10-25 01:42） |", d, count=1)
d = re.sub(r"\| 自检 \|.*\|", "| 自检 | **25 套 / 1062 条断言全绿**（`_verify_batch*.py` 通配逐个跑） |", d, count=1)
d = d.replace("跑全部自检（24 套 / 1020 条断言）", "跑全部自检（25 套 / 1062 条断言）")
row36 = ("| 36 | 10-25 | **桃味气泡水变牌修复**：`FromHand` 的 `source` 改 `null`（药水模型永不抛 `ExecutionFinished` → 手牌 holder 不归位 → 白光后卡面不刷新）、"
         "逐张 `CardCmd.Transform(单张)`（同整活/原版护驾）；选牌界面 99 张 → **任意张**（`0~999999999` + 新文案 `STS2_MOMOI_ANY_TRANSFORM`）；顺手修 3 条过期断言 |")
anchor = "> 批次 24~26 是**角色动画**"
if anchor in d:
    d = d.replace(anchor, row36 + "\n\n" + anchor, 1)
else:
    d = d.rstrip("\n") + "\n" + row36 + "\n"
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
