# 工作区目录说明

> 2026-10-12 整理。**只做归类移动，没有删除任何东西**；移动清单见 `../_archive/move_manifest_*.txt`。
> 权威设计表是 `STS2Momoi.xlsx`，快照 `_design_dump.txt` **由 xlsx 重建**（`_scripts/_sync_design_dump.py`），两者必须一致。

```
工作区/
├─ STS2Momoi.xlsx            ★ 权威设计表（卡牌 / 遗物 / 药水 三个 sheet，卡牌表从第 3 行起）
├─ _design_dump.txt          ★ 设计快照（= xlsx 的纯文本版，134 条；改完 xlsx 请跑 _sync_design_dump.py）
│
├─ _scripts/                 所有 Python 脚本（一次性与可复跑的都在这）
│   ├─ _sync_design_dump.py        xlsx → _design_dump.txt 整份重建（推荐每次改表后跑）
│   ├─ _update_batch*_tables.py    各批次「只改表格」的补丁脚本（含 xlsx/dump 双向同步）
│   ├─ _update_batch*_loc.py       各批次「只改本地化」的补丁脚本（zhs + eng）
│   ├─ _verify_batch9.py           卡牌文本/代码特征自检（当前 64 条断言）
│   ├─ _check_keyword_dup.py       体检：描述里手写了「会被自动追加的关键词」导致重复显示
│   ├─ _regen_art_status.py        重生成 _data/_card_art_status.{json,txt}
│   ├─ _icon_inventory.py          统计 power 图标缺口 → _data/_power_icon_inventory.json
│   ├─ _index_cards.py             导出 卡名 ↔ 类名 ↔ 文件 对照 → _data/_card_index.txt
│   ├─ _dump_loc.py / _dump_xlsx.py / _q.py   查询小工具
│   ├─ _tidy_workspace.py          本次目录整理的脚本（幂等，可重复跑）
│   └─ migrate_cards.py / _xlsx_update*.py    历史迁移脚本
│
├─ _data/                    机读快照与统计（脚本输出）
│   ├─ _card_art_status.json / .txt      逐卡卡面完成度（133/133 全部真实成品）
│   ├─ _power_icon_inventory.json        power 图标现状
│   ├─ _card_index.txt                   卡名 / 类名 / 代码文件
│   ├─ _cards_full.json / _idx_cards.json / _idx_powers.json
│   └─ _relic_potion_dump.txt / _xlsx_dump.json / _xlsx_vs_json.txt
│
├─ _docs/
│   ├─ _待做图标清单.md        42 个 power 图标 + 8 遗物 + 3 药水的待办（给美术用）
│   └─ STS2_Momoi_迁移文档.md  ★ 工作区版交接文档（现行，2026-10-16 重写；全文版在仓库根同名文件）
│
├─ _backup/                  各种改动前的备份
│   ├─ _xlsx_backup/             改动前的 STS2Momoi.xlsx（按批次命名）
│   ├─ _dump_backup/             改动前的 _design_dump.txt
│   └─ _cardart_backup9/         批次9 替换前的卡面
│
├─ _session_export/ _session_export2/   历史会话导出（时间线 / 工具调用 / 压缩摘要）
│
├─ 卡面成品区/ 卡面成品7/ 卡面成品8/     已接入/待接入的卡面
├─ 参考图集/                            画风参考
├─ 编辑区/                              正在做的图（每个卡一个目录，内含 _src/_work）
├─ 已删卡_备份/                         删卡时的源码/本地化/图/表格行备份
├─ 美术准备/                            卡面状态表等
└─ 标准卡面画布.psd  工程文件.lnk
```

## 常用操作

```bash
PY="C:\Users\asus\AppData\Local\Python\pythoncore-3.14-64\python.exe"   # 本机 python 会命中 Store 占位程序

# 改完 xlsx 后同步快照
"$PY" 工作区/_scripts/_sync_design_dump.py

# 全部 13 套自检（524 条断言）
for v in 9 11 12 13 14 15 16 17 18 19 20 21 22; do "$PY" "工作区/_scripts/_verify_batch$v.py" | tail -1; done

# 关键词重复显示体检
"$PY" 工作区/_scripts/_check_keyword_dup.py

# 卡面完成度统计
"$PY" 工作区/_scripts/_regen_art_status.py

# 卡池总览 / power 总览
"$PY" 工作区/_scripts/_index_cards.py       # 卡名 ↔ 类名 ↔ 文件
"$PY" 工作区/_scripts/_power_overview.py    # 重生成 _docs/_power总览.md
```

> **现状（2026-10-16）**：卡面 **133/133 全部成品**，power/遗物/药水图标全部成品 —— **卡面时代结束**。
> 唯一的美术缺口是**角色素材**（`images\characters\` 12 张 + 选人背景 + 商店/篝火 + 战斗差分 6 张），
> 后续重心 = **角色美术 → 卡牌调整 → 新的模组内容**。详见
> `_docs\STS2_Momoi_迁移文档.md`（工作区版，现行）与仓库根 `STS2_Momoi_迁移文档.md`（全文版）。
>
> `美术准备/` 整个目录是**生图时代的遗留**（ComfyUI 产出/脚本/状态/日志），接手不必再看；
> `_docs\_待做图标清单.md` 同理（图标已全部完成）。

> 注意：卡面接入后要 `dotnet build`（`STS2 Momoi\STS2 Momoi.csproj`）才会进 PCK 并部署到
> `D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi\`。
