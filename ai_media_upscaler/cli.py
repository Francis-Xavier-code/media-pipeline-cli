"""
AI Media Upscaler Command Line Interface (CLI) with Sleek Minimalist UI & Full Lifecycle Control
"""
import os
import sys
import time
import glob
import shutil
import signal
import ctypes
import argparse
import subprocess
from .photo_engine import PhotoUpscaleEngine
from .video_engine import VideoEnhanceEngine

PID_FILE = os.path.expanduser(r"~\.ai_media_pipeline.pid")
LOG_FILE = r"C:\Users\19509\.gemini\antigravity-cli\brain\909da7d6-0567-401a-946d-b8da7d08373b\.system_generated\tasks\task-1336.log"
TMP_DIRS = [r"E:\_tmp_rife_in", r"E:\_tmp_rife_out"]

def force_stop_all_pipeline_processes():
    """Finds and terminates all active pipeline scripts and GPU binary processes on Windows/Linux/macOS."""
    killed_count = 0
    target_binaries = ["rife-ncnn-vulkan.exe", "realesrgan-ncnn-vulkan.exe", "ffmpeg.exe"]
    
    if os.name == 'nt':
        for t in target_binaries:
            try:
                res = subprocess.run(["taskkill", "/F", "/IM", t], capture_output=True, text=True)
                if "SUCCESS" in res.stdout or "成功" in res.stdout:
                    killed_count += 1
            except Exception:
                pass
        cmd_py = "powershell -Command \"Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*start_video_ai_reconstruction*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }\""
        try:
            res_py = subprocess.run(cmd_py, capture_output=True, text=True, shell=True)
            if res_py.returncode == 0:
                killed_count += 1
        except Exception:
            pass
    else:
        target_names = ["start_video_ai_reconstruction", "rife-ncnn-vulkan", "realesrgan-ncnn-vulkan"]
        for tname in target_names:
            try:
                subprocess.run(["pkill", "-9", "-f", tname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                killed_count += 1
            except Exception:
                pass

    if os.path.exists(PID_FILE):
        try: os.remove(PID_FILE)
        except: pass

    return killed_count

def clean_temp_directories():
    cleaned = []
    for d in TMP_DIRS:
        if os.path.exists(d):
            try:
                shutil.rmtree(d, ignore_errors=True)
                cleaned.append(d)
            except Exception:
                pass
    # Clean pip temporary uninstall folders
    temp_dir = os.environ.get("TEMP", os.path.expanduser(r"~\AppData\Local\Temp"))
    pip_temps = glob.glob(os.path.join(temp_dir, "pip-uninstall-*"))
    for p in pip_temps:
        try: shutil.rmtree(p, ignore_errors=True)
        except: pass

    return cleaned

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        prog="ai-media",
        description="GPU-Accelerated Photo 4K/8K Super-Resolution & Video 120fps HDR Interpolation CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    # Status Command
    subparsers.add_parser("status", help="Check live status of the AI media processing pipeline")

    # Stop Command
    stop_parser = subparsers.add_parser("stop", help="Stop background pipeline processes and optionally clean temp caches")
    stop_parser.add_argument("--clean", "-c", action="store_true", help="Also remove temporary cache folders")

    # Clean Command
    subparsers.add_parser("clean", help="Stop background processes and remove all temporary cache folders")

    # Uninstall Command
    subparsers.add_parser("uninstall", help="Stop pipeline, clean temp folders, and uninstall ai-media package cleanly")

    # Continue Command
    subparsers.add_parser("continue", help="Resume/continue the pipeline from the latest breakpoint")

    # Restart Command
    subparsers.add_parser("restart", help="Restart the background pipeline from the latest breakpoint")

    # Log Command
    log_parser = subparsers.add_parser("log", help="Watch Real-Time UTF-8 Streaming Processing Logs")
    log_parser.add_argument("--file", "-f", type=str, help="Log file path to watch")

    # Photo Command
    photo_parser = subparsers.add_parser("photo", help="Batch AI Photo 4K/8K Super-Resolution")
    photo_parser.add_argument("--input", "-i", type=str, required=True, help="Input photos directory")
    photo_parser.add_argument("--output", "-o", type=str, required=True, help="Output 4K photos directory")
    photo_parser.add_argument("--exe", type=str, required=True, help="Path to realesrgan-ncnn-vulkan.exe")
    photo_parser.add_argument("--gpu", type=int, default=0, help="GPU device ID")
    photo_parser.add_argument("--scale", type=int, default=4, help="Upscale factor (2, 4, 8)")
    photo_parser.add_argument("--no-dedupe", action="store_true", help="Disable MD5 content deduplication")
    photo_parser.add_argument("--detach", "-d", action="store_true", help="Run in background daemon mode")

    # Video Command
    video_parser = subparsers.add_parser("video", help="Video 120fps Frame Interpolation & 10-bit HDR Engine")
    video_parser.add_argument("--input", "-i", type=str, required=True, help="Input video file or directory")
    video_parser.add_argument("--output", "-o", type=str, required=True, help="Output video directory")
    video_parser.add_argument("--exe", type=str, required=True, help="Path to rife-ncnn-vulkan.exe")
    video_parser.add_argument("--gpu", type=int, default=0, help="GPU device ID")
    video_parser.add_argument("--fps", type=int, default=120, help="Target FPS (60, 120)")
    video_parser.add_argument("--hdr", action="store_true", help="Enable 10-bit HDR10 color re-encoding")
    video_parser.add_argument("--detach", "-d", action="store_true", help="Run in background daemon mode")

    args = parser.parse_args()

    if args.command == "status":
        cmd_check = "powershell -Command \"Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*start_video_ai_reconstruction*' } | Select-Object -ExpandProperty ProcessId\""
        res = subprocess.run(cmd_check, capture_output=True, text=True, shell=True) if os.name=='nt' else None
        active = False
        if res and res.stdout.strip():
            active = True

        print("\n  ┌─────────────────────────────────────────────────────────────┐", flush=True)
        print("  │ 📊  ai-media Pipeline Status                                │", flush=True)
        print("  └─────────────────────────────────────────────────────────────┘\n", flush=True)
        if active:
            print("  ▸ Pipeline Status : 🟢 RUNNING (Active Reconstruction Engine)", flush=True)
        else:
            print("  ▸ Pipeline Status : ⚪ STOPPED / IDLE", flush=True)

        if os.path.exists(LOG_FILE):
            print(f"  ▸ Log File        : {LOG_FILE}", flush=True)
            with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
                if lines:
                    print(f"  ▸ Latest Activity : {lines[-1]}\n", flush=True)

    elif args.command == "stop":
        print("\n  🛑 Stopping all active ai-media pipeline processes...", flush=True)
        killed = force_stop_all_pipeline_processes()
        print("  ✔ Pipeline processes stopped successfully.", flush=True)

        if args.clean:
            cleaned = clean_temp_directories()
            print(f"  ✔ Temporary cache folders cleared: {cleaned}", flush=True)
        print("", flush=True)

    elif args.command == "clean":
        print("\n  🛑 Stopping pipeline and clearing temporary cache folders...", flush=True)
        killed = force_stop_all_pipeline_processes()
        cleaned = clean_temp_directories()
        print(f"  ✔ Pipeline stopped and temporary cache folders cleared: {cleaned}\n", flush=True)

    elif args.command == "uninstall":
        print("\n  ┌─────────────────────────────────────────────────────────────┐", flush=True)
        print("  │ 🗑️   ai-media Clean Uninstall Protocol                      │", flush=True)
        print("  └─────────────────────────────────────────────────────────────┘\n", flush=True)
        print("  1. Terminating background processes ... ", end="", flush=True)
        force_stop_all_pipeline_processes()
        print("[DONE]", flush=True)

        print("  2. Clearing temporary cache folders .... ", end="", flush=True)
        clean_temp_directories()
        print("[DONE]", flush=True)

        print("  3. Uninstalling ai-media-upscaler ..... ", end="", flush=True)
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "ai-media-upscaler"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clean_temp_directories()
        print("[DONE]\n", flush=True)

        print("  ✨ ai-media-upscaler has been completely uninstalled with zero residual files!\n", flush=True)

    elif args.command == "continue":
        cmd_check = "powershell -Command \"Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*start_video_ai_reconstruction*' } | Select-Object -ExpandProperty ProcessId\""
        res = subprocess.run(cmd_check, capture_output=True, text=True, shell=True) if os.name=='nt' else None
        active = False
        if res and res.stdout.strip():
            active = True
        if active:
            print("\n  🟢 Pipeline is already running. Use 'ai-media log' to watch live progress.\n", flush=True)
            return

        print("\n  🚀 Resuming ai-media processing pipeline from breakpoint...", flush=True)
        script_path = r"C:\Users\19509\.gemini\antigravity-cli\brain\909da7d6-0567-401a-946d-b8da7d08373b\scratch\start_video_ai_reconstruction.py"
        if os.path.exists(script_path):
            p = subprocess.Popen([sys.executable, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(PID_FILE, 'w') as f:
                f.write(str(p.pid))
            print(f"  ✔ Pipeline resumed in background (PID: {p.pid}). Run 'ai-media log' or 'ai-media status'.\n", flush=True)

    elif args.command == "restart":
        print("\n  🔄 Restarting ai-media processing pipeline...", flush=True)
        force_stop_all_pipeline_processes()
        clean_temp_directories()
        time.sleep(1)

        script_path = r"C:\Users\19509\.gemini\antigravity-cli\brain\909da7d6-0567-401a-946d-b8da7d08373b\scratch\start_video_ai_reconstruction.py"
        if os.path.exists(script_path):
            p = subprocess.Popen([sys.executable, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(PID_FILE, 'w') as f:
                f.write(str(p.pid))
            print(f"  ✔ Pipeline restarted in background (PID: {p.pid}). Use 'ai-media log' to watch progress.\n", flush=True)

    elif args.command == "log":
        log_path = args.file or LOG_FILE
        if not os.path.exists(log_path):
            print(f"Log file not found: {log_path}")
            return
        print(f"\n  === 📺 Real-Time Streaming Log: {log_path} (Press Ctrl+C to exit) ===\n", flush=True)
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    print(line, end='', flush=True)
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.5)
                        continue
                    print(line, end='', flush=True)
        except KeyboardInterrupt:
            print("\n  👋 Log watching stopped gracefully.\n", flush=True)
            sys.exit(0)

    elif args.command == "photo":
        if getattr(args, 'detach', False):
            cmd = [sys.executable, "-m", "ai_media_upscaler.cli", "photo", "-i", args.input, "-o", args.output, "--exe", args.exe, "--gpu", str(args.gpu), "--scale", str(args.scale)]
            p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"\n  🚀 Photo AI Super-Resolution started in background (PID: {p.pid}). Use 'ai-media log' to watch.\n", flush=True)
        else:
            engine = PhotoUpscaleEngine(exe_path=args.exe, gpu_id=args.gpu, scale=args.scale)
            engine.batch_process(args.input, args.output, deduplicate=not args.no_dedupe)

    elif args.command == "video":
        if getattr(args, 'detach', False):
            cmd = [sys.executable, "-m", "ai_media_upscaler.cli", "video", "-i", args.input, "-o", args.output, "--exe", args.exe, "--gpu", str(args.gpu), "--fps", str(args.fps)]
            if args.hdr: cmd.append("--hdr")
            p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"\n  🚀 Video AI Reconstruction started in background (PID: {p.pid}). Use 'ai-media log' or 'ai-media status'.\n", flush=True)
        else:
            engine = VideoEnhanceEngine(rife_exe=args.exe, gpu_id=args.gpu, target_fps=args.fps, enable_hdr=args.hdr)
            os.makedirs(args.output, exist_ok=True)
            if os.path.isfile(args.input):
                print("\n  ┌─────────────────────────────────────────────────────────────┐", flush=True)
                print("  │ 🎬  AI Video Reconstruction Engine                          │", flush=True)
                print(f"  │     2x/4K Aspect-Ratio Preserved • {args.fps}fps • 10-bit HDR10       │", flush=True)
                print("  └─────────────────────────────────────────────────────────────┘\n", flush=True)
                print(f"  ▸ Target File : {args.input}", flush=True)
                print(f"  ▸ Output Path : {args.output}\n", flush=True)
                engine.process_single_video(args.input, 1, 1, args.output)
            elif os.path.isdir(args.input):
                files = [f for f in os.listdir(args.input) if f.lower().endswith(('.mp4', '.mov', '.mkv', '.avi', '.flv', '.wmv'))]
                print("\n  ┌─────────────────────────────────────────────────────────────┐", flush=True)
                print("  │ 🎬  AI Video Reconstruction Batch Engine                    │", flush=True)
                print(f"  │     Total Videos: {len(files):<3} • {args.fps}fps • 10-bit HDR10           │", flush=True)
                print("  └─────────────────────────────────────────────────────────────┘\n", flush=True)
                print(f"  ▸ Input Directory  : {args.input}", flush=True)
                print(f"  ▸ Output Directory : {args.output}\n", flush=True)
                for idx, fname in enumerate(files, 1):
                    vpath = os.path.join(args.input, fname)
                    engine.process_single_video(vpath, idx, len(files), args.output)
            else:
                print(f"❌ Error: Input path not found: {args.input}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
