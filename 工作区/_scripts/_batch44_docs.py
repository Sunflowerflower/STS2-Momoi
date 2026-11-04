# -*- coding: utf-8 -*-
"""批次44 文档：§21.51 + 数字/套件表同步 + 发布清单补 1.0.1。"""
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


rep(P_MAIN, "> **本次状态（2026-10-26 批次43）**",
 """> **本次状态（2026-10-28 批次44）**：**平衡批 + 两个真 bug + 图鉴全解锁，版本 1.0.1**。
> 22 项数值/费用调整（过载 2 费·活力 2/3、修行 2 费、BA启动 2/3、整装待发 4/6、天马行空 4/4、博览群游 5/7、激战 2/2、翻滚射击 6/8、对策 4/5、我复活啦 2/3、捕鱼达人 8/8、旅行异蛙 6/6、相遇 6/7、时 火力 2/3、LOSE！2/3、节奏游戏 18/20·6/5·1 费、绷到我了 2 血/6-8、五万年 4/6、植物大战僵尸 1/1、传送门悖论 1 费、构想之盾升级不再给固有；矛与盾 11/15 上一批已到位）。
> **注能（开发者协同：绿）两处修复**：① 新增 `MomoiImbuedDrawPilePatch` —— 第 1 回合抽牌前把这张牌挪到抽牌堆**底部**（等价原版 `ShouldStartAtBottomOfDrawPile`），不再「开局抽到等于少抽一张」；② 开局自动打出改成**直接结算**（挂两个能力 + 离开战斗），不再走 `CardCmd.AutoPlay` 的完整出牌流程 —— 这是「抓两张时打沙漏开局卡 30 秒」最可能的原因（出牌队列/能力牌飞行动画/动画 cue 在 AutoPrePlay 阶段叠加），现在是同步结算 + 每张只算一次 + 异常兜底。
> **图鉴全解锁**：新增 `MomoiCompendiumUnlockPatch`（挂在 `SaveManager.InitProgressData` 之后）把本模组卡牌/遗物/药水批量 `Progress.MarkXxxAsSeen` 并落盘，图鉴不再问号；设置页「其他」里另加**手动「解锁全部图鉴」按钮**兜底。
> `dotnet build` **0 错误**，DLL **508,416 B** / PCK **131,853,648 B**；三十一套自检 **1347 条断言全绿**。
> **发布包**：`工作区\\发布包\\STS2_Momoi_v1.0.1.zip`（125.0 MB，顶层 `STS2_Momoi/`）。详见 §21.51。
> **上一轮（2026-10-26 批次43）**""",
 "顶部状态块")

rep(P_MAIN, "> - **2026-10-26 会话（批次43）**：设置页收尾（隐藏简介 / 去掉进度说明卡 / 日志目录跨平台）、换预览图、**打本地发布 zip**（见 §21.50）。",
 "> - **2026-10-26 会话（批次43）**：设置页收尾（隐藏简介 / 去掉进度说明卡 / 日志目录跨平台）、换预览图、**打本地发布 zip**（见 §21.50）。\n"
 "> - **2026-10-28 会话（批次44）**：22 项平衡调整、注能置底与直接结算（修开局卡顿）、图鉴全解锁、版本 1.0.1 发布包（见 §21.51）。",
 "数据来源行")

d = io.open(P_MAIN, encoding="utf-8").read()
d = re.sub(r"\| \*\*当前部署版本\*\* \|.*\|",
           "| **当前部署版本** | `STS2_Momoi.dll` **508,416 B**（**10-28 06:33**）、`STS2_Momoi.pck` **131,853,648 B**（**10-28 06:34**）、`STS2_Momoi.json` 729 B（**游戏王小桃 1.0.1**） |",
           d, count=1)
d = d.replace("30 套 / **1291** 条", "31 套 / **1347** 条")
d = d.replace("全部 30 套 / 1291 条", "全部 31 套 / 1347 条")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 部署版本 + 套件数字")

rep(P_MAIN, """| `_verify_batch43.py` | **26** | **设置页收尾（隐藏简介/去掉说明卡）+ 预览图 + 本地发布 zip 校验** |
| **合计** | **1291**（30 套） |""",
 """| `_verify_batch43.py` | 26 | 设置页收尾（隐藏简介/去掉说明卡）+ 预览图 + 本地发布 zip 校验 |
| `_verify_batch44.py` | **56** | **22 项平衡 + 注能置底/直接结算 + 图鉴全解锁 + 1.0.1 包** |
| **合计** | **1347**（31 套） |""",
 "§10 套件表")

tail = """
### 21.51 批次44：平衡批 + 注能修复 + 图鉴全解锁（1.0.1，2026-10-28）

#### 1. 平衡调整（22 项，逐条照用户清单）

| 卡 | 改动 |
|---|---|
| **过载** `Overload` | 耗能 **1 → 2**；活力 **3/4 → 2/3** |
| **修行** `AsceticTraining` | 耗能 **1 → 2** |
| **BA启动！** `BaBoot` | 活力 **3/4 → 2/3** |
| **整装待发** `GearUp` | 格挡 **6/8 → 4/6** |
| **天马行空** `BulletRain` | 伤害 **5/7 → 4/4**（升级只加 1 次额外攻击，不再加伤害） |
| **博览群游** `ExperienceCombo` | 伤害 **7/9 → 5/7** |
| **矛与盾** `SpearShield` | 伤害 **8/11 → 11/15**（批次 40 已到位，本批只核对） |
| **植物大战僵尸** | 耗能 **1/0 → 1/1**（升级不再减费） |
| **传送门悖论** `PortalParadox` | 耗能 **0/0 → 1/1** |
| **激战** `ConfusedShot` | 伤害 **3/3 → 2/2** |
| **翻滚射击** `RollAndShoot` | 格挡 **7/9 → 6/8** |
| **对策** `Countermeasure` | 活力 **5/7 → 4/5**（升级 +1） |
| **我复活啦！** `ImBack` | 活力 **3/5 → 2/3**（升级 +1） |
| **捕鱼达人！** `FishingMaster` | 伤害 **11/11 → 8/8** |
| **旅行异蛙** `TravelFrog` | 格挡 **6/7 → 6/6**（升级只加「每堆数值」） |
| **相遇** `Encounter` | 格挡 **8/10 → 6/7** |
| **构想之盾** `ConceptShield` | 升级**不再给固有** |
| **来自时的援护** `MomoiSupportToki` | 火力 **3/4 → 2/3** |
| **LOSE！** `LoseCard` | 活力 **3/5 → 2/3**（升级 +1） |
| **节奏游戏！** `RhythmGame` | 伤害 **18/24 → 18/20**；每方块降伤 **6/4 → 6/5**；耗能 **0/0 → 1/1**（power 里的叠加常数同步） |
| **绷到我了** `ItCrackedMe` | 失去生命 **1/1 → 2/2**；格挡 **5/7 → 6/8** |
| **我还能绷五万年呢** `FiftyThousandYears` | 格挡 **5/7 → 4/6**（下回合格挡跟着变，因为它就是本次获得的量） |

#### 2. 注能（开发者协同：绿）：置底 + 直接结算

**① 置底（`MomoiImbuedDrawPilePatch`）** ——照原版 `Imbued` 的机制复现：

```csharp
// 原版：EnchantmentModel.ShouldStartAtBottomOfDrawPile => true
//       CombatManager.SetupPlayerTurn 在 TurnNumber == 1 抽牌前扫抽牌堆并 MoveToBottomInternal
// 我们这张是卡牌（没有附魔模型），所以直接给 SetupPlayerTurn 打 Prefix，同样在第 1 回合抽牌前把它挪到堆底。
```

这样抽 5 张够不到堆底 → 不再「开局抽到这张等于少抽一张」。

**② 直接结算（不再 `CardCmd.AutoPlay`）** ——针对「抓两张时打沙漏开局卡 30 秒」：

- `CardCmd.AutoPlay` 会走完整出牌流程（出牌队列动画、**能力牌飞行动画** `AwaitFinished`、卡牌动画 cue、`PushModel`…），
  在 **AutoPrePlay 阶段连续两张**时最容易互相等待；玩家反馈正好是「抓了两张开发者协同：绿」。
- 现在改成**直接挂能力**（`PowerCmd.Apply<DexterityPower>` + `Apply<DevGreenPower>`）+ `CardPileCmd.RemoveFromCombat(this, skipVisuals: true)`，
  语义与「打出这张能力牌」一致，但完全不碰出牌队列/节点动画。
- 另外加了 `_imbuedApplied` 单次标记（每张牌每场只结算一次）、`Pile.Type.IsCombatPile()` 校验、try/catch + 日志。

> 说明：没有玩家日志，这是按「AutoPrePlay 阶段连续 AutoPlay 能力牌」这条最可疑的路径修；如果还有卡顿，请抓 `godot.log` 里
> `[Imbued]` 与 `[Visual]` 两行的时间戳。

#### 3. 图鉴默认全解锁（不再问号）

问号来自 `Progress.DiscoveredCards` 没有记录（`NotSeen`）。新增 `MomoiCompendiumUnlockPatch`：

```csharp
// 挂在 SaveManager.InitProgressData 之后（档案进度已加载）
foreach (var card in ModelDb.AllCards.Where(c => c.Pool is STS2_MomoiCardPool))
    if (!progress.DiscoveredCards.Contains(card.Id)) { progress.MarkCardAsSeen(card.Id); marked++; }
// 遗物 / 药水同理（MarkRelicAsSeen / MarkPotionAsSeen）
if (marked > 0) SaveManager.Instance.SaveProgressFile();
```

- 用 `Progress.MarkXxxAsSeen`，**不用** `SaveManager.Instance.MarkCardAsSeen(card)`（那个要求 `LocalContext.IsMine`，主菜单会被静默跳过）。
- 设置页「其他」里另加**手动「解锁全部图鉴」按钮**（`MomoiCompendiumUnlock.MarkAll`）兜底。
- 纪元门控方面：本模组没有注册任何纪元，卡池也不会 `FilterThroughEpochs` 卡住（0.6.7 也没有 `SetEpochRequirementsIgnoredForMod`）。

#### 4. 版本 1.0.1 + 发布包

- csproj `<Version>1.0.1</Version>` + 清单 `version: 1.0.1`（设置页诊断卡会显示 1.0.1）。
- `工作区\\_scripts\\_make_release_zip.py` 重新打包 → **`工作区\\发布包\\STS2_Momoi_v1.0.1.zip`（125.0 MB）**，顶层 `STS2_Momoi/`。
- 顺手清掉了中间出现的**双层嵌套** zip（`STS2_Momoi_v1.0.0/STS2_Momoi/…`，玩家解压会变成 `mods/STS2_Momoi_v1.0.0/` 加载不到）。

#### 5. 产物 / 验证

- `dotnet build` **0 错误** → DLL **508,416 B**、PCK **131,853,648 B**（10-28 06:34）。
- 新增 `_verify_batch44.py` **56 条**；同步修正过期断言：`batch15/20/27/29/37/40/42`（数值与版本号）。
- **三十一套合计 1347 条断言全绿**。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.51")

# ---- 发布清单：版本 1.0.1 ----
dv = io.open(P_REL, encoding="utf-8").read()
dv = dv.replace("version 1.0.0", "version 1.0.1").replace("STS2_Momoi_v1.0.0.zip", "STS2_Momoi_v1.0.1.zip")
dv = dv.replace("`<Version>1.0.0</Version>`", "`<Version>1.0.1</Version>`")
dv = dv.replace("**name 游戏王小桃 / author alkaid616 / version 1.0.0", "**name 游戏王小桃 / author alkaid616 / version 1.0.1")
dv = dv.replace('"latest_version": "1.0.0"', '"latest_version": "1.0.1"').replace('"title": "游戏王小桃 1.0.0"', '"title": "游戏王小桃 1.0.1"')
io.open(P_REL, "w", encoding="utf-8").write(dv)
print("  OK 发布清单 -> 1.0.1")

# ---- 工作区文档 ----
d = io.open(P_WS, encoding="utf-8").read()
d = re.sub(r"\| 部署 \|.*\|", "| 部署 | `STS2_Momoi.dll` **508,416 B**（10-28 06:33）、`STS2_Momoi.pck` **131,853,648 B**（10-28 06:34）、清单 **游戏王小桃 1.0.1** |", d, count=1)
d = re.sub(r"\| 自检 \|.*\|", "| 自检 | **31 套 / 1347 条断言全绿**（`_verify_batch*.py` 通配逐个跑） |", d, count=1)
d = d.replace("跑全部自检（30 套 / 1291 条断言）", "跑全部自检（31 套 / 1347 条断言）")
row = ("| 44 | 10-28 | **22 项平衡调整**（过载 2 费·活力 2/3、修行 2 费、整装待发 4/6、天马行空 4/4、博览群游 5/7、节奏游戏 18/20·6/5·1 费…）；"
       "**注能修复**：新增置底补丁（第 1 回合抽牌前沉底）+ 开局改**直接结算**（不再 `CardCmd.AutoPlay`，修「两张绿开局卡 30 秒」）；"
       "**图鉴全解锁**（`InitProgressData` 后批量 MarkXxxAsSeen + 落盘，设置页另有手动按钮）；版本 **1.0.1** + 发布包 `STS2_Momoi_v1.0.1.zip` |")
anchor = "> 批次 24~26 是**角色动画**"
if anchor in d:
    d = d.replace(anchor, row + "\n\n" + anchor, 1)
else:
    d = d.rstrip("\n") + "\n" + row + "\n"
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
