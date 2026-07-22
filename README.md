# ✨ AI Media Upscaler CLI

🌐 **[简体中文](README_ZH.md)** | **English**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GPU Accelerated](https://img.shields.io/badge/GPU-NVIDIA%20RTX%20Accelerated-green.svg)](#)
[![Agent Skill](https://img.shields.io/badge/AI%20Agent-Zero%20Clone%20Ready-purple.svg)](skills/media-upscaler/SKILL.md)

> **GPU-Accelerated Photo 4K/8K AI Super-Resolution and Video 120fps HDR Interpolation CLI.**

`media-pipeline` (ai-media) is a high-performance, lightweight CLI tool for batch upgrading photos and videos using GPU hardware acceleration (Vulkan & TensorRT).

---

## 🖼️ Before vs After Preview

![AI Before vs After Visual Comparison Banner](assets/comparison_banner.jpg)

---

## ✨ Features

- **⏩ Automatic Breakpoint Resume**: Interruptions, shutdowns, or re-runs instantly skip 100% completed files and resume right where it left off!
- **⚡ Real-Time Streaming Logs**: Instant, unbuffered progress logging with execution time, frame count, and output file sizes.
- **📐 Aspect-Ratio Safe Scaling**: Auto-detects portrait (vertical) vs landscape (horizontal) media, preventing squished or stretched distortion.
- **🖼️ Photo 4K/8K AI Super-Resolution**: Batch upscales images using Real-ESRGAN Vulkan models.
- **🎬 Video 120fps Frame Interpolation**: Interpolates 24fps/30fps videos up to 60fps/120fps using RIFE.
- **🌟 10-bit HDR10 Conversion**: Re-encodes videos to 10-bit HDR using hardware NVENC GPU encoders.
- **🔒 Tiling Protection**: Prevents VRAM Out-of-Memory crashes by processing frames in tile chunks.

---

## 🤖 Zero-Manual-Clone 1-Sentence Prompt for AI Agents (OpenClaw / Claude / Cursor / AGY)

Users **do NOT need to manually clone** the repository. Give this 1-sentence prompt directly to any AI Agent, and it will fetch the raw skill spec, auto-install, and execute:

> 💬 *"Read https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/skills/media-upscaler/SKILL.md, auto-install it, and use GPU AI to batch upscale my photos and videos to 4K 120fps HDR."*

---

## 🛠️ Installation (Optional)

```bash
pip install git+https://github.com/Francis-Xavier-code/media-pipeline-cli.git
```

---

## 🚀 CLI Usage

### 1. Photo 4K/8K AI Upscaling
```bash
ai-media photo \
  --input "./input_photos" \
  --output "./output_4k_photos" \
  --exe "./bin/realesrgan-ncnn-vulkan.exe" \
  --gpu 0 \
  --scale 4
```

### 2. Video 120fps & 10-bit HDR Interpolation
```bash
ai-media video \
  --input "./input_video.mp4" \
  --output "./output_120fps_hdr" \
  --exe "./bin/rife-ncnn-vulkan.exe" \
  --gpu 0 \
  --fps 120 \
  --hdr
```

---

## 🏗️ Architecture

```mermaid
graph TD
    A["Raw Media Files (Photos / Videos)"] --> B["ai-media CLI Controller / AI Agent"]
    B -->|Photo Upscaling| C["Real-ESRGAN Vulkan GPU Engine (4K/8K/16K PNG)"]
    B -->|Video Interpolation| D["RIFE Vulkan GPU Engine (120fps Smoothness)"]
    B -->|10-bit HDR Re-encoding| E["NVIDIA NVENC Hardware Encoder (10-bit HDR10 HEVC)"]
    C --> F["Ultra-HD Output Storage"]
    D --> F
    E --> F
```

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
