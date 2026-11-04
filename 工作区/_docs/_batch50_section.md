### 21.57 批次50：绝地求生括号 / 明日奈层数 / 循环叙事时机（1.0.6，2026-11-02）

**背景**：批次49 实机反馈三条（一是文本，二是文本，三是循环叙事的报错与手感）。

#### 1. 绝地求生：括号里的推算值只在战斗中显示

`STS2_MOMOI_CARD_BATTLE_ROYALE.description` / `.smartDescription` 末尾的「（抽{N}张牌，获得{N}能量）」改成 `{InCombat:（…）|}` 包裹（和 火力爆发 / 剧本打击 / 天马行空 同一套写法，见 §21.53），局外看图鉴时不再显示这行推算值；嵌套的 `{CalculatedCards:diff()}` / `{CalculatedEnergy:energyIcons()}` 在 InCombat 分支里正常解析。英文同理 `{InCombat: (Draw …)|}`（前导空格放进分支里，局外不留尾随空格）。

#### 2. 来自明日奈的援护：power 文本显示剩余回合数

- **卡面不动**（固定 40%/25%）；**power 文本**改成「直到你的下[blue]{Amount}[/blue]个回合开始前，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。」（eng `Until the start of your next [blue]{Amount}[/blue] turn(s), …`），`{Amount}` 就是叠加后的剩余回合数。
- **叠加逻辑没改**：`PowerCmd.Apply(…, 1, …)` 让 `Amount`（`PowerStackType.Counter`，右下角计数器直接显示 `Amount`）递增 = 持续回合数 +1；百分比走 `ApplySource(cardSource)` 的规则「升级的 40% 覆盖 25%，25% 覆盖不了 40%」，所以「25% 叠加到 40% 上」只加回合数、不改百分比，反过来 40% 既覆盖百分比也加回合数。
- 计时仍在 `AfterSideTurnStart`（`PowerCmd.TickDownDuration(this)`，批次49 从 `AfterSideTurnEnd` 挪过来的），即覆盖「打出当回合 + 之后的敌方回合」，到自己下回合开始时减 1，减到 0 消失。

#### 3. 循环叙事：报错、时机、一次性

用户反馈「打出循环叙事后，下回合开始时局内报错」+「power 应该在触发效果后直接消失，而不是只减少一个层数」+「时机应该在丢牌之前，参考原版战士的能力牌惊逃」。

**排查结论**：`%APPDATA%\SlayTheSpire2\logs\godot.log`（含 1.0.5 实机那段，07:49 落盘）里**没有本模组抛出的异常** —— 4 处 `NullReferenceException` 的栈顶都是 `NPauseMenu.CloseToMenu()` / `NMainMenu.OnContinueButtonPressed`（KitLib 的老问题），退出时的 `ObjectDisposedException … NGlobalUi` 来自 `KitLib.UI.DevPanelUI.SpliceRail`；循环叙事那段只有 12 条 `[Imbued] CyclicNarrative auto-played at combat start` 和一条 `Player 1 chose cards []`（选择界面确实弹出、玩家选了 0 张），没有任何 `[Imbued] … fail`。

**真正的时序问题**（按原版回合结束顺序，`Core/Combat/CombatManager.cs` 核对）：

```
Hook.BeforeSideTurnEnd            (:1522)
  → Hook.BeforeFlush              (:1550)
  → FlushPlayerHand               (:1665 → 内部 :1710 CardPileCmd.Add(cardsToFlush, PileType.Discard))
  → Hook.AfterSideTurnEnd         (:1676)
```

旧实现挂在 `AfterSideTurnEnd`，也就是**弃手牌之后**：弃牌堆里已经混进本回合刚弃掉的手牌，而且这些卡的节点正处在「归位 / 回收」动画中，此时再用**带动画**的 `CardPileCmd.Add(selected, PileType.Draw, …)` 把牌塞进抽牌堆，节点的归属就和「下回合重建手牌 / 抽牌」撞车 —— 症状正好是「下回合开始时报错」（和 §21.36 桃味气泡水的白卡是同一类问题：牌堆数据变了、节点没跟上）。

**改法**：

| 项 | 旧 | 新 |
|---|---|---|
| 时机 | `AfterSideTurnEnd`（弃手牌之后） | `BeforeSideTurnEnd`（弃手牌之前；原版 `TheBombPower` / `HailstormPower` 也挂这里） |
| 结束 | `PowerCmd.TickDownDuration(this)`（减一层） | `await PowerCmd.Remove(this)`（触发后直接消失，一次性；层数只表示「这次最多能选几张」） |
| 搬运 | `CardPileCmd.Add(selected, PileType.Draw, CardPilePosition.Random)` | 同上 + `skipVisuals: true`（回合结束阶段不做归位动画，避免节点撞车） |
| 兜底 | 无 | `try/catch` + `[Cyclic] moved N card(s) from discard to draw pile` / `[Cyclic] end-of-turn shuffle failed: …` |

选择界面仍是 `CardSelectorPrefs(prompt, 0, max) { Cancelable = true }`：`MinSelect(0) != MaxSelect` 才会强制弹窗，所以就算弃牌堆只有 1 张，也让玩家自己决定要不要洗回去；选 0 张 = 跳过（`FromCombatPile` 返回空集合直接不进 `CardPileCmd.Add`）。

#### 版本与自检

- csproj / 清单 **1.0.6**（`min_version` 仍 0.6.7）；DLL **515,072 B**、PCK **57,832,996 B**；`工作区\发布包\STS2_Momoi_v1.0.6.zip`（54.2 MB，`STS2_Momoi_v1.0.5.zip` 已删）；`工作区\工坊发布\STS2_Momoi\Content\STS2_Momoi\` 同步 1.0.6（**没有上传**，等实机确认后再传）。
- 新脚本 `工作区\_scripts\_verify_batch50.py`（38 条）；同步修正批次49 遗留的 8 条过期断言（`_verify_batch12.py` 2 条、`_verify_batch13.py` 1 条、`_verify_batch16.py` 1 条、`_verify_batch49.py` 4 条）。全量 **36 套 / 1671 条断言全绿**。

#### 教训

- 「回合结束」有 5 个钩子（`BeforeSideTurnEndVeryEarly` / `BeforeSideTurnEndEarly` / `BeforeSideTurnEnd` / `AfterSideTurnEnd` / `AfterSideTurnEndLate`），**弃手牌发生在 `BeforeSideTurnEnd` 之后、`AfterSideTurnEnd` 之前**；想「丢牌之前结算」只能用 `BeforeSideTurnEnd`（带 `PlayerChoiceContext`）。
- 回合结束/开始这类阶段里改牌堆数据，尽量 `skipVisuals: true`，别让节点动画跨越阶段边界。
- 自检里按「花括号深度」切类定义时，`class X : Base, IInterface` 的接口列表在 `{` **之前**，不在块内 —— 判断「是否实现某接口」要匹配声明行。
- 版本号批量替换（`1.0.5` → `1.0.6`）只应落在版本断言与 csproj / 清单上，替换后要 grep 确认没有误伤文本。
