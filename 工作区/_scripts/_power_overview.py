# -*- coding: utf-8 -*-
"""生成 power 总览文档：工作区/_docs/_power总览.md

自动从 C# 源码抽 StackType / InstanceType / DisplayAmount / 可见性，
再叠加人工撰写的“叠加语义”说明（这部分代码里读不出来，是按设计意图写的）。
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
OUT = os.path.join(ROOT, "工作区", "_docs", "_power总览.md")

# 类名 -> （叠加语义说明, 备注）
SEMANTICS = {
    "EngineeringDeptAidPower": ("不叠加", "纯记录，**不显示**"),
    "VeritasTrackerPower": ("不叠加", "纯记录，**不显示**"),
    "CnCTrackerPower": ("不叠加", "纯记录，**不显示**"),
    "AsunaGuardPower": ("叠加：层数 = 剩余回合数；减伤百分比不叠加，取当前持有的最高档（升级 40% 覆盖 25%，反之不覆盖）",
                        "剩余回合数"),
    "YoshimiRepeatPower": ("不叠加（每次打出都是独立实例，各算各的剩余回合）", "该实例剩余回合数"),
    "ConceptSpearPower": ("叠加：层数累加到「每点构想伤害」上", "对所有敌人造成的伤害"),
    "ConceptShieldPower": ("叠加：层数累加到「每张构想格挡」上", "实际获得的格挡"),
    "SpearShieldPower": ("叠加：层数累加到格挡与伤害上", "叠加层数"),
    "FlameAttachPower": ("叠加：层数累加到「附带灼烧层数」上", "被击中敌人拿到的灼烧层数"),
    "RhythmGamePower": ("叠加：层数累加到伤害上（每张独立数值相加）", "叠加层数"),
    "TetrisFullHandPower": ("一张方块最多对应一个 buff：同档位互相覆盖，**升级版额外覆盖非升级版**",
                            "**不显示数字**（层数恒为 1）"),
    "CyclicNarrativePower": ("叠加：层数 = 剩余持续回合数", "剩余持续回合数"),
    "FellToSecondTierPower": ("不叠加（每个实例独立）", "这次实际获得的金币数"),
    "RankUpPower": ("不叠加（每个实例独立；层数 = 剩余可维持回合数，初始 2）", "剩余回合数"),
    "FocusPower": ("叠加：层数累加构想数值增量；保留张数只看构想数值（多张取最大）", "叠加层数"),
    "GameKingFormPower": ("叠加：层数累加每张牌首次打出获得的缓冲层数（升级 ×2）", "实际获得的缓冲数"),
    "DarkPsychologyPower": ("叠加：层数 = 触发次数", "剩余次数"),
    "PlantForeshadowPower": ("叠加：层数 = 剩余触发次数", "剩余次数"),
    "WatchOutPower": ("叠加：层数 = 剩余触发次数", "剩余次数"),
    "MaidWeaponPower": ("叠加：层数 = 剩余触发次数", "剩余次数"),
    "MaidWeaponUpgradedPower": ("叠加：层数 = 剩余触发次数", "剩余次数"),
    "YuzuEscortPower": ("叠加：层数 = 每回合额外打出的小游戏牌张数", "叠加层数"),
    "DualBladeMomoiPower": ("叠加：层数 = 每次触发添加的小刀张数（两者同一个数）", "每次添加的小刀张数"),
    "DualBladeMomoiUpgradedPower": ("叠加：层数 = 每次触发添加的小刀+张数（两者同一个数）", "每次添加的小刀+张数"),
    "DevGreenPower": ("叠加：层数 = 回合开始时获得的活力（两者同一个数）", "回合开始时获得的活力"),
    "DevSecretsPower": ("叠加：层数 = 被叠加次数；实际增量 = 层数×（普通 1 / 升级 2）", "实际数值增量（Gain）"),
    "LearnByDoingPower": ("叠加：层数 = 被叠加次数；实际增量 = 层数×（普通 1 / 升级 2）", "叠加层数（增量）"),
    "BurnPower": ("叠加：层数 = 灼烧伤害", "灼烧层数"),
    "BurnTurnsPower": ("不叠加（与灼烧同生共死）", "灼烧剩余回合数"),
    "FirepowerPower": ("叠加：层数 = 可拦截的活力消耗次数", "火力层数"),
    "NoProblemPower": ("叠加：层数 = 卡牌耗能增加量", "能量图标"),
    "PostQuestPower": ("不叠加（每次打出都是独立实例）", "**不显示数字**"),
    "CreativeTastePower": ("叠加：层数 = 每回合加入手牌的牌数", "叠加层数"),
    "CreativeTasteUpgradedPower": ("叠加：层数 = 每回合加入手牌的升级牌数", "叠加层数"),
    "RolePlayPower": ("不叠加（每次打出都是独立实例）", "**不显示数字**"),
    "InspirationPower": ("叠加：层数 = 触发时加入手牌的牌数", "叠加层数"),
    "InspirationUpgradedPower": ("叠加：层数 = 触发时加入手牌的牌数", "叠加层数"),
    "HelpFromManyPower": ("叠加：层数 = 每回合洗入的支援牌数", "叠加层数"),
    "HelpFromManyUpgradedPower": ("叠加：层数 = 每回合洗入的升级支援牌数", "叠加层数"),
    "RallyAgainPower": ("不叠加（每张重整旗鼓独立存在，打出构想依次触发）", "当前即将回复的生命值（实时）"),
    "MyTurnPower": ("叠加：层数 = 剩余额外回合数", "剩余额外回合数"),
    "SnakeGamePower": ("不叠加（未升级版；每次打出都是独立实例，只管自己放出去的那三张牌）", "**不显示数字**"),
    "SnakeGameUpgradedPower": ("不叠加（升级版；每次打出都是独立实例，只管自己放出去的那三张牌）", "**不显示数字**"),
    "MinesweeperPower": ("叠加：层数 = 还能自动打出几次炸弹", "还剩几次"),
    "ParkourPower": ("不叠加（未升级版；每次打出都是独立实例）", "**不显示数字**"),
    "ParkourUpgradedPower": ("不叠加（升级版；每次打出都是独立实例）", "**不显示数字**"),
    "ShmupPower": ("不叠加（每次打出都是独立实例）", "**不显示数字**"),
    "PacManPower": ("不叠加（每次打出都是独立实例，升级/非升级各自生效）", "**不显示数字**"),
    "PlantsNextTurnPower": ("不叠加（每次打出都是独立实例，各给各的牌）", "**不显示数字**"),
    "WinEnergyPower": ("叠加：层数 = 剩余生效回合数（回合结束 -1；0 层时还要拦一次重置才消失）", "剩余生效回合数"),
    "ShowMyStrengthPower": ("不叠加（每张独立实例，各自算 10 张倒计时）", "距离下次获得能量的出牌数"),
    "RepeatMovePower": ("不叠加（记录所选牌）", "**不显示数字**"),
    "MontagePower": ("叠加：层数 = 回合结束打出的牌数", "叠加层数"),
    # 继承原版 TemporaryStrengthPower：Title 取自 OriginModel（卡「来自小玉的协助」），
    # Description 指向硬编码的 TEMPORARY_STRENGTH_POWER.* —— 所以模组自己没有它的本地化键。
    "KotamaStrengthPower": ("叠加：层数 = 本回合获得的力量（原版临时力量写法）",
                            "力量层数；标题显示的是来源卡名「来自小玉的协助」"),
}


def load_zh(table):
    return json.load(open(os.path.join(MOD, "localization", "zhs", table + ".json"), encoding="utf-8"))


def load_en(table):
    return json.load(open(os.path.join(MOD, "localization", "eng", table + ".json"), encoding="utf-8"))


def key_of(cls):
    return "STS2_MOMOI_POWER_" + re.sub(r"(?<!^)(?=[A-Z])", "_", cls).upper()


def collect_bases():
    """把「没有 [RegisterPower] 但被当成基类用」的类（如 SnakeGamePowerBase）也抽出来，
    否则子类继承不到 StackType / InstanceType。"""
    out = {}
    for root, _, files in os.walk(CODE):
        for f in sorted(files):
            if not f.endswith(".cs"):
                continue
            txt = open(os.path.join(root, f), encoding="utf-8").read()
            for m in re.finditer(r"\bclass\s+([A-Za-z_]\w*)\s*(?::\s*([A-Za-z_][\w.]*))?", txt):
                cls = m.group(1)
                rest = txt[m.end():]
                nxt = rest.find("\npublic ")
                seg = rest if nxt < 0 else rest[:nxt]
                stack = re.search(r"StackType\s*=>\s*PowerStackType\.(\w+)", seg)
                inst = re.search(r"InstanceType\s*=>\s*PowerInstanceType\.(\w+)", seg)
                if stack or inst:
                    out[cls] = dict(stack=stack.group(1) if stack else None,
                                    inst=inst.group(1) if inst else None)
    return out


def collect():
    out = []
    for root, _, files in os.walk(CODE):
        for f in sorted(files):
            if not f.endswith(".cs"):
                continue
            txt = open(os.path.join(root, f), encoding="utf-8").read()
            for m in re.finditer(r"\[RegisterPower\][\s\S]{0,400}?\bclass\s+([A-Za-z_]\w*)\s*(?::\s*([A-Za-z_][\w.]*))?", txt):
                cls = m.group(1)
                base = (m.group(2) or "").split(".")[-1].strip()
                # 取到下一个 [Register...] 或文件结束
                rest = txt[m.start():]
                nxt = rest.find("\n[Register", 10)
                seg = rest if nxt < 0 else rest[:nxt]
                stack = re.search(r"StackType\s*=>\s*PowerStackType\.(\w+)", seg)
                inst = re.search(r"InstanceType\s*=>\s*PowerInstanceType\.(\w+)", seg)
                disp = re.search(r"override\s+int\s+DisplayAmount\s*=>\s*([^;]+);", seg)
                hidden = "IsVisibleInternal => false" in seg
                out.append(dict(cls=cls, base=base, file=os.path.basename(f),
                                stack=stack.group(1) if stack else "Single",
                                inst=inst.group(1) if inst else "None",
                                disp=disp.group(1).strip() if disp else "",
                                hidden=hidden,
                                _has_stack=bool(stack), _has_inst=bool(inst)))
    return out


def _sem(r):
    """返回 (叠加说明, 右下角说明)，去掉重复前缀。"""
    if r["hidden"]:
        return ("不叠加", "**完全不显示**")
    a, b = SEMANTICS.get(r["cls"], ("叠加：层数按数值生效", "右下角 = 叠加层数"))
    a = re.sub(r"^叠加[：:]\s*", "", a)
    b = re.sub(r"^右下角\s*=\s*", "", b)
    if r["stack"] != "Counter" and not a.startswith("不叠加"):
        a = a
    elif r["stack"] != "Counter":
        a = a
    return (a, b)


def main():
    zh, en = load_zh("powers"), load_en("powers")
    powers = collect()
    # 继承解析：子类没写 StackType/InstanceType 时，沿用本模组基类（含无 [RegisterPower] 的抽象基类）。
    bases = collect_bases()
    byname = {p["cls"]: p for p in powers}
    for p in powers:
        base = bases.get(p.get("base", ""))
        if base is None:
            continue
        if not p.get("_has_stack") and base.get("stack"):
            p["stack"] = base["stack"]
        if not p.get("_has_inst") and base.get("inst"):
            p["inst"] = base["inst"]
    seen = set()
    rows = []
    for p in powers:
        if p["cls"] in seen:
            continue
        seen.add(p["cls"])
        k = key_of(p["cls"])
        title = zh.get(k + ".title", "（无标题）")
        rows.append(dict(p, title=title,
                         desc=zh.get(k + ".description", ""),
                         en=zh.get(k + ".title", "")))

    # 按中文名排序
    rows.sort(key=lambda r: r["title"])

    lines = []
    lines.append("# 模组 power 总览（自动生成 + 人工核对语义）")
    lines.append("")
    lines.append("> 生成脚本：`工作区/_scripts/_power_overview.py`；数据源：`STS2 MomoiCode/**/*.cs` + `localization/zhs/powers.json`。")
    lines.append("> 改完 power 之后重跑一次这个脚本即可刷新。")
    lines.append("")
    lines.append("## 名词说明")
    lines.append("")
    lines.append("| 字段 | 含义 |")
    lines.append("|---|---|")
    lines.append("| **叠加** | `StackType=Counter` 会叠加，`Single` 不叠加 |")
    lines.append("| **实例** | `Instanced` = 每次施加都新建一个独立实例（图标会出现多个） |")
    lines.append("| **右下角** | power 图标右下角那个数字实际显示什么 |")
    lines.append("")
    lines.append("## 总表")
    lines.append("")
    lines.append("| power | 能否叠加 / 怎么叠加 | 实例 | 右下角 | 文本 |")
    lines.append("|---|---|---|---|---|")
    for r in rows:
        sem = _sem(r)
        inst = "独立实例" if r["inst"] == "Instanced" else "唯一"
        disp = sem[1]
        desc = r["desc"].replace("\n", "⏎").replace("|", "/")
        lines.append("| %s | %s | %s | %s | %s |" % (r["title"], sem[0], inst, disp, desc))
    lines.append("")
    lines.append("## 逐个详情")
    lines.append("")
    for r in rows:
        sem = _sem(r)
        lines.append("### %s" % r["title"])
        lines.append("")
        lines.append("- 类名：`%s`（%s）" % (r["cls"], r["file"]))
        lines.append("- 叠加：%s" % sem[0])
        lines.append("- 实例：%s" % ("每次施加新建独立实例（`Instanced`）" if r["inst"] == "Instanced" else "同一目标上只有一个（新施加叠层）"))
        lines.append("- 右下角：%s" % sem[1])
        if r["hidden"]:
            lines.append("- 可见性：**隐藏**（纯逻辑记录，不出图标）")
        lines.append("- 文本：%s" % r["desc"].replace("\n", "  \n    "))
        lines.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("已写出 %s（%d 个 power）" % (os.path.relpath(OUT, ROOT), len(rows)))
    miss = [r["cls"] for r in rows if r["cls"] not in SEMANTICS]
    if miss:
        print("没有人工语义、用了默认值的：", miss)


if __name__ == "__main__":
    main()
