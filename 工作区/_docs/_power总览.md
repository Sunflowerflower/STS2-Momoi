# 模组 power 总览（自动生成 + 人工核对语义）

> 生成脚本：`工作区/_scripts/_power_overview.py`；数据源：`STS2 MomoiCode/**/*.cs` + `localization/zhs/powers.json`。
> 改完 power 之后重跑一次这个脚本即可刷新。

## 名词说明

| 字段 | 含义 |
|---|---|
| **叠加** | `StackType=Counter` 会叠加，`Single` 不叠加 |
| **实例** | `Instanced` = 每次施加都新建一个独立实例（图标会出现多个） |
| **右下角** | power 图标右下角那个数字实际显示什么 |

## 总表

| power | 能否叠加 / 怎么叠加 | 实例 | 右下角 | 文本 |
|---|---|---|---|---|
| "雷酱"炮台支援 | 不叠加（每次打出都是独立实例，各算各的剩余回合） | 独立实例 | 该实例剩余回合数 | 接下来的[blue]{Amount}[/blue]个回合结束时，重复：获得[blue]{Block}[/blue]点[gold]格挡[/gold]、[blue]1[/blue]层[gold]火力[/gold]，对随机敌人造成[blue]{Damage}[/blue]点伤害。 |
| C&C援护进度 | 不叠加 | 唯一 | 纯记录，**不显示** | 记录本局游戏已选择的援护选项（解锁进度）。 |
| 专注 | 层数累加构想数值增量；保留张数只看构想数值（多张取最大） | 唯一 | 叠加层数 | 若你本回合没有打出过[gold]小游戏牌[/gold]，在你的回合结束时使[gold]构想[/gold]数值+[blue]{Amount}[/blue]；若你本回合没有打出过[gold]构想[/gold]，在你的回合结束时可选择最多[blue]{RetainCount}[/blue]张[gold]手牌[/gold][gold]保留[/gold]。 |
| 创造性品味 | 层数 = 每回合加入手牌的牌数 | 唯一 | 叠加层数 | 在你的回合开始时，将[blue]{Amount}[/blue]张随机[gold]小游戏牌[/gold]加入你的[gold]手牌[/gold]。 |
| 创造性品味 | 层数 = 每回合加入手牌的升级牌数 | 唯一 | 叠加层数 | 在你的回合开始时，将[blue]{Amount}[/blue]张[gold]升级[/gold]过的随机[gold]小游戏牌[/gold]加入你的[gold]手牌[/gold]。 |
| 双刀王小桃 | 层数 = 每次触发添加的小刀张数（两者同一个数） | 唯一 | 每次添加的小刀张数 | 本回合当你打出一张不为[gold]小刀[/gold]的[gold]攻击牌[/gold]后，添加[blue]{Amount}[/blue]张[gold]小刀[/gold]到你的[gold]手牌[/gold]。 |
| 双刀王小桃 | 层数 = 每次触发添加的小刀+张数（两者同一个数） | 唯一 | 每次添加的小刀+张数 | 本回合当你打出一张不为[gold]小刀[/gold]的[gold]攻击牌[/gold]后，添加[blue]{Amount}[/blue]张[gold]小刀+[/gold]到你的[gold]手牌[/gold]。 |
| 发布委托 | 不叠加（每次打出都是独立实例） | 独立实例 | **不显示数字** | 下回合开始时，将一张{UpgradedMark}随机[gold]小游戏牌[/gold]放入你的[gold]手牌[/gold]。 |
| 吃豆人 | 不叠加（每次打出都是独立实例，升级/非升级各自生效） | 独立实例 | **不显示数字** | 在你的回合开始时，若你有[red]诅咒[/red]牌，则打出[blue]1[/blue]张{FrenzyName}并随机[gold]消耗[/gold]你的[blue]1[/blue]张[red]诅咒[/red]牌；若你没有[red]诅咒[/red]牌则改为将[blue]1[/blue]张{WinName}加入你的[gold]手牌[/gold]。 |
| 埋下伏笔 | 层数 = 剩余触发次数 | 唯一 | 剩余次数 | 下[blue]{Amount}[/blue]次抽到[gold]构想[/gold]时，使[gold]构想[/gold]数值+[blue]1[/blue]。 |
| 工程部的援助 | 不叠加 | 唯一 | 纯记录，**不显示** | 记录上次选择的援助选项（不可连续选择相同选项）。 |
| 幸运儿的祝福 | 层数 = 剩余回合数；减伤百分比不叠加，取当前持有的最高档（升级 40% 覆盖 25%，反之不覆盖） | 唯一 | 剩余回合数 | [blue]{Amount}[/blue]回合内，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。 |
| 开发秘籍 | 层数 = 被叠加次数；实际增量 = 层数×（普通 1 / 升级 2） | 唯一 | 实际数值增量（Gain） | 打出[gold]小游戏牌[/gold]时使[gold]构想[/gold]升级，数值+[blue]{Gain}[/blue]。 |
| 开发者协同：绿 | 层数 = 回合开始时获得的活力（两者同一个数） | 唯一 | 回合开始时获得的活力 | 在你的回合开始时获得[blue]{Amount}[/blue]点[gold]活力[/gold]。 |
| 当心误射 | 层数 = 剩余触发次数 | 唯一 | 剩余次数 | 下[blue]{Amount}[/blue]次打出[gold]攻击牌[/gold]时，随机将[gold]抽牌堆[/gold]的[blue]1[/blue]张[gold]攻击牌[/gold]加入[gold]手牌[/gold]。 |
| 得道多助 | 层数 = 每回合洗入的支援牌数 | 唯一 | 叠加层数 | 在你的回合开始时，将[blue]{Amount}[/blue]张随机[gold]支援牌[/gold]洗入你的[gold]抽牌堆[/gold]。优先生成未拥有的。 |
| 得道多助 | 层数 = 每回合洗入的升级支援牌数 | 唯一 | 叠加层数 | 在你的回合开始时，将[blue]{Amount}[/blue]张[gold]升级[/gold]过的随机[gold]支援牌[/gold]洗入你的[gold]抽牌堆[/gold]。优先生成未拥有的。 |
| 循环叙事 | 层数 = 剩余持续回合数 | 唯一 | 剩余持续回合数 | 接下来的[blue]{Amount}[/blue]个回合结束时，将本回合所有进入过[gold]弃牌堆[/gold]的牌洗入[gold]抽牌堆[/gold]。 |
| 打灰机 | 不叠加（每次打出都是独立实例） | 独立实例 | **不显示数字** | 当任何生物死亡时，获得[blue]{Block}[/blue]点[gold]格挡[/gold]，将[blue]1[/blue]张[gold]{FuelName}[/gold]放入你的[gold]手牌[/gold]，抽[blue]1[/blue]张牌。 |
| 扫雷 | 层数 = 还能自动打出几次炸弹 | 唯一 | 还剩几次 | 当你下[blue]{Amount}[/blue]次抽到[gold]炸弹[/gold]时，将其直接打出。 |
| 掉到二档了。。。 | 不叠加（每个实例独立） | 独立实例 | 这次实际获得的金币数 | 在战斗结束时，获得[blue]{Gold}[/blue][gold]金币[/gold]。 |
| 日复一日，必有精进 | 层数 = 被叠加次数；实际增量 = 层数×（普通 1 / 升级 2） | 唯一 | 叠加层数（增量） | 生成[gold]构想[/gold]时，立即使其数值+[blue]{Gain}[/blue]。 |
| 暗黑心理学 | 层数 = 触发次数 | 唯一 | 剩余次数 | 下[blue]{Amount}[/blue]次获得[gold]力量[/gold]时将不再获得，改为使[gold]构想[/gold]数值+[blue]1[/blue]。 |
| 构想之盾 | 层数累加到「每张构想格挡」上 | 唯一 | 实际获得的格挡 | 在你的回合结束时，[gold]手牌[/gold]中每有一张[gold]构想[/gold]就获得[blue]{BlockPer}[/blue]点[gold]格挡[/gold]。 |
| 构想之矛 | 层数累加到「每点构想伤害」上 | 唯一 | 对所有敌人造成的伤害 | 当你打出[gold]构想[/gold]时，该[gold]构想[/gold]每有[blue]1[/blue]点数值，就对所有敌人造成[blue]{DamagePer}[/blue]点伤害[blue]1[/blue]次。 |
| 柚子护航 | 层数 = 每回合额外打出的小游戏牌张数 | 唯一 | 叠加层数 | 你每回合打出的前[blue]{Amount}[/blue]张[gold]小游戏牌[/gold]会多打出一次，然后失去[blue]1[/blue]点[gold]活力[/gold]。 |
| 植物大战僵尸 | 不叠加（每次打出都是独立实例，各给各的牌） | 独立实例 | **不显示数字** | 下回合将[gold]{Card}[/gold]加入你的[gold]手牌[/gold]。 |
| 没问题……吗？ | 层数 = 卡牌耗能增加量 | 唯一 | 能量图标 | 卡牌在本回合耗能增加{Amount:energyIcons()}。 |
| 游戏王形态 | 层数累加每张牌首次打出获得的缓冲层数（升级 ×2） | 唯一 | 实际获得的缓冲数 | 每当你生成一张[gold]小游戏牌[/gold]时，为其添加[blue]1[/blue]个随机附魔。⏎首次打出一个牌名的[gold]小游戏牌[/gold]后，获得[blue]{BufferPer}[/blue]层[gold]缓冲[/gold]。 |
| 满手牌结算 | 一张方块最多对应一个 buff：同档位互相覆盖，**升级版额外覆盖非升级版** | 独立实例 | **不显示数字**（层数恒为 1） | 本回合[gold]手牌[/gold]达到上限时：[gold]消耗[/gold]所有[gold]手牌[/gold]，抽[blue]{Cards}[/blue]张牌，获得{Energy:energyIcons()}，将[gold]弃牌堆[/gold]的所有[gold]方块[/gold]返回[gold]手牌[/gold]，并[gold]消耗[/gold][gold]俄罗斯方块[/gold]。 |
| 火力 | 层数 = 可拦截的活力消耗次数 | 唯一 | 火力层数 | 当[gold]活力[/gold]将被全部消耗时，改为消耗[blue]1[/blue]层[gold]火力[/gold]并保留[gold]活力[/gold]。 |
| 火焰附加 | 层数累加到「附带灼烧层数」上 | 唯一 | 被击中敌人拿到的灼烧层数 | 当你拥有[gold]火力[/gold]时，每当你造成伤害时，被击中的敌人获得[blue]{BurnTotal}[/blue]层[gold]灼烧[/gold]。 |
| 灵感爆发 | 层数 = 触发时加入手牌的牌数 | 唯一 | 叠加层数 | 当你打出数值不低于[blue]6[/blue]的[gold]构想[/gold]后，将[blue]{Amount}[/blue]张[gold]我的回合！[/gold]加入你的[gold]手牌[/gold]。 |
| 灵感爆发 | 层数 = 触发时加入手牌的牌数 | 唯一 | 叠加层数 | 当你打出数值不低于[blue]5[/blue]的[gold]构想[/gold]后，将[blue]{Amount}[/blue]张[gold]我的回合！+[/gold]加入你的[gold]手牌[/gold]。 |
| 灼烧 | 层数 = 灼烧伤害 | 唯一 | 灼烧层数 | 在其回合开始时失去[blue]{Amount}[/blue]点生命。⏎拥有[gold]灼烧[/gold]的敌人每次造成未被格挡的伤害时，附加[blue]1[/blue]层[gold]灼烧[/gold]。 |
| 灼烧·剩余回合 | 不叠加（与灼烧同生共死） | 唯一 | 灼烧剩余回合数 | [gold]灼烧[/gold]的剩余回合数。归零时与[gold]灼烧[/gold]一起消失。 |
| 真理部的协助 | 不叠加 | 唯一 | 纯记录，**不显示** | 记录已选择的援助选项（全部选过后解锁新选项）。 |
| 矛与盾 | 层数累加到格挡与伤害上 | 唯一 | 叠加层数 | 当你打出[gold]构想[/gold]时，该[gold]构想[/gold]每有[blue]1[/blue]点数值，就获得[blue]{BlockPer}[/blue]点[gold]格挡[/gold]。⏎在你的回合结束时，[gold]手牌[/gold]中每有一张[gold]构想[/gold]就对所有敌人造成[blue]{DamagePer}[/blue]点伤害。 |
| 终于上一档了！ | 不叠加（每个实例独立；层数 = 剩余可维持回合数，初始 2） | 独立实例 | 剩余回合数 | 在战斗结束时，额外获得[blue]{GoldFull}[/blue][gold]金币[/gold]和[blue]1[/blue]份卡牌奖励。 |
| 能量保留 | 层数 = 剩余生效回合数（回合结束 -1；0 层时还要拦一次重置才消失） | 唯一 | 剩余生效回合数 | 下[blue]{Amount}[/blue]个回合结束时，多余的能量可以留到下一回合。 |
| 节奏游戏！ | 层数累加到伤害上（每张独立数值相加） | 唯一 | 叠加层数 | 在你的回合开始时，将[blue]1[/blue]~[blue]4[/blue]张[gold]方块[/gold]加入你的[gold]手牌[/gold]。在你的回合结束时，[gold]消耗[/gold]所有[gold]方块[/gold]，并对所有敌人造成[blue]{DamageTotal}[/blue]点伤害；每以该法[gold]消耗[/gold][blue]1[/blue]张[gold]方块[/gold]，该伤害降低[blue]{PerBlockTotal}[/blue]点。 |
| 蒙太奇 | 层数 = 回合结束打出的牌数 | 唯一 | 叠加层数 | 回合结束时，从你的[gold]抽牌堆[/gold]中选择[blue]{Amount}[/blue]张牌将其打出。如果这张牌与你打出的上一张牌类型相同/不同，将[blue]1[/blue]张[gold]构想[/gold]加入你的[gold]手牌[/gold]/使[gold]构想[/gold]数值+[blue]1[/blue]。 |
| 虚拟女仆武器 | 层数 = 剩余触发次数 | 唯一 | 剩余次数 | 下[blue]{Amount}[/blue]次打出[gold]攻击牌[/gold]时，将一张[gold]当心误射！[/gold]加入你的[gold]手牌[/gold]并打出。 |
| 虚拟女仆武器 | 层数 = 剩余触发次数 | 唯一 | 剩余次数 | 下[blue]{Amount}[/blue]次打出[gold]攻击牌[/gold]时，将一张[gold]当心误射！+[/gold]加入你的[gold]手牌[/gold]并打出。 |
| 见识下我的实力吧 | 不叠加（每张独立实例，各自算 10 张倒计时） | 独立实例 | 距离下次获得能量的出牌数 | 你每打出[blue]10[/blue]张牌时，获得{EnergyPer:energyIcons()}。 |
| 角色扮演 | 不叠加（每次打出都是独立实例） | 独立实例 | **不显示数字** | 在你的回合开始时，将[blue]1[/blue]张[gold]{SplashName}[/gold]（[gold]消耗[/gold]）放入所有玩家的[gold]手牌[/gold]中。 |
| 贪吃蛇 | 不叠加（未升级版；每次打出都是独立实例，只管自己放出去的那三张牌） | 独立实例 | **不显示数字** | 每当你打出一张牌时，随机化[gold]{MaulName}[/gold]，[gold]{SnakeName}[/gold]和[gold]{FireName}[/gold]的耗能。 |
| 贪吃蛇 | 不叠加（升级版；每次打出都是独立实例，只管自己放出去的那三张牌） | 独立实例 | **不显示数字** | 每当你打出一张牌时，随机化[gold]{MaulName}[/gold]，[gold]{SnakeName}[/gold]和[gold]{FireName}[/gold]的耗能。 |
| 赖招复读 | 不叠加（记录所选牌） | 独立实例 | **不显示数字** | 在你的回合开始时，将所选牌的复制品加入你的[gold]手牌[/gold]。 |
| 重整旗鼓 | 不叠加（每张重整旗鼓独立存在，打出构想依次触发） | 独立实例 | 当前即将回复的生命值（实时） | 每当你打出[gold]构想[/gold]后，回复[green]{HealPer}[/green]点生命并获得[blue]{VigorPer}[/blue]点[gold]活力[/gold]。 |
| 额外回合 | 层数 = 剩余额外回合数 | 唯一 | 剩余额外回合数 | 下[blue]{Amount}[/blue]个回合结束时，额外获得一回合。 |
| （无标题） | 层数 = 本回合获得的力量（原版临时力量写法） | 唯一 | 力量层数；标题显示的是来源卡名「来自小玉的协助」 |  |

## 逐个详情

### "雷酱"炮台支援

- 类名：`YoshimiRepeatPower`（AssistCards.cs）
- 叠加：不叠加（每次打出都是独立实例，各算各的剩余回合）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：该实例剩余回合数
- 文本：接下来的[blue]{Amount}[/blue]个回合结束时，重复：获得[blue]{Block}[/blue]点[gold]格挡[/gold]、[blue]1[/blue]层[gold]火力[/gold]，对随机敌人造成[blue]{Damage}[/blue]点伤害。

### C&C援护进度

- 类名：`CnCTrackerPower`（AssistCards2.cs）
- 叠加：不叠加
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：纯记录，**不显示**
- 文本：记录本局游戏已选择的援护选项（解锁进度）。

### 专注

- 类名：`FocusPower`（RemainingCards3.cs）
- 叠加：层数累加构想数值增量；保留张数只看构想数值（多张取最大）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：若你本回合没有打出过[gold]小游戏牌[/gold]，在你的回合结束时使[gold]构想[/gold]数值+[blue]{Amount}[/blue]；若你本回合没有打出过[gold]构想[/gold]，在你的回合结束时可选择最多[blue]{RetainCount}[/blue]张[gold]手牌[/gold][gold]保留[/gold]。

### 创造性品味

- 类名：`CreativeTastePower`（MinigameFlowCards.cs）
- 叠加：层数 = 每回合加入手牌的牌数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：在你的回合开始时，将[blue]{Amount}[/blue]张随机[gold]小游戏牌[/gold]加入你的[gold]手牌[/gold]。

### 创造性品味

- 类名：`CreativeTasteUpgradedPower`（MinigameFlowCards.cs）
- 叠加：层数 = 每回合加入手牌的升级牌数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：在你的回合开始时，将[blue]{Amount}[/blue]张[gold]升级[/gold]过的随机[gold]小游戏牌[/gold]加入你的[gold]手牌[/gold]。

### 双刀王小桃

- 类名：`DualBladeMomoiPower`（ReworkBatch.cs）
- 叠加：层数 = 每次触发添加的小刀张数（两者同一个数）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：每次添加的小刀张数
- 文本：本回合当你打出一张不为[gold]小刀[/gold]的[gold]攻击牌[/gold]后，添加[blue]{Amount}[/blue]张[gold]小刀[/gold]到你的[gold]手牌[/gold]。

### 双刀王小桃

- 类名：`DualBladeMomoiUpgradedPower`（ReworkBatch.cs）
- 叠加：层数 = 每次触发添加的小刀+张数（两者同一个数）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：每次添加的小刀+张数
- 文本：本回合当你打出一张不为[gold]小刀[/gold]的[gold]攻击牌[/gold]后，添加[blue]{Amount}[/blue]张[gold]小刀+[/gold]到你的[gold]手牌[/gold]。

### 发布委托

- 类名：`PostQuestPower`（MinigameFlowCards.cs）
- 叠加：不叠加（每次打出都是独立实例）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：**不显示数字**
- 文本：下回合开始时，将一张{UpgradedMark}随机[gold]小游戏牌[/gold]放入你的[gold]手牌[/gold]。

### 吃豆人

- 类名：`PacManPower`（RemainingCards5.cs）
- 叠加：不叠加（每次打出都是独立实例，升级/非升级各自生效）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：**不显示数字**
- 文本：在你的回合开始时，若你有[red]诅咒[/red]牌，则打出[blue]1[/blue]张{FrenzyName}并随机[gold]消耗[/gold]你的[blue]1[/blue]张[red]诅咒[/red]牌；若你没有[red]诅咒[/red]牌则改为将[blue]1[/blue]张{WinName}加入你的[gold]手牌[/gold]。

### 埋下伏笔

- 类名：`PlantForeshadowPower`（NewCardsBatch.cs）
- 叠加：层数 = 剩余触发次数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：剩余次数
- 文本：下[blue]{Amount}[/blue]次抽到[gold]构想[/gold]时，使[gold]构想[/gold]数值+[blue]1[/blue]。

### 工程部的援助

- 类名：`EngineeringDeptAidPower`（AssistCards.cs）
- 叠加：不叠加
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：纯记录，**不显示**
- 文本：记录上次选择的援助选项（不可连续选择相同选项）。

### 幸运儿的祝福

- 类名：`AsunaGuardPower`（AssistCards2.cs）
- 叠加：层数 = 剩余回合数；减伤百分比不叠加，取当前持有的最高档（升级 40% 覆盖 25%，反之不覆盖）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：剩余回合数
- 文本：[blue]{Amount}[/blue]回合内，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。

### 开发秘籍

- 类名：`DevSecretsPower`（RemainingSpecialCards.cs）
- 叠加：层数 = 被叠加次数；实际增量 = 层数×（普通 1 / 升级 2）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：实际数值增量（Gain）
- 文本：打出[gold]小游戏牌[/gold]时使[gold]构想[/gold]升级，数值+[blue]{Gain}[/blue]。

### 开发者协同：绿

- 类名：`DevGreenPower`（RemainingSpecialCards.cs）
- 叠加：层数 = 回合开始时获得的活力（两者同一个数）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：回合开始时获得的活力
- 文本：在你的回合开始时获得[blue]{Amount}[/blue]点[gold]活力[/gold]。

### 当心误射

- 类名：`WatchOutPower`（WatchOut.cs）
- 叠加：层数 = 剩余触发次数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：剩余次数
- 文本：下[blue]{Amount}[/blue]次打出[gold]攻击牌[/gold]时，随机将[gold]抽牌堆[/gold]的[blue]1[/blue]张[gold]攻击牌[/gold]加入[gold]手牌[/gold]。

### 得道多助

- 类名：`HelpFromManyPower`（RemainingCards3.cs）
- 叠加：层数 = 每回合洗入的支援牌数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：在你的回合开始时，将[blue]{Amount}[/blue]张随机[gold]支援牌[/gold]洗入你的[gold]抽牌堆[/gold]。优先生成未拥有的。

### 得道多助

- 类名：`HelpFromManyUpgradedPower`（RemainingCards3.cs）
- 叠加：层数 = 每回合洗入的升级支援牌数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：在你的回合开始时，将[blue]{Amount}[/blue]张[gold]升级[/gold]过的随机[gold]支援牌[/gold]洗入你的[gold]抽牌堆[/gold]。优先生成未拥有的。

### 循环叙事

- 类名：`CyclicNarrativePower`（NewCardsBatch.cs）
- 叠加：层数 = 剩余持续回合数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：剩余持续回合数
- 文本：接下来的[blue]{Amount}[/blue]个回合结束时，将本回合所有进入过[gold]弃牌堆[/gold]的牌洗入[gold]抽牌堆[/gold]。

### 打灰机

- 类名：`ShmupPower`（RemainingCards4.cs）
- 叠加：不叠加（每次打出都是独立实例）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：**不显示数字**
- 文本：当任何生物死亡时，获得[blue]{Block}[/blue]点[gold]格挡[/gold]，将[blue]1[/blue]张[gold]{FuelName}[/gold]放入你的[gold]手牌[/gold]，抽[blue]1[/blue]张牌。

### 扫雷

- 类名：`MinesweeperPower`（RemainingCards4.cs）
- 叠加：层数 = 还能自动打出几次炸弹
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：还剩几次
- 文本：当你下[blue]{Amount}[/blue]次抽到[gold]炸弹[/gold]时，将其直接打出。

### 掉到二档了。。。

- 类名：`FellToSecondTierPower`（RemainingCards2.cs）
- 叠加：不叠加（每个实例独立）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：这次实际获得的金币数
- 文本：在战斗结束时，获得[blue]{Gold}[/blue][gold]金币[/gold]。

### 日复一日，必有精进

- 类名：`LearnByDoingPower`（RemainingSpecialCards.cs）
- 叠加：层数 = 被叠加次数；实际增量 = 层数×（普通 1 / 升级 2）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数（增量）
- 文本：生成[gold]构想[/gold]时，立即使其数值+[blue]{Gain}[/blue]。

### 暗黑心理学

- 类名：`DarkPsychologyPower`（DarkPsychology.cs）
- 叠加：层数 = 触发次数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：剩余次数
- 文本：下[blue]{Amount}[/blue]次获得[gold]力量[/gold]时将不再获得，改为使[gold]构想[/gold]数值+[blue]1[/blue]。

### 构想之盾

- 类名：`ConceptShieldPower`（ConceptFlowCards.cs）
- 叠加：层数累加到「每张构想格挡」上
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：实际获得的格挡
- 文本：在你的回合结束时，[gold]手牌[/gold]中每有一张[gold]构想[/gold]就获得[blue]{BlockPer}[/blue]点[gold]格挡[/gold]。

### 构想之矛

- 类名：`ConceptSpearPower`（ConceptFlowCards.cs）
- 叠加：层数累加到「每点构想伤害」上
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：对所有敌人造成的伤害
- 文本：当你打出[gold]构想[/gold]时，该[gold]构想[/gold]每有[blue]1[/blue]点数值，就对所有敌人造成[blue]{DamagePer}[/blue]点伤害[blue]1[/blue]次。

### 柚子护航

- 类名：`YuzuEscortPower`（YuzuEscort.cs）
- 叠加：层数 = 每回合额外打出的小游戏牌张数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：你每回合打出的前[blue]{Amount}[/blue]张[gold]小游戏牌[/gold]会多打出一次，然后失去[blue]1[/blue]点[gold]活力[/gold]。

### 植物大战僵尸

- 类名：`PlantsNextTurnPower`（RemainingCards5.cs）
- 叠加：不叠加（每次打出都是独立实例，各给各的牌）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：**不显示数字**
- 文本：下回合将[gold]{Card}[/gold]加入你的[gold]手牌[/gold]。

### 没问题……吗？

- 类名：`NoProblemPower`（CommonAttackCards.cs）
- 叠加：层数 = 卡牌耗能增加量
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：能量图标
- 文本：卡牌在本回合耗能增加{Amount:energyIcons()}。

### 游戏王形态

- 类名：`GameKingFormPower`（RemainingCards3.cs）
- 叠加：层数累加每张牌首次打出获得的缓冲层数（升级 ×2）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：实际获得的缓冲数
- 文本：每当你生成一张[gold]小游戏牌[/gold]时，为其添加[blue]1[/blue]个随机附魔。  
    首次打出一个牌名的[gold]小游戏牌[/gold]后，获得[blue]{BufferPer}[/blue]层[gold]缓冲[/gold]。

### 满手牌结算

- 类名：`TetrisFullHandPower`（RemainingCards5.cs）
- 叠加：一张方块最多对应一个 buff：同档位互相覆盖，**升级版额外覆盖非升级版**
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：**不显示数字**（层数恒为 1）
- 文本：本回合[gold]手牌[/gold]达到上限时：[gold]消耗[/gold]所有[gold]手牌[/gold]，抽[blue]{Cards}[/blue]张牌，获得{Energy:energyIcons()}，将[gold]弃牌堆[/gold]的所有[gold]方块[/gold]返回[gold]手牌[/gold]，并[gold]消耗[/gold][gold]俄罗斯方块[/gold]。

### 火力

- 类名：`FirepowerPower`（FirepowerPower.cs）
- 叠加：层数 = 可拦截的活力消耗次数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：火力层数
- 文本：当[gold]活力[/gold]将被全部消耗时，改为消耗[blue]1[/blue]层[gold]火力[/gold]并保留[gold]活力[/gold]。

### 火焰附加

- 类名：`FlameAttachPower`（FlameAttach.cs）
- 叠加：层数累加到「附带灼烧层数」上
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：被击中敌人拿到的灼烧层数
- 文本：当你拥有[gold]火力[/gold]时，每当你造成伤害时，被击中的敌人获得[blue]{BurnTotal}[/blue]层[gold]灼烧[/gold]。

### 灵感爆发

- 类名：`InspirationPower`（RemainingCards3.cs）
- 叠加：层数 = 触发时加入手牌的牌数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：当你打出数值不低于[blue]6[/blue]的[gold]构想[/gold]后，将[blue]{Amount}[/blue]张[gold]我的回合！[/gold]加入你的[gold]手牌[/gold]。

### 灵感爆发

- 类名：`InspirationUpgradedPower`（RemainingCards3.cs）
- 叠加：层数 = 触发时加入手牌的牌数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：当你打出数值不低于[blue]5[/blue]的[gold]构想[/gold]后，将[blue]{Amount}[/blue]张[gold]我的回合！+[/gold]加入你的[gold]手牌[/gold]。

### 灼烧

- 类名：`BurnPower`（BurnPower.cs）
- 叠加：层数 = 灼烧伤害
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：灼烧层数
- 文本：在其回合开始时失去[blue]{Amount}[/blue]点生命。  
    拥有[gold]灼烧[/gold]的敌人每次造成未被格挡的伤害时，附加[blue]1[/blue]层[gold]灼烧[/gold]。

### 灼烧·剩余回合

- 类名：`BurnTurnsPower`（BurnPower.cs）
- 叠加：不叠加（与灼烧同生共死）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：灼烧剩余回合数
- 文本：[gold]灼烧[/gold]的剩余回合数。归零时与[gold]灼烧[/gold]一起消失。

### 真理部的协助

- 类名：`VeritasTrackerPower`（AssistCards2.cs）
- 叠加：不叠加
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：纯记录，**不显示**
- 文本：记录已选择的援助选项（全部选过后解锁新选项）。

### 矛与盾

- 类名：`SpearShieldPower`（ConceptFlowCards.cs）
- 叠加：层数累加到格挡与伤害上
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：当你打出[gold]构想[/gold]时，该[gold]构想[/gold]每有[blue]1[/blue]点数值，就获得[blue]{BlockPer}[/blue]点[gold]格挡[/gold]。  
    在你的回合结束时，[gold]手牌[/gold]中每有一张[gold]构想[/gold]就对所有敌人造成[blue]{DamagePer}[/blue]点伤害。

### 终于上一档了！

- 类名：`RankUpPower`（RemainingCards2.cs）
- 叠加：不叠加（每个实例独立；层数 = 剩余可维持回合数，初始 2）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：剩余回合数
- 文本：在战斗结束时，额外获得[blue]{GoldFull}[/blue][gold]金币[/gold]和[blue]1[/blue]份卡牌奖励。

### 能量保留

- 类名：`WinEnergyPower`（RemainingSpecialCards.cs）
- 叠加：层数 = 剩余生效回合数（回合结束 -1；0 层时还要拦一次重置才消失）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：剩余生效回合数
- 文本：下[blue]{Amount}[/blue]个回合结束时，多余的能量可以留到下一回合。

### 节奏游戏！

- 类名：`RhythmGamePower`（RemainingCards5.cs）
- 叠加：层数累加到伤害上（每张独立数值相加）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：在你的回合开始时，将[blue]1[/blue]~[blue]4[/blue]张[gold]方块[/gold]加入你的[gold]手牌[/gold]。在你的回合结束时，[gold]消耗[/gold]所有[gold]方块[/gold]，并对所有敌人造成[blue]{DamageTotal}[/blue]点伤害；每以该法[gold]消耗[/gold][blue]1[/blue]张[gold]方块[/gold]，该伤害降低[blue]{PerBlockTotal}[/blue]点。

### 蒙太奇

- 类名：`MontagePower`（ReworkBatch.cs）
- 叠加：层数 = 回合结束打出的牌数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：叠加层数
- 文本：回合结束时，从你的[gold]抽牌堆[/gold]中选择[blue]{Amount}[/blue]张牌将其打出。如果这张牌与你打出的上一张牌类型相同/不同，将[blue]1[/blue]张[gold]构想[/gold]加入你的[gold]手牌[/gold]/使[gold]构想[/gold]数值+[blue]1[/blue]。

### 虚拟女仆武器

- 类名：`MaidWeaponPower`（ReworkBatch.cs）
- 叠加：层数 = 剩余触发次数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：剩余次数
- 文本：下[blue]{Amount}[/blue]次打出[gold]攻击牌[/gold]时，将一张[gold]当心误射！[/gold]加入你的[gold]手牌[/gold]并打出。

### 虚拟女仆武器

- 类名：`MaidWeaponUpgradedPower`（ReworkBatch.cs）
- 叠加：层数 = 剩余触发次数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：剩余次数
- 文本：下[blue]{Amount}[/blue]次打出[gold]攻击牌[/gold]时，将一张[gold]当心误射！+[/gold]加入你的[gold]手牌[/gold]并打出。

### 见识下我的实力吧

- 类名：`ShowMyStrengthPower`（RemainingSpecialCards.cs）
- 叠加：不叠加（每张独立实例，各自算 10 张倒计时）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：距离下次获得能量的出牌数
- 文本：你每打出[blue]10[/blue]张牌时，获得{EnergyPer:energyIcons()}。

### 角色扮演

- 类名：`RolePlayPower`（MultiplayerCards.cs）
- 叠加：不叠加（每次打出都是独立实例）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：**不显示数字**
- 文本：在你的回合开始时，将[blue]1[/blue]张[gold]{SplashName}[/gold]（[gold]消耗[/gold]）放入所有玩家的[gold]手牌[/gold]中。

### 贪吃蛇

- 类名：`SnakeGamePower`（RemainingCards4.cs）
- 叠加：不叠加（未升级版；每次打出都是独立实例，只管自己放出去的那三张牌）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：**不显示数字**
- 文本：每当你打出一张牌时，随机化[gold]{MaulName}[/gold]，[gold]{SnakeName}[/gold]和[gold]{FireName}[/gold]的耗能。

### 贪吃蛇

- 类名：`SnakeGameUpgradedPower`（RemainingCards4.cs）
- 叠加：不叠加（升级版；每次打出都是独立实例，只管自己放出去的那三张牌）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：**不显示数字**
- 文本：每当你打出一张牌时，随机化[gold]{MaulName}[/gold]，[gold]{SnakeName}[/gold]和[gold]{FireName}[/gold]的耗能。

### 赖招复读

- 类名：`RepeatMovePower`（ReworkBatch.cs）
- 叠加：不叠加（记录所选牌）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：**不显示数字**
- 文本：在你的回合开始时，将所选牌的复制品加入你的[gold]手牌[/gold]。

### 重整旗鼓

- 类名：`RallyAgainPower`（RemainingCards3.cs）
- 叠加：不叠加（每张重整旗鼓独立存在，打出构想依次触发）
- 实例：每次施加新建独立实例（`Instanced`）
- 右下角：当前即将回复的生命值（实时）
- 文本：每当你打出[gold]构想[/gold]后，回复[green]{HealPer}[/green]点生命并获得[blue]{VigorPer}[/blue]点[gold]活力[/gold]。

### 额外回合

- 类名：`MyTurnPower`（RemainingCards3.cs）
- 叠加：层数 = 剩余额外回合数
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：剩余额外回合数
- 文本：下[blue]{Amount}[/blue]个回合结束时，额外获得一回合。

### （无标题）

- 类名：`KotamaStrengthPower`（AssistCards2.cs）
- 叠加：层数 = 本回合获得的力量（原版临时力量写法）
- 实例：同一目标上只有一个（新施加叠层）
- 右下角：力量层数；标题显示的是来源卡名「来自小玉的协助」
- 文本：

