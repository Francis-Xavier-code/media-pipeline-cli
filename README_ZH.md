# ✨ AI Media Upscaler CLI (媒体 AI 画质重构工具)

🌐 **简体中文** | **[English](README.md)** | **[📚 完整文档目录 (docs/)](docs/CLI_USAGE_ZH.md)** | **[🏗️ 系统架构设计](docs/ARCHITECTURE_ZH.md)** | **[📦 Releases (发布包)](https://github.com/Francis-Xavier-code/media-pipeline-cli/releases)**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](#)
[![GPU Accelerated](https://img.shields.io/badge/GPU-Vulkan%20%7C%20NVENC%20%7C%20Metal-green.svg)](#)
[![Hardware Safety](https://img.shields.io/badge/Hardware%20Safety-CPU%20Fallback%20Net-orange.svg)](#)
[![Agent Skill](https://img.shields.io/badge/AI%20Agent-Zero%20Clone%20Ready-purple.svg)](skills/media-upscaler/SKILL.md)

> **基于 GPU 硬件加速 + CPU 软硬件全自动保底的跨平台 (Windows / Linux / macOS) 媒体 AI 重构与全生命周期后台进程管理工具。**

---

## ⚡ 1 行在线一键安装 (1-Line Online Installer)

在任意终端窗口中直接复制运行，无需手动克隆仓库，即装即用：

### 🪟 Windows (在 PowerShell 中运行):
```powershell
irm https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.ps1 | iex
```

### 🐧 Linux & 🍎 macOS (在 Terminal 终端中运行):
```bash
curl -fsSL https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.sh | bash
```

---

## ⚙️ 守护进程与全生命周期管理指令 (Daemon Process & Lifecycle Management)

提供完整的系统级后台进程管控命令，支持查杀、断点接力、缓存清理与干净卸载：

```bash
# 1. 📊 查看后台渲染状态 (进程 PID、活动状态、最新渲染动态)
ai-media status

# 2. 🛑 强力停止后台渲染进程
ai-media stop

# 3. 🧹 停止后台进程 + 全自动清空中间临时缓存文件夹 (E:\_tmp_rife_in 等)
ai-media clean

# 4. 🚀 从断点无缝恢复/继续后台渲染 (秒级跳过已完成文件)
ai-media continue

# 5. 🔄 重启后台渲染进程 (自动强制重置并接力断点)
ai-media restart

# 6. 📺 实时查看无乱码 UTF-8 流式渲染日志 (按 Ctrl+C 优雅退出)
ai-media log

# 7. 🗑️ 停止进程 + 清理缓存 + 一键干净卸载 ai-media (零残留)
ai-media uninstall
```

---

## 🤖 零手动克隆 · 一句话给 AI Agent 自动搞定 (支持 OpenClaw / Claude Code / Cursor / AGY 等)

用户**无需手动克隆仓库**，直接在聊天框中**点击复制**下面代码块里的【一句话指令】发送给任意 AI Agent，AI 就会自动远程读取规范、安装环境并执行渲染：

```bash
请读取远程规范 https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/skills/media-upscaler/SKILL.md ，自动帮我安装并使用 GPU/CPU 自动保底机制将指定目录下的图片和视频批量重构为 4K 120帧 HDR 画质。
```

---

## 🛡️ 软硬件三级保底降级机制 (Zero-Crash Hardware Safety Net)

针对低配电脑、无独显笔记本、过老集显或无 GPU 的云服务器，系统构建了全自动软硬件降级链：

```mermaid
graph TD
    A["开始处理媒体文件"] --> B{"1. GPU Vulkan 硬件检测"}
    B -->|支持| C["GPU Vulkan 硬件加速 (-g 0)"]
    B -->|不支持 / 无独显| D["⚠️ 自动降级: CPU 多线程 AI 模式 (-g -1)"]
    
    C --> E{"2. 视频编码器硬件检测"}
    D --> E
    
    E -->|NVIDIA GPU| F["NVIDIA NVENC 硬件编码 (hevc_nvenc)"]
    E -->|Apple Silicon| G["Apple VideoToolbox 硬件编码 (hevc_videotoolbox)"]
    E -->|集显 / 无 GPU| H["⚠️ 自动降级: CPU 通用软件编码 (libx265 / libx264)"]
    
    F --> I["🎉 100% 成功重构输出"]
    G --> I
    H --> I
```

---

## 💻 跨平台支持 (Cross-Platform Matrix)

| 操作系统 | GPU 优先硬件加速 API | CPU 自动保底降级模式 |
| :--- | :--- | :--- |
| **🪟 Windows** | Vulkan (NVIDIA / AMD / Intel) | CPU Multi-threading (`-g -1`) + `libx265` |
| **🐧 Linux (Ubuntu/Debian/Arch)** | Vulkan API | CPU Multi-threading (`-g -1`) + `libx265` |
| **🍎 macOS (Apple Silicon M1/M2/M3/M4 & Intel)** | Apple Metal / MoltenVK | CPU Multi-threading (`-g -1`) + `libx265` |

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

## 🚀 命令行直接调用指南 (CLI Direct Command)

```bash
# 1. 批量图片 AI 4K/8K 超分
ai-media photo -i "./input_photos" -o "./output_photos" --exe "./realesrgan-ncnn-vulkan.exe" --scale 4

# 2. 单个或批量视频 120帧 + 10-bit HDR 重构
ai-media video -i "./input_video.mp4" -o "./output_video" --exe "./rife-ncnn-vulkan.exe" --fps 120 --hdr
```

---

## 📄 开源许可

本项目基于 MIT 许可证开源。详情请参阅 [LICENSE](LICENSE) 文件。
