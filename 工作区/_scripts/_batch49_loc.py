# -*- coding: utf-8 -*-
"""批次49 本地化：明日奈（持续到下回合开始）、循环叙事（注能 + 回合结束选牌洗回）、选择界面文本。"""
import io, json

ROOT = "C:/Users/asus/RiderProjects/STS2 Momoi/STS2 Momoi/STS2_Momoi/localization"

UPDATES = {
    ("zhs", "cards"): {
        "STS2_MOMOI_CARD_MOMOI_SUPPORT_ASUNA.description":
            "获得{Vigor:diff()}点[gold]活力[/gold]。\n获得{Dex:diff()}点[gold]敏捷[/gold]。\n"
            "直到你的下回合开始前，你受到的所有伤害降低{IfUpgraded:show:40%|25%}。",
        "STS2_MOMOI_CARD_MOMOI_SUPPORT_ASUNA.smartDescription":
            "获得{Vigor:diff()}点[gold]活力[/gold]。\n获得{Dex:diff()}点[gold]敏捷[/gold]。\n"
            "直到你的下回合开始前，你受到的所有伤害降低{IfUpgraded:show:40%|25%}。",
        "STS2_MOMOI_CARD_CYCLIC_NARRATIVE.description":
            "[gold]注能[/gold]。\n本回合结束时，将[gold]弃牌堆[/gold]的最多1张牌洗入你的[gold]抽牌堆[/gold]。",
        "STS2_MOMOI_CARD_CYCLIC_NARRATIVE.smartDescription":
            "[gold]注能[/gold]。\n本回合结束时，将[gold]弃牌堆[/gold]的最多1张牌洗入你的[gold]抽牌堆[/gold]。",
    },
    ("eng", "cards"): {
        "STS2_MOMOI_CARD_MOMOI_SUPPORT_ASUNA.description":
            "Gain {Vigor:diff()} Vigor.\nGain {Dex:diff()} Dexterity.\n"
            "Until the start of your next turn, all damage you take is reduced by {IfUpgraded:show:40%|25%}.",
        "STS2_MOMOI_CARD_MOMOI_SUPPORT_ASUNA.smartDescription":
            "Gain {Vigor:diff()} Vigor.\nGain {Dex:diff()} Dexterity.\n"
            "Until the start of your next turn, all damage you take is reduced by {IfUpgraded:show:40%|25%}.",
        "STS2_MOMOI_CARD_CYCLIC_NARRATIVE.description":
            "[gold]Imbued[/gold].\nAt the end of this turn, shuffle up to 1 card from your [gold]Discard Pile[/gold] "
            "into your [gold]Draw Pile[/gold].",
        "STS2_MOMOI_CARD_CYCLIC_NARRATIVE.smartDescription":
            "[gold]Imbued[/gold].\nAt the end of this turn, shuffle up to 1 card from your [gold]Discard Pile[/gold] "
            "into your [gold]Draw Pile[/gold].",
    },
    ("zhs", "powers"): {
        "STS2_MOMOI_POWER_ASUNA_GUARD_POWER.description":
            "直到你的下回合开始前，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。",
        "STS2_MOMOI_POWER_ASUNA_GUARD_POWER.smartDescription":
            "直到你的下回合开始前，你受到的所有伤害降低[blue]{ReductionPct}%[/blue]。",
        "STS2_MOMOI_POWER_CYCLIC_NARRATIVE_POWER.description":
            "本回合结束时，将[gold]弃牌堆[/gold]的最多[blue]{Amount}[/blue]张牌洗入你的[gold]抽牌堆[/gold]。",
        "STS2_MOMOI_POWER_CYCLIC_NARRATIVE_POWER.smartDescription":
            "本回合结束时，将[gold]弃牌堆[/gold]的最多[blue]{Amount}[/blue]张牌洗入你的[gold]抽牌堆[/gold]。",
    },
    ("eng", "powers"): {
        "STS2_MOMOI_POWER_ASUNA_GUARD_POWER.description":
            "Until the start of your next turn, all damage you take is reduced by [blue]{ReductionPct}%[/blue].",
        "STS2_MOMOI_POWER_ASUNA_GUARD_POWER.smartDescription":
            "Until the start of your next turn, all damage you take is reduced by [blue]{ReductionPct}%[/blue].",
        "STS2_MOMOI_POWER_CYCLIC_NARRATIVE_POWER.description":
            "At the end of this turn, shuffle up to [blue]{Amount}[/blue] cards from your [gold]Discard Pile[/gold] "
            "into your [gold]Draw Pile[/gold].",
        "STS2_MOMOI_POWER_CYCLIC_NARRATIVE_POWER.smartDescription":
            "At the end of this turn, shuffle up to [blue]{Amount}[/blue] cards from your [gold]Discard Pile[/gold] "
            "into your [gold]Draw Pile[/gold].",
    },
    ("zhs", "card_selection"): {
        "STS2_MOMOI_CYCLIC_NARRATIVE_HEADER": "选择最多{Amount}张牌洗入你的抽牌堆。",
    },
    ("eng", "card_selection"): {
        "STS2_MOMOI_CYCLIC_NARRATIVE_HEADER": "Choose up to {Amount} cards to shuffle into your Draw Pile.",
    },
}

report = []
for (lang, table), entries in UPDATES.items():
    path = f"{ROOT}/{lang}/{table}.json"
    data = json.load(io.open(path, encoding="utf-8"))
    for key, value in entries.items():
        old = data.get(key)
        data[key] = value
        report.append(f"{lang}/{table} {key}: {'ADDED' if old is None else ('SAME' if old == value else 'UPDATED')}")
    io.open(path, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

io.open("C:/tmp/loc49_report.txt", "w", encoding="utf-8").write("\n".join(report) + "\n")
print("ok", len(report))
