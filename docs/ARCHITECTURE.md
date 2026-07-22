# 🏗️ System Architecture & Hardware Acceleration Specification

🌐 **[简体中文](ARCHITECTURE_ZH.md)** | **English** | **[CLI Guide](CLI_USAGE.md)** | **[Home](../README.md)**

This document details the internal design, Vulkan GPU tiling protection, RIFE optical-flow interpolation, and 10-bit HDR NVENC pipeline of `media-pipeline-cli`.

---

## 📐 1. Architecture Flowchart

```mermaid
graph TD
    A["Raw Media Input (Photos / Videos)"] --> B["Python CLI Controller (ai-media)"]
    B --> C["MD5 Binary Deduplication Engine"]
    C -->|Photo Queue| D["Real-ESRGAN Vulkan GPU Engine (-t 256 Tiling)"]
    C -->|Video Queue| E["FFmpeg Frame Extraction"]
    E --> F["RIFE Vulkan Optical-Flow GPU Interpolation Engine (120fps)"]
    F --> G["NVIDIA NVENC 10-bit HDR10 Encoder (scale=iw*2:ih*2)"]
    D --> H["Ultra-HD PNG Storage"]
    G --> I["Ultra-HD 120fps HDR MP4 Storage"]
```

---

## 🔒 2. Key Technical Innovations

1. **MD5 Photo Deduplication**: Pre-computes MD5 hashes to skip binary duplicate files (`file.jpg` vs `file(1).jpg`), saving 50%+ rendering time.
2. **Vulkan Tiling Protection (`-t 256`)**: Locks VRAM consumption at ~3 GB regardless of output resolution, eliminating CUDA Out-of-Memory crashes.
3. **Aspect-Ratio Safe Scaling (`scale=iw*2:ih*2`)**: Auto-detects portrait vs landscape aspect ratio.
4. **10-bit HDR10 NVENC Acceleration**: Hardware encodes 10.7 billion colors (`yuv420p10le`, BT.2020, SMPTE 2084).
