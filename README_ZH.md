# ✨ AI Media Upscaler CLI (媒体 AI 画质重构工具)

🌐 **简体中文** | **[English](README.md)** | **[📚 完整文档目录 (docs/)](docs/CLI_USAGE_ZH.md)** | **[🏗️ 系统架构设计](docs/ARCHITECTURE_ZH.md)** | **[📦 Releases (发布包)](https://github.com/Francis-Xavier-code/media-pipeline-cli/releases)**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](#)
[![GPU Accelerated](https://img.shields.io/badge/GPU-Vulkan%20%7C%20NVENC%20%7C%20Metal-green.svg)](#)
[![Agent Skill](https://img.shields.io/badge/AI%20Agent-Zero%20Clone%20Ready-purple.svg)](skills/media-upscaler/SKILL.md)

> **基于 GPU 硬件加速的跨平台 (Windows / Linux / macOS) 图片 4K/8K AI 超分辨率重构与视频 120帧 10-bit HDR 补帧渲染工具。**

`media-pipeline` (ai-media) 是一个轻量级、高性能的 Python 命令行工具，利用显卡 GPU 硬件加速（Vulkan, Apple Metal, NVIDIA NVENC & macOS VideoToolbox 芯片），实现照片画质无损放大与视频极致丝滑重构。

---

## ⚡ 1 行在线一键安装脚本 (1-Line Online Installer)

无需手动 `git clone`，直接在终端中复制运行以下 1 行脚本即可全自动安装：

### 🪟 Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.ps1 | iex
```

### 🐧 Linux & 🍎 macOS (Terminal / Bash):
```bash
curl -fsSL https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.sh | bash
```

---

## 💻 跨平台支持 (Cross-Platform Matrix)

| 操作系统 | GPU 硬件加速 API | 视频硬件编码器 |
| :--- | :--- | :--- |
| **🪟 Windows** | Vulkan (NVIDIA / AMD / Intel) | NVIDIA NVENC (`hevc_nvenc`) |
| **🐧 Linux (Ubuntu/Debian/Arch)** | Vulkan API | NVIDIA NVENC / VAAPI |
| **🍎 macOS (Apple Silicon M1/M2/M3/M4 & Intel)** | Apple Metal / MoltenVK | macOS VideoToolbox (`hevc_videotoolbox`) |

---

## 📦 Releases 发布包说明 (Portable Binaries)

我们已经在 **[GitHub Releases (v1.0.0)](https://github.com/Francis-Xavier-code/media-pipeline-cli/releases)** 正式上线官方 Release 发行版本！

您可以前往 [Releases 页面](https://github.com/Francis-Xavier-code/media-pipeline-cli/releases) 查看完整 Changelog 或获取独立二进制依赖：
- **Real-ESRGAN Vulkan**: [Real-ESRGAN Releases](https://github.com/xinntao/Real-ESRGAN/releases)
- **RIFE Vulkan**: [RIFE Releases](https://github.com/nihui/rife-ncnn-vulkan/releases)
- **FFmpeg**: 系统常规安装即可 (`sudo apt install ffmpeg` / `brew install ffmpeg`)

---

## 🖼️ 修复前后画质对比 (Before vs After)

![AI 修复前后画质实测对比](assets/comparison_banner.jpg)

| 📷 修复前 (原始低清/SDR) | ✨ 修复后 (Real-ESRGAN AI 4K/8K 无损重构) |
| :---: | :---: |
| 原图像素较低，纹理模糊 | **像素级细节重写，升级至 13K 超清无损 PNG** |

---

## 📚 详细文档目录 (docs/)

- 📖 **[CLI 命令使用指南 (CLI_USAGE_ZH.md)](docs/CLI_USAGE_ZH.md)**：包含 `photo` / `video` / `log` 参数及 Python API 调用。
- 🏗️ **[系统架构设计说明 (ARCHITECTURE_ZH.md)](docs/ARCHITECTURE_ZH.md)**：包含显存切块保护、光流插帧与 10-bit HDR 加速原理。

---

## 🚀 命令行快速上手 (CLI)

```bash
# 1. 查看实时日志
ai-media log

# 2. 图片 AI 超分
ai-media photo -i "./input_photos" -o "./output_photos" --exe "./realesrgan-ncnn-vulkan"

# 3. 视频 120帧与 HDR 重构
ai-media video -i "./input_video.mp4" -o "./output_video" --exe "./rife-ncnn-vulkan" --fps 120 --hdr
```

---

## 📄 开源许可

本项目基于 MIT 许可证开源。详情请参阅 [LICENSE](LICENSE) 文件。
