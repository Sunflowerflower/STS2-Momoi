# 游戏王小桃 / Game King Momoi —— 尖塔2角色 Mod

《Slay the Spire 2》的角色 Mod：新增可玩角色**游戏王小桃**，以及一整套围绕「游戏」设计的卡牌体系。

- **135 张卡牌**：角色牌池 91 张 + 衍生牌池 44 张（其中小游戏牌 14 张、游戏牌 6 张）
- **9 件遗物** + **3 瓶药水**
- 核心机制：**构想**（保留成长的特殊牌）、**小游戏牌**（还原经典小游戏的衍生牌）、**火力 / 活力**、**灼烧**、**支援牌**
- Steam 工坊条目：<https://steamcommunity.com/sharedfiles/filedetails/?id=3830602273>
- 依赖前置模组：[RitsuLib](https://steamcommunity.com/sharedfiles/filedetails/?id=3747602295)（`min_version` 0.6.7）

> 本仓库是**源码仓库**：包含全部 C# 代码、本地化文本、场景/着色器、设计文档与自检脚本。
> 图片 / 音频 / 视频资源（约 181MB）与构建产物（`.pck`）**不在仓库内**，原因见下文「资源去哪了」。

---

## 技术栈

| 项目 | 说明 |
|---|---|
| 语言 / 运行时 | C# / .NET 9（`net9.0`），程序集名 `STS2_Momoi` |
| Mod 框架 | [RitsuLib](https://steamcommunity.com/sharedfiles/filedetails/?id=3747602295)（NuGet `STS2.RitsuLib`），提供卡牌/遗物/药水注册、Harmony 补丁封装、设置页、动画状态机等 |
| 引擎 | Godot 4.5 mono（只用于资源打包与场景/着色器；逻辑全在 C#） |
| 目标游戏版本 | Slay the Spire 2 测试版 `0.111.0` |
| 当前 Mod 版本 | `1.0.8` |

---

## 目录结构

```
STS2 Momoi/                     ← 可以独立编译的工程
├─ STS2 Momoi.sln
├─ STS2 Momoi.csproj            ← 版本号、RitsuLib 包引用、PCK 导出与部署目标
├─ STS2_Momoi.json              ← Mod 清单（id / version / dependencies.min_version）
├─ project.godot, export_presets.cfg
├─ local.props.template         ← 复制成 local.props 并填本机 Steam 路径
├─ STS2 MomoiCode/              ← ★ 全部 C# 代码（约 90 个文件）
│  ├─ Entry.cs                  ← 入口：注册卡池/角色/补丁/设置，Mod 初始化
│  ├─ Cards/                    ← 卡牌与能力（Power）实现，按主题分文件
│  ├─ Characters/               ← 角色、卡池、遗物池、药水池、视觉 cue
│  ├─ Relics/ Potions/          ← 遗物与药水
│  ├─ Patches/                  ← Harmony 补丁（伤害修正、UI、工坊池隔离、预热等）
│  ├─ Settings/                 ← 设置页（本机设置存 settings.json）
│  ├─ Audio/ Tips/ Diagnostics/ ← 音频、侧栏提示、诊断日志开关
│  └─ CombatStats.cs RunStats.cs
└─ STS2_Momoi/                  ← Mod 资源目录（打进 .pck）
   ├─ localization/{zhs,eng}/   ← ★ 全部文本（扁平 JSON 键值，见下）
   ├─ scenes/ scripts/ shaders/ materials/
   └─ images/ audio/ videos/    ← ⚠ 不在仓库内（见「资源去哪了」）

STS2_Momoi_迁移文档.md           ← ★ 主设计文档：§21.1 ~ §21.59 逐批次的改动、根因分析、踩坑记录
research.md                      ← 早期探索笔记（游戏 API / Mod 可行性）
工作区/                          ← 工作区（大文件已在 .gitignore 排除）
├─ _docs/                       ← 发布清单、美术待补清单、代码审核、开发经验等
├─ _scripts/                    ← 构建/发布/自检脚本（★ 38 套 _verify_batch*.py，约 1792 条断言）
├─ _data/                       ← 卡牌索引、美术状态等机器可读快照
└─ STS2Momoi.xlsx               ← 卡牌数值总表
```

---

## 代码是怎么组织的（给读代码的人 / AI）

1. **一张卡 = 一个类**，继承 RitsuLib 的 `ModCardTemplate`，用 `base(费用, CardType, CardRarity, TargetType)` 声明基础属性，`CanonicalVars` 里挂 `DamageVar` / `BlockVar` / `DynamicVar`，`OnPlay` 里用 `DamageCmd` / `CreatureCmd` / `PowerCmd` 组合效果，`OnUpgrade` 里改数值。
2. **能力（Power）= `ModPowerTemplate` 子类**，通过 `AfterXxx` / `ModifyXxx` 钩子工作；层数显示走 `DisplayAmount`。
3. **文本**全在 `STS2_Momoi/localization/{zhs,eng}/*.json`，是**扁平键**（`"STS2_MOMOI_CARD_XXX.description": "…"`），支持 `{Damage}` 变量与 `{IfUpgraded:show:…|…}` / `{InCombat:…|}` 条件段；颜色约定：`[gold]` 关键词、`[blue]` 能力数值、`[green]` 治疗、`[red]` 背景风味。
4. **补丁**集中在 `Patches/`，每个补丁实现 RitsuLib 的 `IPatchMethod`（`PatchId` / `GetTargets()` / `Prefix|Postfix`），统一在 `Entry.cs` 里 `patcher.RegisterPatch<T>()` 注册。
5. **诊断日志**统一走 `Diagnostics/MomoiDiag`，默认关闭（设置页「输出详细日志」），不要直接用 `Entry.Logger.Info` 写热路径。

---

## 构建

前置：

1. 安装《Slay the Spire 2》测试版（需要其 `sts2.dll`）
2. 本地 NuGet 缓存里有 `STS2.RitsuLib`（由游戏/工坊前置模组提供，见 `STS2 Momoi/README.md` 更详细的说明）
3. 复制 `STS2 Momoi/local.props.template` → `local.props`，把游戏安装路径填进去

```bash
cd "STS2 Momoi"
dotnet build "STS2 Momoi.csproj"
```

构建会：编译 DLL → 用 Godot headless 导出 `STS2_Momoi.pck` → 部署到 `<游戏目录>/mods/STS2_Momoi/`。
只改 C# 想跳过 PCK 导出时，加 `-p:STS2_SKIP_PCK_EXPORT=true`。

⚠ 贴图导入规则（体积优化）写在 `*.import` 里，而 `*.import` 被 `.gitignore` 忽略：从干净克隆构建前要先跑 `工作区/_scripts/_optimize_textures.py`，否则 PCK 会从 55MB 回到 130MB。

## 资源去哪了

`STS2_Momoi/images`（173MB 卡图/立绘/图标）、`audio`、`videos` 以及 `*.pck`、`bin`、`obj`、`.godot` 都**没有**进仓库：

- 对阅读/修改代码没有帮助，但会让克隆体积从 3MB 涨到 190MB+
- 美术素材有第三方版权（见 `NOTICE.md`），不适合放公开仓库再分发
- 想要能直接玩的版本，请订阅 Steam 工坊条目

## 自检

仓库里带了 38 套纯文本断言脚本，覆盖「卡牌数值、本地化措辞、补丁目标、版本号、发布包内容」等：

```bash
for f in 工作区/_scripts/_verify_batch*.py; do python "$f"; done
```

（脚本里硬编码了 Windows 绝对路径 `C:\Users\asus\RiderProjects\STS2 Momoi`，换机器需要改 `ROOT`。）

## 许可

- **代码**：MIT，见 `LICENSE`
- **美术 / 音频素材**：版权归原作者，仅用于本 Mod，详见 `NOTICE.md`

## 反馈

Mod 交流群：263898222 ｜ 作者 QQ：2631262742
