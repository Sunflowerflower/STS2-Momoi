# -*- coding: utf-8 -*-
"""批次49：更新迁移文档顶部状态块 + 追加 §21.56。"""
import glob
import io
import os
import sys

BS = chr(92)
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DOC = [p for p in glob.glob(os.path.join(ROOT, "STS2_Momoi_*.md")) if os.path.basename(p) == "STS2_Momoi_迁移文档.md"][0]
SECTION = [p for p in glob.glob(os.path.join(ROOT, "工作区", "_docs", "_batch49_section.md"))][0]

NEW49 = [
    "> **本次状态（2026-11-02 批次49）**：**体积砍半 + 多人构想 bug + 角色贴图大小开关 + 能力伤害改原版形状 + 循环叙事重做，版本 1.0.5**。",
    "> 体积：pck **131,854,936 B → 57,834,244 B（-56%）**，发布 zip **131 MB → 54.2 MB**。Godot 默认导入全是**无损**（`compress/mode=0` 占 ctex 117.46 MB），"
    "所以卡面（1000×760）改 `process/size_limit=512` 保持无损、战斗帧改**有损 WebP 0.95**（帧偏扁平，VRAM 压缩反而更大）；可见像素 PSNR 42.4 dB。",
    "> ⚠ 365 个 `*.import` 被 `.gitignore` 忽略：清缓存/换机器后**必须先跑 `工作区"
    + BS + "_scripts" + BS + "_optimize_textures.py` 再导 pck**，否则体积回到 131 MB（规则见 §21.56 第 1 节）。",
    "> 多人：`DriedInspiration.AfterPlayerTurnStart` 少了 `if (player != Owner) return;` —— 队友回合开始也会被塞「构想」。",
    "> 设置新增「**角色贴图大小**」滑块（0.2~1.2，默认 **0.7**，步长 0.05）：Prefix `NCreature.ScaleTo` 只对 `Entity.IsPlayer` 乘倍率，"
    "再在 `NCombatRoom.AddCreature` Postfix 补一次 `ScaleTo(1f, 0)`（传 1 而非倍率，否则平方）。怪物不受影响。",
    "> 明日奈：减伤时长「本回合」→「**直到你的下回合开始前**」——`TickDownDuration` 从 `AfterSideTurnEnd` 挪到 `AfterSideTurnStart`。",
    "> 能力伤害：构想之矛 / 矛与盾 / 节奏游戏 / 来自大师的援护 一律改成原版能力形状 `CreatureCmd.Damage(..., ValueProp.Unpowered, ...)`"
    "（同 Panache / FlameBarrier / Juggernaut）——**不吃力量/活力/虚弱/易伤，也不播攻击动画**；援护里手工补的活力/易伤与 `FirepowerHooks.SpendVigorAsync` 一并删掉。",
    "> 数值：BA启动！普通→**罕见** + 活力 2-3→**3-4**；再启新篇 罕见→**普通**。",
    "> 循环叙事重做：1 费技能（罕见·升级 0 费）+ **注能**（与开发者协同·绿 共用 `IImbuedCard` / `ImbuedSupport`，置底 + 开局自动打出）；"
    "打出后「本回合结束时，将弃牌堆的最多 1 张牌洗入你的抽牌堆」，选择界面 `STS2_MOMOI_CYCLIC_NARRATIVE_HEADER`「选择最多{Amount}张…」，`MinSelect=0` 保证只剩 1 张也由玩家确认、可跳过。",
    "> `dotnet build` **0 错误 / 31 警告**，DLL **515,072 B** / PCK **57,834,244 B**；`工作区" + BS + "发布包" + BS + "STS2_Momoi_v1.0.5.zip` **54.2 MB**；"
    "三十五套自检 **1632 条全绿**。详见 §21.56。",
]

NOTE47 = ("> **上一轮（2026-10-31 批次47）**：飞溅 / 万花筒 / 棱彩宝石 三个「角色隔离」开关（`[ThreadStatic]` 作用域标记 + "
          "`UnlockState.get_CharacterCardPools` Postfix）+ 工坊发布素材与**首次上传成功**（条目 3830602273，`private`）；版本 1.0.4（见 §21.54）。")


def main() -> int:
    text = io.open(DOC, encoding="utf-8").read()

    anchor48 = "> **本次状态（2026-10-31 批次48）**："
    anchor47 = "> **上一轮（2026-10-31 批次47）**："
    end_marker = "> **上一轮（2026-10-28 批次46）**："

    i = text.index(anchor48)
    j = text.index(end_marker)
    block = text[i:j]
    lines = block.split("\n")
    k = next(idx for idx, ln in enumerate(lines) if ln.startswith(anchor47))
    body48 = lines[1:k]
    if not body48:
        print("[FAIL] 批次48 正文没抓到")
        return 1

    head48 = lines[0].replace("本次状态", "上一轮")
    if head48 == lines[0]:
        print("[FAIL] 批次48 标题没改成功")
        return 1

    new_block = "\n".join(NEW49 + [head48] + body48 + [NOTE47]) + "\n"
    text = text[:i] + new_block + text[j:]

    section = io.open(SECTION, encoding="utf-8").read()
    if "### 21.56" not in text:
        text = text.rstrip("\n") + "\n" + section
        print("[OK] 追加 §21.56")

    ctrl = [(n, repr(line[:40])) for n, line in enumerate(text.split("\n"), 1)
            if any(ord(c) < 32 and c not in "\t" for c in line)]
    if ctrl:
        print(f"[FAIL] 仍有控制字符：{ctrl[:5]}")
        return 1

    io.open(DOC, "w", encoding="utf-8", newline="\n").write(text)
    print(f"[OK] 写入 {os.path.basename(DOC)}：{len(text.split(chr(10)))} 行")
    print(f"[INFO] 批次48 正文 {len(body48)} 行；文件大小 {os.path.getsize(DOC)} B")
    return 0


sys.exit(main())
