### 21.59 批次52：贴图大小默认 1.0（小桃本体 0.7）+ 出牌卡顿修复（1.0.8，2026-11-04）

#### 1. 设置「角色贴图大小」：默认 1.0、范围 0.5~1.5，小桃本体固定 0.7

用户反馈：滑块会同时缩放**所有**玩家角色，而小桃的素材本身就偏大，默认 0.7 时别人（原版角色）也跟着变小。要求「默认值 1.0、范围 0.5~1.5，但王小桃默认用素材的 0.7，设置里仍显示 1.0」，并明确「影响所有角色本来算 bug，但这个 bug 保留当特色」。

实现（`STS2 Momoi/STS2 MomoiCode/Settings/MomoiSettings.cs`）：

| 项 | 改前 | 改后 |
|---|---|---|
| `MomoiModSettings.CharacterTextureScale` | `0.7` | **`1.0`** |
| `MomoiSettingsStore.TextureScaleFactor` | `Math.Clamp(x, 0.2, 1.2)` | `Math.Clamp(x, 0.5, 1.5)` |
| general 段滑块 | `AddSlider(…, 0.2, 1.2, 0.05, v => $"{v:0.00}x")` | `AddSlider(…, 0.5, 1.5, 0.05, …)` |

`STS2 Momoi/STS2 MomoiCode/Patches/MomoiCharacterScalePatch.cs`:

```csharp
public const float MomoiDefaultScale = 0.7f;   // 王小桃素材自身的比例（写死，不进设置）

[HarmonyPrefix]  NCreature.ScaleTo(float size)
    if (__instance?.Entity is not { IsPlayer: true }) return;   // 怪物不动
    size *= MomoiSettingsStore.TextureScaleFactor;              // 滑块
    if (__instance.Entity.Player?.Character is STS2_MomoiCharacter) { size *= MomoiDefaultScale; }
```

* 为什么写死而不是改素材：素材是按美术观感画的，0.7 是「这张立绘在战斗里的正确比例」，属于内容而不是玩家偏好；放进设置会让「换角色 = 换观感」变得不可预期。
* `MomoiCombatRoomAddCreaturePatch`（`NCombatRoom.AddCreature` Postfix → `GetCreatureNode(creature)?.ScaleTo(1f, 0.0)`）保持传 `1f`：Postfix 走的是同一个 Prefix，传倍率会乘两次。
* 判定用 `Character is STS2_MomoiCharacter` 而不是「有没有我们的遗物/卡池」——玩家在自定义种子/改装角色下也成立。

#### 2. 出牌卡顿：逐条对照 QA，最后定位在「帧贴图首次解码」

按 QA 的五条逐一核对本项目：

| QA 条目 | 本项目情况 |
|---|---|
| 1. 特效场景没进缓存（`PreloadManager` 切场景清缓存 → 每次 `ResourceLoader.Load`） | **命中（本地版本）**：我们没有 VFX 场景，但战斗帧是**按路径声明**的贴图序列（`STS2 MomoiCharacter.cs` 的 `ModVisualCues.CueSet()`，600×820 一帧十几张）。第一次播到才解码，且切场景后缓存被清 → 每场战斗第一次出牌必停顿 |
| 2. `OnPlay` / 钩子里同步做重活 | 无牌堆全扫、无同步读图；但 `VigorPower.BeforeAttack/AfterAttack` 与 `MomoiCardAnimationCue.Trigger` **每张牌都无条件写一行 log**（写盘 + 格式化），属于白捡的开销 |
| 3. 整手牌描述反复重算（`ComputedDynamicVar`） | 全项目**没有** `ComputedDynamicVar`；`IndependentCalculatedVar` 只做一次字典查名，可忽略 |
| 4. 特效节点堆积（粒子 / `QueueFreeSafely` / `fixed_fps`） | 不适用：我们只创建 `AudioStreamPlayer` 与一个控制器 `Node` |
| 5. 角色动画没声明好（缺 Cast → 回落默认动画） | 动画走 RitsuLib `VisualCueSet`，`Attack`/`Cast` 都显式声明；**但** `MomoiAnimMachineTrackPatch` 同时挂在 `ModAnimStateMachine.Start` 和 **`SetTrigger`** 上（只为登记实例），而 `SetTrigger` 是每次攻击/施法都跑的热方法 |

修复（5 项）：

1. **cue 帧贴图预热** —— 新 `Patches/MomoiCueWarmupPatch.cs`：`NCombatRoom.AddCreature` Postfix，仅当进房间的是小桃玩家时，挂一个临时 `Node`，用 `DirAccess.Open($"{Entry.ResPath}/images/characters/cue")` 列出全部帧路径，**每帧 4 张** `ResourceLoader.Load<Texture2D>(path, cacheMode: ResourceLoader.CacheMode.Reuse)`（`await ToSignal(tree, SceneTree.SignalName.ProcessFrame)` 分帧），完成后 `QueueFree()`。`Reuse` 让贴图常驻，不再被换场景清掉。
2. **卡框材质只读一次 + UV 变体缓存** —— `Patches/MomoiCardFrameMaterialPatch.cs` 静态 `_cached` / `_loadAttempted`；`Patches/MomoiCardFrameVisualPatch.cs` 用 `Dictionary<(Vector2 Offset, Vector2 Scale), ShaderMaterial> Variants` 缓存 `Duplicate()` 出来的材质，并用 `ReferenceEquals(frame.Material, material)` 避免重复赋值（原来每次 `NCard.Reload` 都新建一份材质 → 手牌区一堆重复材质，触发额外重绘）。
3. **音频流缓存** —— `Audio/MomoiAudio.cs` 直放路径加 `ConcurrentDictionary<string, AudioStream> StreamCache` + `GetOrAdd`，不再每次 `ResourceLoader.Load<AudioStream>`。
4. **动画面板监听瘦身** —— `MomoiAnimMachineTrackPatch` 只留 `ModAnimStateMachine.Start`。
5. **热路径日志收口** —— 新增 `Diagnostics/MomoiDiag.cs` + 设置项「输出详细日志」（`verbose_logging`，默认关）：`MomoiDiag.Log` 只在开启时写盘。`VigorFirepowerPatch`（6 条）、`MomoiCardAnimationCuePatch`（3 条）、`MomoiAudio`、各小游戏/循环叙事/注能诊断日志（`GameLife` 1、`MinigameFlowCards` 6、`MinigameSupport` 1、`NewCardsBatch` 1、`RemainingCards2` 4、`ReworkBatch` 1、`ImbuedSupport`、`MomoiImbuedAndCompendiumPatches`）全部改走开关；**失败类 `Warn` 仍无条件输出**（排查要靠它）。

> 诊断建议（用户曾问怎么定位）：装 Speed Control 加速看卡顿是否随动画时长一起缩——跟着缩就是动画/等待，不缩就是逻辑侧；再看 `godot.log` 出牌那一刻的异常与 WARN。本批把「逻辑侧」的写盘与重复实例化都清掉了。

#### 3. 产物与自检

* 版本 **1.0.8**：`STS2 Momoi/STS2 Momoi.csproj` `<Version>1.0.8</Version>` + `STS2 Momoi/STS2_Momoi.json` `"version": "1.0.8"`（`min_version: 0.6.7` 不变）。
* `dotnet build "STS2 Momoi.csproj"` → **0 错误 / 31 既有警告**；DLL **520,704 B** / PCK **57,833,324 B**（体积优化未回退）。
* 新自检 `工作区/_scripts/_verify_batch52.py`（11 段），工坊 Content 同步 1.0.8 后重新上传（条目 id 3830602273 不变）。

#### 4. 本批踩的坑（都值得记）

1. **`python` CLI 是坏的**：`python - <<'PYEOF'` 直接静默不执行（退出码 0 但什么都没改）。第一次改 `VigorFirepowerPatch.cs` 的日志因此完全没生效，回读才发现。→ 一律 `"C:/Users/asus/AppData/Local/Python/pythoncore-3.14-64/python.exe"`。
2. **文件带 BOM**：`s.splitlines()[0].startswith("using")` 因 `\ufeff` 恒为 False，插 `using` 要按「最后一个 using 行之后」插。
3. **C# 模式语法**：`if (__instance?.Entity is not { IsPlayer: true } creature)` 不成立（属性模式不能绑定变量），要么 `is not { IsPlayer: true }` 直接 return，要么 `is { IsPlayer: true } creature`。
4. **PIL 已装但只在项目解释器里**：图片脚本用绝对路径跑，别用 `python`。
