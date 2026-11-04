# -*- coding: utf-8 -*-
"""批次22 文档更新：
1) 根文档 STS2_Momoi_迁移文档.md —— 半角标题、§0/§5/§6 重写、§7.4 折叠、§11 时间线压缩、§13 索引清理、追加 §21.25 与 §22
2) 工作区\_docs\STS2_Momoi_迁移文档.md —— 重写成现行自包含版（删掉 08-23 的生图内容）
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
P_MAIN = os.path.join(ROOT, "STS2_Momoi_迁移文档.md")
P_WS = os.path.join(ROOT, "工作区", "_docs", "STS2_Momoi_迁移文档.md")


def rep(src, old, new, label):
    assert old in src, "没找到：" + label
    assert src.count(old) == 1, "有多处匹配：" + label
    print("  ✓ " + label)
    return src.replace(old, new)


def cut(src, start, end, new, label):
    i = src.find(start)
    assert i >= 0, "没找到起点：" + label
    j = src.find(end, i)
    assert j > i, "没找到终点：" + label
    print("  ✓ %s（原 %d 字符 → %d）" % (label, j - i, len(new)))
    return src[:i] + new + src[j:]


doc = open(P_MAIN, encoding="utf-8").read()
print("== 根文档 ==")

# ---------- 1. 标题 ----------
doc = rep(doc, "# STS2_Momoi 角色 Mod —— 迁移交接文档（2026-10-04 版）",
          "# STS2_Momoi 角色 Mod —— 迁移交接文档（2026-10-16 版）", "标题日期")

# ---------- 2. 顶部状态块 ----------
doc = rep(doc, "> **本次状态（2026-10-15 批次21）**",
          """> **本次状态（2026-10-16 批次22）**：**卡面时代正式结束** —— 卡面 **133/133 全部真实成品**，power 47 / 遗物 / 药水图标全部成品；本文档已把所有「还要生图」的旧章节（ComfyUI 配方、火蛇怒咬/油腻打击/毁灭与新生专项、美术管线坑）**折叠成一段历史小结**（§5.2），后续重心改为 **角色美术 + 卡牌调整 + 新模组内容**（§6 / §22）。本批代码改动：**曳光弹升级后灼烧终于会变 4**（真因是 `IndependentCalculatedVar` 继承了 `DynamicVar.Clone()` 的浅拷贝 —— 克隆体里持有的还是规范化实例，而 `UpgradeValueBy` 升的是卡自己那份；改成按名字实时解析）、**破势重做**（2 费不变、16/20 伤害、`活力在这张牌上发挥 4/5 倍效果` 由新补丁 `VigorMultiplierPatch` 乘在 `VigorPower.ModifyDamageAdditive` 的返回值上）、**整活**卡面补「升级过的」、**吃豆人**的「没有诅咒」改为查抽牌堆+手牌+弃牌堆（并把抽/弃牌堆里的诅咒拉出来消耗）、**堕落**改罕见且同时给 1 层虚弱、**独特点子**改普通、**专注** 1→0 费、**博览群游** 0→1 费。`dotnet build` **0 错误**，DLL **442,880 B** / PCK **75,402,024 B**；十三套自检 **524 条断言全绿**。详见 §21.25。
> **上一轮（2026-10-15 批次21）**""", "顶部状态块")

# ---------- 3. §0 重写 ----------
sec0 = """## 0. 30 秒接手指南

### 0.1 这个项目现在是什么状态
> **代码侧**：134 张卡 + 54 个 power + 9 遗物 + 3 药水，全部实现完毕并部署（DLL **442,880 B** / PCK **75,402,024 B**，2026-10-16，0 错误 0 警告）。
> **美术侧**：**卡面 / power / 遗物 / 药水 100% 完成**（卡面 133/133 真实成品）；**唯一缺口 = 角色素材**（头像 / 选人图 / 地图标记 / 能量球 / 选人背景 / 商店 / 篝火 / 战斗差分 / 多人手臂 / 转场 / 音频），现在仍是模板自带的铁甲战士占位。
> **后续重心**：**角色美术 → 卡牌调整 → 新的模组内容**（§6、§22）。

### 0.2 接手后应该立刻做的事（优先级从上到下）
1. **角色美术（最大且唯一的缺口）**：逐项清单见 **`工作区\\_docs\\_美术待补清单.md`**（RitsuLib `CharacterAssetProfile` 的 42 个字段 + 每个文件现在的样子）。战斗差分只要**覆盖同名文件**即可，管线（`VisualCueSet`）已接好，不用改代码。
2. **卡牌调整**：一律等用户逐条点名；改完跑 `_verify_batch9~22`（13 套 / 524 条断言）+ `dotnet build`（§2、§10）。
3. **新模组内容（卡/遗物/药水/power）**：先改权威表 `工作区\\STS2Momoi.xlsx`，再同步四处（§7.2）。
4. **别再看旧美术产出**：`工作区\\美术准备\\产出\\`、`美术准备\\脚本\\`、ComfyUI 的 input/output 全是生图时代的遗留，接手不需要它们（§5.2）。
5. **已完成项不要重做**：卡面成品区 / 成品 4~8 / 批次 10 的三批图标均已进包。

### 0.3 30 秒上手命令
```bash
PY="C:\\Users\\asus\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe"   # 系统 python 会命中 Store 占位程序
cd "C:\\Users\\asus\\RiderProjects\\STS2 Momoi"
"$PY" 工作区/_scripts/_verify_batch22.py          # 跑自检（9/11/12/…/22 共 13 套）
cd "STS2 Momoi" && dotnet build "STS2 Momoi.csproj"   # 构建（自动导出 PCK + 部署；游戏必须先关）
```

---

"""
doc = cut(doc, "## 0. 30 秒接手指南", "## 1. 项目概况", sec0, "§0 重写")

# ---------- 4. §1 表格：部署版本 + 去掉 ComfyUI 行 ----------
i = doc.find("| **当前部署版本** |")
j = doc.find("\n", i)
doc = doc[:i] + ("| **当前部署版本** | `STS2_Momoi.dll` **442,880 B**（**10-16 16:01**）、"
                 "`STS2_Momoi.pck` **75,402,024 B**（**10-16 16:02**）、`STS2_Momoi.json` 409 B |") + doc[j:]
print("  ✓ §1 部署版本行")

doc = rep(doc, """| ComfyUI | `D:\\ComfyUI-aki-v3.2\\ComfyUI-aki-v3.2.7z\\ComfyUI-aki-v3.2\\ComfyUI`，API `127.0.0.1:8188` |
| ComfyUI 输入/输出 | 输入 `ComfyUI\\input\\momoi_ref\\`（**文件名必须 ASCII**）；输出 `ComfyUI\\output\\`，脚本会自动拷回 `产出\\` |
| 机器 | Windows / RTX 4060 Laptop 8 GB / 32 GB RAM / aki python 3.13.11 + torch 2.13.0+cu130 / 系统 python 3.14 |""",
          """| 美术处理 | **程序化**（`numpy` / `opencv` / `Pillow` 脚本，在 `工作区\\_scripts\\` 与 `工作区\\编辑区\\<卡名>\\_src\\`）；**生图时代的 ComfyUI 已弃用**（§5.2） |
| 美术待补清单 | `工作区\\_docs\\_美术待补清单.md`（角色素材 42 个字段逐项） |
| 自检 | `工作区\\_scripts\\_verify_batch{9,11..22}.py`（13 套 / 524 条断言） |
| 机器 | Windows / RTX 4060 Laptop 8 GB / 32 GB RAM / 系统 python 3.14（`C:\\Users\\asus\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe`） |""",
          "§1 表格：生图行 → 程序化行")

# ---------- 5. §5 折叠 ----------
sec5 = """## 5. 美术现状（**卡面已 100% 完成**）

### 5.1 现状（实测 2026-10-16）

| 类别 | 文件数 | 状态 |
|---|---|---|
| 卡面 `images\\cards\\*.png` | 133 | ✅ **133/133 全部真实成品**（0 张共用占位、0 张纯色占位） |
| power 图标 `images\\powers\\*.png` | 47 | ✅ 全部成品（批次 10 接入 48 张：含 4 张拆分 + 1 张改名） |
| 遗物图标 `images\\relics\\*.png` | 20 | ✅ 成品 + 白剪影轮廓（`*_outline.png` 本来就是小白图，体积 <6 KB 属正常） |
| 药水图标 `images\\potions\\*.png` | 6 | ✅ 同上 |
| **角色素材 `images\\characters\\`** | 12 | ❌ **仍是模板自带的铁甲战士占位** ← **当前唯一的美术缺口** |
| 战斗视觉 `images\\characters\\cue\\` | 6 | ⚠️ 管线已接好（`VisualCueSet`），图是线稿占位，**覆盖同名文件即可** |

逐项清单（尺寸 / 用途 / 现在长什么样）：**`工作区\\_docs\\_美术待补清单.md`**。

### 5.2 生图时代的历史小结（**已弃用，不必再看**）

卡面阶段用过 **ComfyUI**（`D:\\ComfyUI-aki-v3.2\\…`，API `127.0.0.1:8188`）+ 两阶段管线
（`_pipeline.wf_base` → `qa`，`er_sde`/`simple`，1536×1152 → 交付 1000×760，模型/LoRA 选型 + WD14 身份判定），
以及单卡精修（火蛇怒咬 masked redraw + 材质替换、油腻打击、毁灭与新生 长臂分层/alpha bleed）。

**这套东西已随卡面收官一并退役**：配方、专项调参、踩坑（原 §5.2 / §5.4 / §5.5 / §5.6 / §7.4）都不再维护。
保留结论只有三条：
1. 生图产物一律**不可直接当成品**，必须逐张读图对照要求（这条现在等价于「程序化产出也要逐张核对」）。
2. 白底抠图边缘发灰要用 **alpha bleed / color bleed**（RGB 渗出、alpha 不动）。
3. 需要刚性平移局部肢体时用**分层**做法（保护场归零 + 图层叠最上），别硬拉整图。

后来所有美术工作（成品 4~8、power/遗物/药水图标、白剪影轮廓、编辑区重绘）都改成 **程序化处理**
（`numpy` / `opencv` / `Pillow`），产物按批留在 `工作区\\美术成品区\\`（`卡面成品区` / `卡面修改1` / `药水成品区` / `遗物成品区`）
与 `工作区\\编辑区\\`（每个条目一个目录，内含 `_src` 脚本与 `_work` 中间产物）。

> 旧产出目录（`工作区\\美术准备\\产出\\`、`美术准备\\脚本\\`、`美术准备\\状态\\`、`美术准备\\日志\\`、ComfyUI `input`/`output`）
> 仅作历史留存，接手时不必再看。

---

"""
doc = cut(doc, "## 5. 美术管线（ComfyUI）", "## 6. 未完成工作清单", sec5, "§5 折叠为现状 + 历史小结")

# ---------- 6. §6 重写 ----------
sec6 = """## 6. 后续工作清单（**重心 = 角色美术 + 卡牌调整 + 新模组内容**）

### 6.1 角色美术（当前最大缺口）
- [ ] `images\\characters\\` 12 张全部替换（现在是铁甲战士占位）：`STS2_Momoi_character_icon.png`（88×88）、`_icon_outline.png`、`STS2_Momoi_character_select.png`（132×195）、`_select_locked.png`、`STS2_Momoi_map_marker.png`（49×64）、`STS2_Momoi_energy_orb_layer_1..5.png`、`energy_big.png`、`energy_text.png`。
- [ ] `scenes\\characters\\STS2_Momoi_character_select_bg.tscn`（选人背景，现在是深蓝底 + 上面那两张铁甲战士图）。
- [ ] `STS2_Momoi_merchant.tscn` / `STS2_Momoi_rest_site.tscn`（商店 / 篝火，现在直接复用那张 132×195 面罩图）。
- [ ] **战斗差分 6 张**：`images\\characters\\cue\\{idle,attack,cast,hit,dead,relaxed}.png`（600×820）。
      管线已接好（`VisualCues: ModVisualCues.CueSet()…Build()` + `scenes\\characters\\STS2_Momoi_character.tscn`），
      **只覆盖同名文件即可，不用改代码**；说明见 `images\\characters\\cue\\README.md`。
- [ ] 多人模式手臂 ×4、场景转场、音频（逐项见 `_美术待补清单.md`）。

### 6.2 卡牌调整
- 入口 = **用户逐条点名**；不要自己开新战场、不要顺手美化（§7.1）。
- 每次改完：改本地化 → `dotnet build` → 跑 `_verify_batch9~22`（13 套 / 524 条断言）。
- 数值改动的**正确姿势**：卡面上出现的数字用 `BlockVar` / `DamageVar` / `CardsVar` / `IndependentCalculatedVar`；
  不要用普通 `DynamicVar`（会 `InvalidCastException`，且不随升级重算）。

### 6.3 新的模组内容
- 新卡 / 遗物 / 药水 / power：先改权威表 `工作区\\STS2Momoi.xlsx`（+ `_sync_design_dump.py`），再同步本地化四处（§7.2）。
- 新机制优先走 `Patches\\*.cs`；**每个补丁都要登记进 `Entry.cs`**，否则静默不生效（§7.3）。

### 6.4 代码侧遗留（低优先级 / 待玩家复测）
- 08-23 版列的待复测项，此后多轮重构已覆盖大部分，但**没有一条被明确标记「已复测通过」**。遇玩家反馈优先怀疑：
  秒人斧战斗结束移除时机（复制品）、绝地求生的能量公式（=max(0,3-手牌数)，用户未确认）、黄金矿工的「10X 金币」（现按 10/12 固定）、
  跑酷升级版「本场战斗免费」（现简化为本回合免费）、得道多助支援牌池 14 种（不含「来自优香的关爱」）、
  多人卡（义愤填膺 / 抽鬼牌 / 玩玩这款）**单机未测**。
- 09-21 的「19 项批」代码层核验通过 43/46，3 条为误报（破势自身 Stun、FeedingFrenzy 由吃豆人/PvZ 合法使用、构想遗留死代码已清理）。
- 批次 16 的全量代码审核结论见 `工作区\\_docs\\_代码审核_批次16.md`。

---

"""
doc = cut(doc, "## 6. 未完成工作清单", "## 7. 注意事项与踩坑（**最值钱的部分**）", sec6, "§6 重写")

# ---------- 7. §7.4 折叠 ----------
sec74 = """### 7.4 美术管线坑（**已随生图管线退役，仅留结论**）
- 生图/程序化产出一律**逐张读图对照要求**，不要「差不多就交」。
- 白底抠图边缘发灰 → **alpha bleed / color bleed**（RGB 渗出、alpha 不动）。
- 需要刚性平移局部肢体 → **分层**（保护场归零 + 图层叠最上），别硬拉整图。
- 其余（ComfyUI LoadImage 节点细节、denoise/调度器试错、mask 尺寸对齐等）全部作废，不再记录。

"""
doc = cut(doc, "### 7.4 美术管线坑", "### 7.5 会话与工具坑", sec74, "§7.4 折叠")

# ---------- 8. §11 时间线：压缩生图期 ----------
old_rows_start = "| 08-27~31 | 文本规范化大扫除；草莓牛奶重做；游戏王形态重做；开始美术；\"开工前最后一轮改动\" |"
i = doc.find(old_rows_start)
assert i >= 0
j = doc.find("| **2026-10-02** |", i)
assert j > i
doc = doc[:i] + """| 08-27~31 | 文本规范化大扫除；草莓牛奶重做；游戏王形态重做；开始美术；"开工前最后一轮改动" |
| 09-04~09-28 | **生图时代（已结束）**：ComfyUI 环境搭建 → 模型/LoRA 选型与 WD14 身份判定 → 批量第 1/2/3 轮 → 已拼卡面 41 张接入 → 成品区 30 张接入；期间有**单卡精修**（火蛇怒咬 masked redraw + 材质替换、油腻打击 v3~v9、毁灭与新生 长臂分层 + alpha bleed）。细节（§5.2/§5.4/§5.5/§5.6/§7.4 旧文）已按用户要求**折叠删除**；产物留在 `工作区\\美术准备\\产出\\`。 |
| 09-19~21 | 嘲讽/双刀王小桃/梗卡重做；心流重做；85 卡总览；A/B1/B2/C 未定稿清单 |
| 09-23 | 六项任务批 → xlsx 同步 → **构建部署（PCK 46,151,992，0 错误）**；美术准备目录整理 |
| 09-24~26 | 单卡精修收尾（火蛇怒咬旧批次**全部作废清空**）；文件夹规则改"一张卡一个文件夹" |
""" + doc[j:]
print("  ✓ §11 时间线：生图期压缩为 2 行")

# ---------- 9. §13 资料索引：清理生图行 ----------
doc = rep(doc, '| 任务/映射 json | `脚本\\jobs*.json`、`_cards_todo.json`、`_todo.json`、`_成品区映射.json`、`_预览中文名映射.json`、`状态\\*.json` |\n| 生成脚本 | `脚本\\_pipeline.py`（wf_base / wf_hires / wf_inpaint / wf_detail / **wf_mredraw** / wf_chain / qa）、`_prompts_all.py`、`_prompts_r3.py`（mask / 抠图 / 合成背景等小工具按需重写，都不会超过几十行） |\n| 卡面接入与统计 | 接入脚本 `脚本\\_apply_batch3~7.py`、**`脚本\\_apply_batch8.py`（成品7 全量 9 张 + 删卡 + 新能力图标）**；统计脚本 `脚本\\_art_status_report.py`；备份 `备份\\成品3/4/5/6/7替换备份\\`（另含 `成品7全量替换备份`）、`备份\\已删卡备份\\`、**`工作区\\已删卡_备份\\`（轮回 / 金色传说 / 趁热打铁，含源码/本地化/图/表格行）**；报告 `工作区\\_data\\_card_art_status.txt` / `.json`、`_archive\x08atch_reports\\_apply_batch3~8_report.json`、`_archive\x08atch_reports\\_batch3~8_contact_sheet.jpg`（`_batch8_contact_sheet.jpg` = 成品7 的 9 张，已逐张核对） |',
          """| 卡面接入与统计 | 接入脚本 `工作区\_scripts\_apply_batch10_art.py`、`_cleanup_dead.py`、`_batch10b~10d.py`；统计脚本 `工作区\_scripts\_regen_art_status.py`；备份 `工作区\_backup\batch1*_pre\`、`工作区\已删卡_备份\`（轮回 / 金色传说 / 趁热打铁 / 天意侵蚀，含源码/本地化/图/表格行）；报告 `工作区\_data\_card_art_status.txt` / `.json` |
| （已弃用）生图时代脚本 | `工作区\美术准备\脚本\`（ComfyUI 管线 / 提示词 / 单卡精修脚本）—— 仅作历史留存，接手不必再看（§5.2） |""",
          "§13 资料索引：生图行 → 程序化行 + 弃用说明")

# ---------- 10. 追加 §21.25 与 §22 ----------
tail = """

### 21.25 批次22：曳光弹升级灼烧的真因、破势重做、五处文本/数值（2026-10-16）

#### 1. 🔴 曳光弹升级后灼烧不涨（3 → 4）—— `DynamicVar.Clone()` 是浅拷贝

`IndependentCalculatedVar` 记着构造时的 `burnBase` / `burnExtra` 两个实例。问题在于
`DynamicVarSet.Clone()`（每次进战斗、每次降级都会跑）是 `Values.Select(v => v.Clone())`，
而 `DynamicVar.Clone()` 只是 `MemberwiseClone()` + `ResetToBase()` ——
于是克隆出来的 `IndependentCalculatedVar` 里 `_base`/`_extra` **仍然指向规范化实例**，
而 `DynamicVars["BurnBase"].UpgradeValueBy(1)` 升的是**这张卡自己那份克隆**。
结果：升级后卡面与结算读的都是没被升级的原实例，永远显示 3。

**修法**（`Cards\\DynamicVarSupport.cs`）：只记名字，运行时按名字从持有者的 `DynamicVars` 里取，取不到才退回构造时那个实例。

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
| 活力收益 | 每点活力最终伤害 +10%（升级 +20%），走 `ModifyDamageMultiplicative` | **「活力在这张牌上发挥 4 倍（升级 5 倍）的效果」**，走新补丁 `Patches\\VigorMultiplierPatch.cs` |

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

> 侧栏是**自动**的：`Patches\\MinigameSidebarPatch.cs` 按描述原文扫描关键词，
> 「活力」→ `FromPower<VigorPower>()`、「虚弱」→ `FromPower<WeakPower>()`，所以破势/堕落**不用手写 HoverTip**。

#### 4. 产物

- `dotnet build` **0 错误** → DLL **442,880 B**、PCK **75,402,024 B**（10-16 16:02）。
- `_verify_batch22.py` **43 条全绿**；十三套合计 **524 条断言全绿**。

---

## 22. 后续路线图（2026-10-16 起）

| 优先级 | 方向 | 入口 |
|---|---|---|
| ★★★ | **角色美术**：`images\\characters\\` 12 张 + 选人背景 + 商店/篝火 + 战斗差分 6 张 + 多人手臂/转场/音频 | `工作区\\_docs\\_美术待补清单.md`；差分只要覆盖同名文件 |
| ★★ | **卡牌调整**：用户点名的数值/文本/机制微调 | 本地化四处同步 + `_verify_batch*` + `dotnet build` |
| ★ | **新模组内容**：新卡 / 遗物 / 药水 / power / 新机制 | `工作区\\STS2Momoi.xlsx`（权威）→ 本地化 → 代码 → 表格 |
| ★ | **可选的体验补齐**：卡面右下角计数语义、侧栏关键词、局内提示的进一步打磨 | `DisplayAmount` / `MinigameSidebarPatch` |

**协作红线（不会变）**：用户点名的才动手；文本逐字照抄；不手写会被自动追加的关键词徽章；报告要短。
"""
doc = doc.rstrip("\n") + "\n" + tail
print("  ✓ 追加 §21.25 + §22")

open(P_MAIN, "w", encoding="utf-8").write(doc)
print("根文档已写回：", doc.count("\n") + 1, "行")
