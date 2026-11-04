# -*- coding: utf-8 -*-
"""重新生成 _card_art_status.json / .txt（卡面缺口统计）"""
import json, os, re, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
IMGDIR = os.path.join(MOD, "images", "cards")
z = json.load(open(os.path.join(MOD, "localization", "zhs", "cards.json"), encoding="utf-8"))
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")

code = ""
for dp, _, fs in os.walk(CODE):
    for f in fs:
        if f.endswith(".cs"):
            code += open(os.path.join(dp, f), encoding="utf-8").read()

# 真实的卡类名（不能用 snake→Pascal 推：STS2_MomoiStrike 这类是带下划线的类名）
CLASSES = set(re.findall(r"class\s+([A-Za-z0-9_]+)\s*:\s*\w*ModCardTemplate", code))

def snake_upper(cls):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", cls).upper()

# 游戏那边的蛇形命名没有稳定规则（STS2_MomoiStrike → STS2_MOMOI_STRIKE），
# 所以用「去下划线 + 全小写」的归一化来配对。
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

CLS_BY_KEY = {norm(c): c for c in CLASSES}

MINIGAME = ("小游戏牌", "游戏牌")


def tag_of(cls):
    m = re.search(r"class\s+%s\b[\s\S]{0,1500}?CanonicalTags\s*=>[\s\S]{0,200}?\{([^}]*)\}" % cls, code)
    s = m.group(1) if m else ""
    if "FullGameTag" in s:
        return "游戏牌"
    if "MinigameSupport.Tag" in s:
        return "小游戏牌"
    if "IsSupportCardType" in s:
        return "支援牌"
    return "普通牌"


rows = []
seen = {}
for k, v in sorted(z.items()):
    if not k.endswith(".title") or not k.startswith("STS2_MOMOI_CARD_"):
        continue
    snake = k[:-len(".title")][len("STS2_MOMOI_CARD_"):]
    cls = CLS_BY_KEY.get(norm(snake))
    if cls is None:
        continue
    p = os.path.join(IMGDIR, cls + ".png")
    if not os.path.exists(p):
        continue
    b = open(p, "rb").read()
    md5 = hashlib.md5(b).hexdigest()
    seen.setdefault(md5, []).append(cls)
    rows.append(dict(cls=cls, cn=v, size=len(b), kind=None, tag=tag_of(cls), edit=False, md5=md5))

for r in rows:
    n = len(seen[r["md5"]])
    if r["size"] < 4096:
        r["kind"] = "纯色小占位"
    elif n > 1:
        r["kind"] = "共用占位图"
    else:
        r["kind"] = "真实成品"
    r["edit"] = (n > 1 and seen[r["md5"]][0] == r["cls"]) or r["kind"] == "真实成品"

summary = {}
for r in rows:
    summary[r["kind"]] = summary.get(r["kind"], 0) + 1
shared = [[md5, len(cls), cls[0], next(r["size"] for r in rows if r["md5"] == md5)]
          for md5, cls in seen.items() if len(cls) > 1]
need = [r for r in rows if r["kind"] != "真实成品"]
for r in rows:
    r.pop("md5", None)

out = dict(total=len(rows), summary=summary, shared_groups=shared,
           need_ai=[r for r in need if r["tag"] not in MINIGAME],
           no_ai=[r for r in need if r["tag"] in MINIGAME],
           rows=rows)
json.dump(out, open(os.path.join(ROOT, "工作区", "_data", "_card_art_status.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

L = ["总卡类(有PNG): %d" % len(rows)]
for k in ("真实成品", "共用占位图", "纯色小占位"):
    L.append("  %s: %d" % (k, summary.get(k, 0)))
L.append("")
L.append("共用的重复图组:")
if shared:
    for md5, n, ex, sz in shared:
        L.append("  [%d 张 / %d B] 例: %s" % (n, sz, ex))
else:
    L.append("  （无）")
L.append("")
L.append("================ 待做 AI 卡面 %d 张 ================" % len(out["need_ai"]))
for r in out["need_ai"]:
    L.append("  %-22s %-22s [%s] %9d B" % (r["cn"], r["cls"], r["tag"], r["size"]))
L.append("")
L.append("================ 小游戏牌/游戏牌（按约定不做 AI 卡面）%d 张 ================" % len(out["no_ai"]))
for r in out["no_ai"]:
    L.append("  %-22s %-22s [%s] %9d B" % (r["cn"], r["cls"], r["tag"], r["size"]))
open(os.path.join(ROOT, "工作区", "_data", "_card_art_status.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
