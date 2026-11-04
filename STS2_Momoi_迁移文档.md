# STS2_Momoi 角色 Mod —— 迁移交接文档（2026-10-25 版）

> **取代**：2026-10-02 版本文档（同路径，内容已并入本文件）。
> **数据来源**：
> - 主会话 `…\sessions\--C--Users-asus-RiderProjects-STS2 Momoi--\2026-09-24T15-52-55-390Z_01a0d41e-….jsonl`（141 MB / 5205 条，覆盖 08-23 → 09-25 05:37 UTC，5 次压缩）
> - 续篇会话 `…\2026-09-25T05-39-04-810Z_01a0d713-….jsonl`（134 MB / 985 条，覆盖 09-25 05:39 → 09-26 10:47 UTC）
> - **2026-10-02 会话**：`工作区\卡面成品3` 全量接入 + 构建部署 + 未完成卡面重新统计（见 §15）。
> - **2026-10-04 会话**：删除天意侵蚀 / 新增「绷住」链 4 张卡 / `工作区\卡面成品4` 全量接入 / xlsx + 设计 dump 同步 / 重新统计（见 §16）。
> - **2026-10-11 → 10-16（批次 9~22）**：文本大改 + 卡面成品8 → 批次10 美术全量接入（power/遗物/药水图标 + 战斗模型管线 + 废案清理）→ 批次 11~19 文本/机制/颜色规范 → **批次 20~22 卡牌调整**（阿比舒、勇者加护、消消乐、曳光弹、破势、吃豆人、堕落、独特点子、专注、博览群游），逐条见 §21。
> - **2026-10-17 会话（批次24）**：`工作区\编辑区\人物\待机动画.aep` → 战斗待机帧序列（去绿幕/水印/去重/600×820），接入 `VisualCueSet`（见 §21.27）。
> - **2026-10-18 会话（批次25）**：`工作区\编辑区\人物\素材1.aep` → 攻击1/2/3、能力1/2、嘲讽1 六套帧序列 + 按卡牌类型分流（见 §21.28）。
> - **2026-10-20 会话（批次27）**：卡牌调整 + 游戏人生标签作用域修复 + 拆场兜底（见 §21.30）。
> - **2026-10-22 会话（批次29）**：跑酷删 power、六张数值卡、两个稀有度、专注重做（见 §21.32）。
> - **2026-10-22 会话（批次30）**：专注 1 费 + 卡面/power 文本合成一句、天马行空升级版补「+1」（见 §21.34）。
> - **2026-10-24 会话（批次35）**：剧本打击括号数跟升级（0/1）、重整旗鼓阈值 20%→25%（见 §21.40）。
> - **2026-10-25 会话（批次36）**：桃味气泡水变牌修复（`source: null` + 逐张变换）、选牌界面改「任意张」（见 §21.42）。
> - **2026-10-25 会话（批次39）**：九张卡数值/费用、自助指南附魔（GainsBlock）、? 事件全面体检（见 §21.46）。
> - **2026-10-25 会话（批次40）**：一批卡牌费用/数值/机制、新卡「传送门悖论」与「过载」、建筑师打斗演出（见 §21.47）。
> - **2026-10-25 会话（批次41）**：创作的痛苦删火力、多段攻击合成单条命令（活力只扣一次）、100连抽同修（见 §21.48）。
> - **2026-10-26 会话（批次42）**：发布完善（正式名 / 清单字段 / 版本 1.0.0 / 设置页四节 / 诊断 / 工坊预览图与发布清单）（见 §21.49）。
> - **2026-10-26 会话（批次43）**：设置页收尾（隐藏简介 / 去掉进度说明卡 / 日志目录跨平台）、换预览图、**打本地发布 zip**（见 §21.50）。
> - **2026-10-28 会话（批次44）**：22 项平衡调整、注能置底与直接结算（修开局卡顿）、图鉴全解锁、版本 1.0.1 发布包（见 §21.51）。
> - **2026-10-28 会话（批次45）**：注能回退成 AutoPlay、衍生牌图鉴问号修复、版本 1.0.2 发布包（见 §21.52）。
> - **2026-10-28 会话（批次46）**：黄金矿工读当前耗能、费用/数值批、仅局内括号、卡牌统计、版本 1.0.3（见 §21.53）。
> - **2026-10-22 会话（批次31）**：死亡动画 50 帧接入 `dead` 序列 + 24×24 小能量图标 `energy_text.png`；大能量图标 256×256 待做（见 §21.35）。
> - **2026-10-23 会话（批次32）**：中文名/血量/选人文案、左上角像素头像、256 大能量图标 + 静态表盘、桃红能量描边、4 张多人手势、休息处右半场镜像、文本/卡框参考（见 §21.36）。
> - **2026-10-23 会话（批次33）**：描述两行 + 他、能量图标上移/描边加深、海玻璃/色彩哲学家本地化、RitsuLib 设置页两个开关（见 §21.37）。
> - **2026-10-21 会话（批次28）**：死亡动画 AE 底稿（不部署）+ relaxed + 像素小桃 UI 头像 + 选人视频背景/音效接口；**2026-10-22 跟进** 把 relaxed 改到商店、休息处改用 `休息处.png`、重调死亡节奏（见 §21.31 / §21.33）。
> - **2026-10-18 会话（批次26）**：`工作区\编辑区\人物\受击动画.psd` → hit 序列（9 帧 / 1.0s / HitSpeed，见 §21.29）。
> - 本文档 = 会话压缩摘要 + 时间线逐条核对 + **项目文件实测**（路径/体积/mtime/**md5** 交叉验证）+ 本次接手的全部实验与结论。
> **本次状态（2026-11-04 批次52）**：**贴图大小默认 1.0（小桃本体固定 0.7）+ 出牌卡顿修复，版本 1.0.8**。
> 设置：`角色贴图大小` 默认 **1.0**、范围 **0.5~1.5**、步长 0.05；王小桃自己额外乘写死的 `MomoiDefaultScale = 0.7f`（设置界面仍显示 1.0）。滑块影响所有玩家角色是**刻意保留的特色**，怪物不受影响。
> 卡顿：定位到「战斗帧贴图首次解码」（我们按路径声明帧序列，换场景会清缓存）—— 新增 `MomoiCueWarmupPatch`（进战斗房间时逐帧 4 张、`CacheMode.Reuse` 预热全部 cue 帧）；另外卡框材质/UV 变体改成静态缓存（原来每次 `NCard.Reload` 都 `Duplicate()`）、`AudioStream` 加 `ConcurrentDictionary` 缓存、动画面板不再挂 `ModAnimStateMachine.SetTrigger`、热路径日志收口到新增的「输出详细日志」开关（`MomoiDiag`，默认关）。
> `dotnet build` **0 错误 / 31 警告**；DLL **520,704 B** / PCK **57,833,324 B**；工坊 Content 同步 1.0.8 后**已重新上传**（id 3830602273，内容 58,354,796 B，`Successfully uploaded`），标题改为 `王小桃 / Momoi —— 尖塔2角色mod`；`workspace.json` 现在只写 `description` / `tags` / `dependencies`，标题、可见性、更新说明交给工坊页面（详见 §21.59 第 3.1 节）。
>
> **上一轮（2026-11-02 批次51）**：**工坊「更新改动」落地** —— 更新说明移到 `workspace.json` / `workshop.json` 的 `changeNotes`（`[h2]1.0.1更新：[/h2]` + `[list]` 内 9 条 `[*]`），简介回退成 1394 字符原版；1.0.7 重新上传（条目 3830602273，`Found 1 dependencies.` / `Successfully uploaded`），工坊 Content 同步 1.0.7（见 §21.58）。
> **上一轮（2026-11-02 批次49）**：**体积砍半 + 多人构想 bug + 角色贴图大小开关 + 能力伤害改原版形状 + 循环叙事重做，版本 1.0.5**。
> 体积：pck **131,854,936 B → 57,834,244 B（-56%）**，发布 zip **131 MB → 54.2 MB**。Godot 默认导入全是**无损**（`compress/mode=0` 占 ctex 117.46 MB），所以卡面（1000×760）改 `process/size_limit=512` 保持无损、战斗帧改**有损 WebP 0.95**（帧偏扁平，VRAM 压缩反而更大）；可见像素 PSNR 42.4 dB。
> ⚠ 365 个 `*.import` 被 `.gitignore` 忽略：清缓存/换机器后**必须先跑 `工作区\_scripts\_optimize_textures.py` 再导 pck**，否则体积回到 131 MB（规则见 §21.56 第 1 节）。
> 多人：`DriedInspiration.AfterPlayerTurnStart` 少了 `if (player != Owner) return;` —— 队友回合开始也会被塞「构想」。
> 设置新增「**角色贴图大小**」滑块（0.2~1.2，默认 **0.7**，步长 0.05）：Prefix `NCreature.ScaleTo` 只对 `Entity.IsPlayer` 乘倍率，再在 `NCombatRoom.AddCreature` Postfix 补一次 `ScaleTo(1f, 0)`（传 1 而非倍率，否则平方）。怪物不受影响。
> 明日奈：减伤时长「本回合」→「**直到你的下回合开始前**」——`TickDownDuration` 从 `AfterSideTurnEnd` 挪到 `AfterSideTurnStart`。
> 能力伤害：构想之矛 / 矛与盾 / 节奏游戏 / 来自大师的援护 一律改成原版能力形状 `CreatureCmd.Damage(..., ValueProp.Unpowered, ...)`（同 Panache / FlameBarrier / Juggernaut）——**不吃力量/活力/虚弱/易伤，也不播攻击动画**；援护里手工补的活力/易伤与 `FirepowerHooks.SpendVigorAsync` 一并删掉。
> 数值：BA启动！普通→**罕见** + 活力 2-3→**3-4**；再启新篇 罕见→**普通**。
> 循环叙事重做：1 费技能（罕见·升级 0 费）+ **注能**（与开发者协同·绿 共用 `IImbuedCard` / `ImbuedSupport`，置底 + 开局自动打出）；打出后「本回合结束时，将弃牌堆的最多 1 张牌洗入你的抽牌堆」，选择界面 `STS2_MOMOI_CYCLIC_NARRATIVE_HEADER`「选择最多{Amount}张…」，`MinSelect=0` 保证只剩 1 张也由玩家确认、可跳过。
> `dotnet build` **0 错误 / 31 警告**，DLL **515,072 B** / PCK **57,834,244 B**；`工作区\发布包\STS2_Momoi_v1.0.5.zip` **54.2 MB**；三十五套自检 **1632 条全绿**。详见 §21.56。
> **上一轮（2026-10-31 批次48）**：**RitsuLib 前置依赖写对 + 工坊 required item + 简介前置链接**（版本仍 1.0.4）。
> 关键发现：清单里 `dependencies[].version` 是**无用字段**（原版 `Core/Modding/ModDependency.cs:10` 只认 `[JsonPropertyName("min_version")]`，未知字段被 System.Text.Json 静默忽略），所以过去的「版本对齐」从来没生效过。
> 已改 `min_version: 0.6.7` —— 把 `PackageReference` 临时钉到 0.6.7 **全工程编译 0 错误**（警告数与 0.6.10 一致）才敢写这个底线。
> csproj 目标 `SyncManifestDependencies`（会把该字段改写成编译时的包版本 → 每升一次 NuGet 就抬一次下限）换成 `ValidateManifestDependencies`：**只校验不改写**，缺键或下限高于编译包直接 Error。
> 工坊：`workspace.json` / `workshop.json` 的 `dependencies` = `[3747602295]`（数字、不加引号）→ 上传日志 `Added dependency on 3747602295`；简介加 `[h2]前置[/h2]` + `[url=...]RitsuLib[/url]（必需，最低 0.6.7）`，删掉裸文本「（需要RitsuLib）」。
> README 中英双份把「`dependencies[].version` 才是最低版本」的错误说明改正。
> `dotnet build` **0 错误**；三十四套自检 **1536 条断言全绿**。详见 §21.55。
> **上一轮（2026-10-31 批次47）**：飞溅 / 万花筒 / 棱彩宝石 三个「角色隔离」开关（`[ThreadStatic]` 作用域标记 + `UnlockState.get_CharacterCardPools` Postfix）+ 工坊发布素材与**首次上传成功**（条目 3830602273，`private`）；版本 1.0.4（见 §21.54）。
> **上一轮（2026-10-28 批次46）**：黄金矿工改读当前耗能、一批费用/数值/文本、卡牌统计 91+44=135、版本 1.0.3（见 §21.53）。
> **上一轮（2026-10-28 批次45）**：两处收尾，版本 **1.0.2**。
> ① **注能（开发者协同：绿）回退成正常的 `CardCmd.AutoPlay` 自动打出** —— 上一批为了绕开局卡 30 秒改成直接结算，
> 但那个 bug 目前无法稳定复现，先改回原版行为（保留「第 1 回合抽牌前置底」的修复、单次打出标记和日志兜底）。
> ② **衍生牌图鉴问号修好了**：`MomoiCompendiumUnlock` 之前只按 `STS2_MomoiCardPool` 过滤，而**小游戏牌 / 构想 / 支援 / 绷住链 / 传送门悖论其一其二都在 `TokenCardPool`**，
> 所以它们仍是问号 → 改成按 **id 前缀 `STS2_MOMOI_`** 遍历（卡牌 / 遗物 / 药水都改），图鉴里全部可见。
> `dotnet build` **0 错误**，DLL **507,904 B** / PCK **131,853,648 B**；三十一套自检 **1349 条断言全绿**。
> **发布包**：`工作区\发布包\STS2_Momoi_v1.0.2.zip`（125.0 MB，顶层 `STS2_Momoi/`）。详见 §21.52。
> **上一轮（2026-10-28 批次44）**：**平衡批 + 两个真 bug + 图鉴全解锁，版本 1.0.1**。
> 22 项数值/费用调整（过载 2 费·活力 2/3、修行 2 费、BA启动 2/3、整装待发 4/6、天马行空 4/4、博览群游 5/7、激战 2/2、翻滚射击 6/8、对策 4/5、我复活啦 2/3、捕鱼达人 8/8、旅行异蛙 6/6、相遇 6/7、时 火力 2/3、LOSE！2/3、节奏游戏 18/20·6/5·1 费、绷到我了 2 血/6-8、五万年 4/6、植物大战僵尸 1/1、传送门悖论 1 费、构想之盾升级不再给固有；矛与盾 11/15 上一批已到位）。
> **注能（开发者协同：绿）两处修复**：① 新增 `MomoiImbuedDrawPilePatch` —— 第 1 回合抽牌前把这张牌挪到抽牌堆**底部**（等价原版 `ShouldStartAtBottomOfDrawPile`），不再「开局抽到等于少抽一张」；② 开局自动打出改成**直接结算**（挂两个能力 + 离开战斗），不再走 `CardCmd.AutoPlay` 的完整出牌流程 —— 这是「抓两张时打沙漏开局卡 30 秒」最可能的原因（出牌队列/能力牌飞行动画/动画 cue 在 AutoPrePlay 阶段叠加），现在是同步结算 + 每张只算一次 + 异常兜底。
> **图鉴全解锁**：新增 `MomoiCompendiumUnlockPatch`（挂在 `SaveManager.InitProgressData` 之后）把本模组卡牌/遗物/药水批量 `Progress.MarkXxxAsSeen` 并落盘，图鉴不再问号；设置页「其他」里另加**手动「解锁全部图鉴」按钮**兜底。
> `dotnet build` **0 错误**，DLL **508,416 B** / PCK **131,853,648 B**；三十一套自检 **1347 条断言全绿**。
> **发布包**：`工作区\发布包\STS2_Momoi_v1.0.1.zip`（125.0 MB，顶层 `STS2_Momoi/`）。详见 §21.51。
> **上一轮（2026-10-26 批次43）**：**先出本地发布包**（不上工坊）。设置页按反馈收尾：**隐藏页面顶部的模组简介**（`WithDescriptionHidden(true)`，等正式简介写好再开）、
> **「进度」节删掉「不需要纪元/时间线」的说明卡**（该节现在只放「重置本模组设置」，标题改成「其他」）、
> **打开日志目录**确认是跨平台的（按 `OS.GetUserDataDir()` 的 `logs` 实时解析，不写死 `%APPDATA%`；目录不存在时退回 user 目录）。
> 预览图换成用户给的 `工作区\美术成品区\预览图.png`（512×512 / 253 KB）。
> 新增 `工作区\_scripts\_make_release_zip.py`：校验 `mods\STS2_Momoi\` 三个文件与清单字段后，打出**顶层就是 `STS2_Momoi/`** 的本地 mod 包
> → `工作区\发布包\STS2_Momoi_v1.0.0.zip`（125.0 MB，含 README.txt 安装说明）。
> `dotnet build` **0 错误**，DLL **504,320 B** / PCK **131,853,468 B**；三十套自检 **1291 条断言全绿**。详见 §21.50。
> **上一轮（2026-10-26 批次42）**：**发布完善**。模组正式中文名 **「游戏王小桃」**（清单 `name` / 设置页标题 / README；角色名仍是「王小桃」）；
> 清单从模板占位改成正式值（`author alkaid616`、中英双语 description、`version 1.0.0`、`min_game_version 0.111.0`，csproj 同步 `<Version>1.0.0</Version>`）；
> **设置页重排成四节**：`general`（色彩哲学家/海玻璃卡池开关）、`audio`（六档音量）、`progress`（「本模组不需要纪元/时间线」说明卡 + **重置本模组设置** 按钮）、`diagnostics`（**模组+游戏版本信息卡** + **打开日志目录**）。
> 免纪元已确认到位（`RequiresEpochAndTimeline => false`，全模组无 `RequireEpoch`）。按用户决定**本版不接遥测**、不加特效强度开关。
> 工坊配套：预览图 `工作区\美术成品区\工坊预览图_512.png`（512×512 / 139 KB），发布清单 `工作区\_docs\_发布清单.md`（tags / Required Items / 更新检查模板 / 上线自测项）。
> `dotnet build` **0 错误**，DLL **504,320 B** / PCK **131,853,468 B**；二十九套自检 **1265 条断言全绿**。详见 §21.49。
> **上一轮（2026-10-25 批次41）**：**多段攻击的活力/火力重复消耗修好了**。真因是把多段拆成了多条 `AttackCommand`：
> `VigorPower.BeforeAttack` 只给第一条命令记快照，`AfterAttack` 一次把层数扣光，后面几条命令只能吃残值。
> **创作的痛苦**：删去上一批加的「获得 2/3 层火力」；三段合成**一条命令**（`WithHitCount(3)` + `WithWaitBeforeHit(0.5f, 0.5f)`），
> 段间 0.5s 间隔与每段弹幕/命中特效都保持原样（故意**不**加 `OnlyPlayAnimOnce`，否则每段弹幕也只会播一次）。
> **100连抽！**：100 次伤害也是 100 条命令（同样的活力 bug + 每条命令都播一次攻击动画，卡顿）→ 合成 `WithHitCount(Repeat)` + `OnlyPlayAnimOnce()`。
> 顺手把全部模组卡扫了一遍：其余多段牌（来自妮露的援护 / 捕鱼达人 / 激战 / 街啪6 各分支）本来就是 `WithHitCount` 单命令 ✓。
> `dotnet build` **0 错误**，DLL **500,736 B** / PCK **131,853,468 B**；二十八套自检 **1222 条断言全绿**。详见 §21.48。
> **上一轮（2026-10-25 批次40）**：**一大批卡牌改动 + 两张新卡 + 建筑师打斗演出**。
> 消耗/费用：复盘与王不见王「升级前消耗、升级后删去」；循环叙事 0 费且升级给保留；日复一日 3/2 费且保留升级前后都有；发布委托 2/2 费；局势升温 2/2 费；黄金矿工 1/0 费；愤怒的小鸟 1/1 费。
> 数值：瓶颈突破构想 1/2、构想之矛 11/15、矛与盾伤害 11/15、整装待发 6/8 + 活力火力 2/3、局势升温 12/16、发布委托格挡 11/14、伏笔回收→罕见、100连抽→稀有。
> 机制：创作的痛苦新增「获得 2/3 层火力」；扫雷炸弹改成**洗入抽牌堆随机位置**（同原版守墓人）；再启新篇**只有手牌没构想时才加自己费用**；博览群游改**随机敌人**（同原版散射炮）。
> 新卡：**传送门悖论**（0c 技能，从两张衍生牌选一张入手；升级给升级版并删去消耗）+ **过载**（1c 能力，2/3 火力，火力减少时按能力层数获得活力）。
> **建筑师房对打演出**：RitsuLib 只从 `ancients.json` 生成对话，`StartAttackers/EndAttackers` 是 C# 字段 → 我们补了 `MomoiArchitectCutscenePatch` 在 `TheArchitect.LoadDialogue` 之后按拜访次数补上攻击者配置。
> `dotnet build` **0 错误**，DLL **501,760 B** / PCK **131,852,476 B**；二十七套自检 **1201 条断言全绿**。详见 §21.47。
> **上一轮（2026-10-25 批次39）**：**数值批 + 事件 bug 修复**。九张卡的数值/费用按用户点名调整（节奏游戏 18/24 且每方块 6/4、打灰机格挡 6/8 抽 1/2、消消乐 1/0 费且升级不再给保留、植物大战僵尸 1/0 费、花凛 32/40、晴 6/9、千寻 7/10、茜 12/15、大师 3/4+4/6、小玉 3/4）。
> **自助指南附魔 bug 找到真因**：原版 `Nimble`（灵巧）靠 `CardModel.GainsBlock` 筛目标，而 mod 里 **16 张会给格挡的卡都没 override 这个标志** → 灵巧只能选到「防御」。已全部补齐（顺带这些卡也自动获得原版「格挡」侧栏）。
> 另按「所有 ? 事件」逐条过了一遍：**色彩哲学家**的选项文案键是按 `EnergyColorName.ToUpperInvariant()` 拼的（`…options.STS2_MOMOI`），mod 的 `events.json` 里已有该键（本批补回被覆盖的「桃红色」标题）；补了角色 `bestiaryQuote`；并给 `EnergyIconHelper.GetPath` 加兜底（我们的池子在游戏图集里没有 `energy_sts2_momoi.tres`）。
> `dotnet build` **0 错误**，DLL **495,616 B** / PCK **130,899,152 B**；二十六套自检 **1139 条断言全绿**。详见 §21.46。
> **上一轮（2026-10-25 批次38）**：**选人 BGM + 对群弹幕 + 死亡事件收尾** —— 白天 `select_bg_1` 绑定 **Pixel Time**，夜间 `select_bg_2` 绑定 **Operation☆DOTABATA**，两首跟随模组「音乐音量」，切出选人界面时暂停；死亡语音默认 **500%**、最高 **700%**，由全局 `CreatureDiedEvent` 覆盖战斗死亡/事件死亡/主动放弃；创作痛苦/天马行空使用对群弹幕，创作痛苦第 1 段立即、2/3 段前各 0.5s。`dotnet build` **0 错误**，DLL **494,592 B** / PCK **130,898,644 B**（1059 条目，26 补丁）；25 个自检脚本 **1085 条全绿**。**尚未实机确认**选人 BGM/音乐音量、死亡音量/事件死亡/主动放弃、对群弹幕、地火、复活音与 100连抽性能。详见 **§21.45**、§21.43、§21.44。
> **上一轮（2026-10-25 批次36）**：**桃味气泡水变牌修好了** —— 白光后卡面迟迟不恢复的真因是 `FromHand` 的 `source` 传了药水模型：
> `NPlayerHand.AfterCardsSelected(source)` 在 `source != null` 时把「手牌 holder 归位」挂到 `source.ExecutionFinished` 上，
> 而药水模型永远不抛这个事件 → 选中的卡牌节点一直留在「已选卡牌容器」里，`CardCmd.Transform` 也就找不到手牌节点、变牌白光后不刷新。
> 现在改成 **`source: null`**（与消消乐同一修法）+ **逐张 `CardCmd.Transform(单张)`**（与「整活」/原版「护驾！！！」完全同一条路径）。
> 选牌界面也从「99 张」改成 **任意张**（`0 ~ 999999999` 的原版写法 + 自带文案「选择任意张牌来变化。」）。
> `dotnet build` **0 错误**，DLL **492,032 B** / PCK **128,360,432 B**；二十五套自检 **1062 条断言全绿**。详见 §21.42。
> **上一轮（2026-10-24 批次35）**：卡牌调整小批。**剧本打击**的括号数改为跟着升级走 —— 和「天马行空」的（额外攻击 0 次 / 1 次）一致，现在局内外都显示（**抽0张牌 / 抽1张牌**）；做法是把升级的 +1 从 `ConceptCards` 的 multiplier 挪到 `CardsBase`（`CalculatedVar` 局外 multiplier 记 0，原来局外一律显示「抽0张牌」），并去掉文本里的 `{InCombat:…}` 包装。**重整旗鼓**自动打出的血量阈值 **20% → 25%**（卡与 power 两处判定 + 中英文本 + 注释，升级前后都是 25%，其他效果没动）。
> ⚠ 又一次自检脚本覆盖：新建 `_verify_batch31.py` 与 10-22 动画批同名，已把本批脚本改名 `_verify_batch35.py`，并按 §21.35 重建 `_verify_batch31.py`（死亡 50 帧 / 能量图标 24·256 / 多人手臂 422×1200，24 条）。
> `dotnet build` **0 错误**，DLL **492,032 B** / PCK **128,360,432 B**；二十四套自检 **1020 条断言全绿**。详见 §21.40。
> **上一轮（2026-10-23 批次34）**：**选择文案/能量/事件开关收尾** —— 选择界面描述改为两行「游戏开发部的编剧，爱玩给木。
或许她真的能成为游戏王。」，代词改为**她**（修正笔误）；`flavor` 在当前原版选人界面**不显示**（只读 `.description`，见 §21.37）。大能量图标内容**上移 12px**；战斗左下角表盘再**左移 4px、上移 2px**；能量数字/卡池能量描边加深为桃红 **#D95C97**；**卡框**改为左粉右蓝浅渐变（三种类型外框全渐变、正文区深色+少量渐变）；**卡牌拖尾**改为外蓝内粉。新增 **海玻璃** `SEA_GLASS.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.title = 给木玻璃`；**色彩哲学家**新增 `STS2_MOMOI` 选项「**桃红色**」。新增 **残血动画低血量 `low_hp`**（去掉 3 组蹲起 + 左脸颊汗滴）和 **残血 BGM**（AudioStreamPlayer，播完仍残血续播、离开残血不打断、奖励界面/死亡 2 秒淡出、战斗结束停止；最终建筑师对话场景不播放；音量设置现为六档，含受击/死亡独立音量）。新增 **RitsuLib 设置页**（`settings.json`，Global）两个开关 + 音量栏：色彩哲学家卡池 / 海玻璃，配套 `MomoiPhilosopherPoolPatch`、`MomoiSeaGlassPoolPatch`。`dotnet build` 0 错误，DLL **492,032 B** / PCK **128,360,432 B**（1053 条目），**26 补丁**；本轮未启动游戏，运行时待验证。二十五个脚本 **1085** 条自检全绿（`_verify_batch28.py` 97 + `_verify_batch32.py` 117）。详见 §21.38 / §21.39 / §21.39.1。
> **上一轮（2026-10-23 批次32）**：**角色身份/视觉统一** —— 中文名正式 **王小桃**（英文仍 Momoi），初始生命 **72**，选择界面标题/描述/风味改为「游戏开发部的编剧，爱玩给木。」「或许她真的能成为游戏王。」；左上角头像改用 `STS2_Momoi_icon.tscn`（像素小桃）；**大能量图标** `energy_big.png` 换成用户 256×256 图，战斗能量表盘改为**单张静态**（不再 5 层旋转），能量数字描边/卡池能量描边改为桃红 **#F08CB8**；4 张多人手势 **422×1200** 接入；休息处 `Visuals` 移进 `ControlRoot`，右半场（2/4 号位）随原版 `FlipX` 水平镜像。新增文本参考 `工作区\_docs\_文本参考_王小桃.md` 与卡框参考 `工作区\_docs\_卡框参考.md`。`dotnet build` 0 错误，DLL **455,168 B** / PCK **120,090,016 B**；PCK 956 条目；18 补丁；二十二套 **939** 条自检全绿（`_verify_batch28.py` 97 + `_verify_batch32.py` 40）。
> **上一轮（2026-10-22 批次31）**：**死亡动画正式接入** —— 从 AEP 渲出 50 张透明帧（**1400×1250**，脚底/头顶与 idle 对齐），接入 `.Sequence("dead")` + `DeadSpeed`，2.0833s、末帧保持；AEP 本体仍不部署。**小能量图标已换** —— 用户给的 24×24 `momoi_energy_icon.png` 已作为 `energy_text.png`（小/文本能量图标）；大图标 `energy_big.png` 应为 **256×256**，等用户重做。`dotnet build` **0 错误**，DLL **454,656 B** / PCK **120,245,976 B**；PCK **962** 条目；18 补丁；二十一套自检 **899 条全绿**（`_verify_batch28.py` 92 条）。详见 §21.35。
> **上一轮（2026-10-22 批次30）**：**专注**最终定稿 —— 耗能**回到 1 费（升级 0 费）**；卡面与 power 文本都**并成一句**（照「蒙太奇」那种「A/B，X/Y」的写法，不再重复两遍「在你的回合结束时」）：
> `在你的回合结束时，若你本回合没有打出过小游戏牌/构想，使构想数值+1/选择最多构想数值张牌保留。`（power 侧的构想加值用 `{Amount}`、保留张数仍用 `{RetainCount}` 显示实际数值）。
> **天马行空**升级版卡面补上「+1」：`额外攻击等同构想数值{IfUpgraded:show:+1|}次`（升级前不带，实际效果本来就是升级 +1 次，未改代码）。
> `dotnet build` **0 错误**，DLL **454,656 B** / PCK **115,635,008 B**；二十一套自检 **889 条断言全绿**。详见 §21.34。
> **上一轮（2026-10-22 批次28b）**：按用户修改后的 `relaxed动画1&2.psd` 重导出两张 600×820；**relaxed 改到商店**（`STS2_Momoi_merchant.tscn`，scale **0.45**、position **(0,-182)**，脚底约 0，两张每 **1.1457856s** 交替）；**休息处改用 `休息处.png`**（`rest_site.png`，scale **0.65**、position **(10,42)**，不再用 relaxed/GDScript）；死亡 AE 重调为 **2.0833s**：抽动 **0.10–0.50s 连续无间隔**，灰化 **0.10–0.30s**（抽搐一半即完成），**0.50–1.00s 原地停半秒**，倒下 **1.00–1.58s**（-93° 过冲）。AEP 已重建（`工作区\编辑区\人物\死亡动画.aep`，不部署）。`dotnet build` **0 错误**，DLL **454,656 B** / PCK **115,635,600 B**；18 补丁；自检见 §21.33。
> **上一轮（2026-10-22 批次29）**：卡牌调整批。**跑酷！**去掉「回合开始时重复」，**两个 power（含基类）+ 死图标 + 本地化键一起删除**（现在是 0 费一次性「选最多一张特定牌」）；数值：**WIN！** 能量 3/4、**火焰附加** 灼烧 2/3、**热身** 火力 2/3、**构想之矛** 10/14、**博览群游** 7/9、**再起新篇** 活力 3/4；稀有度：**瓶颈突破→普通**、**玩玩新作！→罕见**；**专注小重做** —— 判定从「连续 2 回合」改成 **本回合**，0 费（升级前后都是 0），卡面与 power 文本按用户措辞重写。
> ⚠ 同批还修了自检脚本的一次覆盖事故：新建 `_verify_batch28.py` 时与本会话（10-21）同名文件冲突，把动画批的自检覆盖了；已把本批脚本改名为 `_verify_batch29.py`，并按 §21.27 / §21.31 与磁盘实测**重建** `_verify_batch24.py`（idle，26 条）与 `_verify_batch28.py`（死亡AE/relaxed/像素头像/选人背景；本批跟进已重写为 **82 条**）。当时发现 `工作区\编辑区\人物\死亡动画.aep` 本体不在磁盘（只剩日志目录与 `_work` 预览）；**2026-10-22 跟进已按新节奏重建 AEP，见 §21.33**。
> `dotnet build` **0 错误**，DLL **454,656 B** / PCK **115,402,920 B**；二十套自检 **831 条断言全绿**。详见 §21.32。
> **上一轮（2026-10-21 批次28）**：**角色表现层补齐** —— 死亡动画 AE 底稿（2.5833s，原地抽动 → 渐灰 → 绕脚底逆时针倒下；**只出 AEP，不进 mod**）；`relaxed` 两张底图按参考 AEP 的 **2.291571s/循环**（每张 **1.1457856s**）接入**休息点**（`STS2_Momoi_rest_site.tscn` + GDScript 交替）和战斗 `relaxed` cue；选人界面换成 `像素小桃.png` 的 5 张 UI 图；选人背景改成两段 `选人界面1&2.aep` 对应的 `.ogv` 视频（裁掉顶部水印）+ 模糊底图，背景/音效共用一个随机变体（音效接口留空，`SelectSfxVariants[2]`），进入选人界面重置；两个背景都加入预载。`dotnet build` **0 错误**，DLL **456,704 B** / PCK **115,427,764 B**；启动日志 **18/18 补丁成功**；`_verify_batch28.py` **102 条全绿**。
> **上一轮（2026-10-20 批次27）**：一次实操反馈批（角色动画期穿插的卡牌调整）。**游戏人生**跨局污染修好了 —— 真因是 `CardModel.CloneForCombat` **不重建 `_tags`**，战斗克隆体与牌组本尊共用同一个 `HashSet`，所以 `AddModCardTag` 写进去等于写进牌组、随存档跨局保留；改成按实例引用的「本场战斗临时游戏牌」表（`MinigameSupport.TemporaryGameCards`，战斗开始清空），并在开局清理旧版泄漏的标签；顺带给手牌选择加了拆场兜底（QuickRestart 时原版 `PlayerChoiceSynchronizer` 会抛 `ArgumentOutOfRangeException`，日志 20261020-152615）。数值/稀有度：**激战** 5→3 伤、费 1→0；**开发秘籍** → 稀有；**100连抽！** → 罕见 + **固有（升级前后都有）** + 升级改为费 4→3；**复盘** 攻击→**技能**、费 2→1、删掉伤害只留消耗堆回手。UI 文本：**连连看** 选牌文案 →「选择2张牌消耗」；**跑酷！**「选择一张」→「**选择最多一张**」（MinSelect=0 可以跳过，卡面+两个能力文本同步）；**节奏游戏！** power 右下角数字 → **将要造成的伤害**；**吃豆人** 没诅咒时给的 富足 → **WIN！**（升级 WIN！+），卡面+能力文本同步；**黄金矿工** 删掉已失效的死侧栏 `sidebar2`（不再给金币）。`dotnet build` **0 错误**，DLL **454,656 B** / PCK **109,989,948 B**；十七套自检 **732 条断言全绿**。详见 §21.30。
> **上一轮（2026-10-18 批次26）**：**受击动画完成** —— `受击动画.psd` 的 9 个全画布图层按 1→9 拆帧，去 alpha 边缘杂色、按待机头部比例缩放（PSD 人物比源视频约大 22%，scale 用 **1.0**），600×820、脚底 y=815；按原版铁甲战士 Spine `hurt` **1.0s** 按 `1→3→5→7→8→9→8→7` 回弹，前 7 个条目各 1 个 24fps 槽、最后的 7 占 17 槽，总 24 槽 = 1.0s；接入 `hit` 非循环序列（播完回 idle），新增 `HitSpeed` 倍率。`dotnet build` **0 错误**，DLL **453,120 B** / PCK **109,990,924 B**；十七套自检 **718 条断言全绿**（`_verify_batch26.py` 24 条）。详见 §21.29。
> **上一轮（2026-10-18 批次25）**：**攻击/能力/嘲讽动画全套接入** —— 解析 `素材1.aep` 的 6 个最终合成（攻击1 id266 / 攻击2 id535 / 攻击3 id564 / 嘲讽1 id593 / 能力1 id651 / 能力2 id476），AE 渲染 215 帧 → 去绿幕/水印/去重成 **105 张唯一帧**，沿用待机比例（源→画布 1.22047、身体中心 466、脚底 815）；攻击2/3 画布加宽到 716/644 给挥臂留空间。按卡牌分流：一般攻击→attack1、支援攻击→attack2、构想→attack3、稀有 Power→cast2、其他 Power→cast1（技能从批次26 起暂不播）、嘲讽/WIN！→taunt1；在 `Hook.BeforeCardPlayed` 主动播并压制重复触发器。每个动作有独立调速参数。`dotnet build` **0 错误**，DLL **452,608 B** / PCK **108,940,860 B**；十六套自检 **694 条断言全绿**（`_verify_batch25.py` 101 条）。详见 §21.28。
> **上一轮（2026-10-17 批次24）**：**人物待机动画接上了** —— 读 `工作区\编辑区\人物\待机动画.aep` 的 comp「待机」（932×720 / 24fps / 193 帧 = 3×46 帧循环 + 55 帧坐下-站起），AE 渲染 TIFF 后程序化**去绿幕 / 去溢色 / 去右上角 `SechiAnimation bilibili` 水印 / 按 4×·2× 慢放去重成 42 张唯一帧**，统一 **600×820**、脚底对齐、premultiplied Lanczos + alpha bleed；`VisualCueSet` 改成 `.Sequence("idle", …).Loop()`（68 个 Frame 条目，24fps，8.04s）。`dotnet build` **0 错误**，DLL **445,952 B** / PCK **84,743,552 B**；十五套自检 **593 条断言全绿**（`_verify_batch24.py` 44 条）。详见 §21.27。
> **上一轮（2026-10-16 批次23）**：文本收尾两处 —— **「击晕」补成金色关键词**（3 张：来自哈雷的援护、来自千寻的援护、破势；侧栏本来就有，是 `StunIntent.GetStaticHoverTip()`）；**「终于上一档了！」的金币补金色**（`{IfUpgraded:show:25|20}[gold]金币[/gold]`，两处），**金币不加侧栏**（补丁的关键词扫描表里本来就没有金币/Gold，与原版一致）。`dotnet build` **0 错误**，DLL **442,880 B** / PCK **75,402,280 B**；十四套自检 **549 条断言全绿**。详见 §21.26。
> **上一轮（2026-10-16 批次22）**：**卡面时代正式结束** —— 卡面 **133/133 全部真实成品**，power 47 / 遗物 / 药水图标全部成品；本文档已把所有「还要生图」的旧章节（ComfyUI 配方、火蛇怒咬/油腻打击/毁灭与新生专项、美术管线坑）**折叠成一段历史小结**（§5.2），后续重心改为 **角色美术 + 卡牌调整 + 新模组内容**（§6 / §22）。本批代码改动：**曳光弹升级后灼烧终于会变 4**（真因是 `IndependentCalculatedVar` 继承了 `DynamicVar.Clone()` 的浅拷贝 —— 克隆体里持有的还是规范化实例，而 `UpgradeValueBy` 升的是卡自己那份；改成按名字实时解析）、**破势重做**（2 费不变、16/20 伤害、`活力在这张牌上发挥 4/5 倍效果` 由新补丁 `VigorMultiplierPatch` 乘在 `VigorPower.ModifyDamageAdditive` 的返回值上）、**整活**卡面补「升级过的」、**吃豆人**的「没有诅咒」改为查抽牌堆+手牌+弃牌堆（并把抽/弃牌堆里的诅咒拉出来消耗）、**堕落**改罕见且同时给 1 层虚弱、**独特点子**改普通、**专注** 1→0 费、**博览群游** 0→1 费。`dotnet build` **0 错误**，DLL **442,880 B** / PCK **75,402,280 B**；十三套自检 **524 条断言全绿**。详见 §21.25。
> **上一轮（2026-10-15 批次21）**：**「系统：阿比舒」只有 2 段的真因** —— 上一批改用 `CreatureCmd.Damage` 之后，我把它当成能带「命中次数」的 `AttackCommand` 了；**`CreatureCmd.Damage` 每次只结算一次伤害**，所以「第 1 段打 2 次」写成一次 → 实战只有 2 段（日志 081556 印证）。已改成循环调两次，两段 AddHit 都记在同一个 `AttackContext` 里（钩子仍各跑一次）。**曳光弹**：基础伤害 7→6（升级 8）、基础灼烧 2→3（升级 4）、活力换灼烧由「每 2 点 1 层」改为「**每 1 点 1 层**」，文本同步。**费用**：来自时的援助 2→0，系统：阿比舒 0→1。`dotnet build` **0 错误**，DLL **441,856 B** / PCK **75,401,344 B**；十二套自检 **481 条断言全绿**。详见 §21.24。
> **上一轮（2026-10-15 批次20）**：**系统：阿比舒的最后一段「4 倍」改成真正的乘法修正**（`ModifyDamageMultiplicative` 门控 `_finalHit`）—— 这样力量/活力/同类型阿比舒的加伤一起被 ×4、易伤只乘一次、虚弱按原版各自乘一次；分两段用 `CreatureCmd.Damage`（**不能**用两次 `DamageCmd.Attack().Execute()`，那样 `BeforeAttack/AfterAttack` 会各跑一遍、活力被消耗两次），外套一个 `AttackContext` 让钩子只跑一次，最后一段单独加原版超能光束特效；基础伤害回到 1（升级 2）、Growth 回到 1（不再随升级变化），**卡面描述未动**。**来自勇者的加护**升级伤害 11 → 10。**消消乐首句**缩成「选择任意张类型相同的牌消耗。」。期间我用切片拼接改文件时忘了接回尾部，把 `RemainingSpecialCards.cs` 截成 289 行，已从 `工作区\_backup\batch15_pre` 完整恢复（diff 确认只差本次那一行）并补回被覆盖的两处改动，`_verify_batch20.py` 新增「文件恢复完整性」一节逐项断言。`dotnet build` **0 错误**，DLL **441,856 B** / PCK **75,401,344 B**；十一套自检 **464 条断言全绿**。详见 §21.23。
> **上一轮（2026-10-15 批次19）**：**纠正一个我一直搞错的前提** —— **卡面里的数字默认不上色，只有 power 的数字才用 `[blue]`**。逐表核对了原版 `localization/zhs`：`cards` 605 张描述里只有 **1 处** `[blue]`（整句高亮），而 `powers` 有 174 处、`relics` 277 处、`potions` 61 处。已把我在批次12/15/17/18 给卡面加的 `[blue]` 全部去掉（消消乐 / 来自花凛的援护 / 重整旗鼓 / 扫雷 / 吃豆人！ 共 20 条），去标记后与你给的原文完全一致；power / 遗物 / 药水的 `[blue]` 保留。`dotnet build` **0 错误**，DLL **438,784 B** / PCK **75,401,392 B**；十套自检 **436 条断言全绿**。详见 §21.22。
> **上一轮（2026-10-15 批次18）**：**更正上一轮归属** —— `target is { IsAlive: true } ? target : null` 改的是 **「来自妮露的援护」**（消耗全部火力、每层额外打一次），不是双刀王小桃；改动本身正确，与原卡设计一致。**消消乐重做**：删掉两个侧栏与整个类型分支，三消（≥3 张）统一改为 **打出并消耗**（能打出的先 AutoPlay；只对还在战斗牌堆里的牌补消耗 → 本来就带消耗的已进消耗堆、能力牌进 Limbo，两者都跳过；无法打出的直接消耗），超三张仍是每张抽 1 牌 + 1 能量；升级效果改为 **添加「保留」**（`AddKeyword`，降级时移除）；第二次选牌提示改为自定义的「选择任意牌」；文本按你给的原文（不手写自动追加的「小游戏牌。」「消耗。」）。`dotnet build` **0 错误**，DLL **438,784 B** / PCK **75,402,096 B**；九套自检 **423 条断言全绿**。详见 §21.21。
> **上一轮（2026-10-15 批次17）**：**消消乐「幽灵牌」真因找到** —— `NPlayerHand.SelectCards` 在 `AfterCardsSelected(source)` 里，**传了 `source` 就会把「把选中的卡从选牌容器搬回手牌」推到 `source.ExecutionFinished`（= 整段 OnPlay 结束）**；所以紧接着消耗时：不跳过动画→ `already has a parent`（日志 145708/153533），跳过动画（批次15 的『修复』）→ 节点留在选牌容器、收尾时又被搬回手牌 = **幽灵牌**。正解是两次 `FromHand` 的 `source` 都传 `null`（收尾当场完成）+ 恢复正常消耗动画。**系统：阿比舒**改用原版爪击/撕咬写法（加伤直接累加到 `Damage.BaseValue`），这样卡面 `{Damage:diff()}` 与打出的数值天然一致；并把「+2」的蓝色去掉；全模组扫查「卡面伤害 ≠ 实际伤害」结论是**只此一处**。按你的裁定：**心流改回可叠加**（两次 -4、3 费到 0，同原版火箭飞拳）、幸运儿的祝福**不加门控**、王道**不改**、机会难得选红色**只补文本**「这张牌在本回合可以免费打出。」、局势升温注释同步改名。**蒙太奇**新增 `AutoPlayProbe`：AutoPlay 被阻止时不发构想奖励。`dotnet build` **0 错误**，DLL **439,808 B** / PCK **75,403,056 B**；八套自检 **397 条断言全绿**。详见 §21.20。
> **上一轮（2026-10-14 批次16）**：**全模组代码审核**（5 个审核员并行逐文件通读 133 卡 + 54 power + 9 遗物 + 4 补丁，与原版反编译源码逐条核对契约）。**挖到两处必崩**：玩火+ / 熬夜+ 悬停即抛 —— `HoverTipFactory.FromCard(card, upgrade:true)` 会给不可升级的牌（`Burn`/`PoorSleep`，`MaxUpgradeLevel == 0`）调 `UpgradeInternal()`，那里直接 `throw InvalidOperationException`。另修：**俄罗斯方块**漏了「弃牌堆方块返回手牌」（批次13 重写时删掉的，而溢出方块恰恰就在弃牌堆）、**集结减费**漏算大多数支援牌（只按 tag 判，而大部分支援牌没 tag）且被减两次（批次15 改了现算 hook 但补丁里的旧写法没删）、**「雷酱」快照可能双倍易伤**（`PreviewValue` 是带目标的展示值）、双刀重复打出对死目标空放、心流/剑来的减费语义与文案不符、火焰附加硬编码层数、`ThrowingPlayerChoiceContext` 用错地方、`Cards` 变量该用 `CardsVar`、6 处空引用。完整报告 `工作区\_docs\_代码审核_批次16.md`，另有 **4 项留给你拍板**（机会难得选红色的隐藏免费、明日奈减伤是否挡 DoT、心流减费覆盖/叠加、自动打出被阻止是否还算触发）。`dotnet build` **0 错误**，DLL **439,296 B** / PCK **75,402,656 B**；七套自检 **369 条断言全绿**。详见 §21.19。
> **上一轮（2026-10-14 批次15）**：**又挖到两个真 bug 的根因**：①**卡面格挡数 ≠ 实际获得** —— `new DynamicVar("Block", N)` 的 `UpdateCardPreview` 是空实现、不跑 `Hook.ModifyBlock`，而 `GainBlock` 那侧用的是 `BlockVar(..., Move)`；**全模组扫描共 10 张卡中招**（含你点名的来自算术使的关爱、旅行异蛙），已全部改成「声明与使用统一用 BlockVar」；②**集结减费只生效一次** —— `EnergyCost.AddThisCombat` 是追加式相对修正，进手牌/打出各算一次且后续不再重算，改用读取时现算的 `TryModifyEnergyCostInCombat`。另：**消消乐第二次选牌后消耗报 `Can't add child 'Card' to 'CombatUi'`**（日志 145708/153533）—— 两段选牌后卡牌节点还挂在选牌 UI 下，飞行动画搬节点时撞上；消耗改成 `skipVisuals: true`；**贪吃蛇 power 标题查不到** —— 类上留了两个 `[RegisterPower]` 导致 RitsuLib 注册失败（与批次13 同一类失误，已新增全仓重复特性扫描）；**系统：阿比舒** 基础 2/升级 3 + 成长 +1/+2；**来自小玉的协助** 用 `IModPowerAssetOverrides` 补 power 图标；**注能放弃附魔** —— 效果直接写进卡牌类、删掉 `MomoiImbued` 与整个附魔图标目录，只保留词条与侧栏；循环叙事卡牌文本回滚。`dotnet build` **0 错误**，DLL **438,272 B** / PCK **75,402,656 B**；六套自检 **342 条断言全绿**。详见 §21.18。
> **上一轮（2026-10-14 批次14）**：**power 右下角语义全面对齐**（掉到二档了/游戏王形态/开发秘籍/扫雷/能量保留/额外回合/双刀王小桃/开发者协同·绿；「终于上一档了！」经查代码本来正确，是上一份文档写错了）；**扫雷**补 `DisplayAmount` 与新文本（数字蓝、炸弹金）；**满手牌结算**改为「升级版额外覆盖非升级版」（`RemoveSameTier → RemoveOverridden`）；**能量保留**改为可叠加（层数=剩余回合），并绕开「0 层自动移除」的坑 —— 回合末用 `SetAmount` 减 1、回合先拦一次重置再移除，否则 1 层时会在回合末被删掉、能量照样清空；**贪吃蛇/跑酷**拆成升级前/升级后两个 power（抽象基类 + Instanced，贪吃蛇用 `Track()` 只管自己放出去的那三张牌）；**「力量（本回合）」**删的是三个永远读不到的死本地化键（类必须留 —— 原版 `TemporaryStrengthPower` 是抽象类）；`_power总览.md` 生成器支持无特性的抽象基类继承解析。`dotnet build` **0 错误**，DLL **438,272 B** / PCK **75,385,260 B**；五套自检 **291 条断言全绿**。详见 §21.17。
> **上一轮（2026-10-14 批次13）**：**又挖到三个真 bug 的根因**：①「雷酱」吃活力 —— 火力拦截是挂在 `VigorPower.AfterAttack` 上的 Patch，只对走 `AttackCommand` 的消耗生效，而雷酱的攻击是 `.Unpowered()` + 手动扣活力，直接绕过了拦截（现已统一走 `FirepowerHooks.SpendVigorAsync`；全模组排查只此一处，所以矛与盾/节奏游戏都不会出问题）；②「我复活啦！」不进消耗牌堆 —— `AfterPreventingDeath` 时玩家 `CurrentHp==0` 而 `CardPileCmd.Add` 有 `creature.IsDead` 守卫会静默失败，现已改成**先回血再搬牌**；③构想卡面数值恒为 0 —— `NCard.UpdateText` 渲染前会 `DynamicVars.ClearPreview()` 把 PreviewValue 打回 BaseValue，必须像原版 `BlockVar` 那样在 `UpdateCardPreview` 里赋值（新增 `ConceptCountVar` / `ConceptEnergyVar`）。另：**俄罗斯方块**改为同档位覆盖 + 升级版优先结算 + 本回合打出的方块全消耗 + 文本显示抽几张/几能量；**花凛**加 `IsPrimaryEnemy` 挡同族小队爪牙（帝皇蟹两部位照常吃增伤）；**循环叙事**改为可叠加（层数=剩余回合）；**植物大战僵尸 power** 显示实际卡名；新增用户要求的 **`工作区\_docs\_power总览.md`**（52 个 power 的文本/叠加/右下角语义，脚本自动生成可重跑）。`dotnet build` **0 错误**，DLL **435,200 B** / PCK **75,382,252 B**；四层自检 **250 条断言全绿**。详见 §21.16。
> **上一轮（2026-10-14 批次12）**：**power 全面规范化** —— 全表文本数字改蓝/关键词改金（179 条，裸数字 0 条、标签全闭合）；**三个真 bug 挖到根**：①「我复活啦！」能挡两次致死 —— 牌组本体与局内副本是两个实例、各自记 `_used`，而 `RunState.IterateHookListeners` 两边都会问 `ShouldDieLate`，现已统一存在本体上；②注能附魔显示占位图 —— `EnchantmentModel.IconPath` 是 ID 拼路径、没有 AssetProfile 可覆写，已按 entry 补 `images/enchantments/momoi_imbued.png`；③打灰机！/来自大师的援助的卡面格挡不进 `Hook.ModifyBlock`（`DynamicVar`→`BlockVar` 修正）。**“雷酱”炮台支援重做**（独立实例/层数=剩余回合/从卡面快照/Unpowered 跳过程序化修正但自己补活力与易伤）；**花凛援护删 power** 改 Boss 增伤牌；**幸运儿的祝福可叠加**（层数=回合、百分比取高者）；**构想局内数值变绿**（`PreviewValue` vs `EnchantedValue`）；右下角计数语义修正（矛/盾/火焰附加/重整旗鼓）；重整旗鼓实时显示；记录型 power 隐藏。`dotnet build` **0 错误**，DLL **432,128 B** / PCK **75,381,676 B**；三层自检 **51+102+64 全绿**。详见 §21.15。
> **上一轮（2026-10-13 批次11）**：**遗物/药水描述全面染色 + 侧栏**（新增 `Tips/MomoiSidebarTips.cs`，遗物与药水拿不到卡牌那套自动关键词侧栏，必须手写）；**9 个遗物 flavor** 统一换成原版那句红色「这个遗物的细节将在未来揭晓……」；**没吃完的薯片新增商店房间触发**（参考原版餐券）；**全表诅咒红字**（含 16 个原版诅咒牌名与两侧栏，漏网 0 条）；**桃味气泡水贴图不显示的真因找到了 —— 类里根本没写 `AssetProfile`**（全量扫描 133+53+9+3 个注册类，只此一个），顺手把 3 个药水的轮廓图换成真白色剪影；捕鱼达人删掉多余的「对1名敌人」；**power 图标 47 张全量自测无占位图**。`dotnet build` **0 错误**，DLL **432,128 B** / PCK **75,376,152 B**；自检 `_verify_batch11.py` **102 条全绿**。详见 §21.14。
> **上一轮（2026-10-13 批次10）**：**四批成品图全量接入** —— `卡面修改1`(1) / `power图标成品`(48，含 4 张拆分 + 1 张改名) / `遗物成品区`(9) / `药水成品区`(3)；**改名**「活学活用 → 日复一日，必有精进」的 power title 补齐；**清理废弃 power**（27 张死图标 + 10 个孤儿词条，含死代码 `MomentumBreakPower`）；**美味饼干接入 `VanillaRelicVisualOverrides`**（它是原版遗物，本来就该走这个接口）；**修正 9 个遗物的轮廓图**（原来是彩色原图，改成纯白剪影）；**人物战斗模型不再用铁甲战士** —— 换成模组自己的 tscn + RitsuLib `VisualCueSet`（`images/characters/cue/{idle,attack,cast,hit,dead,relaxed}.png`，当前为线稿占位，覆盖同名文件即可）。另查明：**人物相关的所有 UI 素材（头像/选人图/地图标记/能量球/商店/篝火）至今仍是模板自带的铁甲战士占位图**，待补清单见 `工作区\_docs\_美术待补清单.md`。`dotnet build` **0 错误**，DLL **431,104 B** / PCK **75,368,540 B**。详见 §21.13。

---

## 0. 30 秒接手指南

### 0.1 这个项目现在是什么状态
> **代码侧**：**133 张卡** + 54 个 power + 9 遗物 + 3 药水，全部实现完毕并部署（DLL **494,592 B** / PCK **130,898,644 B**，2026-10-25，0 错误；**26 个补丁**）。
> **美术侧**：**卡面 / power / 遗物 / 药水 100% 完成**；**战斗动画 `idle` / `attack1/2/3` / `cast1/2` / `taunt1` / `hit` 全部换成真动画**（§21.27 / §21.28 / §21.29）；**`relaxed` 两张图已接商店交替**；**休息处改用 `休息处.png`**；**像素小桃 UI 头像 5 张 + 左上角头像场景**；**选人视频背景 2 套 + 白天/夜间选人 BGM**；**死亡动画 50 帧已接入**；**24×24 小 + 256×256 大能量图标 + 静态表盘**；**4 张多人手势**；**休息处右半场镜像**。**剩余视觉缺口** = 选人转场动画（BGM 已完成）；卡框和拖尾已改为粉蓝；技能牌动画仍待做（§6.1、§22）。
> **后续重心**：**实机验收 → 小幅手感修正 → 剩余美术（选人转场 / 技能牌动画）→ 新的模组内容**（§6、§22）。

### 0.2 接手后应该立刻做的事（优先级从上到下）
1. **角色美术（剩余缺口已缩小）**：战斗动画已完成（`idle` + `attack1/2/3` + `cast1/2` + `taunt1` + `hit`，§21.27 / §21.28 / §21.29）；`relaxed` **商店**交替、休息处 `休息处.png`、像素 UI 头像、**左上角头像**、选人视频背景、**死亡动画 50 帧**、**24×24 小 + 256×256 大能量图标 + 静态表盘**、**4 张多人手势**、**休息处右半场镜像**已完成（§21.31 / §21.33 / §21.35 / §21.36）；剩技能牌动画、**选人转场动画**（BGM 已完成；卡框和拖尾已完成）。逐项清单见 **`工作区\_docs\_美术待补清单.md`**。战斗差分只要**覆盖同名文件**即可，管线（`VisualCueSet`）已接好，不用改代码。
2. **卡牌调整**：一律等用户逐条点名；改完跑 `_verify_batch*.py`（32 套 / **1389** 条断言）+ `dotnet build`（§2、§10）。
3. **新模组内容（卡/遗物/药水/power）**：先改权威表 `工作区\STS2Momoi.xlsx`，再同步四处（§7.2）。
4. **别再看旧美术产出**：`工作区\美术准备\产出\`、`美术准备\脚本\`、ComfyUI 的 input/output 全是生图时代的遗留，接手不需要它们（§5.2）。
5. **已完成项不要重做**：卡面成品区 / 成品 4~8 / 批次 10 的三批图标均已进包。

### 0.3 30 秒上手命令
```bash
PY="C:\Users\asus\AppData\Local\Python\pythoncore-3.14-64\python.exe"   # 系统 python 会命中 Store 占位程序
cd "C:\Users\asus\RiderProjects\STS2 Momoi"
"$PY" 工作区/_scripts/_verify_batch24.py         # idle 资产自检（44 条）
"$PY" 工作区/_scripts/_verify_batch25.py         # 攻击/能力/嘲讽 + 分流自检（101 条）
"$PY" 工作区/_scripts/_verify_batch26.py         # 受击动画自检（24 条）
"$PY" 工作区/_scripts/_verify_batch28.py         # 死亡 AE / relaxed 商店 / 休息处新图 / 像素头像 / 选人背景
"$PY" 工作区/_scripts/_verify_batch27.py         # 批次27：游戏人生标签作用域 / 六张数值 / UI 文本（56 条）
"$PY" 工作区/_scripts/_verify_batch29.py         # 批次29：跑酷删 power / 七张数值 / 专注重做（35 条）
"$PY" 工作区/_scripts/_verify_batch30.py         # 批次30：专注 1 费 + 单句文本 / 天马行空升级 +1（21 条）
for f in 工作区/_scripts/_verify_batch*.py; do "$PY" "$f" || break; done   # 全量 26 套 / 1139 条
cd "STS2 Momoi" && dotnet build "STS2 Momoi.csproj"   # 构建（自动导出 PCK + 部署；游戏必须先关）
# 不想敲命令：直接双击仓库根目录的 构建并部署.bat（会先检查游戏是否在运行）
```

---

## 1. 项目概况

| 项 | 值 |
|---|---|
| 项目根 | `C:\Users\asus\RiderProjects\STS2 Momoi\` |
| C# 源码 | `STS2 Momoi\STS2 MomoiCode\`（.NET 9 / LangVersion 13，Godot.NET.Sdk 4.5.1） |
| 资源与本地化 | `STS2 Momoi\STS2_Momoi\`（PCK 资源目录，命名用下划线） |
| 解决方案 | `STS2 Momoi.sln`；工程文件 `STS2 Momoi\STS2 Momoi.csproj` |
| 游戏 | Slay the Spire 2 **v0.111.0**（Steam，`D:\SteamLibrary\steamapps\common\Slay the Spire 2\`，`sts2.dll` 2026-08-22 18:17） |
| RitsuLib | 依赖声明 `0.5.18`（`STS2_Momoi.json`）；`mods\STS2-RitsuLib\` 是本地版（2026-08-29 03:24） |
| 部署目录 | `D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi\` |
| **当前部署版本** | `STS2_Momoi.dll` **508,416 B** / `STS2_Momoi.pck` **131,855,024 B**（10-28 **1.0.3**） |
| 设计表格（权威） | `工作区\STS2Momoi.xlsx`（卡牌 / 遗物 / 药水 三 sheet）；快照 `_cards_full.json`、`_design_dump.txt` |
| 解包原版源码 | `C:\Users\asus\Desktop\Slay the Spire 2\src\`（含 sts2.xml） |
| API 研究笔记 | `research.md`（项目根，51 KB） |
| 教程站 | https://tutorials.sts2modding.com/docs/04-ritsulib/ |
| 技能 | `C:\Users\asus\.pi\agent\skills\sts2-ritsulib-character-mod\`、`…\image-gen\` |
| 美术处理 | **程序化**（`numpy` / `opencv` / `Pillow` 脚本，在 `工作区\_scripts\` 与 `工作区\编辑区\<卡名>\_src\`）；**生图时代的 ComfyUI 已弃用**（§5.2）；待机/攻击/能力/嘲讽/受击管线见 `工作区\编辑区\人物\_src\README.md` |
| 美术待补清单 | `工作区\_docs\_美术待补清单.md`（角色素材 42 个字段逐项） |
| 自检 | `工作区\_scripts\_verify_batch*.py`（32 套 / **1389** 条断言） |
| 机器 | Windows / RTX 4060 Laptop 8 GB / 32 GB RAM / 系统 python 3.14（`C:\Users\asus\AppData\Local\Python\pythoncore-3.14-64\python.exe`） |

---

## 2. 构建与部署

```bash
# 1) 游戏必须关闭（mods 目录 dll 被占用会构建失败）
cd "C:\Users\asus\RiderProjects\STS2 Momoi\STS2 Momoi"
dotnet build "STS2 Momoi.csproj"                          # 编译 + 复制到 mods + 导出 PCK
dotnet build "STS2 Momoi.csproj" -p:RunPckExport=false    # 只编 C#，不导出 PCK（快）

# 最省事：双击仓库根目录的 构建并部署.bat（自动检查游戏、构建、部署，并打印 DLL/PCK 时间）
```

- csproj 关键点：引用 `$(Sts2DataDir)\sts2.dll`（路径由 `local.props` 提供，模板 `local.props.template`）；`Krafs.Publicizer 2.2.1` 使**原版私有成员可访问**；`SyncManifestDependencies` 自动把 `STS2_Momoi.json` 的 RitsuLib 版本对齐 NuGet 包版本；`ExportPCK` 调用 `$(GodotExe) --headless --export-pack`。
- **游戏更新后必须重新编译**（否则运行时 `MissingMethodException`；08-22 踩过 `CardCmd.Exhaust` 改签名）。
- 控制台测试指令：`card {ID}` / `relic {ID}` / `power {ID}`；卡 ID 形如 `STS2_MOMOI_CARD_{类名 SNAKE_CASE 大写}`。
- 日志：`%APPDATA%\SlayTheSpire2\devmode-reports\devmode-report-<时间戳>\godot.log`。
- 根目录 `.godot\mono\temp\bin\Debug\STS2_Momoi.dll` 是中间产物，不是部署目标。
- 健康信号：构建 0 错误 + PCK 体积变化（最近一次 **71,522,456 B**，2026-10-11；DLL 427,520 B）。

---

## 3. 代码架构现状

### 3.1 Entry.cs（`STS2_MomoiCode\Entry.cs`）
- `ModId = "STS2_Momoi"`、`ResPath = "res://STS2_Momoi"`。
- 初始化：`RitsuLibFramework.EnsureGodotScriptsRegistered` + `ModTypeDiscoveryHub.RegisterModAssembly`（自动注册扫描；新增内容类只要 attribute 正确就不用改 Entry）。
- 注册 3 个 CardTag：`minigame`（可临时加入）、`fullgame`（可掉落、不可临时加入、吃小游戏增益）、`support`（支援牌）。
- `RunManager.Instance.RunStarted += _ => RunStats.Reset();`
- **补丁必须登记**（`RitsuLibFramework.CreatePatcher(ModId, "core-patches")`，当前 **16 个**，`PatchAll()` 失败直接抛异常）：
  `VigorRebindPatch`、`VigorConsumePatch`、`VigorMultiplierPatch`、`CombatStartResetPatch`、`MinigamePlayedPatch`、`FirepowerGainedPatch`、`PlayerTurnEndSnapshotPatch`、`DiscardTrackingPatch`、`TurnDiscardResetPatch`、`DustyTomeAfterObtainedPatch`、`MinigameCardSidebarPatch`、`GrindingCurseTrackPatch`、`CardKeywordLabelPatch`、`MomoiBeforeCardPlayedCuePatch`、`MomoiAfterCardPlayedCuePatch`、`MomoiStateMachineCueSuppressPatch`
  （**新增补丁忘了登记 = 静默不生效**，本项目经典坑。）

### 3.2 静态状态类
- `CombatStats`（战斗级，战斗开始重置）：`MinigamesPlayed`、`TotalFirepowerGained`、`ObtainedMinigames`、`LastPlayedMinigame`、`AbishuDamageBonus`、`SupportCardsPlayed`、`GrindingState.Reduction`；`Reset()` 同时调 `GrindingCursePool.Reset()`。
- `RunStats`（run 级，新局重置）：`VeritasPicked`、`CnCPicked`、`WhiteBlackChoice`。

### 3.3 四大机制
1. **构想（Concept）**：`ConceptCard`（Token 池），计数存 `ConceptCounterCapability`（卡实例 capability + 同步 DynamicVar）；遗物「枯竭灵感」回合开始：手牌无构想→最左生成（升级版 +2 计数）、有→计数 +1 并按计数塞诅咒（3 苦恼 / 4 睡眠不佳 / 5 疑虑 / 6+ 执迷）。**所有按构想数值生效的卡统一取手牌中构想最大值**（`ConceptCounterCapability.GetMaxCountInHand`）。显示用 `{ConceptCount:diff()}` + `{InCombat:…|…}`。
2. **小游戏（Minigame）**：`minigame` = 可临时加入；`fullgame` = 游戏牌（捕鱼达人 / 格斗游戏→街啪6 / 黄金矿工 / 抽鬼牌）。`MinigameSupport.AllMinigameCards` 12 种（连连看/消消乐/贪吃蛇/愤怒的小鸟/扫雷/绝地求生/跑酷/俄罗斯方块/打灰机/吃豆人/植物大战僵尸/节奏大师）。
3. **活力与火力**：活力 = 原版 `VigorPower`；火力 = 自建 `FirepowerPower`。攻击时若有火力 → 活力保留、火力 -1（`VigorConsumePatch`，仅 `command.Attacker == Owner`）。活力扣减不低于 0（`MinigameSupport.LoseVigor`）。
4. **灼烧（Burn）**：`BurnPower`（层数）+ `BurnTurnsPower`（剩余回合，双图标；层归零两图标都消失）。拥有者**自己回合开始**结算伤害 = 层数；持续 2 回合；**叠层时仅当剩余 ≤1 才重置为 2**；火蛇怒咬 `ApplyExtraTurn()` = max(2,当前)+1；有灼烧的敌人造成未格挡伤害时附加 1 层（`AfterAttack`，仅 Enemy 侧）。~~消亡用原版 `DemisePower`~~（唯一使用者天意侵蚀已于 2026-10-04 删除，**当前无卡使用消亡**）。
5. **「绷住」链（2026-10-04 新增）**：`SeriousFace` → `ItCrackedMe` → `HoldingItEasy` → `FiftyThousandYears`，逐级把下一张衍生牌加入手牌（来源牌升级则加入 + 版）；末张为虚无 + 下回合格挡（原版 `BlockNextTurnPower`，可叠加）。见 §16。
   - 图标背景：灼烧 / 灼烧·剩余回合已改红色（与中毒等负面状态一致）。

### 3.4 内容资产盘点（实测）
| 目录 | 数量 | 备注 |
|---|---|---|
| `images\cards\` | **133 PNG** | ✅ 与 133 个卡类一一对应，**133/133 真实成品**（2026-10-16 实测） |
| `images\powers\` | **47 PNG** | ✅ 全部成品（批次 10 替换 48 张：含 4 张拆分 + 1 张改名；死图标已清 27 张） |
| `images\relics\` | **20 PNG** | ✅ 9 个遗物的成品图 + 白剪影轮廓（`*_outline.png` 本来就是小白图，体积小属正常） |
| `images\potions\` | **6 PNG** | ✅ 3 个药水的成品图 + 轮廓 |
| `images\characters\` | 14 PNG | ✅ 5 张 UI 头像 + `rest_site.png` + `energy_text.png`（24×24）+ `energy_big.png`（256×256）+ 4 张多人手势 + 2 张选人模糊底图；无铁甲战士能量球占位（§5.1、§6.1） |
| `images\characters\cue\` | **208 PNG** | ✅ `idle` 42 + `attack1` 8 + `attack2` 24 + `attack3` 16 + `taunt1` 21 + `cast1` 24 + `cast2` 12 + `hit` 9 + `relaxed` 2 + `dead` 50 = **208 张真动画帧**；无旧占位 |
| `localization\zhs` | 8 个 json | cards 514 行 / powers 179 行 / relics 21 行 / potions 7 行 / characters / ancients / card_selection / enchantments |
| `localization\eng` | 同构 | 与 zhs 同步维护 |

遗物 9 个（`Relics\DriedInspiration.cs` + `Relics\MoreRelics.cs`）：枯竭灵感(Starter)、满溢灵感(Ancient)、没吃完的薯片(Common)、胜利的剧本(Uncommon)、收藏完好的旧游戏机(Uncommon)、绿色挂饰(Rare)、桌游「The·人生」(Rare)、G.Bible(Rare)、「镜子」(Shop)。
药水 3 个（`Potions\MomoiPotions.cs`）：速溶咖啡(Common)、草莓牛奶(Uncommon)、桃味气泡水(Rare)。

---

## 4. 卡牌现状（133 张）

- 卡类 133 个 ↔ `images\cards\` 133 张 PNG（**2026-10-08** 卡池数量未变，仅改名/换图后已对齐）。
- 稀有度池：可掉落 **20 普通 / 35 罕见 / 25 稀有**，另有初始牌、先古牌、先古绑定牌、Token 池（构想 + 小游戏 + 支援 + 多人卡 + 绷住链）。
- 2026-10-11 批（§20）：**游戏牌 / 小游戏牌 / 支援牌 三个卡牌关键词**（描述顶行金色文本，`Keywords\MomoiKeywords.cs` + `Patches\CardKeywordLabelPatch.cs`）；**删金色传说 `GoldenLegend` → 新增游戏人生 `GameLife`**（1c 攻击·罕见：9/12 伤害 + 给手牌加游戏牌标签，升级连所有同名牌）；**删趁热打铁 `DayAndNight`(+`DayAndNightPower`) → 新增暗黑心理学 `DarkPsychology`**（2c 技能·稀有：敌方力量被拦、改为构想+1，可叠加）；火焰附加 稀有→罕见；文本修正：局势升温「1张灼伤」、双线叙事「使构想数值+2」。两者备份在 `工作区\已删卡_备份\`。
- 2026-10-09 批（§19）：**见招拆招 → 对策 `Countermeasure`**（全量改名）；**轮回 `Reincarnation` + 能力 `ReincarnationDrainPower` 删除**（完整备份在 `工作区\已删卡_备份\轮回_Reincarnation\`，可重新启用）；**新增我复活啦！`ImBack`**（0c 稀有技能：3/5 活力 + 免死一次）；针锋相对 删保留（两版都无）、修行 保留（两版都有）；街啪6 侧栏3 改「3点能量及以上」；白与黑 文本补「在本场战斗中」。
- 已删除/改名的历史（易混）：火力解放→**王道**、新途→**埋下伏笔**、底气→**序章**、嘲讽（重做）、双刀王小桃（重做为稀有技能）、**天意侵蚀（2026-10-04 删除，普通牌位由严肃绷住顶替）**、**私人订制`Handpick` / 便携式掩体`FindCover`（2026-10-05 删除，分别由堕落 / 王不见王顶替）**、**游戏学习`GameStudy` → 开发秘籍`DevSecrets`（2026-10-05 全量改名，含能力 `DevSecretsPower`、图标 `dev_secrets_power.png`、本地化键）**。
- 新增（2026-10-04）：「绷住」链 4 张 —— 严肃绷住（普通，0c）→ 绷到我了（衍生，0c，严肃绷住衍生）→ 轻松绷住（衍生，0c）→ 我还能绷五万年呢（衍生，1c，虚无）；类名 `SeriousFace` / `ItCrackedMe` / `HoldingItEasy` / `FiftyThousandYears`（脚本 `_apply_batch4.py` 里有名称映射，别手敲）。
- 新增（2026-10-05）：堕落 `Depravity`（普通，0c：自身 1 层脆弱 + 随机小游戏牌入手）、王不见王 `KingsNeverMeet`（罕见，1c→**升级 0c**：1 层缓冲 + 接下来 1 回合无法从卡牌中获得格挡）——后者参考原版无色技能「应急按钮」`PanicButton` / `NoBlockPower`；两者均只依赖原版 power，无新自建能力。
- 命名批（09-04）：弹雨→天马行空、火焰子弹→曳光弹、活力打击→试探打击、对局复盘→复盘、火力打击→火力爆发、灼热打击→油腻打击、玩火→局势升温、混乱射击→激战、抛弃烦恼→茅塞顿开、阅历连击→博览群游、借力打力→还施彼身、精挑细选→私人订制、预热→热身、拾遗→玩玩新作！、对症下药→见招拆招、快找掩体！→便携式掩体、战胜心魔→祛魔、活学活用→日复一日，必有精进、夜以继日→趁热打铁。
- 卡面状态表：`工作区\美术准备\状态\_卡面状态.json`（127 条，9-21 版，**已滞后**：不含 09-20 以后新增/删除的卡；只用来查「类名 ↔ 中文名 ↔ 类别」，不要信 `state` 字段）。**2026-10-02 起，卡面完成度/类别以 `工作区\_data\_card_art_status.txt` / `.json`（逐卡实测，类别回退读 xlsx）为准。**

---

## 5. 美术现状（**卡面已 100% 完成**）

### 5.1 现状（实测 2026-10-22）

| 类别 | 文件数 | 状态 |
|---|---|---|
| 卡面 `images\cards\*.png` | 133 | ✅ **133/133 全部真实成品**（0 张共用占位、0 张纯色占位） |
| power 图标 `images\powers\*.png` | 47 | ✅ 全部成品（批次 10 接入 48 张：含 4 张拆分 + 1 张改名） |
| 遗物图标 `images\relics\*.png` | 20 | ✅ 成品 + 白剪影轮廓（`*_outline.png` 本来就是小白图，体积 <6 KB 属正常） |
| 药水图标 `images\potions\*.png` | 6 | ✅ 同上 |
| **角色素材 `images\characters\`** | 14 | ✅ 5 张 UI 头像 + `rest_site.png` + `energy_text.png`（24×24）+ `energy_big.png`（256×256）+ 4 张多人手势 + 2 张选人模糊底图；没有铁甲战士能量球占位（5 层已删） |
| 战斗视觉 `images\characters\cue\` | 208 | ✅ **208 张真动画帧**（idle 42 + attack1/2/3 48 + cast1/2 36 + taunt1 21 + hit 9 + relaxed 2 + dead 50）；无旧 `attack/cast` 占位 |
| 休息点 `rest_site.tscn` | 1 | ✅ **`休息处.png`（rest_site.png）** 静态躺姿，scale 0.65 / position (10,42)，不再用 relaxed |
| 商店 `merchant.tscn` | 2 帧 | ✅ **relaxed 两张交替**，scale 0.45 / position (0,-182)，脚底约 0 |
| 选人背景 | 2 场景 + 2 视频 + 2 BGM | ✅ 两段 `.ogv`（裁顶部水印）+ 模糊底图；白天 Pixel Time / 夜间 Operation☆DOTABATA（§21.45） |

逐项清单（尺寸 / 用途 / 现在长什么样）：**`工作区\_docs\_美术待补清单.md`**。

### 5.2 生图时代的历史小结（**已弃用，不必再看**）

卡面阶段用过 **ComfyUI**（`D:\ComfyUI-aki-v3.2\…`，API `127.0.0.1:8188`）+ 两阶段管线
（`_pipeline.wf_base` → `qa`，`er_sde`/`simple`，1536×1152 → 交付 1000×760，模型/LoRA 选型 + WD14 身份判定），
以及单卡精修（火蛇怒咬 masked redraw + 材质替换、油腻打击、毁灭与新生 长臂分层/alpha bleed）。

**这套东西已随卡面收官一并退役**：配方、专项调参、踩坑（原 §5.2 / §5.4 / §5.5 / §5.6 / §7.4）都不再维护。
保留结论只有三条：
1. 生图产物一律**不可直接当成品**，必须逐张读图对照要求（这条现在等价于「程序化产出也要逐张核对」）。
2. 白底抠图边缘发灰要用 **alpha bleed / color bleed**（RGB 渗出、alpha 不动）。
3. 需要刚性平移局部肢体时用**分层**做法（保护场归零 + 图层叠最上），别硬拉整图。

后来所有美术工作（成品 4~8、power/遗物/药水图标、白剪影轮廓、编辑区重绘）都改成 **程序化处理**
（`numpy` / `opencv` / `Pillow`），产物按批留在 `工作区\美术成品区\`（`卡面成品区` / `卡面修改1` / `药水成品区` / `遗物成品区`）
与 `工作区\编辑区\`（每个条目一个目录，内含 `_src` 脚本与 `_work` 中间产物）。

> 旧产出目录（`工作区\美术准备\产出\`、`美术准备\脚本\`、`美术准备\状态\`、`美术准备\日志\`、ComfyUI `input`/`output`）
> 仅作历史留存，接手时不必再看。

---

## 6. 后续工作清单（**重心 = 角色美术 + 卡牌调整 + 新模组内容**）

### 6.1 角色美术（当前最大缺口）
- [x] **像素小桃 UI 头像 5 张**：`icon` / `icon_outline` / `character_select` / `_locked` / `map_marker` 已替换（源 `像素小桃.png`）；预览 `_work/pixel_avatars_preview.png`，旧占位备份在 `_work/placeholder_avatar_backup/`。
- [x] **小能量图标**：`energy_text.png` = 用户 24×24 `momoi_energy_icon.png`。
- [x] **大能量图标 + 静态表盘**：`energy_big.png` = 用户 256×256 `momoi_energy_icon_big.png`；`STS2_Momoi_energy_counter.tscn` 改为单张静态，不再 5 层旋转。
- [x] **左上角头像**：`STS2_Momoi_icon.tscn` + `IconPath`，不再回退铁甲战士。
- [x] **4 张多人手势**：`STS2_Momoi_arm_{point,rock,paper,scissors}.png`，422×1200，已填 `Multiplayer`。
- [x] **休息处右半场镜像**：`Visuals` 移进 `ControlRoot`，2/4 号位随 `FlipX` 水平镜像。
- [x] **选人背景**：两段 `.ogv` + 模糊底图 + 两个 `.tscn`；白天/夜间 BGM 已绑定并跟随音乐音量（§21.45）。
- [x] **商店 relaxed**：`STS2_Momoi_merchant.tscn` 用 `relaxed.png` / `relaxed_2.png` 每张 **1.1457856s** 交替；`Visuals` scale **0.45**、position **(0,-182)**、脚底约 0；脚本 `momoi_merchant_visuals.gd`。
- [x] **休息处新图**：`休息处.png` → `images/characters/rest_site.png`，静态 Sprite2D，scale **0.65**、position **(10,42)**；hitbox `(-220,-160)-(220,245)`；不再用 relaxed。
- [x] **待机差分**：`idle.png` + `idle_01..41.png`（42 张，600×820，24fps / 8.04s 循环）已接入；自检 `_verify_batch24.py`。
- [x] **攻击/能力/嘲讽差分**：`attack1` 8 / `attack2` 24 / `attack3` 16 / `cast1` 24 / `cast2` 12 / `taunt1` 21；按卡牌类型/稀有度分流，自检 `_verify_batch25.py`。
- [x] **受击差分**：`hit.png` + `hit_01..08.png`（9 帧，600×820，总 1.0s，`HitSpeed` 可调），自检 `_verify_batch26.py`。
- [x] **relaxed 差分**：`relaxed.png` / `relaxed_2.png`（各 1.1457856s，循环 2.291571s；**商店交替** + 战斗 cue）；休息处改用 `rest_site.png`。
- [x] **死亡动画**：`死亡动画.aep` 2.0833s → 50 张 1400×1250 透明帧，接入 `.Sequence("dead")` + `DeadSpeed`；AEP 本体不部署（§21.35）。
- [ ] **技能牌动画**：普通技能/状态/诅咒当前保持 idle（`Choose()` 返回 null，等技能美术）；做好后再加 cue 分支。
      管线已接好（`VisualCues` + 自定义状态机 + `scenes\characters\STS2_Momoi_character.tscn`），
      **只覆盖同名文件即可，不用改代码**；说明见 `images\characters\cue\README.md` 与 `工作区\编辑区\人物\_src\README.md`。
- [x] **卡框**：`momoi_card_frame_gradient.gdshader` + material，左粉右蓝浅渐变；下方正文区压暗，保持文字对比。
- [x] **卡牌拖尾**：原版 `card_trail_ironclad.tscn` + `CharacterTrailStyle` 外蓝内粉。
- [ ] **选人转场**：`CharacterSelectTransitionPath` 仍回退原版。
- [x] 选人 BGM 已完成；仅剩选人转场动画/技能牌动画。

### 6.2 卡牌调整
- 入口 = **用户逐条点名**；不要自己开新战场、不要顺手美化（§7.1）。
- 每次改完：改本地化 → `dotnet build` → 跑 `_verify_batch*.py`（32 套 / **1389** 条断言）。
- 数值改动的**正确姿势**：卡面上出现的数字用 `BlockVar` / `DamageVar` / `CardsVar` / `IndependentCalculatedVar`；
  不要用普通 `DynamicVar`（会 `InvalidCastException`，且不随升级重算）。

### 6.3 新的模组内容
- 新卡 / 遗物 / 药水 / power：先改权威表 `工作区\STS2Momoi.xlsx`（+ `_sync_design_dump.py`），再同步本地化四处（§7.2）。
- 新机制优先走 `Patches\*.cs`；**每个补丁都要登记进 `Entry.cs`**，否则静默不生效（§7.3）。

### 6.4 代码侧遗留（低优先级 / 待玩家复测）
- 08-23 版列的待复测项，此后多轮重构已覆盖大部分，但**没有一条被明确标记「已复测通过」**。遇玩家反馈优先怀疑：
  秒人斧战斗结束移除时机（复制品）、绝地求生的能量公式（=max(0,3-手牌数)，用户未确认）、黄金矿工的「10X 金币」（现按 10/12 固定）、
  跑酷升级版「本场战斗免费」（现简化为本回合免费）、得道多助支援牌池 14 种（不含「来自优香的关爱」）、
  多人卡（义愤填膺 / 抽鬼牌 / 玩玩这款）**单机未测**。
- 09-21 的「19 项批」代码层核验通过 43/46，3 条为误报（破势自身 Stun、FeedingFrenzy 由吃豆人/PvZ 合法使用、构想遗留死代码已清理）。
- 批次 16 的全量代码审核结论见 `工作区\_docs\_代码审核_批次16.md`。

---

## 7. 注意事项与踩坑（**最值钱的部分**）

### 7.1 协作与流程（不遵守会被骂）
- **用户对卡牌文本措辞极其敏感**：没被要求就不要动任何文本/描述；"有问题在修改前提问"。
- **不做多余操作**：曾把"参考姿势图"整张当底图重画，被判越界 ✗ —— 只改用户点名的点，别顺手美化。
- **只做被点名的卡**：用户在 09-26 明确"先暂停、停掉所有工作、写文档"；此前也多次纠正"别自己开新战场"。
- **生成铁律**：先把要求固化成清单文件（放该卡产出目录，如 `要求清单.md`）→ 生成 → **逐张读图自查**逐条对照 → 不合格重跑，不要"差不多就交"。
- **一张卡一个文件夹**；每轮 10 张；现在生成 1536×1152、交付 1000×760。
- 用户给参考图时，**优先直接当 img2img 输入**。
- 用户会用"专业级 AI 的回答"直接指导实现（附魔表、斩杀逻辑、额外回合、`GetResultLocationForCardPlay` 等），照抄那些原版写法通常是对的。
- **报告要短**：用户多次遇到 `413 Failed to buffer the request body`（请求体超限），长回复+大量图片容易触发；进展用表格/短句。

### 7.2 文本与本地化
- 关键词（消耗/固有/保留/虚无/回合结束…）由 `CanonicalKeywords` 自动附加徽章，**描述里不要再手写**（指不要手写“消耗。”这行徽章文本；正文里提到这些词仍要 `[gold]词[/gold]` 染色，见上条 1）。
- 能量图标：`{Energy:energyIcons()}` 必须绑 `EnergyVar`；文字里不要再写数字（会变成 `00O`）。
- 数值不加 `[blue]`（交给游戏自动着色），关键词名用 `[gold]`；耗能增减统一写"减少/增加{能量图标}"。
- **侧栏（HoverTip）没有卡牌变量**，不能用卡牌 DynamicVar（街啪6 曾因此本地化报错）。
- 升级前后不同文本：`{IfUpgraded:show:…|…}`（可嵌套，已验证）。
- 动态数值：`CalculatedVar("X").WithMultiplier(...)` 必须配 `new CalculationBaseVar(Xm)` + `new CalculationExtraVar(Ym)`（用普通 DynamicVar 会 `InvalidCastException`）；战斗外 multiplier 返回 0；`{InCombat:局内|局外}` 控制显示。
- **关键词染色 + 提示文本（2026-10-04 立下的规矩）**：塔 2 与塔 1 不同——**提示文本是靠「描述里染色 `[gold]词[/gold]`」+ 模型上的 HoverTip 两者搭配**实现的（教程 04-04-card-properties 专节）。以后改卡先照这三条来：
  1. **原版术语**（格挡/手牌/抽牌堆/弃牌堆/消耗牌堆/牌组/力量/敏捷/易伤/虚弱/无实体/消耗/保留/虚无/升级/变化/斩杀…）→ 一律写 `[gold]术语[/gold]`；对照表直接看原版 `localization\zhs\cards.json`（如 `CLOAK_AND_DAGGER`、`DODGE_AND_ROLL`、`BEGONE`、`FEEL_NO_PAIN`）。
     * 模组 **已于 2026-10-04 全量补齐**（83 张卡 / zhs 286 处 / eng 287 处），详见 §16.6/§16.7；脚本 `脚本\_sweep_keywords_all.py`（幂等，可重跑）。
     * **英文侧按原版大写**：`Hand` / `Draw Pile` / `Discard Pile` / `Exhaust Pile` / `Block` / `Exhaust(ed)` / `Retain` / `Transform` / `Fatal` / `Deck` / `Upgrade(d)`；英文裸写在模组里一律不要。
     * **不染的**：牌类型词以外的普通名词（生命/能量/回合/伤害）；**攻击牌已按用户决定染金**（原版不染，但模组自己一直在染）。英文小写的动词 attack 不染（只染 `Attack` 卡牌类型）。
  2. **描述里点名另一张卡**（“将一张 XX 加入手牌”）→ 写成 `[gold]{IfUpgraded:show:XX+|XX}[/gold]`（**加号与升级分支都放在 gold 里面**），并在卡牌类里配 `AdditionalHoverTips => [HoverTipFactory.FromCard<XX>(IsUpgraded)]`；原版参照 `BEGONE`。
  3. **提示文本的自动化**：`Patches\MinigameSidebarPatch.cs` 已按描述原文扫描并自动追加侧栏（活力/火力/灼烧/无实体/易伤/缓冲/虚弱/力量/敏捷/格挡/**消耗**/**保留**/变化/斩杀/脆弱/能量/击晕）；其中「消耗/保留」只在卡本身**没有**该关键词时才加（`__instance.Keywords.Contains(...)` 去重，否则与自动徐章重复）。格挡/消耗/保留/变化这条链上**新增卡不用手写任何 HoverTip**。
  4. **侧栏的「标题 + 说明」两段式（2026-10-05 定的）**：小游戏牌/游戏牌这类侧栏要写成**两段**——标题（如「小游戏牌」）**不写 `[gold]`**（`scenes/ui/hover_tip.tscn` 的 %Title 是 **金色 Label**，不信 markup，写了会直接显示方括号）；说明用富文本（可用 `[gold]`）。
     构造：`new HoverTip(new LocString("cards", KEY + ".title"), new LocString("cards", KEY + ".description"))`，本地化里就写 `KEY.title` / `KEY.description` 两个键。
     三条集中挂在 `MinigameSidebarPatch`：小游戏牌（tag=minigame）→「小游戏牌 / 这张牌为小游戏牌。」；游戏牌（tag=fullgame）→「游戏牌 / 这张牌视为小游戏牌，但不会作为小游戏牌局内添加。」；描述里提到小游戏牌但两类都不是（打游戏！/拾遗/堕落…）→「小游戏牌 / 一种特殊的衍生牌。」。**逐卡再手写同一侧栏会因 Id 不同而重复显示，一律不要再手写。**
- 关键词徽章（消耗/固有/保留/虚无/回合结束…）仍由 `CanonicalKeywords` 自动附加，**描述里不要手写这些词**（与上一条的「文本里提到这些词」区分开）。
- **自带标签的牌要在描述顶行显示金色标签（2026-10-11）**：游戏牌 / 小游戏牌 / 支援牌 用**模组自定义关键词**实现（`Keywords\MomoiKeywords.cs`，注册时 `CardDescriptionPlacement = BeforeCardDescription` → RitsuLib 会把「金色标题 + 句号」插到描述最上方；句号取自 `card_keywords` 表的 `PERIOD`）。
  * 哪些牌带哪个关键词 = `Patches\CardKeywordLabelPatch.cs` 挂住 `CardModel.GetKeywordsWithSources` 按**标签/类型**现算（**不要**逐卡写 `CanonicalKeywords`：那个属性各卡自己 override，挂基类 getter 会被绕过，项目里额外提示文本那个补丁踩过同样的坑）。
  * 好处：局内给一张牌加标签（如「游戏人生」的 `AddModCardTag`）→ 标签一变，描述顶行会**立刻**出现「游戏牌。」。
  * 本地化在 `localization\{zhs,eng}\card_keywords.json`（**新文件**，含 `PERIOD`）。
- 改文本要**同步四处**：`localization\zhs`、`localization\eng`、`工作区\STS2Momoi.xlsx`、`_design_dump.txt`（后两者存**纯文本**，不含 `[gold]` 等 markup，纯染色改动无需动表）。

### 7.3 C# / RitsuLib 坑（cumulative）
- **所有补丁必须登记进 Entry.cs**，忘了 = 静默不生效。
- async 方法不能 Transpiler（逻辑在 MoveNext）；用 Prefix + `ref Task __result` 跳过原方法。
- 攻击命令必须 `FromCard(card, cardPlay)`（`TargetingRandomOpponents` / `TargetingAllOpponents` 少了会卡死）。
- 卡牌选择：`FromChooseACardScreen` **最多 3 张**（>3 抛异常），4+ 用 `FromSimpleGrid`。
- 战斗中 `RemoveFromDeck` 会报错 → 秒人斧改为战斗结束移除。
- 战斗中生成卡必须 `combatState.CreateCard(ModelDb.Card<T>(), player)`（`RunState.CreateCard` 不挂 CombatState 会卡死）。
- `PowerInstanceType.Instanced` 的 power **必须 override `InitInternalData`**，否则 `GetInternalData` 返回 null 卡死。
- `EnergyCost.AfterCardPlayedCleanup()` 会清掉 WhenPlayed 修正 → 跨回合用卡牌 `Played` 事件。
- 「本回合免费」用 `card.SetToFreeThisTurn()`；「本回合耗能-1」用 `card.EnergyCost.AddUntilPlayed(-1, reduceOnly: true)`。
- 最终伤害倍数用 `PowerModel.ModifyDamageMultiplicative`（限定 `cardSource is 本卡` 防误伤）；斩杀判定 `attack.Results.SelectMany(r=>r).Any(r => r.WasTargetKilled)`。
- 上回合回放：`CombatManager.Instance.History.Entries.OfType<CardPlayFinishedEntry>()` + `e._playerTurnNumbers[player.NetId]`（Publicizer）。
- 牌堆移动追踪：Patch `CardPileCmd.Add`（传送门悖论防递归用 capability 标记）。
- 心流的正解 = MakeItSo 式 `AfterCardPlayedLate` + `CombatManager.Instance.History.CardPlaysFinished`（不是 Patch 计数）。
- 本场战斗生成卡的追踪：`Hook.AfterCardGeneratedForCombat`（开荒诅咒池用）。

### 7.4 美术管线坑（**已随生图管线退役，仅留结论**）
- 生图/程序化产出一律**逐张读图对照要求**，不要「差不多就交」。
- 白底抠图边缘发灰 → **alpha bleed / color bleed**（RGB 渗出、alpha 不动）。
- 需要刚性平移局部肢体 → **分层**（保护场归零 + 图层叠最上），别硬拉整图。
- 其余（ComfyUI LoadImage 节点细节、denoise/调度器试错、mask 尺寸对齐等）全部作废，不再记录。

### 7.5 会话与工具坑
- **不要一次读入超大会话日志**（141 MB 那份正是 413 的成因）。要翻历史用 `工作区\_session_export\`（`extract.py`）与 `工作区\_session_export2\`（`extract2.py`）：`user_msgs.txt` / `assistant_text.txt` / `toolcalls.txt` / `compactions.txt` / `tail_detail.txt`。
- **历史卡面文本可以从会话日志找回**（相遇/贪吃蛇就是这么还原的）。
- **git 仓库没有任何提交**（`git status` 全是 "new file"）→ **不能把 git 当回滚来源**。
- 不要在上下文紧张时批量读图（一次 read = 数千 token）。
- **bash 坑**：`cd X && nohup python … &` 里的 `cd` 只在后台子壳生效，后续相对路径会失败 → **一律用绝对路径**；python 输出重定向到文件时是**块缓冲**（日志可能长时间为空，别误判卡死）；heredoc 写 Python 极易出语法错 → **用 write 工具整文件重写**。
- **2026-10-11 起：本机 `python` 会命中 WindowsApps 的 Store 占位程序**（`C:\Users\asus\AppData\Local\Microsoft\WindowsApps\python`，直接退出码 49、无输出）→ **用 `py -3`**，或全路径 `C:\Users\asus\AppData\Local\Python\pythoncore-3.14-64\python.exe`；**别用 `python - <<'PY'` 这种回退写法**（会掉进交互式 REPL 卡死）。
- ComfyUI 单张 1536×1152 / 32 步 ≈ **2.5~3 分钟**（RTX 4060 Laptop）；一轮 6 张 ≈ 18 分钟，脚本一定要能"跳过已完成"（`_run_v9x.py` 都带这个逻辑）。

---

## 8. 设计规范（用户要求，逐条遵守）
- 卡面描述 = 实际效果，**动态数值实时显示**；伤害显示要含活力/力量/易伤/药水（走 `Hook.ModifyDamage` 管道）。
- 用"抽"不用"摸"；能量写成图标；"升级过的"（不是"升级后"）。
- 初始牌 / 多人卡 / Token 牌不进奖励；可掉落 = 20 普通 / 35 罕见 / 25 稀有。
- 描述避免小作文；很多卡要配**侧栏**说明（构想诅咒表、灼烧、火力、活力、无实体、易伤/虚弱/力量/敏捷/格挡/能量…）。
- "使构想数值+1"类效果默认对**手牌中所有构想**生效。
- 表情要求：收敛活泼但不 OOC。
- 美术交付 1000×760 PNG；小游戏牌/游戏牌不做 AI 卡面。
- 遗物/药水代码与本地化已完成，**美术图标仍缺**。

---

## 9. 关键 API 速查

| 需求 | 写法 |
|---|---|
| 动态显示数值 | `CalculatedVar("X").WithMultiplier(λ)` + `new CalculationBaseVar/CalculationExtraVar` |
| 能量图标 | `{Energy:energyIcons()}`（需 EnergyVar） |
| 升级差异文本 | `{IfUpgraded:show:…\|…}`（可嵌套） |
| 生成卡（战斗中） | `combatState.CreateCard(ModelDb.Card<T>(), player)` |
| 复制卡 | `ModelDb.GetById<CardModel>(id).ToMutable()` |
| 附魔 | `CardCmd.Enchant<T>(card, 1)`；自定义附魔继承 `EnchantmentModel`；`IsCanonical` 跳过模板 |
| 局部移除卡 | 战斗内 `RemoveFromDeck` 报错 → 改用战斗结束钩子 |
| 牌堆动画 | `CardCmd.PreviewCardPileAdd(await CardPileCmd.AddGeneratedCardToCombat(...))` + `Cmd.Wait(0.5f)` |
| 抽到触发 | `AfterCardDrawn(choiceContext, card, fromHandDraw)` |
| 额外回合 | `PowerModel.ShouldTakeExtraTurn(Player)` |
| 结束回合 | `PlayerCmd.EndTurn(player, canBackOut: false)` |
| 眩晕 | `CreatureCmd.Stun(target)`；意图 `Monster.IntendsToAttack` |
| 随机化耗能 | `EnergyCost.SetThisTurnOrUntilPlayed(rng.NextInt(4))` + `NCard.FindOnTable(card)?.PlayRandomizeCostAnim()` |
| 战斗结束奖励 | `combatState.RunState.CurrentRoom is CombatRoom room` → `room.AddExtraReward(...)` |
| Run 级事件 | `RunManager.Instance.RunStarted += _ => …` |
| Instanced power | `PowerInstanceType.Instanced` + override `InitInternalData` |
| 上回合回放 | `History.Entries.OfType<CardPlayFinishedEntry>()` + `_playerTurnNumbers[NetId]` |

---

## 10. 测试与验证

### 10.1 自检套件（**改完必跑**）
```bash
PY="C:\Users\asus\AppData\Local\Python\pythoncore-3.14-64\python.exe"
cd "C:\Users\asus\RiderProjects\STS2 Momoi"
for f in 工作区/_scripts/_verify_batch*.py; do "$PY" "$f" | tail -1; done   # 全部 32 套 / 1389 条
```

| 套件 | 断言数 | 管什么 |
|---|---|---|
| `_verify_batch9.py` | 63 | 卡牌文本 / 代码特征（匹配前会剥掉 `[gold]` 等标签） |
| `_verify_batch11~19.py` | 102 / 52 / 32 / 37 / 50 / 27 / 28 / 26 / 13 | 遗物药水文本 → power 文本 → 机制 → 数值语义 → 颜色规范 |
| `_verify_batch20~23.py` | 28 / 17 / 43 / 25 | 阿比舒（4 倍倍率 + 3 段）、曳光弹与费用、批次 22 全项、金色关键词收尾 |
| `_verify_batch24.py` | 26 | idle 帧序列（42 帧 / 600×820 / 无损 / 接线） |
| `_verify_batch25~26.py` | 101 / 24 | 攻击/能力/嘲讽分流、hit 回弹序列 |
| `_verify_batch27.py` | 56 | 游戏人生标签作用域 + 六张数值卡 + 三处 UI 文本 |
| `_verify_batch28.py` | 97 | 死亡节奏 / relaxed 商店 / 休息处新图 / 像素头像 / 选人背景 / PCK |
| `_verify_batch29.py` | 36 | 跑酷删 power + 七张数值 + 两个稀有度 + 专注重做 |
| `_verify_batch30.py` | 21 | 专注 1 费 + 卡面/power 单句文本 + 天马行空升级版「+1」 |
| `_verify_batch31.py` | 24 | 死亡动画 50 帧 / 能量图标 24·256 / 多人手臂 422×1200 |
| `_verify_batch32.py` | 117 | 角色身份/头像/能量/多人手势/镜像 + 文本/特效参考 |
| `_verify_batch35.py` | 21 | 剧本打击括号数跟升级（0/1）+ 重整旗鼓阈值 25% |
| `_verify_batch36.py` | 19 | 桃味气泡水变牌（source:null + 逐张变换）+ 「任意张」选牌界面 |
| `_verify_batch37.py` | 55 | 九张卡数值/费用 + GainsBlock 全覆盖 + 事件/角色文本兜底 |
| `_verify_batch40.py` | 62 | 批次40 全部卡牌改动 + 传送门悖论 + 过载 + 建筑师打斗补丁 |
| `_verify_batch41.py` | 21 | 创作痛苦删火力 + 多段合成单命令 + 全卡多命令扫描 |
| `_verify_batch42.py` | 43 | 正式名/清单字段/版本/免纪元 + 设置页 + 诊断 + 预览图 |
| `_verify_batch43.py` | 26 | 设置页收尾（隐藏简介/去掉说明卡）+ 预览图 + 本地发布 zip 校验 |
| `_verify_batch44.py` | 58 | 22 项平衡 + 注能置底/AutoPlay + 图鉴全解锁（含衍生牌）+ 发布包版本 |
| `_verify_batch46.py` | **40** | **黄金矿工当前耗能 + 费用/数值批 + 仅局内括号 + 卡牌统计 + 1.0.3 包** |
| **合计** | **1389**（32 套） | 任一失败都要先查清是脚本过期还是代码回归，再继续 |

### 10.2 其它验证手段
- 游戏内控制台：`card STS2_MOMOI_CARD_XXX` 加卡、`power XXX` 加能力；卡 ID = 类名 SNAKE_CASE 大写。
- 日志：`%APPDATA%\SlayTheSpire2\devmode-reports\devmode-report-<时间戳>\godot.log`（先 grep `Exception|Error|STS2_Momoi`）。
  **实战数据可解包 `combat-stats.json` 核对** —— 批次 21 就是靠它查到「阿比舒只打 2 段」的（每次打出只 2 条 `DamageDealt`）。
- 每次改完：`dotnet build`（0 错误 + PCK 体积变化）→ 进游戏控制台验卡 → 让用户复测。
- 美术侧：程序化产出一律**逐张 read 对照**（批次 15 的格挡预览错配、批次 22 的 `IndependentCalculatedVar` 浅拷贝都是逐张核对发现的）。

---

## 11. 时间线

| 日期 | 轮次/内容 |
|---|---|
| 08-23 | 接手修复：审计 xlsx vs 代码 vs 本地化；第 1 轮（CalculatedVar `IntValue` 系统性修复、回合末钩子顺序、复制保留升级）；灼烧双图标机制重构 |
| 08-24~26 | 第 2 轮全攻击牌改 `CalculatedDamageVar` + `IndependentCalculatedVar`；第 3~7 轮；8.26 清单 38 项；遗物 8 个 + 药水 3 个；自动注册/补丁登记问题 |
| 08-27~31 | 文本规范化大扫除；草莓牛奶重做；游戏王形态重做；开始美术；"开工前最后一轮改动" |
| 09-04~09-28 | **生图时代（已结束）**：ComfyUI 环境搭建 → 模型/LoRA 选型与 WD14 身份判定 → 批量第 1/2/3 轮 → 已拼卡面 41 张接入 → 成品区 30 张接入；期间有**单卡精修**（火蛇怒咬 masked redraw + 材质替换、油腻打击 v3~v9、毁灭与新生 长臂分层 + alpha bleed）。细节（§5.2/§5.4/§5.5/§5.6/§7.4 旧文）已按用户要求**折叠删除**；产物留在 `工作区\美术准备\产出\`。 |
| 09-19~21 | 嘲讽/双刀王小桃/梗卡重做；心流重做；85 卡总览；A/B1/B2/C 未定稿清单 |
| 09-23 | 六项任务批 → xlsx 同步 → **构建部署（PCK 46,151,992，0 错误）**；美术准备目录整理 |
| 09-24~26 | 单卡精修收尾（火蛇怒咬旧批次**全部作废清空**）；文件夹规则改"一张卡一个文件夹" |
| **2026-10-02** | **卡面成品3 全量接入（§15）**：10 张成品（修行 / 剑来！/ 剧本打击 / 我的回合！/ 构想之盾 / 构想之矛 / 毁灭与新生 / 油腻打击 / 火焰附加 / 火蛇怒咬）覆盖 `images\cards\`，旧图备份 `备份\成品3替换备份\`；`dotnet build` **0 错误 0 警告**，PCK **46,151,992 → 48,970,264 B**（10 张全部 reimport）。同批实测重算卡面完成度：**真实成品 66 / 共用占位 52 / 纯色小占位 12**（§5.3、§6.2） |
| **2026-10-04** | **删天意侵蚀 + 新增「绷住」链 + 卡面成品4 接入（§16）**：删除 `DivineErosion`（代码/本地化/卡图；卡图备份 `备份\已删卡备份\`）；新增 `SeriousFace` / `ItCrackedMe` / `HoldingItEasy` / `FiftyThousandYears`（0c/0c/0c/1c 技能，末张虚无；下回合格挡用原版 `BlockNextTurnPower`、禁抽用原版 `NoDrawPower`）；`卡面成品4` 14 张全部接入；xlsx 第 9 行原地换成严肃绷住 + 追加 3 行衍生牌、`_design_dump.txt` 同步为 124 条；`dotnet build` **0 错误**，DLL 420,352→**424,960 B**、PCK 48,970,264→**54,772,636 B**。重算：**真实成品 80 / 共用占位 43 / 纯色小占位 10** |
| **2026-10-05** | **卡池改动（§17）**：删 `Handpick`（私人定制）/`FindCover`（便携式掩体）；新增 `Depravity`（堕落，普通 0c：自身 1 层脆弱 + 随机小游戏牌入手）与 `KingsNeverMeet`（王不见王，罕见 1c→升级 0c：1 层缓冲 + 1 回合无法从卡牌获得格挡，照抄原版 `PanicButton`/`NoBlockPower`）；`GameStudy`→`DevSecrets`（含能力/图标/本地化键/卡 ID 全量改名）；`卡面成品5` 19 张接入；xlsx/dump 同步；`dotnet build` **0 错误**，DLL 424,960 B、PCK 54,781,132 → **62,060,848 B**。重算：**真实成品 98 / 共用占位 29 / 纯色小占位 6**、待做 AI 卡面 18 张（§6.2） |
| **2026-10-08** | **数值调整 + 改名 + 卡面成品6（§18）**：火焰附加 2c→**1c**、天马行空伤害 4/6→**5/7**、独特点子 2c→**1c** 且伤害 6/8→**4/6**（仍 2 次）、打游戏！升级后 **0c**；`RhythmMaster`→**`RhythmGame`（节奏游戏！）**、`BorrowStrength`→**`TitForTat`（针锋相对）**（含能力/图标/本地化键/引用全量改名）；`卡面成品6` **26 张**接入（含全部 20 张小游戏牌/游戏牌）；xlsx/dump 同步；`dotnet build` **0 错误**，DLL 424,960 B、PCK 62,061,440 → **69,326,972 B**。重算：**真实成品 122 / 共用占位 10 / 纯色小占位 1**（剩 11 张普通牌） |
| **2026-10-09** | **保留/文本改 + 改名 + 删轮回 + 新增我复活啦！（§19）**：针锋相对 删「保留」（两版都无）、修行 加「保留」（两版都有）；街啪6 侧栏3 → 「消耗3点能量及以上」；**见招拆招 `RightRemedy` → 对策 `Countermeasure`**（全量改名）；白与黑 → 「选择后将在本场战斗中删去另一个选项。」；**删轮回 `Reincarnation` + `ReincarnationDrainPower`**（完整备份 `工作区\已删卡_备份\轮回_Reincarnation\`，可重新启用）；**新增我复活啦！ `ImBack`**（0c 稀有：3/5 活力 + 免死一次：消耗 + 从牌组移除 + 回复到 10% 最大生命 + 5/6 层再生）；`卡面成品7` 1 张接入；xlsx/dump 同步；`dotnet build` **0 错误**，DLL 424,960 → **423,424 B**、PCK 69,326,972 → **69,909,720 B**。重算：**真实成品 123 / 共用占位 9 / 纯色小占位 1**（剩 10 张） |

## 12. 变更历史补充（2026-09-05 那批）
- 开荒：加笨拙(Clumsy)预览；文本改 `{InCombat:实际张数|3}`。
- 熬夜：加睡眠不佳(PoorSleep)预览。
- LOSE！：加创作的痛苦(CreativePain)预览（升级版预览创作的痛苦+）。
- 街啪6 侧栏：还原为"消耗X点能量："文字（侧栏无卡牌变量环境）；卡面描述里的 1 费能量图标保留。
- （09-20 开荒再次重做：2/3 能量 + 4 诅咒池 `GrindingCursePool` 固定序 + `GrindingCurseTrackPatch` + 侧栏 4 诅咒预览。）

---

## 13. 资料索引

| 找什么 | 去哪 |
|---|---|
| 卡面接入与统计 | 接入脚本 `工作区\_scripts\_apply_batch10_art.py`、`_cleanup_dead.py`、`_batch10b~10d.py`；统计脚本 `工作区\_scripts\_regen_art_status.py`；备份 `工作区\_backup\batch1*_pre\`、`工作区\已删卡_备份\`（轮回 / 金色传说 / 趁热打铁 / 天意侵蚀，含源码/本地化/图/表格行）；报告 `工作区\_data\_card_art_status.txt` / `.json` |
| （已弃用）生图时代脚本 | `工作区\美术准备\脚本\`（ComfyUI 管线 / 提示词 / 单卡精修脚本）—— 仅作历史留存，接手不必再看（§5.2） |
| 卡牌关键词（金色顶行文本） | `STS2 MomoiCode\Keywords\MomoiKeywords.cs`（注册 GameCard / MinigameCard / SupportCard，BeforeCardDescription）+ `Patches\CardKeywordLabelPatch.cs`（挂 `CardModel.GetKeywordsWithSources`，按标签/类型自动补关键词，局内临时加的标签也会生效）；本地化新建 `localization\{zhs,eng}\card_keywords.json`（含 `PERIOD`） |
| xlsx 同步脚本 | `工作区\_scripts\_xlsx_update_beng.py`（10-04：天意侵蚀→严肃绷住 + 绷住链 3 张衍生牌）、**`工作区\_scripts\_update_batch5_tables.py`（10-05：私人定制→堕落 / 便携式掩体→王不见王 / 游戏学习→开发秘籍，xlsx + dump 一起改）**；卡池/文案脚本 **`脚本\_update_batch5_text.py`**；xlsx 备份 `工作区\_backup\_xlsx_backup\` |
| 关键词染色 | `脚本\_sweep_gold_block.py`（裸「格挡/Block」）、`脚本\_sweep_keywords_all.py`（**全量术语，zhs 驱动 eng，幂等**）、`脚本\_sweep_attack_and_strip_englines.py`（攻击牌 + 删 eng 重复徐章行）、盘点：`_list_bare_block.py` / `_keyword_inventory.py` / `_vanilla_gold_terms.py` / `_vanilla_term_ctx.py` / `_vanilla_cardtype_terms.py`；体检：`_check_loc_markup.py` / `_check_eng_keyword_lines.py`；改前备份 `工作区\_backup\_xlsx_backup\cards_{zhs,eng}_pre_{goldblock,kwall}.json` |
| 官方教程（改卡前先看） | <https://tutorials.sts2modding.com/docs/04-ritsulib/>（卡牌属性/关键词/提示文本：`04-04-card-properties`；加卡：`04-01-add-card`） |
| 原版写法参照 | 游戏自带 `localization\zhs|eng\cards.json`（`BEGONE` / `CLOAK_AND_DAGGER` / `DODGE_AND_ROLL`）；代码 `Desktop\Slay the Spire 2\src\Core\Models\Cards\` |
| **STS1 图标参考（2026-10-11 新增）** | `工作区\参考图集\STS1图标\`（内含 **README.md**：目录说明 + 42 张药水对照表）：`powers/` **279** 张（从 `desktop-1.0.jar` 的 `powers/powers.atlas` 切图，128/48 两种尺寸）、`relics/` **237** + `large_relics/` **122**、`potions/` **42** 张（复刻合成 —— 原版没独立图标，是运行时用图层拼的）、`potion_parts/` 全部原始图层；另有 4 张 `_总览_*.jpg` 可快速浏览。提取脚本见 `脚本\_extract_sts1_icons.py`、`_compose_sts1_potions.py`、`_probe_sts1_potions*.py`。STS1 装在 `D:\SteamLibrary\steamapps\common\SlayTheSpire\`（目录名**没有空格**，别写成 Slay the Spire）|
| 设计权威 | `工作区\STS2Momoi.xlsx`（+ `_cards_full.json` / `_design_dump.txt` / `_relic_potion_dump.txt`） |
| 原版卡 ID 对照 | 8-23 版旧文档 `工作区\STS2_Momoi_迁移文档.md` §8 |
| API 深挖 | `research.md`；`C:\Users\asus\Desktop\Slay the Spire 2\src\` |
| 会话原始记录 | `工作区\_session_export\`（`extract.py`）、`工作区\_session_export2\`（`extract2.py`） |
| 备份 | `工作区\美术准备\备份\{占位图备份,成品替换备份,成品替换备份2,成品2替换备份}` |

---

*文档结束。如需更新，请改写本文件而不是新建副本（避免多个迁移文档互相矛盾）。*

## 14. 生图时代痕迹的清理记录（**已折叠，仅留一句话结论**）

生图时代结束后，为「重新开始」做过一次彻底清理，事实如下（细节不必再看）：

- **2026-09-26**：按用户指令把某张单卡的生成历史与要求/自查文档在**文档层面**作废清空（本文档原 §5.4 旧内容、§11.1~§11.5 已删）。
- **同日追加**：按「A~G 全删，一点不留」**物理删除**该卡的全部生成痕迹——
  产出目录 1.1 GB / 1432 文件、ComfyUI `input\momoi_ref\` 68 个、ComfyUI `output\` 340 个、
  参考图库 54 MB、专用脚本 147 个 py、日志 73 个。
- **保留且不删的**：通用管线脚本（`工作区\美术准备\脚本\_pipeline.py` 等，现已弃用）、其余卡的一切产物、用户自己的工程文件（`.psd`）。
- **游戏侧从未有过残留**：该卡的 `images\cards\<类名>.png` 一直是当时的共用占位图，后来于 2026-10-02 被成品覆盖（§15）。

> **该卡的名称与图片在本文档里不再展开**；它现在只是一张普通的已完成卡面卡（成品见 `工作区\美术成品区\卡面成品区\`）。

---

## 15. 2026-10-02 卡面成品3 接入记录

**任务**：用户指令「阅读迁移文档 → 把 `工作区\卡面成品3` 中全部已完成卡面应用到模组中 → 统计未完成的卡面 → 更新迁移文档」。

**接入映射**（中文名 → 类名 → `images\cards\<类名>.png`）。映射来源 = `localization\zhs\cards.json` 的 `.title`，并与 `状态\_卡面状态.json`、`脚本\_预览2中文名映射.json` **三方交叉核对一致**：

| 成品文件 | 源文件（大小 / 模式） | 目标类名 | 被替换的旧图（已备份） |
|---|---|---|---|
| 修行.png | 784,347 B RGBA | AsceticTraining | 4,037 B 纯色占位 |
| 剑来！.png | 488,042 B RGBA | SwordCome | 349,797 B 共用占位 |
| 剧本打击.png | 749,175 B RGBA | ScriptStrike | 349,797 B 共用占位 |
| 我的回合！.png | 568,108 B RGBA | MyTurn | 491 B 纯色占位 |
| 构想之盾.png | 641,909 B RGBA | ConceptShield | 349,797 B 共用占位 |
| 构想之矛.png | 814,440 B RGBA | ConceptSpear | 349,797 B 共用占位 |
| 毁灭与新生.png | 437,517 B RGBA | DestructionAndRebirth | 349,797 B 共用占位 |
| 油腻打击.png | 1,018,669 B RGB | ScorchingStrike | 349,797 B 共用占位 |
| 火焰附加.png | 485,635 B RGBA | FlameAttach | 349,797 B 共用占位 |
| 火蛇怒咬.png | 641,689 B RGBA | FireSerpentBite | 349,797 B 共用占位 |

**做法**（沿用成品区/成品2 的旧约定；脚本 `工作区\美术准备\脚本\_apply_batch3.py`）：
1. 旧图先备份到 `工作区\美术准备\备份\成品3替换备份\`（10/10）；
2. 源 PNG **原字节直拷** 到 `images\cards\<类名>.png` —— 不改尺寸/模式（10 张全部已是 **1000×760**），接入后逐张 md5 与源一致（10/10）；
3. `.import` 文件不动 —— Godot 按 mtime 自动 reimport（导出日志确认 10 张全部 `reimport`）；
4. 确认游戏未运行 → `cd "STS2 Momoi" && dotnet build "STS2 Momoi.csproj"` → **0 错误 0 警告 / 9.5 s**，PCK **46,151,992 → 48,970,264 B**（+2,818,272 B）。

**验证**：对照图 `_batch3_contact_sheet.jpg`（10 张 5×2 缩略图）；部署目录 `mods\STS2_Momoi\` 三件套 = dll 420,352 B（09-23，代码未动）+ pck 48,970,264 B（10-02 23:20）+ json 409 B。

**同批产出的统计文件**（可直接当后续“还差哪些卡面”的唯一数据源）：
- `工作区\_data\_card_art_status.txt` —— 人读版：汇总 + 逐卡列表（共用占位 52 / 纯色小占位 12）；
- `工作区\_data\_card_art_status.json` —— 机读版：`rows[] = {cls, cn, size, kind, tag, edit}`（`edit` = 编辑区是否已有工作目录）。

---

## 16. 2026-10-04 删天意侵蚀 + 新增「绷住」链 + 卡面成品4 接入

**任务**：用户指令「删除普通牌天意侵蚀，增加普通牌严肃绷住」+ 「绷住」链 4 张卡的完整设计（含升级差异）+ 「我还能绷五万年呢的下回合格挡 power 参考闪躲翻滚（能叠加）、轻松绷住的本回合禁止抽牌 power 参考战斗专注」+ 「应用 `工作区\卡面成品4\` 的全部卡面，同步文档、表格，并继续统计未完成的卡面」。

### 16.1 「绷住」链设计（实际实现）

| 卡 | 类名 | 类型 / 稀有度 | 耗费 | 效果 | 升级 |
|---|---|---|---|---|---|
| 严肃绷住 | `SeriousFace` | 技能 / **普通** | 0 | 获得 4 点格挡；将 1 张「绷到我了」加入手牌 | 6 点格挡；改加入「绷到我了+」 |
| 绷到我了 | `ItCrackedMe` | 技能 / 衍生 | 0 | 失去 1 点生命；获得 5 点格挡；将 1 张「轻松绷住」加入手牌 | 7 点格挡；改加入「轻松绷住+」 |
| 轻松绷住 | `HoldingItEasy` | 技能 / 衍生 | 0 | 获得 2 点格挡；抽 1 张牌；本回合内不能再抽牌；将 1 张「我还能绷五万年呢」加入手牌 | 3 点格挡；改加入「我还能绷五万年呢+」 |
| 我还能绷五万年呢 | `FiftyThousandYears` | 技能 / 衍生 / **虚无** | 1 | 获得 5 点格挡；在下个回合获得 5 点格挡；结束你的回合 | 7 / 7 |

- 代码：`STS2 Momoi\STS2_MomoiCode\Cards\HoldItInCards.cs`（含 `HoldItInChain.AddNext<T>()`：`combatState.CreateCard` → 来源牌升级则 `CardCmd.Upgrade` → `CardPileCmd.AddGeneratedCardToCombat(…, PileType.Hand, …)`）。
- **照抄原版的部分**（踩坑时先看这张表）：

| 需求 | 原版参考 | 用到的东西 |
|---|---|---|
| 失去 1 点生命 | 放血 `Bloodletting` | `HpLossVar` + `CreatureCmd.Damage(…, ValueProp.Unblockable \| Unpowered \| Move, …)` |
| 本回合不能再抽牌 | 战斗专注 `BattleTrance` | 先 `CardPileCmd.Draw` 再 `PowerCmd.Apply<NoDrawPower>`（**顺序不能反**，否则自己那张也会被禁） |
| 下个回合获得格挡 | 闪躲翻滚 `DodgeAndRoll` |  `CreatureCmd.GainBlock` 的**返回值** → `PowerCmd.Apply<BlockNextTurnPower>`（`StackType.Counter` ⇒ 可叠加） |
| 虚无 | — | `CanonicalKeywords = { CardKeyword.Ethereal }` |
| 结束你的回合 | 预借时间 | `PlayerCmd.EndTurn(Owner, canBackOut: false)` |

- 4 张卡都带 `GainsBlock => true`（与原版格挡卡一致，自动附格挡侧栏），并给下一张衍生牌加了 `AdditionalHoverTips`（`HoverTipFactory.FromCard<T>(IsUpgraded)`，升级时预览 + 版）。
- 本地化：`localization\zhs\cards.json` + `eng\cards.json` 各 **134 张 / 525 键**；描述用「绷到我了{IfUpgraded:show:+|}」把升级差异写进同一模板。

### 16.2 天意侵蚀删除清单

| 位置 | 处理 |
|---|---|
| `Cards\ConceptFlowCards.cs` | 删除 `DivineErosion` 类（全库唯一引用处） |
| `localization\{zhs,eng}\cards.json` | 删除 4 个键（title / description / smartDescription / flavor） |
| `images\cards\DivineErosion.png` + `.import` | 删除；PNG 备份到 `备份\已删卡备份\` |
| `.godot\imported\DivineErosion.png-*.ctex/.md5` | 删除（避免残留进 PCK；导出日志已确认 **0 残留**） |
| xlsx / `_design_dump.txt` | 第 9 行原地改为「严肃绷住」/ 条目 `[6]` 改写 |

> ⚠ 历史快照 `工作区\_cards_full.json`、`_idx_cards.json`、`_xlsx_dump.json`、`美术准备\状态\*.json`、`v2预览索引.txt`、`migrate_cards.py` 里**仍有「天意侵蚀」**——它们是按日期归档的旧快照，**不要当现行数据源**。

### 16.3 卡面成品4 接入（14 张）

| 成品文件 | 目标类名 | 原图 |
|---|---|---|
| 严肃绷住.png | `SeriousFace` | 新建（新卡）|
| 绷到我了.png | `ItCrackedMe` | 新建（新卡）|
| 轻松绷住.png | `HoldingItEasy` | 新建（新卡）|
| 我还能绷五万年呢.png | `FiftyThousandYears` | 新建（新卡）|
| 义愤填膺.png | `RighteousIndignation` | 349,797 B 共用占位 |
| 传送门悖论其一.png | `PortalParadoxOne` | 349,797 B 共用占位 |
| 传送门悖论其二.png | `PortalParadoxTwo` | 349,797 B 共用占位 |
| 发布委托.png | `PostQuest` | 349,797 B 共用占位 |
| 天马行空.png | `BulletRain` | 349,797 B 共用占位 |
| 游戏王形态.png | `GameKingForm` | 349,797 B 共用占位 |
| 熬夜.png | `StayUpLate` | 349,797 B 共用占位 |
| 王道.png | `KinglyWay` | 4,038 B 纯色占位 |
| 矛与盾.png | `SpearShield` | 489 B 纯色占位 |
| 试探打击.png | `VigorStrike` | 349,797 B 共用占位 |

- 全部 **1000×760**，原字节直拷（md5 **14/14** 一致），旧图备份 `备份\成品4替换备份\`；脚本 `脚本\_apply_batch4.py`（`--dry` 可空跑）。
- 对照图 `_batch4_contact_sheet.jpg`（14 张，图内文字与卡名一一对应，已人工核对）；导出日志确认 14 张全部 `reimport`。
- 构建：`dotnet build` **0 错误**（40 个历史警告，无新增）；DLL 420,352 → **424,960 B**、PCK 48,970,264 → **54,772,636 B**。

### 16.4 表格 / 文档同步结果

- `工作区\STS2Momoi.xlsx` 卡牌表：第 9 行原地换成「严肃绷住」（保留行样式），末尾追加 3 行衍生牌（第 134/135/136 行）→ 共 **133 张**、普通牌回到 **20**。备份 `工作区\_backup\_xlsx_backup\STS2Momoi_2026-10-04_0209_pre_beng.xlsx`；脚本 `工作区\_scripts\_xlsx_update_beng.py`。
- `工作区\_design_dump.txt`：条目 `[6]` 改写为严肃绷住，追加 `[121]`~`[123]` → 共 **124** 条。
- 卡面统计：`工作区\_data\_card_art_status.txt` / `.json` 重新生成（统计脚本已改为**类别回退读 xlsx**，能覆盖新卡）；结果 **真实成品 80 / 共用占位 43 / 纯色小占位 10**，待做 AI 卡面 **36 张**，小游戏牌·游戏牌 17 张不做（§6.2）。

### 16.5 未能自动验证的部分（交给用户复测）

- 只有 C# 编译期验证 + 资源打包验证，**没有跑过游戏**：4 张新卡的实际手感需进游戏用控制台测（`card STS2_MOMOI_CARD_SERIOUS_FACE` / `…_IT_CRACKED_ME` / `…_HOLDING_IT_EASY` / `…_FIFTY_THOUSAND_YEARS`）。
- 重点看三条：① `BlockNextTurnPower` 的**下回合格挡在结束回合后是否如期触发、多次打出是否叠加**；② `NoDrawPower` 是否**只禁后续抽牌**（本次抽的那张正常）；③ 升级链是否逐级给 + 版。
- **旧存档提醒**：卡牌已删但存档里可能还写着 `STS2_MOMOI_CARD_DIVINE_EROSION`（mod 里**没有任何存档迁移/清理机制**）。若遇旧存档报错/卡卫图标异常，建议**开新档**复测；假如后续还要删卡，应同步考虑加一个“清理未知卡 ID”的钩子。

### 16.6 关键词染色修正（用户验收后追加，2026-10-04）

**用户反馈**：「严肃绷住描述里的绷到我了（以及轻松绷住 / 我还能绷五万年呢）应该是关键字类型，而不是白色文字；格挡也应该是关键字」。

**先查依据（以后改卡都先走这一步）**：
- 教程 <https://tutorials.sts2modding.com/docs/04-ritsulib/04-04-card-properties/> → 专节「添加卡牌提示文本」：**塔 2 的提示文本 = 描述里 `[gold]词[/gold]` 染色 + 模型上的 HoverTip，两者搭配**（与塔 1 不同）。
- 原版卡参照：`BEGONE`（zhs `[gold]{IfUpgraded:show:仆从打击+|仆从打击}[/gold]` + `HoverTipFactory.FromCard<MinionStrike>(base.IsUpgraded)`）、`CLOAK_AND_DAGGER`（`点[gold]格挡[/gold]` + `张[gold]小刀[/gold]` + `你的[gold]手牌[/gold]`，代码只给 `GainsBlock` + `FromCard<Shiv>`）、`DODGE_AND_ROLL`（两行都用 `[gold]格挡[/gold]`）。
- 原版词表：逐个词数过——zhs 里 `[gold]格挡[/gold]` 106 次 vs 裸格挡 2 次；`手牌` 109 次；`小刀/灵魂/碎屑` 等卡名全部染成 gold。

**本轮改动**：

| 项 | 内容 |
|---|---|
| 4 张新卡 | 格挡 → `[gold]格挡[/gold]`；点名卡 → `[gold]{IfUpgraded:show:XX+|XX}[/gold]`；手牌 → `[gold]手牌[/gold]`；eng 对应 `[gold]Block[/gold]` / `[gold]hand[/gold]`。提示文本早已到位（格挡走 `GainsBlock` + 补丁，卡名走 `AdditionalHoverTips`），**未改一行 C#**。 |
| 全模组格挡（用户选 B 案） | zhs **19 张卡 / 37 处**裸「格挡」→ `[gold]格挡[/gold]`；eng 同步 **37 处** `Block` → `[gold]Block[/gold]`；纯 markup、零措辞改动；脚本 `脚本\_sweep_gold_block.py`（含 `--dry`），改前备份 `工作区\_backup\_xlsx_backup\cards_{zhs,eng}_pre_goldblock.json`。 |
| 表格/dump | **未动**（xlsx / `_design_dump.txt` 存纯文本，本来就不带 markup） |

**两个特意避开的坑**：
- **不能无脑正则替换**：`{Block:diff()}` 里的 `Block`、`[gold]Block[/gold]` 里的 `Block` 都要跳过 → 脚本先把 `[gold]…[/gold]` 与 `{…}` 标为保护区间，只替换保护区间外的匹配。
- **eng 的“Block”有歧义**：`RHYTHM_MASTER` / `TETRIS` 里的 “Block cards / random Blocks” 指的是**方块牌**（不是格挡），所以 eng 只按 zhs 命中的 **19 张卡**同步，不用“含 Block 就改”。

**未做（留给出题/后续）**：
- eng 侧方块牌的说法仍写作 “Block cards”（zhs 已经是 `[gold]方块[/gold]`）；这是卡名类染色，不属于本次“格挡”范围，**要改请先确认**。
- 全模组其它术语（手牌 54 处、抽牌堆 15、弃牌堆 11、消耗 16、保留 2 等，均为 zhs 裸文本）本次**未动**——用户当前只选了 B 案（仅格挡）；以后要扫请再跑同一套思路的脚本。

**构建**：`dotnet build` **0 错误**（40 个历史警告）→ DLL 424,960 B（未变，无代码改动）、PCK 54,773,404 → **54,774,364 B**（10-04 02:39）。

### 16.7 关键词染色全量补齐（用户追加：「其他应该添加关键字的也全部添加，像抽牌堆、弃牌堆这种的」，2026-10-04）

**范围怎么定的**：先把原版 `localization/zhs|eng/cards.json` 里被 `[gold]` 包住的**非卡名术语**全提取出来（zhs 58 个 / eng 57 个，脚本 `脚本\_vanilla_gold_terms.py`），取出模组用得到的 16 组，逐组数了原版的写法（`脚本\_vanilla_term_ctx.py`）再动手。

**本轮改了多少**（`[gold]` 片段计数，对比 `_xlsx_backup\cards_{zhs,eng}_pre_kwall.json`）：

| 轮次 | zhs | eng | 涉及卡 |
|---|---|---|---|
| 本轮（本轮 16 组术语） | 368 → **624**（+256） | 239 → **506**（+267） | 83 / 96 张 |
| 先前「格挡」轮（§16.6） | +37 | +37 | 19 张 |
| **合计** | 331 → **624**（+293） | 202 → **506**（+304） | — |

术语对照表（zhs → eng 用原版词形）：消耗牌堆→Exhaust Pile、抽牌堆→Draw Pile、弃牌堆→Discard Pile、手牌→Hand、牌组→Deck、消耗→Exhaust/Exhausted、保留→Retain、升级→Upgrade/Upgraded、变化→Transform、斩杀→Fatal、构想→Concept、小游戏牌→Minigame、攻击牌→Attack、方块→（eng 不动，见下）。

**做法**（脚本 `脚本\_sweep_keywords_all.py`，幂等可重跑）：
- **zhs 规则驱动 eng**：zhs 命中哪个词，才在同一张卡的 eng 里改对应词 —— 避开 eng 的一词多义（`Block` 既是格挡又是方块牌；`attack` 既是动词又是攻击牌）。
- **保护区间**：`[gold]…[/gold]` 与 `{…}` 内不替换；**长词优先**（消耗牌堆→消耗、小游戏牌→游戏牌）。
- **中文侧守卫**：构想 后接 之矛/之盾 不换（卡名）；方块 前面是 黄/蓝/紫/绿 不换。
- **eng 二遍补扫**：zhs 没提但 eng 自己说了的（如 `ASCETIC_TRAINING` 的 "from your hand"）再扫一遍；把模组小写的 hand/draw pile/deck/exhaust/transform 统一成原版大写词形。
- **体检**：`脚本\_check_loc_markup.py`（`[gold]` 配对/嵌套/`{}` 内出现 + 术语裸写残留）→ 收尾后 zhs 裸写 **0**、eng 只剩 8 处小写动词 attack（故意不染）。

**刻意不染**：技能牌/能力牌/状态牌（原版就不染，只有 攻击牌 按用户决定染）；生命/能量/回合/伤害等普通名词；eng 侧的**方块牌**（模组把俄罗斯方块译作 "Blue Block / Block cards"，与格挡关键词同形 → 只统一了 zhs 的 `[gold]方块[/gold]`）。

**顺手修掉的两个 eng 历史 bug**（都是体检里暴露的）：
1. `CONCEPT_SPEAR` / `CONCEPT_SHIELD` 的 `{IfUpgraded:show:[gold]stronger |}` **缺 `[/gold]`** → 改为 `[gold]stronger [/gold]`（与 zhs 对齐，共 4 条）。
2. eng 里 **10 张卡末尾手写的 `Exhaust.` / `Retain.` 行**（BORROW_STRENGTH / DUAL_NARRATIVE / FIRE_SERPENT_BITE / FORESHADOW_RECOVERY / SYSTEM_ABISHU / 5 张支援牌）——代码已用 `CanonicalKeywords` 声明，游戏会自动追加英文徐章，手写会在英文界面**显示两份** → 删除（20 条）。

**代码改动（本轮唯一一处 C#）**：`Patches\MinigameSidebarPatch.cs` 新增 4 条提示文本规则：`消耗 → FromKeyword(CardKeyword.Exhaust)`、`保留 → FromKeyword(CardKeyword.Retain)`（两者带 `__instance.Keywords.Contains(...)` 去重）、`变化 → Static(StaticHoverTip.Transform)`、`斩杀 → Static(StaticHoverTip.Fatal)`。

**构建**：`dotnet build` **0 错误**（40 个历史警告）→ DLL 424,960 → **425,472 B**、PCK 54,774,364 → **54,780,972 → 54,781,132 B**（10-04 02:58 / 03:00，后者含下面的卡名补充）。

**收尾补充（同一轮，最后一小改）**：体检脚本 `_check_cardname_refs.py` 又查出 **2 张卡里的「点名原版卡」没染色**（原版 `TheBomb` 炸弹、`Splash` 飞溅）：

| 卡 | 修法 |
|---|---|
| 抽鬼牌！`OLD_MAID` | zhs/eng 两处：`[gold]{IfUpgraded:show:炸弹+|炸弹}[/gold]` / `[gold]{IfUpgraded:show:Bomb+|Bomb}[/gold]`；并给代码补上 `HoverTipFactory.FromCard<TheBomb>(IsUpgraded)` |
| 角色扮演！`ROLE_PLAY` | zhs/eng 两处：同上写法改 `飞溅 / Splash`（代码本来就有 `FromCard<Splash>`）|

脚本 `脚本\_fix_cardname_refs.py`（共 12 条：中英各 6）；收尾自检：**裸卡名引用 0 条**。

**未做（需用户点头才动）**：
- eng 侧方块牌 "Block cards" 的染色（与格挡同形，建议保持现状）；
- `工作区\_design_dump.txt` / xlsx 里的描述是**纯文本**（本来就不带 markup），本次未改；如果以后想让表格也带关键词标记，需要另定格式。

---

## 17. 2026-10-05 卡池改动（删 2 / 增 2 / 改名 1）+ 卡面成品5

**任务**：用户指令「删除普通牌 **私人定制**，新增普通牌 **堕落**（0c：给予自身1层脆弱 + 将1张随机小游戏牌加入手牌，升级后为升级版）；把 **游戏学习** 改名为 **开发秘籍**，所有的地方都要改；删除罕见牌 **便携式掩体**，新增罕见牌 **王不见王**（1c，升级 0c：获得1层缓冲 + 你在接下来的1回合内无法再从卡牌中获得格挡，power 参考原版无色技能 应急按钮）；应用 `工作区\卡面成品5` 的全部卡面，然后跟之前一样修改文档、表格，统计未完成卡面」。

### 17.1 代码改动

| 操作 | 内容 |
|---|---|
| 删除 | `Cards/MinigameFlowCards.cs` 里的 `Handpick`（私人定制，2c 技能·普通）与 `FindCover`（便携式掩体，1c 技能·罕见）两个类（全库无其它引用，`BlockCards` 等公共 helper 保留） |
| 新增 | `Cards/NewCardsBatch2.cs`：`Depravity`（堕落，0c 技能·普通）、`KingsNeverMeet`（王不见王，1c 技能·罕见，升级 0c） |
| 改名 | `Cards/RemainingSpecialCards.cs`：`GameStudy`→`DevSecrets`、`GameStudyPower`→`DevSecretsPower`、`GameStudyData`→`DevSecretsData`；图标路径与文件 `images/powers/game_study_power.png` → `dev_secrets_power.png`。**卡 ID 随类名变化：`STS2_MOMOI_CARD_GAME_STUDY` → `STS2_MOMOI_CARD_DEV_SECRETS`，能力 ID 同理** |
| 侧栏 | `Patches/MinigameSidebarPatch.cs` 加了两条：① 描述含「脆弱/Frail」→ `HoverTipFactory.FromPower<FrailPower>()`；② 描述点到「小游戏牌/Minigame」但**卡本身不是小游戏牌**时，补上小游戏牌侧栏（打游戏！/拾遗/堕落 这类“产生小游戏牌”的卡都受益；靠 `Tags.Contains(MinigameSupport.Tag)` 去重，小游戏牌自己不会重复） |

关键实现（都照抄原版/项目既有写法）：
- **堕落**：`PowerCmd.Apply<FrailPower>(ctx, Owner.Creature, 1, Owner.Creature, this)` + `MinigameSupport.CreateRandomMinigameCard(combatState, Owner, IsUpgraded)`，并保留 `CombatStats.RecordMinigameObtained(card)`（与 打游戏！/拾遗 的「本场未获得过」去重逻辑一致）；`OnUpgrade()` 为空——升级差异只体现在 `IsUpgraded` 分支。
- **王不见王**：`BufferPower` 1 层 + `NoBlockPower`（`DynamicVar("Turns", 1)`）；**与「应急按钮」`PanicButton` 用同一个 power**，文案也照原版写 `{Turns:diff()} {Turns:plural:turn|turns}`；升级 `base.EnergyCost.UpgradeBy(-1)`。

### 17.2 本地化 / 表格 / dump

- `localization\{zhs,eng}\cards.json`：删 `HANDPICK.*` / `FIND_COVER.*`；`GAME_STUDY.*` 整块改名 `DEV_SECRETS.*`（zhs 标题→开发秘籍、eng→Dev Secrets，效果文案不变）；新增 `DEPRAVITY.*` / `KINGS_NEVER_MEET.*`（各 title/description/smartDescription/flavor 四键，**原位插在被删卡的位置**）→ 键数仍 **525**。
- `localization\{zhs,eng}\powers.json`：`GAME_STUDY_POWER.*` → `DEV_SECRETS_POWER.*`。
- `工作区\STS2Momoi.xlsx`：第 41 行原地换成「堕落」、第 63 行换成「王不见王」（类型/稀有度/耗能/描述/升级描述/备注全改），第 85 行「游戏学习」→「开发秘籍」；脚本 `工作区\_scripts\_update_batch5_tables.py`，备份 `_xlsx_backup\STS2Momoi_2026-10-05_*_pre_batch5.xlsx`。
- `工作区\_design_dump.txt`：条目 `[40]`（旧显示名「精挑细选」）改写为堕落、`[62]`（旧显示名「快找掩体！」）改写为王不见王、`[87]` 改名开发秘籍。
- 新卡文案（脚本 `脚本\_update_batch5_text.py` 里有全文）：
  - 堕落 zhs「给予自身1层[gold]脆弱[/gold]。\n将一张{IfUpgraded:show:升级过的|}随机[gold]小游戏牌[/gold]加入你的[gold]手牌[/gold]。」/ eng「Gain 1 [gold]Frail[/gold].\nAdd a {IfUpgraded:show:upgraded |}random [gold]Minigame[/gold] card to your [gold]Hand[/gold].」
  - 王不见王 zhs「获得1层[gold]缓冲[/gold]。\n你在接下来的{Turns:diff()}回合内无法再从卡牌中获得[gold]格挡[/gold]。」/ eng 与原生 PanicButton 同款句式。
  - 脆弱/缓冲/格挡都已按 §7.2 的规矩染色（buff/debuff 名一律 `[gold]`）。

### 17.3 卡面成品5 接入（19 张）

| 成品 | 类名 | 原图 |
|---|---|---|
| 堕落 / 王不见王 | `Depravity` / `KingsNeverMeet` | 新建（新卡） |
| 开发秘籍 | `DevSecrets` | 原 `GameStudy.png`（349,797 B 共用占位）→ 新名新图 |
| 专注 / 伏笔回收 / 再启新篇 / 局势升温 / 开荒 / 整装待发 / 火力爆发 / 灵感爆发 / 热身 / 瓶颈突破 / 翻滚射击 | `Focus` / `ForeshadowRecovery` / `NewChapter` / `PlayWithFire` / `Grinding` / `GearUp` / `FirepowerStrike` / `Inspiration` / `WarmUp` / `BottleneckBreak` / `RollAndShoot` | 349,797 B 共用占位 |
| 序章 / 循环叙事 / 整活 / 蒙太奇 | `Prologue` / `CyclicNarrative` / `Slapstick` / `Montage` | 4 KB 级纯色占位 |
| 王道 | `KinglyWay` | 成品4 的旧图（本次为新版） |

- 全部 **1000×760**，原字节直拷（md5 **19/19** 一致）；旧图备份 `备份\成品5替换备份\`；脚本 `脚本\_apply_batch5.py`（带 `--dry`）。
- 删图：`Handpick.png` / `FindCover.png` / `GameStudy.png`（PNG 备份 `备份\已删卡备份\`，同时删 `.import` 与 `.godot\imported` 缓存，导出日志确认 0 残留）。
- 能力图标改名：`images\powers\game_study_power.png` → `dev_secrets_power.png`（旧 `.import`/ctex 一并清理）。

### 17.4 构建与统计

- 三方自检：卡片 PNG **133**（133 − 2 删 − 1 改名 + 2 新卡 + 1 改名后新图）↔ 代码卡类 **133** ↔ 本地化 **134**（多的仍是 `FRIENDLY_DUEL_B` 翻面）✓；DLL 里已无 `Handpick`/`FindCover`，含 `Depravity`/`KingsNeverMeet`/`DevSecrets` ✓。
- `dotnet build` **0 错误**（40 个历史警告）→ DLL **424,960 B**、PCK **62,060,848 B**（10-05 23:39；19 张新图全部 reimport）。
- 卡面完成度重算：**真实成品 98 / 共用占位 29 / 纯色小占位 6**；待做 AI 卡面 **18 张**（全是普通牌），小游戏牌/游戏牌 17 张按约定不做（§5.3 / §6.2）。

### 17.5 待用户确认 / 风险

- **改名会改卡 ID**：`…_GAME_STUDY` → `…_DEV_SECRETS`（能力同理）。**旧存档里若带着这张卡/能力，建议开新档**（与一删卡同理，mod 无存档迁移机制）。
- 游戏内验证建议（控制台）：`card STS2_MOMOI_CARD_DEPRAVITY`、`card STS2_MOMOI_CARD_KINGS_NEVER_MEET`、`card STS2_MOMOI_CARD_DEV_SECRETS`；重点三条：① 堕落的脆弱是否施加在**自身**（不是敌人）、随机小游戏牌是否到手、升级版是否为升级小游戏牌；② 王不见王的缓冲层数与「无法从卡牌中获得格挡」回合数是否与原版应急按钮一致（且**不影响已获得的格挡**）；③ 开发秘籍（原游戏学习）在改名后小游戏牌触发、减费是否正常。
- `localization\_loc_dump.txt` 是旧快照（仍含 FIND_COVER / GAME_STUDY / HANDPICK 字样），**未更新**——它不是权威数据源，以 `localization\{zhs,eng}\{cards,powers}.json` 为准。

### 17.6 小游戏牌 / 游戏牌侧栏重构（用户追加，2026-10-05）

**用户要求**：
1. 角色池里「有关小游戏牌」的牌**不在小游戏牌池里**；
2. 这些牌的侧栏改成：**小游戏牌**（金色）+「一种特殊的衍生牌。」；
3. 小游戏牌本体的侧栏改成：**小游戏牌**（金色）+「这张牌为小游戏牌。」；
4. 游戏牌的侧栏改成：**游戏牌**（金色）+「这张牌视为小游戏牌，但不会作为小游戏牌局内添加。」。

**关键发现（以前为什么不对味）**：
- `scenes/ui/hover_tip.tscn` 里 `%Title` 是 **金色 Label**（`Color(0.937,0.784,0.318)`）且**不吃 markup**；`%Description` 才是富文本标签。
- 旧实现把侧栏写成 **description-only**（`new HoverTip(new LocString("cards", KEY))`，Title=null）→ 界面上只有一行灰白小字「小游戏牌。」，与「金色标题 + 说明」两段式不符。

**改动**：

| 项 | 内容 |
|---|---|
| 本地化 | 由 2 个单键改为 3×2 键：`STS2_MOMOI_MINIGAME_CARD_SIDEBAR.{title,description}`（小游戏牌 / 这张牌为小游戏牌。）、**新增** `STS2_MOMOI_MINIGAME_KEYWORD_SIDEBAR.{title,description}`（小游戏牌 / 一种特殊的衍生牌。）、`STS2_MOMOI_GAME_CARD_SIDEBAR.{title,description}`（游戏牌 / 这张牌视为小游戏牌，但不会作为小游戏牌局内添加。）；eng 同步。cards.json 键数 525 → **529**。脚本 `脚本\_update_sidebar_texts.py` |
| 补丁 | `Patches/MinigameSidebarPatch.cs`：tag=minigame → 小游戏牌侧栏；tag=fullgame → 游戏牌侧栏；两者都不是但描述提到「小游戏牌/Minigame」→ 关键词侧栏「一种特殊的衍生牌。」；新增 `SidebarTip(key)` 帮助函数（标题 + 说明两段式，标题交给主题染金） |
| 清掉逐卡手写 | 10 处手写的 `GAME_CARD_SIDEBAR` 全部删除（6 张游戏牌改由补丁按 tag 附加；4 张并非游戏牌的卡不再显示该侧栏）；其中 4 处的 `AdditionalHoverTips` 只剩这一个侧栏 → 整个重载一并删除。脚本 `脚本\_remove_manual_game_sidebars.py` |

**「有关小游戏牌」的 20 张卡**（打游戏！/拾遗/堕落/开发秘籍/游戏王形态/专注/心流/博览群游/来自勇者的加护/柚子护航！/熬夜/独特点子/整活/复盘/赖招复读/玩玩这款！/毁灭与新生/发布委托/创造性品味/来自兄弟的协助）：
- 全部**不带** `minigame`/`fullgame` tag，也不在 `MinigameSupport.AllMinigameCards`（写死的 14 个 Token 类）→ 确认**不在小游戏牌池里** ✓；核查脚本 `脚本\_probe_minigame_pools.py` 可复跑。
- 它们现在的侧栏统一是「小游戏牌 / 一种特殊的衍生牌。」；真正的小游戏牌是「小游戏牌 / 这张牌为小游戏牌。」；6 张游戏牌是「游戏牌 / 这张牌视为小游戏牌，但不会作为小游戏牌局内添加。」。
- **顺手修正**：义愤填膺、激战 原本挂着「游戏牌」侧栏（但 xlsx 里标签为空、正文也不提小游戏牌）→ 已移除（若认为需要保留请说明）。

**构建**：`dotnet build` **0 错误**（40 个历史警告）→ DLL 424,960 B、PCK 62,060,848 → **62,061,440 B**（10-06 00:19）。

---

## 18. 2026-10-08 数值调整 + 两处改名 + 卡面成品6

**任务**：用户指令「火焰附加升级前后的耗能都降为1点，其他效果不变；天马行空升级前后的伤害调整为5/7；独特点子升级前后的耗能改为1点，升级前后的伤害调整为造成4/6点伤害2次；打游戏！升级后的耗能降为0点，其他效果不变；节奏大师改名为节奏游戏！；还施彼身改名为针锋相对；应用这次所有改动，以及卡面成品6文件夹里的所有完成卡面到模组中，然后跟之前一样，需要修改和统计的地方继续修改和统计」。

### 18.1 数值调整（4 张）

| 卡 | 项 | 旧 | 新 |
|---|---|---|---|
| 火焰附加 `FlameAttach` | 耗能（含升级） | 2 / 2 | **1 / 1** |
| 天马行空 `BulletRain` | 伤害（含升级） | 4 / 6 | **5 / 7** |
| 独特点子 `UniqueIdea` | 耗能、伤害（含升级） | 2 / 2、6 / 8 | **1 / 1、4 / 6**（仍 2 次） |
| 打游戏！ `PlayGames` | 升级耗能 | 1（升级后仍 1） | **0**（`base.EnergyCost.UpgradeBy(-1)`） |

- 只动数值（`base(cost, …)` / `CalculationBaseVar` / `OnUpgrade()`）；文案全是动态变量，**本地化一个字没改**。
- 打游戏！的表格里本来就写着「费用 1 -> 0」，本次是**代码补上对齐**。
- 顺手修正表里两处与实现不符的旧备注：独特点子的「变化目标都是稀有牌」→ 小游戏牌（升级后为升级版）；dump 条目 [17] 的「随机罕见牌」同上。

### 18.2 两处改名（全量，含 ID）

| 旧 | 新 | 影响面 |
|---|---|---|
| 节奏大师 `RhythmMaster` | **节奏游戏！`RhythmGame`** | 类名、能力 `RhythmMasterPower`→`RhythmGamePower`、图标 `rhythm_master_power.png`→`rhythm_game_power.png`、本地化键（cards+powers、中英）、**`MinigameSupport.AllMinigameCards` 里的类型引用**、卡图文件名 |
| 还施彼身 `BorrowStrength` | **针锋相对 `TitForTat`** | 类名、本地化键（cards、中英）、卡图文件名 |

- 英文标题同步：`Rhythm Master` → `Rhythm Game!`，`Borrowed Force` → `Tit for Tat`。
- **卡 ID 随类名变化**：`…_RHYTHM_MASTER` → `…_RHYTHM_GAME`、`…_BORROW_STRENGTH` → `…_TIT_FOR_TAT`、`…_POWER_RHYTHM_MASTER_POWER` → `…_POWER_RHYTHM_GAME_POWER` → **旧存档/旧控制台命令要换新 ID**（mod 无存档迁移机制）。
- 脚本：`脚本\_rename_rhythm_titfortat.py`（本地化）、`脚本\_apply_batch6.py`（卡图与能力图标文件改名）。

### 18.3 卡面成品6 接入（26 张）

其中 **17 张小游戏牌/游戏牌**此前一直挂着共用占位图（“不做 AI 卡面”的约定），本次一次性补齐：

| 类别 | 卡 |
|---|---|
| 小游戏牌（13） | 吃豆人！/ 愤怒的小鸟 / 打灰机！/ 扫雷 / 植物大战僵尸 / 消消乐！/ 绝地求生 / 节奏游戏！/ 贪吃蛇 / 超级玛丽 / 跑酷！/ 连连看！/ 黄金矿工！ |
| 游戏牌（4） | 捕鱼达人！/ 旅行异蛙 / 街啪6 / 角色扮演！ |
| 普通牌（7） | 博览群游 / 埋下伏笔 / 局势升温（新版）/ 渔获 / 独特点子 / 翻滚射击（新版）/ 赖招复读 / 集思广益 |
| 改名卡（2） | 节奏游戏！`RhythmGame`、针锋相对 `TitForTat` |

- 全部 **1000×760**，原字节直拷（md5 **26/26** 一致）；旧图备份 `备份\成品6替换备份\`；删旧名图 `RhythmMaster.png` / `BorrowStrength.png`（含 `.import` 与 `.godot\imported` 缓存，PNG 备份 `备份\已删卡备份\`）；能力图标改名 `rhythm_master_power.png` → `rhythm_game_power.png`。
- 对照图 `_batch6_contact_sheet.jpg`（26 张，已逐张核对卡名与画面）。
- ⚠ **针锋相对.png 是「按文件名」应用的**：它与成品5 的旧「局势升温」图**字节完全相同**（1,227,032 B、同一 mtime 10-05 19:16）。已问过用户，答复「就按文件名应用」——即**针锋相对 = 「两人躺床上」那张**，**局势升温 = 成品6 里新的「两张 chibi 对峙 + 闪电」那张**。若以后想对调，把两张图换名后重跑 `_apply_batch6.py` 即可。

### 18.4 构建与统计

- `dotnet build` **0 错误**（40 个历史警告）→ DLL **424,960 B**、PCK 62,061,440 → **69,326,972 B**（10-08 08:21）；26 张新图全部 reimport；DLL 里已无 `RhythmMaster`/`BorrowStrength`，含 `RhythmGame`/`TitForTat`。
- 三方自检：133 卡类 ↔ 133 PNG ↔ 本地化 134 卡（多的仍是 `FRIENDLY_DUEL_B` 翻面）✓；标记检查无新增问题。
- 卡面完成度重算：**真实成品 122 / 共用占位 10 / 纯色小占位 1**；待做 AI 卡面 **11 张**（全部是普通牌，§6.2）；**小游戏牌/游戏牌 20 张已全部有图**。
- 表格同步：xlsx 第 8/20/23/96/104 行、`_design_dump.txt` 条目 [5]/[17]/[100]/[105]；脚本 `工作区\_scripts\_update_batch6_tables.py`；备份 `_xlsx_backup\STS2Momoi_2026-10-08_*_pre_batch6.xlsx`。

### 18.5 待用户验证

- 控制台：`card STS2_MOMOI_CARD_FLAME_ATTACH`（1 费）、`…_BULLET_RAIN`（5 伤 / 升级 7）、`…_UNIQUE_IDEA`（1 费 4 伤×2 / 升级 6 伤×2）、`…_PLAY_GAMES`（升级后 0 费）、`…_RHYTHM_GAME`、`…_TIT_FOR_TAT`。
- 重点两条：① 独特点子打出后是否**变化为随机小游戏牌**（升级版为升级过的小游戏牌）；② 节奏游戏！改名后小游戏触发与方块逻辑正常。

---

## 19. 2026-10-09 保留/文本批量修改 + 见招拆招改名 + 删轮回 + 新增我复活啦！

**任务**：用户指令「争锋相对升级前后都删去保留效果；修行升级前也获得保留效果；街啪6侧边栏消耗3点能量改为消耗3点能量及以上；见招拆招改名为对策；白与黑文本：选择后将在本场战斗中删去另一个选项；删除稀有技能牌轮回（保留一份备份，后面可能会重新启用这张卡），新增稀有技能牌我复活啦！…（附专业 AI 的局内删牌 / 免死钩子指导，说明可以参考但不要全盘接收、不要擅自加效果）；应用卡面成品7的目前唯一一个卡面我复活啦！」。

### 19.1 保留 / 文本改动

| 卡 | 改动 | 实现 |
|---|---|---|
| 针锋相对 `TitForTat` | 升级前后都**删去保留** | `CanonicalKeywords` 由 `{ Exhaust, Retain }` → `{ Exhaust }`（升级「不再消耗」的行为不变） |
| 修行 `AsceticTraining` | 升级**前**也获得保留 | `CanonicalKeywords => { Retain }`（原来只在 `OnUpgrade` 里 `LocalKeywords.Add(Retain)`，该冗余行已删） |
| 街啪6 侧栏第 4 条 | 「消耗3点能量：」→「**消耗3点能量及以上：**」 | 本地化 `STS2_MOMOI_CARD_FIGHTING_GAME.sidebar3`（zhs+eng；eng `Spend 3 Energy:` → `Spend 3 or more Energy:`） |
| 白与黑 `WhiteAndBlack` | 「选择后将删去另一个选项。」→「**选择后将在本场战斗中删去另一个选项。**」 | zhs/eng 的 description + smartDescription（eng：`The other option is removed.` → `... removed for this combat.`）；实际行为本来就是仅本场战斗生效，本次只是把文本说清楚 |
| 见招拆招 → **对策** | 全量改名 | 类 `RightRemedy` → **`Countermeasure`**、本地化键 `RIGHT_REMEDY.*` → `COUNTERMEASURE.*`、zhs 标题→对策 / eng→`Countermeasure`、卡图 `RightRemedy.png` → `Countermeasure.png`。**卡 ID 变为 `STS2_MOMOI_CARD_COUNTERMEASURE`**（旧存档注意） |

### 19.2 删除 轮回（保留可重启备份）

- 删除范围：卡类 `Reincarnation`（3c 稀有技能）+ 能力类 `ReincarnationDrainPower`（`Cards/RemainingCards2.cs` 内，共 101 行）、本地化键（cards 4 键 × 2 语言、powers 3 键 × 2 语言）、卡图 `Reincarnation.png`、能力图标 `reincarnation_drain_power.png`（含 `.import` 与 `.godot` 缓存）、xlsx 行 68、dump 条目 `[68]`。
- **完整备份（可一键重启）**：`工作区\已删卡_备份\轮回_Reincarnation\`
  `Reincarnation_and_Power.cs.txt`（两类源码，含 XML 注释与 `[RegisterCard]`/`[RegisterPower]`）、`loc_{zhs,eng}_{cards,powers}.json`、`Reincarnation.png`、`reincarnation_drain_power.png`、`table_backup.json`（xlsx 行 + dump 条目原文）、**`README.md`（6 步重启步骤）**。
- 依赖的共享设施**没动**：`CombatStats.LastTurnPlayed` + `PlayerTurnEndSnapshotPatch`（重启后直接可用）。

### 19.3 新增 我复活啦！ `ImBack`

| 项 | 值 |
|---|---|
| 类型 | 0 费技能（**稀有**，`STS2_MomoiCardPool`） |
| 效果 | 获得 **3** 点活力（升级 **5**） |
| 免死 | 你的生命值将被减少至 0 或以下时：改为**消耗**并从**牌组中移除**这张牌 → 将你**回复到你最大生命值的 10%** → 获得 **5** 层再生（升级 **6**） |
| 免死后的卡 | 本场战斗的副本进消耗牌堆，牌组本尊被移除（这张牌本局游戏彻底消失，符合“从牌组中移除”） |

**实现要点**（照抄原版 + 采纳指导里正确的部分，**没有加任何额外效果**）：
- 免死：`ShouldDieLate(creature)`（尾钩）+ `AfterPreventingDeath(creature)`，抄原版 `LizardTail`；`_used` 标记保证**只生效一次**；`creature != Owner.Creature` 保证**不会拦敌人的死亡**；**局外（combatState 为 null）同样会被判定到**（见 §19.7）。
- 牌组移除：抄原版 `DeprecatedCard` 的 `DeckVersion` 写法 —— `CardPileCmd.RemoveFromDeck(original)` 只接受 `Pile.Type == PileType.Deck` 的卡，所以**不能把战斗克隆直接传进去**；克隆体的 `DeckVersion` 才指向本尊，且战斗中生成的卡 `DeckVersion` 为 null（已判空）。
- 谁当 preventer 由框架决定（多个同名卡只有第一个拦下来的会被回调 `AfterPreventingDeath`），所以代码对“本尊”和“副本”两种身份都做了处理：`DeckVersion != null` → 本次是副本；否则用 `FindCombatClone()` 在 手牌/抽牌堆/弃牌堆/Play 里找副本（已在消耗牌堆的副本不会二次触发）。
- 顺序按用户要求：**先消耗副本 → 再从牌组移除本尊** → 最后 `CreatureCmd.Heal(回复到 10% 所需的差值)` + `PowerCmd.Apply<RegenPower>`；两个调用用 `new ThrowingPlayerChoiceContext()`（无 choiceContext 的钩子里模组既有写法）。
- 「回复到 10%」用的是 `Heal(target - CurrentHp)` 而不是 `Heal(10% MaxHp)`，这样即使 HP 被压到负数也**精确落在 10%**，同时保留治疗动画。
- 无状态漏存：`_used` 不是 `SavedProperty`，但卡一旦触发就从牌组移除，不会二次生效。
- 侧栏：`MinigameSidebarPatch` 新增 `再生/Regen → FromPower<RegenPower>()`；「消耗」不是本卡关键词（只在触发时消耗），所以由补丁的文本扫描自动补 Exhaust 提示。

### 19.4 卡面成品7（1 张）

- `我复活啦！.png`（1000×760 RGBA，1,179,104 B）→ `images/cards/ImBack.png`（原字节直拷，md5 一致）；
- 删图：`Reincarnation.png`、`reincarnation_drain_power.png`（备份见 §19.2，能力图标同时从 `images\powers` 移除）；
- 卡图改名：`RightRemedy.png` → `Countermeasure.png`（见招拆招改名；该卡目前仍是 349,797 B 共用占位图）。

### 19.5 构建 / 表格 / 统计

- `dotnet build` **0 错误**（39 个历史警告，比上批少 1 条）→ DLL 424,960 → **423,424 B**、PCK 69,326,972 → **69,909,720 B**（10-09 13:15）；`ImBack.png` 已 reimport 进包；DLL 内含 `ImBack`/`Countermeasure`/`ShouldDieLate`/`AfterPreventingDeath`，已无 `Reincarnation`/`RightRemedy`。
- 三方自检：133 卡类 ↔ 133 PNG ↔ 本地化 134 卡（多的仍是 `FRIENDLY_DUEL_B` 翻面）✓。
- 表格：xlsx 第 23/45/68/69/127 行、`_design_dump.txt` 条目 [21]/[44]/[68]/[70]/[91]（后三个在 dump 里还是旧名 借力打力/对症下药/活学活用，已一并按现名改写）；脚本 `工作区\_scripts\_update_batch7_tables.py`，备份 `_xlsx_backup\STS2Momoi_2026-10-09_*_pre_batch7.xlsx`。
- 卡面完成度重算：**真实成品 123 / 共用占位 9 / 纯色小占位 1**；待做 AI 卡面 **10 张**（双线叙事、复盘、对策、心流、曳光弹、机会难得选红色！、玩玩这款！、趁热打铁、重整旗鼓、金色传说！）。

### 19.6 待用户验证（重点）

1. **我复活啦！的免死链**：控制台 `card STS2_MOMOI_CARD_IM_BACK`，然后在战斗中把自己打到 0 血：
   - 是否**没有死**、回复到 10% 最大生命、获得 5/6 层再生；
   - 该牌是否**从牌组中消失**（牌堆界面确认），消耗牌堆里能看到它；
   - 触发后**再死一次**应当正常死亡（`_used`）；
   - 牌只放在牌组里没抽到 / 在抽牌堆 / 在手牌 / 在弃牌堆 —— 四种情况都应触发；已经在消耗牌堆时不触发。
2. 针锋相对：升级版是否**不再保留**（回合结束会正常弃掉）；修行：未升级版是否**有保留**。
3. 对策改名后：卡图/名称/描述正常（仍是占位图，等用户出图）。
4. 街啪6 侧栏第 4 条文案；白与黑 描述是否显示「在本场战斗中」。

### 19.7 我复活啦！局外免死修复（报错复盘，2026-10-09 13:44 反馈）

**用户反馈**：局外掉血至 0 以下时报错（日志 `devmode-report-20261009-132443`），并要求**局外也要免死并回血、并从牌组移除**（局外没有战斗牌堆与能力系统，所以不消耗、不给再生）。

**报错原文（godot.log）**：
```
[ERROR] System.InvalidOperationException: Tried to get Hand pile while out of combat.
   at MegaCrit.Sts2.Core.Entities.Cards.PileTypeExtensions.GetPile(PileType pileType, Player player)
   at STS2_Momoi.Cards.ImBack.FindCombatClone()
   at STS2_Momoi.Cards.ImBack.AfterPreventingDeath(Creature creature)
   at MegaCrit.Sts2.Core.Commands.CreatureCmd.KillWithoutCheckingWinCondition(...)
   at MegaCrit.Sts2.Core.Commands.CreatureCmd.Damage(...)
   at MegaCrit.Sts2.Core.Models.Events.SunkenStatue.DiveIntoWater()
```
**根因**：`PileTypeExtensions.GetPile()` 在局外会直接 `throw new InvalidOperationException("Tried to get {pileType} pile while out of combat.")`（因为 `CardPile.Get` 返回 null）。我原来的 `FindCombatClone()` 无条件遍历 Hand/Draw/Discard/Play 四个**战斗牌堆**，于是在**局外事件致死**（本例是「沉没雕像」事件）时抛异常 → `TaskHelper.LogTaskExceptions` 接住 → 后续的「从牌组移除 + 回血」全被跳过（玩家被救下来了但停在 0 血、卡也没删）。
> 另外：免死本身是**生效**的 —— `Hook.ShouldDie(runState, combatState: null, …)` 在局外同样会遍历玩家牌组里的卡（`RunState.IterateHookListeners` + `RunState.Contains` 只要求 `!HasBeenRemovedFromState && Owner.IsActiveForHooks`），所以 `ShouldDieLate` 在局外被问到了，问题只出在 `AfterPreventingDeath` 的实现。

**修法**（`Cards/ImBack.cs`）：
1. `FindCombatClone()` 改用 **`CardPile.Get(pileType, player)`**（局外返回 **null**，不抛异常）替代 `pileType.GetPile(player)`，并只在局内调用；
2. `AfterPreventingDeath` 分「局内/局外」两条路径：
   | 步骤 | 局内 | 局外 |
   |---|---|---|
   | ① 消耗战斗中的副本 | ✅ `CardCmd.Exhaust`（在 Hand/Draw/Discard/Play 才消耗，已在消耗牌堆的副本跳过） | ⏭️ 跳过（没有战斗牌堆） |
   | ② 从牌组移除本尊 | ✅ `CardPileCmd.RemoveFromDeck`（只接受 `Pile.Type == Deck` 的卡） | ✅ 同样执行 |
   | ③ 回复到最大生命值的 10% | ✅ `Heal(target - CurrentHp)`（HP 为负也精确落在 10%） | ✅ 同样执行 |
   | ④ 获得 5/6 层再生 | ✅ `PowerCmd.Apply<RegenPower>` | ⏭️ 跳过（没有能力系统） |
3. 局内/局外判定 = `player.Creature.CombatState != null`；
4. 顺序保持用户要求：**先消耗副本 → 再从牌组移除本尊 → 回血 → 再生**（局外自然退化为「移除 + 回血」）。

**参考过、没采纳的部分**（用户说“可以参考但不要全盘接收”）：
- 指导里的示例用 `Math.Max(1m, MaxHp * 0.3m)` **直接 Heal 百分比**；本卡保留“回复**到** 10%”的算法（`Heal(target - CurrentHp)`），因为它是「回复到」而不是「回复 10%」。
- 指导提到 `ShouldDie`（精灵写法，优先）与 `ShouldDieLate`（尾巴写法）二选一 —— 本卡沿用 **`ShouldDieLate`**（原版蜥蜴尾巴写法，效果已实测可在局外触发）。
- 指导提到“伤害阈值才触发”需要在 `BeforeDamageReceived` 存伤害 —— 本卡**没有阈值需求**，不引入额外状态。
- 多人局非战斗致死的特例（`CreatureCmd.cs:522`：非战斗 + 多人 + 非 force 时直接回 1 点血并 return，**不会走到 Hook**）→ 本卡在这种情况**不消耗**，与原版精灵瓶/蜥蜴尾巴一致，无需额外处理。

**构建**：`dotnet build` **0 错误**（39 个历史警告）→ DLL 423,424 → **423,936 B**、PCK 69,909,656 → **69,909,720 B**（10-09 13:30）。

**待用户复测**：① 局外事件掉血至 0（如沉没雕像）→ 应免死 + 回到 10% 血 + 卡从牌组消失，且**不再报错**；② 局内免死链仍正常（消耗 + 移除 + 10% + 再生）；③ 触发过再一次致死应正常死亡；④ 局外触发后再进战斗，牌组里应当已经没有这张牌。

> 文案未动：卡面描述现在写的是局内版本（“改为消耗并从牌组中移除这张牌，然后…获得再生”）；局外是不消耗、不给再生的子集。若希望描述里也写清局外行为（例如加一句“（局外改为直接从牌组移除）”），说一声就加。

---

## 20. 2026-10-11 文本修正 + 三个卡牌关键词 + 删/增 2 张 + 卡面成品7 全量

**任务**：用户指令「局势升温文本『2张灼烧』改正为『1张灼伤』（实际效果不变，是抽牌堆/弃牌堆各塞 1 张，原文有误）；双线叙事『使构想的数值加2。』→『使构想数值+2。』；删除罕见技能牌金色传说（保留备份），新增罕见攻击牌游戏人生…；为所有游戏牌/小游戏牌/支援牌的卡牌文本最上方加金色『游戏牌。』『小游戏牌。』『支援牌。』（可以用关键字实现）；支援牌侧栏也要有（支援牌 / 这张牌为支援牌。），得道多助和集结原有的支援牌标签保留；删除罕见能力牌趁热打铁（保留备份）；火焰附加 稀有→罕见；新增稀有技能牌暗黑心理学（使一名敌人在下次获得力量时将不再获得，改为使构想数值+1。消耗。升级：不再消耗）…（附 AI 给的修饰器钩子实现建议，说明可参考但要实现要求的效果、别擅自加效果）；应用卡面成品7 的所有卡面」。

### 20.1 文本修正（2 处）

| 卡 | 旧 | 新 | 说明 |
|---|---|---|---|
| 局势升温 `PlayWithFire` | 分别将**2 张灼烧**加入你的弃牌堆和抽牌堆。（eng: `Add 2 Burn … and 2 to …`） | 分别将**1 张灼伤**加入你的弃牌堆和抽牌堆。（eng: `Add 1 Burn … and 1 to …`） | 实际代码就是 `combatState.CreateCard(ModelDb.Card<Burn>())` ×2，一个进弃牌堆一个进抽牌堆 → 每边 **1 张**；且这张是原版的 **灼伤** 状态牌（`BURN`），不是「灼烧」层数（原版卡表：`BURN.title = 灼伤`）——之前两张牌共用一个词，容易误读，本次按用户要求区分开 |
| 双线叙事 `DualNarrative` | 使构想的数值加2。 | 使构想**数值+2**。 | 只改措辞（与「剧情推进！使构想数值+1」统一）；效果/数值不变 |

### 20.2 三个卡牌关键词：游戏牌 / 小游戏牌 / 支援牌（描述顶行金色文本）

用户要求「在卡牌文本直接看到这几个字」，实现方式选了**模组自定义关键词**（用户在提示里也认可这条路）：

| 项 | 内容 |
|---|---|
| 关键词注册 | `STS2 MomoiCode\Keywords\MomoiKeywords.cs`：`[RegisterOwnedCardKeyword("GameCard"/"MinigameCard"/"SupportCard", CardDescriptionPlacement = BeforeCardDescription, IncludeInCardHoverTip = false)]`；RitsuLib 会把「**金色标题 + 句号**」插到卡牌描述最上方（句号取自 `card_keywords` 表的 `PERIOD`，与卡牌描述里的 `[gold]` 无关，所以**标题里不要写 markup**） |
| 本地化 | **新建** `localization\{zhs,eng}\card_keywords.json`：`STS2_MOMOI_KEYWORD_GAME_CARD.{title,description}` 等 + `PERIOD`（中英各 13 键）。RitsuLib 的键由「限定 ID」生成，为防 stem 规范化差异（`GAME_CARD` vs `GAMECARD`）**两种拼法都写了**，多余键不会被引用 |
| 哪些牌带哪个 | `Patches\CardKeywordLabelPatch.cs`（挂 `CardModel.GetKeywordsWithSources`，**非虚公共方法**，所有卡都走它）：`fullgame` 标签 → 游戏牌；`minigame` 标签 → 小游戏牌；支援牌类型（支援池 14 种 + 解锁后的千寻/时，见 `MinigameSupport.AllSupportCardTypes`）→ 支援牌 |
| 为什么不用 `CanonicalKeywords` | 它是虚属性、各卡自己 override 过（小游戏牌/游戏牌很多都写了 `{ Exhaust }`），挂基类 getter 会被派生类绕过（项目里 `ExtraHoverTips` 补丁踩过同款坑）；而 `GetKeywordsWithSources` 是非虚公共方法，一处覆盖全部卡 |
| 局内动态 | 「游戏人生」用 `AddModCardTag(FullGameTag)` 给手牌加标签 → 同一个补丁下一帧就会让描述顶行出现「游戏牌。」（卡面用 `UpdateVisuals` 刷新） |
| 支援牌侧栏 | `MinigameSidebarPatch` 新增：`STS2_MOMOI_SUPPORT_CARD_SIDEBAR`（标题「支援牌」+ 说明「这张牌为支援牌。」），与小游戏牌/游戏牌侧栏同款两段式；得道多助/集结原有的「支援牌清单」侧栏**保留不动** |

> 未与用户确认的细节：支援牌集合按**支援池类型**判定（`MinigameSupport.AllSupportCards` + 千寻/时 = 16 张，含柚子护航！）；代码里带 `support` 标签的只有「来自勇者的加护 / 开发者协同：绿」两张，两张都在支援池里，所以按类型判定同时也覆盖了它们。

### 20.3 删除 / 新增（各 2 张 + 1 处稀有度）

| 操作 | 内容 |
|---|---|
| 删除 | **金色传说！`GoldenLegend`**（1c 技能·罕见：随机稀有牌入手，消耗/升级 0c）→ 完整备份 `工作区\已删卡_备份\金色传说_GoldenLegend\`（源码/本地化 4 键×2 语言/卡图/表格行） |
| 删除 | **趁热打铁 `DayAndNight`**（1c 能力·罕见：每回合首次构想→失 1 活力+加 1 构想，升级固有）+ 能力 `DayAndNightPower` → 备份 `工作区\已删卡_备份\趁热打铁_DayAndNight\`（含能力源码、本地化、卡图、能力图标、表格行） |
| 新增 | **游戏人生 `GameLife`**（1c 攻击·**罕见**）：造成 **9**（升级 **12**）点伤害；为一张**手牌**添加「游戏牌」标签（升级：连同它的**所有同名牌**）。选择界面过滤掉已经是游戏牌/小游戏牌的牌（`!MinigameSupport.IsMinigameCard(c)`）；**标签只作用于本场战斗的这张牌**（不写回牌组本尊，战斗结束即失效 —— 用户 2026-10-11 追加要求，见 §20.7），并用 `UpdateVisuals` 刷新手牌卡面让顶行文本立即出现 |
| 新增 | **暗黑心理学 `DarkPsychology`**（2c 技能·**稀有**）+ 能力 `DarkPsychologyPower`：使一名敌人在下次获得力量时将不再获得，改为使**所有玩家**手牌中的构想数值 +1（多人局对每个玩家都生效，没有构想的玩家不受影响）；**消耗**；升级**不再消耗**（`LocalKeywords.Remove(CardKeyword.Exhaust)`） |
| 稀有度 | 火焰附加 `FlameAttach`：**稀有 → 罕见**（`CardRarity.Rare` → `Uncommon`），效果不变 |

**暗黑心理学（能力）实现要点**（采纳了 AI 建议的「修饰器钩子」路线，**没有加额外效果**）：
- 能力在**敌人身上**（`TargetType.AnyEnemy` + `PowerCmd.Apply<DarkPsychologyPower>(choiceContext, target, 1, …)`），`PowerType.Debuff`、`PowerStackType.Counter`（**只叠次数**，每层抵消一次力量获得）。
- 拦截：`TryModifyPowerAmountReceived(canonicalPower, target, amount, applier, out modifiedAmount)` —— `canonicalPower is StrengthPower && target == Owner && amount > 0` 时把 `modifiedAmount = 0` 并返回 true（**写法与原版神器 `ArtifactPower` 完全同款**）；`amount <= 0` 直接放行 → **只拦力量增加，不拦力量减少**。
- 触发后：`AfterModifyingPowerAmountReceived(power)`（原版在 `PowerCmd` 里**即使结算量变成 0 也一定会调用**，所以放这里最稳）→ ① 遍历 `combatState.Players`，对每个玩家调 `ConceptCounterCapability.AddCountToAllInHand(...)`（构想的既有工具，自带卡面刷新）；② `PowerCmd.Decrement(this)` 消耗 1 层（减到 0 自动移除）。
- 关于「临时减力量」：原版没有单独的「扣力量 power」，`TemporaryStrengthPower`（束缚 `DarkShackles` 派生）是「立刻真扣、回合结束真还」两次**真实**的 `StrengthPower` 增减 → 所以回合结束的「补回」属于力量增加，**会被本能力拦掉**（用户已确认这就是想要的行为）。
- 能力图标：`images\powers\dark_psychology_power.png`（先复制 `game_study.png` 占位，后续可替换）。

### 20.4 卡面成品7 全量（9 张）

| 成品 | 类名 | 原图 |
|---|---|---|
| 暗黑心理学 / 游戏人生 | `DarkPsychology` / `GameLife` | 新建（新卡） |
| 复盘 / 对策 / 心流 / 曳光弹 / 玩玩这款！ | `GameReview` / `Countermeasure` / `FlowState` / `FlameBullet` / `PlayThisOne` | 349,797 B 共用占位 |
| 抽鬼牌！ | `OldMaid` | 早期成品（本次为新版） |
| 我复活啦！ | `ImBack` | 上一批已接入（**md5 相同，跳过**） |

- 全部 1000×760，原字节直拷（md5 **9/9** 一致）；旧图备份 `备份\成品7全量替换备份\`；脚本 `脚本\_apply_batch8.py`（带 `--dry`）。
- 删图：`GoldenLegend.png` / `DayAndNight.png` / `images\powers\day_and_night_power.png`（含 `.import` 与 `.godot\imported` 缓存）。
- ⚠ `工作区\卡面成品6\` 已被用户删除（内容上一批已全部应用，不影响）。

### 20.5 构建 / 表格 / 统计

- `dotnet build` **0 错误**（38 个历史警告）→ DLL 423,936 → **427,520 B**、PCK 69,909,720 → **71,522,456 B**（10-11 09:50）；9 张新图全部 reimport；DLL 内含 `GameLife` / `DarkPsychology(+Power)` / `MomoiKeywords` / `CardKeywordLabelPatch`，已无 `GoldenLegend` / `DayAndNight`。
- 三方自检：133 卡类 ↔ 133 PNG ↔ 本地化 134 卡（多的仍是 `FRIENDLY_DUEL_B` 翻面）✓；`_check_loc_markup.py` 无新增问题（zhs 裸写 0、eng 只剩 8 处小写动词 attack）。
- 表格：xlsx 第 18/58/94/96/98 行、`_design_dump.txt` 条目 `[15]`/`[57]`/`[98]`/`[100]`/`[102]`（dump 里 局势升温/金色传说！/趁热打铁 分别还叫 玩火/金色传说！/夜以继日，已一并改成现名）；脚本 `工作区\_scripts\_update_batch8_tables.py`，备份 `_xlsx_backup\STS2Momoi_2026-10-11_*_pre_batch8.xlsx`。
- 卡面完成度重算：**真实成品 130 / 共用占位 2 / 纯色小占位 1** → **只剩 3 张没有卡面**：双线叙事、重整旗鼓（共用占位）、机会难得，选红色！（纯色）。

### 20.6 待用户验证（重点）

1. **顶行金色标签**：随便看一张小游戏牌（如 吃豆人！）→ 描述最上方应是金色「小游戏牌。」；游戏牌（捕鱼达人！等）→「游戏牌。」；支援牌（柚子护航！/来自勇者的加护…）→「支援牌。」。
   - 若三个关键词**都没显示**：大概率是 `card_keywords.json` 的键拼法不对（RitsuLib 用限定 ID 生成键）→ 看 `%APPDATA%\SlayTheSpire2\devmode-reports\...\godot.log` 有没有缺本地化的报错，按报错里的键名改 `card_keywords.json` 即可（两种拼法都写了就是为了兜底）。
   - 若显示成 `[gold]小游戏牌[/gold]。` 这种带方括号的 → 说明 `IncludeInCardHoverTip`/标题注入了 markup，把 card_keywords 里的 `.title` 改成纯文字（本来就是纯文字）。
2. **游戏人生**：`card STS2_MOMOI_CARD_GAME_LIFE` → ① 选择界面里**不应出现**已是游戏牌/小游戏牌的牌；② 选中的牌描述顶行应立刻出现「游戏牌。」；③ 升级版应连同**本场战斗里所有同名牌**（手牌/抽牌堆/弃牌堆）一起加；④ 加过标签的牌应当开始吃小游戏牌相关增益（如 专注/心流/博览群游/游戏王形态 的计数）；⑤ **战斗结束后**（下一场战斗）该牌应不再有「游戏牌。」顶行文本、也不再算小游戏牌（标签不写回牌组本尊）。
3. **暗黑心理学**：`card STS2_MOMOI_CARD_DARK_PSYCHOLOGY` → 给敌人挂上后，敌人下一次获得力量应**不涨力量**、转而你的（所有玩家的）构想数值 +1，且能力层数 -1；叠 2 层应能挡 2 次；升级版打出后**不进消耗堆**。
4. **火焰附加**：稀有度应为罕见（奖励/图鉴里体现）；**游戏人生** 是罕见攻击牌；**暗黑心理学** 是稀有技能牌。

> 环境提醒：本机 `python` 现在会命中 WindowsApps 的 Store 占位程序（退出码 49、无输出），本批全部改用 `py -3`（已记入 §7.5）。

### 20.7 追加修正：游戏人生 的标签改为「只在本场战斗生效」（2026-10-11 用户要求）

**用户要求**：「游戏人生给手牌添加游戏牌标签的效果应该是只有那一场战斗生效，不影响牌组的本尊。」

**改法**（`Cards/GameLife.cs`，只动两处）：
| 位置 | 旧 | 新 |
|---|---|---|
| `ApplyGameCardLabel` | `AddModCardTag` 之后还会 `card.DeckVersion.AddModCardTag(...)`（写回牌组本尊） | **删掉**牌组本尊那一段；只给战斗中的这个实例加标签 |
| `ApplyToSameNameCards`（升级版） | 遍历 手牌/抽牌堆/弃牌堆 **+ `Owner.Deck.Cards`** | **去掉牌组那一轮**；只处理本场战斗三个牌堆里的同名牌 |

- 效果语义：战斗内该牌（及其同名牌）立即变成「游戏牌」（吃小游戏牌相关增益 + 描述顶行出现金色「游戏牌。」），**战斗结束即失效**，牌组本尊不受影响、不影响后续战斗。
- 顶行文本不需要额外处理：`CardKeywordLabelPatch` 是按**标签**现算的，战斗克隆体的标签一变就会跟着变 ✓。
- 同步：xlsx 第 58 行与 `_design_dump.txt` 条目 `[57]` 的备注已改成「标签只作用于本场战斗的这张牌（不写回牌组本尊）」；脚本 `工作区\_scripts\_fix_gamelife_notes.py`。
- 构建：`dotnet build` **0 错误**（38 个历史警告）→ DLL 427,520 → **427,008 B**、PCK **71,522,472 B**（10-11 09:57）。

---

## 21. 2026-10-11 批次9：文本大改 + 重整旗鼓改名 + 卡面成品8 + 三处机制改动

> 脚本：`工作区/_scripts/_update_batch9_loc.py`（卡牌本地化）、`_update_batch9_pow.py`（能力侧栏）、
> `_update_batch9_tables.py`（xlsx + 设计 dump）、`_verify_batch9.py`（50 条自检）、
> `_icon_inventory.py` + `_regen_art_status.py`（统计）。
> 备份：`工作区/_backup/_xlsx_backup/STS2Momoi_*_pre_batch9.xlsx`、`工作区/_backup/_cardart_backup9/`。

### 21.1 改名：重振旗鼓 → 重整旗鼓

「重振旗鼓」是常见错写，正确写法是**重整旗鼓**。全局替换 12 处：
本地化 `zhs/cards.json`（卡名）、`zhs/powers.json`（能力名）、
`STS2 MomoiCode/Cards/RemainingCards3.cs`（3 处注释）、`Patches/DustyTomePatch.cs`（2 处注释）、
`STS2_Momoi_迁移文档.md`（4 处）、`工作区/STS2_Momoi_迁移文档.md`（1 处）、`工作区/_design_dump.txt`（1 条标题）、
xlsx 第 97 行。**类名 / 卡 ID（RallyAgain / STS2_MOMOI_CARD_RALLY_AGAIN）没有动**，只改显示名。

### 21.2 卡面成品8（3 张，全部接完）

`工作区/卡面成品8/` → `STS2_Momoi/images/cards/`，文件名沿用类名：

| 源文件 | 目标 | 旧状态 | 新 |
|---|---|---|---|
| `双线叙事.png` | `DualNarrative.png` | 共用占位 349,797 B | 792,616 B |
| `机会难得，选红色！.png` | `PickRed.png` | 纯色占位 489 B | 583,887 B |
| `重整旗鼓.png` | `RallyAgain.png` | 共用占位 349,797 B | 365,703 B |

**统计结果：133/133 全部真实成品，0 个占位**（`工作区\_data\_card_art_status.json` / `.txt` 已重生成）。

> 注：重生成脚本的类名配对要用「去下划线 + 全小写」的归一化 —— 游戏那边的蛇形命名并不规则
> （`STS2_MomoiStrike` → `STS2_MOMOI_STRIKE`，而不是 `S_T_S2_MOMOI_STRIKE`）。

### 21.3 双线叙事：只复制选中的一张 + 给原构想加重放

| | 改动前 | 改动后 |
|---|---|---|
| 复制范围 | 手牌里**所有**构想各复制一张 | **只复制玩家选中的那 1 张** |
| 重放 | 无 | **被复制的那张原构想** `BaseReplayCount++`（已有重放则次数 +1） |
| 复制品 | 只附魔灵魂之力 | 只附魔灵魂之力（**不加重放**，与之前一致） |

- 选择界面：`CardSelectCmd.FromHand` + `c => c is ConceptCard` 过滤，提示词新增本地化键
  `card_selection.TO_CLONE_CONCEPT`（zhs「选择1张构想复制」/ eng「Choose 1 Concept to copy」）。
  手牌里没有构想时 `FromHand` 会直接返回空列表（`list.Count == 0` 分支），不会卡住。
- 重放写法照抄原版**重构 Transfigure** 的 `item.BaseReplayCount++`（Krafs.Publicizer 让 setter 可见）。
- 侧栏新增 `HoverTipFactory.Static(StaticHoverTip.ReplayStatic)` 解释重放。
  ⚠️ `HoverTipFactory.FromEnchantment<T>()` 返回的是 `IEnumerable<IHoverTip>`，写进集合要用 `..` 展开。

### 21.4 吃豆人！：模仿历史课（HistoryCourse）的复制品机制

用户要求：**先检测有没有诅咒牌** —— 有才打出疯狂进食（且不进弃牌堆/消耗堆，打完即消失），没有就直接给富足。

原实现是「先 `AutoPlay` 疯狂进食 → 再 `CardCmd.Exhaust` 它 → 再看有没有诅咒」，两个问题：
① 没诅咒时也白打一张；② 那张牌是自己 `Exhaust` 掉的，会进消耗堆。

新实现（`RemainingCards5.cs` 的 `PacManPower.AfterSideTurnStart`）：

```csharp
var curses = PileType.Hand.GetPile(player).Cards.Where(c => c.Type == CardType.Curse).ToList();
if (curses.Count == 0) { /* 直接给富足（+），return */ }
var frenzy = combatState.CreateCard(ModelDb.Card<FeedingFrenzy>(), player);
if (upgraded) CardCmd.Upgrade(frenzy);          // 先升级再复制，复制品才带 + 号
await CardCmd.AutoPlay(ctx, frenzy.CreateDupe(player), null);   // ← 关键
await CardCmd.Exhaust(ctx, 随机一张诅咒);
```

**为什么 `CreateDupe` 就能「不进任何牌堆」**（原版历史课的三步，实测成立）：
1. `CardModel.CreateDupe` 会把复制品的 `IsDupe` 置 true，并 `RemoveKeyword(Exhaust)`；
2. `CardModel.GetResultLocationForCardPlay()` 对 `IsDupe` 直接返回 `PileType.None`；
3. 打完由 `CardPileCmd.RemoveFromCombat(this)` 从战斗里删掉（`CardCmd.AutoPlay` 会先把无牌堆的卡放进 Play 堆，
   `RemoveFromCombat` 要求 `Pile.IsCombatPile`，Play 满足，不会抛）。

### 21.5 渔获 / 秒人斧：改成打出时立即移除（复制品不移除）

两张牌原来的 `GetResultLocationForCardPlay` 覆写里用的是 `TaskHelper.RunSafely(CardPileCmd.RemoveFromDeck(...))`
—— **fire-and-forget**。秒人斧砍死最后一名敌人时战斗立刻结束，这个后台任务可能来不及跑完。

改成在 `OnPlay` 里**先 await 掉移除、再结算伤害**：

```csharp
private async Task RemoveSelfFromDeck()
{
    if (IsClone) return;                                  // 复制品不移除
    var deckCard = DeckVersion;
    if (deckCard != null && deckCard.Pile?.Type == PileType.Deck)   // 不加这层保护 RemoveFromDeck 会抛
        await CardPileCmd.RemoveFromDeck(deckCard);
}
```

`IsClone`（= `CloneOf != null`，等价于 `IsDupe`）正好区分本尊与复制品。
`RemoveFromDeck` 内部会 `if (card.Pile.Type != PileType.Deck) throw`，所以要判 `Pile?.Type`。

### 21.6 相遇：墨影紫色 + 墨影侧栏

- 文本里的 `墨影小刀` 拆成 `[purple]墨影[/purple][gold]小刀[/gold]`（紫色 tag 是原版 `RichTextPurple`，参考原版**墨之刃**）。
- 侧栏加 `.. HoverTipFactory.FromEnchantment<Inky>()`（参考原版 `BladeOfInk` 的写法）。

### 21.7 文本改动清单（19 张卡 + 9 个能力侧栏；zhs + eng 同步）

| 卡 | 改动 |
|---|---|
| 双线叙事 | 全句重写（固有 / 重放 / 消耗） |
| 吃豆人！ | 「若你有诅咒牌…若你没有诅咒牌…」 |
| 渔获 / 秒人斧 | 「战斗结束时，」→「打出时，」 |
| 来自大师们的援助 / 来自骇客们的协助 / 来自C&C的援护 | 后两句用「，」连成一句 |
| 相遇 | 一句话化 + 墨影紫色 |
| 俄罗斯方块！ | 精简（去「溢出部分进入弃牌堆」「（10张）」「该效果不可叠加」） |
| 构想 | 抽牌 / 能量 / 活力三句用「，」连成一句 + 「在你的回合开始时」 |
| 连连看！ | 去掉「（无论是否升级）」 |
| 消消乐！ | 第 1 句去逗号、「张」、连成一段；升级仍是「更强的」 |
| 植物大战僵尸 | 连成一段；耗能改为「下次打出前变为 0」；升级仍是「升级过的」 |
| 绝地求生 | 主行 `{Cards:diff()}` / `{Energy:energyIcons()}` 显示最大值，括号显示实时值 + 「消耗。」 |
| 扫雷 | 「直接打出这张牌。」→「直接打出那张炸弹。」 |
| 大姐头 | 「复制出的牌」→「复制品」 |
| 火焰附加 | 改成「每有一次拥有火力的攻击造成伤害，就给予{Burn:diff()}层灼烧。」 |
| 见识下我的实力吧 | 「每打出10张牌」→「你每打出10张牌」 |
| 节奏游戏！/ 矛与盾 / 构想之盾 / 开发者协同：绿 / 角色扮演！/ 得道多助 / 跑酷！ | 「回合开始时 / 结束时」→「在你的回合开始时 / 结束时」 |

**绝地求生的实现细节**：`CalculatedVar.Calculate()` 在**非战斗状态直接返回 0**
（要 `CombatManager.Instance.IsInProgress && cardModel.CombatState != null` 才走 multiplier），
所以图鉴里它必然是 0 —— 不能当主行显示。新增静态 `DynamicVar("Cards", 4)` / `EnergyVar("Energy", 3)` 当主行，
`OnUpgrade` 里各 `UpgradeValueBy(1)`（5 / 4）。

**火焰附加**：用户给的两行文字都写「给予 1 层」会看不出升级，这里保留 `{Burn:diff()}` 占位符，
基牌显示 1、升级显示 2（本地化里两侧字符串完全一致）。

### 21.8 验证 & 产物

- `工作区/_scripts/_verify_batch9.py`：**50 条断言全绿**（本地化文本 + 代码特征 + 卡面体积）。
- `dotnet build` **0 错误**（38 个历史警告）→ DLL **427,520 → 428,544 B**、PCK **71,522,456 → 72,318,136 B**（10-11 16:28）。
- `工作区/_docs/_待做图标清单.md`：**42 个 power 图标**（A 共用占位 33 + B 借用火力图 3 + C 纯色小占位 6）
  + 遗物 8 + 药水 3；`KotamaStrengthPower` 继承原版临时力量图标**不需要做**；
  `images/powers/` 里另有 26 张已废弃占位可随手清掉。规格 **256×256 RGBA**。

### 21.9 环境提醒（重要）

本机 `python` 会命中 **WindowsApps 的 Store 占位程序**（静默退出、退出码 49）。
本批全部改用绝对路径：`C:\Users\asus\AppData\Local\Python\pythoncore-3.14-64\python.exe`。
另：`bash` 里用 `python - <<'PY'` 跑脚本时，**不要在命令行参数里传中文文件名**（会被转码搞坏），
改成脚本内 `os.listdir` / `glob` 取。

### 21.12 批次9d：衍生牌升级后「整个卡名」变绿 + 目录整理（2026-10-12）

#### （1）为什么只有那个「+」是绿的

绿色来自 `ShowIfUpgradedFormatter`（`Core/Localization/Formatters/ShowIfUpgradedFormatter.cs`）：

```csharp
case UpgradeDisplay.UpgradePreview:
    formattingInfo.Write("[green]");
    formattingInfo.FormatAsChild(format, ...);   // 只给**第一个分支的内容**套绿
    formattingInfo.Write("[/green]");
```

老写法 `[gold]名字{IfUpgraded:show:+}[/gold]` 把 `[gold]名字` 留在分支外、分支里只有「+」，
所以预览升级版时只有 + 号被染绿。

**统一改成**（第一个分支自带 `[green]`，保证 `Upgraded` 模式也是绿的；第二个分支保持金色，未升级时不变）：

```
{IfUpgraded:show:[green]名字+[/green]|[gold]名字[/gold]}
```

三种 `UpgradeDisplay` 模式都对：`Normal` → 金色名字；`Upgraded` → 绿色名字+；`UpgradePreview` → 绿色（同名标签嵌套仍为绿）。

覆盖 10 张（用户点名 9 张 + 同类漏网的「虚拟女仆武器！」）：

| 卡 | 变绿的衍生牌名 |
|---|---|
| 灵感爆发 | 我的回合！+ |
| 捕鱼达人！ | 渔获+ |
| 双刀王小桃 | 小刀+ |
| 打灰机！ | 燃料+ |
| LOSE！ | 创作的痛苦+ |
| 贪吃蛇 | 撕咬+ / 蛇咬+ / 火蛇怒咬+ |
| 扫雷 | 炸弹+（**只改「将1张炸弹+加入抽牌堆」那处**；「直接打出那张炸弹」没有升级含义，保持金色） |
| 愤怒的小鸟 | 愤怒+ / 异鸟扑击+ |
| 虚拟女仆武器！ | 当心误射！+（用户没点名，但写法完全一样，一并改了） |
| 来自时的援护 | 系统：阿比舒+ —— **这张原来写死了名字、连「+」都没有**。代码本来就 `if (IsUpgraded) CardCmd.Upgrade(abishu)`，只是文本没写，属纯文本修复 |

脚本 `工作区\_scripts\_update_batch9d_loc.py`（zhs + eng 各 13 处）。全库已无 `[gold]X{IfUpgraded:show:+}[/gold]` 老写法。

#### （2）设计 dump 与 xlsx 对齐（本来是脱节的）

`工作区\_design_dump.txt` 早已和 xlsx 脱节：**索引停在旧编号**（重整旗鼓 dump 里是 `[101]`，xlsx 实际第 94 项）、
dump 124 条 vs xlsx 134 条、dump 里还有 25 条是 xlsx 已改名的旧卡（来自琴里的援助 / 方块 / 对局复盘 / 火焰子弹 …）。

`工作区\_scripts\_sync_design_dump.py`：**以 xlsx 为唯一来源整份重建**，索引改用当前 `行号-3`，
旧 dump 备份到 `工作区\_backup\_dump_backup\`。现在 134 = 134 且逐条一致。

#### （3）目录整理

散在根目录的 19 个 `_build_*.log`、批次报告、脚本、json 快照全部归位（**只移动、不删除**）：

```
STS2 Momoi/                       ← 仓库根，现在只剩 4 个条目
  STS2_Momoi_迁移文档.md           ← 唯一权威交接文档
  research.md  STS2 Momoi.sln  _archive/
  _archive/
    build_logs/     _build_*.log（19 个）
    batch_reports/  _apply_batch*_report.json、_batch*_contact_sheet.jpg、_check_titfortat.jpg
    old_docs/       旧版移交文档副本（项目里那份 76KB 的）
    move_manifest_*.txt  本次移动清单
  STS2 Momoi/                     ← 工程
    _tools/         _patch_*.py、_verify6.py、_xlsx_update7.py、_fix_batch_a.py、_art_map.json
  工作区/
    STS2Momoi.xlsx                ← 权威设计表（不动）
    _design_dump.txt              ← 设计快照（与 xlsx 同步）
    _scripts/   所有 *.py（26 个）
    _data/      _card_art_status.*、_power_icon_inventory.json、_cards_full.json、
                _idx_*.json、_relic_potion_dump.txt、_xlsx_dump.json、_card_index.txt …
    _docs/      _待做图标清单.md、旧版工作区移交文档
    _backup/    _xlsx_backup/、_dump_backup/、_cardart_backup9/
    _session_export/ _session_export2/
    卡面成品区/ 卡面成品7/ 卡面成品8/ 参考图集/ 编辑区/ 已删卡_备份/ 美术准备/
    标准卡面画布.psd  工程文件.lnk
```

- 脚本里的输出路径已同步改到新位置（`_regen_art_status.py` → `工作区\_data\`、
  `_icon_inventory.py` / `_index_cards.py` → `工作区\_data\`、`_sync_design_dump.py` → `工作区\_backup\_dump_backup\`、
  各 `_update_batch*_tables.py` → `工作区\_backup\_xlsx_backup\`），改完逐个复跑验证过。
- 本文档里的路径引用一并更新（15 处）。
- `.gitignore` 已忽略 `bin/`、`obj/`、`.godot/`、`*.log`、`*.uid`、`*.import`；最大的一块是 `.godot/`（**137 MB** 缓存，删了下次构建会重建，按需处理）。
- 本次**只移动不删除**；移动清单见 `_archive\move_manifest_*.txt`，要还原照着反着搬即可。

#### 产物

- `dotnet build` **0 错误** → DLL **430,080 B**、PCK **72,319,324 B**（10-12 06:09）。
- `工作区\_scripts\_verify_batch9.py` 仍 **64 条全绿**；`_regen_art_status.py` 复跑 **133/133 真实成品**；
  `_sync_design_dump.py --dry` 显示与 xlsx **零差异**。

### 21.13 批次10：成品图全量接入 + 废弃 power 清理 + 人物战斗模型管线（2026-10-13）

#### （1）接入的成品图（脚本 `工作区\_scripts\_apply_batch10_art.py`，61 个文件）

| 来源目录 | 落地位置 | 数量 |
|---|---|---|
| `工作区\卡面修改1\` | `images/cards/DualNarrative.png` | 1 |
| `工作区\power图标成品\` | `images/powers/*.png`（256×256） | 48 |
| `工作区\遗物成品区\` | `images/relics/{类名}.png` | 9 |
| `工作区\药水成品区\` | `images/potions/{类名}.png` | 3 |

power 图标里包含 **4 张原来共用的图被拆分**（`fell_to_second_tier_power` / `spear_shield_power` /
`role_play_power` / `my_turn_power`）+ **1 张改名**（`taunt_power.png` → `win_energy_power.png`），
对应 C# 里 5 处 `IconPath` 已同步改：
`RemainingCards2.cs:781`(FellToSecondTierPower)、`ConceptFlowCards.cs:574`(SpearShieldPower)、
`MultiplayerCards.cs:75`(RolePlayPower)、`RemainingCards3.cs:1153`(MyTurnPower)、
`RemainingSpecialCards.cs:574`(WinEnergyPower)。

#### （2）改名：活学活用 → 日复一日，必有精进

卡牌名（`cards.json`）与 xlsx/设计 dump 早已是「日复一日，必有精进」，
但 **power 的 `title` 还停在「活学活用 / Learn by Doing」** —— 已改 `localization/{zhs,eng}/powers.json`
+ `RemainingSpecialCards.cs` 里的注释。类名 `LearnByDoingPower` 与 ID 保持不变（改 ID 会丢存档引用）。

#### （3）删除废弃 power（脚本 `工作区\_scripts\_batch10b.py`）

共 **27 张图标 + 10 个本地化词条** 分两步清理：

- `_cleanup_dead.py`：27 个无任何引用的 power 图标（+`.import`）+ 4 个孤儿词条
  （`TAUNT_POWER` / `CNC_TRACKER_POWER` / `COURAGE_BOON_POWER` / `ONE_SHOT_AXE_REMOVAL_POWER`）。
- `_batch10b.py`：**`MomentumBreakPower`（破势的 power）**。它是旧实现的遗留 ——
  伤害倍数后来内联进了卡牌自己的 `ModifyDamageMultiplicative`，power 再没有任何代码去 `Apply`，
  属于死代码。已删类（`RemainingCards2.cs` 第 115~173 行）+ 图标 + `powers.json` 6 个词条。
  **卡牌本身的行为完全不变。**

> 排查方法：对每个 `[RegisterPower]` 类名全文搜索，只有它在属性里出现一次 = 没人用。
> 53 个 power 类里只有 `MomentumBreakPower` 命中；`KotamaStrengthPower` 继承原版图标（`icon: None`）不算缺失。

#### （4）美味饼干接入 `VanillaRelicVisualOverrides`（`_batch10c.py`）

`工作区\遗物成品区\美味饼干_王小桃.png` 一直没有对应遗物类 —— 因为「美味饼干」是**原版遗物**
（`YUMMY_COOKIE`，先古稀有度），它的 `IconBaseName` 是写死的 if-else：

```csharp
// src/Core/Models/Relics/YummyCookie.cs
if (characterModel is Defect) return "yummy_cookie_defect";
return "yummy_cookie_ironclad";   // ← 小桃会落到这里，显示铁甲战士那版
```

所以必须走 RitsuLib 的按角色覆盖接口，现已接入：

```csharp
VanillaRelicVisualOverrides:
[
    new(CharacterOwnedVanillaRelicModelId.YummyCookie, new RelicAssetProfile(
        IconPath:        $"{RelicRoot}/YummyCookie_Momoi.png",
        IconOutlinePath: $"{RelicRoot}/YummyCookie_Momoi_outline.png",
        BigIconPath:     $"{RelicRoot}/YummyCookie_Momoi.png"))
]
```

#### （5）遗物轮廓图修正（`_batch10c.py`）

原来 9 个自建遗物的 `IconOutlinePath` 直接指向**彩色原图**，而原版的轮廓图是**纯白剪影**
（对比 `参考图集/images/atlases/relic_outline_atlas.sprites/yummy_cookie_ironclad.tres` 证实）。
已用「alpha 阈值 + 边界洪水填充补洞」批量生成 `{类名}_outline.png`（10 张，含美味饼干），
`DriedInspiration.cs` + `MoreRelics.cs` 共 9 处 `IconOutlinePath` 改为 `_outline.png`。

#### （6）人物战斗模型管线（`_batch10d.py`）

**问题**：`STS2 MomoiCharacter.CharacterScenePath` 一直指向
`res://scenes/creature_visuals/ironclad.tscn` —— **进战斗站着的是原版铁甲战士**。

**改法**（RitsuLib 非 Spine 方案，教程 04-15-2）：

```csharp
private const string CharacterScenePath = $"{SceneRoot}/STS2_Momoi_character.tscn";
...
VisualCues: ModVisualCues.CueSet()
    .Single("idle",    $"{CueRoot}/idle.png")
    .Single("attack",  $"{CueRoot}/attack.png")
    .Single("cast",    $"{CueRoot}/cast.png")
    .Single("hit",     $"{CueRoot}/hit.png")
    .Single("dead",    $"{CueRoot}/dead.png")
    .Single("relaxed", $"{CueRoot}/relaxed.png")
    .Build(),
```

- 场景 `STS2_Momoi_character.tscn` 重写：`Visuals(Sprite2D, pos(0,-246) scale 0.6) / Bounds / IntentPos / CenterPos / TalkPos`。
- cue 图放 `images/characters/cue/`，当前 **6 张都是同一张占位图** ——
  从 `images/cards/DualBladeMomoi.png`（线稿卡面）用连通域分析抠出的半身像，贴到 600×820 透明画布、底边对齐。
- 覆盖同名文件 → `dotnet build` 即可看到效果，**不用碰 Godot 编辑器**。目录里有 `README.md` 说明。
- 多帧动画改用 `.Sequence("attack", seq => seq.Frame(p1, 0.06f)...)`。
- 未覆盖状态机（`SetupCustomCombatAnimationStateMachine` / `StandardCue`）—— 教程首要示例只需 `VisualCues`，
  若日后发现动作不触发再加。

#### （7）重要结论：人物相关素材**全是铁甲战士的占位图**

模组是从模板复制的，模板的人物素材就是铁甲战士那一套，从来没换过。实测确认：

`character_icon(88×88)` / `character_icon_outline` / `character_select(132×195)` /
`character_select_locked` / `map_marker(49×64)` / `energy_orb_layer_1..5` /
`energy_big` / `energy_text` —— **全部是铁甲战士的头盔、红色 V 形标记、红色能量球**；
`character_select_bg.tscn` 是「纯色 Rect + 这两张铁甲战士图」；
`merchant.tscn` / `rest_site.tscn` 直接复用那张 132×195 的面罩。

待补清单见 `工作区\_docs\_美术待补清单.md`（按 RitsuLib `CharacterAssetProfile` 官方 42 个字段逐项列的）。

#### 产物

- `dotnet build` **0 错误** → DLL **431,104 B**、PCK **75,368,540 B**（10-13 20:04）。
- 资源自检：代码里 49 条写死路径**无缺失**；卡 133/133、power 47 文件/53 类（5 个升级变体共用 + 1 个继承原版）、
  遗物 9 类各带轮廓图、药水 3、cue 6。
- 备份：`工作区\_backup\batch10_pre`（被覆盖的图）、`batch10_dead`（删掉的图标/词条）、
  `batch10b_dead`、`batch10c_pre`（改了轮廓路径的 2 个 .cs）、`batch10d_pre`（旧 tscn）。

### 21.14 批次11：遗物/药水描述染色与侧栏 + 诅咒红字 + 桃味气泡水贴图修复（2026-10-13）

#### （1）原版颜色惯例（全部实测自 `游戏目录/localization/{zhs,eng}`）

| 标记 | 用途 | 原版实例 |
|---|---|---|
| `[gold]` | 关键词 / 牌堆 / 手牌 / 升级 / 消耗 / 保留 / 变化 / 金币 / 休息处 / 商店房间 / 力量 | `DARKSTONE_PERIAPT`、`MEAL_TICKET`、`ETERNAL_FEATHER` |
| `[blue]` | 数值（含最大生命值提升量、金币门槛、张数） | `BLOOD_SOAKED_ROSE.description` 的 `[blue]1[/blue]` |
| `[green]` | 回血数值、升级后的衍生牌名 | `BLOOD_VIAL` 的 `[green]{Heal}[/green]` |
| `[red]` | 诅咒 / 诅咒牌名 / 遗物未揭晓 flavor | `BLOOD_SOAKED_ROSE` 的 `[red]执迷[/red]`、`[red]这个遗物的细节将在未来揭晓……[/red]` |

#### （2）🔴 桃味气泡水贴图不显示 —— 根因：**类里根本没写 `AssetProfile`**

```csharp
// 修复前
public sealed class PeachSoda : ModPotionTemplate
{
    public override PotionRarity Rarity => PotionRarity.Rare;
    public override PotionUsage Usage => PotionUsage.CombatOnly;
    public override TargetType TargetType => TargetType.Self;
    protected override async Task OnUse(...)   // ← 直接从这里开始，没有 AssetProfile
```

RitsuLib 找不到资源路径就走占位贴图 —— 这就是用户看到的「nope」小图标。
**顺带把所有注册类做了一遍全量扫描（133 卡 / 53 能力 / 9 遗物 / 3 药水），只有这一个漏网。**

同时把三个药水的 `OutlinePath` 从「彩色原图」改成真正的**白色剪影**（原版 `potion_outline_atlas` 证实是纯白剪影）：
`NPotion.cs` 里 `Outline` 是 `show_behind_parent` + `modulate=(0,0,0,0.5)` 的**背衬层**，
`NLabPotionHolder` 还会把它按 `halfTransparentWhite` 显示——用彩图当轮廓在药水实验室的「未发现」状态会显示成彩色鬼影。
现在 `images/potions/{InstantCoffee,PeachSoda,StrawberryMilk}_outline.png` 由脚本生成（alpha 阈值 + 边界洪水填充补洞）。

#### （3）遗物 / 药水侧栏

新增 `STS2 MomoiCode/Tips/MomoiSidebarTips.cs` 作为统一入口（`ModRelicTemplate.AdditionalHoverTips` /
`ModPotionTemplate.AdditionalHoverTips`，两者在 RitsuLib 里都 `<inheritdoc/>` 了 `ExtraHoverTips`）：

| 侧栏 | 来源 |
|---|---|
| 小游戏牌 | `LocString("cards", "STS2_MOMOI_MINIGAME_KEYWORD_SIDEBAR.*")`（与卡牌那边同一套键） |
| 消耗 / 保留 | `HoverTipFactory.FromKeyword(CardKeyword.Exhaust / Retain)` |
| 变化 | `HoverTipFactory.Static(StaticHoverTip.Transform)`（读 `static_hover_tips.json` 的 `TRANSFORM`） |
| 力量 | `HoverTipFactory.FromPower<StrengthPower>()` |
| 构想 / 构想+ | `HoverTipFactory.FromCard<ConceptCard>()` / `FromCard<ConceptCard>(upgrade: true)` |

> 注意：`Patches/MinigameSidebarPatch.cs` 的自动关键词侧栏只挂在 `ModCardTemplate.get_ExtraHoverTips`
> 上，**遗物和药水拿不到**，必须自己写。

#### （4）没吃完的薯片：新增商店房间触发

参考原版餐券 `RelicModel.AfterRoomEntered` + `room is MerchantRoom`：

```csharp
public override async Task AfterRoomEntered(AbstractRoom room)
{
    var player = Owner;
    if (player == null || room is not (RestSiteRoom or MerchantRoom)) return;
    var amount = player.Gold / 50;
    if (amount > 0) { Flash(); await CreatureCmd.GainMaxHp(player.Creature, amount); }
}
```
（原来是 `BeforeRoomEntered` + 只认 `RestSiteRoom`。）

#### （5）文本改动汇总（`工作区\_scripts\_batch11_text.py`，共 74 条）

- **9 个遗物 flavor** 全部换成原版那句红色「这个遗物的细节将在未来揭晓……」（原来只有枯竭灵感有一句自写的）。
- **9 个遗物描述**：按上表染色；其中 4 条按用户给的新文案逐字替换
  （薯片 / 旧游戏机 / 胜利的剧本 / 绿色挂饰 / 镜子）。
- **3 个药水描述**：速溶咖啡（构想金 / 睡眠不佳红）、草莓牛奶（7、1 蓝 / 力量金）、
  桃味气泡水（`将你[gold]手牌[/gold]中的任意张牌[gold]变化[/gold]为随机[gold]小游戏牌[/gold]。` —— 去掉标记后与要求原文一字不差）。
- **捕鱼达人！** 删掉多余的「对1名敌人 / to an enemy」。
- **诅咒红字**：卡牌表 + 能力表里所有「诅咒」「Curse」以及 16 个原版诅咒牌名的裸词全部包上 `[red]`
  （含 `CONCEPT_CARD.sidebarCurse` / `GRINDING.sidebar` 两条侧栏，以及吃豆人 power 的侧栏）。
  全表复扫：**漏网 0 条**。

#### （6）power 图标自测（用户要求「不应该有 nope 的图标」）

对 47 个图标文件与 52 个 `[RegisterPower]` 类做了三重核对：
引用路径无缺失 ✅、无孤儿文件 ✅、无单色/近纯色占位图（按 RGB 标准差 + 唯一色数筛）✅；并肉眼过了一遍 47 张总览图。

#### 产物

- `dotnet build` **0 错误** → DLL **432,128 B**、PCK **75,376,152 B**（10-13 21:51）。
- 自检：`_verify_batch11.py` **102 条全绿**；`_verify_batch9.py` **64 条全绿**（其中吃豆人文本断言已同步更新）。
- 备份：`工作区\_backup\batch11_pre`（6 个本地化 json）。

### 21.15 批次12：power 全面规范化 + 花凛重做 + 三大 bug 定位（2026-10-14）

#### （1）🔴「我复活啦！」一张牌能挡两次致死攻击 —— 根因

`Hook.ShouldDie` 遍历 `runState.IterateHookListeners(combatState)`，而 `RunState.IterateHookListeners`
会**先遍历牌组卡（`player.Deck.Cards`）、再遍历 `CombatState.IterateHookListeners()`（战斗中的卡）**，
并且只把**第一个**返回 false 的对象记为 `preventer` 去调 `AfterPreventingDeath`。

所以牌组本体与局内副本是**两个不同实例、各有各的 `_used` 字段**：

| 死亡次数 | 谁拦下的 | 结果 |
|---|---|---|
| 第 1 次 | 牌组本体（`_used = true`） | 挡下 |
| 第 2 次 | 本体 `_used` 已 true → 轮到局内副本（副本的 `_used` 还是 false） | 又挡下 |
| 第 3 次 | 两个都 true | 才死 |

**修复**：把标记统一存在**牌组本体**上，副本通过 `DeckVersion` 读写同一份：

```csharp
private ImBack Root => DeckVersion as ImBack ?? this;
private bool Used { get => Root._used; set => Root._used = value; }
public override bool ShouldDieLate(Creature creature) => creature != Owner.Creature || Used;
```

#### （2）🔴 桃味气泡水式问题的普适教训：注册类必须写 AssetProfile

批次11 已修，这里只记结论：**任何 `[Register*]` 类漏写 AssetProfile 就会显示占位图**。
批次12 又发现一处类似的 —— **注能附魔贴图**.

`EnchantmentModel.IconPath` 的取值链路是写死的：

```csharp
public string IconPath => ResourceLoader.Exists(IntendedIconPath) ? IntendedIconPath
                        : (ResourceLoader.Exists(BetaIconPath) ? BetaIconPath : MissingIconPath);
public string IntendedIconPath => ImageHelper.GetImagePath("enchantments/" + Id.Entry.ToLowerInvariant() + ".png");
// → res://images/enchantments/{entry小写}.png
```

`MomoiImbued` 是直接继承 `EnchantmentModel`（不是 `ModEnchantmentTemplate`），**没有可覆写的 AssetProfile**，
所以只能按 ID 补图。本地化键是 `MOMOI_IMBUED.title` → entry 即 `MOMOI_IMBUED`
→ 应有 `res://images/enchantments/momoi_imbued.png`。
已从 `工作区\参考图集\images\enchantments\imbued.png` 复制过去（并额外放了两个可能的 ID 变体名做保险）。

#### （3）「雷酱」炮台支援（`YoshimiRepeatPower`）重做

| 需求 | 实现 |
|---|---|
| 每个 power 独立存在 | `InstanceType = PowerInstanceType.Instanced`（**`FindExistingInstanceForStacking` 对 Instanced 直接返回 null**，永远新建实例） |
| 计数显示剩余回合数 | `StackType = Counter`，施加时 `amount = 卡面 Turns`；`DisplayAmount => Amount`；每回合末 `PowerCmd.TickDownDuration(this)` |
| 文本里的「几」是实际值 | `接下来的[blue]{Amount}[/blue]个回合结束时…` |
| 数值取自**卡面**而非实际伤害 | 施加时从 `MomoiSupportYoshimi.FaceBlock/FaceDamage` 快照（读 `DynamicVars.Block.PreviewValue` / `CalculatedDamage.PreviewValue`） |
| 伤害/格挡不受力量·敏捷·虚弱·脆弱 | 攻击加 `.Unpowered()`（= `Move \| Unpowered`），格挡用 `ValueProp.Unpowered \| ValueProp.Move` |
| 但吃活力与易伤 | 原版 `VigorPower`/`VulnerablePower` 都以 `props.IsPoweredAttack()`（= 有 Move 且**无** Unpowered）为门槛，所以 Unpowered 会把它们一起挡掉；本能力自己实现 `ModifyDamageAdditive`（+活力）与 `ModifyDamageMultiplicative`（×1.5 易伤），并用 `_inRepeatAttack` 把自己的修正限定在这一次重复攻击上，攻击后 `PowerCmd.ModifyAmount` 扣掉活力 |

顺带：**打灰机！/ 来自大师的援助** 的卡面格挡原本 `new DynamicVar("Block", N)` + 手搓 `new BlockVar(BaseValue, Move)`，
卡面数字不走 `Hook.ModifyBlock` → 显示的永远是不含敏捷的值。改成 `new BlockVar(N, ValueProp.Move)` +
`CreatureCmd.GainBlock(..., DynamicVars.Block, ...)`（原版 `Armaments`/`Backflip` 的写法）后卡面会实时显示正确数值。

#### （4）构想局内数值变绿

原版 `HighlightDifferencesFormatter`（`{X:diff()}`）与 `EnergyIconsFormatter` 都靠
`DynamicVar.ToHighlightedString`：**比较 `PreviewValue` 与 `EnchantedValue`**，大才染绿；
`EnergyIconsFormatter` 还规定 **1~3 直接堆叠图标（无数字），4 及以上才出数字**。

所以修法是在 `ConceptCounterCapability.SyncDisplayVars` 里 **`BaseValue = 0`（连带重置 EnchantedValue），只写 `PreviewValue = Count`**：

```csharp
foreach (var name in new[] { "ConceptCount", "ConceptDraw", "Energy", "ConceptVigor" })
{
    var v = card.DynamicVars[name];
    v.BaseValue = 0;
    v.PreviewValue = Count;
}
```

数值 0 → 两者相等 → 白色；≥1 → 绿色；能量 1~3 无数字、4+ 才出绿数字。

#### （5）隐藏纯记录用 power

原版 `PowerModel.IsVisibleInternal`（`AmbergrisPower` 就是 `false`）。
`AssistTrackerPowerBase` / `AssistTrackerPowerBase2` 各加一句
`protected override bool IsVisibleInternal => false;` → C&C援护进度 / 工程部的援助 / 真理部的协助不再显示。

#### （6）幸运儿的祝福（`AsunaGuardPower`）

- `StackType: Single → Counter`（叠层数 = 持续回合数），`DisplayAmount => Amount`，回合末 `TickDownDuration`
- 减伤百分比不叠加：`ApplySource` 里 `if (upgraded || !data.Upgraded)` —— **升级的 40% 覆盖 25%，25% 覆盖不了 40%**
- 卡牌侧删掉原先「已有则 Remove 再 Apply」的手搓逻辑，直接 `Apply(amount: 1)`
- 文本改成巨像式：`[blue]{Amount}[/blue]回合内，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。`

#### （7）来自花凛的援护：删 power，改 Boss 增伤牌

`KarinFinishPower` 整个删除（图标 + `powers.json` 6 个词条一并清理）。
卡牌改为 **2 费攻击·衍生·支援牌**：`CalculationBaseVar(36)`（升级 44）+ `DynamicVar("BossPct", 50)`（升级 75），
Boss 增伤走 `ModifyDamageMultiplicative` + `CombatRoomHelper.GetCombatRoom(Owner).RoomType == RoomType.Boss`
（与渔获同一套判定）。

#### （8）右下角计数语义（`PowerModel.DisplayAmount`）

| power | 改成 |
|---|---|
| 构想之矛 | `=> DamagePer`（对所有敌人造成的伤害） |
| 构想之盾 | `=> BlockPer`（实际获得的格挡） |
| 火焰附加 | `=> BurnAmount`（被击中敌人拿到的灼烧层数） |
| 矛与盾 | **不改**（仍是叠加层数） |
| 重整旗鼓 | `=> PendingHeal`（现算的即将回复量） |

#### （9）重整旗鼓实时数值

按“显示层与数据层解耦”的原版做法（`HardenedShellPower` / `FeralPower`）：

```csharp
public override int DisplayAmount => PendingHeal;                      // 每次读取现算
public override Task AfterCurrentHpChanged(Creature c, decimal d)      // 挨打/回血立即刷新
{ if (c == Owner) RefreshDisplayVars(); return Task.CompletedTask; }
public override Task AfterApplied(...) { Owner.MaxHpChanged += OnOwnerMaxHpChanged; ... }
public override Task AfterRemoved(Creature oldOwner) { oldOwner.MaxHpChanged -= OnOwnerMaxHpChanged; ... }
```

> 注意 `PowerModel.AfterRemoved` 的签名是 `AfterRemoved(Creature oldOwner)`，不是无参。

#### （10）power 文本全面规范化（`_batch12_text.py`，179 条）

- 数字（含百分比/张数/层数/回合数）→ `[blue]N[/blue]`；回血数值 → `[green]`；关键词 → `[gold]`
- 全表复扫：power 描述里**裸数字 0 条**、富文本标签**全部成对**
- 「恢复」→「回复」（重整旗鼓卡牌 + power 文本）
- 吃豆人卡牌/power 的「消耗」→ `[gold]消耗[/gold]`（卡牌会由 `MinigameSidebarPatch` 自动补上消耗侧栏）

#### 产物

- `dotnet build` **0 错误** → DLL **432,128 B**、PCK **75,381,676 B**（10-14 01:00）。
- 自检：`_verify_batch12.py` **51 条全绿**、`_verify_batch11.py` **102 条全绿**、`_verify_batch9.py` **64 条全绿**。
- 备份：`工作区\_backup\batch12_pre`（4 个本地化 json + 花凛 power 图标）。

### 21.16 批次13：火力/活力、俄罗斯方块、我复活啦、构想数值、Boss 判定（2026-10-14）

#### （1）🔴「雷酱」炮台支援突破了火力拦截吃活力 —— 根因

模组的火力规则是**挂在 `VigorPower.AfterAttack` 上的 Patch**（`VigorConsumePatch`）：

```csharp
// Patches/VigorFirepowerPatch.cs
[new(typeof(VigorPower), nameof(VigorPower.AfterAttack))]
Prefix(...) { 有火力 → 扣 1 层火力，跳过原方法（活力保留）; 否则走原版（活力正常消耗） }
```

也就是说：**只有经过 `AttackCommand` 的活力消耗才会被拦截**。
而「雷酱」的重复攻击为了绕开力量/虚弱，加了 `.Unpowered()`（`VigorPower.BeforeAttack/AfterAttack` 都以
`props.IsPoweredAttack()` 为门槛，跳过了），于是原版消耗路径整条都没走；
我又在攻击后**自己**调了 `PowerCmd.ModifyAmount(vigor, -n)` —— 直接绕过火力把活力吃掉了。

**修复**：把「有火力就扣火力、没火力才扣活力」抽成一个统一入口，谁都不能自己扣活力：

```csharp
// FirepowerHooks.SpendVigorAsync(ctx, owner, vigorAmount)
if (owner.GetPower<FirepowerPower>() is { Amount: > 0 } fp) { 扣 1 层火力; return; }
if (vigorAmount > 0 && owner.GetPower<VigorPower>() is { } v) { 扣 v 层活力; }
```

**全模组排查结论**：只有「雷酱」这一处手动扣活力（已改）。其余回合结束造成伤害的 power 都走正常的
`DamageCmd.Attack(...).FromCard(...)`（没有 `.Unpowered()`），活力/火力由原版 + Patch 处理，所以
**矛与盾、节奏游戏都不会出这个问题** —— 与用户实测一致。

#### （2）🔴「我复活啦！」没进消耗牌堆 —— 根因：牌堆搬动发生在回血之前

`AfterPreventingDeath` 触发时玩家 `CurrentHp == 0`，而 `Creature.IsDead => CurrentHp <= 0`。
`CardPileCmd.Add` 里有这道守卫：

```csharp
if (card3.HasBeenRemovedFromState || creature.IsDead || (card3.IsInCombat && creature.CombatState == null))
{
    return ... success = false;   // 静默失败
}
```

原顺序是「先消耗副本 → 再移除牌组本尊 → 再回血」，所以消耗那一步被静默丢掉；
而 `CardPileCmd.RemoveFromDeck` 没有这道守卫，所以牌组移除照常生效 —— 症状正好是
「牌组里没了、局内没进消耗堆、还能再打」。

**修复**：把回血提到最前面，顺序改成 **回血 → 消耗局内副本 → 移除牌组本尊 → 给再生**。

#### （3）🔴 构想卡面数值恒为 0 —— 根因：PreviewValue 每次渲染前会被清掉

`NCard.UpdateText` 渲染前一定会：

```csharp
Model.DynamicVars.ClearPreview();                 // → 每个 var 都 ResetToBase()，PreviewValue 打回 BaseValue
Model.UpdateDynamicVarPreview(previewMode, target, Model.DynamicVars);   // 之后才跑各 var 的 UpdateCardPreview
```

所以在别处写 `PreviewValue` 会被冲掉。**必须像原版 `BlockVar` / `CalculatedDamageVar` 那样，
在自己的 `UpdateCardPreview` 里赋值**：

```csharp
public sealed class ConceptCountVar : DynamicVar          // ConceptEnergyVar : EnergyVar 同理
{
    public override void UpdateCardPreview(CardModel card, CardPreviewMode previewMode, Creature? target, bool runGlobalHooks)
        => PreviewValue = card.TryGetCapability<ConceptCounterCapability>(out var c) ? c.Count : 0;
}
```

`BaseValue` 保持 0 → `ToHighlightedString` 比较 `PreviewValue` 与 `EnchantedValue(=0)`
→ 0 白、≥1 绿；能量 1~3 堆叠图标、4+ 出绿数字。

#### （4）俄罗斯方块（满手牌结算）

- **同档位覆盖**：`TetrisFullHandPower.RemoveSameTier(player, IsUpgraded)` 在打出时先移除同档位的旧实例
  → 一张俄罗斯方块最多对应一个结算 buff。
- **升级版优先结算**：`ResolveOneToSettle(player)` 取「有升级版就取升级版，否则取非升级版」；
  两个实例都会收到 `AfterCardChangedPiles`，但只有被选中的那个真的 `Settle()`（无论两张的打出顺序）。
- **本回合打出过的俄罗斯方块全部消耗**：`Settle` 里改成扫 `Play + Discard` 两堆（手上的一开始就随
  「消耗所有手牌」带走），不再只处理传进来的那一张。
- **文本**：补 `DynamicVar("Cards", 3)` 与 `EnergyVar("Energy", 2)`，
  描述从「抽牌，获得能量」改成「抽[blue]{Cards}[/blue]张牌，获得{Energy:energyIcons()}」。

#### （5）来自花凛的援护：爪牙不该吃 Boss 增伤

游戏里**没有「Boss」这个怪物标记**（`IsBoss`/`IsElite` 都搜不到）。原版 Pantograph 的写法是房间层级：
`RunState.CurrentRoom.RoomType == RoomType.Boss`。
但同族小队（TheKinBoss）骨架会把两个 `KinFollower` 爪牙也放进 Boss 房间，它们挂的是 `MinionPower`
→ `IsPrimaryEnemy == false`。所以再加一条目标判定：

```csharp
if (cardSource != this || target == null || !InBossRoom() || !target.IsPrimaryEnemy) return 1m;
```

帝皇蟹的 Crusher / Rocket **都没挂 MinionPower**，两个部位都是 primary enemy，照常吃增伤，不需要白名单。

#### （6）循环叙事改为可叠加

`StackType: Single → Counter`（层数 = 剩余持续回合数），`DisplayAmount => Amount`，
回合末 `PowerCmd.TickDownDuration(this)`；文本改为
「接下来的[blue]{Amount}[/blue]个回合结束时，将本回合所有进入过[gold]弃牌堆[/gold]的牌洗入[gold]抽牌堆[/gold]。」
> 顺手修掉一个自己引入的 bug：编辑时留下了**两个 `[RegisterPower]` 特性**，已删掉重复的那个。

#### （7）植物大战僵尸 power 显示实际卡名

`PlantsNextTurnPower` 加 `StringVar("Card")`，在 `SetOtherCard` 里写 `other.Title`
→ 描述从「另一张牌」变成「下回合将[gold]{Card}[/gold]加入你的[gold]手牌[/gold]。」
（升级版会带 `+`，因为取的是那张升级后实例的 Title）。

#### （8）新增：`工作区\_docs\_power总览.md`

用户要求的「所有 power 的文本 + 能否叠加 + 怎么叠加」总览，**由脚本从源码自动生成**：
`工作区\_scripts\_power_overview.py` → 扫描 `[RegisterPower]` 类，抽
`StackType` / `InstanceType` / `DisplayAmount` / `IsVisibleInternal`（**含基类继承解析**，
如 `DualBladeMomoiUpgradedPower : DualBladeMomoiPower`），再叠加脚本里人工写好的「叠加语义」表。

#### 产物

- `dotnet build` **0 错误** → DLL **435,200 B**、PCK **75,382,252 B**（10-14 03:27）。
- 自检：`_verify_batch13.py` **32 条全绿**，加上 batch9/11/12 共 **250 条断言全绿**。
- 备份：`工作区\_backup\batch13_pre`（powers.json / cards.json）。

### 21.17 批次14：power 右下角语义统一 + 贪吃蛇/跑酷拆分（2026-10-14）

#### （1）知识：`DisplayAmount` 到底谁在显示

`PowerModel.DisplayAmount` 默认 `=> Amount`，UI 只在 `InvokeDisplayAmountChanged()` 时重读。
凡是不想显示「叠加层数」而是要显示「实际生效数值」的，都要 override 并在数值变化时手动 `InvokeDisplayAmountChanged()`。

本批把右下角语义逐个对齐：

| power | 右下角改成 | 实现 |
|---|---|---|
| 掉到二档了。。。 | 这次实际给的金币数 | `=> GetInternalData<Data>().Gold` |
| 游戏王形态 | 实际获得的缓冲层数 | `=> DynamicVars["BufferPer"].BaseValue` |
| 开发秘籍 | 实际数值增量（Gain） | `=> DynamicVars["Gain"].BaseValue` |
| 双刀王小桃 | 每次添加的小刀张数 | `=> Amount`（与叠加层数本就同一个数） |
| 开发者协同：绿 | 回合开始时获得的活力 | `=> Amount`（同上） |
| 扫雷 | 还剩几次自动打出炸弹 | `=> Amount` |
| 额外回合 | 剩余额外回合数 | `=> Amount` |
| 终于上一档了！ | 剩余回合数（**文档写错了，代码本来没问题**） | `=> Amount`（默认） |

> 「专注」复核后确认无需调整：**保留张数只看构想数值**（多张构想取最大值，`GetMaxCountInHand`），
> power 的层数只叠加「构想数值 +N」这一项。

#### （2）扫雷（MinesweeperPower）

本身已经是 `StackType.Counter` + 每次触发 `Decrement`，本批只补 `DisplayAmount => Amount` 与文本：
「当你下[blue]{Amount}[/blue]次抽到[gold]炸弹[/gold]时，将其直接打出。」；卡牌文本里的 `1` 也补成蓝色。

#### （3）满手牌结算：升级版额外覆盖普通版

```csharp
// RemoveSameTier → RemoveOverridden
if (upgraded || !existing.Upgraded)   // 升级版覆盖全部；普通版只覆盖普通版
```
所以一个玩家身上最多同时存在**一个**该 buff，且升级版一定会把普通版顶掉。

#### （4）能量保留（WinEnergyPower）改为可叠加

这里有个必须绕过的坑：`CardPileCmd.Add` / `PowerModel.ShouldRemoveDueToAmount()` 都是**非虚**的，
0 层时会自动移除，而「能量保留」恰恰需要在 0 层时**再活一会儿** —— 它靠 `ShouldPlayerResetEnergy`
去拦下个回合开始时的能量重置。

所以：
* `StackType => Counter`，层数 = 剩余生效回合数，`DisplayAmount => Amount`；
* **回合结束** `SetAmount(Math.Max(0, Amount - 1))`（用 `SetAmount` 而不是 `TickDownDuration`，后者会顺手把 0 层删掉）；
* **回合开始** 先让 `ShouldPlayerResetEnergy` 拦住这一轮重置，再看 `Amount <= 0` 就 `PowerCmd.Remove`。

否则「1 层」的时候会在回合结束被删掉，下回合开始时能量照样清空 —— 效果等于没有。

#### （5）贪吃蛇 / 跑酷：拆成升级前、升级后两个 power

两个都用「抽象基类 + 两个 `[RegisterPower]` 子类」的写法（`SnakeGamePowerBase` / `ParkourPowerBase`），
基类里 `InstanceType = Instanced`、`StackType = Single`：

* **贪吃蛇**：卡在生成那三张牌之后调用 `power.Track(created)`；power 只随机化**自己那份列表里、且还在手牌中**的牌
  → 多张贪吃蛇各管各的、升级版管升级牌。描述里的卡名走 `StringVar`（`ModelDb.Card<Maul>().Title + "+"`），
  所以中英与升级后缀都自动正确。
* **跑酷**：`protected abstract bool Upgraded` 决定「选升级牌 + 本场战斗免费（而非本回合免费）」，
  卡按 `IsUpgraded` 施加对应类。

#### （6）「力量（本回合）」：删的是死键，不是类

`KotamaStrengthPower : TemporaryStrengthPower` 必须留着 —— 原版 `TemporaryStrengthPower` 是**抽象类**，
文档明写「Every model that grants a temporary strength power creates an associated power that subclasses this」。
但原版基类把 `Title` 指向 `OriginModel`（= 卡「来自小玉的协助」），`Description` 指向硬编码的
`TEMPORARY_STRENGTH_POWER.*` —— 所以模组的 `STS2_MOMOI_POWER_KOTAMA_STRENGTH_POWER.*` 三个键永远不会被读到，
已作为死键删除。

#### （7）文档生成器升级

`工作区\_scripts\_power_overview.py` 现在会：
* 额外扫描**没有 `[RegisterPower]` 的抽象基类**（否则 `SnakeGamePower` 这种继承不到 `InstanceType`）；
* 给 `*UpgradedPower` 的中文名加「（升级）」后缀，避免两条同名。

#### 产物

- `dotnet build` **0 错误** → DLL **438,272 B**、PCK **75,385,260 B**（10-14 09:25）。
- 自检：`_verify_batch14.py` **41 条全绿**，五套合计 **291 条断言全绿**。
- 备份：`工作区\_backup\batch14_pre`。

### 21.18 批次15：格挡预览错配、集结减费、消消乐、阿比舒、注能改写法（2026-10-14）

#### （1）🔴 卡面格挡数 ≠ 实际获得（来自算术使的关爱 / 旅行异蛙）

`new DynamicVar("Block", N)` 是普通变量，它的 `UpdateCardPreview` 是**空实现**，
不会跑 `Hook.ModifyBlock` —— 所以卡面数字不含敏捷加成、也不受脆弱削减。
`CreatureCmd.GainBlock(..., new BlockVar(base, ValueProp.Move), ...)` 那边走的是正常管道，
于是「显示 12，实际拿 9（脆弱）」。

**修法**（原版 `Armaments` / `Backflip` 的写法）：两边都用同一个 `BlockVar`。

```csharp
new BlockVar(12m, ValueProp.Move),                       // 声明
await CreatureCmd.GainBlock(Owner.Creature, DynamicVars.Block, cardPlay);   // 使用
```

**全模组扫描结果：共 10 张卡中招，全部已改**
（来自小鸟的援助 12 / 翻滚射击 7 / 结果好就没问题！16 / 来自算术使的关爱 12 / 整装待发 8 /
对策 6 / 发布委托 7 / 旅行异蛙 6 / 相遇 8 / 心流 16）。
脚本 `工作区\_scripts\_batch15_block.py` 负责改声明，`GainBlock` 那侧另用一条正则统一替换
（注意：**同一个 .cs 里有多个类时，必须一次性按文件汇总改写**，否则后一个类的改动会把前一个覆盖掉 —— 第一次跑就踩了这个坑）。

#### （2）🔴 集结的减费只生效一次

`EnergyCost.AddThisCombat(-N)` 是往 `_localModifiers` 里**追加**一条相对修正：
进手牌时算一次、打出时又算一次（重复扣），之后**再打出支援牌不会重算** → 就是「只生效一次」。

**修法**：改用读取时现算的 hook，不再改状态：

```csharp
public override bool TryModifyEnergyCostInCombat(CardModel card, decimal originalCost, out decimal modifiedCost)
{
    modifiedCost = originalCost;
    if (card != this || originalCost < 0m) return false;
    var reduction = CombatStats.SupportCardsPlayed;      // 实时的本场支援牌数
    if (reduction <= 0) return false;
    modifiedCost = Math.Max(0m, originalCost - reduction);
    return modifiedCost != originalCost;
}
```

`CombatState.IterateHookListeners()` 会遍历所有战斗牌堆里的卡（含手牌），所以 hook 一定会被调到。

#### （3）🔴 消消乐第二次选牌后没正常消耗（日志 145708 / 153533）

两张日志里都是同一串：

```
ERROR: Can't add child 'Card' to 'CombatUi', already has a parent '@Control@6355'
   [1] CardPileCmd.MoveCardNodeToNewPileBeforeTween(NCard, PileType)
   [10] CardCmd.Exhaust(...)
   [14] STS2_Momoi.Cards.Match3+<OnPlay>d__11.MoveNext()
```

`CardPileCmd.Add` 里 `if (!skipVisuals) { GetTweenForCardsChangingPiles(...) }`，
而 `MoveCardNodeToNewPileBeforeTween` 是「先从原父节点摘下来、再挂到 CombatUi」；
两段选牌结束后卡牌节点可能还挂在选牌 UI 的子容器下，摘除走的是延迟路径 →
紧接着的 AddChild 就撞上「already has a parent」。

**修法**：`CardCmd.Exhaust(choiceContext, card, causedByEthereal: false, skipVisuals: true)`
—— 跳过搬节点的 tween，模型照常进消耗堆。

#### （4）贪吃蛇 power 描述本地化报错

日志里 245 次 `Key 'SNAKE_GAME_POWER.title' not found`，真因是 RitsuLib 的注册报了：

```
[ERROR] [AutoRegister] Failed to inspect type 'STS2_Momoi.Cards.SnakeGamePower':
Type declares multiple auto-registration attributes for the same logical inheritance slot 'RegisterPowerAttribute'
```

也就是**类上留了两个 `[RegisterPower]`**（和批次13 的 CyclicNarrative 是同一种失误），
注册失败 → 模型没有正式 ID → 标题查不到。
已删掉重复特性。**并新增了一个全仓扫描：检查每个类声明紧邻的属性块里是否有重复的注册特性**，
批次15 自检里常态保留。

#### （5）系统：阿比舒

- 基础伤害 `CalculationBaseVar(1) → 2`（升级 3）
- 新增 `DynamicVar("Growth", 1)`（升级 2），`CombatStats.AddAbishuBonus(int amount = 1)`
- 文本改为 `...造成的伤害+[blue]{Growth}[/blue]。`

#### （6）来自小玉的协助：power 贴图

`KotamaStrengthPower` 继承原版 `TemporaryStrengthPower`（抽象类，必须留），
拿不到 `ModPowerTemplate.AssetProfile`，所以图标会去原版 `power_atlas` 找
`sts2_momoi_power_kotama_strength_power` 而落空（日志里有对应的 Missing sprite 警告）。

**修法**：实现 RitsuLib 的 `IModPowerAssetOverrides`（`PowerIconPathPatch` 就是给实现它的模型用的）：

```csharp
public sealed class KotamaStrengthPower : TemporaryStrengthPower, IModPowerAssetOverrides
{
    public PowerAssetProfile AssetProfile => new(
        IconPath: $"{Entry.ResPath}/images/powers/kotama_strength_power.png",
        BigIconPath: $"{Entry.ResPath}/images/powers/kotama_strength_power.png");
    public string? CustomIconPath => AssetProfile.IconPath;
    public string? CustomBigIconPath => AssetProfile.BigIconPath;
}
```

图标来自 `工作区\power图标成品\来自小玉的协助.png` → `images/powers/kotama_strength_power.png`。

#### （7）注能：放弃附魔思路

原来 `DevGreen` 在 `AfterCreated` 里 `CardCmd.Enchant<MomoiImbued>`，
而 `MomoiImbued : EnchantmentModel`（原版基类，没有可覆写的 `AssetProfile`）→
`EnchantmentModel.IconPath` 按 `Id.Entry` 拼路径找不到图 → 附魔栏显示 nope。

**修法**：把注能的效果直接写进卡牌类，删掉附魔本体：

```csharp
// DevGreen
public override async Task AfterAutoPrePlayPhaseEntered(PlayerChoiceContext choiceContext, Player player)
{
    if (player == Owner && Owner.PlayerCombatState.TurnNumber <= 1)
    {
        await CardCmd.AutoPlay(choiceContext, this, null);
    }
}
```

* `ShouldStartAtBottomOfDrawPile` 是 `EnchantmentModel` 的虚属性，`CardModel` 上没有 → 卡牌版不需要。
* 卡只要在战斗牌堆里、`ShouldReceiveCombatHooks` 为真就能收到这个钩子，不用额外注册。
* 牌打完去向由 `GetResultLocationForCardPlay` 决定：能力牌进 Limbo（本场不再回来）。
* **注能的词条与侧栏保留**：`localization/{zhs,eng}/enchantments.json` 原样留着，
  改用 `AdditionalHoverTips` 挂上去（`LocString("enchantments", "MOMOI_IMBUED.title")`）。
* **只删附魔图标**：整个 `images/enchantments/` 目录已删。
* `MomoiImbued` 类已删除。

#### （8）其它

* 循环叙事卡牌文本回滚：去掉我上一批擅自加的「（重复打出可以叠加持续回合数）」，恢复成
  「将本回合所有进入过[gold]弃牌堆[/gold]的牌洗入[gold]抽牌堆[/gold]。\n本回合结束时，重复此效果。」

#### 产物

- `dotnet build` **0 错误** → DLL **438,272 B**、PCK **75,402,656 B**（10-14 16:37）。
- 自检：`_verify_batch15.py` **50 条全绿**；六套合计 **342 条断言全绿**。
- 备份：`工作区\_backup\batch15_pre`（8 个 .cs + 附魔图标 + 新 power 图标）。

### 21.19 批次16：全模组代码审核（133 卡 + 54 power + 9 遗物 + 4 补丁）（2026-10-14）

5 个审核员并行逐文件通读，与原版反编译源码逐条核对契约，我逐条复核后动手修。
完整报告：`工作区\_docs\_代码审核_批次16.md`；原始 5 份记录：`工作区\_docs\_审核_批次16.md`。

#### 🔴 必崩的两处：给不可升级的牌预览升级版

```csharp
// HoverTipFactory.FromCard(card, upgrade: true)
if (upgrade) { card = (CardModel)card.MutableClone(); card.UpgradeInternal(); ... }
// CardModel.CurrentUpgradeLevel setter:
if (value > MaxUpgradeLevel) throw new InvalidOperationException($"{Id} cannot be upgraded past its MaxUpgradeLevel.");
```
| 位置 | 预览的牌 | MaxUpgradeLevel |
|---|---|---|
| `Cards/BurnFlowCards.cs:94`（玩火+） | `Burn`（状态牌） | **0** |
| `Cards/MinigameFlowCards.cs:197`（熬夜+） | `PoorSleep`（诅咒） | **0** |

→ 悬停即抛。已恒传 `upgrade: false`。全仓另外 36 处 `FromCard<T>(IsUpgraded)` 逐一核过，目标卡都可升级。

#### 🔴 俄罗斯方块少了「弃牌堆方块返回手牌」

批次13 我重写 `Settle` 时把这趟循环删掉了。而**溢出方块恰恰躺在弃牌堆**
（`Tetris.OnPlay` 在手牌满时把方块放进 `Discard`）——最常见的触发场景下效果完全没发生。已补回。

#### 🔴 集结的减费：漏算 + 减两次

1. `CombatStats.SupportCardsPlayed` 的唯一写点用 `MinigameSupport.IsSupportCard(card)`（**只看 tag**），
   而模组里大部分支援牌没有 tag（只有 `IsSupportCardType` 认得）→ 打出这类牌集结不减费。
   改成 `IsSupportCard(card) || IsSupportCardType(card)`。
2. 批次15 把集结改成现算 hook 后，`CombatStats.MinigamePlayedPatch` 里**仍留着**旧的
   `EnergyCost.AddThisCombat(-1, reduceOnly: true)` → 现算 + 追加 = **减 2 倍**。已删除那段。

#### 🟠 「雷酱」快照可能双倍易伤

`FaceDamage` 原本读 `DynamicVars.CalculatedDamage.PreviewValue` —— 那是**展示值**，
由 `Hook.ModifyDamage(... target ...)` 带目标算出来；若卡面最后一次重绘带着易伤目标，它已经乘过 1.5，
而 `YoshimiRepeatPower` 自己还会再补一次易伤 → 最坏 1.5×1.5。
改成自己重算同一条管道、`target` 传 `null`（易伤/虚弱需要目标，就不会介入），力量/活力照常算进去。

#### 🟠 其余已修

| 项 | 修法 |
|---|---|
| 双刀王小桃重复打出对**死目标**空放（`AutoPlay` 对非 null 目标不做存活检查） | `target is { IsAlive: true } ? target : null` |
| 心流：`AddUntilPlayed` 是**追加**型，同回合触发两次变 -4（基础 3 费被钳成 0），与文案「减少 2c」不符 | 改 `SetUntilPlayed(Canonical - reduce)`（覆盖式） |
| 剑来！：文案「**本回合**耗能 -1c」，`AddUntilPlayed` 只在打出时清理，会留到下一回合 | 改 `AddThisTurnOrUntilPlayed` |
| 火焰附加把「升级 2 层」硬编码（`? 2 : 1`），且 `cardSource == null` 时静默按 1 算 | 读来源卡的 `BurnPerStack` |
| 非战斗 `GetPile` 会抛：`ConceptCounterCapability` 4 个 helper、`ShuffleDiscardsEnteredThisTurn` | 改 `CardPile.Get`（返回 null） |
| `ThrowingPlayerChoiceContext` 的 `SignalPlayerChoiceBegun` 直接抛 `NotImplementedException`；钩子本来给了真实 ctx 的地方不该用它 | 俄罗斯方块结算 / 节奏游戏伤害 / 重整旗鼓自动打出改用真实 `choiceContext` |
| `DynamicVarSet.Cards` 是强转 `CardsVar`，普通 `DynamicVar("Cards", n)` 被读就 `InvalidCastException` | `BA启动！` 改 `CardsVar(2)` |
| 6 处空引用（`Owner.PlayerCombatState` / `Owner.Player` 未判空） | 加 `?.` / 局部变量判空 |
| 2 个声明后从未使用的 `tracker` 局部变量 | 删除 |

#### 复核后确认「写法正确」的（避免以后重复排查）

`IsClone` 确实覆盖 `CreateClone`+`CreateDupe`；渔获/秒人斧的 `RemoveFromDeck` 前置条件齐全；
`RankUpPower` 换「掉到二档了」不会在胜利时重复发奖（胜利走 `RemoveAllPowersInternalExcept`，故意跳过 `AfterRemoved`）；
`BattleRoyale` 的 `CalculatedVar` 里调 `GetPile` 不会在图鉴界面炸（`CalculatedVar.Calculate` 有 `IsInProgress && CombatState != null` 门控）；
`AutoPlay(..., null)` 无合法目标时走 `MoveToResultPileWithoutPlaying` 不抛；
跨战斗状态由 `Hook.BeforeCombatStart → CombatStats.Reset()` 统一重置。

#### 留给你拍板的 4 项（我没擅自改）

1. **机会难得，选红色！** 代码给了 `picked.EnergyCost.SetUntilPlayed(0)`（下次打出免费），卡面**完全没写**；注释还说「本场战斗免费」。删代码 or 补文本？
2. **来自明日奈的援护**的减伤**不看 `props`**，对 DoT（灼烧/中毒，`Unpowered`/`Unblockable`）也生效；
   原版 `ColossusPower` 等都有 `if (!props.IsPoweredAttack()) return 1m;` 门控，而卡面文案是「你受到的**所有**伤害降低」。
3. **心流**减费是覆盖（我改的）还是可叠加？
4. **自动打出被阻止时是否还算触发**（蒙太奇会照发构想奖励；王道手牌满时卡会进弃牌堆但减费照挂）。

#### 产物

- `dotnet build` **0 错误** → DLL **439,296 B**、PCK **75,402,656 B**（10-14 17:04）。
- 自检：`_verify_batch16.py` **27 条全绿**；七套合计 **369 条断言全绿**。

### 21.20 批次17：消消乐根因、阿比舒改 claw 写法、若干回滚（2026-10-15）

#### 🔴 消消乐的「幽灵牌」真因：`source` 把选牌收尾推后了

`NPlayerHand.SelectCards` 结束时调 `AfterCardsSelected(source)`（`src/Core/Nodes/Combat/NPlayerHand.cs:676`），里面：

```csharp
if (source != null) source.ExecutionFinished += OnSelectModeSourceFinished;   // ← 推后
else OnSelectModeSourceFinished(null);                                        // ← 当场
```

而 `OnSelectModeSourceFinished`（:919）才是把选中的卡从 `_selectedHandCardContainer` 搬回手牌的那一步：

```csharp
foreach (NSelectedHandCardHolder item in _selectedHandCardContainer.Holders.ToList())
{ NCard cardNode = item.CardNode; item.QueueFreeSafely(); Add(cardNode); }
```

卡传了 `source: this` → 这步被推到 **本卡 `ExecutionFinished`（= 整段 OnPlay 结束）** 才做。于是我们在 OnPlay 里紧接着消耗这些卡时：

| 消耗写法 | 结果 |
|---|---|
| 不跳过动画 | `MoveCardNodeToNewPileBeforeTween` 要搬的节点还挂在选牌容器下 → `Can't add child 'Card' to 'CombatUi', already has a parent`（批次15 前的日志 145708 / 153533） |
| `skipVisuals: true`（批次15 的“修复”） | 没搬节点 → 节点一直留在选牌容器，`ExecutionFinished` 时又被 `Add(cardNode)` 搬回手牌 → **一张幽灵牌** |

**正解**：两次 `FromHand` 的 `source` 都传 `null`，让每次选牌的收尾**当场完成**，再走正常的消耗动画。
（`source` 在 `NPlayerHand` 里只用于这个 `ExecutionFinished` 订阅，传 null 没有别的副作用；卡牌自己的 `source` 语义在单次选牌的卡里才需要。）

#### 系统：阿比舒改用原版爪击 / 撕咬的写法

旧写法把加伤存在 `CombatStats.AbishuDamageBonus` 里现算，`DamageCmd.Attack(decimal)` 拿的是 `CalculatedDamage + bonus`，
而**卡面 `{CalculatedDamage:diff()}` 永远只显示基础值** → 打出的伤害比卡面高，对不上。
（而且这种“加成在 var 外面”的写法，只要卡面不重算就永远对不上。）

按原版 `Claw.cs` / `Maul.cs` 重写：

```csharp
private decimal _extraDamageFromAbishuPlays;
private decimal ExtraDamageFromAbishuPlays { get => ...; set { AssertMutable(); ... } }

protected override IEnumerable<DynamicVar> CanonicalVars =>
[ new DamageVar(2m, ValueProp.Move), new DynamicVar("Growth", 1m) ];

// OnPlay：先打伤害（本次对自己的加伤不影响这一击），再给所有阿比舒加伤
foreach (var card in owner.PlayerCombatState.AllCards.OfType<SystemAbishu>().ToList())
    card.BuffFromAbishuPlay(increase);

private void BuffFromAbishuPlay(decimal extraDamage)
{ DynamicVars.Damage.BaseValue += extraDamage; ExtraDamageFromAbishuPlays += extraDamage; }

protected override void AfterDowngraded()
{ base.AfterDowngraded(); DynamicVars.Damage.BaseValue += ExtraDamageFromAbishuPlays; }
```

加伤直接写在 `Damage.BaseValue` 上 → 卡面 `{Damage:diff()}` 与打出的数值天然一致；
`CombatStats.AbishuDamageBonus` / `AddAbishuBonus` 已删除；文本改为
`…{Damage:diff()}点伤害…造成的伤害+{Growth:diff()}。`（**那个 2 不再是蓝色**）。

**全模组扫查「卡面伤害 ≠ 实际伤害」**：把每张卡的 `DamageCmd.Attack(...)` 参数与卡面占位符逐一对照 +
搜「用全局值参与伤害计算」的写法，结论是**只有阿比舒这一处**。
`CommonAttackCards` / `FirepowerFlowCards` 里那几个 `WithMultiplier((_,_) => CombatStats.XXX)` 是写在
`CalculatedVar` 内部的，`UpdateCardPreview` 会算进去 → 卡面与实际一致 ✓。

#### 回滚 / 按你的裁定调整

| 项 | 结果 |
|---|---|
| 心流减费 | **改回 `AddUntilPlayed`（可叠加）**：每 3 张小游戏牌 -2，触发两次就是 -4（3 费基础直接到 0），与原版火箭飞拳同款；注释里写明「不要改成 SetUntilPlayed」 |
| 幸运儿的祝福 | **不加门控**：对所有伤害生效（含灼烧/中毒这类 DoT） |
| 王道手牌满 | **不改**：卡进弃牌堆、减费照挂 |
| 机会难得，选红色！ | 代码不改；**补文本**「这张牌在本回合可以免费打出。」（「本场战斗免费」当废案） |
| 局势升温 | 标题早已是「局势升温」，只把代码注释里的「玩火」同步改名 |
| 蒙太奇 | AutoPlay 被阻止时**不发构想奖励**：新增 `AutoPlayProbe.WillActuallyPlay(...)`（照抄 `CardCmd.AutoPlay` 的前置分支：`Unplayable` 关键字 / `Hook.ShouldPlay` / 目标可用性） |

#### 产物

- `dotnet build` **0 错误** → DLL **439,808 B**、PCK **75,403,056 B**（10-15 06:11）。
- 自检：`_verify_batch17.py` **28 条全绿**；八套合计 **397 条断言全绿**。

### 21.21 批次18：消消乐重做 + 妮露援护归属确认（2026-10-15）

#### 0. 更正：批次16 那条「双刀王小桃」改动其实在「来自妮露的援护」

`Cards/AssistCards2.cs` 里 `target is { IsAlive: true } ? target : null` 所在类是 **`MomoiSupportNeru`（来自妮露的援护）**
（消耗全部火力、每层额外打出一次），不是双刀王小桃。改动本身正确，与本卡设计一致：
**原目标死了就交给 `AutoPlay`（传 null）去重挑随机存活敌人**，不会静默空放。

#### 1. 消消乐重做

| 项 | 改动 |
|---|---|
| 第二次选牌提示 | 从通用的「选择一张牌」改为自定义 `STS2_MOMOI_CARD_MATCH3.pickAny` =「**选择任意张牌**」（第一段仍是通用提示） |
| 两个侧栏 | **删除**（`sidebar1` / `sidebar2` 连代码里的 `AdditionalHoverTips` 一起删） |
| 攻击/技能/能力的类型分支 | **整段删除**（原来 ≥3 张按类型给伤害/格挡/按顺序打出，现在统一成「打出并消耗」） |
| 三消（≥3 张） | 改为 **打出并消耗**：`AutoPlayProbe.WillActuallyPlay` 为真先 `AutoPlay`；然后**只对还在战斗牌堆里**（Hand/Draw/Discard/Play）的牌补一次 `CardCmd.Exhaust` —— 这样三种边界都对：<br>· 本来就带「消耗」的牌 → 打出后已在消耗堆 → 跳过（不会“找不到对象”）；<br>· 能力牌 → 打出后进 Limbo（`Pile` 为 None）→ 跳过；<br>· 无法打出的牌（`Unplayable` / 被 `Hook.ShouldPlay` 阻止）→ 没被 AutoPlay 消耗、仍在手牌 → 直接消耗。 |
| 超三张 | 不变：每超出 1 张抽 1 张牌 + 获得 1 能量 |
| 升级效果 | `OnUpgrade` 改为 `AddKeyword(CardKeyword.Retain)`（**添加「保留」**），并加 `AfterDowngraded` 移除；卡面「保留。」由 `CardKeywordOrder.beforeDescription` 自动追加 |
| `CanonicalVars` | 删掉 `CalculationBaseVar/ExtraDamageVar/CalculatedDamageVar/BlockVar`，只留 `EnergyVar(1)` |
| 文本 | `选择[blue]1[/blue]张牌并选择任意张与其类型相同的牌[gold]消耗[/gold]。若[gold]消耗[/gold]的牌不低于[blue]3[/blue]张则改为打出并[gold]消耗[/gold]，超过[blue]3[/blue]张则每超出一张就抽[blue]1[/blue]张牌并获得{Energy:energyIcons()}。`（**不手写**「小游戏牌。」「消耗。」——那两个由标签补丁与 `CardKeyword.Exhaust` 自动追加） |

#### 产物

- `dotnet build` **0 错误** → DLL **438,784 B**、PCK **75,402,096 B**（10-15 06:40）。
- 自检：`_verify_batch18.py` **26 条全绿**；九套合计 **423 条断言全绿**。

### 21.22 批次19：颜色标记的「按表」规范（2026-10-15）

**纠正一个我一直搞错的前提**：卡面里的数字**默认不上色**，只有 power 的数字才用 `[blue]`。

逐表核对原版 `localization/zhs`（`.description` 里的标记计数）：

| 表 | 原版标记分布 | 结论 |
|---|---|---|
| `cards` | `gold` 694、`purple` 1、**`blue` 1** | 卡面几乎只用 `[gold]` 标关键词；**数字不上色**；变量数字靠 `{X:diff()}` 由格式化器自动染色 |
| `powers` | `gold` 213、**`blue` 174** | power 的数字用 `[blue]` |
| `relics` | `gold` 322、**`blue` 277**、`purple` 15、`red` 14、`green` 13 | 遗物数字用 `[blue]`、回血用 `[green]` |
| `potions` | `gold` 63、**`blue` 61**、`green` 3 | 药水同上 |

原版卡面样例（数字都是裸的）：

```
ACROBATICS  抽{Cards:diff()}张牌。\n丢弃1张牌。
ADRENALINE  获得{Energy:energyIcons()}。\n抽2张牌。
BALL_LIGHTNING  造成{Damage:diff()}点伤害。\n[gold]生成[/gold]1个[gold]闪电[/gold]充能球。
```

**改动**：把我在批次12/15/17/18 给卡面加上的 `[blue]` 全部去掉（5 张卡 × 2 条 × 2 语言 = 20 条）：
`消消乐`、`来自花凛的援护`、`重整旗鼓`、`扫雷`、`吃豆人！`。
去标记后与用户给的原文完全一致，例如消消乐现在是：
`选择1张牌并选择任意张与其类型相同的牌[gold]消耗[/gold]。若[gold]消耗[/gold]的牌不低于3张则改为打出并[gold]消耗[/gold]，超过3张则每超出一张就抽1张牌并获得{Energy:energyIcons()}。`

> 保留不动的：powers 的 `[blue]`（73/72 处）、relics/potions 的 `[blue]`（原版就这么写）、
> 卡面的 `[gold]` 关键词、用户点名要求的卡面 `[red]` 诅咒名与 `[green]` 升级牌名。
> 另：`RALLY_AGAIN_POWER` 的回复量用的是 `[green]{HealPer}[/green]`（跟遗物/药水的回血惯例一致）；
> 严格按「power 只用 gold+blue」的话也可以改成 `[blue]`，留着等用户定。

#### 产物

- `dotnet build` **0 错误** → DLL **438,784 B**、PCK **75,401,392 B**（10-15 06:46）。
- 自检：`_verify_batch19.py` **13 条全绿**；十套合计 **436 条断言全绿**。
- 备份：`工作区\_backup\batch19_pre`。

### 21.23 批次20：阿比舒的 4 倍改为乘法修正、勇者加护 10 伤、消消乐首句、一次文件恢复（2026-10-15）

#### 1. 系统：阿比舒 —— 最后一段的「4 倍」改成真正的乘法

旧写法是 `DamageCmd.Attack(baseDamage * 4)` —— 那是把 **面板数值** 乘 4，之后管道里再加力量/活力，
所以实际是 `(base×4 + 力量 + 活力) × 易伤 × 虚弱`，与「最后一段是 4 倍伤害」不符。
（也不能反过来把 4 提前乘进面板，那样目标易伤会被吃好几次。）

**改成乘法修正**（参考本模组「来自勇者的加护」的伤害翻倍）：

```csharp
private bool _finalHit;   // 只在最后一段置真

public override decimal ModifyDamageMultiplicative(Creature? target, decimal amount, ValueProp props,
    Creature? dealer, CardModel? cardSource, CardPlay? cardPlay)
    => cardSource == this && _finalHit ? 4m : 1m;
```

这样：
* 力量 / 活力 / 同类型阿比舒累积的加伤**一起被 ×4**（力量为负也会被 ×4）；
* 易伤、脆弱这类需要目标的修正**各自只乘一次**；
* 虚弱按原版是最终伤害 -25%，与 ×4 各自乘一次 = 「翻倍的是不吃虚弱的那份，然后再吃一次虚弱」。

**代码结构**（先 2 次基础伤害，再 1 次 4 倍，特效只给最后一段）：

```csharp
var targets = combatState.HittableEnemies.ToList();
var baseDamage = DynamicVars.Damage.BaseValue;

// 整张牌算「一次攻击」：BeforeAttack / AfterAttack 各只跑一次
// （不然每一段各跑一遍 → 活力会被消耗两次，而不是被最后一段的 4 倍放大）。
await using var attackContext = await AttackCommand.CreateContextAsync(combatState, choiceContext, cardPlay);

attackContext.AddHit(await CreatureCmd.Damage(choiceContext, targets, baseDamage, ValueProp.Move, Owner.Creature, this, cardPlay));

await PlayHyperbeamVfx(combatState);          // 原版超能光束（NHyperbeamVfx + NHyperbeamImpactVfx）
_finalHit = true;
try   { attackContext.AddHit(await CreatureCmd.Damage(choiceContext, targets, baseDamage, ValueProp.Move, Owner.Creature, this, cardPlay)); }
finally { _finalHit = false; }
```

> ⚠️ 注意：**不能用两次 `DamageCmd.Attack(...).Execute(...)`**（那正是网上那段建议的写法）——
> `AttackCommand.Execute` 自己会调 `Hook.BeforeAttack` / `Hook.AfterAttack`（`AttackCommand.cs:549 / :672`），
> 外面再套 `AttackContext` 就变成**三遍**，活力会被消耗两次。
> 原版用 `AttackContext` 的两张卡（`EchoingSlash` / `Omnislice`）在上下文里走的都是 **`CreatureCmd.Damage`**，
> 并且 `AttackCommand.Results` 的注释也写明「用了 AttackContext 时这里是空的」，所以命中要 `ctx.AddHit(...)` 记进去。

数值回到：基础伤害 **1**（升级 2），`Growth` **1**（不随升级变化，升级只加基础伤害）。卡面描述未改。

#### 2. 来自勇者的加护：升级伤害 11 → 10

`OnUpgrade` 的 `CalculationBase.UpgradeValueBy(3)` → `(2)`（基础 8）。

#### 3. 消消乐首句缩短

`选择1张牌并选择任意张与其类型相同的牌消耗。` → **`选择任意张类型相同的牌消耗。`**
（两段选牌的 UI 不动，只是文案不再提「先选 1 张」；语义不变、字数更省。）

#### 4. 一次文件恢复（重要教训）

在替换 `RemainingSpecialCards.cs` 里的 `CourageBoon.OnUpgrade` 时，我用「切片 + 拼接」写回文件，
**忘了把切片之后的尾部接回去** → 979 行的文件被截成 289 行。
恢复方式：`工作区\_backup\batch15_pre\RemainingSpecialCards.cs`（§21.18 开始时的完整备份，979 行）
→ diff 确认与截断前**只差一行**（就是本次要改的 CourageBoon）→ 覆盖回去后再补：
`相遇` 的 `BlockVar` 改造 + `DevGreen` 注能改写法（删 `MomoiImbued`、加侧栏与钩子）+ CourageBoon 10 伤。
最后由 `_verify_batch20.py` 的「文件恢复完整性」一节逐项断言确认无其它丢失。

**教训**：改单文件里的一个片段时用精确文本替换（`str.replace`），不要手写切片拼接。

#### 产物

- `dotnet build` **0 错误** → DLL **441,856 B**、PCK **75,401,344 B**（10-15 07:29）。
- 自检：`_verify_batch20.py` **28 条全绿**；十一套合计 **464 条断言全绿**。

### 21.24 批次21：阿比舒 3 段修复、曳光弹数值、两张卡的费（2026-10-15）

#### 🔴 「系统：阿比舒」只有 2 段伤害 —— `CreatureCmd.Damage` 一次只结算一次

上一批改成 `CreatureCmd.Damage` 之后，我把它当成能带「命中次数」的 `AttackCommand` 了：
`CreatureCmd.Damage(...)` **每次调用只结算一次伤害**，所以「第 1 段打 2 次」只写了一次 → 实战只有 2 段
（日志 20261015-081556 里每次打出只有 2 条 `DamageDealt`）。

**修法**：循环调两次。

```csharp
// ⚠ CreatureCmd.Damage 每次只结算**一次**伤害（它不是 AttackCommand 的 WithHitCount），
//   所以 2 次要调两次 —— 只调一次就会变成“只有 2 段”而不是卡面写的 3 次。
for (int i = 0; i < 2; i++)
    attackContext.AddHit(await CreatureCmd.Damage(choiceContext, targets, baseDamage, ValueProp.Move,
        Owner.Creature, this, cardPlay));
```
两段 AddHit 都在同一个 `AttackContext` 里 → `BeforeAttack` / `AfterAttack` 仍是各一次，活力只消耗一次 ✓。

#### 曳光弹（`FlameBullet`）

| 项 | 旧 | 新 |
|---|---|---|
| 基础伤害 | 7（升级 9） | **6（升级 8）** |
| 基础灼烧 | 2（升级 3） | **3（升级 4）** |
| 活力换灼烧 | 每 **2** 点活力 +1 层（`vigor.Amount / 2`） | 每 **1** 点活力 +1 层（`vigor.Amount`） |
| 文本 | 毎有2点活力… | 「每有1点[gold]活力[/gold]，额外给予1层[gold]灼烧[/gold]。」 |

#### 费用

- **来自时的援助**（`MomoiSupportToki`）：2 → **0**
- **系统：阿比舒**（`SystemAbishu`）：0 → **1**

#### 产物

- `dotnet build` **0 错误** → DLL **441,856 B**、PCK **75,401,344 B**（10-15 08:18）。
- 自检：`_verify_batch21.py` **17 条全绿**；十二套合计 **481 条断言全绿**。


### 21.25 批次22：曳光弹升级灼烧的真因、破势重做、五处文本/数值（2026-10-16）

#### 1. 🔴 曳光弹升级后灼烧不涨（3 → 4）—— `DynamicVar.Clone()` 是浅拷贝

`IndependentCalculatedVar` 记着构造时的 `burnBase` / `burnExtra` 两个实例。问题在于
`DynamicVarSet.Clone()`（每次进战斗、每次降级都会跑）是 `Values.Select(v => v.Clone())`，
而 `DynamicVar.Clone()` 只是 `MemberwiseClone()` + `ResetToBase()` ——
于是克隆出来的 `IndependentCalculatedVar` 里 `_base`/`_extra` **仍然指向规范化实例**，
而 `DynamicVars["BurnBase"].UpgradeValueBy(1)` 升的是**这张卡自己那份克隆**。
结果：升级后卡面与结算读的都是没被升级的原实例，永远显示 3。

**修法**（`Cards\DynamicVarSupport.cs`）：只记名字，运行时按名字从持有者的 `DynamicVars` 里取，取不到才退回构造时那个实例。

```csharp
protected override DynamicVar GetBaseVar() => Resolve(_baseName, _baseFallback);

private DynamicVar Resolve(string name, DynamicVar fallback)
    => _owner is CardModel card && card.DynamicVars is { } set && set.TryGetValue(name, out var v) ? v : fallback;
```

> 同一坑的潜在受害者：任何「升级会动到 IndependentCalculatedVar 引用变量」的卡。
> 博览群游（HitsBase/HitsExtra 都不升级）当时是侥幸没暴露。

#### 2. 破势（`MomentumBreak`）重做 —— 活力发挥 4/5 倍

| 项 | 旧 | 新 |
|---|---|---|
| 耗能 | 3（升级 2） | **2（升级还是 2，升级不再减费）** |
| 伤害 | 20（升级 20） | **16（升级 20，+4）** |
| 活力收益 | 每点活力最终伤害 +10%（升级 +20%），走 `ModifyDamageMultiplicative` | **「活力在这张牌上发挥 4 倍（升级 5 倍）的效果」**，走新补丁 `Patches\VigorMultiplierPatch.cs` |

为什么不在卡里做：原版 `Hook.ModifyDamageInternal` 对力量与活力都是 `num += 各 power 的 ModifyDamageAdditive 返回值`——
**同一条加伤通道**。在卡里手动再加一次力量/活力会变成 `1+n` 倍而不是 `n` 倍。
劫持返回值（Harmony Postfix + `ref decimal __result`）只改「加多少」，不影响「吃不吃」（活力那堆 dealer/cardSource 判定原样保留）；
`VigorPower` 是 `sealed`，也没法继承。多段牌每段都会走这个钩子，所以 n 倍天然按段生效。

```csharp
public static ModPatchTarget[] GetTargets() => [new(typeof(VigorPower), nameof(VigorPower.ModifyDamageAdditive))];

public static void Postfix(CardModel? cardSource, ref decimal __result)
{
    if (__result == 0m || cardSource is not MomentumBreak momentum) return;
    __result *= momentum.IsUpgraded ? 5m : 4m;
}
```
（**补丁必须登记进 `Entry.cs`**，已加 `patcher.RegisterPatch<Patches.VigorMultiplierPatch>();`）

卡面文本（用户逐字给定，已照抄）：
```
造成{CalculatedDamage:diff()}点伤害。
[gold]活力[/gold]在这张牌上发挥{IfUpgraded:show:5|4}倍的效果。
若目标的意图为攻击，且这张牌造成的伤害大于目标即将对你造成的伤害，击晕该敌人并将这张牌的耗能增加{CostIncrease:energyIcons()}。
```

#### 3. 其余五项

| 卡 | 改动 |
|---|---|
| 整活 `Slapstick` | 卡面补「升级过的」（效果本来就对）：`…[gold]变化[/gold]为{IfUpgraded:show:升级过的|}随机[gold]小游戏牌[/gold]。` |
| 吃豆人 `PacMan` | 「没有诅咒」= **抽牌堆 + 手牌 + 弃牌堆全都没有**（原来只看手牌）；有诅咒时随机消耗 1 张——抽牌堆/弃牌堆里的会被**拉出来消耗**。用 `CardPile.Get`（`PileType.X.GetPile` 非战斗会抛异常） |
| 堕落 `Depravity` | 稀有度 普通 → **罕见**；效果与文本都加 1 层**虚弱**（`和1层[gold]虚弱[/gold]` 加在原「脆弱」后面），升级效果不变 |
| 独特点子 `UniqueIdea` | 稀有度 罕见 → **普通** |
| 专注 `Focus` | 耗能 **1**（升级 0）；博览群游 `ExperienceCombo` 耗能 **1**（升级前后都是 1） |

> 侧栏是**自动**的：`Patches\MinigameSidebarPatch.cs` 按描述原文扫描关键词，
> 「活力」→ `FromPower<VigorPower>()`、「虚弱」→ `FromPower<WeakPower>()`，所以破势/堕落**不用手写 HoverTip**。

#### 4. 产物

- `dotnet build` **0 错误** → DLL **442,880 B**、PCK **75,402,024 B**（10-16 16:02）。
- `_verify_batch22.py` **43 条全绿**；十三套合计 **524 条断言全绿**。

---

## 22. 后续路线图（2026-10-16 起）

| 优先级 | 方向 | 入口 |
|---|---|---|
| ★★★ | **角色美术**：战斗动画 `idle`/`attack1/2/3`/`cast1/2`/`taunt1`/`hit` 已完成（§21.27 / §21.28 / §21.29）；**relaxed 商店、休息处 `休息处.png`、像素 UI 头像、选人视频背景**已完成（§21.31 / §21.33）；剩技能牌动画、**选人转场动画**（BGM 已完成；卡框和拖尾已改为粉蓝） | `工作区\_docs\_美术待补清单.md`；差分只要覆盖同名文件 |
| ★★ | **卡牌调整**：用户点名的数值/文本/机制微调 | 本地化四处同步 + `_verify_batch*` + `dotnet build` |
| ★ | **新模组内容**：新卡 / 遗物 / 药水 / power / 新机制 | `工作区\STS2Momoi.xlsx`（权威）→ 本地化 → 代码 → 表格 |
| ★ | **可选的体验补齐**：卡面右下角计数语义、侧栏关键词、局内提示的进一步打磨 | `DisplayAmount` / `MinigameSidebarPatch` |

**协作红线（不会变）**：用户点名的才动手；文本逐字照抄；不手写会被自动追加的关键词徽章；报告要短。

### 21.26 批次23：金色关键词收尾（击晕 / 金币）（2026-10-16）

| 卡 | 改动 |
|---|---|
| 来自哈雷的援护 `MomoiSupportHare` | `[gold]击晕[/gold]所有敌人。` |
| 来自千寻的援护 `MomoiSupportChihiro` | `…[gold]击晕[/gold]该敌人。` |
| 破势 `MomentumBreak` | `…[gold]击晕[/gold]该敌人并将…`（承接批次 22 的文本） |
| 终于上一档了！ `RankUp` | `战斗结束后额外获得{IfUpgraded:show:25|20}[gold]金币[/gold]与一组卡牌奖励。\n如果下个回合结束前未能结束战斗，则只能额外获得{IfUpgraded:show:15|10}[gold]金币[/gold]。` |

- 英文同步 `[gold]Stun[/gold]` / `[gold]Gold[/gold]`（与 `RANK_UP_POWER` 里已有的写法一致）。
- **击晕的侧栏是现成的**：`Patches\MinigameSidebarPatch.cs` 里 `Has("击晕", "Stun") || Has("眩晕", "Stun")` → `StunIntent.GetStaticHoverTip()`，本次没有动它。
- **金币不加侧栏**：补丁的关键词扫描表里本来就没有「金币 / Gold」，所以上色纯粹是显示效果，符合原版（原版金币也没有侧栏）。
- 全表复核：`cards` 里已无裸的「击晕 / Stun / 金币 / Gold」正文（`GOLD_MINER.title` = "Gold Miner!" 是卡名，不动；`GOLD_MINER.sidebar2` 里还有一处「25金币/25 gold」属于**该卡侧栏**，**按「不擅自修改」原则未动**，见下方备注）。

**产物**：`dotnet build` 0 错误 → DLL **442,880 B**、PCK **75,402,280 B**（10-16 17:15）；`_verify_batch23.py` **25 条全绿**，十四套合计 **549 条**。

> 备注（待用户裁决，未自行修改）：`STS2_MOMOI_CARD_GOLD_MINER.sidebar2`（金币矿工·升级后说明）里有「每有1点耗能，战斗结束就额外获得25金币。」，
> 其中的「金币」与同段落的「能量 / 手牌」都没有 `[gold]`；如果要统一，可以一并补上（属于该卡侧栏文本，只影响显示）。

---

### 21.27 批次24：AEP 待机动画 → 战斗 idle 帧序列（2026-10-17）

**目标**：把 `工作区\编辑区\人物\待机动画.aep` 的 comp「待机」变成战斗待机动画，去掉绿幕和右上角水印。

**源 / 时间线**

- AEP `待机`：932×720，24.0002 fps，8.0417 s / **193 帧**；`预合成 3` = 3 × `预合成 2`（1.9167 s / 46 f）+ 55 帧收尾。
- `预合成 2`：源视频约 **6.1–6.5 s** 的站立待机，**4× 慢放**；收尾段：源视频约 **13.25–14.40 s**，**2× 慢放**（坐下-站起）。
- 源视频：`工作区\参考图集\截图\桃井绿屏 [蔚蓝档案动画片].mp4`（AEP 内嵌引用，932×720 / 24 fps / 2:00）。
- AE 渲染：comp `待机` → `带有 Alpha 的 TIFF 序列`（模板名带尾随空格），193 张 TIFF；帧编号 0095–0287 是 comp 显示起点偏移，脚本按排序后的 193 张读，不依赖编号。

**处理**（`工作区\编辑区\人物\_src\_build_idle_cue.py`）

1. **水印**：源视频右上角 `SechiAnimation bilibili`，白字 bbox `x 611–906 / y 25–63`；先把 `x 580..931 / y 0..99` 填成绿幕色 `(27,255,1)`，再参与抠像；最终裁切框 `x 297..660 / y 125..643` 本来也不含水印。最终 42 帧水印区 alpha 全 0。
2. **绿幕**：`greenness = G - max(R,B)`；背景实测 ≈228，人物 ≤0。`alpha = 1 - clamp((greenness-12)/(205-12))`，软边保留到 205；`G = min(G, max(R,B))` 去溢色，Lanczos 缩放后再 clamp 一次。最终不透明像素最大绿差 **0**。
3. **去重**：逐帧比较前景 mask（XOR≤80）与 RGB 平均差（≤2.5），得到 **42 张唯一帧**；AEP 的 4×/2× 慢放变成 `(Frame, Hold)`。3 段循环与第 1 段最大 RGB 差 **0.003**。
4. **画布**：统一 **600×820**；人物可见高度 **620 px**（与旧占位图一致），水平按 comp 中心 `x=466` 对到画布中心，脚底贴底（站立帧底边 y=815，收尾姿态 y=819）。premultiplied alpha + Lanczos4 + 边缘 6 px 颜色渗出。
5. **序列**：193 帧 = 3×46 帧循环 + 55 帧收尾；`VisualCueSet` 用 `.Sequence("idle", seq => { … }).Loop()`，**68 个 `Frame` 条目**（循环 13 张×3 + 收尾 29 张），24 fps，总 8.0417 s。

**产物**

- `images\characters\cue\idle.png` + `idle_01.png` … `idle_41.png`（42 张 RGBA，600×820，无损导入 `compress/mode=0`）。
- `STS2 MomoiCode\Characters\STS2 MomoiCharacter.cs`：`IdleLoop`（13 项，Hold 和 46）、`IdleOutro`（29 项，Hold 和 55）、`IdleFramePath`、`IdleLoopReps = 3`、`CueFps = 24f`；`.Single("idle")` 已删除。
- `工作区\编辑区\人物\_src`：`_render_aep.jsx`、`_build_idle_cue.py`、`README.md`；`_work`：`idle_manifest.json`、`idle_contact.png`、`idle_preview.gif`、`idle_csharp.txt`、`idle_placeholder_backup.png`。
- `dotnet build` **0 错误**，DLL **445,952 B** / PCK **84,743,552 B**（10-17 18:58）；PCK 内 42 个 `.ctex` 全部 600×820 RGBA，621 个条目 **md5 自检全通过**。
- `_verify_batch24.py` **44 条全绿**；十五套合计 **593 条**（原 549 + 44）。

**调速（2026-10-17 追加）**：`STS2 MomoiCharacter` 顶部有 `IdleLoopSpeed` / `IdleOutroSpeed` / `IdleCrouchSpeed` 三个倍率（默认 1）。站立循环改第一个；整段坐下-站起改第二个；只加快蹲下/站起（帧组 16-19 / 24-28 / 33-37）改第三个。公式 `时长 = Hold / (24 × 倍率)`；例：`IdleLoopSpeed = 1.1f; IdleOutroSpeed = 1.15f; IdleCrouchSpeed = 1.4f;`。改完只需 `dotnet build`，不用重跑 AEP/抠像。

**补充修复（开场不动）**：RitsuLib 的 `NCreatureCombatAnimationInitialBootstrapPatch` 只在角色返回战斗动画状态机时，才会在 `NCreature._Ready` 主动播 `idle`。只配 `VisualCues` 时，战斗开场不会触发 idle，画面就停在场景默认的 `idle.png`（第 0 帧）。已在 `STS2 MomoiCharacter` 重写 `SetupCustomCombatAnimationStateMachine`，先用 `StandardCue` 接好 idle；批次25 已扩展为自建状态机（idle + attack1/2/3 + cast1/2 + taunt1 + hit/dead/relaxed），见 §21.28。

**注意**

- 本批只替换了 **idle**；`hit/dead/relaxed` 仍是旧线稿占位；`attack/cast` 已在 §21.28 替换。
- 42 张 600×820 RGBA 在运行时约 **82 MB VRAM**；PCK 只增加约 **9.3 MB**（`.ctex` 无损）。
- 改 AEP 后重跑 `_src/README.md` 的三步；`IdleLoop/IdleOutro` 是脚本生成的，不要手改。

---

### 21.28 批次25：攻击/能力/嘲讽动画 + 按卡牌分流（2026-10-18）

**源 / 合成**（`工作区\编辑区\人物\素材1.aep`，932×720 / 24fps；AEP 里同名 comp 很多，**必须按 id 取**）：

| cue | comp | id | 总帧 | 唯一帧 | 画布 |
|---|---|---|---|---|---|
| `attack1` | 攻击动画1 | 266 | 21 | 8 | 600×820 |
| `attack2` | 攻击动画2 | 535 | 31 | 24 | **716×820** |
| `attack3` | 攻击动画3 合成 1 | 564 | 31 | 16 | **644×820** |
| `taunt1` | 嘲讽动画1 合成 1 | 593 | 38 | 21 | 600×820 |
| `cast1` | 能力动画1 | 651 | 48 | 24 | 600×820 |
| `cast2` | 能力动画2 | 476 | 46 | 12 | 600×820 |

**处理**（`工作区\编辑区\人物\_src\_render_anim_aep.jsx` + `_build_anim_cues.py`）

1. 按 id 渲染 6 个 comp → 215 张 TIFF（`pi_anim_render/<cue>/`）。
2. 水印/绿幕/去溢色同 §21.27；额外把 **最低脚底 `foot_ref` 对齐到画布 y=815**（与待机站立帧同一条地面线），不再用源 comp 固定的 y=640。
3. 去重：前景 XOR≤500 / RGB 平均差≤8.0（动作比待机快，阈值放宽）→ **215 → 105 张唯一帧**。
4. 画布：沿用待机比例 **1.22047**；源 `x=466` → 画布中心；高 820；`attack2`/`attack3` 只把画布加宽到 716/644（Sprite2D 居中，身体中心不变）。
5. 校验：所有帧水印区 alpha=0、不透明像素最大绿差 0、脚底最低点 ≥795；contact sheet 在 `_work/*_contact.png`。

**接入**

- `VisualCueSet` 增加 6 条 **非循环** 序列：`attack1/2/3`、`cast1/2`、`taunt1`；旧的 `attack.png`/`cast.png` 不再被引用（文件保留）。
- `SetupCustomCombatAnimationStateMachine` 改成自建状态机：
  `idle`（循环）→ `attack1/2/3`、`cast1/2`、`taunt1`、`hit`（播完回 idle）；`dead` 终止；`relaxed` 循环。
  标准 `Attack/Cast/PowerUp` 回退到 `attack1/cast1`；`Idle/Hit/Dead/Relaxed` 照常。
- 新增 3 个补丁（`Patches\MomoiCardAnimationCuePatch.cs`，已登记 Entry，启动日志 **16 patches, 0 failed**）：
  - `MomoiBeforeCardPlayedCuePatch`（`Hook.BeforeCardPlayed`）：按卡牌选 cue 并主动 `SetAnimationTrigger`，然后加压制标记。
  - `MomoiAfterCardPlayedCuePatch`（`Hook.AfterCardPlayed`）：卡牌结束后清标记。
  - `MomoiStateMachineCueSuppressPatch`（`ModAnimStateMachine.SetTrigger`）：卡牌期间压制 `Attack/Cast/PowerUp`，防止同一张牌被通用动画覆盖/重置。
- 分流规则（`Choose(CardModel)`）：
  | 卡牌 | cue |
  |---|---|
  | 嘲讽 `Taunt` / WIN！ `WinCard` | `taunt1` |
  | 构想 `ConceptCard` | `attack3`（先只给它） |
  | `Attack` 且 `MinigameSupport.IsSupportCardType` | `attack2` |
  | 其他 `Attack` | `attack1` |
  | `Power` 且 `Rarity == Rare` | `cast2` |
  | 其他 `Power` | `cast1` |
  | 技能 / 状态 / 诅咒 | 暂无动画（保持 idle，等技能美术） |
- 每个动作独立调速：`Attack1Speed` / `Attack2Speed` / `Attack3Speed` / `Cast1Speed` / `Cast2Speed` / `Taunt1Speed`（默认 1，公式 `Hold/(24×倍率)`）。

**产物**

- `images\characters\cue\` 现共 **152 PNG**：147 张真动画帧（idle 42 + attack1 8 + attack2 24 + attack3 16 + taunt1 21 + cast1 24 + cast2 12）+ 3 张使用中的占位（hit/dead/relaxed）+ 2 张旧 attack/cast 占位。
- `dotnet build` **0 错误**，DLL **452,608 B** / PCK **108,940,860 B**（10-18 12:48）；PCK **832 条目 md5 全通过**；运行时约 **+220 MB VRAM**（105 张新帧）+ 待机 82 MB。
- 自检：`_verify_batch25.py` **101 条全绿**；十六套合计 **694 条**。游戏内实测（用户确认）：一般攻击 / 支援攻击 / 构想 / 稀有 Power / 其他 Power / 嘲讽 / WIN！ 的分类、大小、接地全部正常。

**注意**

- `hit/dead/relaxed` 当时仍是占位（`hit` 已在 §21.29 替换）；`attack.png`/`cast.png` 保留但不再引用。
- 构想只走 `attack3`；不想用时删掉 `Choose` 里的 `card is ConceptCard` 分支即可。
- 动画在 `BeforeCardPlayed` 主动播；如果想让伤害/结算更贴合动画，可再调 `AttackAnimDelay` / `CastAnimDelay` 或把触发点改成卡牌自带时机。
- 改 AEP 后重跑 `_src/README.md` 的三步；数组/C# 分流不要手改生成部分。

---

### 21.29 批次26：受击动画（PSD → hit 序列）（2026-10-18）

**源**：`工作区\编辑区\人物\受击动画.psd`，524×646，9 个全画布像素图层：
`1受击开始`、`2` … `9受击结束`。透明底，**没有绿幕/水印**，不需要抠像。

**处理**（`工作区\编辑区\人物\_src\_build_hit_cue.py`）

1. 每个图层按 `layer.offset` 合成回 524×646 全画布 → 9 帧。
2. **大小**：PSD 画的人物比待机源视频大约 **22%**（金发像素面积 55.2k vs 37.2k，线性约 1.22×），
   所以 hit 的缩放用 **1.0**（不是待机的 1.22047），让头部/身体与待机同大；生成后金发面积比 1.04，匹配。
3. **画布/接地**：600×820；人物水平居中；最低脚底 y=566 → 画布 y=815（与待机站立帧同一地面线）。
   第一帧本身是受击蹲姿，所以整体比 idle 低，这是原图姿态，不是缩放错。
4. **边缘**：alpha bleed + premultiplied Lanczos4 + 轻度 `G=min(G,max(R,B))`；最终不透明像素绿差 0。
5. **时间**：用 `@esotericsoftware/spine-core` 4.2 读原版 `ironclad.skel`，`hurt` 时长 **1.0s**
   （Silent 0.7333s，作参考）。序列顺序 **1→3→5→7→8→9→8→7**（回弹）；前 7 个条目各 **1 槽**（0.0417s），最后的 7 占 **17 槽**（0.708s）；总 24 槽 = **1.0s**。
6. **调速**：`HitSpeed` 默认 1；总时长 = 1.0 / HitSpeed。改 `HitFrames` 的单帧 Hold（保持总和 24）可改停顿节奏。

**接入**

- `VisualCueSet` 的 `hit` 从 `.Single("hit.png")` 改成 `.Sequence("hit", ...)`；状态机 `hit` 仍是
  `WithNext("idle")`，非循环，播完回 idle。
- 卡牌分流补丁只压制 `Attack/Cast/PowerUp`，**不压制 `Hit`**；受击触发照常。
- `HitSpeed` 在 `STS2 MomoiCharacter.cs` 顶部；状态机日志会打印 `h={HitSpeed}`。

**产物**

- `images\characters\cue\hit.png` + `hit_01..08.png`（9 帧，600×820，无损导入）。
- `工作区\编辑区\人物\_work\hit_manifest.json`（9 帧、holds、1.0s、scale/crop）、
  `hit_contact.png`、`hit_vs_idle_dark/white.png`（大小对照）。
- `dotnet build` **0 错误**，DLL **453,120 B** / PCK **109,990,924 B**（10-18 13:51）；
  PCK **848 条目 md5 全通过**。
- `_verify_batch26.py` **24 条全绿**；十七套合计 **718 条**（原 694 + 24）。

**注意**

- 受击 9 帧是 PSD 的 9 个关键姿势，1.0s 内播放会比 Spine 的插值动画更“关键帧感”；想更顺可以加中间帧/光流。
- 想整体更快/更慢改 `HitSpeed`；想只改某几帧停顿改 `HitFrames` 的 Hold。
- 技能牌暂不播技能动画：`Choose()` 对非 Power/非攻击/非 Taunt/Win/Concept 返回 `null`，保持 idle；等技能动画做好后在这里加分支。
- `dead.png` / `relaxed.png` 仍是线稿占位；旧 `attack.png`/`cast.png` 仍保留但未引用。
- 如果觉得受击整体偏下/偏大，改 `_build_hit_cue.py` 的 `SCALE` 或接地对齐后重跑三步。

### 21.30 批次27：游戏人生标签作用域、六张数值卡、三处 UI 文本（2026-10-20）

> 本批是**卡牌调整**穿插在角色动画期（批次 24~26）里的一次实操反馈批。

#### 1. 🔴 游戏人生：游戏牌标签跨战斗 / 跨局残留

**现象**：上一把用「游戏人生」给「打击」等牌加的「游戏牌」标签，新开一局还在（`MinigameSupport.IsMinigameCard` 仍为真）。

**真因**：`CardModel.CloneForCombat` **不重建 `_tags`** —— 战斗克隆体的 `_tags` 与牌组本尊**共用同一个 `HashSet`**。
所以 `AddModCardTag(手牌那张)` 实际上写进了**牌组本尊**，打完这场还在，并且随存档进到下一局。

**修法**（不再碰卡的持久状态）：

```csharp
// Cards\MinigameSupport.cs
private static readonly HashSet<CardModel> TemporaryGameCards = new(ReferenceEqualityComparer.Instance);
public static void MarkTemporaryGameCard(CardModel card) => TemporaryGameCards.Add(card);
public static bool IsTemporaryGameCard(CardModel card) => TemporaryGameCards.Contains(card);
public static void ClearTemporaryGameCards() => TemporaryGameCards.Clear();

public static bool IsMinigameCard(CardModel card) =>
    card.Tags.Contains(Tag) || card.Tags.Contains(FullGameTag) || IsTemporaryGameCard(card);
```

- 读标签的地方统一走 `IsMinigameCard` / `IsTemporaryGameCard`：`Patches\CardKeywordLabelPatch.cs`（金色顶行「游戏牌。」）
  与 `Patches\MinigameSidebarPatch.cs` 都已补上。
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

---

### 21.31 批次28：死亡 AE 底稿 + relaxed 休息点 + 像素 UI + 选人视频背景（2026-10-21）

> **2026-10-22 后续**：本节的“relaxed 休息点”已改成“relaxed 商店”；休息处改用 `休息处.png`；死亡节奏也重调为 **2.0833s**。以 **§21.33** 为准；本节保留 10-21 的原始记录。

#### 1. 死亡动画 AE 底稿（**只出 AEP，不进 mod**）

源：`工作区\编辑区\人物\死亡动画底图.psd`（1187×1126，两层；第 2 层「死亡动画变灰」虽然隐藏，但像素和第 1 层相同，**不是真灰度**）。

产物：**`工作区\编辑区\人物\死亡动画.aep`**
- comp **`死亡动画`**：**1920×1500 / 24fps / 2.583333s**（比原版铁甲战士 death 略长，给抽动留时间）。
- 人物层用 PSD 的可见层；`anchor=(594,1084)`（脚底）、`position=(1400,1150)`、初始 `rotation=0`；另加一条 **guide layer**「Preview Guide (not rendered)」和深色 comp 背景，方便审阅。
- **灰化**：AE 的 `ADBE Black&White` 是颜色混合器，不是去饱和；改用 **`ADBE Tint`**（Map Black→纯黑、Map White→纯白），把 **Amount to Tint** 从 **0** 线性拉到 **100**（0.10s→1.15s），得到真灰度。
- **原地抽动**：4 个 burst（0.15 / 0.45 / 0.75 / 1.05s），每个约 0.16s，位置 ±24px、旋转 ±3°，线性插值；脚底 anchor 不跑位。
- **倒下**：1.28s / 1.32s 保持 0°，2.12s **-90°**，2.18s 过冲 **-93°**，2.30s 回 **-90°** 并保持到结尾；负角度 = AE 的**逆时针**，绕脚底向后倒。
- **末帧**：PSD 层 `outPoint` 原为 comp duration，渲染最后一帧会空；已延长到 `duration+1.0`，末帧稳定显示倒地的灰化人物。
- 审阅：`_work\death_preview.gif`、`_work\death_preview_sheet.png`、`_work\death_final_frame.png`。
- **未部署**：mod PCK 里没有 `.aep` / 死亡动画文件；`dead.png` 仍是线稿占位。以后接入时按 `dead.png` + `dead_01..` 序列渲染，不要把 AEP 塞进 PCK。

> AE 脚本环境备注：本机 AE 的崩溃恢复弹窗会卡住 `app.newProject()`；可靠做法是 `AfterFX.exe -noui -r script.jsx`，脚本第一行先 `app.open(一个有效 AEP)`，再新建 comp / 导入 PSD。构建脚本会在保存前清掉 `relaxed动画1&2交替频率参考.aep` 的 3 个参考项（先删 comp 再删 footage）；当前 AEP 只剩 `死亡动画` comp、`死亡动画底图.psd` 和 guide。

#### 2. relaxed：休息点两张图交替

源：`工作区\编辑区\人物\relaxed动画1&2.psd`（340×444，两个可见姿态）+ `relaxed动画1&2交替频率参考.aep`（comp `12交替频率`，**2.29157118453398s**）。

- 管线 `_src\_build_relaxed_cue.py`：裁 `(14,23,326,418)`、scale **1.325897**、输出 **600×820**、脚底约 **814**；产出 `cue\relaxed.png` / `cue\relaxed_2.png`；`_work\relaxed_manifest.json` 记录 `cycle_seconds=2.29157118453398`、`frame_seconds=1.1457856`。
- 战斗 `VisualCues`：`.Sequence("relaxed", …)`，两张各 `1.1457856 / RelaxedSpeed` 秒，`Loop()`；`RelaxedSpeed` 默认 1。
- **休息点**（真正在游戏里看到的）：`scenes\characters\STS2_Momoi_rest_site.tscn` 的 `Visuals` 改 **Sprite2D + `scripts\momoi_rest_site_visuals.gd`**；`scale=(0.75,0.75)`、`position=(0,-261)`，让 600×820 画布里的人物头顶约 **-347**、脚底约 **42**，正好落在原版休息点 hitbox 的上沿/地面附近；`hitbox` 调到 `(-160,-350)-(160,80)`；旧的假 `Shadow` 删除。GDScript 每 **1.1457856 / speed** 秒交换 `texture`，`speed` 可在场景里调。
- Headless 验证（Godot 4.5.1）：加载场景后 0s / 1.2s / 2.4s 的 `Visuals.texture` 依次为 `relaxed.png` → `relaxed_2.png` → `relaxed.png`。

#### 3. 像素小桃 UI 头像

源：`工作区\编辑区\人物\像素小桃.png`（160×167 RGBA，可见 bbox 113×154）；管线 `_src\_build_pixel_avatar.py`。

| 文件 | 尺寸 |
|---|---|
| `STS2_Momoi_character_icon.png` | 88×88 |
| `STS2_Momoi_character_icon_outline.png` | 88×88 纯白剪影 |
| `STS2_Momoi_character_select.png` | 132×195 |
| `STS2_Momoi_character_select_locked.png` | 132×195 灰度/压暗 |
| `STS2_Momoi_map_marker.png` | 49×64 |

旧占位备份在 `工作区\编辑区\人物\_work\placeholder_avatar_backup\`；预览 `_work\pixel_avatars_preview.png`。

#### 4. 选人界面：两段视频背景 + 音效接口

源：`工作区\编辑区\人物\选人界面1&2.aep`（comp 932×720；1 是 0~10.79s，2 是 74.54~79.54s；源视频右上角有 `SechiAnimation bilibili` 水印，在平墙上）。

- 视频：`ffmpeg` 裁掉顶部 **70px**（`crop=932:650:0:70`）→ 放大 **1721×1200**，24fps，`libtheora -q:v 8`，无音轨；产物 `videos\select_bg_1.ogv`（10.79s / ~2.6MB）、`select_bg_2.ogv`（5s / ~1.76MB）。
- 场景：`scenes\characters\STS2_Momoi_character_select_bg_1.tscn` / `_bg_2.tscn`；根 Control 全屏，2560×1200 的 `TextureRect` 模糊底图 + 1721×1200 的 `VideoStreamPlayer`（`autoplay=true`、`loop=true`、`expand=true`、`mouse_filter=2`）。模糊底图在 `images\characters\select_bg_1_blur.png` / `_2_blur.png`（2560×1200）。
- C#（`STS2 MomoiCharacter.cs`）：`SelectBg1ScenePath` / `SelectBg2ScenePath`；`static int? _selectVariant` + `SelectVariant => _selectVariant ??= Rng.Chaotic.NextInt(2)`，两个背景各自绑定固定 BGM。`SelectSfxVariants` 占位已删除；`CustomCharacterSelectSfx` / `CustomCharacterTransitionSfx` 返回 null，避免回退铁甲战士音效。
- **重置**：`Patches\MomoiSelectVariantPatch.cs` 前缀 `NCharacterSelectScreen._Ready` → `ResetSelectVariant()`，每次进选人界面重新成对随机。
- **预载**：`Patches\MomoiSelectBgPreloadPatch.cs` 在 `CharacterModel.get_AssetPathsCharacterSelect` 后追加两个背景场景，避免随机到未预载的那个时同步加载卡顿。
- `Entry.cs` 补丁总数 **18**；启动日志 `18 applied, 0 ignored, 0 failed`。

#### 5. 产物 / 验证

- `dotnet build` **0 错误** → DLL **456,704 B** / PCK **115,427,764 B**（10-21 00:05）；PCK **864** 条目，含两段 `.ogv`、两个选人 `.scn`、`momoi_rest_site_visuals.gdc`、`relaxed*.ctex`、像素头像 `.ctex`。
- 启动日志：18 个补丁全成功、`STS2_Momoi initialized`；旧占位头像不再被引用。
- `_verify_batch28.py` **102 条**：死亡 AEP 未部署 / 末帧非空、relaxed 尺寸与半周期、休息点场景/脚本、像素头像尺寸、选人场景/视频/变体/patch、PCK 条目、启动日志、文档同步。
- 待办：`dead` 接入（把 AEP 渲成 `dead` 序列）；技能牌动画；能量球 5 层 + `energy_big`/`energy_text`；商店立绘；左上角头像场景；多人手臂/转场/音频。

### 21.32 批次29：跑酷删 power、七张数值卡、专注重做（2026-10-22）

#### 1. 跑酷！：删掉「回合开始时重复」，power 一并删除

原效果 = 打出时选一张 + 挂一个 power，每回合开始重复到受伤为止。按需求只留前半段：

- **删代码**：`ParkourPower` / `ParkourUpgradedPower` / 抽象基类 `ParkourPowerBase`（含 `BeforeHandDraw` 重复逻辑与 `AfterDamageReceived` 停止逻辑）全删；
  `OnPlay` 只 `await PickOne(...)`。
- **删死资源**：`images/powers/parkour_power.png`（+`.import`）、`powers.json` 里 6 个 `PARKOUR_POWER*` / `PARKOUR_UPGRADED_POWER*` 键（中英各 6 条）。
- **删本地化文本**：卡面第二行「在你的回合开始时，重复此效果，直至你受到伤害或失去生命。」（中英同步）。
- 现在是 **0 费一次性**（`消耗` 由 `CanonicalKeywords` 自动追加）：从 5 张随机特定牌里**选最多一张**（`MinSelect=0` 可跳过），本{回合|场战斗}免费。

#### 2. 六张卡的数值

| 卡 | 改动 |
|---|---|
| **WIN！** `WinCard` | 能量 4/6 → **3（升级 4，+1）** |
| **火焰附加** `FlameAttach` | 灼烧 1/2 → **2（升级 3）** |
| **热身** `WarmUp` | 火力 1/2 → **2（升级 3）** |
| **构想之矛** `ConceptSpear` | 伤害 8/11 → **10（升级 14，+4）** |
| **博览群游** `ExperienceCombo` | 伤害 8/11 → **7（升级 9，+2）** |
| **再起新篇** `NewChapter` | 活力 2/3 → **3（升级 4）** |

#### 3. 稀有度

- **瓶颈突破** `BottleneckBreak`：罕见 → **普通**
- **玩玩新作！** `Salvage`：普通 → **罕见**

#### 4. 专注：连续 2 回合 → 本回合

**旧**：`TurnsNoMinigame` / `TurnsNoConcept` 两个计数器累加，要求「连续 2 个回合」都没打出；
**新**：两个 bool（`PlayedMinigameThisTurn` / `PlayedConceptThisTurn`），**每个回合结束时各判定一次**：

| 判定 | 效果 |
|---|---|
| 本回合没打出过**小游戏牌** | 构想数值 +1（按层数叠加 `Amount`） |
| 本回合没打出过**构想** | 可选择最多（构想数值）张手牌**保留** —— 在 `BeforeSideTurnEnd`（弃牌前）判定 |
| 回合结束 | 两个标记重置 |

耗能 **0**（升级前后都是 0，`OnUpgrade` 因此没有内容）。卡面文本按用户给的措辞：

```
在你的回合结束时，若你本回合没有打出过[gold]小游戏牌[/gold]，使[gold]构想[/gold]数值+1。
在你的回合结束时，若你本回合没有打出过[gold]构想[/gold]，可选择最多[gold]构想[/gold]数值张[gold]手牌[/gold][gold]保留[/gold]。
```

power 文本同步（`{Amount}` / `{RetainCount}` 保留，小游戏牌/构想/手牌/保留 都染金）。

#### 5. ⚠ 自检脚本覆盖事故与恢复

本批新建自检时用了 `_verify_batch28.py`，与 **10-21 会话（批次28：死亡AE/relaxed/像素头像/选人背景）** 的同名脚本冲突 → 原文件被覆盖。
处理：

1. 本批脚本改名为 **`_verify_batch29.py`**（批次号对齐）。
2. 按 §21.31 与磁盘实测**重建** `_verify_batch28.py`（本批跟进已重写为 **82 条**：死亡节奏/商店 relaxed/休息处新图/像素头像/选人背景/PCK/文档）。
3. 一并重建 10-17 会话丢失的 `_verify_batch24.py`（26 条：42 张 idle 帧 / 600×820 RGBA / 无损导入 / IdleLoop·IdleOutro·三个倍率 / 开场主动播 idle）。
4. **发现**：当时 `工作区\编辑区\人物\死亡动画.aep` 本体不在磁盘（只剩 `死亡动画.aep 日志` 目录与 `_work\death_*` 预览/分层图）；**2026-10-22 跟进已按新节奏重建 AEP（§21.33）**，当前 `_verify_batch28.py` 已改为断言 AEP 存在 / 节奏脚本 / 未部署 / 末帧。

**教训**：新建自检脚本前先 `ls 工作区/_scripts/_verify_batch*.py` 看号段；本项目批次号已跨会话交叉使用（24~26 动画 / 27 卡牌 / 28 动画 / 29 卡牌）。

#### 6. 产物

- `dotnet build` **0 错误** → DLL **454,656 B**、PCK **115,402,920 B**（10-22 02:20）。
- `_verify_batch29.py` **35 条全绿**；**二十套合计 831 条断言全绿**。
- 同步修正的旧断言：`batch9`（PARKOUR power 行 / 吃豆人文本）、`batch11`（孤儿图标）、`batch14`（跑酷拆 power 一节改「已删除」）、
  `batch22`（专注改 0 费）、`batch27`（跑酷 power 文本 → 已删除）；`_power总览.md` 重生成（**52 个 power**）。

---

### 21.33 批次28 后续：relaxed 商店 / 休息处新图 / 死亡节奏重调（2026-10-22）

#### 1. relaxed 重新应用：从修改后的 PSD 重导出

- 源：`工作区\编辑区\人物\relaxed动画1&2.psd`（用户 2026-10-21 16:28 修改）→ 重跑 `_src\_build_relaxed_cue.py`。
- 输出仍是 `cue\relaxed.png` / `cue\relaxed_2.png`，**600×820**，脚底 814，scale 1.325897；`_work\relaxed_manifest.json` 半周期 **1.1457856s**、循环 **2.291571s**。
- 战斗 `VisualCues` 仍保留 `relaxed` 两张循环（`RelaxedSpeed`）；本批实际使用点是**商店**。

#### 2. 商店（merchant）：缩小 + 上移 + 坐上圆形地毯

- `scenes\characters\STS2_Momoi_merchant.tscn` 的 `Visuals` 改为 **Sprite2D + `scripts\momoi_merchant_visuals.gd`**：
  - `texture = relaxed.png`，两张每 **1.1457856 / speed** 秒交替；
  - `scale=(0.45,0.45)`（旧像素占位是 132×195×1.25 ≈ 244 高；relaxed 0.45 可见高约 233，**更小**）；
  - `position=(0,-182)`：可见脚底约 **0**（旧像素脚底约 26，**上移 26px**），人物身体在圆形地毯上，脚/腿落在毯面。
- Headless 验证：加载商店场景后 0s / 1.2s / 2.4s → `relaxed.png` → `relaxed_2.png` → `relaxed.png`。

#### 3. 休息处：改用 `休息处.png`，不再 relaxed

- 源：`工作区\编辑区\人物\休息处.png`（1000×1000，可见 bbox `(184,235)-(788,763)`）→ 复制为 `images\characters\rest_site.png`。
- `scenes\characters\STS2_Momoi_rest_site.tscn`：
  - `Visuals` 静态 Sprite2D，`texture=rest_site.png`；
  - `scale=(0.65,0.65)`、`position=(10,42)`；可见范围约 `x=-195..197, y=-130..213`，铺在休息处圆形地毯上；
  - `Hitbox` 扩到 `(-220,-160)-(220,245)`，`SelectionReticle` 扩到 `(-230,-180)-(230,260)`；
  - **移除** `momoi_rest_site_visuals.gd`、relaxed 纹理引用和旧 `Shadow`；ThoughtBubble 改到头附近 `(85,160)` / `(-85,140)`。

#### 4. 死亡 AE：抽搐加快、灰化提前、停 0.5s、快速倒下

- 重建 `工作区\编辑区\人物\死亡动画.aep`：comp **死亡动画 / 1920×1500 / 24fps / 2.083333s（50 帧）**；AEP 只剩死亡 comp、PSD、guide（参考项已清理）。
- **抽搐**：4 段连续，`0.10 / 0.20 / 0.30 / 0.40s` 起，每段 **0.10s**（5 key × 0.025s），段间**无间隔**；总 0.10–0.50s。位置 ±24px、旋转 ±3°，脚底 anchor 不动。
- **灰化**：`ADBE Tint` Amount **0 → 100** 在 **0.10–0.30s** 完成，正好是抽搐一半；之后保持全灰。
- **停顿**：**0.50–1.00s** 原地静止 0.50s。
- **倒下**：1.00s 起，1.02s 保持 0°，**1.42s -90°**，1.48s 过冲 **-93°**，1.58s 回 -90° 并保持；比旧版 1.28–2.30s 快约一半。
- 审阅：`_work\death_preview.gif` / `death_preview_sheet.png` / `death_final_frame.png`；**未部署**，PCK 无 AEP，`dead.png` 仍是占位。

#### 5. 产物 / 验证

- `dotnet build` **0 错误** → DLL **454,656 B** / PCK **115,635,600 B**（10-22 02:25）；PCK **864** 条目，含 `momoi_merchant_visuals.gdc`、`rest_site.png.import`/ctex、两段 `.ogv`、两个选人 `.scn`、`relaxed*.ctex`；不含旧 `momoi_rest_site_visuals`、不含 AEP。
- 启动日志 **18 applied, 0 ignored, 0 failed**；`STS2_Momoi initialized`。
- `_verify_batch28.py` **82 条全绿**（死亡节奏/商店 relaxed/休息处新图/像素头像/选人背景/PCK/文档）；二十套合计 **867 条断言全绿**。
- 待办：选人音效槽；`dead` 接入；技能牌动画；能量球/左上角头像/多人/转场/音频。

### 21.34 批次30：专注 1 费 + 文本并成一句、天马行空升级版补「+1」（2026-10-22）

#### 1. 专注：耗能改回 1 费（升级 0 费）

上一批我按「升级前后都 0 费」改过头了，用户更正为 **1 费 / 升级 0 费**：
`base(1, …)` + `OnUpgrade → EnergyCost.UpgradeBy(-1)`。

#### 2. 专注：卡面 / power 文本并成一句

旧写法把「在你的回合结束时」说了两遍，字数过多。照**蒙太奇**那种「A/B，X/Y」的写法合成一句：

```
在你的回合结束时，若你本回合没有打出过[gold]小游戏牌[/gold]/[gold]构想[/gold]，使[gold]构想[/gold]数值+1/选择最多[gold]构想[/gold]数值张牌[gold]保留[/gold]。
```

**power 侧**同句式，只把两个数字换成变量（**保留张数仍显示实际数值** —— 用户一开始就要求「最多构思数值张」的数值要实时显示）：

```
在你的回合结束时，若你本回合没有打出过[gold]小游戏牌[/gold]/[gold]构想[/gold]，使[gold]构想[/gold]数值+[blue]{Amount}[/blue]/选择最多[blue]{RetainCount}[/blue]张牌[gold]保留[/gold]。
```

- `{RetainCount}` 的刷新逻辑没动（`AfterCardPlayed` 与 `BeforeSideTurnEnd` 各写一次当前构想数值）。
- 效果判定仍是「**本回合**」两个 bool（批次29 的改法），只改文案。
- 按新措辞去掉了旧文本里的「[gold]手牌[/gold]」（用户写的是「张牌」）。

#### 3. 天马行空：升级版卡面补「+1」

实际效果本来就是「构想数值 + 升级 +1 次」（`HitsBase` 0 → 升级 +1），只是升级版卡面漏了这个 +1：

```
对所有敌人造成{CalculatedDamage:diff()}点伤害。
额外攻击等同[gold]构想[/gold]数值{IfUpgraded:show:+1|}次。（额外攻击{ExtraHits:diff()}次）
```

升级前不显示（`{IfUpgraded:show:+1|}` 的空分支），代码未改。

#### 4. 产物

- `dotnet build` **0 错误** → DLL **454,656 B**、PCK **115,635,008 B**（10-22 04:29）。
- `_verify_batch30.py` **21 条全绿**；二十一套合计 **889 条断言全绿**。
- 同步修正旧断言：`batch22`（专注 1 费 + 升级 -1）、`batch29`（专注费用与「单句」结构、power 关键词不再含「手牌」）。

> 注：`_verify_batch28.py` 已由 10-22 的动画会话改写为 82 条的「死亡节奏/商店 relaxed/休息处新图」版本，本批未动它。

---

### 21.35 批次31：死亡动画 50 帧接入 + 能量图标/手臂尺寸（2026-10-22）

#### 1. 死亡动画接入

- **AEP 保持源工程**：`工作区\编辑区\人物\死亡动画.aep`（2.0833s / 50 帧，抽动 0.10–0.50s 无间隔、灰化 0.10–0.30s、停 0.50–1.00s、倒下 1.00–1.58s）。
- **渲染透明帧**：复制 AEP 并删除 guide 层（`death_alpha.aep`），`aerender` 输出 1920×1500 TIFF；AE 的 TIFF 是 **RGB + 未指定 alpha**，`PIL` 会丢 alpha，必须用 `tifffile` 读 4 通道。
- **统一画布**：AEP 人物可见高度 **1010px**（y=140..1149），idle 可见高度 **617px**（y=198..815）→ scale **0.610891**；画布 **1400×1250**，人物脚底放在 **y=1030**、身体中心 **x=700**。场景 `Visuals` 的 scale 0.6 下：
  - 头顶/脚底与 idle 完全对齐（`scene_ground=-3`）；
  - 倒地后身体向左延伸到画布 x≈83，1400 宽足够；y≈829..1229，1250 高足够。
- 产物：`cue\dead.png` + `cue\dead_01..49.png`，共 **50 张 1400×1250 RGBA**（约 9.6MB）。
- C#：`DeadFrameCount = 50`、`DeadSpeed = 1f`，`VisualCues` 的 `dead` 从 `.Single(...)` 改为 `.Sequence("dead", …)`，每帧 `1/24/DeadSpeed` 秒，不循环，末帧保持；状态机 `dead` 仍是终止状态。
- 预览：`_work\dead_cue_sheet.png`、`_work\dead_vs_idle.png`。
- **AEP 本体不进 PCK**；PCK 含 50 个 `dead*.png` 导入条目/ctex。死亡动画已可在游戏里触发（`Dead` → `dead`）。

#### 2. 能量图标尺寸（回答）

| 用途 | 文件 | 尺寸 | 说明 |
|---|---|---|---|
| 小 / 文本能量图标 | `energy_text.png`（`TextEnergyIconPath`） | **24×24** | 用户给的 `momoi_energy_icon.png` 就是这个小图标；已替换进 mod |
| 大能量图标 | `energy_big.png`（`BigEnergyIconPath`） | **256×256** | 需要重新做；当前仍是铁甲战士占位 |
| 能量表盘 5 层 | `energy_orb_layer_1..5` | **256×256** ×5 | 可选；做完整动态表盘才需要 |

参考原版：
- `C:\Users\asus\Desktop\Slay the Spire 2\images\packed\sprite_fonts\ironclad_energy_icon.png` = **24×24**；
- `...\images\ui\combat\energy_counters\ironclad\ironclad_orb_layer_1..5.png` = **256×256**；
- 所以「一大一小」= **24×24（小/文本）+ 256×256（大）**。小图标已接；大图标等新图。

#### 3. 原版手臂参考尺寸（回答）

**多人模式手臂**（`CharacterMultiplayerAssetSet` 的 4 张）：
- 原版：`C:\Users\asus\Desktop\Slay the Spire 2\images\ui\hands\multiplayer_hand_<角色>_{point,rock,paper,scissors}.png`
- 铁甲战士版全部 **422×1200 RGBA**；小桃的 4 张按这个尺寸/画法做即可。

**商店手臂**：
- 不在 `images\` 里；它是 **Spine**（`NMerchantHand`，`rotate_me` 骨骼），位于：
  - `...\animations\backgrounds\merchant_room\hand\merchanthand.png` = **1664×916**
  - `...\merchanthand_2.png` = **840×1972**
  - `.atlas` 里 `arm` 区域 `415×1175`（rotate 90）、`sleeve` `475×516`、`shadow` `492×1180`，atlas `scale:0.6`
  - fake merchant 版 `fakemerchanthand.png` = **848×671**（区域 `335×844`，scale 0.4）
- 商店手臂不是一张可直接替换的 422×1200 静态图；要改需要替换/覆盖 Spine 资源或改 `NMerchantHand` 相关场景，不能只靠 `CharacterAssetProfile`。
- 参考联系表：`_work\arm_reference_sheet.png`（4 张多人手臂 + 3 张商店手 atlas 页）。

#### 4. 产物 / 验证

- `dotnet build` **0 错误** → DLL **454,656 B** / PCK **120,245,976 B**（10-22 18:55）。
- PCK **956** 条目；含 50 个死亡帧、`energy_text`/`energy_big` ctex、4 张多人手势、商店 `momoi_merchant_visuals.gdc`、休息处 `rest_site.png`、两段选人视频；不含 AEP。
- 启动日志 **18 applied / 0 failed**。
- `_verify_batch28.py` **92 条全绿** + `_verify_batch32.py` **40 条全绿**；**二十二套合计 939 条断言全绿**。
- 待办：大能量图标 256×256；5 层能量表盘（可选）；技能牌动画；左上角头像场景；选人音效；多人手臂/商店 Spine 可选；转场/音频。

---

### 21.36 批次32：王小桃身份/头像/能量/多人手势/镜像 + 文本/卡框参考（2026-10-23）

#### 1. 角色身份与选择界面

- 中文名正式 **王小桃**；英文名 **Momoi**；初始生命 **72**（`StartingHp => 72`）。
- `localization/zhs|eng/characters.json`：
  - `title` / `titleObject`：王小桃 / Momoi
  - `description`：游戏开发部的编剧，爱玩给木。/ The Game Development Club's writer, who loves games.
  - `flavor`：或许她真的能成为游戏王。/ Perhaps she really can become the King of Games.
  - `selectMessage`：同 description。
  - 代词统一为 她 / she、她的 / her。
- `NameColor` 改为桃红 `#F08CB8`（`STS2_MomoiCharacter.MomoiPink`）。

#### 2. 左上角头像

- 新增 `scenes/characters/STS2_Momoi_icon.tscn`：根 `TextureRect`，贴图 `STS2_Momoi_character_icon.png`（像素小桃），`expand_mode=1` / `stretch_mode=5` / `mouse_filter=2`。
- `CharacterUiAssetSet.IconPath` 指向这个场景；之前没写，回退到铁甲战士 `ironclad_icon.tscn`，所以左上角一直是战士。

#### 3. 能量图标三种 + 桃红数字

| 用途 | 文件 | 尺寸 | 接入 |
|---|---|---|---|
| 卡面文字内联 | `energy_text.png`（`TextEnergyIconPath`） | **24×24** | 用户 `momoi_energy_icon.png` |
| 卡面左上角（静态） | `energy_big.png`（`BigEnergyIconPath`） | **256×256** | 用户 `momoi_energy_icon_big.png` |
| 战斗左下角（原动态） | `STS2_Momoi_energy_counter.tscn` | 128×128 显示 | 改成**单张静态** `energy_big`，`RotationLayers` 留空，不再 5 层/旋转 |

- `STS2_Momoi_energy_counter.tscn` 保留 `%Layers` / `%RotationLayers` / `%EnergyVfxBack/Front` / `Label` 节点，`Layers` 只有一张 256×256 `energy_big`。
- 原版 5 层 `STS2_Momoi_energy_orb_layer_1..5.png` 已删除（不需要旋转点）。
- **数字颜色**：按原版机制改的是 `EnergyLabelOutlineColor`（角色）和 `CardPoolModel.EnergyOutlineColor`（卡面），都设为 **桃红 `#F08CB8`**；数字填充仍是原版奶油色，描边呈桃红。
- 若以后要数字填充也变桃红，需要额外 patch `NEnergyCounter.RefreshLabel` / `NCard` 的 `FontColor`；本批未做。

#### 4. 多人模式手势（4 张）

- 用户文件 → `images/characters/`：
  - `point.png` → `STS2_Momoi_arm_point.png`
  - `rock.png` → `STS2_Momoi_arm_rock.png`
  - `scissors.png` → `STS2_Momoi_arm_scissors.png`
  - `paper.png` → `STS2_Momoi_arm_paper.png`
- 全部 **422×1200 RGBA**，与原版 `images/ui/hands/multiplayer_hand_ironclad_*.png` 一致。
- `CharacterAssetProfile.Multiplayer` 已填 4 条路径；指向/猜拳会走小桃的手。

#### 5. 多人篝火右半场镜像

- 原版 `NRestSiteRoom` 对 `i % 2 == 1` 的玩家调用 `NRestSiteCharacter.FlipX()`；`FlipX()` 翻转的是 `ControlRoot` 和 Spine 子节点。
- 我们的 `STS2_Momoi_rest_site.tscn` 之前把 `Visuals` 放在根下，不在 `ControlRoot` 里，所以右侧 2/4 号位只翻了 Hitbox/UI，人物图没翻。
- 已把 `Visuals` 移进 `ControlRoot`（仍 `position=(10,42)`、`scale=(0.65,0.65)`）；右侧玩家现在会随 `ControlRoot.Scale.X=-1` 水平镜像。
- Headless 验证：设置 `ControlRoot.Scale=(-1,1)` 后 `Visuals` 的全局变换为横向镜像（Godot 分解显示为旋转 180°+纵向负缩放，矩阵等价）。

#### 6. 文本/卡框参考

- 新增 **`工作区\_docs\_文本参考_王小桃.md`**：
  - 角色选择字段；
  - 桃红 `#F08CB8` / `[color=#F08CB8]` 规则；
  - 先古之民 `ancients.json` 的 key 结构、已有 ID、DARV 示例；
  - 色彩哲学家 `ColorfulPhilosophers.cs` + `events.json` 的选项结构，以及加入 `STS2_MOMOI` 需要 patch `CardPoolColorOrder` 的提醒；
  - 事件 `{character}`/`[gold]`/`[blue]` 用法。
- 新增 **`工作区\_docs\_卡框参考.md`**：
  - 原版 `card.tscn` 的 `%Frame` 300×422；类型帧 atlas 区域 598×844（ancient 618×862）；`card_frame_sdf.exr` + HSV 材质；
  - 原版红/蓝/绿/橙/粉材质；当前模组 `PoolFrameMaterial` 仍是蓝色 HSV 0.42/0.65/0.72；
  - 三条设计路线（只换 HSV / 自定义材质 / 完全自定义形状）和桃红建议。
- 卡框参考图：`工作区\编辑区\人物\_work\card_frame_reference.png`（attack/skill/power/quest/ancient 五张原版帧）。

#### 7. 视觉占位审计（本批后）

> 后续批次33已把卡框改为粉蓝渐变；以下为批次32时状态，当前剩余见 §21.37。

**仍需要补的视觉**：

1. **卡框**：仍是原版 attack/skill/power/quest 形状 + 蓝色 HSV 换色（`PoolFrameTintMaterial`）；没有小桃专属花纹/角花。
2. **选人转场**：`CharacterSelectTransitionPath` 未写，回退铁甲战士的 transition 材质。
3. **卡牌拖尾**：`TrailPath`/`TrailStyle` 未写，回退原版拖尾。
4. **音频**：按用户要求最后做；目前全部回退原版（不属于视觉，但一并列出）。
5. **商店手臂**：是商人本人的 Spine，不是角色；按用户确认**不改**。

**已清理/不再算占位**：

- 5 层能量球贴图（已删除，改用静态大图）。
- 旧 `attack.png` / `cast.png`（已删除；cue 目录现在 208 张全是真帧）。
- 旧 `STS2_Momoi_character_select_bg.tscn`（已删除；实际用 `_bg_1/_2` 两段视频）。
- 左上角头像、能量小/大图标、4 张多人手势、休息处、商店、卡框之外的选人图/地图标记均为小桃自己的资源。

#### 8. 产物 / 验证

- `dotnet build` **0 错误** → DLL **455,168 B** / PCK **120,090,016 B**（10-23 00:06）；PCK 956 条目；18 补丁。
- `_verify_batch28.py` 需同步 256 大图标/静态表盘/头像场景/手势/镜像；本批新增自检见 `_verify_batch32.py`（若存在）。
- 卡框设计落地前，先按 `_卡框参考.md` 选路线 A/B/C。

---

### 21.37 批次33：描述两行 / 能量微调 / 海玻璃 / 色彩哲学家 / 设置页（2026-10-23）

#### 1. 选择界面描述与 `flavor`

- 原版 `NCharacterSelectScreen` 只读：
  - `CharacterSelectTitle = <CharacterId>.title`
  - `CharacterSelectDesc = <CharacterId>.description`
  - 具体赋值在 `NCharacterSelectScreen.cs`：`_description.Text = new LocString("characters", characterModel.CharacterSelectDesc)...`
- **`flavor` 在当前原版选人界面没有任何读取点**；它只是本地化表里保留的备用字段（以后角色图鉴/其他界面可以接），所以改 `flavor` 不会显示在选择界面。
- 因此本批把两行都放进 `description`：
  ```text
  游戏开发部的编剧，爱玩给木。
  或许她真的能成为游戏王。
  ```
- 代词统一为 **她 / she、她的 / her**；`flavor` 仍保留第二行，方便以后接图鉴。
- `selectMessage` 设为两行同文（若未来其他 UI 读取）。

#### 2. 大能量图标：上移 12px + 数字加深

- `energy_big.png` 256×256：内容整体上移 **12px**，底部补透明；备份 `_work\energy_big_original.png`。
- 这会同时影响：
  - 卡面左上角静态大图标（上移 12px）；
  - 战斗左下角静态表盘（`Layer1` 再左移 4px、上移 2px）。
- 能量数字/卡池能量描边从 `#F08CB8` 加深为 **`#D95C97`**（`MomoiPink`）：
  - `EnergyLabelOutlineColor`
  - `CardPoolModel.EnergyOutlineColor`
  - 能量表盘 `Label` 的默认 `font_outline_color`
- 数字填充仍是原版奶油色；这是原版“数字 = 奶油填充 + 角色色描边”的机制。

#### 3. 海玻璃

- 原版 `SeaGlass.Title` 在 `CharacterId != null` 时读：
  `SEA_GLASS.<Character.Id.Entry>.title`
- 已新增中英文本：
  ```text
  SEA_GLASS.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.title = 给木玻璃 / Game Glass
  ```
- 奥罗巴斯的 `SeaGlassOptions` 会遍历 `ModelDb.AllCharacters`，本角色自动进入选项；设置关闭时由补丁过滤掉。

#### 4. 色彩哲学家

- 新增本地化（`localization\zhs|eng\events.json`）：
  ```text
  COLORFUL_PHILOSOPHERS.pages.INITIAL.options.STS2_MOMOI.title = 桃红色 / Peach Red
  COLORFUL_PHILOSOPHERS.pages.INITIAL.options.STS2_MOMOI.description =
    获得[blue]{Cards}[/blue]张王小桃的卡牌。 / Obtain [blue]{Cards}[/blue] cards from Momoi.
  ```
- `ColorfulPhilosophers.CardPoolColorOrder` 原版只列 5 个原版池；本模组用 Postfix 追加 `STS2_MomoiCardPool`，并在设置关闭时不追加。
- 选项 key 后缀来自 `EnergyColorName.ToUpperInvariant()`，即 `STS2_MOMOI`。

#### 5. RitsuLib 设置页 + 两个开关

新增 `STS2 MomoiCode\Settings\MomoiSettings.cs`：

- 数据类 `MomoiModSettings`（可继续加字段）：
  - `PhilosopherPool`，默认 true；
  - `SeaGlassPool`，默认 true。
- 持久化：`ModDataStore.For(Entry.ModId).Register<MomoiModSettings>(key:"settings", fileName:"settings.json", scope:Global, ...)`。
- 两个 `ModSettingsValueBinding<MomoiModSettings,bool>`，读取用 `.Read()`。
- `RitsuLibFramework.RegisterModSettings` 页面：
  - 标题「王小桃」；
  - 分区「通用」；
  - 开关「色彩哲学家出现该角色卡池」；
  - 开关「海玻璃出现该角色」。
- 以后要加“卡牌数值微调 / 是否生成新事件 / 只在选王小桃时遇到新事件”，只要在 `MomoiModSettings` 加字段、加 Binding、在页面加控件，再在对应逻辑里 `.Read()`。

补丁：

- `Patches\MomoiPhilosopherPoolPatch.cs`：`get_CardPoolColorOrder` Postfix；开启时 `.Concat([STS2_MomoiCardPool]).DistinctBy(p => p.Id)`。
- `Patches\MomoiSeaGlassPoolPatch.cs`：`get_SeaGlassOptions` Postfix；关闭时过滤 `Relic is SeaGlass && CharacterId == 王小桃`。
- `Entry.cs` 补丁总数从 18 → **22**；启动日志 `22 applied, 0 ignored, 0 failed`。

#### 6. 游戏内验证

- 通过临时 `steam_appid.txt` 直接启动游戏，日志：
  - `Patcher - core-patches: 22 applied, 0 ignored, 0 failed`
  - `KitLib FrameworkBridge ... 1 | 0 | — | 王小桃`（设置页标题）
  - 无 STS2_Momoi 相关 Harmony 失败。
- 说明两个新 Postfix 目标都被 RitsuLib 找到了，设置页也已注册。
- 临时 `steam_appid.txt` 已删除，游戏已关闭。

#### 6.5 卡框：左粉右蓝浅渐变

- 新增 `STS2 Momoi\STS2_Momoi\shaders\momoi_card_frame_gradient.gdshader` 和 `materials\momoi_card_frame_gradient.tres`。
- `STS2_MomoiCardPool.PoolFrameMaterial` 改为该材质（不再用蓝色 HSV）。
- 新增 `Patches\MomoiCardFrameMaterialPatch.cs`：拦截 `CardModel.get_FrameMaterial`，对 `STS2_MOMOI_` 开头的所有卡牌返回渐变材质。这样 TokenCardPool 里的技能/能力/支援牌也不会再是深色原版框。
- 新增 `Patches\MomoiCardFrameVisualPatch.cs`：`NCard.Reload` 后直接对 `%Frame` 赋材质。之前只改 `CardModel.FrameMaterial` 可能被 RitsuLib/其他 prefix 再次覆盖，实际画面不生效；这个兜底保证所有王小桃卡真正换材质。
- `BannerMaterial` / `PortraitBorder` 不动，稀有度横幅/边框仍按原版。
- 渐变：左 `#F5BFD6` → 右 `#BDD6FA`，用 `UV.x` 线性插值；只取原版卡框的亮度保留凹槽/高光/黑描边，不加任何图案元素。
- **三种类型（attack/skill/power）的外框都走完整渐变**；底部外框不再被正文遮罩压暗。
- 文字框/背景：深色底 + 少量渐变，原图较亮的文字框描边保留一点渐变；文字对比度优先。
- 稀有度框/稀有度条不经过这个材质，保持原版。
- 预览：`工作区\编辑区\人物\_work\momoi_card_frame_types_preview.png`（attack / skill / power 三张）。

#### 6.6 卡牌拖尾

- `CharacterAssetProfile.Vfx` 使用原版 `res://scenes/vfx/card_trail_ironclad.tscn`，只覆盖 `CharacterTrailStyle` 颜色：
  - 外轨迹 `#8FB8FF`（蓝，宽）
  - 内轨迹 `#F5A9C9`（粉，窄）
  - 大小火花/主副精灵分别用粉蓝中间色
- 没有新增拖尾贴图，形状/长度/行为与原版铁甲战士一致；视觉上是外蓝内粉的双色拖尾。
- 仍未做：**选人转场动画**；技能牌动画；音频最后做。商店手臂是商人 Spine，不改。

#### 6.7 开发经验总结

- 完整经验见 `工作区\_docs\_开发经验_卡框与拖尾.md`（CardAssetProfile 各部位、CardModel getter、卡框/拖尾调试顺序）。

#### 7. 产物 / 自检

- `dotnet build` **0 错误** → DLL **492,032 B** / PCK **128,360,432 B**（1053 条目，24 补丁）。
- `_verify_batch28.py` 97 条；`_verify_batch32.py` 117 条；二十五个脚本合计 **1085 条全绿**。
- 卡框已改为**左粉右蓝浅渐变**（三种类型外框全渐变，正文区深色+少量渐变），拖尾也改为外蓝内粉。仍未做的视觉：**选人转场动画**、技能牌动画；残血 BGM 已完成。商店手臂是商人 Spine，按确认不改。


### 21.38 批次34：残血 low_hp + 残血 BGM（2026-10-23）

#### 1. 残血帧

- 以现有 `idle.png` + `idle_01..41.png` 为底，**保留待机的 3 轮站立循环**，从 `IdleOutro` 中删掉三组蹲起：
  - `16-19`、`24-28`、`33-37`（共 14 个唯一帧）。
- 剩余 28 个唯一帧，全部在**左脸颊靠边**加一滴汗：
  - 形状：深棕描边 + 浅蓝填充 + 白高光，和现有简笔画黑描边/平涂风格一致；
  - 锚点按每帧角色 bbox 的 `left/top` 偏移，保留在脸颊上；
  - 尺寸 22×29（600×820 画布）。
- 产物 `STS2_Momoi/images/characters/cue/low_hp.png` + `low_hp_01..27.png`（28 张）。
- 构建脚本：`工作区/编辑区/人物/_src/_build_low_hp_cue.py`；联系表 `_work/low_hp_contact.png`。
- C#：`LowHpFrameMap` 把原 idle 帧号映射到 low_hp 文件序号；`VisualCues` 新增 `.Sequence("low_hp")`，使用与 idle 相同的 `IdleLoopSpeed` / `IdleOutroSpeed`，`Loop()`。
- 状态机新增循环状态 `low_hp` 和触发器 `LowHp`；正常回 `idle`。

#### 2. 残血触发

`Patches/MomoiLowHpPatch.cs`：

- `NCreature._Ready` Postfix，只给 `STS2_MomoiCharacter` 的玩家角色挂 `MomoiLowHpController`。
- 音量设置现为「音量」栏六档滑块（总/音乐/语音/音效/受击/死亡），见 §21.43。
- 控制器每帧检查 `Creature.CombatState` / `IsDead` / `GetHpPercentRemaining() <= 0.25`；
- 低血量时若当前状态是 `idle`，调用 `SetAnimationTrigger("LowHp")`；离开 25% 且当前是 `low_hp` 时，调用 `SetAnimationTrigger("Idle")`。
- 攻击/受击等状态期间不硬切残血 idle；等它们自然回到 idle 后再切。
- 通过新增 `MomoiAnimMachineTrackPatch` 在 `ModAnimStateMachine.Start/SetTrigger` 后按 `Backend.OwnerNode` 登记状态机；控制器从 `MomoiAnimMachineRegistry` 读取当前状态，不再反射 RitsuLib 内部补丁类。

#### 3. 残血 BGM

- 源文件：`C:\Users\asus\Downloads\残血bgm.ogg`，复制到 `STS2_Momoi/audio/low_hp_bgm.ogg`；Godot 导入 `loop=false`。
- 控制器自己创建 `AudioStreamPlayer`（`Bus = "SFX"`，挂在 `NCreature` 下），不依赖 FMOD 循环事件。
- 行为：
  - 进入残血时开始播；如果当前已经在播，不叠加、不重头播；
  - 播完 `Finished` 时仍残血 → 再播一遍；
  - 离开残血**不打断**当前这一遍；这一遍播完时不残血就不续播；
  - 死亡 / 战斗结束（`Creature.CombatState == null`）→ 2 秒淡出后 Stop；奖励界面（`NOverlayStack.Peek() is NRewardsScreen`）→ 2 秒淡出后 Stop；最终建筑师对话场景（`CombatState.Encounter is TheArchitectEventEncounter`）不播放，若在播则 2 秒淡出；
  - 下一场战斗重新进入残血会重新开始。
- 这符合“播完一遍完整、仍残血重复、离开不中断、战斗结束停止”的要求，不用 `SfxCmd.PlayLoop/StopLoop`。

#### 4. 构建 / 自检

- `dotnet build` 0 错误；DLL **492,032 B** / PCK **128,360,432 B**（**1053 条目**，**25 补丁**）。
- `_verify_batch28.py` 97 条；`_verify_batch32.py` 117 条；25 套合计 **1085 条全绿**。
- 运行时尚未由助手启动验证；待进游戏确认残血触发、汗滴位置、BGM 续播/不中断/战斗结束停止。


### 21.39 先古之民对话参考（2026-10-23）

- 新增 `工作区/_docs/_先古之民对话整理.md`，从游戏 `localization/zhs/ancients.json` 整理。
- 覆盖 **9** 位先古/建筑师、**287** 条有文本的台词（212 条先古 + 75 条角色），按先古 → 角色 → 对话组排列；包含 `firstVisitEver`、通用 `ANY`、`0-0r` 重复访问、按钮文案，以及每位先古的语气/关系速记和给王小桃的切入点。
- 生成脚本：`工作区/_scripts/_build_ancients_dialog_md.py`；可重复运行，源文件更新后重跑即可。


### 21.39.1 王小桃先古之民对话实现（2026-10-24）

- 写入 `STS2 Momoi/STS2_Momoi/localization/{zhs,eng}/ancients.json`，每个语言 **166** 个键、**36** 组对话（9 位先古/建筑师 × 4 组）。
- 生成脚本：`工作区/_scripts/_build_momoi_ancient_dialogues.py`。
- **四组都进入重复池**（高访问存档不再只看到组 0）：
  - 四组的**每一行** key 都带 `r`（例如 `.0-0r.char` / `.1-0r.char` / `.2-0r.ancient`）。`AncientDialogue.PopulateLines` 会检查同一组所有行，必须整组一致。
  - 同时写 `...0-visit` / `...1-visit` / `...2-visit` / `...3-visit` 覆盖 RitsuLib 非建筑师的默认映射（默认 0/1/4/7），让四组分别落在第 0/1/2/3 次访问。
  - 组 0/1/2/3 先分别在第 0/1/2/3 次访问优先出现；第 4 次及以后四组都在重复池中随机。
- **文字特效**：
  - 涅奥：所有 ancient 台词包 `[sine]...[/sine]`。
  - 坦克斯：所有 ancient 台词整句 `[b]...[/b]`；组 3 的“小桃与坦克斯战斗了。”用 `[i][font_size=22]...[/font_size][/i]`，还原原版旁白。
  - 特兹卡塔拉：关键词 `战斗` 用 `[jitter][b]...[/b][/jitter]`；其余原版关键词若未出现在本组文本中则不硬加。
  - 瓦库：组 2 的 `伙伴` / `勇气` 用 `[aqua]...[/aqua]`；组 3 的“瓦库大笑起来。”用原版 `[i][font_size=22]` 旁白。
  - 颜色规范沿用原版：红=会痛的敌人/至亲，青=被挂念之物，金=人名。
- **校验**：`_verify_batch32.py` 新增 zhs/eng 166 键、所有对话行 r、32 个 visit 键、坦克斯加粗/斜体、特兹卡塔拉 jitter、瓦库 aqua 等断言。
- 构建：DLL **492,032 B** / PCK **128,360,432 B**（1053 条目，24 补丁）；25 套 **1085 条全绿**。

### 21.40 批次35：剧本打击括号数跟升级、重整旗鼓阈值 25%（2026-10-24）

#### 1. 剧本打击：括号里的抽牌数改成跟着升级走（0 张 / 1 张）

**现象**：卡面第二句已经写了「抽等同构想数值{IfUpgraded:show:+1|}张牌」，但括号里那句被 `{InCombat:…}` 包着，
**局外**（牌组/奖励/商店里看）固定走 else 分支，升级版也显示「（抽0张牌）」。

**修法**（与「天马行空」完全一致：升级的 +1 放在 base 变量上，而不是写在 multiplier 里）：

```csharp
// 之前：multiplier 里自算 +1 → 局外 multiplier 记 0，升级版也显示 0
new IndependentCalculatedVar("ConceptCards", cardsBase, cardsExtra)
    .WithMultiplier((card, _) => ConceptCounterCapability.GetMaxCountInHand(card.Owner.Creature) + (card.IsUpgraded ? 1 : 0));

// 现在：照着天马行空（HitsBase 0 → 升级 +1）的写法
.WithMultiplier((card, _) => ConceptCounterCapability.GetMaxCountInHand(card.Owner.Creature));

protected override void OnUpgrade()
{
    DynamicVars.CalculationBase.UpgradeValueBy(2);
    DynamicVars["CardsBase"].UpgradeValueBy(1);   // 抽牌数 +1（局内外都显示）
}
```

- 局外：`CardsBase` = **0 / 1** → 显示「（抽0张牌）/（抽1张牌）」✓
- 局内：`CardsBase + 1 × 构想数值` = 构想数值（+1 升级）✓ 与实际抽牌一致（`OnPlay` 仍读 `ConceptCards`）
- 文本去掉 `{InCombat:…}`：`……张牌。\n（抽{ConceptCards:diff()}张牌）`

#### 2. 重整旗鼓：自动打出阈值 20% → 25%

两处判定（升级前后都是同一段代码，所以两版一起变；其它效果一律没动）：

| 位置 | 旧 | 新 |
|---|---|---|
| 卡 `RallyAgain.TryAutoPlayIfLowHp` | `if (me.CurrentHp > me.MaxHp / 5) return;` | `if (me.CurrentHp > me.MaxHp / 4) return;` |
| power `RallyAgainPower.AfterDamageReceived` | `if (Owner.CurrentHp * 5 >= Owner.MaxHp) return;` | `if (Owner.CurrentHp * 4 >= Owner.MaxHp) return;` |

中文文本「当生命值低于20%时…」→「低于25%时」，英文 `below 20%` → `below 25%`，注释同步。

#### 3. ⚠ 又一次自检脚本覆盖（第三次）

本批新建自检时又用了已存在的号：`_verify_batch31.py`（10-22 动画批：死亡 50 帧 / 能量图标 / 多人手臂）。
处理：

1. 本批脚本改名 **`_verify_batch35.py`**（批次号对齐当前最新 §21.38 / 批次34）。
2. 按 §21.35 与磁盘实测**重建** `_verify_batch31.py`（24 条：dead 50 帧 1400×1250 / `DeadFrameCount=50` / `DeadSpeed` / 不循环 / energy_text 24×24 / energy_big 256×256 / 4 张手臂 422×1200 / 审阅图 / AEP 不在 PCK 源目录）。

**新规矩（写进流程）**：新建自检前先 `ls 工作区/_scripts/_verify_batch*.py` **并**看根文档最新 `### 21.x 批次NN`，取 `NN+1` 命名；已发生 3 次同名覆盖（24、28、31）。

#### 4. 产物

- `dotnet build` **0 错误** → DLL **492,032 B**、PCK **128,360,432 B**（10-24 03:17）。
- `_verify_batch35.py` **21 条全绿**；**二十四套合计 1020 条断言全绿**（实测，逐个跑）。
- 文档 §10 的套件表/命令改为「按通配遍历全部脚本」，避免再出现表内数字与实际脚本数量对不上的情况。


### 21.41 音效与战斗特效（2026-10-24）

#### 1. 自定义音效

- `STS2 Momoi/STS2_Momoi/audio/` 新增 `hurt.ogg`（源 `受伤.m4a` 经 ffmpeg 转 ogg）、`ba_boot.ogg`、`creative_pain.ogg`、`minigame_generated.ogg`、`winning_script.ogg`。
- `STS2 MomoiCode/Audio/MomoiSfx.cs` 用 `VirtualFmodEventRegistry.RegisterOneShots` 注册 5 个 virtual FMOD 事件；`Entry.Initialize` 调用 `Register()`。
- 触发：
  - 受伤：`MomoiLowHpController` 订阅 `NCreature.Entity.CurrentHpChanged`，HP 下降时播放，120ms 节流；不依赖起始遗物，遗物被替换后仍有效。
  - `BaBoot.OnPlay` / `CreativePain.OnPlay` 直接 `SfxCmd.Play`。
  - 小游戏牌生成：`DriedInspiration` / `OverflowingInspiration` 的 `AfterCardGeneratedForCombat`；`MinigameSupport.CanBeTemporarilyAdded` 只认 `minigame` 标签，不含 `fullgame` 游戏牌。
  - `WinningScript.FlashSfx` 指向 `winning_script` 事件，效果触发时 `Flash()`。

#### 2. 特效

- 火蛇怒咬：`VfxCmd.PlayOnCreatureCenter(target, "vfx/vfx_bite")`。
- 构想：`VfxCmd.PlayFullScreenInCombat("vfx/vfx_adrenaline", Owner.Creature)`。
- 灼烧血条：`BurnPower` 实现 RitsuLib `IHealthBarForecastSource`，白/黄/橙渐变 + `MaterialUtils.CreateDoomBarShaderMaterial`，`FromRight`、`AffectsHpLabel=false`，与中毒/灾厄兼容。
- 敌人灼烧伤害：`BurnTurnsPower` 结算时对敌人 `NGroundFireVfx.Create(owner)`（原版焚烧）。
- 秒人斧：伤害 `WithHitFx("vfx/vfx_giant_horizontal_slash")`。
- 100连抽！/创作的痛苦！：`MomoiVfx.PlayWhirlwind`（原版旋风斩的横线 + 烟雾暗角）。**100连抽每段命中都加** `vfx/vfx_giant_horizontal_slash`，旋风持续到攻击结束；创作痛苦取消斩击、只保留旋风。
- 针锋相对：`vfx/vfx_molten_fist` + `blunt_attack.mp3`，两段各一次。

#### 3. 构建 / 自检

- 构建（历史值）：DLL **492,032 B** / PCK **128,360,432 B**（1053 条目，24 补丁）。
- 自检（历史值，现为 25 个脚本 / 1085 条）：`_verify_batch32.py` 117 条。
- 新增音效/特效说明：`工作区/_docs/_音效与特效.md`。

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

- `dotnet build` **0 错误** → DLL **492,032 B**、PCK **128,360,432 B**（10-25 01:42）。
- `_verify_batch36.py` **19 条全绿**；**二十五套合计 1062 条断言全绿**（通配逐个跑）。


### 21.43 音量分组 / 新音效 / 枪械与多段攻击特效（2026-10-25）

#### 1. 六档音量

- 设置页新增独立「音量」栏：**总音量 / 音乐音量 / 语音音量 / 音效音量 / 受击语音音量 / 死亡语音音量**；前五项 0–100，死亡 0–700（默认 500）。
- 总音量乘到所有分类；音乐控残血 BGM 与选人 BGM；普通语音收纳 BA启动、创作痛苦语音、小游戏生成、胜利剧本、当心误射、虚拟女仆武器；受击/死亡各有独立音量；音效收纳枪声、创作痛苦冲击音；免死复活归语音。
- 旧的「残血 BGM 音量」`LowHpVolume` 已由音乐音量取代。
- `MomoiAudio` 每次播放前刷新 virtual event 注册音量；残血 BGM 直接写 `MusicVolumeDb`。
- 免死/死亡等 combat-ending 边界用直通 `AudioStreamPlayer`，绕开 SfxCmd 的静默过滤。

#### 2. 新音效

新增 `creative_pain_impact`、`gunshot`、`death_voice`、`watch_out_voice`、`maid_weapon_voice`、`revive`；共 11 个自定义事件。

#### 3. 多段攻击动画

- 攻击牌只登记 `attack1/2/3`，`MomoiStateMachineCueSuppressPatch` 把每段标准 `Attack` 改写成登记动画。
- 除 **100连抽！**（仍只播一次，等未来新攻击动画占位）外，多段攻击每段都播放一次攻击动画；创作痛苦每段伤害前都播。
- 100连抽每段都加 `vfx/vfx_giant_horizontal_slash`；旋风斩横线/暗角用 persistent handle 持续到攻击结束。创作痛苦取消斩击，保留持续旋风背景，并新增冲击音。
- 创作痛苦拆成 3 条单段 AttackCommand：第 1 段无等待，第 2/3 段前各 0.5s；多段攻击逐段动画。
- 小刀特效改为每次命中一发 `NShivThrowVfx`（粉黄混色），多段伤害各自叠一发；枪声每段一声。
- 灼烧地面火：`AfterPowerAmountChanged` 覆盖首次/叠层；`NGroundFireVfx.AssetPaths` 已加入角色 `ExtraAssetPaths` 预载。
- 死亡语音改为订阅 `CreatureDiedEvent`：`WasRemovalPrevented=false` 且本地玩家才播；覆盖战斗死亡、事件死亡、主动放弃；默认 500%，最高 700%；旧版 180/200 的死亡音量一次性迁移到 500%；免死复活改用语音音量。

#### 4. 卡牌特效/音效

- 打击、翻滚射击、曳光弹、试探打击、火力爆发、博览群游：单体每次命中一发 `NShivThrowVfx`（粉黄混色）+ 每段基础枪声；多段伤害各自叠发。
- 天马行空：对群每次命中一组 `NDaggerSprayFlurryVfx`（粉）+ 每个目标 `NDaggerSprayImpactVfx`（黄），枪声每段一声。
- 创作痛苦：对群 3 段各一组弹幕；第 1 段立即，第 2/3 段前各 0.5s，因此三组弹幕有 0.5s 间隔；无斩击，旋风持续到结束。
- 曳光弹、局势升温、油腻打击额外加恶魔之焰地面火 + `attack_fire` 音效。
- 王道、破势、秒人斧：君王之剑 `NBigSlashVfx` + `NBigSlashImpactVfx` + `regent_sovereign_blade`。
- 针锋相对：熔融之拳 `vfx/vfx_molten_fist` + `blunt_attack.mp3`，两段两次。
- 敌人被施加/叠加灼烧与受到灼烧伤害都触发 `NGroundFireVfx`（原版焚烧）。

#### 5. 构建 / 自检

- DLL **494,592 B** / PCK **130,898,644 B**（**1059 条目**，**26 补丁**）。
- 25 个脚本 **1085 条全绿**（`_verify_batch32.py` 117 条）。
- 详细音效/音量/特效说明：`工作区/_docs/_音效与特效.md`。

### 21.44 批次37：阶段总结与工程经验（2026-10-25）

> 本节是截至批次37的**权威状态**。§21.41 / §21.42 里「100连抽只给首击加特效」「创作痛苦 0.74s」「四档音量」「23 个脚本」等描述是撰写当时的历史记录，已被本节和 §21.43 取代；查现状时以本节为准。

#### 1. 当前进度：功能开发已完成，进入实机验收

| 模块 | 状态 | 当前结果 |
|---|---|---|
| 角色身份 / 卡池 | ✅ 完成 | 中文名 **王小桃**、英文 **Momoi**，初始生命 **72**，代词 **她 / she / her**；`[RegisterCard]` 共 **133** 张 |
| 战斗动画 | ✅ 完成 | `idle` 42、`attack1` 8、`attack2` 24、`attack3` 16、`cast1` 24、`cast2` 12、`taunt1` 21、`hit` 9、`dead` 50、`low_hp` 28 帧；600×820，脚底 815 |
| 死亡 / 残血 | ✅ 完成 | `dead` 2.0833s（抽动→灰化→停→倒下）；`low_hp` 去掉 3 组蹲起 + 左脸颊汗滴；残血 BGM 播完续播、离开不打断、奖励/死亡/战斗结束 2 秒淡出 |
| 商店 / 休息处 / 选人 | ✅ 完成 | 商店 relaxed 2 张交替；休息处 `休息处.png`；选人两段 `.ogv` + 模糊底 + 白天/夜间 BGM（跟随音乐音量） |
| UI / 能量 / 多人 | ✅ 完成 | 像素头像 5 张 + 左上角头像场景；24×24 小能量、256×256 大能量、静态表盘；4 张 422×1200 多人手势；篝火右半场镜像 |
| 先古之民对话 | ✅ 完成 | 9 位先古之民 × 4 组 = **36** 组；中/英各 **166** 个键；四组都可重复；`0-visit`~`3-visit` 分别落在第 0/1/2/3 次访问 |
| 卡牌 / 机制 / 文本 | ✅ 完成 | 卡池、遗物、药水、能力、中文/英文、关键词颜色与稀有度框保持原版规则；卡框只改 `%Frame`，不改 `%PortraitBorder` |
| 战斗特效 | 🟡 已实现，待实机 | 君王斩击、熔融之拳、恶魔之焰、灼烧地面火、旋风背景、单体单发小刀、对群弹幕、100连抽逐段横斩 |
| 音效 / 音量 | 🟡 已实现，待实机 | 11 个自定义音效 + 残血 BGM + 两首选人 BGM；六档音量；受击、死亡独立音量；死亡默认 **500%**、最高 700% |
| 构建 / 自检 | ✅ 完成 | DLL **494,592 B** / PCK **130,898,644 B** / **1059** 条目 / **26** 补丁；**25** 个脚本 **1085** 条全绿 |
| 实机验收 | ⏳ 待用户 | 选人 BGM/音乐音量、受击/死亡音量、地火、死亡语音（含事件/放弃）、复活音、单体单发/对群弹幕、创作痛苦节奏、多段攻击、100连抽性能 |

**结论：代码和资源接入已经收尾，剩余工作以「实机验收 + 小幅手感修正」为主，不再适合同时开新的视觉大改。**

#### 2. 批次37 实际改了什么

| 问题 | 最终实现 | 关键路径 |
|---|---|---|
| 小刀像一整组弹幕 / 对群效果 | 单体枪械每次命中一发 `NShivThrowVfx`；天马行空/创作痛苦改用对群 `NDaggerSprayFlurryVfx` + `NDaggerSprayImpactVfx`，每次命中一组 | `Cards/MomoiGunStyle.cs` |
| 创作痛苦节奏/特效 | 拆成 3 条单段 `AttackCommand`；第 1 段立即，第 2/3 段前各 `Cmd.CustomScaledWait(0.5f, 0.5f)`；每段一组对群弹幕，组间 0.5s；不额外加枪声；不再用会连第一段一起等的 `WithWaitBeforeHit` | `Cards/CreativePain.cs` |
| 受击语音音量 | 新增 `HurtVoiceVolume`，默认 100%；受伤走 `MomoiAudio.PlayHurtVoice` | `Settings/MomoiSettings.cs`、`Audio/MomoiAudio.cs`、`Patches/MomoiLowHpPatch.cs` |
| 死亡语音太小 | 新增 `DeathVoiceVolume`，默认 **500%**、最高 700%；旧版 180/200 一次性迁移；`CreatureDiedEvent` 直通播放 | `Settings/MomoiSettings.cs`、`Audio/MomoiDeathVoice.cs` |
| 免死复活音归类 | `PlayDirectVoice(Revive)`，跟普通语音走，不再占音效音量 | `Patches/MomoiReviveSfxPatch.cs` |
| 灼烧地火不出现 | `NGroundFireVfx.AssetPaths` 加入角色 `ExtraAssetPaths` 预载；首次施加/叠层走 `AfterPowerAmountChanged` | `Characters/STS2 MomoiCharacter.cs`、`Powers/BurnPower.cs` |
| 死亡音效只覆盖战斗 | 订阅全局 `CreatureDiedEvent`，`WasRemovalPrevented=false` 且本地玩家才播；覆盖战斗、事件死亡、主动放弃；不再由战斗控制器轮询 | `Audio/MomoiDeathVoice.cs` |

**注意：** 批次37 新增 `MomoiDeathVoice.cs` 并把 PCK 从 **1053** 变成 **1054** 条目；批次38 加入两首选人 BGM，最终 PCK **1059** 条目、**130,898,644 B**，DLL **494,592 B**。

#### 3. 工程经验：这次真正踩到的坑

##### 3.1 原版 VFX 先看「粒子数量」，不要被名字骗

- `NDaggerSprayFlurryVfx` 的名字是 Flurry，场景里 `vfx_dagger_spray_dagger.tscn` 的 `amount = 18`，一次就是**整组 18 发**，不是「一发小刀」。
- 要单发，应使用 `NShivThrowVfx`（单把飞刀 + 命中），不要试图把 Flurry 的 `amount` 改小：那会连带改原版资源和其他卡。
- 对群/弹幕牌反而适合 `NDaggerSprayFlurryVfx`（攻击者侧一组）+ `NDaggerSprayImpactVfx`（每个目标命中）；`WithAttackerFx` 默认每段命中都触发，所以多段就是多组，间隔由调用方控制。
- **多段伤害的语义**：单体一发子弹对应一次命中；对群一组弹幕对应一次命中。3 段就是 3 次，不要用 `first` 标志只生成首段。
- 颜色只改 `ApplyTint` 的 tint，不改原版场景、粒子速度、命中结构。

##### 3.2 战斗 VFX 必须预载，尤其是「原版卡片本来会预载」的资源

- 原版攻击牌会通过 `ExtraRunAssetPaths` 预载 `NGroundFireVfx.AssetPaths`；角色 Mod 如果只写 `scenePath` 而不预载，战斗中可能加载不到，表现就是「逻辑执行了，但地火没出现」。
- 角色侧统一放 `ExtraAssetPaths`：
  - `NGroundFireVfx.AssetPaths`
  - `NHorizontalLinesVfx.AssetPaths`
  - `NSmokyVignetteVfx.AssetPaths`
  - `NShivThrowVfx.scenePath`
  - `NBigSlashVfx.scenePath` / `NBigSlashImpactVfx.scenePath`
  - `vfx_bite` / `vfx_adrenaline` / `vfx_molten_fist` / `vfx_giant_horizontal_slash` 等
- 判断是「逻辑没执行」还是「资源没加载」：先在代码里确认 `AfterPowerAmountChanged` 是否触发，再看 VFX 路径是否预载，不要只凭画面猜。

##### 3.3 施加 Power 和叠层不是一个回调

- `AfterApplied` 通常只在**首次施加**时触发一次；后续叠层/加层不会重复。
- 需要「每次施加/叠层都触发」时用 `AfterPowerAmountChanged`，并自己判断 `amount > 0`。
- 需要「受到该 Power 伤害时触发」时，放在伤害结算/`BurnTurnsPower` 的对应位置，不能和「施加时」混在一个回调里。

##### 3.4 VFX 的生命周期：`using` 会提前销毁

- `using var whirlwind = MomoiVfx.PlayWhirlwind(...)` 在作用域结束时 Dispose；如果后面还要继续攻击，旋风会被提前收掉。
- 长背景（100连抽、创作痛苦）要用 `persistent: true` 的 handle，攻击循环结束后再 Dispose。
- 单次命中特效返回的 Node 由调用方/场景管理；不要在循环里创建后马上释放还在播的节点。
- 100连抽每段一个横斩会产生大量 VFX；如果实机掉帧，优先**降低命中特效密度**，但保留「每段斩击」的语义和持续旋风背景。

##### 3.5 多段攻击动画：标准 `Attack` 事件可以被逐段改写

- 攻击牌只登记 `attack1/2/3`，不主动播放；`MomoiStateMachineCueSuppressPatch` 把每段标准 `"Attack"` 改写成登记的动画。
- 每条 `AttackCommand` = 一次动画；因此「3 段」应该拆成 3 条命令，而不是一条 `WithHitCount(3)` 后只播一次。
- **`WithWaitBeforeHit` 连第一段之前也会等**。如果需求是「第一段立即、后续段间隔」，必须拆命令 + 手动 `CustomScaledWait`。
- **100连抽！** 是明确的例外：仍只播一次 `Attack1` 占位，等未来新攻击动画；逐段只做横斩 VFX。
- 不要为了拿状态机去反射 RitsuLib 内部类；用 `MomoiAnimMachineTrackPatch` 登记，控制器从 registry 读。

##### 3.6 音频：virtual event 的音量在「播放前」刷新

- `MomoiAudio` 的 `MasterGain × 分类 Gain` 不是设置一次就永久生效；每次 `Play` 前都要把当前音量写进 `VirtualFmodEventRegistry.RegisterOneShot`。
- 分类音量：
  - 总音量乘所有分类；
  - 音乐控残血 BGM 与选人 BGM；
  - 语音控 BA启动、创作痛苦语音、小游戏生成、胜利剧本、当心误射、虚拟女仆武器、复活；
  - 受击 / 死亡各有一档，避免「死亡语音和受击语音一样大、听不见」；
  - 音效控枪声、创作痛苦冲击音。
- 死亡默认 **500%**、最高 700%，是为了解决素材本身偏小，不是把总音量拉高；总音量仍然可以整体压到 0。
- `SfxCmd.Play` 在战斗结束/奖励界面可能被静默；死亡、复活这类边界音效用直通 `AudioStreamPlayer`。
- 直通播放要挂到 `NRun.Instance?.GlobalUi` 等稳定父节点；事件死亡/主动放弃时 NRun 可能已在切换，`NGame.Instance` 是更稳的兜底。日志打 `[Audio] direct ...`；找不到父节点/流时打 `[Audio] direct no parent ...` / `[Audio] direct missing ...`。
- 死亡触发点不要只看战斗控制器 HP：事件死亡/主动放弃不会经过 `_Process` 或 `CurrentHpChanged`。应订阅 RitsuLib `CreatureDiedEvent`，用 `WasRemovalPrevented` 过滤免死，用 `LocalContext.IsMe` 只让本地玩家播自己的；不要在钩子里发网络消息。
- 如果必须在 `BeforeDeath` 做，注意它在 `ShouldDie` 之前分发，免死也会响；更稳的是 `CreatureDiedEvent`。
- 残血 BGM 用独立 `AudioStreamPlayer`：播完仍在残血→续播；离开残血→不打断；奖励/死亡/战斗结束→2 秒淡出；最终建筑师场景不播。

##### 3.7 Godot 卡框：`AtlasTexture` 的 UV 是整张图集坐标

- `%Frame` 是 `AtlasTexture`，shader 的 `UV` 不是单张卡的 0~1，而是整个图集坐标。
- 必须按 `AtlasTexture.Region / Atlas.GetSize()` 为每张卡复制材质并写 `uv_offset` / `uv_scale`，再在 shader 里还原 `card_uv`；只改共享材质会把正文遮罩压到整张卡上，外框发黑/发紫。
- 只改 `%Frame`；`%PortraitBorder` / `%TitleBanner` 是稀有度语义，不要顺手改。
- 判断「材质没生效」先看节点是否是 `AtlasTexture`、材质是否被每张卡覆盖，不要先怀疑 shader 公式。

##### 3.8 选牌/变牌：`source` 决定节点何时归位

- 药水/非卡牌模型作为 `FromHand(..., source: this)` 的 source 时，`NPlayerHand` 会把「选中卡归位」挂到它的 `ExecutionFinished`，而药水永远不会发这个事件。
- 表现是「变牌白光结束、卡面白很久/不刷新」或「幽灵牌」。
- 选牌后要立刻变换/消耗时，`source` 传 `null`，并逐张 `CardCmd.Transform`，和原版「护驾！！！」/「整活」一致。
- 这类问题优先查节点树和事件，而不是给 UI 加延时。

##### 3.9 先古对话：同一组所有行都要带 `r`

- `AncientDialogue.PopulateLines` 要求**同一组的所有行**都带 `r`，只给首行加会抛异常。
- 只让组 0 可重复，会导致高访问存档（例如 Neow 169 次）几乎只看到组 0；四组全带 `r` 后才会在 0~3 组间随机。
- `0-visit`~`3-visit` 对应第 0/1/2/3 次访问；第 4 次及以后四组都可重复。
- 改颜色时中/英两份都要同步，关键词颜色只加在出现该词的组。

##### 3.10 自检脚本：别只信上一次的「全绿」

- 当前是 **25** 个 `_verify_batch*.py`，合计 **1085** 条；`_verify_batch32.py` 117 条。旧文档写的「23 个脚本」是错的。
- 断言过期很常见：设置项改名、补丁数从 24 变 25、特效路径替换，都会让旧脚本假红。
- 修脚本时要区分：
  - 代码真的退化；
  - 变量本来就被后续批次取代；
  - 脚本自己插错行/覆盖了别的批次。
- 新建脚本前先用通配确认文件名不冲突；本会话已出现多次 `_verify_batchXX` 覆盖事故。
- 自检是**源文件静态检查**，不能证明游戏内 VFX/音频真的播放；最终仍要实机验收。

##### 3.11 构建与文档

- 构建前关闭游戏，否则 PCK 可能被占用；`dotnet build` 会同时导出 PCK 并部署。
- 判断是否真的部署：看 mods 目录的 **DLL 体积 / PCK 体积 / PCK file_count**，不要只看 `Build succeeded`。
- 文档最容易出现三种漂移：
  1. 同一节号重复（本文件曾有两个 `§21.42`，现已拆成 `§21.42` / `§21.43`）；
  2. 旧数字（23 个脚本、四档音量、24 补丁）；
  3. 旧行为（100连抽只给首击、创作痛苦 0.74s、针锋相对 `vfx_thrash`）。
- 处理原则：**新增「当前权威状态」节 + 给历史节标注「历史值/已被取代」**，不要在每个历史段落里反复改数字，否则下一次仍会漂移。
- 文档里的「自检全绿」必须写清脚本数和断言数；「未启动游戏」必须明确写，不能把静态检查当成实机通过。

#### 4. 已知缺口与风险

| 项目 | 类型 | 现状 / 处理 |
|---|---|---|
| 受击 / 死亡独立音量 | 待实机 | 六档滑块已接入；确认死亡 500% 与受击 100% 能分别听出差异 |
| 死亡语音仍不响 | 待实机 / 诊断 | 看 `[DeathVoice] CreatureDiedEvent`、`[Audio] direct ...`、`[Audio] direct missing ...`；事件死亡/主动放弃也要测 |
| 灼烧地火不出现 | 待实机 | 已补预载；看首次施加/叠层是否触发 `AfterPowerAmountChanged` |
| 复活音 | 待实机 | 已走语音音量；确认瓶中小精灵/蜥蜴尾巴/我复活啦！都触发 |
| 单发小刀 / 对群弹幕 | 待实机 | 单体每次命中一发 `NShivThrowVfx`；天马行空/创作痛苦每组弹幕；创作痛苦 3 组间隔 0.5s |
| 创作痛苦节奏 | 待实机 | 第 1 段立即、2/3 段各 0.5s；三组弹幕有间隔，动画/音效不早停 |
| 100连抽性能 | 风险 | 100 个横斩 + 持续旋风可能掉帧；必要时降低 VFX 密度，但保留每段斩击与旋风 |
| 选人 BGM | ✅ 完成 | 白天 Pixel Time / 夜间 Operation☆DOTABATA；战士选人/转场音效占位已删；跟随音乐音量 |
| 技能牌动画 | 占位 | 目前普通技能保持 idle；等专用动画 |
| 角色默认 `AttackSfx/CastSfx` | 占位 | 仍回退原版；后续再决定归属音量栏 |
| 100连抽攻击动画 | 占位 | 当前只播一次 `Attack1`，等新动画替换 |

#### 5. 建议的实机验收顺序

1. **设置页**：把总音量拉低/拉高，确认六档都能独立变化；受击 100%、死亡 500% 的差异要能听出来，死亡最高可拉到 700%。
2. **死亡**：普通战斗死亡、事件死亡（如真理之碑）、主动放弃各测一次，确认死亡语音都响且不被受击音盖住。
3. **灼烧**：给敌人施加灼烧、再叠一层、再让灼烧跳伤害，三次都应看到地面火。
4. **免死**：分别测瓶中小精灵、蜥蜴尾巴、我复活啦！，确认复活音都响且受语音音量控制。
5. **枪械牌**：单体多段枪械每段一发小刀；天马行空每次命中一组弹幕；枪声每段一声。
6. **创作痛苦**：确认第一段立即、第二/三段各约 0.5s，三组弹幕有间隔，旋风持续到结束，旧语音 + 冲击音各一次。
7. **多段攻击**：确认每段伤害各播一次攻击动画；100连抽只播一次攻击动画但每段有横斩。
8. **性能**：100连抽期间观察掉帧；如果明显卡顿，再降低命中 VFX 密度，不改变持续旋风。

#### 6. 关键文件索引

| 用途 | 路径 |
|---|---|
| 角色 / 预载 | `STS2 Momoi/STS2 MomoiCode/Characters/STS2 MomoiCharacter.cs` |
| 卡池 | `STS2 Momoi/STS2 MomoiCode/Characters/STS2 MomoiCardPool.cs` |
| 设置 | `STS2 Momoi/STS2 MomoiCode/Settings/MomoiSettings.cs` |
| 音量 / 直通播放 | `STS2 Momoi/STS2 MomoiCode/Audio/MomoiAudio.cs` |
| 音效事件 | `STS2 Momoi/STS2 MomoiCode/Audio/MomoiSfx.cs` |
| 枪械 / 小刀 | `STS2 Momoi/STS2 MomoiCode/Cards/MomoiGunStyle.cs` |
| 创作痛苦 | `STS2 Momoi/STS2 MomoiCode/Cards/CreativePain.cs` |
| 灼烧 | `STS2 Momoi/STS2 MomoiCode/Powers/BurnPower.cs` |
| 低血量 / 受击 | `STS2 Momoi/STS2 MomoiCode/Patches/MomoiLowHpPatch.cs` |
| 死亡语音事件 | `STS2 Momoi/STS2 MomoiCode/Audio/MomoiDeathVoice.cs` |
| 免死音效 | `STS2 Momoi/STS2 MomoiCode/Patches/MomoiReviveSfxPatch.cs` |
| 战斗 VFX | `STS2 Momoi/STS2 MomoiCode/Cards/MomoiVfx.cs` |
| 音效/特效说明 | `工作区/_docs/_音效与特效.md` |
| 残血/音频经验 | `工作区/_docs/_开发经验_残血动画与音频.md` |
| 先古对话 | `工作区/_docs/_王小桃先古对话.md` |
| 自检 | `工作区/_scripts/_verify_batch*.py` |

#### 7. 本批构建 / 自检证据

- `dotnet build "STS2 Momoi/STS2 Momoi.csproj"`：**0 错误**。
- DLL **494,592 B**。
- PCK **130,898,644 B**，`file_count` **1059**。
- 补丁 **25** 个。
- 自检：**25** 个 `_verify_batch*.py`，合计 **1085** 条通过、**0** 条失败。
- 本轮**未启动游戏**；上表「待实机」项必须由用户确认后才算关闭。

### 21.45 批次38：选人 BGM 回归 + 对群弹幕 + 死亡事件收尾（2026-10-25）

> 本节是批次38的当前状态。§21.31 里「选人音效接口 `SelectSfxVariants = [null, null]`」是历史记录，已被本节取代。

#### 1. 选人界面 BGM

| 背景 | 曲目 | 文件 | 绑定 |
|---|---|---|---|
| 白天 `select_bg_1` | **Pixel Time** | `STS2_Momoi/audio/select_bgm_day.ogg` | `STS2_Momoi_character_select_bg_1.tscn` 的 `SelectBgm` |
| 夜间 `select_bg_2` | **Operation☆DOTABATA** | `STS2_Momoi/audio/select_bgm_night.ogg` | `STS2_Momoi_character_select_bg_2.tscn` 的 `SelectBgm` |

- 源文件：`C:\Users\asus\Downloads\Pixel Time.ogg`、`C:\Users\asus\Downloads\Operation☆DOTABATA.ogg`；复制进 PCK 后使用独立 `loop=true` 的 `.ogg.import`。
- 每个背景场景放一个 `AudioStreamPlayer` 子节点，加入组 `momoi_select_bgm`，`autoplay=true`、`loop=true`、初始 `volume_db=-80`。
- `MomoiSelectBgmPatch` 挂在 `NCharacterSelectScreen._Process` 的 Postfix：每帧把 `MomoiAudio.MusicVolumeDb`（总音量 × 音乐音量）写到组内播放器；背景被移除时节点随场景释放；选人界面被缓存隐藏时 `StreamPaused=true`，显示后恢复。
- 背景仍是 `SelectVariant` 二选一，两首 BGM 各自绑定背景，不需要音效和背景分别随机。
- `CustomCharacterSelectSfx => null`、`CustomCharacterTransitionSfx => null`，不再回退铁甲战士的选人/转场音效；旧的 `SelectSfxVariants` 占位已删除。

#### 2. 创作痛苦 / 天马行空

- 对群走 `MomoiGunStyle.ApplyBarrage`：攻击者侧一组粉色 `NDaggerSprayFlurryVfx`，每个目标黄色 `NDaggerSprayImpactVfx`。
- 单体枪械仍走 `MomoiGunStyle.Apply`：每次命中一发 `NShivThrowVfx`。
- 创作痛苦拆成 3 条单段 `AttackCommand`：第 1 段立即，第 2/3 段前各 `Cmd.CustomScaledWait(0.5f, 0.5f)`，三组弹幕起点为 0 / 0.5 / 1.0s；不加枪声，保留旧语音 + 冲击音和持续旋风。
- 天马行空每次命中一组弹幕；枪声每段一声。

#### 3. 死亡事件 / 音量

- 默认 **500%**，滑块最高 **700%**；不改成 400/500。
- 旧版 180/200 一次性迁移到 500%；0/100 等主动设置不碰。
- 死亡由全局 `CreatureDiedEvent` 触发：`WasRemovalPrevented == false` 且 `LocalContext.IsMe` 才播；覆盖战斗死亡、事件死亡、主动放弃，不走网络消息。
- 直通 `AudioStreamPlayer`，父节点兜底 `NGame.Instance`；日志 `[DeathVoice] CreatureDiedEvent` / `[Audio] direct ...` / `[Audio] direct no parent ...`。
- 战斗控制器不再重复播死亡音；受击音仍走独立受击音量。

#### 4. 构建 / 自检

- `dotnet build "STS2 Momoi/STS2 Momoi.csproj"`：**0 错误**。
- DLL **494,592 B**。
- PCK **130,898,644 B**，`file_count` **1059**。
- 补丁 **26** 个。
- 自检：**25** 个脚本，合计 **1085** 条通过、**0** 条失败。
- 本轮**未启动游戏**；选人 BGM/音乐音量、死亡音量 500/700、事件死亡/主动放弃、对群弹幕均待实机确认。

#### 5. 实机验收重点

1. 白天背景播放 Pixel Time，夜间背景播放 Operation☆DOTABATA；音乐滑块实时生效，0% 静音。
2. 选人界面切出后 BGM 暂停，重新进入恢复，不叠播。
3. 普通战斗死亡、事件死亡、主动放弃都能听到死亡语音；免死只响复活音。
4. 创作痛苦第 1 段立即，第 2/3 段各 0.5s，三组弹幕可见。
5. 天马行空每次命中一组弹幕，枪声每段一声。

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
- 卡面 `工作区\美术成品区\过载.png` → `images/cards/Overload.png`；图标 `过载power.png` → `images/powers/overload_power.png`（尺寸刚好 1000×760 / 256×256）。

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

### 21.48 批次41：多段攻击的活力/火力重复消耗（创作的痛苦 / 100连抽）（2026-10-25）

#### 1. 根本原因

把一张多段攻击**拆成多条 `AttackCommand`** 时：

- `VigorPower.BeforeAttack` 只在**第一条**命令上记下 `commandToModify` 与 `amountWhenAttackStarted`；
- 这条命令执行完进入 `AfterAttack` 时，**一次把全部层数扣光**；
- 后面几条命令里 `base.Amount` 已经是 0 → 它们只能吃残值。

所以玩家看到的是「活力/火力只作用在第 1 段，而且被扣了多次/一次扣光」。正确写法是 **一条命令 + `WithHitCount(n)`**，
段间间隔用 `WithWaitBeforeHit(fast, standard)`，动画只播一次用 `OnlyPlayAnimOnce()`。

#### 2. 创作的痛苦！`CreativePain`

| 项 | 处理 |
|---|---|
| 上一批加的「获得 2/3 层火力」 | **删掉**（变量、升级、OnPlay 施加、卡面 `Firepower` 行、中英文本） |
| 三段攻击 | `for` 循环发 3 条命令 → **一条命令** `.WithHitCount(3)` |
| 段间 0.5s | `Cmd.CustomScaledWait(0.5f, 0.5f)` + 拆分 → **`.WithWaitBeforeHit(0.5f, 0.5f)`**（间隔不变） |
| 每段弹幕 / 命中特效 | 仍走 `MomoiGunStyle.ApplyBarrage` 的 `WithAttackerFx` / `WithHitVfxNode`（每段各一次） |
| ⚠ 注意 | **故意不加 `OnlyPlayAnimOnce()`** —— 原版那个开关只控制「攻击者侧特效/动画」是否每段播放，加了会把每段弹幕也一起关掉 |

> 细微差别：`WithWaitBeforeHit` 在**每一段（含第一段）** 的命中特效/伤害前等待，所以第一段伤害比原来晚 0.5s；
> 但「段间隔 0.5s」和「第一段弹幕立刻出现」都保持不变。

#### 3. 100连抽！`HundredPull`

100 次伤害原本是 `for` 循环发 **100 条** `AttackCommand`：
同样的活力 bug（只有第 1 次吃到）+ 每条命令都播一次攻击动画（卡顿）。

改成一条命令：`.WithHitCount(DynamicVars.Repeat.IntValue)` + `.OnlyPlayAnimOnce()`（命中特效 `vfx_giant_horizontal_slash` 每段照常）。

> ⚠ **平衡变化提示**：合成一条命令后，活力按「多段攻击」的正常规则**对每一段都生效**（活力 5 → 100 段共 +500 伤害）。
> 这是原版多段牌的语义；如果觉得过强，可以把这张牌改成 `WithHitCount(1)` 的固定伤害或限制段数。

#### 4. 全模组扫描（其余多段牌）

| 卡 | 现状 |
|---|---|
| 来自妮露的援护 | `WithHitCount(Hits)` ✓ 本来就对 |
| 捕鱼达人！ | `WithHitCount(hits)` ✓ |
| 激战 | `WithHitCount(Hits)` ✓ |
| 街啪6 | 每个能量分支各一条命令（一次打出只走一个分支）✓ |
| 来自晴 / 来自茜的援护 | 只是「对群一条命令」，不是多命令 ✓ |
| 节奏游戏！power 的回合末攻击 | 一条命令 ✓ |
| 来自勇者的加护 / 我复活啦 / 后续任务 等 | 单命令 ✓ |

扫描脚本（写进 `_verify_batch41.py` 第 4 节）：遍历所有 `ModCardTemplate` 的类体，
若一次 `OnPlay` 里出现「>1 条 `DamageCmd.Attack(`」或「循环体里发攻击命令」就报错 —— 目前**零告警**。

#### 5. 产物

- `dotnet build` **0 错误** → DLL **500,736 B**、PCK **131,853,468 B**（10-25 22:30）。
- 新增 `_verify_batch41.py` **21 条**；同步修正过期断言：`batch32`（创作痛苦由循环改成 `WithHitCount`+`WithWaitBeforeHit`）、`batch40`（创作痛苦已删火力）。
- **二十八套合计 1222 条断言全绿**。

### 21.49 批次42：发布完善（正式名 / 清单 / 设置页 / 诊断 / 工坊配套）（2026-10-26）

#### 1. 正式中文名「游戏王小桃」

| 位置 | 改动 |
|---|---|
| `STS2_Momoi.json` → `name` | **游戏王小桃**（游戏内模组列表显示的就是这个） |
| 设置页标题 | `WithTitle(ModSettingsText.Literal("游戏王小桃"))` |
| `README.md` / `README.en.md` 标题 | `# 游戏王小桃（STS2_Momoi）` / `# Game King Momoi (STS2_Momoi)` |

**角色名仍是「王小桃」**（选人界面、台词、卡面文本都没动）；`id` / `pck_name` 也没动 → 存档路径与部署目录不受影响。

#### 2. 清单字段（模板占位 → 正式值）

```json
"name": "游戏王小桃",
"author": "alkaid616",
"version": "1.0.0",
"min_game_version": "0.111.0",
"description": "以「游戏王小桃」为主角的角色模组：构想、小游戏牌、火力/活力三套体系，130+ 张卡牌、9 件遗物、3 瓶药水，以及一整套战斗动画。需要 RitsuLib。 / A character mod ..."
```

- `dependencies` 保持 `STS2-RitsuLib`（构建期的 `SyncManifestDependencies` 会自动把版本对齐 NuGet 包版本）。
- csproj 加 `<Version>1.0.0</Version>`，设置页「诊断」卡直接读程序集版本 → **以后改版本两处一起改**。

#### 3. 设置页：四节

| 节 | 内容 |
|---|---|
| `general` 通用 | 色彩哲学家是否出现本角色卡池 / 海玻璃是否出现本角色 |
| `audio` 音量 | 总音量、音乐、语音、音效、受击语音、死亡语音（死亡 0-700%） |
| `progress` 进度 | **说明卡**：本模组不需要纪元/时间线（`RequiresEpochAndTimeline = false`、无 `RequireEpoch`），角色与全部内容开局即可用；**「重置本模组设置」按钮**（Danger 色调，把 8 个设置项全部写回默认并保存） |
| `diagnostics` 诊断 | **版本信息卡**：`游戏王小桃 1.0.0` / `游戏 v0.111.0` / 日志目录路径 / 依赖说明（`ModSettingsText.Dynamic` 实时取值）；**「打开日志目录」按钮**：`OS.ShellShowInFileManager(Path.Combine(OS.GetUserDataDir(), "logs"))`，目录不存在时退回用户数据目录 |

> 按用户决定：**本版不接遥测**（RitsuLib 只有上报框架、接收端要自建），**不加特效强度开关**。

#### 4. 免纪元（已确认）

- `STS2_MomoiCharacter.RequiresEpochAndTimeline => false`；
- 全模组扫描无 `[RequireEpoch]` 属性、也无 `ModUnlockRegistry.RequireEpoch` 调用 → 卡牌/遗物/药水不会被纪元过滤。

> 注：RitsuLib 0.6.7 没有 `SetEpochRequirementsIgnoredForMod` 这类「临时全解锁」接口；本模组又没有纪元，所以 progress 节只放说明卡 + 重置按钮（这也是用户选的方案）。

#### 5. 工坊配套

- **预览图**：`工作区\美术成品区\工坊预览图_512.png`（512×512 / **139 KB**，远低于 1 MB 上限）——像素小桃立绘 + 模糊粉底 + 标题「游戏王小桃」。
- **发布清单**：`工作区\_docs\_发布清单.md`，含工坊 tags（Characters / schinese / English）、Required Items 填 RitsuLib 工坊 ID、工坊描述草稿、更新检查清单模板（`ModUpdateCheckOptions` + manifest JSON 示例）、上线前自测清单（本地版与工坊版并存、联机同文件、旧存档、中英文本、选人界面、设置页、建筑师打斗）。

#### 6. 产物 / 验证

- `dotnet build` **0 错误** → DLL **504,320 B**、PCK **131,853,468 B**（10-26 00:26），部署清单已是「游戏王小桃 / 1.0.0」。
- 新增 `_verify_batch42.py` **43 条**（清单字段 / 版本 / 免纪元 / 四节结构 / 重置 / 诊断 / 预览图 / README 标题 / 无遥测）。
- **二十九套合计 1265 条断言全绿**。

### 21.50 批次43：设置页收尾 + 换预览图 + 本地发布 zip（2026-10-26）

#### 1. 设置页三处反馈

| 反馈 | 处理 |
|---|---|
| 「进度」不要解释「本模组不需要纪元/时间线」 | 删掉那张说明卡；该节现在**只放「重置本模组设置」**，标题改成「其他」（id 仍是 `progress`，不用重装）。 |
| 「打开日志目录」在别的设备上准不准？ | **准**。路径是 `Path.Combine(OS.GetUserDataDir(), "logs")`，`OS.GetUserDataDir()` 是 Godot 按当前操作系统/账号解析的 `user://` 目录（Windows 是 `%APPDATA%\SlayTheSpire2`，Linux/macOS 各有对应位置），**代码里不写死任何绝对路径**；目录不存在时退回 user 目录本身。副作用：界面文案里原来那句「在文件管理器里打开 %APPDATA%/SlayTheSpire2/logs」也改成了跨平台措辞，诊断信息卡里显示的是**本机解析出的真实路径**。 |
| 暂时不要出现简介 | 设置页顶部那段是 RitsuLib 自动把清单 `description` 显示出来的 → 加 `.WithDescriptionHidden(true)` 隐藏；清单里的 description 保留（模组列表 / 工坊要用），等正式简介写好把这一行删掉即可。 |

#### 2. 预览图

换成用户给的 `工作区\美术成品区\预览图.png`（512×512 / **253 KB**，< 1 MB 上限），我先前合成的那张已删除。
`_发布清单.md` 里的引用同步改成这张。

#### 3. 本地发布包（先不上工坊）

新增 `工作区\_scripts\_make_release_zip.py`，按 QA 的做法**直接把 `mods/` 下那个文件夹压缩成 zip**：

1. 校验 `mods\STS2_Momoi\` 里 `STS2_Momoi.dll` / `.pck` / `.json` 三个文件都在，**文件名与清单 `id` 完全一致**；
2. 校验清单 `has_dll` / `has_pck` 为 true、`dependencies` 含 `STS2-RitsuLib`；
3. 打 zip 时**顶层就是 `STS2_Momoi/`**，额外塞一份 `README.txt`（安装说明 + 本地版/工坊版 id 抢占提醒 + 联机同文件提醒）到压缩包里（不进部署目录）。

产物：**`工作区\发布包\STS2_Momoi_v1.0.0.zip`（125.0 MB）**

```
STS2_Momoi/README.txt
STS2_Momoi/STS2_Momoi.dll
STS2_Momoi/STS2_Momoi.json
STS2_Momoi/STS2_Momoi.pck
```

玩家侧：解压到 `Slay the Spire 2/mods/` → 启动 → 首次运行弹「启用模组」→ 允许。

> ⚠ 本地版和工坊版 `id` 相同会互抢（游戏禁用版本号更低的那个）；以后同时上工坊时让两边版本号一致，或临时移走本地版。

#### 4. 产物 / 验证

- `dotnet build` **0 错误** → DLL **504,320 B**、PCK **131,853,468 B**（10-26 00:53）。
- 新增 `_verify_batch43.py` **26 条**（设置页三处收尾 + 预览图 + 部署目录三文件 + zip 结构与包内清单 + 发布清单文档）；
  同步修正 `batch42`（说明卡已删、预览图换名）。
- **三十套合计 1291 条断言全绿**。

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
- `工作区\_scripts\_make_release_zip.py` 重新打包 → **`工作区\发布包\STS2_Momoi_v1.0.1.zip`（125.0 MB）**，顶层 `STS2_Momoi/`。
- 顺手清掉了中间出现的**双层嵌套** zip（`STS2_Momoi_v1.0.0/STS2_Momoi/…`，玩家解压会变成 `mods/STS2_Momoi_v1.0.0/` 加载不到）。

#### 5. 产物 / 验证

- `dotnet build` **0 错误** → DLL **508,416 B**、PCK **131,853,648 B**（10-28 06:34）。
- 新增 `_verify_batch44.py` **56 条**；同步修正过期断言：`batch15/20/27/29/37/40/42`（数值与版本号）。
- **三十一套合计 1347 条断言全绿**。

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
- `工作区\发布包\STS2_Momoi_v1.0.2.zip`（125.0 MB，顶层 `STS2_Momoi/`：README.txt + dll + json + pck），旧的 v1.0.1 包已删。

#### 4. 产物 / 验证

- `dotnet build` **0 错误** → DLL **507,904 B**、PCK **131,853,648 B**（10-28 07:09）。
- 同步修正断言：`batch15`（注能恢复 AutoPlay）、`batch44`（回退 + id 前缀 + 1.0.2）、`batch42`（版本号）。
- **三十一套合计 1349 条断言全绿**。

### 21.53 批次46：黄金矿工读当前耗能 + 数值/文本批 + 卡牌统计（1.0.3，2026-10-28）

#### 1. 黄金矿工！：读「当前耗能」，而不是卡面印的费

```csharp
// 旧（错）：卡面印的 Canonical —— 被减费/加费过的牌按印的费算
var cost = picked.EnergyCost.Canonical;

// 新（对）：含局部修正 + 全局钩子的当前费用
var cost = picked.EnergyCost.GetWithModifiers(CostModifiers.All);
```

所以「剧情推进！+」（3 → 升级后 0 费）被消耗时，现在会走 **0 费分支**给「巨石+」，而不是按 1 费发能量+抽牌。
费用同时改成 **0/0**（升级只给保留）。

> API 备忘：`GetWithModifiers(CostModifiers.All)` = 当前费用（最常用）；`GetResolved()` = 解析后费用（X 费返回 CapturedXValue）；
> `GetAmountToSpend()` = 实际花费（X 费返回剩余能量）；只想看「印的费 + 改费」用 `CostModifiers.None`。

#### 2. 费用 / 数值

| 卡 | 改动 |
|---|---|
| 黄金矿工！ | **1/0 → 0/0**（升级只给保留） |
| 瓶颈突破 | 伤害 **5/5 → 4/4** |
| 见识下我的实力吧 | **1/0 → 0/0** |
| 日复一日，必有精进 | **3/2 → 3/3**（升级不再减费，升级只加「每次构想减费」） |
| 灵感爆发 | **1/1 → 1/0** |
| 来自勇者的加护 | 伤害 **8/10 → 6/9**（升级 +3） |

#### 3. 文本

- **仅局内显示的括号**：火力爆发「（已获得过 N 层）」、剧本打击「（抽 N 张牌）」、天马行空「（额外攻击 N 次）」、博览群游「（攻击 N 次）」
  统一套 `{InCombat:\n（…）|}`（空 else 分支 = 图鉴不显示），写法与原版 `BARRAGE` / `BODY_SLAM` / `COMPILE_DRIVER` 一致。
- **构想之矛 power**：每点构想的伤害常数 **8/11 → 11/15**（与卡面一致）。
- **矛与盾**：**卡面伤害** 8/11 → **11/15**（power 内部早就是 11/15，只是卡面没同步）。
- **开荒**：卡面「本场战斗中**未获得过**的特定诅咒」→「**未生成过**」；侧栏改成「**将依次生成以下诅咒**：苦恼，睡眠不佳，疑虑，执迷。」（诅咒名仍用红色）。
- **相遇**：「**铸造**」「**生成**」按关键词染金（eng：`Forge` / `Channel`）。

#### 4. 卡牌统计（本批实测）

| 分类 | 数量 |
|---|---|
| **角色卡池**（`[RegisterCard(typeof(STS2_MomoiCardPool))]`，可掉落 / 起始牌） | **91** |
| **衍生牌**（`TokenCardPool`：支援牌 12、构想、系统：阿比舒、绷住链 3、矛与盾、方块 4、渔获、传送门悖论其一/其二、我的回合！/WIN！/LOSE！/见识下我的实力吧/大姐姐、小游戏牌…） | **44** |
| **合计卡牌** | **135** |
| ↳ 其中 **小游戏牌**（minigame 标签） | **14** |
| ↳ 其中 **游戏牌**（fullgame 标签，在角色卡池里） | **6** |

> 顺带发现：`localization/zhs/cards.json` 里有一条 `STS2_MOMOI_CARD_FRIENDLY_DUEL_B.title`，但代码里**没有对应类**
> （是早期「友好的决斗」变体留下的孤儿词条），不影响运行，暂不处理。

#### 5. 版本 1.0.3 + 发布包

- csproj `<Version>1.0.3</Version>` + 清单 `version: 1.0.3`。
- `工作区\发布包\STS2_Momoi_v1.0.3.zip`（125.0 MB，顶层 `STS2_Momoi/`），旧的 v1.0.2 包已删。

#### 6. 产物 / 验证

- `dotnet build` **0 错误** → DLL **508,416 B**、PCK **131,855,024 B**。
- 新增 `_verify_batch46.py` **40 条**（含卡牌统计断言：91 / 44 / 135 / 14 / 6）；同步修正 `batch20/35/40/42/44` 的过期断言。
- **三十二套合计 1389 条断言全绿**。

---

### 21.54 批次47：飞溅 / 万花筒 / 棱彩宝石 角色隔离开关 + 工坊发布素材（1.0.4，2026-10-31）

#### 1. 三个开关

设置页「通用」新增三个开关（默认全开，和已有的「色彩哲学家 / 海玻璃」一致）：

| key | 文案 | 关掉之后 |
|---|---|---|
| `splash_pool` | 飞溅出现该角色卡牌 | 其他角色打出**飞溅**时，不再随机到本模组的攻击牌 |
| `kaleidoscope_pool` | 万花筒出现该角色卡牌 | **万花筒**给的 3 个池里不再有本模组角色池 |
| `prismatic_gem_pool` | 棱彩宝石出现该角色卡牌 | **棱彩宝石**把角色池 union 进奖励候选时不再带本模组角色池 |

#### 2. 实现：作用域标记 + 一处收口（`Patches/MomoiRandomPoolPatches.cs`）

三条途径最后都只读 `UnlockState.CharacterCardPools`（`UnlockState.cs:111` = `Characters.Select(c => c.CardPool)`）：

| 原版入口 | 位置 |
|---|---|
| `Splash.OnPlay(PlayerChoiceContext, CardPlay)` | `Splash.cs:25` |
| `Kaleidoscope.AfterObtained()` | `Kaleidoscope.cs:40` |
| `PrismaticGem.ModifyCardRewardCreationOptions(Player, CardCreationOptions)` | `PrismaticGem.cs:46` |

三个入口各一个 `IPatchMethod`：`Prefix` 置位 / `Postfix` 复位 `[ThreadStatic]` 计数；
`MomoiCharacterCardPoolsPatch`（`UnlockState.get_CharacterCardPools` 的 Postfix）在「任一标记为真且对应开关关闭」时收口：

```csharp
public static bool HideOurPoolNow =>
    (_splashDepth > 0 && !MomoiSettingsStore.SplashPool.Read())
    || (_kaleidoscopeDepth > 0 && !MomoiSettingsStore.KaleidoscopePool.Read())
    || (_prismaticGemDepth > 0 && !MomoiSettingsStore.PrismaticGemPool.Read());

// get_CharacterCardPools 的 Postfix
if (__result is null || !MomoiPoolIsolation.HideOurPoolNow) return;
__result = __result.Where(pool => !MomoiPoolIsolation.IsOurPool(pool));   // pool is STS2_MomoiCardPool
```

为什么不按 QA 说的 `CanBeGeneratedInCombat => false`：那是**静态**的，会把「自己玩小桃」时战斗内的随机生成/变形一起挡掉。
为什么不用 `options.WithFilter(...)`：**万花筒是单池建选项**（`new CardCreationOptions([pool], …)`），
过滤成空后 `CardFactory.CreateForReward` 里 `selectedRarity == CardRarity.None` → 抛
`InvalidOperationException("Tried to create a card for a reward, but we couldn't generate a valid rarity! ...")`，
`Kaleidoscope.cs:44` 的 `.First()` 也拿不到东西。所以只摘「候选池」，`Take(3)` 自然少一个。

安全性：
- 开关默认开 → `HideOurPoolNow` 恒 false，玩法零变化。
- 飞溅/万花筒**本来就排除自己的角色池**，所以自己玩小桃时这两个标记无影响；棱彩宝石是 `CharacterCardPools.Union(options.CardPools)`，玩家自己的池还在，摘掉本模组池不会空。
- 标记只在第一次 `await` 之前的同步段落里为真，三个入口都在那之前读完集合。
- 良性失败模式：万一 `Prefix` 跑了 `Postfix` 没跑，`_depth` 残留；而 `HideOurPoolNow` 只在**开关关闭**时才为 true，所以「开关开着却被隐藏」不会发生。

#### 3. 工坊发布素材（`工作区\工坊发布\`）

| 文件 | 说明 |
|---|---|
| `STS2_Momoi\Content\STS2_Momoi\` | 模组本体三件套（json 783 / dll 512,000 / pck 131,854,936），与 `v1.0.4.zip` 同源 |
| `STS2_Momoi\image.png` | 工坊主图，来自 `工作区\美术成品区\模组头像.png`（用户把 `预览图.png` 改名了），512×512 / 253KB。**上传器只认 `image.png`，而且必须在工作区文件夹里**（放外层报 `There is no file named image.png in the workspace!`） |
| `STS2_Momoi\workspace.json`（另有 `workshop.json` 同内容备份） | `title` 已填、`description` = 简介全文、`visibility: private`、`tags`/`dependencies` 空 |
| `工坊简介.txt` | Steam BBCode：`[b]`/`[h2]`/`[h3]` 全闭合；`[*]` 去掉改成 `[h3]` 小节（Steam 的 `[*]` 必须包在 `[list]` 里）；`（需要Ritsulib）`→`（需要RitsuLib）`；到「作者qq：2631262742」结束 |
| `截图\01..16.jpg` | 由 `工作区\美术成品区\工坊预览图\*.png` 压缩（1/2/3 超 1MB → 217/248/259KB，其余原分辨率转 JPG），全部 <1MB |
| `上传.bat` | `ModUploader.exe upload -w STS2_Momoi`；找不到 exe 时打印下载地址提示 |
| `上传步骤.md` | 四步 + 字段说明 + 报错兜底 + 以后更新的流程 |

生成脚本：`工作区\_scripts\_workshop_images.py`（PIL：RGBA 压黑底、>1920 缩宽、q88 起逐级递减到 <1MB）。

上传前**唯一**需要人工做的：把 `ModUploader.exe` 放进 `工作区\工坊发布\`（本机 DNS 把 github.com 解析到 127.0.0.1，我下不了），双击 `上传.bat`；
上传后到工坊页把可见性改公开、补 16 张截图（上传器只负责 `image.png` 主图）。

> **2026-10-31 实机上传成功**：`ModUploader.exe upload -w STS2_Momoi` → 新条目 id **3830602273**（写进 `STS2_Momoi\mod_id.txt`），当时 `visibility: private`。剩下的人工动作 = 页面上把可见性改公开 + 图片区补 16 张截图 + 按需补 tags；以后更新同一条目直接跑同一条命令。

> **踩坑（bat 编码）**：`上传.bat` 第一版写了中文并加了 `chcp 65001`，双击后 cmd 按 **GBK** 解析 UTF-8 的 bat，多字节字符把命令行切碎，报 `'请先从 https:' 不是内部或外部命令` / `'loader.exe' 不是内部或外部命令`。改成 **纯 ASCII 文案 + CRLF 换行** 后正常；以后 bat 里不要写中文。

#### 4. 版本 1.0.4 + 产物

- csproj `<Version>1.0.4</Version>` + 清单 `version: 1.0.4`；清单 description 改成「135 张卡牌（角色池 91 + 衍生 44）」。
- `工作区\发布包\STS2_Momoi_v1.0.4.zip`（125.0 MB），v1.0.3 包已删。
- `dotnet build` **0 错误** → DLL **512,000 B**、PCK **131,854,936 B**。
- 新增 `_verify_batch47.py` **91 条**；同步修正 `batch42/44/46` 的版本断言、`batch42/43` 的预览图路径（`预览图.png` → `模组头像.png`）。
- **三十三套合计 1480 条断言全绿**。

#### 21.55 批次48：RitsuLib 前置依赖（清单 `min_version` + 工坊 required item + 简介前置链接）

**为什么之前的依赖是「假」的**：清单里一直是 `{"id": "STS2-RitsuLib", "version": "0.6.10"}`，但原版 `Core/Modding/ModDependency.cs:10` 只有
`[JsonPropertyName("min_version")] public string? minVersion;` —— **`version` 是未知字段，`System.Text.Json` 静默忽略**，
于是 `declaredDependency.minVersion == null`，加载器只检查「RitsuLib 在不在」，等于完全没有版本下限。

**本批改动**：

1. `STS2 Momoi/STS2_Momoi.json` 依赖改成 `{"id": "STS2-RitsuLib", "min_version": "0.6.7"}`。
2. `STS2 Momoi.csproj`：`SyncManifestDependencies` → `ValidateManifestDependencies`，**只校验、绝不回写**：
   - 缺 `min_version` → Error；
   - 声明下限**高于**编译所用包版本 → Error（`System.Version.CompareTo`，字符串比较会把 `0.6.10` 判成小于 `0.6.7`）；
   - 通过时打印 `STS2-RitsuLib min_version 0.6.7 <= package 0.6.10`。
   旧目标会把该字段改写成本次编译解析到的包版本（我临时钉 0.6.7 试编译时它就把 `0.6.10` 悄悄改成了 `0.6.7`），
   每升一次 NuGet 就抬一次下限，旧版玩家直接被 `MOD_ERROR.DEPENDENCY_VERSION_UNSUPPORTED` 挡在门外。
3. **底线 0.6.7 是实测的**：把 `PackageReference` 临时改 `Version="0.6.7"` → `dotnet build` **0 错误 / 31 警告（与 0.6.10 一模一样）**，
   然后恢复 `Version="*"`（当前解析 **0.6.10**，Steam 上装的就是 0.6.10）。
4. 工坊：`workspace.json` / `workshop.json` 的 `dependencies` = `[3747602295]`（**数字、不加引号**，3747602295 是 RitsuLib 的工坊 id），
   上传日志确认 `Added dependency on 3747602295`。
5. 简介加前置小节，`工作区/工坊发布/工坊简介.txt` 与两个 json 的 `description` 三处同步：

   ```
   [h2]前置[/h2]
   [url=https://steamcommunity.com/sharedfiles/filedetails/?id=3747602295]RitsuLib[/url]（必需，最低 0.6.7）
   ```

   并删掉原来那句裸文本 `（需要RitsuLib）`。**上传器每次上传都会用 json 覆盖工坊的 title/description**，
   所以前置链接必须落在 json 里，只在网页上手改会被下一次上传冲掉。
6. `README.md` / `README.en.md` 修正：原文（继承自 RitsuLib 模板）写的是「`dependencies[].version` 才是最低版本」，
   还声称「旧版 `min_version` 写法已不支持」，与代码正好相反 —— 改成 `min_version`，并写明写成 `version` 会被静默忽略。

**原版依赖校验链**（`Core/Modding/ModManager.cs:719-767`，任一不满足 → `mod.state = Failed` + 报错弹窗）：

| 情况 | LocString key |
|---|---|
| 依赖 Mod 没加载 | `MOD_ERROR.MISSING_DEPENDENCY` |
| `min_version` 字符串解析不了 | `MOD_ERROR.DEPENDENCY_MIN_VERSION_INVALID` |
| 被依赖方清单没写 `version` | `MOD_ERROR.DEPENDENCY_VERSION_MISSING` |
| 被依赖方 `version` 解析不了 | `MOD_ERROR.DEPENDENCY_VERSION_INVALID` |
| `mod2.version.CompareTo(minVersion) < 0` | `MOD_ERROR.DEPENDENCY_VERSION_UNSUPPORTED` |

另：`ModManifest.ReadFromStream` 会把**纯字符串数组**的老式依赖迁移成 `{id, min_version: null}`，并记 `MOD_ERROR.MIGRATION_REQUIRED`。

**工坊 tags（`Characters` + `schinese`）**：工坊页面**没有**改 tag 的入口，`ISteamUGC::SetItemTags` 只能在上传时调用 —— 所以 tag 必须写进
`workspace.json` / `workshop.json` 的 `tags` 数组，再重跑一次 `upload` 才生效。本项目填 `["Characters", "schinese"]`：
`schinese` 是 Steam 的**简体中文**标签键（没有 `Chinese` 这个键，写了也不显示），`Tools & APIs` 是留给工具/API 类模组的，内容模组别勾。
顺带修掉一个潜藏 bug：`_发布清单.md` 里「图片区补 `截图\01.jpg … 16.jpg`」那行的 `\0` 曾被 heredoc 吃掉、写进了控制字符 `\x01`（grep 看不出来，`repr` 才发现）—— 已修正；以后改含 Windows 路径的 md 一律用 `chr(92)` 拼反斜杠，改完扫一遍 `ord(c) < 32`。

**工坊现状**：条目 **3830602273**（`private`）。2026-10-31 二次上传后内容 132MB，已带新清单、依赖 `3747602295`、含前置小节的简介；
剩余人工动作 = 页面改公开 + 图片区补 `截图/01.jpg … 16.jpg`。

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

#### 追加（同日）：「满溢灵感」「绿色挂饰」的同类多人泄漏

`AfterPlayerTurnStart(PlayerChoiceContext, Player)` 这类带 `Player` 参数的钩子，会对**每个玩家**的回合开始各触发一次，遗物必须自己判宿主：

| 位置 | 钩子 | 原状态 |
|---|---|---|
| `Cards/ConceptCard.cs` `AfterPlayerTurnStart` | 构想自身的数值增长 | 本来就有 `player != Owner` 守卫 |
| `Relics/DriedInspiration.cs` `AfterPlayerTurnStart` | 枯竭灵感发构想 | 批次50 已加守卫 |
| `Relics/MoreRelics.cs` `OverflowingInspiration`（满溢灵感） | 回合开始发「构想+」 | **缺守卫 → 队友回合也会拿到一张构想+** |
| `Relics/MoreRelics.cs` `GreenCharm`（绿色挂饰） | 回合开始可选消耗一张诅咒给构想 +1 | **缺守卫 → 队友回合也会弹选择界面** |

两处都按 `DriedInspiration` 的写法补上：

```csharp
// 多人模式：这个钩子会对所有玩家的回合开始都触发一次，遗物只服务它自己的主人。
if (player != Owner) { return; }
```

其余带 `Player` 参数的钩子逐个核对过，都已有守卫：`Cards/RemainingCards3.cs` 的 `ShouldTakeExtraTurn` / `AfterTakingExtraTurn`（`player == Owner.Player`）、`Cards/RemainingSpecialCards.cs` 的 `ShouldPlayerResetEnergy`（`player != Owner.Player`）、`Cards/ReworkBatch.cs` 的 `BeforeHandDraw`（`player != Owner.Player`）、两张注能牌的 `AfterAutoPrePlayPhaseEntered`（`ImbuedSupport.CanAutoPlayNow` 内含 `player == card.Owner`）。

自检加了第 [6] 段：`DriedInspiration` / `OverflowingInspiration` / `GreenCharm` 三个类体都必须出现 `if (player != Owner)`，`ConceptCard` 必须是 `if (player != Owner ||`。

### 21.58 批次51：工坊更新说明（changeNotes）+ 1.0.7 重新上传（1.0.7，2026-11-02）

用户贴了工坊更新流程的 QA，并要求把本轮的更新清单放到工坊条目上。**两版做法**：

1. **第一版（已废弃）：塞进 `description`（简介下面）** —— 把 `[h2]1.0.1更新：[/h2]` + 9 条 `[*]` 追加到 `工作区/工坊发布/工坊简介.txt` 末尾并同步进两个 json 的 `description`，总长 1394 → 1922 字符，重新上传成功（内容 48,912,164 B，id 3830602273）。但用户在工坊页面**看不到**这段文字（简介字段没有体现）。
2. **第二版（当前）：放进 `changeNotes`（工坊页面「更新改动」栏）** —— `description` 回退成原简介（1394 字符，以 `作者qq：2631262742` 结尾），更新清单写进 `workspace.json` / `workshop.json` 的 `changeNotes`，同时在 `工作区/工坊发布/更新说明.txt` 留一份可复用副本。再上传一次即生效。

写法约束（两处都适用）：

- Steam 的 `[*]` **必须包在 `[list]` / `[olist]` 里**才渲染成圆点，裸露的 `[*]` 会原样显示成方括号文字 → 清单外面套了一层 `[list]` … `[/list]`。
- 标题里的「1.0.1」保留用户原文（当前实际版本 1.0.7），要改只需替换这一个标题。
- `title` / `description` / `changeNotes` / `tags` / `dependencies` 都会在每次 upload 时**覆盖**工坊页面的对应字段 —— 所以任何文案改动必须落回 `workspace.json` 再传，只在网页手改会被下一次上传冲掉。
- `visibility` **不要**写进 json（写了每次上传都会把可见性改回该值）；默认留 `private`，由用户自己在页面改公开。
- 预览图这版 uploader **只认 `image.png`**（QA 里写的 `image.jpg` 是旧版说法），工作区里是 `STS2_Momoi/image.png`（253 KB < 1MB）。

上传命令：`cd 工作区/工坊发布` → `./ModUploader.exe upload -w STS2_Momoi`。工作区里的 `mod_id.txt`（`3830602273`）让 uploader 复用同一条目，订阅/收藏不丢。本次日志：`Using workshop item ID 3830602273 from mod_id.txt` → `Found 1 dependencies.` → `No modifications were made to dependencies.` → `Successfully uploaded '游戏王小桃 / Game King Momoi —— 尖塔2角色mod' … id 3830602273`。以后更新：把新的 dll/pck/json 覆盖进 `STS2_Momoi/Content/STS2_Momoi/`，双击 `工作区/工坊发布/上传.bat`（纯 ASCII + CRLF，避免 cmd 按 GBK 解析中文 bat 报错）。

3. **第三版（当前，用户自己贴）**：用户在页面上仍然看不到「更新改动」里的内容 → 改为输出一份可直接粘贴的**标准格式公告** `工作区/工坊发布/更新公告_标准格式.txt`：`[h2]1.0.1更新：[/h2]` + `[list]` 内 8 条 `[*]` + 末尾那句「感谢大伙的游玩与反馈…」单独提出来做成 `[h3]` 小标题（用户明确要求 h3）。`changeNotes` 与 `更新说明.txt` 同步成这份文本，但**不再由我这侧上传**（用户自己贴到工坊页面）。

标准格式清单（Steam 支持的子集）：`[h1]`~`[h3]`、`[b]`、`[i]`、`[u]`、`[strike]`、`[spoiler]`、`[code]`、`[hr]`、`[list]`+`[*]`、`[olist]`+`[*]`、`[quote]`、`[url=…]`、`[img]`；**不支持** `[table]`/`[color]`/`[size]`/`[font]`/`[align]`/`[indent]`。`[*]` 必须在列表里。

自检：`工作区/_scripts/_verify_batch51.py`（[1] 描述不含更新清单且以作者 qq 结尾、[1b] `changeNotes` 与 `更新说明.txt` 一致且 `[*]` 都在 `[list]` 内、[2] Content 1.0.7、[3] 上传记录与预览图、[4] 版本与发布包、[5] 文档）。另把 `_verify_batch47.py` / `_verify_batch48.py` 里「简介以作者 qq 结尾」的断言恢复/保留（描述不再有清单），`_verify_batch47.py` 恢复「`[*]` 不许出现在描述里」。

### 21.59 批次52：贴图大小默认 1.0（小桃本体 0.7）+ 出牌卡顿修复（1.0.8，2026-11-04）

#### 1. 设置「角色贴图大小」：默认 1.0、范围 0.5~1.5，小桃本体固定 0.7

用户反馈：滑块会同时缩放**所有**玩家角色，而小桃的素材本身就偏大，默认 0.7 时别人（原版角色）也跟着变小。要求「默认值 1.0、范围 0.5~1.5，但王小桃默认用素材的 0.7，设置里仍显示 1.0」，并明确「影响所有角色本来算 bug，但这个 bug 保留当特色」。

实现（`STS2 Momoi/STS2 MomoiCode/Settings/MomoiSettings.cs`）：

| 项 | 改前 | 改后 |
|---|---|---|
| `MomoiModSettings.CharacterTextureScale` | `0.7` | **`1.0`** |
| `MomoiSettingsStore.TextureScaleFactor` | `Math.Clamp(x, 0.2, 1.2)` | `Math.Clamp(x, 0.5, 1.5)` |
| general 段滑块 | `AddSlider(…, 0.2, 1.2, 0.05, v => $"{v:0.00}x")` | `AddSlider(…, 0.5, 1.5, 0.05, …)` |

`STS2 Momoi/STS2 MomoiCode/Patches/MomoiCharacterScalePatch.cs`:

```csharp
public const float MomoiDefaultScale = 0.7f;   // 王小桃素材自身的比例（写死，不进设置）

[HarmonyPrefix]  NCreature.ScaleTo(float size)
    if (__instance?.Entity is not { IsPlayer: true }) return;   // 怪物不动
    size *= MomoiSettingsStore.TextureScaleFactor;              // 滑块
    if (__instance.Entity.Player?.Character is STS2_MomoiCharacter) { size *= MomoiDefaultScale; }
```

* 为什么写死而不是改素材：素材是按美术观感画的，0.7 是「这张立绘在战斗里的正确比例」，属于内容而不是玩家偏好；放进设置会让「换角色 = 换观感」变得不可预期。
* `MomoiCombatRoomAddCreaturePatch`（`NCombatRoom.AddCreature` Postfix → `GetCreatureNode(creature)?.ScaleTo(1f, 0.0)`）保持传 `1f`：Postfix 走的是同一个 Prefix，传倍率会乘两次。
* 判定用 `Character is STS2_MomoiCharacter` 而不是「有没有我们的遗物/卡池」——玩家在自定义种子/改装角色下也成立。

#### 2. 出牌卡顿：逐条对照 QA，最后定位在「帧贴图首次解码」

按 QA 的五条逐一核对本项目：

| QA 条目 | 本项目情况 |
|---|---|
| 1. 特效场景没进缓存（`PreloadManager` 切场景清缓存 → 每次 `ResourceLoader.Load`） | **命中（本地版本）**：我们没有 VFX 场景，但战斗帧是**按路径声明**的贴图序列（`STS2 MomoiCharacter.cs` 的 `ModVisualCues.CueSet()`，600×820 一帧十几张）。第一次播到才解码，且切场景后缓存被清 → 每场战斗第一次出牌必停顿 |
| 2. `OnPlay` / 钩子里同步做重活 | 无牌堆全扫、无同步读图；但 `VigorPower.BeforeAttack/AfterAttack` 与 `MomoiCardAnimationCue.Trigger` **每张牌都无条件写一行 log**（写盘 + 格式化），属于白捡的开销 |
| 3. 整手牌描述反复重算（`ComputedDynamicVar`） | 全项目**没有** `ComputedDynamicVar`；`IndependentCalculatedVar` 只做一次字典查名，可忽略 |
| 4. 特效节点堆积（粒子 / `QueueFreeSafely` / `fixed_fps`） | 不适用：我们只创建 `AudioStreamPlayer` 与一个控制器 `Node` |
| 5. 角色动画没声明好（缺 Cast → 回落默认动画） | 动画走 RitsuLib `VisualCueSet`，`Attack`/`Cast` 都显式声明；**但** `MomoiAnimMachineTrackPatch` 同时挂在 `ModAnimStateMachine.Start` 和 **`SetTrigger`** 上（只为登记实例），而 `SetTrigger` 是每次攻击/施法都跑的热方法 |

修复（5 项）：

1. **cue 帧贴图预热** —— 新 `Patches/MomoiCueWarmupPatch.cs`：`NCombatRoom.AddCreature` Postfix，仅当进房间的是小桃玩家时，挂一个临时 `Node`，用 `DirAccess.Open($"{Entry.ResPath}/images/characters/cue")` 列出全部帧路径，**每帧 4 张** `ResourceLoader.Load<Texture2D>(path, cacheMode: ResourceLoader.CacheMode.Reuse)`（`await ToSignal(tree, SceneTree.SignalName.ProcessFrame)` 分帧），完成后 `QueueFree()`。`Reuse` 让贴图常驻，不再被换场景清掉。
2. **卡框材质只读一次 + UV 变体缓存** —— `Patches/MomoiCardFrameMaterialPatch.cs` 静态 `_cached` / `_loadAttempted`；`Patches/MomoiCardFrameVisualPatch.cs` 用 `Dictionary<(Vector2 Offset, Vector2 Scale), ShaderMaterial> Variants` 缓存 `Duplicate()` 出来的材质，并用 `ReferenceEquals(frame.Material, material)` 避免重复赋值（原来每次 `NCard.Reload` 都新建一份材质 → 手牌区一堆重复材质，触发额外重绘）。
3. **音频流缓存** —— `Audio/MomoiAudio.cs` 直放路径加 `ConcurrentDictionary<string, AudioStream> StreamCache` + `GetOrAdd`，不再每次 `ResourceLoader.Load<AudioStream>`。
4. **动画面板监听瘦身** —— `MomoiAnimMachineTrackPatch` 只留 `ModAnimStateMachine.Start`。
5. **热路径日志收口** —— 新增 `Diagnostics/MomoiDiag.cs` + 设置项「输出详细日志」（`verbose_logging`，默认关）：`MomoiDiag.Log` 只在开启时写盘。`VigorFirepowerPatch`（6 条）、`MomoiCardAnimationCuePatch`（3 条）、`MomoiAudio`、各小游戏/循环叙事/注能诊断日志（`GameLife` 1、`MinigameFlowCards` 6、`MinigameSupport` 1、`NewCardsBatch` 1、`RemainingCards2` 4、`ReworkBatch` 1、`ImbuedSupport`、`MomoiImbuedAndCompendiumPatches`）全部改走开关；**失败类 `Warn` 仍无条件输出**（排查要靠它）。

> 诊断建议（用户曾问怎么定位）：装 Speed Control 加速看卡顿是否随动画时长一起缩——跟着缩就是动画/等待，不缩就是逻辑侧；再看 `godot.log` 出牌那一刻的异常与 WARN。本批把「逻辑侧」的写盘与重复实例化都清掉了。

#### 3. 产物与自检

* 版本 **1.0.8**：`STS2 Momoi/STS2 Momoi.csproj` `<Version>1.0.8</Version>` + `STS2 Momoi/STS2_Momoi.json` `"version": "1.0.8"`（`min_version: 0.6.7` 不变）。
* `dotnet build "STS2 Momoi.csproj"` → **0 错误 / 31 既有警告**；DLL **520,704 B** / PCK **57,833,324 B**（体积优化未回退）。
* 新自检 `工作区/_scripts/_verify_batch52.py`（11 段）；工坊 Content 同步 1.0.8 后 `ModUploader.exe upload -w STS2_Momoi` 重新上传成功：
  `Using workshop item ID 3830602273 from mod_id.txt` / `Found 1 dependencies.` / `No modifications were made to dependencies.` / `Successfully uploaded … id 3830602273`，内容 **58,354,796 B**、预览图 2,353,644 B。
* **`workspace.json` / `workshop.json` 里不再写 `visibility`**：上传器会用 json 覆盖工坊条目，写死 `private` 会把页面上的公开状态改回私密；留空则不动它（tags / dependencies 仍必须写在 json 里，页面没有入口）。

#### 3.1 工坊上传字段归属（用户 2026-11-04 反馈后定稿）

用户反馈「每次上传都把我改过的标题改回去」。查 `template/README.md`（上传器自带的说明书）确认：

> Most properties can be substituted with `null` or removed from the JSON if you wish for them to remain unchanged after the initial upload.

所以 `workspace.json` / `workshop.json` **只留必须由文件维护的三项**（页面没有入口或需要随版本走）：

| 字段 | 是否写进 json | 原因 |
|---|---|---|
| `description` | ✅ 写 | 简介里有 `[h2]前置[/h2]` + RitsuLib 链接，由脚本随版本维护 |
| `tags` | ✅ 写 | **工坊页面没有改 tag 的入口**，只能在 json 里设 |
| `dependencies` | ✅ 写 | required item 同上 |
| `title` | ❌ 不写 | 用户会自己改（含英文区），写了就被覆盖 |
| `visibility` | ❌ 不写 | 用户自己控制公开/私密，写 `private` 会把公开条目改回私密 |
| `changeNote` | ❌ 不写 | 更新说明由用户自己在页面编辑；本地留 `更新说明.txt` / `更新公告_标准格式.txt` 当草稿 |

另外：上传器真正的字段名是 **`changeNote`（单数）**，我们以前写的 `changeNotes` 是**未知键、被忽略** —— 这就是批次51 里「json 写了更新说明但工坊页面看不到」的真正原因（不是 Steam 的问题）。

标题最终定稿：`王小桃 / Momoi —— 尖塔2角色mod`（1.0.8 用这个标题重传过一次，之后不再写 json）。

#### 4. 本批踩的坑（都值得记）

1. **`python` CLI 是坏的**：`python - <<'PYEOF'` 直接静默不执行（退出码 0 但什么都没改）。第一次改 `VigorFirepowerPatch.cs` 的日志因此完全没生效，回读才发现。→ 一律 `"C:/Users/asus/AppData/Local/Python/pythoncore-3.14-64/python.exe"`。
2. **文件带 BOM**：`s.splitlines()[0].startswith("using")` 因 `\ufeff` 恒为 False，插 `using` 要按「最后一个 using 行之后」插。
3. **C# 模式语法**：`if (__instance?.Entity is not { IsPlayer: true } creature)` 不成立（属性模式不能绑定变量），要么 `is not { IsPlayer: true }` 直接 return，要么 `is { IsPlayer: true } creature`。
4. **PIL 已装但只在项目解释器里**：图片脚本用绝对路径跑，别用 `python`。
