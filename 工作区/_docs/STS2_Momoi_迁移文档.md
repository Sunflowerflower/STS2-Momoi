# STS2_Momoi 迁移交接文档 —— **工作区版**（2026-10-16）

> **本文档是自包含的现行版**（旧版 2026-08-23 的内容——117 卡清单、ComfyUI 生图管线、单卡精修等——**已按用户要求删除**：卡面已 100% 完成，生图时代结束）。
> **仓库根的 `STS2_Momoi_迁移文档.md`** 是同一口径的全文版，另含逐批变更历史（§15~§21）与代码侧踩坑细节；本文档只讲**现状 / 后续重心 / 工作区职责 / 常用命令**。
> 两份文档口径必须一致：改完这边记得同步一句到根文档（反之亦然）。

---

## 1. 现状（2026-10-16）

| 项 | 值 |
|---|---|
| 部署 | `STS2_Momoi.dll` **512,000 B**（10-31 11:52）、`STS2_Momoi.pck` **131,854,936 B**（10-31 11:52）、清单 **游戏王小桃 1.0.4** |
| 构建 | `dotnet build` **0 错误 0 警告** |
| 内容 | 135 张卡（角色池 91 + 衍生 44）/ 54 个 power / 9 遗物 / 3 药水 |
| 自检 | **33 套 / 1480 条断言全绿**（`_verify_batch*.py` 通配逐个跑） |
| 卡面 | ✅ **133/133 全部真实成品**（0 共用占位、0 纯色占位） |
| power / 遗物 / 药水图标 | ✅ 全部成品（批次 10 接入 48 power 图标 + 9 遗物 + 3 药水，含白剪影轮廓） |
| **角色素材** | ❌ **唯一缺口**：`images\characters\` 12 张 + 选人背景 + 商店/篝火 + 战斗差分 6 张，仍是模板自带的铁甲战士占位 |

---

## 2. 后续重心（用户 2026-10-16 定的方向）

> **角色美术 → 卡牌调整 → 新的模组内容**。卡面时代结束，不要再找「还要生图」的待办。

### 2.1 角色美术（★★★）
逐项清单（含尺寸、用途、现在长什么样）：**`工作区\_docs\_美术待补清单.md`**。要点：

| 文件 / 位置 | 现在 |
|---|---|
| `images\characters\STS2_Momoi_character_icon.png`（88×88）+ `_icon_outline.png` | 铁甲战士头盔 |
| `STS2_Momoi_character_select.png`（132×195）+ `_select_locked.png` | 铁甲战士面罩 |
| `STS2_Momoi_map_marker.png`（49×64） | 铁甲战士的红色 V 形标记 |
| `STS2_Momoi_energy_orb_layer_1..5.png` / `energy_big.png` / `energy_text.png` | 铁甲战士的红色能量球 / 数字 |
| `scenes\characters\STS2_Momoi_character_select_bg.tscn` | 深蓝底 + 上面那两张图 |
| `STS2_Momoi_merchant.tscn` / `_rest_site.tscn` | 直接复用那张 132×195 面罩图 |
| `images\characters\cue\{idle,attack,cast,hit,dead,relaxed}.png`（600×820） | 线稿占位 |
| 多人手臂 ×4 / 转场 / 音频 | 未做 |

- **战斗差分不用改代码**：`STS2_MomoiCharacter` 已接 `VisualCues: ModVisualCues.CueSet()…Build()`，
  配 `scenes\characters\STS2_Momoi_character.tscn`（`Visuals` Sprite2D pos(0,-246) scale 0.6、`Bounds` ±108/-500..10）；
  **覆盖同名文件即可**，说明写在 `images\characters\cue\README.md`。
- RitsuLib 的 `CharacterAssetProfile` 共 **42 个字段**，待补清单里逐字段列了怎么填。

### 2.2 卡牌调整（★★）
- 入口 = **用户逐条点名**；不要自己开新战场。
- 改本地化 → `dotnet build` → 跑全部自检（32 套 / 1389 条断言）。
- 卡面数字必须用 `BlockVar` / `DamageVar` / `CardsVar` / `IndependentCalculatedVar`（普通 `DynamicVar` 会 `InvalidCastException` 且不随升级重算）。

### 2.3 新的模组内容（★）
- 先改权威表 `STS2Momoi.xlsx` → `_sync_design_dump.py` → 本地化四处（zhs / eng / xlsx / dump）。
- 新机制走 `Patches\*.cs`，**每个补丁都要登记进 `Entry.cs`**（忘了 = 静默不生效）。
- 关键词徽章（消耗/固有/保留/虚无…）由 `CanonicalKeywords` 自动附加，**描述里不要手写**；
  侧栏由 `Patches\MinigameSidebarPatch.cs` 按描述原文扫关键词自动加（活力/虚弱/火力/灼烧/妖体/易伤/缓冲/…）。

---

## 3. 工作区目录职责

```
工作区/
├─ STS2Momoi.xlsx            ★ 权威设计表（卡牌 / 遗物 / 药水 三 sheet；卡牌表从第 3 行起）
├─ _design_dump.txt          设计快照（= xlsx 的纯文本版），由 `_scripts/_sync_design_dump.py` 重建
├─ _scripts/                 所有 Python 脚本（自检、表格/本地化补丁、美术工具、查询小工具）
├─ _data/                    机读快照与统计（`_card_art_status.*`、`_power_icon_inventory.json`、`_card_index.txt` …）
├─ _docs/                    文档：本文件、`_美术待补清单.md`、`_power总览.md`、`_代码审核_批次16.md`、`_待做图标清单.md`（已作废）
├─ _backup/                  改动前备份（按批次：`batch11_pre` … `batch22_pre_迁移文档.md`）
├─ _session_export/ _session_export2/   历史会话导出
├─ 美术产品区分四块：
│   ├─ 美术成品区/卡面成品区/       卡面批次成品（每张一个 png）
│   ├─ 美术成品区/卡面修改1/       批次10 的卡面替换件
│   ├─ 美术成品区/power图标成品/   48 张 power 图标（含 4 张拆分 + 1 张改名）
│   ├─ 美术成品区/遗物成品区/ 药水成品区/   9 遗物 + 3 药水
│   └─ power图标成品/              与上面同一批（历史位置，保留）
├─ 编辑区/                   正在做的图：`卡面/<卡名>/`（内含 `_src` 脚本与 `_work` 中间产物）、`人物/`（空，待角色美术）、`图标/`
├─ 参考图集/                 画风参考 + `STS1图标/`（279 powers + 237 relics + 42 potions 对照图库）
├─ 已删卡_备份/              删卡时的源码/本地化/图/表格行备份
└─ 美术准备/                 生图时代遗留（`产出/` `脚本/` `状态/` `日志/` `备份/` `文档/`）——**接手不必再看**（根文档 §5.2）
```

> **生图管线（ComfyUI / `_pipeline.py` / 提示词 / 单卡精修）已随卡面收官退役**，只留三条结论：
> ① 程序化产出一律逐张 read 对照；② 白底抠图边缘发灰用 alpha bleed / color bleed；③ 刚性平移局部肢体用分层做法。

---

## 4. 常用命令

```bash
PY="C:\Users\asus\AppData\Local\Python\pythoncore-3.14-64\python.exe"   # 本机 python 会命中 Store 占位程序

cd "C:\Users\asus\RiderProjects\STS2 Momoi"

# 改完 xlsx 后同步快照
"$PY" 工作区/_scripts/_sync_design_dump.py

# 全部自检（24 套 / 1020 条；任一套失败先查清是脚本过期还是代码回归）
for f in 工作区/_scripts/_verify_batch*.py; do "$PY" "$f" | tail -1; done

# 体检 / 统计
"$PY" 工作区/_scripts/_check_keyword_dup.py      # 描述里手写了「会被自动追加的关键词」导致重复显示
"$PY" 工作区/_scripts/_regen_art_status.py       # 重算卡面完成度 → _data/_card_art_status.*
"$PY" 工作区/_scripts/_power_overview.py         # 重生成 _docs/_power总览.md

# 构建 + 部署（游戏必须先关）
cd "STS2 Momoi" && dotnet build "STS2 Momoi.csproj"
```

---

## 5. 协作红线（不会变）

1. **用户点名的才动手**，不要顺手美化、不要自己开新战场。
2. **文本逐字照抄**用户给的措辞；不要加解释性句子。
3. **不要手写**会被自动追加的关键词徽章（`固有。` / `消耗。` / `小游戏牌。` / `保留。`）。
4. 颜色规范**按表**：`cards` 数字不上色（只有 `[gold]` 关键词）；`powers` 数字 `[blue]`；`relics`/`potions` 数字 `[blue]`、回血 `[green]`、风味 `[red]`。
5. **报告要短**（用户遇到过 413 请求体超限）。
6. 改单文件片段用**精确文本替换**，不要手写切片拼接（批次 20 因此把 `RemainingSpecialCards.cs` 截断过，靠 `_backup` 才救回来）。

---

*文档结束。改本文件时请保持「现状 / 后续重心」两节的数字与根文档一致。*

---

## 6. 最近的卡牌调整批

| 批次 | 日期 | 内容 |
|---|---|---|
| 20 | 10-15 | 阿比舒最后一段的 4 倍改成真乘法（`ModifyDamageMultiplicative` 门控 `_finalHit`）、勇者加护 11→10 伤、消消乐首句缩短；期间一次文件截断事故已从 `_backup/batch15_pre` 完整恢复 |
| 21 | 10-15 | 阿比舒 3 段修复（`CreatureCmd.Damage` 一次只结算一次）、曳光弹数值（6/8 伤、3/4 灼烧、每 1 点活力 +1 层）、来自时的援助 2→0 费、阿比舒 0→1 费 |
| 22 | 10-16 | 曳光弹升级灼烧真因（`DynamicVar.Clone()` 浅拷贝 → `IndependentCalculatedVar` 改为按名字实时解析）、破势重做（2 费、16/20、活力 4/5 倍走新补丁 `VigorMultiplierPatch`）、整活补「升级过的」、吃豆人诅咒查三堆、堕落改罕见 + 1 层虚弱、独特点子改普通、专注 1→0 费、博览群游 0→1 费 |
| 23 | 10-16 | 「击晕」补金色（3 张，侧栏已有）、「终于上一档了！」金币补金色（**不加侧栏**，与原版一致） |
| 27 | 10-20 | 游戏人生标签改为**只本场战斗**（真因：`CloneForCombat` 不重建 `_tags`，克隆体与牌组本尊共用集合）+ 开局清理旧泄漏标签 + 手牌选择加拆场兜底；激战 5→3/0 费、开发秘籍→稀有、100连抽→罕见+固有+升级费 3、复盘→1 费技能去伤害；连连看选牌文案、跑酷「最多一张」可跳过、节奏游戏右下角显示伤害、吃豆人富足→WIN！、黄金矿工删死侧栏 |

| 29 | 10-22 | 跑酷删「回合开始时重复」+ **两个 power/基类/死图标/本地化键全删**；WIN！3/4、火焰附加灼烧 2/3、热火力 2/3、构想之矛 10/14、博览群游 7/9、再起新篇活力 3/4；瓶颈突破→普通、玩玩新作！→罕见；**专注小重做**（连续 2 回合 → 本回合，0 费，卡面/power 文本重写）；自检脚本覆盖事故已恢复（重建 24/28） |

| 30 | 10-22 | **专注**回到 1 费（升级 0），卡面与 power 文本**并成一句**（`小游戏牌/构想，+1/选择最多…`，power 侧 `{Amount}` + `{RetainCount}` 仍显示实际数值）；**天马行空**升级版卡面补「等同构想数值**+1**次」 |

| 35 | 10-24 | **剧本打击**括号数跟着升级（0 张 / 1 张，+1 从 multiplier 挪到 `CardsBase`，去掉 `{InCombat:…}`）；**重整旗鼓**自动打出阈值 **20% → 25%**（卡 + power 两处判定、中英文本、注释）；自检脚本第三次同名覆盖已恢复（重建 batch31） |

| 36 | 10-25 | **桃味气泡水变牌修复**：`FromHand` 的 `source` 改 `null`（药水模型永不抛 `ExecutionFinished` → 手牌 holder 不归位 → 白光后卡面不刷新）、逐张 `CardCmd.Transform(单张)`（同整活/原版护驾）；选牌界面 99 张 → **任意张**（`0~999999999` + 新文案 `STS2_MOMOI_ANY_TRANSFORM`）；顺手修 3 条过期断言 |

| 39 | 10-25 | 九张卡数值/费用（节奏游戏 18/24·6/4、打灰机 6/8·抽1/2、消消乐 1/0 费且升级不再保留、PvZ 1/0 费、花凛 32/40、晴 6/9、千寻 7/10、茜 12/15、大师 3/4+4/6、小玉 3/4）；**自助指南只能附魔防御的真因**（16 张给格挡的卡缺 `GainsBlock`）+ ? 事件全面体检（色彩哲学家文案键/桃红色、bestiaryQuote、能量图标路径兜底） |

| 40 | 10-25 | 复盘/王不见王「升级前消耗、升级后删去」；循环叙事 0 费+升级保留；日复一日 3/2 费且保留常驻；发布委托 2/2 费·格挡 11/14；局势升温 2/2 费·12/16；黄金矿工 1/0；愤怒的小鸟 1/1；瓶颈突破构想 1/2；构想之矛 11/15；矛与盾 11/15；整装待发 6/8+2/3；伏笔回收→罕见、100连抽→稀有；创作的痛苦加火力 2/3；扫雷炸弹改随机位置；再启新篇只在无构想时加费；博览群游改随机敌人；**新卡传送门悖论 / 过载**；**建筑师对打演出**（LoadDialogue 后补 Start/EndAttackers） |

| 41 | 10-25 | **多段攻击的活力/火力重复消耗修好**（拆多条 `AttackCommand` → `VigorPower.BeforeAttack` 只记第一条、`AfterAttack` 一次扣光）；创作的痛苦删去火力、三段改 `WithHitCount(3)`+`WithWaitBeforeHit(0.5,0.5)`（间隔不变、不加 OnlyPlayAnimOnce 保住每段弹幕）；100连抽 100 段同样合并 + OnlyPlayAnimOnce；全卡扫描零告警 |

| 42 | 10-26 | **发布完善**：正式中文名「游戏王小桃」（清单/设置页/README，角色名不变）；清单改正式值（author alkaid616 / 双语描述 / version 1.0.0 / min_game_version 0.111.0，csproj `<Version>1.0.0</Version>`）；设置页重排 general/audio/progress/diagnostics（版本卡 + 打开日志目录 + 重置设置）；确认免纪元无 RequireEpoch；工坊预览图 512×512/139 KB + 发布清单文档（tags/依赖/更新检查/自测项）。本版不接遥测 |

| 43 | 10-26 | 设置页收尾：隐藏模组简介（`WithDescriptionHidden`）、删掉「进度」里的纪元说明卡（该节只剩重置设置，标题「其他」）、日志目录确认按 `OS.GetUserDataDir()` 跨平台解析；预览图改用用户给的 `预览图.png`；**打出本地发布包** `工作区\发布包\STS2_Momoi_v1.0.0.zip`（顶层 `STS2_Momoi/`，含 README.txt），脚本 `_make_release_zip.py` |

| 44 | 10-28 | **22 项平衡调整**（过载 2 费·活力 2/3、修行 2 费、整装待发 4/6、天马行空 4/4、博览群游 5/7、节奏游戏 18/20·6/5·1 费…）；**注能修复**：新增置底补丁（第 1 回合抽牌前沉底）+ 开局改**直接结算**（不再 `CardCmd.AutoPlay`，修「两张绿开局卡 30 秒」）；**图鉴全解锁**（`InitProgressData` 后批量 MarkXxxAsSeen + 落盘，设置页另有手动按钮）；版本 **1.0.1** + 发布包 `STS2_Momoi_v1.0.1.zip` |

| 45 | 10-28 | **注能回退**成正常的 `CardCmd.AutoPlay`（保留置底修复 + 单次标记 + 日志兜底，卡顿待复现再修）；**衍生牌图鉴问号修复**：`MarkAll` 从「只按 STS2_MomoiCardPool」改成 **id 前缀 `STS2_MOMOI_`**（衍生牌都在 TokenCardPool）；版本 **1.0.2** + 发布包 `STS2_Momoi_v1.0.2.zip` |

| 46 | 10-28 | **黄金矿工读当前耗能**（`GetWithModifiers(CostModifiers.All)`，修「剧情推进！+ 应给巨石+」）+ 0/0 费；瓶颈突破 4/4、见识实力 0/0、日复一日 3/3、灵感爆发 1/0、勇者加护 6/9；**火力爆发/剧本打击/天马行空/博览群游括号改「仅局内显示」**（`{InCombat:\n（…）|}`）；构想之矛 power 11/15、矛与盾卡面伤害 11/15、开荒换「生成」措辞、相遇铸造/生成染金；卡牌统计 91 + 44 = 135（小游戏 14 / 游戏牌 6）；版本 **1.0.3** |

> 批次 24~26 是**角色动画**（10-17/10-18，idle / 攻击·能力·嘲讽 / hit），细节见根文档 §21.27~§21.29。

> 文档同步：本文件写「现状 + 后续重心」，逐批细节在仓库根 `STS2_Momoi_迁移文档.md` §21。
