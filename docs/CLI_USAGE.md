# 📚 ai-media CLI Usage & Python API Documentation

🌐 **[简体中文](CLI_USAGE_ZH.md)** | **English** | **[Architecture Spec](ARCHITECTURE.md)** | **[Home](../README.md)**

Welcome to `ai-media` (media-pipeline-cli). This guide provides comprehensive instructions on CLI options, Python API integration, and performance best practices.

---

## Table of Contents

- [1. Installation & Dependencies](#1-installation--dependencies)
- [2. CLI Usage Reference](#2-cli-usage-reference)
  - [ai-media log - Real-Time Streaming Logs](#ai-media-log---real-time-streaming-logs)
  - [ai-media photo - Batch AI Photo Upscaling](#ai-media-photo---batch-ai-photo-upscaling)
  - [ai-media video - Video 120fps & 10-bit HDR Pipeline](#ai-media-video---video-120fps--10-bit-hdr-pipeline)
- [3. Python API Integration](#3-python-api-integration)
- [4. Breakpoint Resume & Performance](#4-breakpoint-resume--performance)

---

## 1. Installation & Dependencies

```bash
# Global Installation via Git
pip install git+https://github.com/Francis-Xavier-code/media-pipeline-cli.git

# Local Development Mode
git clone https://github.com/Francis-Xavier-code/media-pipeline-cli.git
cd media-pipeline-cli
pip install -e .
```

### Portable Executable Binaries
- `realesrgan-ncnn-vulkan.exe` (Real-ESRGAN GPU Super-Resolution)
- `rife-ncnn-vulkan.exe` (RIFE Optical-Flow Frame Interpolation)
- `ffmpeg.exe` (Static FFmpeg with NVENC 10-bit HDR support)

---

## 2. CLI Usage Reference

### `ai-media log` - Real-Time Streaming Logs

Watches the background media processing task in real time with UTF-8 encoding.

```bash
ai-media log
```

### `ai-media photo` - Batch AI Photo Upscaling

```bash
ai-media photo \
  --input "./photos" \
  --output "./photos_4k" \
  --exe "./bin/realesrgan-ncnn-vulkan.exe" \
  --gpu 0 \
  --scale 4
```

### `ai-media video` - Video 120fps & 10-bit HDR Pipeline

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

## 3. Python API Integration

```python
from ai_media_upscaler import PhotoUpscaleEngine, VideoEnhanceEngine

# Photo Engine
photo_engine = PhotoUpscaleEngine(exe_path="./bin/realesrgan-ncnn-vulkan.exe", gpu_id=0, scale=4)
photo_engine.batch_process(input_dir="./my_photos", output_dir="./my_photos_4k", deduplicate=True)

# Video Engine
video_engine = VideoEnhanceEngine(rife_exe="./bin/rife-ncnn-vulkan.exe", ffmpeg_exe="ffmpeg", gpu_id=0, target_fps=120, enable_hdr=True)
video_engine.process_single_video(vpath="./input.mp4", index=1, total=1, output_dir="./output_hdr")
```

---

## 4. Breakpoint Resume & Performance

1. **Automatic Breakpoint Resume**: Skipping already completed 100% finished files instantly upon re-execution.
2. **Tiling Protection**: Fixed VRAM consumption at ~3 GB using `-t 256` tiling chunks.
