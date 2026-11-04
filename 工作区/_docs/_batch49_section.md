
### 21.56 批次49：体积砍半 + 多人构想修复 + 贴图缩放 + 能力伤害改原版形状 + 循环叙事重做（1.0.5，2026-11-02）

**一句话**：pck 从 **131,854,936 B 降到 57,834,244 B（-56%）**，发布 zip 从 131 MB 降到 **54.2 MB**；同时修掉多人模式「枯竭灵感给队友发构想」的 bug，
新增「角色贴图大小」滑块，四张能力牌的伤害改成原版能力形状（不吃力量/活力/虚弱/易伤），并重做了循环叙事。

#### 1. 体积：先量再砍

mod 里 95% 的体积是 PNG（源目录 177.55 MB / 1011 文件里 168.76 MB 是 `.png`，其中 `images/cards` 100.07 MB、`images/characters` 65.68 MB），
`.ogv` 4.15 MB + `.ogg` 3.74 MB，没有 psd/aseprite/blend/pdb 这类杂物；dll 本来就是 Release、不带 pdb。

真正进 pck 的是 Godot 导入后的 `ctex`（原 124.71 MB），而默认导入全是**无损**（`compress/mode=0` 占 117.46 MB，VRAM 压缩只占 0.03 MB）。
按用途分两类：

| 资产 | 数量 | 原始尺寸 | 处理 | 依据 |
| --- | --- | --- | --- | --- |
| `images/cards/*.png` | 135 | 1000×760（2 张 606×852） | `process/size_limit=512`，保持无损 | 牌堆里实际显示 < 500 px，512 已是 2 倍冗余；**源图不动**，随时可调回 |
| `images/characters/cue/*.png` | 236 | 600×820（146）/ 1400×1250（50 死亡帧）等 | 有损 WebP `lossy_quality=0.95` | 战斗帧偏扁平，VRAM 压缩反而更大（600×820 BPTC ≈ 0.49 MB/帧 vs 无损 0.19 MB） |

质量怎么验的：`attack1.png`（600×820 / 316 KB）→ WebP q95 **65 KB**；**只算 alpha>8 的可见像素 PSNR = 42.4 dB**（q90 是 40.4 dB）。
整图 PSNR 只有 23.5 dB 是假象——透明区的 RGB 噪声被一起算进去了，没有视觉意义。卡面 1000→512 往返 PSNR 34.8 dB（768 是 43.4 dB），
在牌堆显示尺寸下肉眼看不出差别。

规则固化在 `工作区\_scripts\_optimize_textures.py`（可重复执行，`--check` 只校验不改）：

```
python 工作区\_scripts\_optimize_textures.py          # 1) 写导入规则
Godot_v4.5.1-stable_mono_win64.exe --headless --path . --import   # 2) 重建缓存（约 24 s）
dotnet build "STS2 Momoi.csproj"                      # 3) 导出 pck
```

> ⚠ **`*.import` 被 `.gitignore` 忽略**（`STS2 Momoi/.gitignore` 里有 `*.import`、`.godot/`）。
> 换机器、清缓存、`git clean` 之后**必须先跑第 1 步**再导 pck，否则体积直接回到 131 MB。
> 这也是「pck 只有 55 MB，而源目录还是 177 MB」的原因——源图一张没删。

分目录明细（优化前 ctex）：`images/cards` 68.52 MB、`images/characters/cue` 44.53 MB、`audio` 4.02 MB、`images/powers` 2.26 MB（74 张 256×256）、
`images/characters` 1.43 MB（14 张，含 2 张 2560×1200 选人背景）、`images/relics` 0.55 MB（21 张）、`images/potions` 0.17 MB（6 张）。
唯一未压缩音频是 `audio/gunshot.wav`（0.16 MB），暂留。

#### 2. 多人：枯竭灵感只发给主人

`Relics/DriedInspiration.cs` 的 `AfterPlayerTurnStart(PlayerChoiceContext choiceContext, Player player)` 是全局钩子，**对所有玩家的回合开始都会触发**，
原实现没有判归属，于是队友回合开始也会被塞一张「构想」。修法一行：

```csharp
if (player != Owner) { return; }
```

#### 3. 设置：角色贴图大小

设置页「通用」新增滑块 `character_texture_scale`：**0.2 ~ 1.2，默认 0.7，步长 0.05**，右侧显示 `0.70x`。
只对**玩家**生效，怪物一律不缩放：

- `Patches/MomoiCharacterScalePatch.cs` `MomoiCreatureScaleToPatch`：Prefix `NCreature.ScaleTo(size, duration)`，`Entity.IsPlayer` 为真时 `size *= MomoiSettingsStore.TextureScaleFactor;`
- `MomoiCombatRoomAddCreaturePatch`：Postfix `NCombatRoom.AddCreature`，进战斗房间时补一次 `GetCreatureNode(creature)?.ScaleTo(1f, 0.0)`
  —— 传 **1** 而不是倍率，因为 Prefix 会再乘一次（传倍率就变成平方）。

#### 4. 来自明日奈的援护：减伤持续到「你的下回合开始前」

`AsunaGuardPower` 的 `TickDownDuration` 从 `AfterSideTurnEnd` 挪到 `AfterSideTurnStart(CombatSide, IReadOnlyList<Creature>, ICombatState)`
（原版这个钩子不带 `PlayerChoiceContext`）。于是打出当回合 + 随后的敌方回合都还有减伤，己方**下回合开始时**才掉一层，叠层逻辑不变。
卡面与词条同步：「直到你的下回合开始前，受到的所有伤害降低 {IfUpgraded:show:40%|25%}。」，power 文本去掉「{Amount} 回合内」。

#### 5. 能力伤害统一成原版形状（Unpowered）

构想之矛、矛与盾、节奏游戏、来自大师的援护（`YoshimiRepeatPower`）原来走 `DamageCmd.Attack(...).FromCard(...)` —— 那是**攻击**：
吃力量/活力/虚弱/易伤，还会播攻击动画。原版能力（`PanachePower` / `FlameBarrierPower` / `JuggernautPower`）一律是：

```csharp
await CreatureCmd.Damage(choiceContext, combatState.HittableEnemies, damage, ValueProp.Unpowered, Owner, cardSource, null);
```

`ValueProp.Unpowered` 让 `ValuePropExtensions.IsPoweredAttack()` 返回 false（它要求 `Move` 且**不**含 `Unpowered`），力量/活力/虚弱/易伤全部短路；
`HittableEnemies` 重载一次打全体，需要多段就在外面 `for` 循环（每次调用算一次命中）。顺带删掉援护里手工补的活力加算、易伤 ×1.5 和
`FirepowerHooks.SpendVigorAsync` —— 现在它和原版能力完全一致，**不扣活力**。

#### 6. 数值

| 卡 | 项 | 旧 | 新 |
| --- | --- | --- | --- |
| BA启动！ | 稀有度 / 活力 | 普通 / 2-3 | **罕见 / 3-4** |
| 再启新篇 | 稀有度 | 罕见 | **普通** |

#### 7. 循环叙事重做（1 费技能 · 罕见 · 升级 0 费）

- **注能**：与「开发者协同·绿」（`DevGreen`）共用 `Cards/ImbuedSupport.cs` 的 `IImbuedCard` 接口 + 三个 helper
  （`ImbuedTip` / `CanAutoPlayNow` / `TryAutoPlayAsync`）；`Patches/MomoiImbuedAndCompendiumPatches.cs` 的置底补丁改成按接口收集
  （`pile.Cards.Where(c => c is IImbuedCard)`），不再只认 `DevGreen`。卡面/侧栏沿用 `enchantments.MOMOI_IMBUED` 词条与旧 power 图标。
  语义与附魔版注能一致：`ShouldStartAtBottomOfDrawPile` + 第 1 回合 `CardCmd.AutoPlay`，所以即使置底也照样开局自动打出，不会浪费一次抽牌。
- **效果**：`打出时：本回合结束时，将弃牌堆的最多 1 张牌洗入你的抽牌堆`（原来是「本回合所有进过弃牌堆的牌」）。
  Power 侧栏：「本回合结束时，将[弃牌堆]的最多 {Amount} 张牌洗入你的[抽牌堆]。」；右下角层数 = `Amount`，叠加即加 `Amount`。
- **选择界面**：`new CardSelectorPrefs(new LocString("card_selection", "STS2_MOMOI_CYCLIC_NARRATIVE_HEADER"), 0, max) { Cancelable = true }`。
  `MinSelect = 0` 是刻意的：`CardSelectCmd.FromCombatPile` 在 `!RequireManualConfirmation && num <= MinSelect` 时**不弹界面直接全选**，
  只有 `MinSelect != MaxSelect`（构造 `(prompt, min, max)` 会自动置 `RequireManualConfirmation`）才会让玩家自己确认 ——
  于是「弃牌堆只剩 1 张」时也会让玩家决定要不要洗，且可以跳过不选。模板文本「选择最多 {Amount} 张牌洗入你的抽牌堆。」（`{Amount}` 由 prefs 自动填）。

#### 8. 版本与产物

清单与 csproj 均 **1.0.5**（`min_version: 0.6.7` 不变，构建日志 `STS2-RitsuLib min_version 0.6.7 <= package 0.6.10`）；
`dotnet build` **0 错误 / 31 警告**（与基线一致）；DLL **515,072 B** / PCK **57,834,244 B**；
`工作区\发布包\STS2_Momoi_v1.0.5.zip` **54.2 MB**（顶层 `STS2_Momoi/`，旧 1.0.4 zip 已删）。
工坊 `工作区\工坊发布\STS2_Momoi\Content\STS2_Momoi\` 已同步成 1.0.5（下次 `upload` 即覆盖线上条目 3830602273）。

#### 9. 自检

新增 `工作区\_scripts\_verify_batch49.py`（88 条：体积 / 多人守卫 / 贴图缩放 / 明日奈 / Unpowered / 数值 / 循环叙事 / 版本与 zip / 文档），
并把 **18 条**因本次改动而过期的旧断言就地更新（批次 12 / 13 / 15 / 20 / 24 / 28 / 32 / 40 / 44 / 47）。合计 **35 套 / 1632 条全绿**。

#### 10. 踩的坑

- 首轮贴图优化只改到 `compress/mode`，`lossy_quality` 仍是 0.9 —— 脚本按 `replace("compress/lossy_quality=0.7", …)` 写死了旧值，而实际文件里是 0.9。改成正则整行替换后重跑才对。
- 手写「整块替换类定义」时两次把闭合花括号一起切掉 / 引用已删除的局部变量（`source`），都是一编译就暴露。规矩：先 `_backup\batchNN_pre_*` 备份，改完回读文件确认花括号平衡再 build。
- 自检汇总行的解析别用 `条?` 这种多字节可选量词（MSYS grep 会失配），用 `[0-9]+ 通过` 这种朴素模式。
- 老规矩：heredoc 会吃掉一层反斜杠，写进 md 的 Windows 路径一律用 `chr(92)` 拼，写完扫 `ord(c) < 32`。
