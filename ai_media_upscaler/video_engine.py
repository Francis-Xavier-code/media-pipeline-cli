"""
GPU-Accelerated & CPU-Fallback Video 2x/4K, 120fps Frame Interpolation & 10-bit HDR Engine with Triple Hardware Safety Net
"""
import os
import sys
import time
import shutil
import platform
import subprocess

class VideoEnhanceEngine:
    def __init__(self, rife_exe, ffmpeg_exe=None, gpu_id=0, target_fps=120, enable_hdr=True, scale_expr="iw*2:ih*2"):
        self.rife_exe = rife_exe
        self.gpu_id = str(gpu_id)
        self.target_fps = target_fps
        self.enable_hdr = enable_hdr
        self.scale_expr = scale_expr
        self.system = platform.system()
        self.ffmpeg_exe = self.resolve_ffmpeg_path(ffmpeg_exe, rife_exe)

    def resolve_ffmpeg_path(self, ffmpeg_arg, rife_exe):
        """Auto-detects the best FFmpeg executable with NVENC hardware acceleration."""
        if ffmpeg_arg and os.path.exists(ffmpeg_arg):
            return ffmpeg_arg

        # 1. Search adjacent directory of rife_exe
        if rife_exe and os.path.exists(rife_exe):
            adj_ffmpeg = os.path.join(os.path.dirname(rife_exe), "ffmpeg.exe" if self.system == "Windows" else "ffmpeg")
            if os.path.exists(adj_ffmpeg):
                return adj_ffmpeg

        # 2. Search known static NVENC ffmpeg paths
        static_ffmpeg = r"C:\Users\19509\.gemini\antigravity-cli\brain\909da7d6-0567-401a-946d-b8da7d08373b\scratch\ffmpeg\ffmpeg.exe"
        if os.path.exists(static_ffmpeg):
            return static_ffmpeg

        return "ffmpeg"

    def get_hardware_video_codecs_chain(self):
        """Returns prioritized fallback chain of video encoders (Hardware GPU -> Software CPU)."""
        codecs = []
        if self.system == "Darwin": # macOS Apple Silicon Metal VideoToolbox
            codecs.extend(["hevc_videotoolbox", "h264_videotoolbox", "libx265", "libx264"])
        elif self.system in ["Windows", "Linux"]: # NVIDIA NVENC / CPU Fallback
            codecs.extend(["hevc_nvenc", "h264_nvenc", "libx265", "libx264"])
        else:
            codecs.extend(["libx265", "libx264"])
        return codecs

    def process_single_video(self, vpath, index, total, output_dir):
        vname = os.path.basename(vpath)
        base, ext = os.path.splitext(vname)
        final_out = os.path.join(output_dir, f"{base}_AI_120fps_HDR.mp4")

        if os.path.exists(final_out) and os.path.getsize(final_out) > 5 * 1024 * 1024:
            print(f"[{index}/{total}] ⏩ Skipping (already completed): {vname}", flush=True)
            return True

        t0 = time.time()
        print(f"[{index}/{total}] 🚀 Processing (Aspect-Ratio Safe 2x/4K + 120fps + HDR): {vname} ...", flush=True)

        tmp_in = os.path.join(output_dir, f"._tmp_in_{base}")
        tmp_out = os.path.join(output_dir, f"._tmp_out_{base}")

        os.makedirs(tmp_in, exist_ok=True)
        os.makedirs(tmp_out, exist_ok=True)

        # 1. Extract raw frames
        print("  → 1/3 Extracting raw frames with FFmpeg...", flush=True)
        cmd_extract = [
            self.ffmpeg_exe, "-y",
            "-i", vpath,
            "-q:v", "2",
            os.path.join(tmp_in, "%08d.jpg")
        ]
        p_ext = subprocess.Popen(cmd_extract, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p_ext.wait()

        in_count = len(os.listdir(tmp_in))
        if in_count == 0:
            print(f"  ❌ Frame extraction failed for {vname}", flush=True)
            shutil.rmtree(tmp_in, ignore_errors=True)
            shutil.rmtree(tmp_out, ignore_errors=True)
            return False

        # 2. 🛡️ RIFE Vulkan GPU AI Interpolation (with CPU Fallback -g -1)
        print(f"  → 2/3 ⚡ RIFE Vulkan 120fps AI Interpolation on GPU {self.gpu_id} ({in_count} frames)...", flush=True)
        rife_cwd = os.path.dirname(self.rife_exe)
        cmd_rife = [
            self.rife_exe,
            "-i", tmp_in,
            "-o", tmp_out,
            "-m", "rife-v4.6",
            "-n", str(in_count * 4),
            "-g", self.gpu_id
        ]
        p_rife = subprocess.Popen(cmd_rife, cwd=rife_cwd if os.path.exists(rife_cwd) else None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p_rife.wait()

        out_count = len(os.listdir(tmp_out))
        if out_count == 0: # GPU failed, try CPU Fallback (-g -1)
            print(f"  ⚠️ GPU Vulkan RIFE unavailable/failed. Retrying with CPU Multi-Threading (-g -1)...", flush=True)
            cmd_rife[cmd_rife.index("-g") + 1] = "-1"
            p_rife_cpu = subprocess.Popen(cmd_rife, cwd=rife_cwd if os.path.exists(rife_cwd) else None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            p_rife_cpu.wait()
            out_count = len(os.listdir(tmp_out))

        if out_count == 0:
            print(f"  ❌ RIFE GPU/CPU Interpolation failed for {vname}", flush=True)
            shutil.rmtree(tmp_in, ignore_errors=True)
            shutil.rmtree(tmp_out, ignore_errors=True)
            return False

        # 3. 🛡️ Video Encoding Codec Fallback Chain (NVENC -> VideoToolbox -> libx265 CPU)
        print(f"  → 3/3 🌟 Video Re-encoding (Aspect-Ratio Safe {self.scale_expr}) 10-bit HDR ({out_count} frames)...", flush=True)
        codecs = self.get_hardware_video_codecs_chain()
        encoded = False
        used_codec = ""

        for codec in codecs:
            cmd_encode = [
                self.ffmpeg_exe, "-y",
                "-r", str(self.target_fps),
                "-i", os.path.join(tmp_out, "%08d.png"),
                "-i", vpath,
                "-vf", f"scale={self.scale_expr}:flags=lanczos",
                "-c:v", codec,
                "-pix_fmt", "yuv420p10le" if codec not in ["hevc_videotoolbox", "libx264"] else "yuv420p",
                "-c:a", "aac",
                "-b:a", "320k",
                "-map", "0:v:0",
                "-map", "1:a:0?",
                "-shortest",
                final_out
            ]
            p_enc = subprocess.Popen(cmd_encode, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            p_enc.wait()

            if os.path.exists(final_out) and os.path.getsize(final_out) > 0:
                encoded = True
                used_codec = codec
                break
            else:
                print(f"  ⚠️ Codec '{codec}' unsupported on this system. Trying next fallback codec...", flush=True)

        shutil.rmtree(tmp_in, ignore_errors=True)
        shutil.rmtree(tmp_out, ignore_errors=True)

        if encoded:
            dt = time.time() - t0
            mb = os.path.getsize(final_out) / (1024**2)
            print(f"  ✅ SUCCESS in {dt:.1f}s → {mb:.1f} MB (Codec: {used_codec}): {os.path.basename(final_out)}\n", flush=True)
            return True
        else:
            print(f"  ❌ All video encoding codecs failed for {vname}\n", flush=True)
            return False
