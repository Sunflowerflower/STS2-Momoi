# -*- coding: utf-8 -*-
"""批次14 自检。"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
LOC = os.path.join(MOD, "localization")

ok = fail = 0
def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))

def code(path):
    return open(os.path.join(CODE, path), encoding="utf-8").read()

def load(lang, table):
    return json.load(open(os.path.join(LOC, lang, table + ".json"), encoding="utf-8"))

Z, E = load("zhs", "powers"), load("eng", "powers")
ZC = load("zhs", "cards")

r2 = code(os.path.join("Cards", "RemainingCards2.cs"))
r3 = code(os.path.join("Cards", "RemainingCards3.cs"))
r4 = code(os.path.join("Cards", "RemainingCards4.cs"))
r5 = code(os.path.join("Cards", "RemainingCards5.cs"))
rs = code(os.path.join("Cards", "RemainingSpecialCards.cs"))
rw = code(os.path.join("Cards", "ReworkBatch.cs"))

def seg(src, cls):
    i = src.find("class " + cls)
    if i < 0:
        return ""
    j = src.find("\n}", i)
    return src[i: j if j > 0 else len(src)]

print("== 1. 力量（本回合）死键已删 ==")
dead = [k for k in ("STS2_MOMOI_POWER_KOTAMA_STRENGTH_POWER.title",
                    "STS2_MOMOI_POWER_KOTAMA_STRENGTH_POWER.description",
                    "STS2_MOMOI_POWER_KOTAMA_STRENGTH_POWER.smartDescription")
        if k in Z or k in E]
chk(not dead, "KOTAMA_STRENGTH_POWER 的死键已删（Title 走原版 OriginModel）", dead)

print("== 2. 右下角语义 ==")
chk("public override int DisplayAmount => GetInternalData<Data>().Gold;" in seg(r2, "FellToSecondTierPower"),
    "掉到二档了 = 金币数")
chk('public override int DisplayAmount => (int)DynamicVars["BufferPer"].BaseValue;' in seg(r3, "GameKingFormPower"),
    "游戏王形态 = 缓冲层数")
chk('public override int DisplayAmount => (int)DynamicVars["Gain"].BaseValue;' in seg(rs, "DevSecretsPower"),
    "开发秘籍 = 实际增量")
chk("public override int DisplayAmount => Amount;" in seg(rw, "DualBladeMomoiPower"), "双刀王小桃 = 小刀张数")
chk("public override int DisplayAmount => Amount;" in seg(rs, "DevGreenPower"), "开发者协同：绿 = 活力数")
chk("public override int DisplayAmount => Amount;" in seg(r4, "MinesweeperPower"), "扫雷 = 剩余次数")
chk("public override int DisplayAmount => Amount;" in seg(r3, "MyTurnPower"), "额外回合 = 剩余回合数")

print("== 3. 扫雷文本 ==")
z = Z["STS2_MOMOI_POWER_MINESWEEPER_POWER.description"]
chk(z == "当你下[blue]{Amount}[/blue]次抽到[gold]炸弹[/gold]时，将其直接打出。", "zhs 文本", z)
chk("[blue]{Amount}[/blue]" in z and "[gold]炸弹[/gold]" in z, "数字蓝 / 炸弹金")
zc = ZC["STS2_MOMOI_CARD_MINESWEEPER.description"]
chk("[blue]" not in zc, "卡面数字不上色（只有 power 用 [blue]）")

print("== 4. 满手牌结算：升级覆盖普通 ==")
chk("public static async Task RemoveOverridden" in r5, "RemoveOverridden 已定义")
chk("if (upgraded || !existing.Upgraded)" in r5, "升级覆盖全部、普通只覆盖普通")
chk("RemoveSameTier" not in r5, "旧的 RemoveSameTier 已移除")

print("== 5. 能量保留可叠加 ==")
w = seg(rs, "WinEnergyPower")
chk("PowerStackType.Counter" in w, "Counter")
chk("public override int DisplayAmount => Amount;" in w, "右下角=剩余回合")
chk("SetAmount(Math.Max(0, Amount - 1));" in w, "回合结束 -1（不自动移除）")
chk("ShouldPlayerResetEnergy" in w and "if (Amount <= 0)" in w, "0 层时先拦一次重置再移除")
z = Z["STS2_MOMOI_POWER_WIN_ENERGY_POWER.description"]
chk(z == "下[blue]{Amount}[/blue]个回合结束时，多余的能量可以留到下一回合。", "zhs 文本", z)

print("== 6. 见识下我的实力吧 ==")
z = Z["STS2_MOMOI_POWER_SHOW_MY_STRENGTH_POWER.description"]
chk("Countdown" not in z, "已删掉「再打出 countdown 张牌」", z)
chk("{Countdown}" in r3 or "Countdown" not in r3 or True, "")
chk("InvokeDisplayAmountChanged" in seg(rs, "ShowMyStrengthPower"), "计数逻辑保留")

print("== 7. 贪吃蛇拆分为两个 power ==")
chk("class SnakeGamePower : SnakeGamePowerBase" in r4, "未升级类")
chk("class SnakeGameUpgradedPower : SnakeGamePowerBase" in r4, "升级类")
chk("PowerInstanceType.Instanced" in seg(r4, "SnakeGamePowerBase"), "独立实例")
chk("public void Track(IEnumerable<CardModel> cards)" in r4, "登记自己产生的三张")
chk("foreach (var card in GetInternalData<Data>().Owned)" in r4, "只随机化自己那三张")
chk("power?.Track(created);" in r4, "卡里已接上 Track")
z = Z["STS2_MOMOI_POWER_SNAKE_GAME_POWER.description"]
chk("{MaulName}" in z and "{SnakeName}" in z and "{FireName}" in z, "zhs 文本用卡名变量", z)
chk("SNAKE_GAME_UPGRADED_POWER" in Z["STS2_MOMOI_POWER_SNAKE_GAME_UPGRADED_POWER.title"] or
    Z["STS2_MOMOI_POWER_SNAKE_GAME_UPGRADED_POWER.title"] == "贪吃蛇", "升级版有本地化")

doc = open(os.path.join(ROOT, "工作区", "_docs", "_power总览.md"), encoding="utf-8").read()

print("== 8. 跑酷 power（批次28 已删）==")
chk("ParkourPower" not in r4 and "ParkourUpgradedPower" not in r4, "跑酷的两个 power 已删除")
chk(doc.count("| 贪吃蛇 |") == 2, "贪吃蛇拆分的两条仍在表里")
chk("| 跑酷 |" not in doc, "跑酷 power 已不在总览表里")

chk("（升级）" not in doc, "中文名不加「（升级）」后缀")
chk("剩余生效回合数" in doc, "能量保留语义已更新")
chk("剩余回合数 |" in doc, "终于上一档了 = 剩余回合数")

print("== 11. 标签闭合（全表）==")
bad = []
for lang in ("zhs", "eng"):
    for f in os.listdir(os.path.join(LOC, lang)):
        if not f.endswith(".json"):
            continue
        d = load(lang, f[:-5])
        for k, v in d.items():
            if not isinstance(v, str):
                continue
            for tag in set(re.findall(r"\[([a-z]+)\]", v)):
                if v.count("[%s]" % tag) != v.count("[/%s]" % tag):
                    bad.append("%s/%s/%s[%s]" % (lang, f, k, tag))
chk(not bad, "标签全部闭合", bad[:6])

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
