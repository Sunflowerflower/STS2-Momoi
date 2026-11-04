# -*- coding: utf-8 -*-
"""批次22 文档更新（第二段）：数据来源行 + §10 测试与验证。"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

P = r"C:\Users\asus\RiderProjects\STS2 Momoi\STS2_Momoi_迁移文档.md"
d = open(P, encoding="utf-8").read()


def rep(old, new, label):
    global d
    assert old in d, "没找到：" + label
    assert d.count(old) == 1, "多处匹配：" + label
    d = d.replace(old, new)
    print("  OK " + label)


old_src = (r"> - **2026-10-04 会话**：删除天意侵蚀 / 新增「绷住」链 4 张卡 / `工作区\卡面成品4` 全量接入 / "
           r"xlsx + 设计 dump 同步 / 重新统计（见 §16）。")
new_src = old_src + "\n" + (
    r"> - **2026-10-11 → 10-16（批次 9~22）**：文本大改 + 卡面成品8 → 批次10 美术全量接入"
    r"（power/遗物/药水图标 + 战斗模型管线 + 废案清理）→ 批次 11~19 文本/机制/颜色规范 → "
    r"**批次 20~22 卡牌调整**（阿比舒、勇者加护、消消乐、曳光弹、破势、吃豆人、堕落、独特点子、专注、博览群游），"
    r"逐条见 §21。")
rep(old_src, new_src, "数据来源行")

old10 = """## 10. 测试与验证
- 游戏内控制台：`card STS2_MOMOI_CARD_XXX` 加卡、`power XXX` 加能力；卡 ID 用类名 SNAKE_CASE 大写。
- 日志：`%APPDATA%\\SlayTheSpire2\\devmode-reports\\devmode-report-<时间戳>\\godot.log`（先 grep `Exception|Error|STS2_Momoi`）。
- 每次改完：`dotnet build`（0 错误 + PCK 体积变化）→ 进游戏控制台验卡 → 让用户复测。
- **美术侧自查循环**：生成 → `_pipeline.qa()` 自动评分排序 → 自己 read 排序图/放大图逐条对照片卡要求 → 不合格重跑。"""

new10 = """## 10. 测试与验证

### 10.1 自检套件（**改完必跑**）
```bash
PY="C:\\Users\\asus\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe"
cd "C:\\Users\\asus\\RiderProjects\\STS2 Momoi"
for v in 9 11 12 13 14 15 16 17 18 19 20 21 22; do "$PY" "工作区/_scripts/_verify_batch$v.py" | tail -1; done
```

| 套件 | 断言数 | 管什么 |
|---|---|---|
| `_verify_batch9.py` | 64 | 卡牌文本 / 代码特征（匹配前会剥掉 `[gold]` 等标签） |
| `_verify_batch11~19.py` | 102 / 52 / 32 / 42 / 50 / 27 / 28 / 26 / 13 | 遗物药水文本 → power 文本 → 机制 → 数值语义 → 颜色规范 |
| `_verify_batch20~22.py` | 28 / 17 / 43 | 阿比舒（4 倍倍率 + 3 段）、曳光弹与费用、批次 22 全项 + 标签闭合 |
| **合计** | **524** | 任一失败都要先查清是脚本过期还是代码回归，再继续 |

### 10.2 其它验证手段
- 游戏内控制台：`card STS2_MOMOI_CARD_XXX` 加卡、`power XXX` 加能力；卡 ID = 类名 SNAKE_CASE 大写。
- 日志：`%APPDATA%\\SlayTheSpire2\\devmode-reports\\devmode-report-<时间戳>\\godot.log`（先 grep `Exception|Error|STS2_Momoi`）。
  **实战数据可解包 `combat-stats.json` 核对** —— 批次 21 就是靠它查到「阿比舒只打 2 段」的（每次打出只 2 条 `DamageDealt`）。
- 每次改完：`dotnet build`（0 错误 + PCK 体积变化）→ 进游戏控制台验卡 → 让用户复测。
- 美术侧：程序化产出一律**逐张 read 对照**（批次 15 的格挡预览错配、批次 22 的 `IndependentCalculatedVar` 浅拷贝都是逐张核对发现的）。"""

rep(old10, new10, "§10 测试与验证")

open(P, "w", encoding="utf-8").write(d)
print("根文档已更新：", d.count("\n") + 1, "行")
