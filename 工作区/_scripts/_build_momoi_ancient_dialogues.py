# -*- coding: utf-8 -*-
"""Write Wang Xiaotao's custom ancient dialogues to zhs/eng ancients.json.

Group 0's first line gets the `r` suffix, so group 0 is both the VisitIndex=0
dialogue and part of the repeating pool. Later groups stay visit-specific.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"C:\Users\asus\RiderProjects\STS2 Momoi\STS2 Momoi\STS2_Momoi\localization")
CHAR = "STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER"
NEXT = {"zhs": "继续", "eng": "Continue"}

ZH = {
    "NEOW": [
        [("char", "OMAIGOTO，IT'S……"),
         ("ancient", "[sine]…不要说…那个…[/sine]"),
         ("char", "哪个？")],
        [("char", "玩爽了！再来一把！"),
         ("ancient", "[sine]…你开心…就好…[/sine]")],
        [("char", "什么粪怪！我不服！再来！"),
         ("ancient", "[sine]…菜就…多练…[/sine]")],
        [("char", "上次的开局真烂！蓝色大拖鞋你发遗物给我发好了呀！"),
         ("ancient", "[sine]…不满意…你就…roll呗…[/sine]"),
         ("ancient", "[sine]…先看看…这次的吧…[/sine]")],
    ],
    "DARV": [
        [("ancient", "你也是来爬塔的吗？需要我给你整点高级装备吗？"),
         ("char", "我去，老资历！"),
         ("ancient", "？")],
        [("char", "老资历我敬你，给我来本尘封魔典！让我取回我原本的力量！"),
         ("ancient", "让我翻翻这次有没有……")],
        [("char", "老资历发个金字塔，这把我想玩辣个了！"),
         ("ancient", "哈哈哈好久没看到有人玩辣个了，这不得把某人气死！让我找找……")],
        [("char", "垃圾佬别给我发绿帽和狗圈了……上次被你坑惨了！"),
         ("ancient", "嗨哟，那真不好意思，先看看这次的吧！")],
    ],
    "NONUPEIPE": [
        [("ancient", "哇！顶着光环的可爱女孩！我好久没见过这样年轻的访客了！"),
         ("char", "这就是尖塔最美丽的女人吗……"),
         ("ancient", "哦齁齁小姑娘嘴真甜！收下我的赐福，继续你的旅途吧！")],
        [("char", "一路蠕动过来的……要是有张神化就好了。"),
         ("ancient", "那么，来看看这次我为你准备的赐福吧！")],
        [("char", "又见到你了！真让人安心，不像隔壁某个……"),
         ("ancient", "喜欢我的慷慨无私吗？来自异世的攻略者，这次的赐福也不会让你失望的！")],
        [("ancient", "是可爱的小桃！你又来我这了，这次是什么职业？战士，盗贼还是牧师？"),
         ("char", "不，我要成为游戏王！"),
         ("ancient", "你去打败建筑师，就能成为游戏王了。"),
         ("char", "我打建筑师吗？真的假的……")],
    ],
    "OROBAS": [
        [("ancient", "顶着光环？！还带着枪！！"),
         ("char", "在我们那个地方，这些都是标配！"),
         ("ancient", "可是！枪！危险！带上这个！这个安全！")],
        [("ancient", "天使和恶魔打起来了？！打架不好！和平才好！！"),
         ("ancient", "和平是假的？谎言不好！！背叛也不好！！！")],
        [("ancient", "她贪了一座城？！怎么做到的！再说说！！后来呢？！！")],
        [("ancient", "要破坏光环？这样不好！要去救她！大家都去了？这样才对！！这样真好！！！")],
    ],
    "PAEL": [
        [("ancient", "新面孔啊……"),
         ("ancient", "拿走我的一部分，继续上路吧。")],
        [("ancient", "明知此行必死，为何仍要前行？"),
         ("char", "正因为迟早会死，当下才更要有意义的活着！")],
        [("ancient", "放松一下吧，小桃……"),
         ("char", "也好，磨刀不误砍柴工嘛。")],
        [("char", "这次有克隆吗？我抓了适合克隆的牌！"),
         ("ancient", "不知道唉，看看这块是不是？"),
         ("char", "基米！！！")],
    ],
    "TANX": [
        [("ancient", "[b]好稚嫩的女孩，但我能感受到你的潜力！快点变强！！[/b]"),
         ("char", "我会成为游戏王的！")],
        [("ancient", "[b]还在用G3吗？这枪没力气！看我给你准备的M14！满改的！[/b]"),
         ("char", "这枪有力气！")],
        [("ancient", "[b]小桃，你成为游戏王了吗？快来与我一战吧！[/b]")],
        [("ancient", "[b]王小桃，与我一战！[/b]"),
         ("char", "[i][font_size=22]小桃与坦克斯战斗了。[/font_size][/i]"),
         ("ancient", "[b]不愧是游戏王！收下这个！[/b]")],
    ],
    "TEZCATARA": [
        [("ancient", "又有客人？欢迎来到尖塔，小可爱~想吃点什么吗？")],
        [("ancient", "你是说你还有个跟你一样的妹妹？那她会来吗？你们会一起[jitter][b]战斗[/b][/jitter]吗？"),
         ("char", "看情况吧，至少作者短期是没有精力了QwQ。")],
        [("ancient", "你是说勇者牺牲自己拯救世界，而钥匙又牺牲自己拯救王女？"),
         ("ancient", "……多么崇高的牺牲……"),
         ("char", "真是一对苦命鸳鸯……")],
        [("ancient", "你是说她们齐心协力唤醒了钥匙？"),
         ("ancient", "……多么感人的重逢……")],
    ],
    "VAKUU": [
        [("ancient", "带着光环的天使？我讨厌天使……"),
         ("char", "我也讨厌恶魔……")],
        [("char", "就这几张诅咒？还没我构想塞的多呢。"),
         ("ancient", "孩子你无敌了……")],
        [("ancient", "真没想到还有无视契约的狠角，是光环在保护你吗？"),
         ("char", "是并肩同行的[aqua]伙伴[/aqua]与[aqua]勇气[/aqua]！"),
         ("ancient", "……无趣的故事。")],
        [("ancient", "听说你们的二创区不太平啊！"),
         ("char", "[i][font_size=22]瓦库大笑起来。[/font_size][/i]"),
         ("char", "……"),
         ("ancient", "流量与质量，做个选择吧。"),
         ("char", "我全都要！")],
    ],
    "THE_ARCHITECT": [
        [("char", "终于到了！塔顶的风景针不戳呀。"),
         ("ancient", "看够了吗？那就下去吧。"),
         ("char", "你最好别露血条！")],
        [("ancient", "又来了？"),
         ("char", "你血条呢！开创造模式了？"),
         ("ancient", "你应该庆幸我按两下空格不会飞起来。")],
        [("char", "又要到此为止了吗？"),
         ("ancient", "等更新吧。"),
         ("char", "服了……")],
        [("char", "那边的！我又来了！这次给你带了点小饮料！"),
         ("ancient", "谢谢，我不渴。")],
    ],
}

EN = {
    "NEOW": [
        [("char", "OMAIGOTO, IT'S..."),
         ("ancient", "[sine]...Don't say... that...[/sine]"),
         ("char", "Which one?")],
        [("char", "That was fun! One more run!"),
         ("ancient", "[sine]...As long as... you're happy...[/sine]")],
        [("char", "What a garbage elite! I refuse! Again!"),
         ("ancient", "[sine]...Skill issue... practice more...[/sine]")],
        [("char", "Last run's start was awful! Blue slippers, give me a good relic!"),
         ("ancient", "[sine]...Not satisfied... then roll...[/sine]"),
         ("ancient", "[sine]...Now look... at this one...[/sine]")],
    ],
    "DARV": [
        [("ancient", "You're climbing the Spire too? Want me to set you up with some high-tier gear?"),
         ("char", "Whoa, a veteran!"),
         ("ancient", "?")],
        [("char", "I respect you, veteran! Give me a Dusty Tome! Let me reclaim my true power!"),
         ("ancient", "Let me see if I have one this time...")],
        [("char", "Veteran, give me a Pyramid! I want to play that thing this run!"),
         ("ancient", "Hahaha, haven't seen anyone play that in ages! That'll annoy someone! Let me look...")],
        [("char", "Trash man, stop giving me the green hat and dog collar... You screwed me last time!"),
         ("ancient", "Oops, my bad! Let's see what we have this time!")],
    ],
    "NONUPEIPE": [
        [("ancient", "Oh! A cute girl with a halo! It's been so long since I saw such a young visitor!"),
         ("char", "Is this the most beautiful woman in the Spire..."),
         ("ancient", "Ohoho, what a sweet tongue! Take my blessing and continue your journey!")],
        [("char", "I crawled all the way here... If only I had an Apotheosis."),
         ("ancient", "Then let's see what blessing I prepared for you this time!")],
        [("char", "Good to see you again! It's reassuring, unlike a certain neighbor..."),
         ("ancient", "Do you like my generosity? Otherworldly walkthrough-reader, this blessing won't disappoint either!")],
        [("ancient", "It's cute little Momoi! You're back. What class this time? Warrior, thief, or priest?"),
         ("char", "No, I'm going to become the King of Games!"),
         ("ancient", "Defeat the Architect and you can become the King of Games."),
         ("char", "I have to fight the Architect? For real...?")],
    ],
    "OROBAS": [
        [("ancient", "A halo?! And a gun!!"),
         ("char", "Where I'm from, these are standard issue!"),
         ("ancient", "But! Gun! Dangerous! Take this! This is safe!")],
        [("ancient", "Angel and demon fighting?! Fighting bad! Peace good!!"),
         ("ancient", "Peace is fake? Lies bad!! Betrayal also bad!!!")],
        [("ancient", "She coveted a whole city?! How?! Tell me more!! And then?!!")],
        [("ancient", "Break the halo? That's bad! Go save her! Everyone went? That's right!! That's good!!!")],
    ],
    "PAEL": [
        [("ancient", "A new face..."),
         ("ancient", "Take a part of me and continue on your way.")],
        [("ancient", "Knowing this journey may kill you, why still go forward?"),
         ("char", "Because death is inevitable, I have to live meaningfully right now!")],
        [("ancient", "Relax for a while, Momoi..."),
         ("char", "Might as well. Sharpening the axe doesn't delay the woodcutting.")],
        [("char", "Any clones this time? I grabbed cards suited for cloning!"),
         ("ancient", "I don't know... Let's see if this piece works?"),
         ("char", "Kimi!!!")],
    ],
    "TANX": [
        [("ancient", "[b]Such a young girl, but I can feel your potential! Get stronger quickly!![/b]"),
         ("char", "I'll become the King of Games!")],
        [("ancient", "[b]Still using a G3? That gun has no power! Look at the M14 I prepared! Fully modded![/b]"),
         ("char", "This gun has power!")],
        [("ancient", "[b]Momoi, have you become the King of Games? Come fight me![/b]")],
        [("ancient", "[b]Wang Xiaotao, fight me![/b]"),
         ("char", "[i][font_size=22]Momoi fought Tanx.[/font_size][/i]"),
         ("ancient", "[b]As expected of the King of Games! Take this![/b]")],
    ],
    "TEZCATARA": [
        [("ancient", "Another guest? Welcome to the Spire, cutie~ Want something to eat?")],
        [("ancient", "You're saying you have a sister just like you? Will she come? Will you [jitter][b]fight[/b][/jitter] together?"),
         ("char", "Depends. At least the author has no energy for that in the short term QwQ.")],
        [("ancient", "You mean the hero sacrificed themself to save the world, and the key sacrificed themself to save the princess?"),
         ("ancient", "...What a noble sacrifice..."),
         ("char", "What a pair of star-crossed lovers...")],
        [("ancient", "You mean they worked together to awaken the key?"),
         ("ancient", "...What a touching reunion...")],
    ],
    "VAKUU": [
        [("ancient", "An angel with a halo? I hate angels..."),
         ("char", "I hate demons too...")],
        [("char", "Only these few curses? My Concept deck stuffs more than this."),
         ("ancient", "Child, you're invincible...")],
        [("ancient", "I never expected someone who ignores contracts. Is the halo protecting you?"),
         ("char", "It's my [aqua]companions[/aqua] walking beside me, and [aqua]courage[/aqua]!"),
         ("ancient", "...What a boring story.")],
        [("ancient", "I heard your fanwork district is in turmoil!"),
         ("char", "[i][font_size=22]Vakuu laughs.[/font_size][/i]"),
         ("char", "..."),
         ("ancient", "Traffic or quality. Choose one."),
         ("char", "I want both!")],
    ],
    "THE_ARCHITECT": [
        [("char", "Finally here! The view from the top is pretty nice."),
         ("ancient", "Looked enough? Then go down."),
         ("char", "You'd better not show a health bar!")],
        [("ancient", "Back again?"),
         ("char", "Where's your health bar?! Creative mode?"),
         ("ancient", "You should be glad I don't fly when I press space twice.")],
        [("char", "Is this where it ends again?"),
         ("ancient", "Wait for the update."),
         ("char", "Ugh...")],
        [("char", "Hey over there! I'm back! Brought you a little drink this time!"),
         ("ancient", "Thanks. I'm not thirsty.")],
    ],
}


def decorate(locale: str, ancient: str, group: int, text: str) -> str:
    """Apply the color/emphasis tags requested on top of the raw dialogue text."""
    if locale == "zhs":
        if ancient == "NONUPEIPE":
            text = text.replace("神化", "[gold]神化[/gold]")
            text = text.replace("建筑师", "[red]建筑师[/red]")
        elif ancient == "PAEL":
            text = text.replace("必死", "必[red]死[/red]")
            text = text.replace("会死", "会[red]死[/red]")
            text = text.replace("活着", "[green]活着[/green]")
            text = text.replace("克隆", "[gold]克隆[/gold]")
        elif ancient == "TEZCATARA":
            text = text.replace("钥匙", "[pink]钥匙[/pink]")
            text = text.replace("勇者", "[blue]勇者[/blue]")
            text = text.replace("王女", "[blue]王女[/blue]")
            text = text.replace("妹妹", "[green]妹妹[/green]")
        elif ancient == "DARV":
            for word in ("尘封魔典", "金字塔", "绿帽", "狗圈"):
                text = text.replace(word, f"[gold]{word}[/gold]")
        elif ancient == "OROBAS" and group == 2:
            text = text.replace("她", "[color=#000000]她[/color]")
        elif ancient == "OROBAS" and group == 3:
            text = text.replace("她", "[blue]她[/blue]")
        elif ancient == "TANX":
            text = text.replace("G3", "[pink]G3[/pink]")
            text = text.replace("M14", "[gold]M14[/gold]")
        elif ancient == "VAKUU":
            text = text.replace("诅咒", "[red]诅咒[/red]")
            text = text.replace("构想", "[gold]构想[/gold]")
            text = text.replace("流量", "[red]流量[/red]")
            text = text.replace("质量", "[green]质量[/green]")
    else:
        if ancient == "NONUPEIPE":
            text = text.replace("Apotheosis", "[gold]Apotheosis[/gold]")
            text = text.replace("the Architect", "[red]the Architect[/red]")
        elif ancient == "PAEL":
            text = text.replace("may kill you", "may [red]kill[/red] you")
            text = text.replace("death", "[red]death[/red]")
            text = text.replace("live", "[green]live[/green]")
            text = text.replace("clones", "[gold]clones[/gold]")
            text = text.replace("cloning", "[gold]cloning[/gold]")
        elif ancient == "TEZCATARA":
            text = text.replace("key", "[pink]key[/pink]")
            text = text.replace("hero", "[blue]hero[/blue]")
            text = text.replace("princess", "[blue]princess[/blue]")
            text = text.replace("sister", "[green]sister[/green]")
        elif ancient == "DARV":
            for word in ("Dusty Tome", "Pyramid", "green hat", "dog collar"):
                text = text.replace(word, f"[gold]{word}[/gold]")
        elif ancient == "OROBAS" and group == 2:
            text = text.replace("She", "[color=#000000]She[/color]")
        elif ancient == "OROBAS" and group == 3:
            text = text.replace("her", "[blue]her[/blue]")
        elif ancient == "TANX":
            text = text.replace("G3", "[pink]G3[/pink]")
            text = text.replace("M14", "[gold]M14[/gold]")
        elif ancient == "VAKUU":
            text = text.replace("curses", "[red]curses[/red]")
            text = text.replace("Concept", "[gold]Concept[/gold]")
            text = text.replace("Traffic", "[red]Traffic[/red]")
            text = text.replace("quality", "[green]quality[/green]")
    return text


def build(locale: str, data: dict) -> dict:
    out: dict[str, str] = {}
    next_text = NEXT[locale]
    for ancient, dialogues in data.items():
        for gi, lines in enumerate(dialogues):
            for li, (speaker, text) in enumerate(lines):
                # AncientDialogue.PopulateLines requires every line of a repeating
                # dialogue to carry the r suffix. All four groups repeat after their
                # visit-specific first appearance, so high-visit saves don't get stuck
                # on one group forever.
                suffix = "r"
                key = f"{ancient}.talk.{CHAR}.{gi}-{li}{suffix}.{speaker}"
                out[key] = decorate(locale, ancient, gi, text)
                if li < len(lines) - 1:
                    nxt = "红温" if locale == "zhs" and ancient == "NEOW" and gi == 2 and li == 0 else (
                        "Fuming" if locale == "eng" and ancient == "NEOW" and gi == 2 and li == 0 else next_text
                    )
                    out[f"{ancient}.talk.{CHAR}.{gi}-{li}{suffix}.next"] = nxt
            # RitsuLib's non-Architect default maps group 2/3 to visits 4/7.
            # Keep the designed four groups on visits 0/1/2/3.
            if ancient != "THE_ARCHITECT":
                out[f"{ancient}.talk.{CHAR}.{gi}-visit"] = str(gi)
    return out


def main():
    for locale, data in (("zhs", ZH), ("eng", EN)):
        path = ROOT / locale / "ancients.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = build(locale, data)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(locale, len(payload), path)


if __name__ == "__main__":
    main()
