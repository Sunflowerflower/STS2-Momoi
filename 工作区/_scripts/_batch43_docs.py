# -*- coding: utf-8 -*-
"""批次43 文档：§21.50 + 数字/套件表同步。"""
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


rep(P_MAIN, "> **本次状态（2026-10-26 批次42）**",
 """> **本次状态（2026-10-26 批次43）**：**先出本地发布包**（不上工坊）。设置页按反馈收尾：**隐藏页面顶部的模组简介**（`WithDescriptionHidden(true)`，等正式简介写好再开）、
> **「进度」节删掉「不需要纪元/时间线」的说明卡**（该节现在只放「重置本模组设置」，标题改成「其他」）、
> **打开日志目录**确认是跨平台的（按 `OS.GetUserDataDir()` 的 `logs` 实时解析，不写死 `%APPDATA%`；目录不存在时退回 user 目录）。
> 预览图换成用户给的 `工作区\\美术成品区\\预览图.png`（512×512 / 253 KB）。
> 新增 `工作区\\_scripts\\_make_release_zip.py`：校验 `mods\\STS2_Momoi\\` 三个文件与清单字段后，打出**顶层就是 `STS2_Momoi/`** 的本地 mod 包
> → `工作区\\发布包\\STS2_Momoi_v1.0.0.zip`（125.0 MB，含 README.txt 安装说明）。
> `dotnet build` **0 错误**，DLL **504,320 B** / PCK **131,853,468 B**；三十套自检 **1291 条断言全绿**。详见 §21.50。
> **上一轮（2026-10-26 批次42）**""",
 "顶部状态块")

rep(P_MAIN, "> - **2026-10-26 会话（批次42）**：发布完善（正式名 / 清单字段 / 版本 1.0.0 / 设置页四节 / 诊断 / 工坊预览图与发布清单）（见 §21.49）。",
 "> - **2026-10-26 会话（批次42）**：发布完善（正式名 / 清单字段 / 版本 1.0.0 / 设置页四节 / 诊断 / 工坊预览图与发布清单）（见 §21.49）。\n"
 "> - **2026-10-26 会话（批次43）**：设置页收尾（隐藏简介 / 去掉进度说明卡 / 日志目录跨平台）、换预览图、**打本地发布 zip**（见 §21.50）。",
 "数据来源行")

d = io.open(P_MAIN, encoding="utf-8").read()
d = d.replace("29 套 / **1265** 条", "30 套 / **1291** 条")
d = d.replace("全部 29 套 / 1265 条", "全部 30 套 / 1291 条")
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 套件数字")

rep(P_MAIN, """| `_verify_batch42.py` | **43** | **正式名/清单字段/版本/免纪元 + 设置页四节 + 诊断 + 工坊预览图** |
| **合计** | **1265**（29 套） |""",
 """| `_verify_batch42.py` | 43 | 正式名/清单字段/版本/免纪元 + 设置页 + 诊断 + 预览图 |
| `_verify_batch43.py` | **26** | **设置页收尾（隐藏简介/去掉说明卡）+ 预览图 + 本地发布 zip 校验** |
| **合计** | **1291**（30 套） |""",
 "§10 套件表")

tail = """
### 21.50 批次43：设置页收尾 + 换预览图 + 本地发布 zip（2026-10-26）

#### 1. 设置页三处反馈

| 反馈 | 处理 |
|---|---|
| 「进度」不要解释「本模组不需要纪元/时间线」 | 删掉那张说明卡；该节现在**只放「重置本模组设置」**，标题改成「其他」（id 仍是 `progress`，不用重装）。 |
| 「打开日志目录」在别的设备上准不准？ | **准**。路径是 `Path.Combine(OS.GetUserDataDir(), "logs")`，`OS.GetUserDataDir()` 是 Godot 按当前操作系统/账号解析的 `user://` 目录（Windows 是 `%APPDATA%\\SlayTheSpire2`，Linux/macOS 各有对应位置），**代码里不写死任何绝对路径**；目录不存在时退回 user 目录本身。副作用：界面文案里原来那句「在文件管理器里打开 %APPDATA%/SlayTheSpire2/logs」也改成了跨平台措辞，诊断信息卡里显示的是**本机解析出的真实路径**。 |
| 暂时不要出现简介 | 设置页顶部那段是 RitsuLib 自动把清单 `description` 显示出来的 → 加 `.WithDescriptionHidden(true)` 隐藏；清单里的 description 保留（模组列表 / 工坊要用），等正式简介写好把这一行删掉即可。 |

#### 2. 预览图

换成用户给的 `工作区\\美术成品区\\预览图.png`（512×512 / **253 KB**，< 1 MB 上限），我先前合成的那张已删除。
`_发布清单.md` 里的引用同步改成这张。

#### 3. 本地发布包（先不上工坊）

新增 `工作区\\_scripts\\_make_release_zip.py`，按 QA 的做法**直接把 `mods/` 下那个文件夹压缩成 zip**：

1. 校验 `mods\\STS2_Momoi\\` 里 `STS2_Momoi.dll` / `.pck` / `.json` 三个文件都在，**文件名与清单 `id` 完全一致**；
2. 校验清单 `has_dll` / `has_pck` 为 true、`dependencies` 含 `STS2-RitsuLib`；
3. 打 zip 时**顶层就是 `STS2_Momoi/`**，额外塞一份 `README.txt`（安装说明 + 本地版/工坊版 id 抢占提醒 + 联机同文件提醒）到压缩包里（不进部署目录）。

产物：**`工作区\\发布包\\STS2_Momoi_v1.0.0.zip`（125.0 MB）**

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
"""
d = io.open(P_MAIN, encoding="utf-8").read().rstrip("\n") + "\n" + tail
io.open(P_MAIN, "w", encoding="utf-8").write(d)
print("  OK 追加 §21.50")

# 工作区文档
d = io.open(P_WS, encoding="utf-8").read()
d = re.sub(r"\| 自检 \|.*\|", "| 自检 | **30 套 / 1291 条断言全绿**（`_verify_batch*.py` 通配逐个跑） |", d, count=1)
d = d.replace("跑全部自检（29 套 / 1265 条断言）", "跑全部自检（30 套 / 1291 条断言）")
row = ("| 43 | 10-26 | 设置页收尾：隐藏模组简介（`WithDescriptionHidden`）、删掉「进度」里的纪元说明卡（该节只剩重置设置，标题「其他」）、"
       "日志目录确认按 `OS.GetUserDataDir()` 跨平台解析；预览图改用用户给的 `预览图.png`；"
       "**打出本地发布包** `工作区\\发布包\\STS2_Momoi_v1.0.0.zip`（顶层 `STS2_Momoi/`，含 README.txt），脚本 `_make_release_zip.py` |")
anchor = "> 批次 24~26 是**角色动画**"
if anchor in d:
    d = d.replace(anchor, row + "\n\n" + anchor, 1)
else:
    d = d.rstrip("\n") + "\n" + row + "\n"
io.open(P_WS, "w", encoding="utf-8").write(d)
print("  OK 工作区文档")
