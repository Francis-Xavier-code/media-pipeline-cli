# ✨ AI Media Upscaler CLI

🌐 **[简体中文](README_ZH.md)** | **English** | **[📚 Documentation Directory (docs/)](docs/CLI_USAGE.md)** | **[🏗️ Architecture Spec](docs/ARCHITECTURE.md)** | **[📦 Releases](https://github.com/Francis-Xavier-code/media-pipeline-cli/releases)**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](#)
[![GPU Accelerated](https://img.shields.io/badge/GPU-Vulkan%20%7C%20NVENC%20%7C%20Metal-green.svg)](#)
[![Hardware Safety](https://img.shields.io/badge/Hardware%20Safety-CPU%20Fallback%20Net-orange.svg)](#)
[![Agent Skill](https://img.shields.io/badge/AI%20Agent-Zero%20Clone%20Ready-purple.svg)](skills/media-upscaler/SKILL.md)

> **GPU-Accelerated & CPU-Fallback Cross-Platform (Windows, Linux, macOS) Photo 4K/8K AI Super-Resolution and Video 120fps HDR Interpolation CLI with Daemon Process Management.**

`media-pipeline` (ai-media) is a high-performance CLI tool featuring **full daemon process control subcommands (`status`, `stop`, `continue`, `restart`)** and a **Triple Hardware CPU Fallback Net** to guarantee **100% execution success with zero crashes**.

---

## ⚙️ Daemon Process Control Subcommands

```bash
# 1. Check live pipeline status (PID, activity, latest progress)
ai-media status

# 2. Gracefully stop the active background pipeline
ai-media stop

# 3. Resume/continue pipeline execution from breakpoint
ai-media continue

# 4. Restart background pipeline from breakpoint
ai-media restart

# 5. Watch live UTF-8 streaming logs
ai-media log
```

---

## 🛡️ Zero-Crash Hardware Fallback Architecture

```mermaid
graph TD
    A["Start Processing Media File"] --> B{"1. GPU Vulkan Check"}
    B -->|Supported| C["GPU Vulkan Mode (-g 0)"]
    B -->|Not Supported / No GPU| D["⚠️ Auto Fallback: CPU Multi-threading (-g -1)"]
    
    C --> E{"2. Video Codec Check"}
    D --> E
    
    E -->|NVIDIA GPU| F["NVIDIA NVENC (hevc_nvenc)"]
    E -->|Apple Silicon| G["Apple VideoToolbox (hevc_videotoolbox)"]
    E -->|No GPU / Old iGPU| H["⚠️ Auto Fallback: CPU Universal Codec (libx265 / libx264)"]
    
    F --> I["🎉 100% Successful Output"]
    G --> I
    H --> I
```

---

## 🤖 Zero-Manual-Clone 1-Sentence Prompt for AI Agents (OpenClaw / Claude / Cursor / AGY)

```bash
Read https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/skills/media-upscaler/SKILL.md, auto-install it, and use GPU/CPU fallback AI to batch upscale my photos and videos to 4K 120fps HDR.
```

---

## ⚡ 1-Line Online Installers

### 🪟 Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.ps1 | iex
```

### 🐧 Linux & 🍎 macOS (Terminal / Bash):
```bash
curl -fsSL https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.sh | bash
```

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
