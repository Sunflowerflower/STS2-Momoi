# -*- coding: utf-8 -*-
"""查询工具：按中文名/关键词找卡牌本地化 + 代码位置"""
import json, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
ZHS = os.path.join(MOD, "localization", "zhs")
ENG = os.path.join(MOD, "localization", "eng")

_cards = json.load(open(os.path.join(ZHS, "cards.json"), encoding="utf-8"))
_ecards = json.load(open(os.path.join(ENG, "cards.json"), encoding="utf-8"))
_pow = json.load(open(os.path.join(ZHS, "powers.json"), encoding="utf-8"))
_epow = json.load(open(os.path.join(ENG, "powers.json"), encoding="utf-8"))


def by_name(name, keys=("title", "description", "upgrade_description")):
    """按中文卡名找本地化条目"""
    out = {}
    for k, v in _cards.items():
        if k.endswith(".title") and v == name:
            base = k[:-len(".title")]
            out[base] = {kk: _cards.get(base + "." + kk) for kk in keys}
            out[base]["_eng"] = {kk: _ecards.get(base + "." + kk) for kk in keys}
    return out


def search(text, pool="cards", field=None):
    src = _cards if pool == "cards" else _pow
    return {k: v for k, v in src.items() if text in (v or "")}


def code_hits(name, extra=()):
    hits = []
    for dp, _, fs in os.walk(CODE):
        for f in fs:
            if not f.endswith(".cs"):
                continue
            p = os.path.join(dp, f)
            try:
                t = open(p, encoding="utf-8").read()
            except Exception:
                continue
            for pat in (name,) + tuple(extra):
                for m in re.finditer(re.escape(pat), t):
                    ln = t[:m.start()].count("\n") + 1
                    line = t.split("\n")[ln - 1].strip()
                    hits.append((os.path.relpath(p, CODE), ln, line[:150]))
    return hits


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "name":
        for a in sys.argv[2:]:
            print("=" * 70)
            print("卡名:", a)
            for base, v in by_name(a).items():
                print(" key:", base)
                for kk, vv in v.items():
                    print("   ", kk, "=", repr(vv))
            for h in code_hits(a):
                print("  CODE", h[0], h[1], h[2])
    elif mode == "grep":
        for k, v in search(sys.argv[2]).items():
            print(k, "=", repr(v))
    elif mode == "code":
        for h in code_hits(sys.argv[2], sys.argv[3:]):
            print(h[0], h[1], h[2])
