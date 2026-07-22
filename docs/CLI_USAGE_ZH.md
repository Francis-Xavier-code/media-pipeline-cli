# 📚 ai-media CLI 完整命令行与 Python API 使用指南

🌐 **简体中文** | **[English](CLI_USAGE.md)** | **[系统架构设计](ARCHITECTURE_ZH.md)** | **[主页](../README_ZH.md)**

欢迎使用 `ai-media` (media-pipeline-cli)！本文档详细介绍了命令行参数、高级配置、跨平台依赖自动补全、AI Agent 系统自动区分规范及最佳实践。

---

## 目录

- [一、全局安装与环境依赖](#一全局安装与环境依赖)
- [二、CLI 命令行详细说明](#二cli-命令行详细说明)
  - [1. `ai-media log` - 实时日志监视](#1-ai-media-log---实时日志监视)
  - [2. `ai-media photo` - 批量图片 AI 超分](#2-ai-media-photo---批量图片-ai-超分)
  - [3. `ai-media video` - 视频 120帧与 10-bit HDR 重构](#3-ai-media-video---视频-120帧与-10-bit-hdr-重构)
- [三、Python API 开发调用](#三python-api-开发调用)
- [四、智能断点续传与性能优化](#四智能断点续传与性能优化)
- [五、跨平台依赖补全与 AI Agent 系统识别规范](#五跨平台依赖补全与-ai-agent-系统识别规范)

---

## 一、全局安装与环境依赖

### ⚡ 1 行在线一键安装
```bash
# Windows (PowerShell)
irm https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.ps1 | iex

# Linux & macOS (Bash)
curl -fsSL https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.sh | bash
```

---

## 二、CLI 命令行详细说明

### 1. `ai-media log` - 实时日志监视

```bash
ai-media log
```

### 2. `ai-media photo` - 批量图片 AI 超分

```bash
ai-media photo \
  --input "./photos" \
  --output "./photos_4k" \
  --exe "./bin/realesrgan-ncnn-vulkan.exe" \
  --gpu 0 \
  --scale 4
```

### 3. `ai-media video` - 视频 120帧与 10-bit HDR 重构

```bash
ai-media video \
  --input "./input_videos" \
  --output "./output_videos_hdr" \
  --exe "./bin/rife-ncnn-vulkan.exe" \
  --gpu 0 \
  --fps 120 \
  --hdr
```

---

## 三、Python API 开发调用

```python
from ai_media_upscaler import PhotoUpscaleEngine, VideoEnhanceEngine

# 1. 图片超分
photo_engine = PhotoUpscaleEngine(exe_path="./bin/realesrgan-ncnn-vulkan.exe", gpu_id=0, scale=4)
photo_engine.batch_process(input_dir="./photos", output_dir="./photos_4k", deduplicate=True)

# 2. 视频补帧与 HDR
video_engine = VideoEnhanceEngine(rife_exe="./bin/rife-ncnn-vulkan.exe", ffmpeg_exe="ffmpeg", gpu_id=0, target_fps=120, enable_hdr=True)
video_engine.process_single_video(vpath="./input.mp4", index=1, total=1, output_dir="./output_hdr")
```

---

## 四、智能断点续传与性能优化

1. **断点续传**：CLI 自动检测目标目录，若目标文件已存在且大小正常，将秒级跳过，支持任意时刻中断接力。
2. **显存保护 (VRAM Safety)**：Real-ESRGAN 自动开启 `-t 256` 显存切块渲染，显存占用锁定在 ~3GB，零 Out-of-Memory 崩溃风险。

---

## 五、跨平台依赖补全与 AI Agent 系统识别规范

### 🤖 AI Agent 系统自动区分逻辑
当把在线一句话指令发送给 OpenClaw / Claude Code / Cursor / AGY 等 AI Agent 时，Agent 会读取 `skills/media-upscaler/SKILL.md` 规范，**自动识别宿主操作系统**：

1. **🪟 Windows 系统**：
   - 自动检测并下载 Windows 版 `realesrgan-ncnn-vulkan.exe`、`rife-ncnn-vulkan.exe` 和静态 `ffmpeg.exe`。
   - 自动在注册表中更新 `PATH` 环境变量。

2. **🐧 Linux 系统**：
   - 自动通过包管理器补全 FFmpeg：`sudo apt-get install -y ffmpeg`。
   - 自动解压下载 Linux 原生无后缀二进制文件 `realesrgan-ncnn-vulkan-ubuntu` 与 `rife-ncnn-vulkan-ubuntu` 并赋予 `chmod +x` 执行权限。

3. **🍎 macOS 系统 (Apple Silicon Metal & Intel)**：
   - 自动通过 Homebrew 补全 FFmpeg：`brew install ffmpeg`。
   - 自动解压下载 macOS 原生 Metal 硬件加速二进制文件 `realesrgan-ncnn-vulkan-macos` 与 `rife-ncnn-vulkan-macos`。
