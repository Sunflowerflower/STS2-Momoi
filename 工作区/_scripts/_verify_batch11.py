# -*- coding: utf-8 -*-
"""批次11 自检：文本/颜色/侧栏/贴图 逐项核对。"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")

ok = fail = 0
def check(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + detail if detail else ""))

def load(lang, table):
    return json.load(open(os.path.join(MOD, "localization", lang, table + ".json"), encoding="utf-8"))

Z, E = {t: load("zhs", t) for t in ("relics", "potions", "cards")}, \
       {t: load("eng", t) for t in ("relics", "potions", "cards")}

print("== 1. 捕鱼达人 ==")
for lang, d in (("zhs", Z), ("eng", E)):
    for suf in (".description", ".smartDescription"):
        s = d["cards"]["STS2_MOMOI_CARD_FISHING_MASTER" + suf]
        check("对1名敌人" not in s and "to an enemy" not in s, "%s %s 已删「对1名敌人」" % (lang, suf))

print("== 2. 遗物 flavor ==")
RELICS = ["DRIED_INSPIRATION", "OVERFLOWING_INSPIRATION", "UNFINISHED_CHIPS", "WINNING_SCRIPT",
          "OLD_GAME_CONSOLE", "GREEN_CHARM", "BOARD_GAME_OF_LIFE", "G_BIBLE", "MIRROR"]
for r in RELICS:
    k = "STS2_MOMOI_RELIC_" + r + ".flavor"
    check(Z["relics"].get(k) == "[red]这个遗物的细节将在未来揭晓……[/red]", "zhs %s flavor" % r, repr(Z["relics"].get(k)))
    check(E["relics"].get(k) == "[red]Details for this relic will be revealed in the future...[/red]",
          "eng %s flavor" % r, repr(E["relics"].get(k)))

print("== 3. 药水 ==")
P = {
    "INSTANT_COFFEE": ["[gold]构想[/gold]", "[red]睡眠不佳[/red]", "[gold]手牌[/gold]"],
    "STRAWBERRY_MILK": ["[blue]7[/blue]", "[blue]1[/blue]", "[gold]力量[/gold]"],
    "PEACH_SODA": ["[gold]手牌[/gold]", "[gold]变化[/gold]", "[gold]小游戏牌[/gold]"],
}
for p, need in P.items():
    s = Z["potions"]["STS2_MOMOI_POTION_" + p + ".description"]
    for n in need:
        check(n in s, "zhs %s 含 %s" % (p, n))
check(Z["potions"]["STS2_MOMOI_POTION_PEACH_SODA.description"]
      == "将你[gold]手牌[/gold]中的任意张牌[gold]变化[/gold]为随机[gold]小游戏牌[/gold]。",
      "zhs 桃味气泡水 文本一字不差")
plain = re.sub(r"\[/?[a-z]+\]", "", Z["potions"]["STS2_MOMOI_POTION_PEACH_SODA.description"])
check(plain == "将你手牌中的任意张牌变化为随机小游戏牌。", "zhs 桃味气泡水 去标记后 = 要求原文", repr(plain))

print("== 4. 遗物描述着色 ==")
R = {
    "DRIED_INSPIRATION": ["[gold]手牌[/gold]", "[blue]1[/blue]", "[gold]构想[/gold]"],
    "OVERFLOWING_INSPIRATION": ["[green]构想+[/green]", "[blue]1[/blue]", "[gold]手牌[/gold]"],
    "UNFINISHED_CHIPS": ["[blue]50[/blue]", "[gold]金币[/gold]", "[blue]1[/blue]", "[gold]休息处[/gold]", "[gold]商店房间[/gold]"],
    "WINNING_SCRIPT": ["[gold]构想[/gold]", "[gold]升级[/gold]", "[gold]手牌[/gold]"],
    "OLD_GAME_CONSOLE": ["[gold]小游戏牌[/gold]", "[gold]手牌[/gold]"],
    "GREEN_CHARM": ["[gold]消耗[/gold]", "[red]诅咒[/red]", "[gold]构想[/gold]"],
    "BOARD_GAME_OF_LIFE": ["[gold]小游戏牌[/gold]", "[gold]手牌[/gold]"],
    "G_BIBLE": ["[blue]5[/blue]", "[gold]小游戏牌[/gold]", "[green]6[/green]"],
    "MIRROR": ["[gold]保留[/gold]"],
}
for r, need in R.items():
    s = Z["relics"]["STS2_MOMOI_RELIC_" + r + ".description"]
    for n in need:
        check(n in s, "zhs %s 含 %s" % (r, n))
check(Z["relics"]["STS2_MOMOI_RELIC_OLD_GAME_CONSOLE.description"]
      == "在每场战斗开始时，将一张随机[gold]小游戏牌[/gold]加入你的[gold]手牌[/gold]。",
      "zhs 旧游戏机 文本规范")
check(re.sub(r"\[/?[a-z]+\]", "", Z["relics"]["STS2_MOMOI_RELIC_WINNING_SCRIPT.description"])
      == "每当你打出构想时，升级你手牌中的所有牌。", "zhs 胜利的剧本 文本规范")
check(re.sub(r"\[/?[a-z]+\]", "", Z["relics"]["STS2_MOMOI_RELIC_GREEN_CHARM.description"])
      == "在你的回合开始时，你可以消耗一张诅咒牌来使构想数值+1。", "zhs 绿色挂饰 文本规范")
check(re.sub(r"\[/?[a-z]+\]", "", Z["relics"]["STS2_MOMOI_RELIC_MIRROR.description"])
      == "在你的第一个回合结束时，你可以选择一张牌复制并将它们保留一回合。", "zhs 镜子 文本规范")
check(re.sub(r"\[/?[a-z]+\]", "", Z["relics"]["STS2_MOMOI_RELIC_UNFINISHED_CHIPS.description"])
      == "你每有50金币，当你进入商店房间和休息处时就将你的最大生命值提升1点。", "zhs 薯片 文本规范")

print("== 5. 卡牌的诅咒红字 ==")
cz = Z["cards"]
for k in ["STS2_MOMOI_CARD_CONCEPT_CARD.description", "STS2_MOMOI_CARD_CONCEPT_CARD.smartDescription",
          "STS2_MOMOI_CARD_CONCEPT_CARD.sidebarCurse", "STS2_MOMOI_CARD_GRINDING.description",
          "STS2_MOMOI_CARD_GRINDING.smartDescription", "STS2_MOMOI_CARD_GRINDING.sidebar",
          "STS2_MOMOI_CARD_PAC_MAN.description", "STS2_MOMOI_CARD_PAC_MAN.smartDescription",
          "STS2_MOMOI_CARD_DESTRUCTION_AND_REBIRTH.description",
          "STS2_MOMOI_CARD_DESTRUCTION_AND_REBIRTH.smartDescription"]:
    s = cz[k]
    check("[red]诅咒[/red]" in s, "zhs %s 有红「诅咒」" % k.split(".")[-2][-22:] if False else "zhs " + k)
check("[red]睡眠不佳[/red]" in cz["STS2_MOMOI_CARD_STAY_UP_LATE.description"], "zhs 熬夜 红「睡眠不佳」")
check("[red]苦恼[/red]" in cz["STS2_MOMOI_CARD_CONCEPT_CARD.sidebarCurse"], "zhs 侧栏 红「苦恼」")
check("[red]执迷[/red]" in cz["STS2_MOMOI_CARD_GRINDING.sidebar"], "zhs 侧栏 红「执迷」")

# 全表扫描：还有没有漏网的裸「诅咒」/裸诅咒牌名
CURSE_NAMES = ["债务", "凡庸", "受伤", "孢子心灵", "悔恨", "愚行", "愧疚", "执迷", "疑虑",
               "睡眠不佳", "笨拙", "羞耻", "腐朽", "苦恼", "铃铛的诅咒", "霉运"]
leak = []
for k, v in cz.items():
    s = str(v)
    if not isinstance(v, str):
        continue
    for m in re.finditer(r"诅咒|" + "|".join(CURSE_NAMES), s):
        i = m.start()
        # 前面 5 个字符里有没有 [red] 包裹
        if "[red]" not in s[max(0, i - 5):i]:
            leak.append((k, s[max(0, i - 12):i + 12]))
check(not leak, "zhs 无漏网的裸诅咒/诅咒牌名", str(leak[:6]))

print("== 6. 富文本标签闭合（zhs+eng 全表）==")
bad = []
for lang, tables in (("zhs", Z), ("eng", E)):
    for tname, d in tables.items():
        for k, v in d.items():
            if not isinstance(v, str):
                continue
            for tag in re.findall(r"\[([a-z]+)\]", v):
                if v.count("[%s]" % tag) != v.count("[/%s]" % tag):
                    bad.append("%s/%s/%s [%s]" % (lang, tname, k, tag))
check(not bad, "所有标签成对", str(bad[:6]))

print("== 7. 代码侧：侧栏 & 资源 ==")
src = ""
for root, _, files in os.walk(CODE):
    for f in files:
        if f.endswith(".cs"):
            src += open(os.path.join(root, f), encoding="utf-8").read()
pot = open(os.path.join(CODE, "Potions", "MomoiPotions.cs"), encoding="utf-8").read()
rel1 = open(os.path.join(CODE, "Relics", "DriedInspiration.cs"), encoding="utf-8").read()
rel2 = open(os.path.join(CODE, "Relics", "MoreRelics.cs"), encoding="utf-8").read()
check(pot.count("AdditionalHoverTips") == 3, "3 个药水都有侧栏", str(pot.count("AdditionalHoverTips")))
check(rel1.count("AdditionalHoverTips") == 1, "枯竭灵感有侧栏")
check(rel2.count("AdditionalHoverTips") == 6, "MoreRelics 里 6 处侧栏", str(rel2.count("AdditionalHoverTips")))
check("PeachSoda" in pot and pot.count("PotionAssetProfile") == 3, "桃味气泡水已补 AssetProfile",
      "PotionAssetProfile 出现 %d 次（应为 3）" % pot.count("PotionAssetProfile"))
check("MerchantRoom" in rel2 and "AfterRoomEntered" in rel2, "薯片已加商店触发")
check("BeforeRoomEntered" not in rel2, "薯片旧触发已移除")

print("== 8. 贴图文件 ==")
for name in ["InstantCoffee", "StrawberryMilk", "PeachSoda"]:
    for suf in ["", "_outline"]:
        p = os.path.join(MOD, "images", "potions", name + suf + ".png")
        check(os.path.exists(p), "potions/%s%s.png" % (name, suf))
for name in ["DriedInspiration", "OverflowingInspiration", "UnfinishedChips", "WinningScript",
             "OldGameConsole", "GreenCharm", "BoardGameOfLife", "GBible", "Mirror", "YummyCookie_Momoi"]:
    check(os.path.exists(os.path.join(MOD, "images", "relics", name + "_outline.png")), "relics/%s_outline.png" % name)

print("== 9. power 图标 ==")
PW = os.path.join(MOD, "images", "powers")
used = set(re.findall(r'IconPath:\s*\$?"\{Entry\.ResPath\}/images/powers/([a-z0-9_]+\.png)"', src))
missing = [f for f in used if not os.path.exists(os.path.join(PW, f))]
orphan = [f for f in os.listdir(PW) if f.endswith(".png") and f not in used]
check(not missing, "power 图标无缺失（%d 个引用）" % len(used), str(missing))
check(not orphan, "power 图标无孤儿", str(orphan))

print("\n结果：%d 通过 / %d 失败" % (ok, fail))
sys.exit(1 if fail else 0)
