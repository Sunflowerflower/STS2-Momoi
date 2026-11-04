# -*- coding: utf-8 -*-
"""2026-10-12 批次9d · 衍生牌升级后「整个卡名」变绿

背景：绿色来自 ShowIfUpgradedFormatter —— 它在 UpgradePreview 模式下只给**分支内容**套 [green]。
老写法 `[gold]名字{IfUpgraded:show:+}[/gold]` 把名字留在分支外，只有那个「+」变绿。
统一改成：`{IfUpgraded:show:[green]名字+[/green]|[gold]名字[/gold]}`
（第一个分支自带 [green]，保证 Upgraded 模式也绿；第二个分支保持金色，未升级时不变）。

覆盖 9 张（用户点名 8 张 + 同类漏网的「虚拟女仆武器！」）：
  灵感爆发 / 捕鱼达人！ / 双刀王小桃 / 打灰机！ / LOSE！ / 贪吃蛇 / 扫雷 /
  愤怒的小鸟 / 虚拟女仆武器！ / 来自时的援护（这张原本连「+」都没有）
用法：py -3 _update_batch9d_loc.py [--dry]
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi", "localization")


def green(name, gold_wrap=True):
    """生成「未升级=金色名字 / 升级=绿色名字+」的写法"""
    base = "[gold]%s[/gold]" % name if gold_wrap else name
    return "{IfUpgraded:show:[green]%s+[/green]|%s}" % (name, base)


# (卡 key, 旧片段, 新片段)  —— 只替换「带 {IfUpgraded:show:+} 的那一处」
Z = [
    ("INSPIRATION", "[gold]我的回合！{IfUpgraded:show:+}[/gold]", green("我的回合！")),
    ("FISHING_MASTER", "[gold]渔获{IfUpgraded:show:+}[/gold]", green("渔获")),
    ("DUAL_BLADE_MOMOI", "[gold]小刀{IfUpgraded:show:+}[/gold]", green("小刀")),
    ("SHMUP", "[gold]燃料{IfUpgraded:show:+}[/gold]", green("燃料")),
    ("LOSE_CARD", "[gold]创作的痛苦{IfUpgraded:show:+}[/gold]", green("创作的痛苦")),
    ("SNAKE_GAME", "[gold]撕咬{IfUpgraded:show:+}[/gold]", green("撕咬")),
    ("SNAKE_GAME", "[gold]蛇咬{IfUpgraded:show:+}[/gold]", green("蛇咬")),
    ("SNAKE_GAME", "[gold]火蛇怒咬{IfUpgraded:show:+}[/gold]", green("火蛇怒咬")),
    ("MINESWEEPER", "[gold]炸弹{IfUpgraded:show:+}[/gold]", green("炸弹")),
    ("ANGRY_BIRDS", "[gold]愤怒{IfUpgraded:show:+}[/gold]", green("愤怒")),
    ("ANGRY_BIRDS", "[gold]异鸟扑击{IfUpgraded:show:+}[/gold]", green("异鸟扑击")),
    ("MAID_WEAPON", "[gold]当心误射！{IfUpgraded:show:+}[/gold]", green("当心误射！")),
    # 来自时的援护：原来写死了名字、连「+」都没有
    ("MOMOI_SUPPORT_TOKI", "[gold]系统：阿比舒[/gold]",
     "{IfUpgraded:show:[green]系统：阿比舒+[/green]|[gold]系统：阿比舒[/gold]}"),
]

E = [
    ("INSPIRATION", "My Turn!{IfUpgraded:show:+}", green("My Turn!", gold_wrap=False)),
    ("FISHING_MASTER", "[gold]Catch{IfUpgraded:show:+}[/gold]", green("Catch")),
    ("DUAL_BLADE_MOMOI", "[gold]Shiv{IfUpgraded:show:+}[/gold]", green("Shiv")),
    ("SHMUP", "Fuel{IfUpgraded:show:+}", green("Fuel", gold_wrap=False)),
    ("LOSE_CARD", "Creative Pain{IfUpgraded:show:+}", green("Creative Pain", gold_wrap=False)),
    ("SNAKE_GAME", "[gold]Maul{IfUpgraded:show:+}[/gold]", green("Maul")),
    ("SNAKE_GAME", "[gold]Snakebite{IfUpgraded:show:+}[/gold]", green("Snakebite")),
    ("SNAKE_GAME", "[gold]Fire Serpent Bite{IfUpgraded:show:+}[/gold]", green("Fire Serpent Bite")),
    ("MINESWEEPER", "The Bomb{IfUpgraded:show:+}", green("The Bomb", gold_wrap=False)),
    ("ANGRY_BIRDS", "Anger{IfUpgraded:show:+}", green("Anger", gold_wrap=False)),
    ("ANGRY_BIRDS", "Byrd Swoop{IfUpgraded:show:+}", green("Byrd Swoop", gold_wrap=False)),
    ("MAID_WEAPON", "[gold]Watch Out!{IfUpgraded:show:+}[/gold]", green("Watch Out!")),
    ("MOMOI_SUPPORT_TOKI", "[gold]System: Abishu[/gold]",
     "{IfUpgraded:show:[green]System: Abishu+[/green]|[gold]System: Abishu[/gold]}"),
]


def apply(path, table):
    d = json.load(open(path, encoding="utf-8"))
    ok, miss = 0, []
    for ckey, old, new in table:
        key = "STS2_MOMOI_CARD_" + ckey + ".description"
        cur = d.get(key)
        if cur is None:
            miss.append((ckey, "缺 key")); continue
        if old not in cur:
            miss.append((ckey, "未匹配 %r" % old)); continue
        d[key] = cur.replace(old, new)
        sk = key[:-len("description")] + "smartDescription"
        if sk in d:
            d[sk] = d[sk].replace(old, new)
        ok += 1
    return d, ok, miss


def main():
    dry = "--dry" in sys.argv
    total = 0
    for lang, tbl in (("zhs", Z), ("eng", E)):
        p = os.path.join(MOD, lang, "cards.json")
        d, ok, miss = apply(p, tbl)
        total += ok
        print("[%s] %d 处替换" % (lang, ok))
        for c, why in miss:
            print("   !! %s %s" % (c, why))
        if not dry:
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("共 %d 处" % total, "[dry-run]" if dry else "已写入")


if __name__ == "__main__":
    main()
