# -*- coding: utf-8 -*-
"""打一个「本地 mod」发布包：把部署目录里的 STS2_Momoi/ 整个压成 zip（顶层就是该文件夹）。

按 QA 的要求：
1. 校验 mods/STS2_Momoi/ 里 {id}.dll、{id}.pck、{id}.json 三个文件都在，且文件名与清单 id 完全一致；
2. 校验清单的 has_dll / has_pck / dependencies；
3. zip 顶层必须是 `STS2_Momoi/`（玩家解压到 Slay the Spire 2/mods/ 下即可）。

产物：工作区/发布包/STS2_Momoi_v<版本>.zip
"""
import json
import os
import shutil
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")

MODS = r"D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods"
SRC = os.path.join(MODS, "STS2_Momoi")
OUT_DIR = r"C:\Users\asus\RiderProjects\STS2 Momoi\工作区\发布包"

README = """游戏王小桃（STS2_Momoi）本地安装说明
====================================

1) 先安装依赖：RitsuLib（工坊订阅，或把 STS2-RitsuLib 放进 mods/）。
2) 把本压缩包里的整个 `STS2_Momoi` 文件夹解压到：
       Slay the Spire 2/mods/
   解压后目录应当是：
       Slay the Spire 2/mods/STS2_Momoi/STS2_Momoi.json
       Slay the Spire 2/mods/STS2_Momoi/STS2_Momoi.dll
       Slay the Spire 2/mods/STS2_Momoi/STS2_Momoi.pck
3) 启动游戏，首次运行会弹出「启用模组」提示，允许即可。
4) 游戏内：主菜单 → 模组设置 → 游戏王小桃，可以打开日志目录（报错时把 godot.log 一起发出来）。

注意：
* 本包是「本地版」。如果以后从创意工坊订阅同一个 mod（id 相同），游戏会禁用版本号更低的那个，
  建议同时存在时让两边版本号一致，或者临时移走其中一个。
* 联机时两端必须用同一份文件。
"""


def main() -> int:
    if not os.path.isdir(SRC):
        print("[FAIL] 找不到部署目录：" + SRC)
        return 1

    manifest_path = os.path.join(SRC, "STS2_Momoi.json")
    if not os.path.isfile(manifest_path):
        print("[FAIL] 缺清单：" + manifest_path)
        return 1

    manifest = json.load(open(manifest_path, encoding="utf-8-sig"))
    mod_id = manifest["id"]
    version = manifest.get("version", "0.0.0")

    # 1) 文件名必须与 id 一致
    required = [f"{mod_id}.dll", f"{mod_id}.pck", f"{mod_id}.json"]
    missing = [f for f in required if not os.path.isfile(os.path.join(SRC, f))]
    if missing:
        print("[FAIL] 部署目录缺少文件：" + ", ".join(missing))
        return 1
    print("[OK] 三个文件齐全：" + ", ".join(required))

    # 2) 清单字段
    if not manifest.get("has_dll") or not manifest.get("has_pck"):
        print("[FAIL] 清单 has_dll / has_pck 必须都是 true")
        return 1
    deps = [d.get("id") for d in manifest.get("dependencies", [])]
    if "STS2-RitsuLib" not in deps:
        print("[FAIL] 清单 dependencies 里没有 STS2-RitsuLib")
        return 1
    print(f"[OK] 清单：{manifest.get('name')} v{version} / has_dll+has_pck / deps={deps}")

    # 3) 打包（中间用临时目录塞一个 README.txt，不污染部署目录）
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, f"STS2_Momoi_v{version}.zip")
    stage = os.path.join(OUT_DIR, "_stage", mod_id)
    if os.path.isdir(os.path.join(OUT_DIR, "_stage")):
        shutil.rmtree(os.path.join(OUT_DIR, "_stage"))
    os.makedirs(stage, exist_ok=True)
    for f in required:
        shutil.copy2(os.path.join(SRC, f), os.path.join(stage, f))
    with open(os.path.join(stage, "README.txt"), "w", encoding="utf-8-sig") as fh:
        fh.write(README)

    if os.path.exists(out):
        os.remove(out)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, _dirs, files in os.walk(stage):
            for name in sorted(files):
                full = os.path.join(root, name)
                # zip 内路径以 `STS2_Momoi/` 开头
                arc = os.path.join(mod_id, os.path.relpath(full, stage))
                z.write(full, arc.replace("\\", "/"))

    shutil.rmtree(os.path.join(OUT_DIR, "_stage"))
    size = os.path.getsize(out)
    print(f"[DONE] {out}  ({size/1024/1024:.1f} MB)")

    with zipfile.ZipFile(out) as z:
        names = z.namelist()
        print("  顶层：", sorted({n.split('/')[0] for n in names}))
        for n in names:
            print("   ", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
