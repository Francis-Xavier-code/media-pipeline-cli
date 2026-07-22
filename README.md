# ✨ AI Media Upscaler CLI

🌐 **[简体中文](README_ZH.md)** | **English** | **[📚 Documentation Directory (docs/)](docs/CLI_USAGE.md)** | **[🏗️ Architecture Spec](docs/ARCHITECTURE.md)** | **[📦 Releases](https://github.com/Francis-Xavier-code/media-pipeline-cli/releases)**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](#)
[![GPU Accelerated](https://img.shields.io/badge/GPU-Vulkan%20%7C%20NVENC%20%7C%20Metal-green.svg)](#)
[![Agent Skill](https://img.shields.io/badge/AI%20Agent-Zero%20Clone%20Ready-purple.svg)](skills/media-upscaler/SKILL.md)

> **GPU-Accelerated Cross-Platform (Windows, Linux, macOS) Photo 4K/8K AI Super-Resolution and Video 120fps HDR Interpolation CLI.**

`media-pipeline` (ai-media) is a high-performance, lightweight CLI tool for batch upgrading photos and videos using GPU hardware acceleration (Vulkan, Apple Metal, NVIDIA NVENC & macOS VideoToolbox).

---

## 🤖 Zero-Manual-Clone 1-Sentence Prompt for AI Agents (OpenClaw / Claude / Cursor / AGY)

Users **do NOT need to manually clone** the repository. Give this 1-sentence prompt inside a copy-paste code block directly to any AI Agent:

```bash
Read https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/skills/media-upscaler/SKILL.md, auto-install it, and use GPU AI to batch upscale my photos and videos to 4K 120fps HDR.
```

---

## ⚡ 1-Line Online Installers

No manual `git clone` needed! Run this 1-line script in your terminal to auto-install:

### 🪟 Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.ps1 | iex
```

### 🐧 Linux & 🍎 macOS (Terminal / Bash):
```bash
curl -fsSL https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.sh | bash
```

---

## 💻 Cross-Platform Compatibility Matrix

| OS Platform | GPU API | Video Encoder |
| :--- | :--- | :--- |
| **🪟 Windows** | Vulkan (NVIDIA / AMD / Intel) | NVIDIA NVENC (`hevc_nvenc`) |
| **🐧 Linux** | Vulkan API | NVIDIA NVENC / VAAPI |
| **🍎 macOS (Apple Silicon M1/M2/M3/M4 & Intel)** | Apple Metal / MoltenVK | macOS VideoToolbox (`hevc_videotoolbox`) |

---

## 📦 GitHub Releases (v1.0.0)

Official release assets and changelogs are available on **[GitHub Releases (v1.0.0)](https://github.com/Francis-Xavier-code/media-pipeline-cli/releases)**.

---

## 🖼️ Before vs After Preview

![AI Before vs After Visual Comparison Banner](assets/comparison_banner.jpg)

---

## 🚀 CLI Usage

```bash
# 1. Watch Logs
ai-media log

# 2. Photo Upscaling
ai-media photo -i "./input_photos" -o "./output_photos" --exe "./realesrgan-ncnn-vulkan"

# 3. Video 120fps & HDR
ai-media video -i "./input_video.mp4" -o "./output_video" --exe "./rife-ncnn-vulkan" --fps 120 --hdr
```

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
