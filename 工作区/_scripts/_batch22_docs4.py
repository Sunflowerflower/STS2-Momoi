# -*- coding: utf-8 -*-
"""批次22：更新 工作区/README.md（文档定位 + 自检命令 + 现状与后续重心）。"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

P = r"C:\Users\asus\RiderProjects\STS2 Momoi\工作区\README.md"
d = open(P, encoding="utf-8").read()


def rep(old, new, label):
    global d
    assert old in d, "没找到：" + label
    assert d.count(old) == 1, "多处匹配：" + label
    d = d.replace(old, new)
    print("  OK " + label)


rep("│   └─ STS2_Momoi_迁移文档.md  旧版工作区移交文档（现行版在仓库根）",
    "│   └─ STS2_Momoi_迁移文档.md  ★ 工作区版交接文档（现行，2026-10-16 重写；全文版在仓库根同名文件）",
    "文档定位")

rep('''# 卡牌文本/代码自检
"$PY" 工作区/_scripts/_verify_batch9.py''',
    '''# 全部 13 套自检（524 条断言）
for v in 9 11 12 13 14 15 16 17 18 19 20 21 22; do "$PY" "工作区/_scripts/_verify_batch$v.py" | tail -1; done''',
    "自检命令")

rep('''# 卡面完成度统计
"$PY" 工作区/_scripts/_regen_art_status.py
```''',
    '''# 卡面完成度统计
"$PY" 工作区/_scripts/_regen_art_status.py

# 卡池总览 / power 总览
"$PY" 工作区/_scripts/_index_cards.py       # 卡名 ↔ 类名 ↔ 文件
"$PY" 工作区/_scripts/_power_overview.py    # 重生成 _docs/_power总览.md
```

> **现状（2026-10-16）**：卡面 **133/133 全部成品**，power/遗物/药水图标全部成品 —— **卡面时代结束**。
> 唯一的美术缺口是**角色素材**（`images\\characters\\` 12 张 + 选人背景 + 商店/篝火 + 战斗差分 6 张），
> 后续重心 = **角色美术 → 卡牌调整 → 新的模组内容**。详见
> `_docs\\STS2_Momoi_迁移文档.md`（工作区版，现行）与仓库根 `STS2_Momoi_迁移文档.md`（全文版）。
>
> `美术准备/` 整个目录是**生图时代的遗留**（ComfyUI 产出/脚本/状态/日志），接手不必再看；
> `_docs\\_待做图标清单.md` 同理（图标已全部完成）。''',
    "现状与后续重心")

open(P, "w", encoding="utf-8").write(d)
print("工作区 README 已更新：", d.count("\n") + 1, "行")
