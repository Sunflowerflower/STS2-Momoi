# -*- coding: utf-8 -*-
"""批次10：把新美术接入模组

  1) 卡面修改1/双线叙事.png        → images/cards/DualNarrative.png
  2) power图标成品/*.png           → images/powers/<class 用到的文件名>.png
     （其中 4 张是「原来两张 power 共用一张图」，这次拆成独立文件；1 张改名）
  3) 遗物成品区/*.png              → images/relics/<RelicClass>.png
  4) 药水成品区/*.png              → images/potions/<PotionClass>.png

用法：py -3 _apply_batch10_art.py [--dry]
"""
import os, shutil, sys, datetime, re

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
WS = os.path.join(ROOT, "工作区")
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
IMG = os.path.join(MOD, "images")
BAK = os.path.join(WS, "_backup", "batch10_pre")

# ── 1. 卡面 ────────────────────────────────────────────────────────────────
CARD = [("双线叙事.png", "DualNarrative.png")]

# ── 2. power 图标：(工作区/power图标成品 里的中文名子串, 目标文件名) ─────────
#    目标文件名 = 代码 PowerAssetProfile.IconPath 里写的那个
POWER = [
    ("C&C的援护", "cnc_tracker_power.png"),
    ("雷酱", "yoshimi_repeat_power.png"),
    ("专注", "focus_power.png"),
    ("俄罗斯方块", "tetris_full_hand_power.png"),
    ("创造性品味", "creative_taste_power.png"),
    ("双刀王小桃", "dual_blade_momoi_power.png"),
    ("发布委托", "post_quest_power.png"),
    ("吃豆人", "pac_man_power.png"),
    ("埋下伏笔", "plant_foreshadow_power.png"),
    ("大师们的援助", "engineering_dept_aid_power.png"),
    ("幸运儿的祝福", "asuna_guard_power.png"),
    ("开发秘籍", "dev_secrets_power.png"),
    ("开发者协同", "dev_green_power.png"),
    ("当心误射", "watch_out_power.png"),
    ("得道多助", "help_from_many_power.png"),
    ("循环叙事", "cyclic_narrative_power.png"),
    ("打灰机", "shmup_power.png"),
    ("扫雷", "minesweeper_power.png"),
    ("掉到二档", "fell_to_second_tier_power.png"),      # ★ 新文件（原先与「终于上一档」共用 rank_up_power.png）
    ("日复一日", "learn_by_doing_power.png"),
    ("暗黑心理学", "dark_psychology_power.png"),
    ("构想之盾", "concept_shield_power.png"),
    ("构想之矛", "concept_spear_power.png"),
    ("柚子护航", "yuzu_escort_power.png"),
    ("植物大战僵尸", "plants_next_turn_power.png"),
    ("没问题", "no_problem_power.png"),
    ("游戏王形态", "game_king_form_power.png"),
    ("火力", "firepower_power.png"),
    ("火焰附加", "flame_attach_power.png"),
    ("灵感爆发", "inspiration_power.png"),
    ("灼烧·剩余回合", "burn_turns_power.png"),
    ("灼烧", "burn_power.png"),
    ("矛与盾", "spear_shield_power.png"),               # ★ 新文件（原先与「构想之矛」共用）
    ("破势", "momentum_break_power.png"),
    ("终于上一档", "rank_up_power.png"),
    ("能量保留", "win_energy_power.png"),               # ★ 改名（原先叫 taunt_power.png）
    ("节奏游戏", "rhythm_game_power.png"),
    ("花凛的援护", "karin_finish_power.png"),
    ("蒙太奇", "montage_power.png"),
    ("虚拟女仆武器", "maid_weapon_power.png"),
    ("见识下我的实力吧", "show_my_strength_power.png"),
    ("角色扮演", "role_play_power.png"),                # ★ 新文件（原先与「跑酷」共用）
    ("贪吃蛇", "snake_game_power.png"),
    ("赖招复读", "repeat_move_power.png"),
    ("跑酷", "parkour_power.png"),
    ("重整旗鼓", "rally_again_power.png"),
    ("额外回合", "my_turn_power.png"),                  # ★ 新文件（原先与「灵感爆发」共用）
    ("骇客们的协助", "veritas_tracker_power.png"),
]

# ── 3. 遗物图标 ────────────────────────────────────────────────────────────
RELIC = [("G.Bible", "GBible.png"),
         ("旧游戏机", "OldGameConsole.png"),
         ("枯竭灵感", "DriedInspiration.png"),
         ("桌游", "BoardGameOfLife.png"),
         ("薯片", "UnfinishedChips.png"),
         ("满溢灵感", "OverflowingInspiration.png"),
         ("绿色挂饰", "GreenCharm.png"),
         ("胜利的剧本", "WinningScript.png"),
         ("镜子", "Mirror.png")]

# ── 4. 药水图标 ────────────────────────────────────────────────────────────
POTION = [("速溶咖啡", "InstantCoffee.png"),
          ("草莓牛奶", "StrawberryMilk.png"),
          ("桃味气泡水", "PeachSoda.png")]


def pick(src_dir, keys):
    """在目录里按子串找唯一文件（避免手敲“雷酱”“……”这种带特殊符号的文件名）"""
    files = [f for f in os.listdir(src_dir) if f.lower().endswith(".png")]
    out, used, miss = [], set(), []
    for k, target in keys:
        hit = [f for f in files if k in f and f not in used]
        if not hit:
            miss.append((k, "找不到源文件"))
            continue
        if len(hit) > 1:
            miss.append((k, "匹配到多个: %s" % hit))
            continue
        used.add(hit[0])
        out.append((hit[0], target))
    return out, miss, [f for f in files if f not in used]


def main():
    dry = "--dry" in sys.argv
    if not dry:
        os.makedirs(BAK, exist_ok=True)
    jobs = [("卡面修改1", os.path.join(IMG, "cards"), CARD, "卡面"),
            ("power图标成品", os.path.join(IMG, "powers"), POWER, "power 图标"),
            ("遗物成品区", os.path.join(IMG, "relics"), RELIC, "遗物图标"),
            ("药水成品区", os.path.join(IMG, "potions"), POTION, "药水图标")]
    total = 0
    for sub, dst, keys, label in jobs:
        src = os.path.join(WS, sub)
        pairs, miss, leftover = pick(src, keys)
        print("== %s：%d 个待接" % (label, len(pairs)))
        for k, why in miss:
            print("   !! %s %s" % (k, why))
        for s, t in pairs:
            sp, dp = os.path.join(src, s), os.path.join(dst, t)
            old = os.path.getsize(dp) if os.path.exists(dp) else -1
            if not dry:
                if os.path.exists(dp):
                    shutil.copy2(dp, os.path.join(BAK, t))
                shutil.copy2(sp, dp)
            print("   %-28s → %-34s %8d → %8d B" % (s, t, old, os.path.getsize(sp)))
            total += 1
        if leftover:
            print("   （目录里没被这次接入的：%s）" % "、".join(leftover))
    print()
    print("共接入 %d 张" % total, "[dry-run]" if dry else "已写入（旧图备份在 %s）"
          % os.path.relpath(BAK, ROOT))


if __name__ == "__main__":
    main()
