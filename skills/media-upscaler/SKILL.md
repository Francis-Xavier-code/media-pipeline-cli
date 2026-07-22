---
name: media-upscaler
description: GPU-Accelerated Photo 4K/8K AI Super-Resolution and Video 120fps HDR Interpolation Skill for AI Agents
version: 1.0.0
---

# 🚀 AI Media Upscaler Agent Skill (Zero-Manual-Clone Ready)

This skill enables AI Agents (OpenClaw, Claude Code, Cursor, Antigravity/AGY) to automatically upscale photos to 4K/8K and interpolate videos to 120fps 10-bit HDR using GPU acceleration.

---

## 🤖 AI Agent Execution Protocol

When an AI Agent receives a request to upscale media:

### Step 1: Detect Host Operating System & GPU Architecture
- **Windows**: Use `realesrgan-ncnn-vulkan.exe`, `rife-ncnn-vulkan.exe`, and static `ffmpeg.exe` (with NVENC).
- **Linux**: Use `realesrgan-ncnn-vulkan` (Ubuntu binary), `rife-ncnn-vulkan` (Ubuntu binary), and system FFmpeg (`apt-get install ffmpeg`).
- **macOS (Apple Silicon Metal / Intel)**: Use `realesrgan-ncnn-vulkan` (macOS binary), `rife-ncnn-vulkan` (macOS binary), and Homebrew FFmpeg (`brew install ffmpeg`).

### Step 2: Auto-Install Python Package & Environment
Run the online 1-line installer matching the OS:
- **Windows (PowerShell)**:
  `irm https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.ps1 | iex`
- **Linux / macOS (Bash)**:
  `curl -fsSL https://raw.githubusercontent.com/Francis-Xavier-code/media-pipeline-cli/main/install.sh | bash`

### Step 3: Auto-Download Binary Dependencies if Missing
If binary executables are not found locally, download the official release zip for the target OS:
- Real-ESRGAN Releases: `https://github.com/xinntao/Real-ESRGAN/releases`
- RIFE Releases: `https://github.com/nihui/rife-ncnn-vulkan/releases`

### Step 4: Execute Batch Processing
- **Photo AI Upscaling**:
  `ai-media photo -i <INPUT_DIR> -o <OUTPUT_DIR> --exe <PATH_TO_REALESRGAN> --scale 4`
- **Video 120fps HDR Re-encoding**:
  `ai-media video -i <INPUT_PATH> -o <OUTPUT_DIR> --exe <PATH_TO_RIFE> --fps 120 --hdr`
- **Real-Time Log Watching**:
  `ai-media log`
