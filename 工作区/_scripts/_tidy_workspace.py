# -*- coding: utf-8 -*-
"""整理仓库：把散落的 log / json / py 归到分类目录（只移动，不删除）

用法：py -3 _tidy_workspace.py [--dry]
"""
import os, re, shutil, sys, datetime

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
WS = os.path.join(ROOT, "工作区")
PROJ = os.path.join(ROOT, "STS2 Momoi")

# (源目录, 目标目录, 匹配规则)
MOVES = [
    # ── 仓库根：历史构建日志 / 批次报告
    (ROOT, os.path.join(ROOT, "_archive", "build_logs"), r"^_build_.*\.log$"),
    (ROOT, os.path.join(ROOT, "_archive", "batch_reports"),
     r"^(_apply_batch\d+_report\.json|_batch\d+_contact_sheet\.jpg|_check_titfortat\.jpg|_vanilla_gold_terms\.json)$"),
    (ROOT, os.path.join(WS, "_data"), r"^_card_art_status\.(json|txt)$"),

    # ── 工作区：脚本 / 数据 / 备份
    (WS, os.path.join(WS, "_scripts"), r"^(.*\.py)$"),
    (WS, os.path.join(WS, "_data"),
     r"^(_cards_full\.json|_idx_cards\.json|_idx_powers\.json|_relic_potion_dump\.txt|_xlsx_dump\.json|_xlsx_vs_json\.txt|_power_icon_inventory\.json|_card_index\.txt)$"),
    (WS, os.path.join(WS, "_docs"), r"^(_待做图标清单\.md|STS2_Momoi_迁移文档\.md)$"),

    # ── 工程内：一次性补丁脚本 / 旧文档副本
    (PROJ, os.path.join(PROJ, "_tools"),
     r"^(_patch_[abc]\.py|_verify6\.py|_xlsx_update7\.py|_fix_batch_a\.py|_art_map\.json)$"),
    (PROJ, os.path.join(ROOT, "_archive", "old_docs"), r"^(STS2_Momoi_迁移文档\.md)$"),
]


def main():
    dry = "--dry" in sys.argv
    log = []
    for src_dir, dst_dir, pat in MOVES:
        if not os.path.isdir(src_dir):
            continue
        rx = re.compile(pat)
        names = [n for n in sorted(os.listdir(src_dir))
                 if rx.match(n) and os.path.isfile(os.path.join(src_dir, n))]
        if not names:
            continue
        if not dry:
            os.makedirs(dst_dir, exist_ok=True)
        for n in names:
            s, d = os.path.join(src_dir, n), os.path.join(dst_dir, n)
            if os.path.exists(d):
                print("  跳过（目标已存在）:", n)
                continue
            if not dry:
                shutil.move(s, d)
            log.append((os.path.relpath(s, ROOT), os.path.relpath(d, ROOT)))
        print("%-42s -> %-46s  %d 个" % (os.path.relpath(src_dir, ROOT),
                                        os.path.relpath(dst_dir, ROOT), len(names)))

    # 工作区的三个 _backup 目录合并到 _backup/
    for sub in ("_xlsx_backup", "_dump_backup", "_cardart_backup9"):
        s = os.path.join(WS, sub)
        if os.path.isdir(s):
            d = os.path.join(WS, "_backup", sub)
            if not dry:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                if os.path.exists(d):
                    for f in os.listdir(s):
                        shutil.move(os.path.join(s, f), os.path.join(d, f))
                    os.rmdir(s)
                else:
                    shutil.move(s, d)
            print("%-42s -> %-46s  (目录)" % (os.path.relpath(s, ROOT), os.path.relpath(d, ROOT)))

    if not dry and log:
        mf = os.path.join(ROOT, "_archive", "move_manifest_%s.txt"
                          % datetime.datetime.now().strftime("%Y%m%d_%H%M"))
        os.makedirs(os.path.dirname(mf), exist_ok=True)
        open(mf, "w", encoding="utf-8").write(
            "\n".join("%s\t->\t%s" % p for p in log) + "\n")
        print("移动清单 ->", os.path.relpath(mf, ROOT))
    print("[dry-run]" if dry else "整理完成")


if __name__ == "__main__":
    main()
