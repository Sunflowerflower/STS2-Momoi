# -*- coding: utf-8 -*-
"""批次22：给旧清单加作废/现行标记，并把 _美术待补清单.md 的口径更新到「只剩角色美术」。"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

DOCS = r"C:\Users\asus\RiderProjects\STS2 Momoi\工作区\_docs"

# ---------- 1. 图标清单：已全部完成，标记作废 ----------
p = DOCS + r"\_待做图标清单.md"
d = open(p, encoding="utf-8").read()
if not d.startswith("> ⛔"):
    d = ("> ⛔ **本文档已作废（2026-10-16）**：里面的 power / 遗物 / 药水图标**已全部完成并进包**\n"
         "> （批次 10 接入 48 张 power 图标 + 9 遗物 + 3 药水 + 白剪影轮廓；27 张死图标已清理）。\n"
         "> 现存图标现状看 `工作区\\_data\\_power_icon_inventory.json`；**当前唯一的美术缺口是角色素材**，\n"
         "> 见 `工作区\\_docs\\_美术待补清单.md`。本文档仅作历史留存（下面内容可能已经与代码不一致）。\n\n---\n\n") + d
    open(p, "w", encoding="utf-8").write(d)
    print("  OK _待做图标清单.md 标记作废")
else:
    print("  -- _待做图标清单.md 已标记过")

# ---------- 2. 美术待补清单：改为「只剩角色美术」的现行口径 ----------
p = DOCS + r"\_美术待补清单.md"
d = open(p, encoding="utf-8").read()
old_head = "# STS2 Momoi 美术资源总清单（批次10 之后）"
new_head = """# STS2 Momoi 美术资源总清单 —— **当前唯一缺口：角色素材**（2026-10-16 更新）

> **状态一句话**：卡面 **133/133 全部真实成品**；power **47** / 遗物 **20**（含轮廓）/ 药水 **6**（含轮廓）**全部成品**。
> **本文档下半部分列的角色相关素材是现在唯一还没做的美术**（仍是模板自带的铁甲战士占位）。
> 战斗差分（`images\\characters\\cue\\*.png`）**只要覆盖同名文件**，管线（`ModVisualCues.CueSet()`）已接好，不用改代码。
> 上游文档：仓库根 `STS2_Momoi_迁移文档.md` §5 / §6；`工作区\\_docs\\STS2_Momoi_迁移文档.md` §2.1。"""
assert old_head in d
d = d.replace(old_head, new_head, 1)
open(p, "w", encoding="utf-8").write(d)
print("  OK _美术待补清单.md 口径更新")
