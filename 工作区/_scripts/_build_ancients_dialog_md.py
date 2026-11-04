# -*- coding: utf-8 -*-
"""Build a readable, ancient-by-ancient dialogue reference from zhs/ancients.json."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

SRC = Path(r"C:\Users\asus\Desktop\Slay the Spire 2\localization\zhs\ancients.json")
OUT = Path(r"C:\Users\asus\RiderProjects\STS2 Momoi\工作区\_docs\_先古之民对话整理.md")

ANC_ORDER = ["DARV", "NEOW", "NONUPEIPE", "OROBAS", "PAEL", "TANX", "TEZCATARA", "THE_ARCHITECT", "VAKUU"]
CHAR_ORDER = ["ANY", "IRONCLAD", "SILENT", "DEFECT", "NECROBINDER", "REGENT"]
CHAR_NAMES = {
    "ANY": "通用 / ANY",
    "IRONCLAD": "铁甲战士",
    "SILENT": "静默猎手",
    "DEFECT": "故障机器人",
    "NECROBINDER": "亡灵契约师",
    "REGENT": "储君",
}
SPEAKER = {
    "ancient": "先古",
    "char": "角色",
}

TAG_BOLD = re.compile(r"\[b\](.*?)\[/b\]", re.S)
TAG_ITALIC = re.compile(r"\[i\](.*?)\[/i\]", re.S)
TAG_GOLD = re.compile(r"\[gold\](.*?)\[/gold\]", re.S)
TAG_ANY = re.compile(r"\[[^\]]+\]")
NEXT_RE = re.compile(r"^([A-Z_]+)\.talk\.([A-Z_]+)\.(\d+)-(\d+r?)\.(ancient|char|next)$")
FIRST_RE = re.compile(r"^([A-Z_]+)\.talk\.firstVisitEver\.(\d+)-(\d+r?)\.(ancient|char|next)$")


def clean(text: str, ancient: str) -> str:
    text = TAG_BOLD.sub(r"**\1**", text)
    text = TAG_ITALIC.sub(r"*\1*", text)
    text = TAG_GOLD.sub(r"**\1**", text)
    text = TAG_ANY.sub("", text)
    text = text.replace("\n", "\n").strip()
    if ancient == "NEOW" and text:
        text = "（低语）" + text
    return text


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    groups = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
    # ancient -> char -> conversation major -> minor -> suffix
    first_visit = defaultdict(lambda: defaultdict(str))
    titles = {}
    epithets = {}
    losses = {}
    all_keys = list(data)
    for key, value in data.items():
        if not isinstance(value, str):
            continue
        m = NEXT_RE.match(key)
        if m:
            anc, ch, major, minor, suffix = m.groups()
            groups[anc][ch][int(major)][minor][suffix] = value
            continue
        if key.endswith(".title"):
            titles[key.split(".")[0]] = value
        elif key.endswith(".epithet"):
            epithets[key.split(".")[0]] = value
        elif key.endswith(".loss"):
            losses[key.split(".")[0]] = value
        elif (fm := FIRST_RE.match(key)):
            anc, major, minor, suffix = fm.groups()
            first_visit[anc][key] = value

    lines_count = 0
    for anc in groups:
        for ch in groups[anc]:
            for major in groups[anc][ch]:
                for minor in groups[anc][ch][major]:
                    for suffix in ("ancient", "char"):
                        if groups[anc][ch][major][minor].get(suffix):
                            lines_count += 1
    for anc in first_visit:
        for key in first_visit[anc]:
            if key.endswith((".ancient", ".char")):
                lines_count += 1

    out = []
    out.append("# 先古之民对话整理\n")
    out.append("> 来源：`C:\\Users\\asus\\Desktop\\Slay the Spire 2\\localization\\zhs\\ancients.json`  ")
    out.append("> 用途：给王小桃与先古之民 / 建筑师的对话写作做参考。  ")
    out.append("> 整理：按先古之民 → 角色 → 对话组；保留全部台词，去除游戏富文本标签；`next` 只作为推进按钮记录。\n")
    out.append("## 速览\n")
    out.append("| 先古 | 称号 | 可对话角色 | 台词数 |")
    out.append("|---|---|---|---:|")
    for anc in ANC_ORDER:
        if anc not in groups and anc not in titles:
            continue
        chars = [CHAR_NAMES.get(c, c) for c in CHAR_ORDER if c in groups.get(anc, {})]
        n = sum(1 for ch in groups.get(anc, {}).values() for major in ch.values() for minor in major.values()
                for s in ("ancient", "char") if minor.get(s))
        n += sum(1 for key in first_visit.get(anc, {}) if key.endswith((".ancient", ".char")))
        out.append(f"| {titles.get(anc, anc)}（`{anc}`） | {epithets.get(anc, '—')} | {'、'.join(chars) or '—'} | {n} |")
    out.append(f"\n> 共 **{len([a for a in ANC_ORDER if a in groups or a in titles])}** 位先古/建筑师，**{lines_count}** 条有文本的台词；不含 `ERROR` / `PROCEED` 等非对话键。\n")

    out.append("## 阅读说明\n")
    out.append("- `【先古】`/`【建筑师】` 是先古之民/建筑师的台词，`【角色】` 是玩家角色或旁白式动作。")
    out.append("- 对话组编号沿用原键，例如 `2-0` / `2-1` 是同一组的先后节点；组号通常对应不同轮次/路线。")
    out.append("- `ANY` 是不依赖具体角色的通用对话；`firstVisitEver` 是首次见到该先古时的固定台词。")
    out.append("- 按钮文案（`next`）统一放在每组末尾，便于还原原文节奏；它本身不是台词。")
    out.append("- 涅奥的台词原文带 `[sine]`，整理为“（低语）”前缀；其余 `[b]`/`[i]`/`[gold]` 已转成 Markdown 强调。\n")
    out.append("- `OROBAS` 的 JSON 官方 title 是「欧洛巴斯」；模组/旧文档里的「奥罗巴斯」指同一位先古。")


    out.append("## 写作速记（先看这一段）\n")
    out.append("这些是**从台词里归纳的语气/关系**，不是游戏原文；逐句原文在后面。\n")
    out.append("### 达弗：旧物收藏家式的热络商人\n")
    out.append("记得每个角色过去的装备/战利品（铁甲战士的重刃、猎手的战利品、机器人的朋友残骸、亡灵契约师的书），用“来看看我的收藏”包装交易；会把建筑师当作修复/线索的下一站。适合写他一边翻旧货一边用熟人语气套近乎。\n")
    out.append("### 涅奥：断续低语的复生母亲\n")
    out.append("台词大量省略号、低语和“醒来/重铸/祝福”；对铁甲战士谈愤怒与记忆，对静默猎手谈家族与认同，对亡灵契约师直接结盟杀建筑师，对储君则明显偏爱。她是“复活—再挑战”循环的温柔/冷酷源头。\n")
    out.append("### 诺奴佩普：挑剔又爱美的机缘化身\n")
    out.append("关注衣装、仆从、审美和“配不配得上赐福”；对铁甲战士/猎手/储君用勇士、刺客、王室访客等身份称呼，对故障机器人则对“建筑师的造物”产生兴趣。她喜欢有能力的人，也会提醒亡灵契约师别再杀自己的护卫。\n")
    out.append("### 欧洛巴斯：孩子气、跳跃、反暴力的活体虹光\n")
    out.append("短句、重复、感叹号密集；喜欢闪亮东西和故事，怕感染/暴力，认为“建筑师不坏、可以聊聊”，同时明确说瓦库很坏。对储君是头号粉丝式的追故事。适合写插话、打岔、突然兴奋。\n")
    out.append("### 佩尔：沉睡的融化巨龙\n")
    out.append("关键词是睡眠、梦、平静、血肉、父亲；给角色“我的一部分”来减轻痛苦，反对复仇和暴力，但会把“父亲”与建筑师/自由联系在一起。语气慢、困、温柔，偶尔说出让人不安的家族关系。\n")
    out.append("### 坦克斯：直来直去的嵌合兽之王\n")
    out.append("几乎所有话题都能拐到“武器/战斗/变强”；对强者热情，对弱小者说“有潜力”，对橙色储君有喜剧式执着。适合写大声、短句、动手先于思考的对话。\n")
    out.append("### 特兹卡塔拉：慵懒危险的饲火者\n")
    out.append("称人“亲爱的/小可爱”，把燃烧、疾病、禁忌、书和“杀建筑师”说得像闲聊；对亡灵契约师的书/火焰尤其感兴趣。温柔的语气和危险内容形成反差。\n")
    out.append("### 建筑师：冷淡、疲惫、维持秩序\n")
    out.append("对铁甲战士是“怜悯/回塔底”，对亡灵契约师的复仇是“敬谢不敏/无法改变过去/维持秩序”，对故障机器人是轻蔑，对储君嫌聒噪。台词短、冷、带审判感；关键不是咆哮，而是把伤害说成必要秩序。\n")
    out.append("### 瓦库：第一个恶魔与契约商\n")
    out.append("谈交易、代价、复仇、傀儡、部落和“你还会回来”；擅长用角色的朋友/亲人/仇恨做筹码，和欧洛巴斯互相拆台，也把建筑师当作可利用的目标。语气嘲弄、耐心、带笑意。\n")
    out.append("### 给王小桃的切入点（脑洞，不是原文）\n")
    out.append("- 小桃是“游戏开发部编剧、爱玩给木”：可以把先古的宏大叙事翻译成游戏开发/剧本/存档/读档梗，但不要让她只会吐槽，保留她认真写故事的底色。\n")
    out.append("- 达弗→旧游戏卡带/开发机收藏；诺奴佩普→角色皮肤/审美；坦克斯→对战平衡/武器；特兹卡塔拉→禁忌题材/熬夜上火；欧洛巴斯→故事和亮闪闪的素材；佩尔→睡眠/做梦/灵感；涅奥→重开一局/存档；瓦库→用户协议/氪金契约；建筑师→删档/版本号/创作者权限。\n")
    out.append("- 共同母题：建筑师—涅奥—瓦库的三角、交易与代价、角色被反复复活/重来、对“故事能否改变结局”的执念。\n")
    out.append("")
    n = 0
    for anc in ANC_ORDER:
        if anc not in groups and anc not in titles:
            continue
        n += 1
        title = titles.get(anc, anc)
        out.append(f"## {n}. {title}（`{anc}`）\n")
        out.append(f"**称号：** {epithets.get(anc, '—')}  ")
        if anc in losses:
            out.append(f"**失败/损失文本：** {clean(losses[anc], anc)}  ")
        out.append("")
        # first visit
        if anc in first_visit:
            out.append("### 初次见面（firstVisitEver）\n")
            for key in sorted(first_visit[anc], key=lambda k: (int(re.search(r"\.(\d+)-(\d+)", k).group(1)), int(re.search(r"\.(\d+)-(\d+)", k).group(2)), k)):
                val = first_visit[anc][key]
                suffix = key.rsplit(".", 1)[-1]
                if suffix == "next":
                    continue
                label = ("建筑师" if anc == "THE_ARCHITECT" else "先古") if suffix == "ancient" else "角色"
                out.append(f"> **【{label}】** {clean(val, anc)}\n")
            out.append("")
        for ch in CHAR_ORDER:
            if ch not in groups.get(anc, {}):
                continue
            out.append(f"### {CHAR_NAMES.get(ch, ch)}\n")
            for major in sorted(groups[anc][ch]):
                out.append(f"#### 对话组 {major}\n")
                nodes = groups[anc][ch][major]
                nexts = []
                for minor in sorted(nodes, key=lambda x: (int(re.match(r"\d+", x).group(0)), x.endswith("r"))):
                    node = nodes[minor]
                    ancient_line = node.get("ancient")
                    char_line = node.get("char")
                    if ancient_line:
                        ancient_label = "建筑师" if anc == "THE_ARCHITECT" else "先古"
                        out.append(f"> **【{ancient_label}】** {clean(ancient_line, anc)}\n")
                    if char_line:
                        out.append(f"> **【角色】** {clean(char_line, anc)}\n")
                    if node.get("next"):
                        nexts.append(clean(node["next"], anc).replace("（低语）", ""))
                    if not ancient_line and not char_line and node.get("next"):
                        out.append("> （本节点只有推进按钮，没有台词）\n")
                if nexts:
                    out.append("> 推进按钮：" + " → ".join(nexts) + "\n")
                out.append("")
        out.append("---\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out), encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes), ancients={len([a for a in ANC_ORDER if a in groups or a in titles])}, lines={lines_count}")


if __name__ == "__main__":
    main()
