# -*- coding: utf-8 -*-
"""批次22 文档更新（第三段）：§3.4 资产盘点数字、§14 清空记录折叠。"""
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


old34 = """| `images\\cards\\` | **133 PNG** | 与代码中 133 个卡类一一对应（2026-10-08：卡池数量不变，仅改名/换图） |
| `images\\powers\\` | 71 PNG | 其中 **60 张共用同一张占位图（21,515 B）**、4 张共用另一张（32,789 B）→ **63/71 待替换** |
| `images\\relics\\` | 9 PNG | **8 张是 191~192 B 占位**（仅 `DriedInspiration.png` 是真图 41 KB） |
| `images\\potions\\` | 3 PNG | **3 张全是 159~160 B 占位** |
| `images\\characters\\` | 12 PNG | 角色选择/图标/能量球图层/地图标记（多为拼凑素材） |"""

new34 = """| `images\\cards\\` | **133 PNG** | ✅ 与 133 个卡类一一对应，**133/133 真实成品**（2026-10-16 实测） |
| `images\\powers\\` | **47 PNG** | ✅ 全部成品（批次 10 替换 48 张：含 4 张拆分 + 1 张改名；死图标已清 27 张） |
| `images\\relics\\` | **20 PNG** | ✅ 9 个遗物的成品图 + 白剪影轮廓（`*_outline.png` 本来就是小白图，体积小属正常） |
| `images\\potions\\` | **6 PNG** | ✅ 3 个药水的成品图 + 轮廓 |
| `images\\characters\\` | 12 PNG | ❌ **仍是模板自带的铁甲战士占位** ← 当前唯一缺口（§5.1、§6.1） |
| `images\\characters\\cue\\` | 6 PNG | ⚠️ 战斗差分（600×820）线稿占位；管线已接好，覆盖同名文件即可 |"""

rep(old34, new34, "§3.4 资产盘点数字")

# §14 折叠成一段历史说明
i = d.find("## 14. 清空记录")
j = d.find("## 15. 2026-10-02 卡面成品3 接入记录")
assert i > 0 and j > i
new14 = """## 14. 生图时代痕迹的清理记录（**已折叠，仅留一句话结论**）

生图时代结束后，为「重新开始」做过一次彻底清理，事实如下（细节不必再看）：

- **2026-09-26**：按用户指令把某张单卡的生成历史与要求/自查文档在**文档层面**作废清空（本文档原 §5.4 旧内容、§11.1~§11.5 已删）。
- **同日追加**：按「A~G 全删，一点不留」**物理删除**该卡的全部生成痕迹——
  产出目录 1.1 GB / 1432 文件、ComfyUI `input\\momoi_ref\\` 68 个、ComfyUI `output\\` 340 个、
  参考图库 54 MB、专用脚本 147 个 py、日志 73 个。
- **保留且不删的**：通用管线脚本（`工作区\\美术准备\\脚本\\_pipeline.py` 等，现已弃用）、其余卡的一切产物、用户自己的工程文件（`.psd`）。
- **游戏侧从未有过残留**：该卡的 `images\\cards\\<类名>.png` 一直是当时的共用占位图，后来于 2026-10-02 被成品覆盖（§15）。

> **该卡的名称与图片在本文档里不再展开**；它现在只是一张普通的已完成卡面卡（成品见 `工作区\\美术成品区\\卡面成品区\\`）。

---

"""
print("  OK §14 折叠（原 %d 字符 → %d）" % (j - i, len(new14)))
d = d[:i] + new14 + d[j:]

open(P, "w", encoding="utf-8").write(d)
print("根文档已更新：", d.count("\n") + 1, "行")
