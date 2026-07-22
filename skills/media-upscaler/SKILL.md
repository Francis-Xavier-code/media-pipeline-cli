---
name: media-upscaler
description: GPU-Accelerated Photo 4K/8K Super-Resolution & Video 120fps 10-bit HDR Interpolation Agent Skill.
version: 1.0.0
---

# 🚀 Media Upscaler AI Agent Skill

When activated by a user prompt, automatically install the package directly from GitHub and perform GPU-accelerated batch photo super-resolution and video 120fps 10-bit HDR frame interpolation.

## 🛠️ Auto-Installation for AI Agents

AI Agents can automatically install and set up `ai-media` with zero user manual cloning:
```bash
pip install git+https://github.com/Francis-Xavier-code/media-pipeline-cli.git
```

## 📋 Standard Agent Execution Workflow

### 1. Photo Super-Resolution (4K/8K/16K)
Run batch photo upscale with Vulkan Tiling protection:
```bash
ai-media photo --input "<INPUT_DIR>" --output "<OUTPUT_DIR>" --exe "./bin/realesrgan-ncnn-vulkan.exe" --gpu 0 --scale 4
```

### 2. Video 120fps & 10-bit HDR Interpolation
Run video frame interpolation and 10-bit HDR re-encoding:
```bash
ai-media video --input "<INPUT_FILE_OR_DIR>" --output "<OUTPUT_DIR>" --exe "./bin/rife-ncnn-vulkan.exe" --gpu 0 --fps 120 --hdr
```

## 💡 Zero-Manual-Clone 1-Sentence Prompt for Users
Users can copy-paste this single line directly to any AI Agent (OpenClaw, Claude, Cursor, AGY):
> *"Read https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/skills/media-upscaler/SKILL.md, auto-install it, and use GPU AI to batch upscale my photos and videos to 4K 120fps HDR."*
