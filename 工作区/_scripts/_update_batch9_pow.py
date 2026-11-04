# -*- coding: utf-8 -*-
"""2026-10-11 批次9 · 能力（侧栏）文本同步
  * 与卡牌同口径的「在你的回合开始时 / 在你的回合结束时」
  * 吃豆人能力描述按新行为改写
用法：py -3 _update_batch9_pow.py [--dry]
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "localization")

REPL = [
    ("STS2_MOMOI_POWER_SPEAR_SHIELD_POWER.description", "回合结束时，手牌中每有一张构想", "在你的回合结束时，手牌中每有一张构想"),
    ("STS2_MOMOI_POWER_CONCEPT_SHIELD_POWER.description", "回合结束时，手牌中每有一张构想", "在你的回合结束时，手牌中每有一张构想"),
    ("STS2_MOMOI_POWER_DEV_GREEN_POWER.description", "回合开始时获得", "在你的回合开始时获得"),
    ("STS2_MOMOI_POWER_HELP_FROM_MANY_POWER.description", "回合开始时，将", "在你的回合开始时，将"),
    ("STS2_MOMOI_POWER_HELP_FROM_MANY_UPGRADED_POWER.description", "回合开始时，将", "在你的回合开始时，将"),
    ("STS2_MOMOI_POWER_PARKOUR_POWER.description", "回合开始时重复跑酷效果", "在你的回合开始时重复跑酷效果"),
    ("STS2_MOMOI_POWER_RHYTHM_GAME_POWER.description", "回合开始时，将1~4张方块", "在你的回合开始时，将1~4张方块"),
    ("STS2_MOMOI_POWER_RHYTHM_GAME_POWER.description", "回合结束时，消耗所有方块", "在你的回合结束时，消耗所有方块"),
    ("STS2_MOMOI_POWER_ROLE_PLAY_POWER.description", "回合开始时，将1张", "在你的回合开始时，将1张"),
]

# 吃豆人能力：整体改写
PAC = {
    "zhs": ("STS2_MOMOI_POWER_PAC_MAN_POWER.description",
            "在你的回合开始时，若你有诅咒牌，则直接打出{FrenzyName}并消耗随机诅咒；若你没有诅咒牌，则获得{AbundanceName}。"),
    "eng": ("STS2_MOMOI_POWER_PAC_MAN_POWER.description",
            "At the start of your turn, if you have any Curses, play {FrenzyName} directly and exhaust a random Curse; if you have no Curses, gain {AbundanceName}."),
}


def main():
    dry = "--dry" in sys.argv
    n = 0
    for lang in ("zhs", "eng"):
        p = os.path.join(MOD, lang, "powers.json")
        d = json.load(open(p, encoding="utf-8"))
        if lang == "zhs":
            for key, old, new in REPL:
                cur = d.get(key)
                if cur is None:
                    print("  !! 缺 key:", key); continue
                if old not in cur:
                    print("  !! 未匹配:", key, "|", old[:40]); continue
                d[key] = cur.replace(old, new)
                sk = key[:-len("description")] + "smartDescription"
                if sk in d:
                    d[sk] = d[sk].replace(old, new)
                n += 1
        k, txt = PAC[lang]
        d[k] = txt
        sk = k[:-len("description")] + "smartDescription"
        if sk in d:
            d[sk] = txt
        n += 1
        if not dry:
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("[%s] powers.json 更新" % lang)
    print("共 %d 处" % n, "[dry-run]" if dry else "已写入")


if __name__ == "__main__":
    main()
