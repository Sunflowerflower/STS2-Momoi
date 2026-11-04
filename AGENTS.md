# AGENTS.md —— 给 AI / 协作者的工程约定

这个仓库是《Slay the Spire 2》角色 Mod「游戏王小桃」的源码。下面这些约定是**踩过坑之后定下来的**，改动时请遵守；不遵守通常会直接导致游戏内崩溃、文本乱码或构建产物体积暴涨。

---

## 1. 环境

- 只支持 Windows 开发（脚本里硬编码了绝对路径 `C:\Users\asus\RiderProjects\STS2 Momoi`）。
- **不要用 `python` 命令**（本机是坏掉的 Windows Store 别名），一律用绝对路径：
  `C:\Users\asus\AppData\Local\Python\pythoncore-3.14-64\python.exe`
- 构建：`cd "STS2 Momoi" && dotnet build "STS2 Momoi.csproj"`（会编译 + 用 Godot headless 导出 `STS2_Momoi.pck` + 部署到 `<游戏目录>/mods/STS2_Momoi/`）。
  只验证 C# 语法时加 `-p:STS2_SKIP_PCK_EXPORT=true`；要看全部警告要 `-t:Rebuild`（增量构建不会重报警告）。
  基线是 **31 个警告 / 0 个错误**，新增警告要修掉。

## 2. 目录职责

| 路径 | 说明 |
|---|---|
| `STS2 Momoi/STS2 MomoiCode/` | 全部 C#。`Entry.cs` 是唯一入口，负责注册卡池、角色、补丁、设置 |
| `STS2 Momoi/STS2 MomoiCode/Cards/` | 卡牌与能力（Power），按主题分文件 |
| `STS2 Momoi/STS2 MomoiCode/Patches/` | Harmony 补丁，每个补丁一个 `IPatchMethod` 实现 |
| `STS2 Momoi/STS2_Momoi/localization/{zhs,eng}/` | 全部文本，**扁平键** JSON |
| `STS2 Momoi/STS2_Momoi/{scenes,scripts,shaders,materials}/` | Godot 侧资源（进 pck） |
| `STS2 Momoi/STS2_Momoi/{images,audio,videos}/` | 大资源，**被 .gitignore 排除**，不要往仓库里加二进制 |
| `STS2_Momoi_迁移文档.md` | 主设计文档，§21.x 按批次记录改动与根因 |
| `工作区/_scripts/` | 自检与发布脚本（`_verify_batch*.py`、`_make_release_zip.py`、`_optimize_textures.py`） |

## 3. 改代码的硬规矩

1. **一张卡一个类**，继承 `ModCardTemplate`，构造函数里 `base(费用, CardType, CardRarity, TargetType)`。
   数值用 `CanonicalVars` 里的 `DamageVar` / `BlockVar` / `DynamicVar` / `CardsVar`，**不要**在 `OnPlay` 里硬编码数字。
2. **给格挡的卡必须 `public override bool GainsBlock => true;`**（原版 `Nimble` 附魔与自动格挡提示都靠它）。
3. **不要在卡牌描述里手写 `固有。` / `消耗。` / `保留。` / `小游戏牌。`** —— 关键词由 `CardKeywordLabelPatch` / `CanonicalKeywords` 自动附加，手写会重复。
4. **文本颜色约定**（与原版一致）：`[gold]` 只给关键词，`[blue]` 给能力数值，`[green]` 给治疗，`[red]` 给风味文本。卡面数字**不加颜色**。
5. **多段攻击**用一次 `AttackCommand.WithHitCount(n)`；需要分段结算时用 `AttackCommand.CreateContextAsync` + `CreatureCmd.Damage` + `ctx.AddHit`，**不要**连开多个 `DamageCmd.Attack().Execute()`（会把 `VigorPower` 的活力快照冲掉）。
6. **能力造成的伤害**要「不吃力量/活力/易伤」时，用 `CreatureCmd.Damage(..., ValueProp.Unpowered, ...)`，不要用 `DamageCmd.Attack(...).Unpowered()`。
7. **手牌选择**（`CardSelectCmd.FromHand` / `FromCombatPile` / `FromChooseACardScreen`）如果之后要延迟恢复 UI holder，`source` 参数传 `null`，否则会留下「白卡面/幽灵节点」。
8. **不要修改战斗内克隆卡的 tag**（`CardModel.CloneForCombat` 不重建 `_tags`，会污染存档）。临时牌用 `MinigameSupport.TemporaryGameCards` 那套机制。
9. **日志**：热路径（每次出牌/每段攻击）一律走 `Diagnostics/MomoiDiag.Log(...)`，它受设置页「输出详细日志」开关控制；`Entry.Logger.Info` 只用于一次性初始化日志。**失败用 `Warn` 且不要加开关**（排障时要能看到）。
10. **补丁**必须在 `Entry.cs` 里 `patcher.RegisterPatch<T>()` 注册；补丁目标用 `[new(typeof(X), nameof(X.Method))]`，目标重载多时传参数类型数组。
11. **设置项**：数据类 `MomoiModSettings` + `MomoiSettingsStore` 里一个 `ModSettingsValueBinding` + 设置页一行，三处都要加；默认值同时要在 `ResetToDefaults()` 里复位。

## 4. 文本与数值的修改流程

1. 先改 C#（数值真值），再改 `localization/zhs/*.json` 与 `localization/eng/*.json`（两语言必须同时改，键名 `STS2_MOMOI_CARD_<CLASS_UPPER_SNAKE>`）。
2. 改完跑自检：`for f in 工作区/_scripts/_verify_batch*.py; do python "$f"; done`（约 38 套 / 1800 条纯文本断言）。
   断言失败通常意味着「你改了某个值而某条旧断言写死了旧值」，需要判断是回归还是过期断言——**不要为了让断言变绿而回退正确的改动**。
3. 新增一层自检脚本时，编号取 `工作区/_scripts/_verify_batch*.py` 里最大值 +1（历史上多次覆盖别人的脚本）。

## 5. 版本与发布

- 版本号要**同时**改两处：`STS2 Momoi/STS2 Momoi.csproj` 的 `<Version>`、`STS2 Momoi/STS2_Momoi.json` 的 `"version"`（自检脚本里也有硬编码，需要一起替换）。
- 清单里的前置依赖写成 `"dependencies": [{ "id": "STS2-RitsuLib", "min_version": "0.6.7" }]`。
  ⚠ 写成 `"version"` 会被加载器**静默忽略**（`ModDependency` 只认 `min_version`）。
- 打包：`工作区/_scripts/_make_release_zip.py`（产出 `工作区/发布包/STS2_Momoi_v<版本>.zip`，顶层目录 `STS2_Momoi/`）。
- 贴图导入规则写在 `*.import`（被 gitignore）：干净克隆后要先跑 `工作区/_scripts/_optimize_textures.py`，否则 pck 会从 55MB 涨到 130MB。
- 工坊上传用 `工作区/工坊发布/ModUploader.exe upload -w STS2_Momoi`（工作区里必须有 `image.png`、`mod_id.txt`；`workspace.json` 的 `dependencies` 是工坊 id 数组，`tags` 只能在这里改）。

## 6. 文档

- 每次功能性改动在 `STS2_Momoi_迁移文档.md` 末尾追加一节 `### 21.<n> 批次<k>：标题（版本，日期）`，写清**根因 + 改法 + 踩坑**；顶部「本次状态」块同步更新。
- 已知的坑与结论请写在文档里而不是只写在 commit message 里——后续维护者（包括 AI）主要靠读这份文档。

## 7. 不要做的事

- 不要把 `images/`、`audio/`、`videos/`、`*.pck`、`*.dll`、`bin/`、`obj/`、`.godot/` 提交进仓库。
- 不要删除 `STS2 Momoi/STS2 MomoiCode` 里被原版抽象类要求的空实现/空类。
- 不要在没有备份的情况下用「整段切片重写」的方式改文件（历史上曾把 `RemainingSpecialCards.cs` 截断成 289 行）；改动一律用精确文本替换。
- 不要在 shell heredoc 里直接把中文 Windows 路径当参数传递（会乱码/吃反斜杠）；用 `chr(92)` 拼路径，写文件后扫一遍控制字符。
