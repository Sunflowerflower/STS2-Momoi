# -*- coding: utf-8 -*-
"""批次42 文档：§21.49 + 数字/套件表同步 + 指向发布清单。"""
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


rep(P_MAIN, "> **本次状态（2026-10-25 批次41）**",
 """> **本次状态（2026-10-26 批次42）**：**发布完善**。模组正式中文名 **「游戏王小桃」**（清单 `name` / 设置页标题 / README；角色名仍是「王小桃」）；
> 清单从模板占位改成正式值（`author alkaid616`、中英双语 description、`version 1.0.0`、`min_game_version 0.111.0`，csproj 同步 `<Version>1.0.0</Version>`）；
> **设置页重排成四节**：`general`（色彩哲学家/海玻璃卡池开关）、`audio`（六档音量）、`progress`（「本模组不需要纪元/时间线」说明卡 + **重置本模组设置** 按钮）、`diagnostics`（**模组+游戏版本信息卡** + **打开日志目录**）。
> 免纪元已确认到位（`RequiresEpochAndTimeline => false`，全模组无 `RequireEpoch`）。按用户决定**本版不接遥测**、不加特效强度开关。
> 工坊配套：预览图 `工作区\\美术成品区\\工坊预览图_512.png`（512×512 / 139 KB），发布清单 `工作区\\_docs\\_发布清单.md`（tags / Required Items / 更新检查模板 / 上线自测项）。
> `dotnet build` **0 错误**，DLL **504,320 B** / PCK **131,853,468 B**；二十九套自检 **1265 条断言全绿**。详见 §21.49。
> **上一轮（2026-10-25 批次41）**""",
 "顶部状态块")

rep(P_MAIN, "> - **2026-10-25 会话（批次41）**：创作的痛苦删火力、多段攻击合成单条命令（活力只扣一次）、100连抽同修（见 §21.48）。",
 "> - **2026-10-25 会话（批次41）**：创作的痛苦删火力、多段攻击合成单条命令（活力只扣一次）、100连抽同修（见 §21.48）。\n"
 "> - **2026-10-26 会话（批次42）**：发布完善（正式名 / 清单字段 / 版本 1.0.0 / 设置页四节 / 诊断 / 工坊预览图与发布清单）（见 §21.49）。",
 "数据来源行")

d = io.open(P_MAIN, encoding="utf-8").read()
d = re.sub(r"\| \*\*当前部署版本\*\* \|.*\|",
           "| **当前部署版本** | `STS2_Momoi.dll` **504,320 B**（**10-26 00:26**）、`STS2_Momoi.pck` **131,853,468 B**（**10-26 00:26**）、`STS2_Momoi.json` 710 B（**游戏王小桃 1.0.0**） |",
           d, count=1)
d = d.replace("28 套 / **1222** 条", "29 套 / **1265** 条")
d = d.replace("全部 28 套 / 1222 条", "全部 29 套 / 1265 条")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 部署版本 + 套件数字")

rep(P_MAIN, """| `_verify_batch41.py` | **21** | **创作痛苦删火力 + 多段合成单命令 + 全卡多命令扫描** |
| **合计** | **1222**（28 套） |""",
 """| `_verify_batch41.py` | 21 | 创作痛苦删火力 + 多段合成单命令 + 全卡多命令扫描 |
| `_verify_batch42.py` | **43** | **正式名/清单字段/版本/免纪元 + 设置页四节 + 诊断 + 工坊预览图** |
| **合计** | **1265**（29 套） |""",
 "§10 套件表")

tail = """
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

- **预览图**：`工作区\\美术成品区\\工坊预览图_512.png`（512×512 / **139 KB**，远低于 1 MB 上限）——像素小桃立绘 + 模糊粉底 + 标题「游戏王小桃」。
- **发布清单**：`工作区\\_docs\\_发布清单.md`，含工坊 tags（Characters / schinese / English）、Required Items 填 RitsuLib 工坊 ID、工坊描述草稿、更新检查清单模板（`ModUpdateCheckOptions` + manifest JSON 示例）、上线前自测清单（本地版与工坊版并存、联机同文件、旧存档、中英文本、选人界面、设置页、建筑师打斗）。

#### 6. 产物 / 验证

- `dotnet build` **0 错误** → DLL **504,320 B**、PCK **131,853,468 B**（10-26 00:26），部署清单已是「游戏王小桃 / 1.0.0」。
- 新增 `_verify_batch42.py` **43 条**（清单字段 / 版本 / 免纪元 / 四节结构 / 重置 / 诊断 / 预览图 / README 标题 / 无遥测）。
- **二十九套合计 1265 条断言全绿**。
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.49")

# 工作区文档
d = io.open(P_WS, encoding="utf-8").read()
d = re.sub(r"\| 部署 \|.*\|", "| 部署 | `STS2_Momoi.dll` **504,320 B**（10-26 00:26）、`STS2_Momoi.pck` **131,853,468 B**（10-26 00:26）、清单 **游戏王小桃 1.0.0** |", d, count=1)
d = re.sub(r"\| 自检 \|.*\|", "| 自检 | **29 套 / 1265 条断言全绿**（`_verify_batch*.py` 通配逐个跑） |", d, count=1)
d = d.replace("跑全部自检（28 套 / 1222 条断言）", "跑全部自检（29 套 / 1265 条断言）")
row = ("| 42 | 10-26 | **发布完善**：正式中文名「游戏王小桃」（清单/设置页/README，角色名不变）；清单改正式值"
       "（author alkaid616 / 双语描述 / version 1.0.0 / min_game_version 0.111.0，csproj `<Version>1.0.0</Version>`）；"
       "设置页重排 general/audio/progress/diagnostics（版本卡 + 打开日志目录 + 重置设置）；确认免纪元无 RequireEpoch；"
       "工坊预览图 512×512/139 KB + 发布清单文档（tags/依赖/更新检查/自测项）。本版不接遥测 |")
anchor = "> 批次 24~26 是**角色动画**"
if anchor in d:
    d = d.replace(anchor, row + "\n\n" + anchor, 1)
else:
    d = d.rstrip("\n") + "\n" + row + "\n"
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
