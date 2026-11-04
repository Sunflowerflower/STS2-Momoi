# -*- coding: utf-8 -*-
"""批次50 本地化：绝地求生括号仅局内显示 + 明日奈减伤 power 文本带层数。"""
import io
import json
import os

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi\STS2 Momoi\STS2_Momoi\localization"


def load(lang, name):
    path = os.path.join(ROOT, lang, name)
    with io.open(path, encoding="utf-8") as f:
        return path, json.load(f)


def save(path, data):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


changes = 0

# ---------------- 1) 绝地求生：括号内容只在战斗中显示 ----------------
for lang, sep in (("zhs", "（"), ("eng", " (")):
    path, data = load(lang, "cards.json")
    for key in ("STS2_MOMOI_CARD_BATTLE_ROYALE.description",
                "STS2_MOMOI_CARD_BATTLE_ROYALE.smartDescription"):
        value = data[key]
        assert "{InCombat:" not in value, key
        idx = value.rindex(sep)
        data[key] = value[:idx] + "{InCombat:" + value[idx:] + "|}"
        changes += 1
    save(path, data)

# ---------------- 2) 明日奈减伤 power：显示叠加后的持续回合数 ----------------
MARK = {
    "zhs": ("你的下回合开始前", "你的下[blue]{Amount}[/blue]个回合开始前"),
    "eng": ("your next turn", "your next [blue]{Amount}[/blue] turn(s)"),
}
for lang, (old, new) in MARK.items():
    path, data = load(lang, "powers.json")
    for key in ("STS2_MOMOI_POWER_ASUNA_GUARD_POWER.description",
                "STS2_MOMOI_POWER_ASUNA_GUARD_POWER.smartDescription"):
        value = data[key]
        assert value.count(old) == 1, (lang, key, value)
        data[key] = value.replace(old, new)
        changes += 1
    save(path, data)

print("批次50 本地化改完：%d 处" % changes)
