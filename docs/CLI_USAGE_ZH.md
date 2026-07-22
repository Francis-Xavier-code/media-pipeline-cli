# 📚 ai-media CLI 完整命令行与 Python API 使用指南

🌐 **简体中文** | **[English](CLI_USAGE.md)** | **[系统架构设计](ARCHITECTURE_ZH.md)** | **[主页](../README_ZH.md)**

欢迎使用 `ai-media` (media-pipeline-cli)！本文档详细介绍了命令行参数、高级配置、Python API 调用及最佳实践。

---

## 目录

- [一、全局安装与环境依赖](#一全局安装与环境依赖)
- [二、CLI 命令行详细说明](#二cli-命令行详细说明)
  - [1. `ai-media log` - 实时日志监视](#1-ai-media-log---实时日志监视)
  - [2. `ai-media photo` - 批量图片 AI 超分](#2-ai-media-photo---批量图片-ai-超分)
  - [3. `ai-media video` - 视频 120帧与 10-bit HDR 重构](#3-ai-media-video---视频-120帧与-10-bit-hdr-重构)
- [三、Python API 开发调用](#三python-api-开发调用)
- [四、智能断点续传与性能优化](#四智能断点续传与性能优化)

---

## 一、全局安装与环境依赖

使用 `pip` 可进行全局安装或开发模式安装：

```bash
# 1. 远程一键安装
pip install git+https://github.com/Francis-Xavier-code/media-pipeline-cli.git

# 2. 本地开发模式安装
git clone https://github.com/Francis-Xavier-code/media-pipeline-cli.git
cd media-pipeline-cli
pip install -e .
```

### 可执行依赖文件（Portable Binaries）
`ai-media` 依赖 Vulkan GPU 可执行文件：
- **图片超分**：`realesrgan-ncnn-vulkan.exe`
- **视频插帧**：`rife-ncnn-vulkan.exe`
- **视频重编码**：`ffmpeg.exe` (支持 NVENC 硬件加速)

---

## 二、CLI 命令行详细说明

### 1. `ai-media log` - 实时日志监视

用于实时流式查看正在后台运行的媒体处理日志，具备自动 UTF-8 字符集无乱码输出保障。

```bash
# 默认监视后台日志
ai-media log

# 监视指定日志文件
ai-media log --file "/path/to/custom.log"
```

### 2. `ai-media photo` - 批量图片 AI 超分

将低清晰度照片通过 Real-ESRGAN Vulkan GPU 引擎重构为 4K/8K/16K 超高清 PNG 无损画质。

```bash
ai-media photo \
  --input "./photos" \
  --output "./photos_4k" \
  --exe "./bin/realesrgan-ncnn-vulkan.exe" \
  --gpu 0 \
  --scale 4
```

| 参数 | 缩写 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `--input` | `-i` | *(必填)* | 原始照片输入目录 |
| `--output` | `-o` | *(必填)* | 修复后的 4K/8K 照片输出目录 |
| `--exe` | - | *(必填)* | `realesrgan-ncnn-vulkan.exe` 路径 |
| `--gpu` | - | `0` | GPU 设备 ID (0 为主显卡) |
| `--scale` | - | `4` | 放大倍率 (2, 4, 8) |
| `--no-dedupe` | - | `False` | 禁用 MD5 二进制文件去重 |

### 3. `ai-media video` - 视频 120帧与 10-bit HDR 重构

对视频进行 RIFE 深度学习光流 120帧插帧、自适应比例防变形 4K 升级与 10-bit HDR10 (10.7亿色) 重新编码。

```bash
ai-media video \
  --input "./input_videos" \
  --output "./output_videos_hdr" \
  --exe "./bin/rife-ncnn-vulkan.exe" \
  --gpu 0 \
  --fps 120 \
  --hdr
```

| 参数 | 缩写 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `--input` | `-i` | *(必填)* | 原始视频目录或单文件路径 |
| `--output` | `-o` | *(必填)* | 重构后的 120帧 HDR 视频目录 |
| `--exe` | - | *(必填)* | `rife-ncnn-vulkan.exe` 路径 |
| `--gpu` | - | `0` | GPU 设备 ID |
| `--fps` | - | `120` | 目标帧率 (60, 120) |
| `--hdr` | - | `False` | 开启 10-bit HDR10 色彩编码 |

---

## 三、Python API 开发调用

您可以在自己的 Python 项目中直接导入 `ai_media_upscaler` 引擎模块：

```python
from ai_media_upscaler import PhotoUpscaleEngine, VideoEnhanceEngine

# 1. 初始化图片超分引擎
photo_engine = PhotoUpscaleEngine(
    exe_path="./bin/realesrgan-ncnn-vulkan.exe",
    gpu_id=0,
    scale=4
)
photo_engine.batch_process(
    input_dir="./my_photos",
    output_dir="./my_photos_4k",
    deduplicate=True
)

# 2. 初始化视频补帧与 HDR 引擎
video_engine = VideoEnhanceEngine(
    rife_exe="./bin/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe",
    ffmpeg_exe="ffmpeg",
    gpu_id=0,
    target_fps=120,
    enable_hdr=True
)
video_engine.process_single_video(
    vpath="./input.mp4",
    index=1,
    total=1,
    output_dir="./output_hdr"
)
```

---

## 四、智能断点续传与性能优化

1. **断点续传**：CLI 自动检测目标目录，若目标文件已存在且大小正常，将秒级跳过，支持任意时刻中断接力。
2. **显存保护 (VRAM Safety)**：Real-ESRGAN 自动开启 `-t 256` 显存切块渲染，显存占用锁定在 ~3GB，零 Out-of-Memory 崩溃风险。
