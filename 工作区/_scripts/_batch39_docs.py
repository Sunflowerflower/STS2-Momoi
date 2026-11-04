# -*- coding: utf-8 -*-
"""批次39 文档：§21.46 + §10 套件表补 batch37 + 数字同步（根文档 & 工作区文档）。"""
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


rep(P_MAIN, "> **本次状态（2026-10-25 批次38）**",
 """> **本次状态（2026-10-25 批次39）**：**数值批 + 事件 bug 修复**。九张卡的数值/费用按用户点名调整（节奏游戏 18/24 且每方块 6/4、打灰机格挡 6/8 抽 1/2、消消乐 1/0 费且升级不再给保留、植物大战僵尸 1/0 费、花凛 32/40、晴 6/9、千寻 7/10、茜 12/15、大师 3/4+4/6、小玉 3/4）。
> **自助指南附魔 bug 找到真因**：原版 `Nimble`（灵巧）靠 `CardModel.GainsBlock` 筛目标，而 mod 里 **16 张会给格挡的卡都没 override 这个标志** → 灵巧只能选到「防御」。已全部补齐（顺带这些卡也自动获得原版「格挡」侧栏）。
> 另按「所有 ? 事件」逐条过了一遍：**色彩哲学家**的选项文案键是按 `EnergyColorName.ToUpperInvariant()` 拼的（`…options.STS2_MOMOI`），mod 的 `events.json` 里已有该键（本批补回被覆盖的「桃红色」标题）；补了角色 `bestiaryQuote`；并给 `EnergyIconHelper.GetPath` 加兜底（我们的池子在游戏图集里没有 `energy_sts2_momoi.tres`）。
> `dotnet build` **0 错误**，DLL **495,616 B** / PCK **130,899,152 B**；二十六套自检 **1139 条断言全绿**。详见 §21.46。
> **上一轮（2026-10-25 批次38）**""",
 "顶部状态块")

rep(P_MAIN, "> - **2026-10-25 会话（批次36）**：桃味气泡水变牌修复（`source: null` + 逐张变换）、选牌界面改「任意张」（见 §21.42）。",
 "> - **2026-10-25 会话（批次36）**：桃味气泡水变牌修复（`source: null` + 逐张变换）、选牌界面改「任意张」（见 §21.42）。\n"
 "> - **2026-10-25 会话（批次39）**：九张卡数值/费用、自助指南附魔（GainsBlock）、? 事件全面体检（见 §21.46）。",
 "数据来源行")

d = io.open(P_MAIN, encoding="utf-8").read()
d = re.sub(r"\| \*\*当前部署版本\*\* \|.*\|",
           "| **当前部署版本** | `STS2_Momoi.dll` **495,616 B**（**10-25 06:30**）、`STS2_Momoi.pck` **130,899,152 B**（**10-25 06:30**）、`STS2_Momoi.json` 409 B |",
           d, count=1)
d = d.replace("25 套 / **1085** 条", "26 套 / **1139** 条")
d = d.replace("全部 25 套 / 1085 条", "全部 26 套 / 1139 条")
d = d.replace("# 全量 25 套 / 1085 条", "# 全量 26 套 / 1139 条")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 部署版本 + 套件数字")

rep(P_MAIN, """| `_verify_batch36.py` | **19** | **桃味气泡水变牌（source:null + 逐张变换）+ 「任意张」选牌界面** |
| **合计** | **1085**（25 套） |""",
 """| `_verify_batch36.py` | 19 | 桃味气泡水变牌（source:null + 逐张变换）+ 「任意张」选牌界面 |
| `_verify_batch37.py` | **55** | **九张卡数值/费用 + GainsBlock 全覆盖 + 事件/角色文本兜底** |
| **合计** | **1139**（26 套） |""",
 "§10 套件表")

tail = """
### 21.46 批次39：九张卡数值 + 自助指南附魔 bug + ? 事件全面体检（2026-10-25）

#### 1. 卡牌数值 / 费用（用户逐条点名）

| 卡 | 改动 |
|---|---|
| **节奏游戏！** `RhythmGame` | 伤害 **24/30 → 18/24**；每消耗一张方块降伤 **6/5 → 6/4**（power 里的叠加常数同步） |
| **打灰机！** `Shmup` | 格挡 **3/5 → 6/8**；抽牌 **1/1 → 1/2**（改用 `CardsVar`，卡面 `抽{Cards:diff()}张牌。`） |
| **消消乐！** `Match3` | 耗能 **0 → 1（升级 0）**；**升级不再给「保留」**（`OnUpgrade` 改成 `EnergyCost.UpgradeBy(-1)`，`AfterDowngraded` 一起删） |
| **植物大战僵尸** `PlantsVsZombies` | 耗能 **0 → 1（升级 0）** |
| **来自花凛的援护** | 伤害 **36/44 → 32/40** |
| **来自晴的协助** `MomoiSupportHare` | 伤害 **4/6 → 6/9**（升级 +3） |
| **来自千寻的协助** `MomoiSupportChihiro` | 伤害 **6/8 → 7/10**（升级 +3） |
| **来自茜的援护** `MomoiSupportAkira` | 伤害 **10/11 → 12/15**（升级 +3） |
| **来自大师的援助** `MomoiSupportYoshimi` | 格挡 **2/3 → 3/4**；伤害 **3/5 → 4/6** |
| **来自小玉的协助** `MomoiSupportKotama` | 临时力量 **2/3 → 3/4** |

#### 2. 🔴 自助指南：只能给「防御」附魔的根因

原版 `Nimble`（灵巧）的筛选条件是**牌面标志**，不是文本：

```csharp
// Core/Models/Enchantments/Nimble.cs
public override bool CanEnchant(CardModel card) => base.CanEnchant(card) && card.GainsBlock;
```

`CardModel.GainsBlock` 默认 `false`，原版每张给格挡的卡都自己 override。**本 mod 只有 `STS2_MomoiDefend` 写了**，
其余 16 张会给格挡的卡都没写 → 「读个一段（灵巧）」的候选里只剩防御，打灰机/翻滚射击/邮件关怀/装备升级/相遇/心流…
全部选不了。

已给这 **16 张**补上 `public override bool GainsBlock => true;`：

`MomoiSupportYoshimi`、`MomoiSupportKotori`、`RollAndShoot`、`AllsWellThatEndsWell`、`MailCare`、`GearUp`、
`Countermeasure`、`PostQuest`、`YellowBlock`、`BlueBlock`、`PurpleBlock`、`GreenBlock`、`TravelFrog`、`Shmup`、
`Encounter`、`FlowState`（+ 原有 `STS2_MomoiDefend`）。

> 附带好处：原版 `CardModel` 会用这个标志**自动挂「格挡」侧栏**（我们自己的文本扫描侧栏本来就有一份，两条都是同一个说明，不冲突）。

#### 3. ? 事件全面体检（逐个对照原版判定条件）

把原版 20+ 个 `?` 事件里所有**按卡牌属性筛选**的地方都过了一遍，逐条核对 mod 内容：

| 事件 | 判定条件 | 我们的情况 |
|---|---|---|
| 自助指南 `SelfHelpBook` | `Nimble` → `GainsBlock`；`Sharp/Vigorous/Instinct/Corrupted` → `CardType.Attack`；`Swift` 任意 | ❌→✅ **本批修好**（16 张补标志） |
| 帕尔 `Pael` | `Goopy` → `Tags.Contains(CardTag.Defend)` 且 ≥3 张 | ✅ `STS2_MomoiDefend` 带 `CardTag.Defend`，起始 4 张 |
| 螺旋漩涡 `SpiralingWhirlpool` | `Spiral` → `Rarity.Basic` 且 Strike/Defend 标签 | ✅ 起始打击/防御都是 Basic + 对应标签 |
| 树木雕刻 `WoodCarvings` | 变化一张 `Rarity.Basic` 且可移除的牌；`Slither` 需非不可打出、非 X 费 | ✅ |
| 上古之石 `StoneOfAllTime` | `Vigorous` → Attack | ✅ |
| 共生体 `Symbiote` | `Corrupted` → Attack；另有变化选项 | ✅ |
| 被遗忘之墓 `GraveOfTheForgotten` | `SoulsPower` → 需自带 `Exhaust` 关键词 | ✅ 我们有大量消耗牌 |
| 蓝宝石种子 `SapphireSeed` / 水淹书房 / 人形孔洞等 | `Sown` / `Steady` / `PerfectFit` → 无类型限制 | ✅ |
| 塔克斯 `Tanx`（≥3 本能）/ 无努佩佩（≥4 迅速） | 按数量统计 | ✅ 起始牌就够 |
| 融合器 `Amalgamator` | 只处理 `Rarity.Basic` | ✅ |
| 大脑水蛭 `BrainLeech` | 用 `owner.Character.CardPool` 生成奖励 | ✅ 我们的池子三档稀有度齐全 |
| **色彩哲学家** `ColorfulPhilosophers` | 选项文案键 = `COLORFUL_PHILOSOPHERS.pages.INITIAL.options.{EnergyColorName 大写}` | ⚠️→✅ 我们的 `EnergyColorName = "STS2_Momoi"`，键 `…options.STS2_MOMOI`；mod 的 `events.json` 里本来有（本批把我误覆盖的标题恢复为「桃红色」） |
| 混沌香气 `AromaOfChaos` | 读 `characters` 表的 `{角色Id}.aromaPrinciple` | ✅ 已有 |
| 战斗木桩 `BattlewornDummy` | 用 `Character.PotionPool` | ✅ |
| 海玻璃 `Orobas/SeaGlass` | 按 `ModelDb.AllCharacters` 展开 | ✅ 已有开关补丁 |

另外补了两处小缺口：
- `characters.json` 补 **`bestiaryQuote`**（图鉴台词，原版每个角色都有，我们缺键）。
- 新增补丁 **`MomoiEnergyIconPathPatch`**：`EnergyIconHelper.GetPath(prefix)` 会把池子的 `EnergyColorName` 拼成
  `atlases/ui_atlas.sprites/card/energy_sts2_momoi.tres`（游戏自带图集里没有这个条目）→ 预加载报 “Asset not cached”，
  多人界面左上角能量图标为空。现在对 `STS2_Momoi` 前缀返回 mod 自己的 `energy_text.png`。

#### 4. 产物 / 验证

- `dotnet build` **0 错误** → DLL **495,616 B**、PCK **130,899,152 B**（10-25 06:30）。
- 新增 `_verify_batch37.py` **55 条**（数值 + `GainsBlock` 全覆盖 + 事件/角色文本兜底 + 标签闭合）；
  同步修正过期断言：`batch12`（大师格挡 3/4、打灰机 6/8、花凛 32 伤）、`batch18`（消消乐升级改费用、去掉保留）、`batch32`（色彩哲学家标题恢复「桃红色」）。
- **二十六套合计 1139 条断言全绿**。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.46")

# ---------------- 工作区文档 ----------------
d = io.open(P_WS, encoding="utf-8").read()
d = re.sub(r"\| 部署 \|.*\|", "| 部署 | `STS2_Momoi.dll` **495,616 B**（10-25 06:30）、`STS2_Momoi.pck` **130,899,152 B**（10-25 06:30） |", d, count=1)
d = re.sub(r"\| 自检 \|.*\|", "| 自检 | **26 套 / 1139 条断言全绿**（`_verify_batch*.py` 通配逐个跑） |", d, count=1)
d = d.replace("跑全部自检（25 套 / 1062 条断言）", "跑全部自检（26 套 / 1139 条断言）")
row = ("| 39 | 10-25 | 九张卡数值/费用（节奏游戏 18/24·6/4、打灰机 6/8·抽1/2、消消乐 1/0 费且升级不再保留、PvZ 1/0 费、"
       "花凛 32/40、晴 6/9、千寻 7/10、茜 12/15、大师 3/4+4/6、小玉 3/4）；**自助指南只能附魔防御的真因**"
       "（16 张给格挡的卡缺 `GainsBlock`）+ ? 事件全面体检（色彩哲学家文案键/桃红色、bestiaryQuote、能量图标路径兜底） |")
anchor = "> 批次 24~26 是**角色动画**"
if anchor in d:
    d = d.replace(anchor, row + "\n\n" + anchor, 1)
else:
    d = d.rstrip("\n") + "\n" + row + "\n"
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
