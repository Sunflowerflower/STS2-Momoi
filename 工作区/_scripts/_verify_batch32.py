# -*- coding: utf-8 -*-
"""批次32 自检：王小桃身份/头像/能量/多人手势/休息处镜像/文本与卡框参考。"""
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"C:\Users\asus\RiderProjects\STS2 Momoi"
MOD = os.path.join(ROOT, "STS2 Momoi", "STS2_Momoi")
CODE = os.path.join(ROOT, "STS2 Momoi", "STS2 MomoiCode")
IMG = os.path.join(MOD, "images", "characters")
SCN = os.path.join(MOD, "scenes", "characters")
PCK = r"D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi\STS2_Momoi.pck"
DLL = r"D:\SteamLibrary\steamapps\common\Slay the Spire 2\mods\STS2_Momoi\STS2_Momoi.dll"

ok = fail = 0


def chk(cond, label, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label + ("  << " + str(detail) if detail else ""))


def read(p):
    return open(p, encoding="utf-8").read()


def png_size(p):
    with open(p, "rb") as f:
        h = f.read(33)
    if h[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", h[16:24])


def pck_names(path):
    f = open(path, "rb")
    h = f.read(40)
    _, _ = struct.unpack_from("<QQ", h, 24)
    _, do = struct.unpack_from("<QQ", h, 24)
    f.seek(do)
    n = struct.unpack("<I", f.read(4))[0]
    out = []
    for _ in range(n):
        l = struct.unpack("<I", f.read(4))[0]
        out.append(f.read(l).decode("utf-8", "replace").rstrip("\x00"))
        f.read(16)
        f.read(16)
        f.read(4)
    return out


char = read(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs"))
pool = read(os.path.join(CODE, "Characters", "STS2 MomoiCardPool.cs"))
rest = read(os.path.join(SCN, "STS2_Momoi_rest_site.tscn"))
energy = read(os.path.join(SCN, "STS2_Momoi_energy_counter.tscn"))
zh = json.load(open(os.path.join(MOD, "localization", "zhs", "characters.json"), encoding="utf-8"))
en = json.load(open(os.path.join(MOD, "localization", "eng", "characters.json"), encoding="utf-8"))
names = pck_names(PCK)

print("== 1. 名字 / 血量 / 选人文案 ==")
chk("StartingHp => 72" in char, "初始生命 72")
chk("public static readonly Color MomoiPink" in char, "MomoiPink 常量")
chk("NameColor => MomoiPink" in char, "名字颜色桃红")
chk('MomoiPink = new("D95C97")' in char, "数字颜色加深为 #D95C97")
chk("EnergyLabelOutlineColor => MomoiPink" in char, "能量数字描边桃红")
chk("EnergyOutlineColor => STS2_MomoiCharacter.MomoiPink" in pool, "卡池能量描边桃红")
chk(zh.get("STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.title") == "王小桃", "中文标题")
chk(zh.get("STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.description") == "游戏开发部的编剧，爱玩给木。\n或许她真的能成为游戏王。", "中文描述两行")
chk(zh.get("STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.flavor") == "或许她真的能成为游戏王。", "中文风味")
chk(en.get("STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.title") == "Momoi", "英文标题 Momoi")

print("== 2. 左上角头像 ==")
icon = os.path.join(SCN, "STS2_Momoi_icon.tscn")
chk(os.path.isfile(icon), "STS2_Momoi_icon.tscn 存在")
chk("STS2_Momoi_character_icon.png" in read(icon) if os.path.isfile(icon) else False, "图标场景引用像素小桃")
chk("IconPath: $\"{SceneRoot}/STS2_Momoi_icon.tscn\"" in char, "CharacterUiAssetSet.IconPath 已接")
chk(any("STS2_Momoi_icon.scn" in n for n in names), "PCK 含图标场景")

print("== 3. 能量：24 / 256 / 静态表盘 ==")
chk(png_size(os.path.join(IMG, "energy_text.png")) == (24, 24), "小能量 24×24")
chk(png_size(os.path.join(IMG, "energy_big.png")) == (256, 256), "大能量 256×256")
chk("energy_big.png" in energy and "RotationLayers" in energy, "表盘引用大图 + 保留 RotationLayers")
chk(energy.count("Layer1") == 1 and "Layer2" not in energy and "Layer3" not in energy, "表盘只有单张 Layer1")
chk(not os.path.exists(os.path.join(IMG, "STS2_Momoi_energy_orb_layer_1.png")), "旧 5 层球已删")
chk(any("energy_big.png-" in n for n in names), "PCK 含大能量 ctex")
chk("font_outline_color = Color(0.8509804, 0.3607843, 0.5921569" in energy, "表盘 Label 默认深桃红描边")

print("== 4. 多人手势 4 张 422×1200 ==")
for n in ("point", "rock", "paper", "scissors"):
    p = os.path.join(IMG, f"STS2_Momoi_arm_{n}.png")
    chk(os.path.isfile(p) and png_size(p) == (422, 1200), f"arm_{n} 422×1200", png_size(p) if os.path.isfile(p) else None)
chk("Multiplayer: new CharacterMultiplayerAssetSet(" in char, "AssetProfile.Multiplayer 已填")
chk("STS2_Momoi_arm_point.png" in char and "STS2_Momoi_arm_scissors.png" in char, "4 条手势路径")
chk(sum(1 for n in names if "STS2_Momoi_arm_" in n and n.endswith(".ctex")) == 4, "PCK 含 4 张手势 ctex")

print("== 5. 休息处右半场镜像 ==")
chk("parent=\"ControlRoot\"" in rest.split('name="Visuals"')[1][:80], "Visuals 已移进 ControlRoot")
chk("scale = Vector2(0.65, 0.65)" in rest, "Visuals scale 0.65")
chk("position = Vector2(10, 42)" in rest, "Visuals position (10,42)")
chk("offset_bottom = 245.0" in rest, "hitbox 覆盖躺姿")

print("== 6. PCK / 清理 / 参考文档 ==")
chk(os.path.getsize(DLL) >= 455_000, "DLL >=455KB", os.path.getsize(DLL))
chk(40_000_000 <= os.path.getsize(PCK) <= 80_000_000, "PCK 已按贴图规则压缩（约 55MB）", os.path.getsize(PCK))
chk(len(names) >= 950, "PCK 条目 >=950", len(names))
chk(not any("STS2_Momoi_energy_orb_layer" in n for n in names), "PCK 没有旧能量球")
chk(not any(n.endswith("cue/attack.png") or n.endswith("cue/cast.png") for n in names), "PCK 没有旧 attack/cast")
chk(not any("STS2_Momoi_character_select_bg.tscn" in n for n in names), "PCK 没有旧选人背景")
chk(os.path.isfile(os.path.join(ROOT, "工作区", "_docs", "_文本参考_王小桃.md")), "文本参考文档")
chk(os.path.isfile(os.path.join(ROOT, "工作区", "_docs", "_卡框参考.md")), "卡框参考文档")
chk(os.path.isfile(os.path.join(ROOT, "工作区", "编辑区", "人物", "_work", "card_frame_reference.png")), "卡框参考图")
chk(os.path.isfile(os.path.join(MOD, "shaders", "momoi_card_frame_gradient.gdshader")), "卡框渐变 shader")
chk(os.path.isfile(os.path.join(MOD, "materials", "momoi_card_frame_gradient.tres")), "卡框渐变材质")
chk("momoi_card_frame_gradient.tres" in pool, "卡池使用渐变材质")
shader = read(os.path.join(MOD, "shaders", "momoi_card_frame_gradient.gdshader"))
chk("mix(pink, blue" in shader and "body" in shader, "粉蓝渐变 + 正文区压暗")
chk("0.93, 0.97" in shader and "bodyTint" in shader, "外框全渐变 + 底部外框不压暗")
chk("Vfx: new CharacterVfxAssetSet(" in char and "card_trail_ironclad.tscn" in char, "卡牌拖尾使用原版场景")
chk("8FB8FF" in char and "F5A9C9" in char, "卡牌拖尾粉蓝配色（外蓝内粉）")
energy_txt = energy
chk("offset_left = -4.0" in energy_txt and "offset_top = -2.0" in energy_txt, "战斗表盘左移/上移")
from PIL import Image
import numpy as np
a = np.array(Image.open(os.path.join(IMG, "energy_big.png")).convert("RGBA"))
ys, xs = np.where(a[..., 3] > 8)
chk(int(ys.min()) <= 20, "大能量图标上移（内容 top <=20）", int(ys.min()))
chk(os.path.isfile(os.path.join(CODE, "Settings", "MomoiSettings.cs")), "设置存储文件")
settings = read(os.path.join(CODE, "Settings", "MomoiSettings.cs"))
chk("PhilosopherPool" in settings and "SeaGlassPool" in settings, "两个设置字段")
chk("RegisterModSettings" in settings, "设置页注册")
chk(open(os.path.join(CODE, "Entry.cs"), encoding="utf-8").read().count("patcher.RegisterPatch") >= 24,
    "Entry 补丁数 >= 24（后续批次会继续追加，不锁死数字；当前 %d）"
    % open(os.path.join(CODE, "Entry.cs"), encoding="utf-8").read().count("patcher.RegisterPatch"))
chk(os.path.isfile(os.path.join(CODE, "Patches", "MomoiPhilosopherPoolPatch.cs")), "色彩哲学家补丁")
chk(os.path.isfile(os.path.join(CODE, "Patches", "MomoiSeaGlassPoolPatch.cs")), "海玻璃补丁")
chk(os.path.isfile(os.path.join(CODE, "Patches", "MomoiCardFrameMaterialPatch.cs")), "卡框材质补丁")
chk(os.path.isfile(os.path.join(CODE, "Patches", "MomoiCardFrameVisualPatch.cs")), "NCard 卡框兜底补丁")
chk(os.path.isfile(os.path.join(CODE, "Patches", "MomoiLowHpPatch.cs")), "残血控制器补丁")
settings = read(os.path.join(CODE, "Settings", "MomoiSettings.cs"))
# 2026-10-25：残血 BGM 音量项已被移除/重构（现在走 low_hp idle 帧 + MomoiLowHpPatch），改成断言实际实现。
chk(os.path.isfile(os.path.join(CODE, "Patches", "MomoiLowHpPatch.cs"))
    and os.path.isfile(os.path.join(MOD, "images", "characters", "cue", "low_hp.png")), "残血 low_hp 帧 + 补丁")
lowhp_patch = read(os.path.join(CODE, "Patches", "MomoiLowHpPatch.cs"))
chk("StopFadeSeconds" in lowhp_patch and "entity.IsDead" in lowhp_patch, "死亡 2 秒淡出")
chk("TheArchitectEventEncounter" in lowhp_patch, "建筑师对话场景不播残血 BGM")
zh_ancient = json.loads(read(os.path.join(MOD, "localization", "zhs", "ancients.json")))
eng_ancient = json.loads(read(os.path.join(MOD, "localization", "eng", "ancients.json")))
chk(len(zh_ancient) == 166 and len(eng_ancient) == 166, "先古对话 zhs/eng 各 166 键")
chk(all("r." in k for k in zh_ancient if k.endswith((".ancient", ".char"))) and
    sum(1 for k in zh_ancient if k.endswith("-visit")) == 32, "所有对话行 r + visit 覆盖")
chk("[b]" in zh_ancient["TANX.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.0-0r.ancient"] and
    "[i][font_size=22]小桃与坦克斯战斗了。[/font_size][/i]" in zh_ancient["TANX.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.3-1r.char"], "坦克斯加粗/斜体旁白")
chk("[jitter][b]战斗[/b][/jitter]" in zh_ancient["TEZCATARA.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.1-0r.ancient"] and
    "[aqua]伙伴[/aqua]" in zh_ancient["VAKUU.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.2-1r.char"], "特兹卡塔拉抖动/瓦库青色")
chk("[gold]神化[/gold]" in zh_ancient["NONUPEIPE.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.1-0r.char"] and
    "[red]建筑师[/red]" in zh_ancient["NONUPEIPE.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.3-2r.ancient"], "诺奴佩普 金色/红色")
chk("必[red]死[/red]" in zh_ancient["PAEL.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.1-0r.ancient"] and
    "[green]活着[/green]" in zh_ancient["PAEL.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.1-1r.char"] and
    "[gold]克隆[/gold]" in zh_ancient["PAEL.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.3-0r.char"], "佩尔 红/绿/金")
chk("[pink]钥匙[/pink]" in zh_ancient["TEZCATARA.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.2-0r.ancient"] and
    "[blue]勇者[/blue]" in zh_ancient["TEZCATARA.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.2-0r.ancient"] and
    "[blue]王女[/blue]" in zh_ancient["TEZCATARA.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.2-0r.ancient"] and
    "[green]妹妹[/green]" in zh_ancient["TEZCATARA.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.1-0r.ancient"], "特兹卡塔拉 粉/蓝/绿")
chk("[gold]尘封魔典[/gold]" in zh_ancient["DARV.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.1-0r.char"] and
    "[gold]金字塔[/gold]" in zh_ancient["DARV.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.2-0r.char"] and
    "[gold]绿帽[/gold]" in zh_ancient["DARV.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.3-0r.char"] and
    "[gold]狗圈[/gold]" in zh_ancient["DARV.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.3-0r.char"], "达弗 金色物品")
chk("[color=#000000]她[/color]" in zh_ancient["OROBAS.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.2-0r.ancient"] and
    "[blue]她[/blue]" in zh_ancient["OROBAS.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.3-0r.ancient"], "欧洛巴斯 黑色/蓝色她")
chk("[pink]G3[/pink]" in zh_ancient["TANX.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.1-0r.ancient"] and
    "[gold]M14[/gold]" in zh_ancient["TANX.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.1-0r.ancient"], "坦克斯 G3/M14")
chk("[red]诅咒[/red]" in zh_ancient["VAKUU.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.1-0r.char"] and
    "[gold]构想[/gold]" in zh_ancient["VAKUU.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.1-0r.char"] and
    "[red]流量[/red]" in zh_ancient["VAKUU.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.3-3r.ancient"] and
    "[green]质量[/green]" in zh_ancient["VAKUU.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.3-3r.ancient"], "瓦库 红/金/绿")
chk(zh_ancient["THE_ARCHITECT.talk.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.3-1r.ancient"] == "谢谢，我不渴。", "建筑师 我不渴")

chk("MomoiAnimMachineRegistry" in read(os.path.join(CODE, "Patches", "MomoiLowHpPatch.cs")), "残血状态机追踪")
chk(os.path.isfile(os.path.join(MOD, "audio", "low_hp_bgm.ogg")), "残血 BGM 文件")
character = read(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs"))
chk('Sequence("low_hp"' in character and "LowHpFrameMap" in character, "low_hp 帧序列")
chk('AddState("low_hp"' in character and 'AddAnyState("LowHp"' in character, "low_hp 状态机")
chk(sum(1 for n in names if "low_hp" in n and n.endswith(".ctex") and "low_hp_bgm" not in n) == 28, "PCK 含 28 张 low_hp ctex")
chk(any("low_hp_bgm" in n for n in names), "PCK 含残血 BGM")
for f in ("hurt.ogg", "ba_boot.ogg", "creative_pain.ogg", "minigame_generated.ogg", "winning_script.ogg"):
    chk(os.path.isfile(os.path.join(MOD, "audio", f)), "音效文件 " + f)
chk("MomoiSfx.Register" in read(os.path.join(CODE, "Entry.cs")), "启动注册自定义音效")
settings = read(os.path.join(CODE, "Settings", "MomoiSettings.cs"))
chk(all(x in settings for x in ("MasterVolume", "MusicVolume", "VoiceVolume", "SfxVolume", "HurtVoiceVolume", "DeathVoiceVolume")) and
    'AddSection("audio"' in settings and "LowHpVolume" not in settings, "六档音量设置栏")
momoi_audio = read(os.path.join(CODE, "Audio", "MomoiAudio.cs"))
chk(all(x in momoi_audio for x in ("MasterGain", "MusicGain", "VoiceGain", "SfxGain", "HurtGain", "DeathGain", "PlayDirectSfx")), "音量分组/直通音频")
chk(all(os.path.isfile(os.path.join(MOD, "audio", f)) for f in
        ("creative_pain_impact.ogg", "death_voice.ogg", "watch_out_voice.ogg", "maid_weapon_voice.ogg", "gunshot.wav", "revive.ogg")),
    "新增 6 个音效文件")
cue = read(os.path.join(CODE, "Patches", "MomoiCardAnimationCuePatch.cs"))
chk("SetAttackCue" in cue and "GetAttackCue" in cue and "card is not HundredPull" in cue, "多段攻击逐段动画")
creative = read(os.path.join(CODE, "Cards", "CreativePain.cs"))
hundred = read(os.path.join(CODE, "Cards", "HundredPull.cs"))
chk("persistent: true" in creative and "vfx_giant_horizontal_slash" not in creative and "CreativePainImpact" in creative, "创作痛苦：无斩击+持续旋风+新音效")
chk("WithHitCount(3)" in creative and "WithWaitBeforeHit(0.5f, 0.5f)" in creative,
    "创作痛苦：一条命令 3 段 + 0.5s 段间间隔（批次41 修活力多次消耗）")
gunstyle = read(os.path.join(CODE, "Cards", "MomoiGunStyle.cs"))
chk("NShivThrowVfx.Create" in gunstyle and "NDaggerSprayFlurryVfx.Create" in gunstyle, "单体单发 + 对群弹幕双路径")
chk("MomoiGunStyle.ApplyBarrage" in creative and "MomoiGunStyle.ApplyBarrage" in read(os.path.join(CODE, "Cards", "ConceptFlowCards.cs")) and "WithHitCount" in read(os.path.join(CODE, "Cards", "ConceptFlowCards.cs")), "创作痛苦/天马行空对群弹幕")
chk("NDaggerSprayFlurryVfx.scenePath" in read(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs")) and "NDaggerSprayImpactVfx.scenePath" in read(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs")), "弹幕 VFX 预载")
chk("NGroundFireVfx.AssetPaths" in read(os.path.join(CODE, "Characters", "STS2 MomoiCharacter.cs")), "焚烧 VFX 预载")
chk("PlayDirectVoice" in read(os.path.join(CODE, "Patches", "MomoiReviveSfxPatch.cs")), "免死音效归语音")
death_voice = read(os.path.join(CODE, "Audio", "MomoiDeathVoice.cs"))
chk("MomoiDeathVoice.Register" in read(os.path.join(CODE, "Entry.cs")) and "WasRemovalPrevented" in death_voice and "LocalContext.IsMe" in death_voice, "全路径死亡语音事件")
chk("DeathVoiceVolume { get; set; } = 500" in settings and "0, 700" in settings, "死亡音量默认 500 / 最高 700")
chk("persistent: true" in hundred and hundred.count("WithHitFx(\"vfx/vfx_giant_horizontal_slash\")") >= 1, "100连抽逐段斩击+持续旋风")
gun_files = ["STS2_MomoiStrike.cs", "CommonAttackCards.cs", "FirepowerFlowCards.cs", "BurnFlowCards.cs", "ConceptFlowCards.cs"]
chk(sum(read(os.path.join(CODE, "Cards", f)).count("MomoiGunStyle.Apply") for f in gun_files) >= 7, "7 张枪械牌小刀特效/枪声")
intent = read(os.path.join(CODE, "Cards", "IntentCards.cs"))
chk("PlayFiendFire" in read(os.path.join(CODE, "Cards", "BurnFlowCards.cs")) and
    "vfx/vfx_molten_fist" in intent and
    "MomoiSovereignStyle.Apply" in read(os.path.join(CODE, "Cards", "NewCardsBatch.cs")), "恶魔之焰/熔融之拳/君王斩击")
chk("MomoiReviveSfxPatch" in read(os.path.join(CODE, "Patches", "MomoiReviveSfxPatch.cs")) and
    "MomoiReviveSfxPatch" in read(os.path.join(CODE, "Entry.cs")), "免死音效补丁")
chk("DeathVoice" in death_voice and
    "WatchOutVoice" in read(os.path.join(CODE, "Cards", "WatchOut.cs")) and
    "MaidWeaponVoice" in read(os.path.join(CODE, "Cards", "ReworkBatch.cs")), "死亡/当心误射/女仆语音")
chk("MomoiSfx.Hurt" in read(os.path.join(CODE, "Patches", "MomoiLowHpPatch.cs")), "受伤音效")
chk("MomoiSfx.BaBoot" in read(os.path.join(CODE, "Cards", "FirepowerFlowCards.cs")), "BA启动音效")
chk("MomoiSfx.CreativePain" in read(os.path.join(CODE, "Cards", "CreativePain.cs")), "创作痛苦音效")
chk("MinigameGenerated" in read(os.path.join(CODE, "Relics", "DriedInspiration.cs")) and
    "MinigameGenerated" in read(os.path.join(CODE, "Relics", "MoreRelics.cs")), "小游戏生成音效")
chk("FlashSfx => Audio.MomoiSfx.WinningScript" in read(os.path.join(CODE, "Relics", "MoreRelics.cs")), "胜利剧本音效")
chk("vfx/vfx_bite" in read(os.path.join(CODE, "Cards", "BurnFlowCards.cs")) and
    "vfx/vfx_adrenaline" in read(os.path.join(CODE, "Cards", "ConceptCard.cs")), "火蛇/构想特效")
chk("PlayWhirlwind" in read(os.path.join(CODE, "Cards", "HundredPull.cs")) and
    "PlayWhirlwind" in read(os.path.join(CODE, "Cards", "CreativePain.cs")), "旋风斩特效")
# 2026-10-25：特效路径被重排（针锋相对改用 vfx_molten_fist，秒人斧在 HundredPull 用 vfx_giant_horizontal_slash）。
chk("vfx/vfx_giant_horizontal_slash" in read(os.path.join(CODE, "Cards", "HundredPull.cs"))
    and "vfx/vfx_molten_fist" in read(os.path.join(CODE, "Cards", "IntentCards.cs")), "秒人斧/针锋相对特效")
burn_power = read(os.path.join(CODE, "Powers", "BurnPower.cs"))
chk("IHealthBarForecastSource" in burn_power and
    "PlayGroundFire" in burn_power, "灼烧血条/施加与伤害地面火焰")
events = json.load(open(os.path.join(MOD, "localization", "zhs", "events.json"), encoding="utf-8"))
relics = json.load(open(os.path.join(MOD, "localization", "zhs", "relics.json"), encoding="utf-8"))
chk(events.get("COLORFUL_PHILOSOPHERS.pages.INITIAL.options.STS2_MOMOI.title") == "桃红色", "色彩哲学家桃红标题")
chk(relics.get("SEA_GLASS.STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER.title") == "给木玻璃", "海玻璃给木玻璃")
chk(len(names) >= 960, "PCK 条目 >=960", len(names))
chk(40_000_000 <= os.path.getsize(PCK) <= 80_000_000, "PCK 已按贴图规则压缩（约 55MB）", os.path.getsize(PCK))

print()
print(f"结果：{ok} 条通过，{fail} 条失败")
sys.exit(1 if fail else 0)
