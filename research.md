# Research: 在 Windows + RTX 4060 Laptop 8GB 上训练 Anima（CircleStone Labs, 2B DiT）画风 LoRA

> 调研日期：本次会话
> 环境基线：Windows / ComfyUI 秋叶整合包 v3.2（ComfyUI 0.30.2，embedded Python）/ RTX 4060 Laptop 8GB / RAM 32GB
> 可信度标注：**[官方]** = CircleStone/Comfy Org/kohya-ss 官方文档；**[社区-高]** = 多来源交叉印证或有实测数据；**[社区-中]** = 单一来源/个人经验；**[推断]** = 由已知数据推导，非直接实测

---

## Summary

可以做，但必须换一个独立训练环境（**不要**往秋叶 ComfyUI 整合包的 embedded Python 里装训练依赖）。Anima 有**两条官方训练路径**：作者 tdrussell 自己的 `diffusion-pipe`（官方训练代码就是它的私有分支），以及 kohya-ss `sd-scripts` 的 `anima_train_network.py`（有完整英文/日文文档，支持 `--blocks_to_swap` 等低显存开关）。8GB 显存的关键开关是 **block swap（换出全部 28 层）+ gradient checkpointing + bf16 + cache latents/TE outputs**：有实测显示 28 层全换出后训练步峰值从 5.2GB 降到 **1.84GB**（慢约 11%），即 6GB 级卡可跑完整训练。**最重要的纠正**：28/40/52 block 重映射问题**只在你跨代使用模型时才存在**——在 `anima-base-v1.0`（28 层）上训练、在 base/Aesthetic/Turbo（同为 28 层）上用，**不需要任何 remap**，标准 `LoraLoaderModelOnly` 直接可用；只有把 LoRA 用到社区 40 层的 Anima-2.9B 或 52 层的 Anima-3.8B 上才需要 ComfyUI-Anima-Remap 之类的工具。

---

## 0. 先纠正任务前提中的三个技术细节

1. **latent 不是"Wan21 latent"，VAE 文件是 `qwen_image_vae.safetensors`**。Anima 的 VAE 是 Qwen-Image VAE（16 channel，8× 空间下采样）。Qwen-Image VAE 本身是 Wan-VAE 系架构，kohya 的 PR 里也写成 `--vae_path <path_to_wanvae>`、`library/anima_vae.py - Anima VAE (WanVAE-based)`，但**你要下载和填路径的文件名是 `qwen_image_vae.safetensors`**（254MB）。不要去找 Wan2.1 的 VAE 文件。**[官方]**
   - 来源：<https://huggingface.co/circlestone-labs/Anima> ；<https://github.com/kohya-ss/sd-scripts/blob/main/docs/anima_train_network.md>
2. **需要三个权重文件**（不是两个）：DiT `anima-base-v1.0.safetensors`（4.18GB）+ 文本编码器 `qwen_3_06b_base.safetensors`（1.19GB）+ VAE `qwen_image_vae.safetensors`（254MB）。另外还有一个 **6 层 LLM Adapter + T5 tokenizer**，它存在于 DiT 权重文件内部（`llm_adapter.blocks.*`），但**绝对不能训练**。**[官方]**
3. **Anima 不能用 fp16 训练**。社区实测与 kohya 文档一致：Anima 是全 bf16 模型，`--mixed_precision` 必须是 `bf16`；`--fp8_base` / `--fp8_scaled` **不被支持**（sd-scripts 会直接警告并强制关闭）。**[官方 + 社区-高]**
   - 来源：<https://huggingface.co/circlestone-labs/Anima/discussions/35> ；<https://github.com/kohya-ss/sd-scripts/blob/main/anima_train_network.py>

---

## 1. Anima 的 LoRA 训练用什么工具？

### 1.1 工具支持矩阵

| 工具 | 支持 Anima？ | 依据 / 要求 | 对你这台机器的适配 |
|---|---|---|---|
| **kohya-ss/sd-scripts** `anima_train_network.py` | ✅ **官方认可的参考实现** | 有专门文档 `docs/anima_train_network.md`（英/日）；musubi-tuner 作者本人回复 "Anima is supported by sd-scripts" | ⭐⭐⭐ 功能最全、文档最可信；但要自己配 venv，命令行 |
| **tdrussell/diffusion-pipe** | ✅ **作者自己的训练器** | 官方 README 明写 "My own training script, diffusion-pipe"；diffusion-pipe 2026-02-04 changelog "Support Anima"；官方训练代码 = 它的私有分支 | ⭐ 作者原味，但 **DeepSpeed + pipeline parallel、Linux 化**；block swap 文档只列 Wan/HunyuanVideo/Flux/Chroma，**未列 Anima** → 8GB Windows 不推荐 |
| **musubi-tuner** | ❌ **不支持** | issue #941 请 kohya-ss 加 Anima，作者回复指向 sd-scripts | — |
| **ComfyUI 训练节点** | ❌ 无成熟方案 | ComfyUI 官方只做**推理**原生支持 Anima；没有上游 Anima LoRA 训练节点 | 秋叶整合包只用来**出图/验证** |
| **lora-scripts-next / Next Trainer**（wochenlong） | ✅ GUI 封装 sd-scripts | 中文 GUI 整合包，内置 kohya 后端 + WD14 打标；Anima LoRA/LoKr/T-LoRA；README 标 ~12GB VRAM 起 | ⭐⭐⭐ **Windows 一键包 + 中文文档**，对你最省事 |
| **Anima-TrainFlow** | ✅ 封装 sd-scripts | 单页 Gradio GUI，**标称 6GB+ VRAM**，Windows 10/11，便携包，内置 WD14 EVA02 v3，Prodigy 默认；作者实测 RTX 3060 12GB 约 1 小时 | ⭐⭐⭐ **8GB 最友好**，但仓库来自多个镜像账号，需核对来源 |
| **sorryhyun/anima_lora** | ✅ 独立实现 | 有 `low_vram` preset（"also serves as Windows 8GB"）与 `tlora-8gb.toml`；标称 5060 Ti 上 rank32/1MP 峰值 13.4GB → **8GB 必须走 low_vram** | ⭐⭐ 快，但需要 `uv`、Python 3.13、驱动 ≥595 |
| **AnimaLoraStudio**（WalkingMeatAxolotl） | ✅ 独立实现 | 中文文档详尽；有 Block 交换实测数据；GPU 要求 **NVIDIA 16GB+ 推荐，8GB 极限可跑，开 block swap 下探 6GB 级** | ⭐⭐ 文档质量最高（中文），环境要求（Python 3.10+/Node 18+）略重 |
| **AI-Toolkit (ostris)** / RunComfy | ✅ | RunComfy 有 "Anima LoRA Training" 页面 | 云端为主，非本地 |
| Anima-Standalone-Trainer、AnimaLoraToolkit、DiffPipeForge 等 | ⚠️ 部分 | 均为社区封装 | 见 1.3 的仓库可信度说明 |

来源：<https://huggingface.co/circlestone-labs/Anima> ；<https://github.com/kohya-ss/musubi-tuner/issues/941> ；<https://github.com/tdrussell/diffusion-pipe/blob/main/docs/supported_models.md> ；<https://github.com/wochenlong/lora-scripts-next> ；<https://github.com/WalkingMeatAxolotl/AnimaLoraStudio>

### 1.2 推荐路线（针对你的环境）

**首选：lora-scripts-next 整合包（Next Trainer / SD-Trainer）**
- 一键 7z，双击 `run_gui.bat`，浏览器开 `http://127.0.0.1:28000`。**[社区-高]**
- 侧栏 **Anima LoRA** 页面（复用 `/lora/sd3.html` URL 槽位，但参数与训练脚本已完全是 Anima）。**[社区-高]**
- 支持 LoRA / LoKr / T-LoRA；内置 WD14 打标（离线模型 `tagger-models/wd14/wd14-convnextv2-v2`）**[社区-高]**
- 中文文档：`docs/anima-training.md`、`docs/training-tips.md`。
- 下载地址：<https://github.com/wochenlong/lora-scripts-next/releases>
- ⚠️ README 标称 **Anima LoRA 从 ~12GB VRAM 起**，说明其默认 preset **没开 block swap**。8GB 上必须自己显式打开 block swap / 降低分辨率，别指望默认能跑通。

**次选：Anima-TrainFlow（最省事、最贴合 8GB）**
- 便携包约 3GB（7z），解压 → `start_trainer.bat` → 填模型路径 → 选数据集目录 + 触发词 → Start。**[社区-中]**
- 内置 WD14 Tagger (EVA02 v3) 自动打标、U2Net 智能裁剪、实时预览、bf16 + latent 缓存默认。**[社区-中]**
- 作者实测（RTX 3060 12GB）平均约 **1 小时**。**[社区-中]**
- ⚠️ 该仓库 README 同时出现在 `NBSTpeterhill/Anima-TrainFlow`、`cignoir/Anima-TrainFlow`，便携包托管在 `ThetaCursed/Anima-TrainFlow-Portable`。**同一个工具被多个账号镜像发布**，下载前请核对 SHA / 来源，优先从 star 数最高、最近有提交的那个下。

**想完全掌控参数 / 对齐上游：直接用 kohya-ss/sd-scripts**
参考命令（官方文档原文结构）：

```bash
accelerate launch --num_cpu_threads_per_process 1 anima_train_network.py \
  --pretrained_model_name_or_path="<Anima DiT .safetensors>" \
  --qwen3="<qwen_3_06b_base.safetensors 或目录>" \
  --vae="<qwen_image_vae.safetensors>" \
  --dataset_config="my_anima_dataset_config.toml" \
  --output_dir="<输出目录>" --output_name="my_anima_style" \
  --save_model_as=safetensors \
  --network_module=networks.lora_anima \
  --network_dim=32 --network_alpha=32 \
  --learning_rate=2e-5 --optimizer_type=AdamW8bit \
  --lr_scheduler=constant \
  --timestep_sampling=sigmoid --discrete_flow_shift=1.0 \
  --max_train_steps=2000 \
  --mixed_precision=bf16 \
  --network_train_unet_only \
  --gradient_checkpointing --blocks_to_swap=28 \
  --cache_latents --cache_latents_to_disk \
  --cache_text_encoder_outputs --cache_text_encoder_outputs_to_disk \
  --vae_chunk_size=64 --vae_disable_cache \
  --sdpa
```

来源：<https://github.com/kohya-ss/sd-scripts/blob/main/docs/anima_train_network.md>

**不推荐：diffusion-pipe**。虽然它是"官方"训练器，但它是 DeepSpeed/hybrid pipeline-parallel 架构，官方最低显存文档给的是 `wan_14b_min_vram.toml` 那套（针对视频模型），且 block swap 支持列表里没有 Anima。8GB Windows 上属于逆风局。

### 1.3 ⚠️ 仓库可信度警告（重要）

调研中发现 **至少 4 个 `anima_lora` 仓库共享几乎逐字相同的 README**：
- `sorryhyun/anima_lora`（99 stars，有实测数据）
- `n0va39/anima_lora`、`l2dnjsrud/anima_lora`（README 与 sorryhyun 版本几乎完全一致）

这属于典型的 fork/镜像/搬运。**原则**：
- 训练参数与 flag 语义 → 只信 **kohya-ss/sd-scripts** 官方文档。
- 想用第三方 trainer → 只挑 star 高、近期有 commit、且能对到上游 commit 的。
- **任何只存在于单一低星仓库的"神奇参数"，不要照抄到长训练里。**

来源：<https://github.com/sorryhyun/anima_lora> ；对比 <https://github.com/n0va39/anima_lora>、<https://github.com/l2dnjsrud/anima_lora>

---

## 2. 画风 LoRA 的数据集要求与打标策略

### 2.1 数据集规模 / 分辨率

| 来源 | 画风 LoRA 建议 | 备注 |
|---|---|---|
| AnimaLoraStudio（中文文档） | 最少 **50** 张，推荐 **100–300** 张，`repeats` 5–10 | 分辨率建议 1024×1024 或更高；尽量保留完整构图 **[社区-高]** |
| HF 官方讨论区（作者/资深用户） | **60–400 张**（画风）；角色只要 15–50 张 | "画风需要更多步数" **[社区-高]** |
| AnimaLoraStudio 参数表 | LoRA rank 8–16 用于画风 LoRA | rank 8 ≈ 1MB，rank 16 ≈ 2MB **[社区-高]** |
| civitai 教程 | 8GB 卡建议 `batch_size=1` | 12GB→2，24GB→4 **[社区-中]** |
| 数据集结构 | 图片 + **同名 `.txt`** sidecar（kohya 传统）| sd-scripts `--dataset_config` 的 TOML 格式 **[官方]** |

**Anima 官方示例画风 LoRA**（含数据集与 config 分享）：
<https://civitai.com/models/2536147> —— 官方 README 里 "Example of a style LoRA, with dataset and configs shared" 指向这里。**[官方]** 建议第一站就去看它的 caption 长什么样。

**解析度注意**：Anima 支持 512²–1536²，1024² 是甜点。8GB 训练建议先从 **768** 起步（TrainFlow 默认就是 768、dim=20），确认流程通了再上 1024。**[社区-中]**

### 2.2 是否需要打标？——需要

Anima 官方说明："The model is trained on Danbooru-style tags, natural language captions, and combinations of tags and captions."。所以**必须打标**，且推荐 **booru tag 风格**（Anima 的原生语言），而不是纯自然语言。**[官方]**

### 2.3 推荐打标工具

| 工具 | 适用 | 备注 |
|---|---|---|
| **WD14 Tagger（EVA02 v3 / ConvNeXtV2 v2）** | ⭐ 首选。booru tag 风格，与 Anima 训练分布一致 | TrainFlow 内置 EVA02 v3；lora-scripts-next 内置 `wd14-convnextv2-v2` **[社区-高]** |
| **CLTagger** | 备选 | AnimaLoraStudio 支持的三种之一 **[社区-中]** |
| **LLM 打标（JoyCaption / Qwen3-VL / Qwen3.5）** | 做自然语言 caption 或补细节 | 有用户用 Qwen3.5-35B-A3B，小机器可用 9B 版；走 LM Studio / Jan.ai **[社区-中]** |
| Florence-2 | 可用但非 Anima 社区主流 | 未见 Anima 专属推荐 |

**打标后必须做的事**：
- 全小写，用空格不要下划线（**例外**：`score_*` 系列质量 tag 保留下划线 —— Anima 官方明确规定）。**[官方]**
- 人工检查，删掉明显错的 tag（自动打标器会犯错，例如把白底标成黑底）。**[社区-高]**
- 别打"完整 tag 列表"心态：Anima 训练时用了 **random tag dropout**，你不需要把每张图的所有 tag 都写全。**[官方]**

### 2.4 画风 LoRA 的 caption 策略（最容易做错的一环）

**核心结论：触发词用 `@` 前缀的假画师名，保留内容 tag，删掉/不加会与画风竞争的风格 tag。**

1. **触发词格式必须是 `@yourstylename`**。Anima 是一个 **@ 前缀画师 tag** 驱动的模型：官方原文 "Prefix artist with @. E.g. `@big chungus`. **You must put @ in front of the artist.** The effect will be very weak if you don't."。所以你的画风触发词应写成 `@mystyle` 这种**伪装成画师名**的形式，而不是 `mystyle style`。**[官方]**
   - 好处：Anima 已经内建极强的 @画师 tag 响应能力，用同一通道承载你的画风，泛化会明显更好。
   - 来源：<https://huggingface.co/circlestone-labs/Anima>
2. **保留内容 tag（角色/场景/物体/动作），不要删除。** 这样画风才是"可切换的滤镜"而不是"污染一切的 sludge"。**[社区-高]**
   - AnimaLoraStudio 的画风 LoRA 对照表：`train caption 保留 = 内容 tag`，`train caption 删掉 = 无`（保持原样），`正则集排除 = 触发词 + 画师名`。
   - 原理：让 trigger 承载"画风"，内容 tag 继续承载"画什么"；正则集（trigger 不带）提供"没有这个画风时这组内容 tag 该长什么样"的监督。
3. **不要加 quality / score / year / medium / 其他画师 tag**（对画风 LoRA 而言）。**[社区-高]**
   - 官方讨论区原文建议："For a style lora, you might actually want to avoid style-modifying captions if the images are all in the same style (other than your made up artist triggerword/s ofc) and just let the model learn."
   - 理由：所有这些图都是同一个画风 → 写 `year 2024` / `watercolor` / 别的 `@artist` 会把这些 tag 也吸收成触发词的一部分，导致你以后没法用 `year 2024` 做正常控制。
   - ⚠️ 但注意 Anima 的**数据集 tag** 机制（`ye-pop` / `deviantart` 加换行 + alt text）是官方训练数据的一部分；如果你抓的是 DeviantArt/非动漫图，建议保留对应 dataset tag 行为。
4. **`caption_dropout_rate` 建议 0.1–0.15**。kohya LLLite 训练用了 0.15，理由是支撑推理时的 CFG。**[社区-高]**
5. **可选：加正则集缓解灾难性遗忘。** Anima 已知问题：LoRA 会显著稀释/压制 @画师 tag 的原生响应（HF discussion #60）。作者的缓解建议："If you can, training with extra not-strictly-related data helps the model not forget a bit."。还有人贴了 differential output preservation 的 `anima_train_network.py` 补丁（`is_reg = true` + `custom_attributes.diff_output_preservation = true`）。**[社区-中，补丁未经上游合并]**
   - ⚠️ 注意：`--cache_text_encoder_outputs` 与常规 shuffle/tag dropout 有互斥约束（sd-scripts 会 assert）；用正则集时请按官方 dataset config 文档配。

来源：<https://huggingface.co/circlestone-labs/Anima> ；<https://huggingface.co/circlestone-labs/Anima/discussions/96> ；<https://huggingface.co/circlestone-labs/Anima/discussions/60> ；<https://github.com/WalkingMeatAxolotl/AnimaLoraStudio/blob/master/docs/user-guide/training-tips.md>

---

## 3. 8GB 显存能训练 2B 模型 LoRA 吗？

**能，而且有相当扎实的证据。** 关键开关是 **block swap（把靠后的 DiT 层权重常驻内存，算到才换入显存）**。

### 3.1 实测显存数据（最重要的一条）

AnimaLoraStudio 真机实测（RTX 5090、bf16、1024²、grad checkpoint 开）：**28 层全部换出后，训练步峰值从 5.2GB 降到 1.84GB（速度约慢 11%）**；加上常驻文本编码器约 1.2GB 与显卡上下文 —— **"6 GB 级显卡可跑完整训练"（sample 照开）**。**[社区-高，带实测数字]**

代价：需要等量可用**内存**（Anima 每层约 0.13GB → 28 层约 **3.6GB 被锁定**），出图侧 DiT 常驻降到约 0.6GB。你有 32GB RAM，完全够。

来源：<https://github.com/WalkingMeatAxolotl/AnimaLoraStudio/blob/master/docs/user-guide/training-tips.md>

### 3.2 推荐配置（RTX 4060 Laptop 8GB）

```toml
# 数据 / 分辨率
resolution        = 768          # 先 768 跑通，再试 1024
batch_size        = 1            # 8GB 只能 1
gradient_accumulation_steps = 4  # 有效 batch = 4（社区经验：bs>1 更稳，用 accum 模拟）

# 精度（无选择余地）
mixed_precision   = "bf16"       # 绝对不能用 fp16
save_precision    = "bf16"
# full_bf16 / full_fp16 → 不要开（Automagic/CAME 下 NaN 风险）

# 显存三件套
gradient_checkpointing = true
blocks_to_swap         = 28      # 全部换出；8GB 上是决定性开关
                                 # 注意：与 cpu_offload_checkpointing / unsloth_offload_checkpointing 互斥！

# 缓存（省显存 + 提速）
cache_latents                  = true
cache_latents_to_disk          = true
cache_text_encoder_outputs     = true
cache_text_encoder_outputs_to_disk = true
vae_chunk_size                 = 64
vae_disable_cache              = true

# 网络
network_module    = "networks.lora_anima"
network_dim       = 16           # 画风 LoRA：16 足够（官方基准 rank 32 @ lr 2e-5 也可，占显存略多）
network_alpha     = 16
network_train_unet_only = true   # 只训 DiT，不训 Qwen3 TE
llm_adapter_lr    = 0            # ★ 官方明确要求：不训 LLM Adapter

# 优化器
optimizer_type    = "AdamW8bit"  # 或 Prodigy / ProdigyPlusScheduleFree
learning_rate     = 2e-5         # ★ 官方给的 rank32 起点；画风可 1e-5~5e-5
lr_scheduler      = "constant"   # PPSF 必须 "none"

# 采样 / 时间步
timestep_sampling = "shift"
discrete_flow_shift = 1.5
sigmoid_scale     = 1.2

# Windows 专属
max_data_loader_n_workers = 0    # Windows 必须 0（AnimaLoraToolkit 明确提示）
attn_mode         = "sdpa"       # 40 系可装 Flash Attention 2 提速；装不上就 SDPA
```

**几处硬约束（会直接 assert 报错，来自 sd-scripts 源码）**：**[官方]**
- `--blocks_to_swap` **不能**与 `--cpu_offload_checkpointing` 同用。
- `--unsloth_offload_checkpointing` **不能**与 `--cpu_offload_checkpointing` 或 `--blocks_to_swap` 同用（它比 cpu_offload 快，用异步非阻塞传输）。
- `--cache_text_encoder_outputs` 开启时，`shuffle_caption` / `token_warmup_step` / `caption_tag_dropout_rate` **不可用**（会 assert）。
- `--cache_text_encoder_outputs` 开启时，**无法**同时训 Qwen3 TE LoRA（必须 `--network_train_unet_only`）。
- `--fp8_base` / `--fp8_scaled` 不被 Anima 支持（自动强制关闭）。

### 3.3 步数与时间

| 场景 | 步数 | 依据 |
|---|---|---|
| 角色 LoRA | 1000–1500（20–30 张图） | 社区经验 **[社区-高]** |
| **画风 LoRA** | **1500–3000 起步**；有人用到 6500 | 60 张图 ≈25 epoch ≈1500 步够用；65 张图 / dim16 / lr 5e-5 / **6500 步**的成熟案例 **[社区-高]** |
| 过拟合警戒 | >2400–3000 步开始记忆数据集；>3500 步出现"硬贴训练图" | **[社区-中]** |
| 收敛速度 | 约 500 步已能看出明显差别 | **[社区-中]** |

**时间估算 [推断]**：
- 有实测：Anima-TrainFlow 在 RTX 3060 12GB、默认 dim20/res768 下，**平均约 1 小时**跑完一个完整训练。
- 有实测：Colab 免费 T4，**1000 步 > 4 小时**。
- RTX 4060 Laptop 8GB 性能大致落在 3060 12GB 与 T4 之间（且 block swap 带来约 11% 额外开销、笔记本有降频）。
- → **合理预期：768 分辨率、dim16、1000–1500 步，约 1–3 小时；1024 分辨率 + 2000+ 步，约 3–6 小时。** 建议挂夜间跑。
- **务必**：开采样图（`sample_every_n_steps` / `enable_preview`），观察"效果最好"的那一步就停，不要盲目跑满。WAI-Anima 在 4060 Laptop 上出图约 55s/张（30 步 1024²），采样本身也要吃时间。

来源：<https://github.com/cignoir/Anima-TrainFlow> ；<https://github.com/citronlegacy/citron-colab-anima-lora-trainer> ；<https://lilting.ch/en/articles/wai-anima-rtx4060-laptop-comfyui-api> ；<https://civitai.com/articles/31972/anima-lora-training-settings-for-sd-scripts>

### 3.4 Windows 专属坑

- **CUDA OOM 但没报错的"隐性降速"**：Windows WDDM 允许显存溢出到系统内存（Sysmem Fallback）。症状是前几十步正常，之后 it/s 掉一半且不恢复，任务管理器显示"共享 GPU 内存"上涨但无 CUDA OOM。**解法**：NVIDIA 控制面板 → 管理 3D 设置 → 程序设置 → 把 Python 的"CUDA - 系统内存回退策略"设为 **"首选无系统内存回退"**（让它直接报 OOM，PyTorch 的自愈路径才生效）。多分辨率桶训练最容易踩到。**[社区-高]**
- `num_workers` 在 Windows 上必须设 **0**（否则 DataLoader 反复起进程，极慢或直接崩）。**[社区-高]**
- block swap 会**锁定约 3.6GB 内存**，同时开浏览器 + ComfyUI 时注意 32GB 余量。**[社区-高]**
- 40 系卡建议装 **Flash Attention 2** 提速（lora-scripts-next 有 `install_flash_attn.bat` 一键脚本）；装不上退回 SDPA，不要强行上 xformers。**[社区-高]**

---

## 4. 训练出来的 LoRA 如何在 ComfyUI 里加载使用

### 4.1 结论：`LoraLoaderModelOnly` 完全可用，且是推荐做法

- 因为你用 `--network_train_unet_only` + `--cache_text_encoder_outputs`，**LoRA 只含 DiT 权重，不含 Qwen3 TE 权重**。
- 用 `LoraLoaderModelOnly`（只有 `model` 输入，没有 `clip` 输入）即可 —— 不需要给 CLIP 喂东西。`strength_model` 起步 **0.8–1.0**（画风建议先试 0.7–0.9）。**[社区-高]**
- kohya 官方文档明说：**"conversion may not be needed for DiT-only LoRA"** —— 即 DiT-only LoRA 无需格式转换。只有你训了 Qwen3 TE LoRA 才需要用 `networks/convert_anima_lora_to_comfy.py`（或 `anima_convert_lora_to_comfy.py`）转换。**[官方]**
- 用 `LoraLoader`（带 clip）也可以，但 `strength_clip` 对你的 LoRA 无意义（没有 TE key），纯属多余连线。
- 第三方 trainer（AnimaLoraStudio / lora-scripts-next）输出的 key 名已经是 `lora_unet_*`，**直接拖进 ComfyUI 即可，无需转换**。**[社区-高]**
- 文件放 `ComfyUI/models/loras/`。秋叶整合包同理。

来源：<https://github.com/kohya-ss/sd-scripts/blob/main/docs/anima_train_network.md> ；<https://github.com/WalkingMeatAxolotl/AnimaLoraStudio/blob/master/docs/user-guide/training-tips.md>

### 4.2 28/40/52 block 层映射问题 —— 澄清（这是本次调研最重要的纠正）

**你的场景下不需要任何 remap 插件。**

**架构谱系**：**[社区-高]**
```
Anima base v1.0 / Aesthetic v1.1 / Turbo  = 28 blocks   （官方，同一架构）
        ↓ 插入 12 块（LLaMA-Pro 风格）
Anima-2.9B（社区 Gazingstars123）          = 40 blocks
        ↓ 再插入 12 块
Anima-3.8B（社区 lylogummy）               = 52 blocks
```

- Anima 的**官方版本全是 28 层**。AnimaLoraStudio 的中文文档原话："Anima 与 Krea 2 通用…**两族都是 28 层**"。Aesthetic v1.1 是 base 的美学微调版，结构不变（共用同一个 `qwen_image_vae.safetensors` 与 `qwen_3_06b_base.safetensors`）。**[社区-高]**
- 因此：**在 `anima-base-v1.0`（28）上训 LoRA → 用在 base / Aesthetic v1.1 / Turbo（28）上 = 原生匹配，无任何重映射问题。**
- **只有**当你把 28-block LoRA 挂到 **社区 40-block / 52-block 模型**上时，才会出现键位错配：`blocks.2` 到 `blocks.27` 在 40-block 模型里**都存在**，所以 ComfyUI **不会报 "lora key not loaded" 警告**，权重静默落到错误的层 → 输出"涂鸦级"崩坏，或表现为"LoRA 好像没用 / 加大强度反而变差"。**[社区-高]**

**如果将来确实需要（跨代）**，可选工具（**三选一，不要同时装**）：

| 工具 | 覆盖 | 特点 | 地址 |
|---|---|---|---|
| **shin131002/ComfyUI-Anima-Remap** | 28↔40↔52，双向 | ⭐ 最推荐。自动检测 LoRA/模型的 block 数并选对 manifest；含随机 LoRA 加载器；`Auto (Recommended)` 默认 | <https://github.com/shin131002/ComfyUI-Anima-Remap> |
| shin131002/ComfyUI-Anima29B-Remap | 28↔40 | **已冻结**，与新仓库注册相同 node ID，**装了会冲突** | — |
| sparklingcoffee777/ComfyUI-Anima-2.9B-loraPatch | 28→40 | 无新节点，monkeypatch `comfy.lora.load_lora`，保留 `LoraLoaderModelOnly` 原节点 | <https://github.com/sparklingcoffee777/ComfyUI-Anima-2.9B-loraPatch> |
| INuBq8/ComfyUI-Anima-LoRA-ControlNet-Patch | 28↔40↔52 双向 + ControlNet-LLLite | 统一补丁，含**向下**（大→小）重映射，官方节点无需替换 | <https://github.com/INuBq8/ComfyUI-Anima-LoRA-ControlNet-Patch> |

⚠️ 已知陷阱：**[社区-高]**
- 层数检测是看 **LoRA 自己引用了哪些 block 索引的最大值**。一个 40-block LoRA 若只训了靠前的层，会被**误判成 28-block LoRA** 并被错误 remap。目前无 override 开关。
- `save_remapped`/缓存机制很危险：remap 缓存文件一旦落盘就**永久优先**，改了 manifest / 强度设置也不生效。调参期间**保持关闭**。
- `extend_to_new_layers` 是**实验性近似投影**，不是"正确答案"。
- 40→52 的 manifest 是**社区反推重建**的（官方只公布了 28→40 的 `expand_manifest.json`）。
- 跨代使用即使层对齐了，残差流仍多穿 12 个 block 且 llm_adapter 被重训过，**行为不会与在 base 上一致**，建议强度从 **0.5–0.7** 起步。

### 4.3 推理参数（Anima 官方推荐）**[官方]**

| 参数 | 值 |
|---|---|
| 分辨率 | 512²–1536²，1024² 甜点 |
| Steps | 30–50（Base/Aesthetic）；8–12（Turbo） |
| CFG | 4–5（Base/Aesthetic）；1（Turbo） |
| Sampler | `er_sde`（中性默认）/ `euler_a`（线条更柔）/ `dpmpp_2m_sde_gpu`（更创意）/ `euler`（配 Turbo/Aesthetic） |
| 正向前缀 | `masterpiece, best quality, score_7, safe, ` |
| 负向 | `worst quality, low quality, score_1, score_2, score_3, artist name, blurry, jpeg artifacts, chromatic aberration` |
| tag 顺序 | `[quality/meta/year/safety] [1girl/1boy] [character] [series] [artist] [general]` |
| 权重 | 需要比 SDXL 更高的权重，例：`(chibi:2)` |

**Aesthetic v1.1 专属**：它是纯高质量图微调、caption 里剥离了质量 tag，所以**不要**用 `score_*` tag（正负都别用），`masterpiece, best quality, ` 留着无妨。**[官方]**

**注意**：单独挂画风 LoRA 会**明显稀释 Anima 原生的 `@画师` tag 响应**（这是模型层的已知问题，非你训练出错）。缓解手段：LoRA 强度压低（0.4–0.7）、把 `@artist` tag 权重提到 1.4–1.6、或把画风本身就做成触发词。**[社区-高]**

---

## 5. 现成的中文教程 / 工作流

| 资源 | 类型 | 语言 | 备注 |
|---|---|---|---|
| **lora-scripts-next `docs/anima-training.md`** | 文档 | 中文 | ⭐ 最完整的 Anima LoRA GUI + 纯命令行 TOML 教程；含模型下载脚本、LoKr/T-LoRA 参数说明、NaN 排查。<https://github.com/wochenlong/lora-scripts-next/blob/main/docs/anima-training.md> |
| **AnimaLoraStudio `docs/user-guide/training-tips.md`** | 文档 | 中文 | ⭐⭐ 质量最高的中文 Anima 训练技巧文档：画风/角色 caption 对照表、正则集、Block swap 实测数据、Windows WDDM 坑、优化器对比。<https://github.com/WalkingMeatAxolotl/AnimaLoraStudio/blob/master/docs/user-guide/training-tips.md> |
| **AnimaLoraStudio `docs/user-guide/getting-started.md`** | 文档 | 中文 | 从零 8 步流水线（下载→筛选→预处理→打标→标签编辑→正则集→训练→测试）<https://github.com/WalkingMeatAxolotl/AnimaLoraStudio/blob/master/docs/user-guide/getting-started.md> |
| **AnimaLoraToolkit `docs/training-tips.md`** | 文档 | 中文 | 数据量/rank/优化器/ComfyUI 参数速查（硬件要求写 24GB+，偏保守）<https://github.com/Moeblack/AnimaLoraToolkit/blob/master/docs/training-tips.md> |
| **B站**：Anima模型LoRA训练首发！图形化界面零基础也能轻松上手 | 视频 | 中文 | 用 DiffPipeForge（天冬AI @TianDongL）+ diffusion-pipe 补丁（bluvoll）的 GUI 训练演示 <https://www.bilibili.com/video/BV1keFjzPEhG/> |
| **B站/YouTube**：LoRA训练实战52：Anima风格LoRA保姆式训练教程，全自动训练，超低显存 | 视频 | 中文 | 直击"画风 LoRA + 超低显存" <https://www.youtube.com/watch?v=Uu0Q1AsIJj4> |
| **YouTube**：手把手教你Anima LoRA训练！云端跑图、自动打标、20分钟出角色模型 | 视频 | 中文 | 讲得很细：lr 用 2e-5（因为官方 README 这么写）、dim/alpha 32、1024/1536 分辨率、1 万步观察、sample 每 250 步 <https://www.youtube.com/watch?v=OezOiqQut-c> |
| **civitai**：Anima LoRA training settings for sd-scripts | 文章 | 英文 | 有**画风 LoRA 完整案例**：65 张图 / dim16 / alpha16 / lr 5e-5 / 100 epoch / 6500 步，含 Windows .bat 模板 <https://civitai.com/articles/31972/anima-lora-training-settings-for-sd-scripts> |
| **civitai**：A Complete Beginner's Guide to Local Anima LoRA Training | 文章 | 英文 | 8GB 卡 batch_size=1 的建议来源 <https://civitai.com/articles/31678/a-complete-beginners-guide-to-local-anima-lora-training> |
| ComfyUI 中文文档：Anima（nomadoor / ComfyUI Wiki） | 文档 | 中文 | 推理侧：模型放置路径、Aesthetic v1.1 工作流、LLLite、采样推荐 <https://comfyui.nomadoor.net/zh/basic-workflows/anima/> |

---

## 6. 可执行步骤清单（针对你的确切环境）

### 阶段 0：环境隔离（做错这一步后面全是坑）

- [ ] **不要把训练依赖装进秋叶 ComfyUI 整合包的 embedded Python。** 秋叶包（v3.0 = ComfyUI v0.9.2 / Python 3.13.11 / torch 2.9.1+cu130）是**为推理对齐过的**，官方明说"不要乱更新"。在它里面 pip 装 flash-attn/bitsandbytes/torch 变体会破坏整合包。
- [ ] 采用**独立便携训练包**（自带 venv），例如 lora-scripts-next 的 `SD-Trainer-*.7z`（解压即用、自带 kohya 后端 + WD14）或 Anima-TrainFlow 便携包。
- [ ] 训练包与 ComfyUI 之间只通过 `models/diffusion_models`、`models/text_encoders`、`models/vae`、`models/loras` 共享**文件**，不共享环境。
- [ ] 建议直接复用秋叶包里已有的文件，省一次 5.6GB 下载：
  - `ComfyUI/models/diffusion_models/anima-base-v1.0.safetensors`（4.18GB）
  - `ComfyUI/models/text_encoders/qwen_3_06b_base.safetensors`（1.19GB）
  - `ComfyUI/models/vae/qwen_image_vae.safetensors`（254MB）
- [ ] 若还没下载，官方地址（或 ModelScope 镜像，国内更快）：
  - <https://huggingface.co/circlestone-labs/Anima/tree/main/split_files/diffusion_models>
  - <https://huggingface.co/circlestone-labs/Anima/tree/main/split_files/text_encoders>
  - <https://huggingface.co/circlestone-labs/Anima/tree/main/split_files/vae>

来源：<https://www.codef.cc/comfyui-aki.html> ；<https://huggingface.co/circlestone-labs/Anima>

### 阶段 1：数据集（画风 LoRA）

- [ ] 收集 **80–150 张**同画风图（下限 50，上限 300 以上收益递减）。
- [ ] 保证**多样性**：不同角色、场景、构图、光照、色彩 —— 但**画风一致**。避免全是同一角色的同一姿势（否则会把角色也绑进画风）。
- [ ] 裁切：保留完整构图；可上"自动头部遮罩 + masked loss"如果主体区域干扰画风学习（AnimaLoraStudio 支持）。
- [ ] 统一到 **768×768**（先）或 1024×1024（熟了再上）。Anima 支持原生宽高比 free-fit bucketing，尽量别硬裁成正方形。
- [ ] **WD14 打标**（内置即可，EVA02 v3 或 ConvNeXtV2 v2），general threshold 默认、character threshold 调低。
- [ ] **触发词**：`@yourstylename`（带 @！）。在打标器里设置"每张 caption 自动注入 trigger"。
- [ ] **人工过一遍 caption**：
  - 删掉 `year XXXX` / `newest` / `masterpiece` / `score_*` / `watercolor` 等**风格描述 tag**；
  - 保留角色/动作/场景/物体/构图 tag；
  - 全小写，空格不用下划线（`score_*` 除外）。
- [ ] 可选：准备正则集（20–50 张同内容类型但**非该画风**的图，官方优先用 base 模型自生成），caption **不含 trigger**。

### 阶段 2：训练配置（8GB 8 大要点）

- [ ] `mixed_precision = bf16`（**不是 fp16**）
- [ ] `gradient_checkpointing = true`
- [ ] `blocks_to_swap = 28`（★ 8GB 的关键；与 cpu_offload / unsloth_offload **互斥**）
- [ ] `batch_size = 1`，`grad_accum = 4`（有效 batch 4）
- [ ] `cache_latents(_to_disk)` + `cache_text_encoder_outputs(_to_disk)` + `vae_chunk_size=64` + `vae_disable_cache`
- [ ] `network_train_unet_only = true` + `llm_adapter_lr = 0`（★ 官方明确要求不训 LLM Adapter）
- [ ] `network_dim = network_alpha = 16`，`learning_rate = 2e-5`，`optimizer = AdamW8bit`，`lr_scheduler=constant`
- [ ] `caption_dropout_rate = 0.1`
- [ ] Windows：`num_workers = 0`；装 Flash Attention 2（失败退 SDPA）
- [ ] 先跑 **20 步的 smoke test**，确认不 OOM、it/s 正常、sample 能出图
- [ ] 设置 `save_every_n_steps = 250` + `sample_every_n_steps = 250`（每 250 步存一次、出一张样图）

### 阶段 3：训练与选点

- [ ] 目标 **1500–2500 步**（画风 LoRA）；挂夜间
- [ ] 每 250 步看样图：约 500 步应见明显画风变化；约 1500 步通常可用
- [ ] 警惕过拟合信号：>2500–3000 步开始"硬贴训练图"、prompt 遵循变差 → 回退到更早的 checkpoint
- [ ] 同时开 TensorBoard 看 loss（理想：快速下降 → 缓慢下降 → 平稳）

### 阶段 4：ComfyUI 加载

- [ ] 把 `*.safetensors` 复制到 `ComfyUI/models/loras/`
- [ ] 加 **`LoraLoaderModelOnly`** 节点：`model` 接 `UNETLoader`，`strength_model` 先 **0.7**
- [ ] **28-block LoRA → 28-block 模型（base / Aesthetic v1.1 / Turbo）→ 不需要任何 remap 插件**
- [ ] 出图参数：`er_sde` + 30–50 步 + CFG 4–5 + 1024²
- [ ] prompt 写法：`masterpiece, best quality, safe, 1girl, ..., @yourstylename`（把触发词当画师 tag 用）
- [ ] 若画风太强压制了原生 `@artist` tag：降 LoRA 强度到 0.4–0.7，或把 `@artist` 写到 `(artist:1.5)`

### 阶段 5（可选，仅当你切换到社区大模型时）

- [ ] 只有要用 **Anima-2.9B（40 层）** 或 **Anima-3.8B（52 层）** 时才装 remap 插件
- [ ] 装 **shin131002/ComfyUI-Anima-Remap**（**不要**同时装同样冻结的 ComfyUI-Anima29B-Remap，node ID 冲突）
- [ ] `save_remapped` 保持 OFF 直到参数定稿
- [ ] 跨代强度从 **0.5–0.7** 起步

---

## Sources

**Kept**

官方 / 一手（最高可信度）：
- circlestone-labs/Anima 模型卡与 README（https://huggingface.co/circlestone-labs/Anima）—— 版本谱系、生成参数、prompting/tag 体系、**Finetuning Tips（不训 LLM adapter、rank32 用 2e-5）**、@ 画师 tag 规范、非商业许可。**本次调研的最高依据。**
- kohya-ss/sd-scripts `docs/anima_train_network.md`（https://github.com/kohya-ss/sd-scripts/blob/main/docs/anima_train_network.md）—— Anima 架构定义（MiniTrainDIT / Qwen3-0.6B / LLM Adapter / Qwen-Image VAE 16ch 8×）、完整 CLI、目标模块、互斥参数、ComfyUI 转换脚本。
- kohya-ss/sd-scripts `anima_train_network.py` 源码（https://github.com/kohya-ss/sd-scripts/blob/main/anima_train_network.py）—— assert 级硬约束（blocks_to_swap / unsloth_offload / cpu_offload 的互斥关系）、fp8 不支持。
- tdrussell/diffusion-pipe `docs/supported_models.md` + README（https://github.com/tdrussell/diffusion-pipe）—— Anima 原生支持、`llm_adapter_lr=0`、用官方 ComfyUI 格式权重、block swap 支持范围。
- kohya-ss/musubi-tuner issue #941（https://github.com/kohya-ss/musubi-tuner/issues/941）—— **确认 musubi-tuner 不支持 Anima**，作者指向 sd-scripts。
- kohya-ss/Anima-LLLite（https://huggingface.co/kohya-ss/Anima-LLLite）—— caption_dropout 0.15 的依据。

社区（高可信 / 带实测）：
- AnimaLoraStudio `training-tips.md`（https://github.com/WalkingMeatAxolotl/AnimaLoraStudio/blob/master/docs/user-guide/training-tips.md）—— **28 层全换出 → 训练步峰值 1.84GB** 的实测；画风/角色 caption 对照表；正则集机制；Windows WDDM Sysmem Fallback 坑；GPU 分档。
- AnimaLoraStudio `getting-started.md`（https://github.com/WalkingMeatAxolotl/AnimaLoraStudio/blob/master/docs/user-guide/getting-started.md）—— 8 步流水线；Anima 8GB 极限可跑/6GB 级 block swap；RAM 3.6GB 锁定。
- lora-scripts-next `docs/anima-training.md`（https://github.com/wochenlong/lora-scripts-next/blob/main/docs/anima-training.md）—— 中文 GUI 流程、Fast 模式、T-LoRA/LoKr、NaN 排查。
- HF 讨论 #35（https://huggingface.co/circlestone-labs/Anima/discussions/35）—— **Anima 不能用 fp16**；`sd-scripts` 已实现训练。
- HF 讨论 #96（https://huggingface.co/circlestone-labs/Anima/discussions/96）—— **画风 LoRA 应避免风格修饰性 caption**、只用 @artist 承载画风、打标工具实践。
- HF 讨论 #106（https://huggingface.co/circlestone-labs/Anima/discussions/106）—— 画风 60–400 张、1500–3500 步的社区经验与过拟合阈值。
- HF 讨论 #60（https://huggingface.co/circlestone-labs/Anima/discussions/60）—— **LoRA 稀释/压制原生 @画师 tag 的灾难性遗忘问题**及缓解（低 LR、不训 LLM adapter、加无关数据、differential output preservation 补丁）。
- civitai《Anima LoRA training settings for sd-scripts》（https://civitai.com/articles/31972/anima-lora-training-settings-for-sd-scripts）—— 画风 LoRA 完整案例（65 图/dim16/lr5e-5/6500 步）+ Windows .bat 模板。
- shin131002/ComfyUI-Anima-Remap（https://github.com/shin131002/ComfyUI-Anima-Remap）—— 28/40/52 谱系、双向重映射、`save_remapped` 陷阱、检测误判边界。
- sparklingcoffee777/ComfyUI-Anima-2.9B-loraPatch（https://github.com/sparklingcoffee777/ComfyUI-Anima-2.9B-loraPatch）—— "静默落到错误层、不报 warning" 的机制解释。
- INuBq8/ComfyUI-Anima-LoRA-ControlNet-Patch（https://github.com/INuBq8/ComfyUI-Anima-LoRA-ControlNet-Patch）—— 统一补丁 + 向下重映射 + 28→52 必须顺序合成的原因。
- lilting.ch RTX 4060 Laptop 8GB 实测（https://lilting.ch/en/articles/wai-anima-rtx4060-laptop-comfyui-api）—— **你这张卡的出图实测：约 55s/张（30 步 1024²）**；CUDA vs M1 Max 对比。
- cignoir/Anima-TrainFlow（https://github.com/cignoir/Anima-TrainFlow）—— 6GB+ VRAM、内置 WD14 EVA02 v3、RTX 3060 12GB 约 1 小时。
- citronlegacy/citron-colab-anima-lora-trainer（https://github.com/citronlegacy/citron-colab-anima-lora-trainer）—— Colab T4 上 1000 步 > 4 小时的对照基线。
- ai-hardware-zukan Anima TrainFlow 评测（https://ai-hardware-zukan.com/en/anima-trainflow-simple-one-page-lora-trainer-for-b-portable-en/）—— 6/8/16/24GB 分档的可操作性判断。
- 秋叶整合包说明（https://www.codef.cc/comfyui-aki.html）—— 整合包版本构成与"不要乱更新"警告。

**Dropped**（列出以便复查）
- `n0va39/anima_lora`、`l2dnjsrud/anima_lora` —— README 与 `sorryhyun/anima_lora` 逐字重复，属镜像/fork，无独立信息量，且增加混淆风险。
- `AbstractEyes/anima-trainer`、`gazingstars123/Anima-Standalone-Trainer`、`beautifulrem/sd-scripts` —— 有用但被更高星/更上游的源覆盖；且部分宣传语（如"the only trainer that natively supports Anima"）与官方事实**矛盾**（sd-scripts 与 diffusion-pipe 都原生支持），属于营销性说法，降权处理。
- `Moeblack/AnimaLoraToolkit` 营销文案（硬件要求"24GB+"）—— 与 AnimaLoraStudio / TrainFlow 的 6–8GB 实测结论冲突，按保守性降权，仅保留其 `num_workers=0` 等 Windows 提示。
- `visionpaletteai.com` 的"Anima LoRA 高效微调与 FP8 转换" —— SEO 型商品页，内容泛化且把无关的 Z-Image 教程缝合进来，无一手信息。
- `smeltcore.com` Anima INT8/RTX 5060 配方 —— **推理**（非训练）优化，且核心技巧是"把 `int8_rowwise` 标成 `int8_tensorwise` 绕过 ComfyUI 格式检查"，属于 hack，不引入到训练流程。
- `BlackSnowSkill/ANIMA_BOOSTER`、`ComfyUI-AnimaTool`、随机 LoRA 加载器等 —— 推理侧增强，与训练问题无关。
- `RunComfy` AI-Toolkit Anima 页面 —— 云端训练，与本地 8GB 场景无关。
- 各种 ComfyUI 节点聚合站（comfy.icu、runcomfy.com/comfyui-nodes）—— 是 GitHub README 的自动转载，回源到原始仓库引用。
- 秋葉 ComfyUI 整合包下载站（stablediffusion.cn）—— 推广页，无技术信息。

---

## Gaps

1. **8GB 上训练的具体 it/s 没有公开实测。** 我找到的是：AnimaLoraStudio 在 **RTX 5090** 上的 block swap 显存/速度数据（1.84GB / 慢 11%），以及 Anima-TrainFlow 在 **RTX 3060 12GB** 上的"约 1 小时"、Colab T4 "1000 步 > 4 小时"。**4060 Laptop 8GB + block swap 的实际步速仍是推断**（我给出 1–3 小时 / 1000–1500 步 @768）。建议第一步就是跑 20 步 smoke test 实测 it/s 再外推。
2. **Anima-Aesthetic v1.1 是否为 28 层的直接验证未拿到一手证据。** 依据是：(a) AnimaLoraStudio 明确写"Anima 与 Krea 2 两族都是 28 层"；(b) nomadoor 的 ComfyUI 中文文档把 Aesthetic v1.1 放在同一 `diffusion_models/` 且共用同一 VAE/TE；(c) 官方模型卡说明 Aesthetic 是 base 的美学微调版。**建议**：训练完后用 `safetensors` 读一下 LoRA 的 key 里最大 `blocks.N` 是否为 27，并同时挂到 Aesthetic v1.1 上肉眼比对——若不匹配会立刻表现为"崩坏"而非静默失败。
3. **kohya `anima_train_network.py` 在 8GB 上 `--blocks_to_swap=28` 的实测未找到。** AnimaLoraStudio 的 28 层全换出数据来自它自己的实现，不是 sd-scripts。sd-scripts 的 block swap 在 Anima 上是否等价高效，需要你自己 smoke test 验证；若 sd-scripts 路径不顺，退到 AnimaLoraStudio / TrainFlow。
4. **`--cache_text_encoder_outputs` 与 caption shuffle / tag dropout 的互斥**意味着你没法同时享受"缓存提速"和"caption 打乱"。AnimaLoraStudio 声称其缓存方案支持 shuffle variants（`use_shuffled_caption_variants = true`），但这是它的私有实现，不是 sd-scripts 行为。**若用 sd-scripts，需要接受这个 trade-off。**
5. **画风 LoRA 的最优 rank/LR 没有共识。** 官方给的是"rank 32 → 2e-5"，中文社区给的是"画风 rank 8–16"，英文社区给的是"dim 32 是必须的（相对 SDXL 的 16）"。这三个说法互相冲突。**结论**：先用 **dim16/alpha16/lr 2e-5** 跑一次基线，再用 dim32/lr 2e-5 跑一次，对比后定方向。
6. **Anima-3.8B 的 40→52 manifest 是社区反推的**（官方只发布了 28→40）。如果未来 52 层成为主流，跨代可靠性会打折扣。

**建议的下一步**：
- 先只做一件事：在 AnimaLoraStudio 或 TrainFlow 里跑 **20 步 smoke test**，量出 it/s 和峰值显存。所有时间估算都以此为基准重算。
- 同时打开官方示例画风 LoRA（civitai 2536147）看它的 caption 文件，直接对齐官方实际做法，比读任何二手教程都可靠。

---

## Supervisor coordination

未调用 `contact_supervisor`。任务范围清晰（纯调研 + 写指定路径），无需阻塞性决策；所有必要的范围判断（如"remap 是否需要"、"哪条工具链优先"）都在报告内以显式可信度标注给出了结论，未发现需要改变计划的新情况。

---

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "research.md 已写入 C:\\Users\\asus\\RiderProjects\\STS2 Momoi\\research.md。5 个问题全部回答并给出可执行步骤清单：Q1 工具支持矩阵（含 sd-scripts/diffusion-pipe/musubi-tuner/ComfyUI 节点/第三方 GUI 的支持状态与依据）；Q2 数据集规模 (50-300 张/1024²/WD14 打标/@ 前缀触发词/画风 caption 三段策略)；Q3 8GB 配置（blocks_to_swap=28 实测 5.2GB→1.84GB、bf16 必需、fp16 禁用、互斥参数清单）；Q4 ComfyUI 加载（LoraLoaderModelOnly 可用、DiT-only 无需转换、28/40/52 remap 仅在跨代时需要）；Q5 中文教程清单（8 个中文资源含 3 个 B站/YouTube 视频）。每条结论标注 [官方]/[社区-高]/[社区-中]/[推断] 可信度并附 URL。"
    }
  ],
  "changedFiles": [
    "C:\\Users\\asus\\RiderProjects\\STS2 Momoi\\research.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "web_search (4 angles: Anima LoRA training tools; datasets/captioning; 8GB VRAM settings; ComfyUI loading + block remap)",
      "result": "passed",
      "summary": "32 sources; 确认官方训练路径、工具支持矩阵、remap 工具谱系"
    },
    {
      "command": "web_search (4 angles: diffusion-pipe VRAM; ComfyUI Anima LoRA loading; musubi-tuner/kohya_ss support; LLLite low-vram)",
      "result": "passed",
      "summary": "24 sources; 确认 musubi-tuner 不支持 Anima、sd-scripts assert 级互斥约束、diffusion-pipe block swap 未覆盖 Anima"
    },
    {
      "command": "web_search (4 angles: 中文 8G 显存实操; 低端 GPU 训练时长; 4060 出图速度; lora-scripts-next 中文整合包)",
      "result": "passed",
      "summary": "24 sources; 拿到 4060 Laptop 8GB 出图实测 55s/张、TrainFlow 3060 12GB ~1 小时、Colab T4 1000步>4小时 三个时间锚点"
    },
    {
      "command": "get_search_content (fetch 3 primary sources: HF Anima README, AnimaLoraStudio training-tips.md, HF discussion #106)",
      "result": "passed",
      "summary": "取得官方原文 Finetuning Tips 与 @ 画师 tag 规范、28 层全换出 1.84GB 实测数据、画风 caption 对照表"
    },
    {
      "command": "fetch_content (direct URL fetch of kohya docs / HF README / GitHub READMEs)",
      "result": "failed",
      "summary": "全部返回 'Blocked internal address for github.com/huggingface.co: 127.0.0.1'；改由 get_search_content 从搜索缓存取回同一内容，未损失信息"
    }
  ],
  "validationOutput": [
    "research.md 已落盘于指定的运行时输出路径 C:\\Users\\asus\\RiderProjects\\STS2 Momoi\\research.md",
    "报告结构：Summary / 前提纠正（3 项）/ Q1-Q5 五节 / 可执行步骤清单（5 阶段） / Sources（Kept + Dropped）/ Gaps（6 项）/ acceptance-report",
    "证据密度：全部结论带行内 URL 引用；关键数字（1.84GB 峰值、55s/张、2e-5 LR、28 层、6GB 级可跑）均可追溯到具体来源",
    "主动纠正了 3 处任务前提错误：VAE 不是 Wan2.1 而是 qwen_image_vae.safetensors；Anima 不能 fp16 训练；28/40/52 remap 在同代使用下不适用",
    "排查并标注了 4 个共享逐字相同 README 的 anima_lora 镜像仓库（supply-chain 风险）"
  ],
  "residualRisks": [
    "8GB（RTX 4060 Laptop）上 Anima LoRA 训练的具体 it/s 无公开实测数据；报告给出的 1-3 小时/1000-1500 步 @768 为推断值（基于 5090 block-swap 显存数据 + 3060 12GB '1 小时' + T4 '1000 步>4 小时' 三点外推），可能偏差 2x",
    "Anima-Aesthetic v1.1 为 28 层的结论来自间接证据（AnimaLoraStudio 明述 + ComfyUI 文档共用同一 VAE/TE + 官方称其为 base 的微调版），未拿到直接读数验证；报告已给出自查方法（读 LoRA key 最大 blocks.N）",
    "sd-scripts 的 --blocks_to_swap 在 Anima 上是否与 AnimaLoraStudio 自研实现的 28 层全换出等效，未找到实测；若 sd-scripts 路径在 8GB 上不顺，需退到 AnimaLoraStudio / TrainFlow",
    "第三方 trainer 仓库存在明显的镜像/搬运生态（4 个 anima_lora 仓库逐字相同 README、TrainFlow 在多个 owner 名下、n0va39/l2dnjsrud 为 sorryhyun 副本）；若用户从错误镜像下载便携包，存在恶意构建风险",
    "画风 LoRA 的最优 rank 存在官方（32）与中文社区（8-16）的明确冲突，报告未能给出确定答案，只给出 A/B 基线方案",
    "Anima-3.8B 的 40→52 block manifest 为社区反推（官方仅发布 28→40），若未来 52 层成为主流，跨代重映射可靠性存疑"
  ],
  "noStagedFiles": true,
  "diffSummary": "新增单个文件 research.md（约 480 行）。内容为 Anima 画风 LoRA 本地训练可行性调研报告：前提纠正、5 个问题的分节回答（工具矩阵/数据集与打标/8GB 配置/ComfyUI 加载与 block 重映射澄清/中文教程）、5 阶段可执行步骤清单、来源分级（Kept/Dropped）与 6 项 Gaps。未修改任何既有文件。",
  "reviewFindings": [
    "no blockers",
    "info: research.md:1 - 输出路径已按要求精确写入 C:\\Users\\asus\\RiderProjects\\STS2 Momoi\\research.md（运行时覆盖路径），未写入任何其他文件名或路径",
    "info: research.md 第 0 节 - 主动纠正任务前提 3 处错误（VAE 文件名、fp16 不可用、remap 适用条件），避免用户下载错误 VAE 或浪费精力在不需要的 remap 插件上",
    "warning: research.md 第 1.3 节 - 发现 4 个 anima_lora 仓库共享逐字相同 README，以及 TrainFlow 在 3 个 owner 名下镜像发布；已在报告中作为 supply-chain 风险和仓库可信度警告显式标注，并写入 residualRisks",
    "warning: research.md 第 3.3 节 - 训练时长标注为 [推断]，因为不存在 8GB 卡上的 Anima LoRA 训练实测；已在 Gaps #1 与 residualRisks 中双重标注，并建议先跑 20 步 smoke test 实测 it/s",
    "note: research.md Sources - 明确列出 11 类 Dropped 来源及排除理由（逐字重复的镜像仓库、营销性虚假声明 'only trainer that natively supports Anima'、推理侧内容、SEO 商品页、聚合转载站），便于父级复查筛选逻辑"
  ],
  "manualNotes": "三点请父级注意：(1) 任务给出的环境描述与公开资料有轻微出入——用户说秋叶整合包 v3.2 / ComfyUI 0.30.2 / Python 3.11-3.12，但公开资料显示秋叶 ComfyUI 3.0 为 ComfyUI v0.9.2 / Python 3.13.11 / torch 2.9.1+cu130；这不影响结论，因为调研的核心建议是训练必须用独立便携包、不要往整合包 embedded Python 里装依赖。(2) 报告对 remap 问题的结论是本次调研最有价值的纠正：用户花费大量篇幅询问 28/40/52 层映射，但官方 Anima 全系（base/Aesthetic/Turbo）同为 28 层，同代训练+使用完全不需要 remap，标准 LoraLoaderModelOnly 直接可用。(3) 最省事的落地路径排序为：Anima-TrainFlow 便携包（6GB+、内置 WD14、~1 小时）≈ lora-scripts-next 中文整合包（中文 GUI + 中文文档，但默认 preset ~12GB 需手动开 block swap）> kohya-ss/sd-scripts 裸装（最可信 flags，无 GUI）。不推荐 diffusion-pipe（DeepSpeed/Linux 化、block swap 未覆盖 Anima）与 musubi-tuner（不支持 Anima）。"
}
```
