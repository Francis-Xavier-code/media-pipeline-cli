"""
AI Media Upscaler Command Line Interface (CLI) with Process Management (status, stop, continue, restart, log, photo, video)
"""
import os
import sys
import time
import signal
import ctypes
import argparse
import subprocess
from .photo_engine import PhotoUpscaleEngine
from .video_engine import VideoEnhanceEngine

PID_FILE = os.path.expanduser(r"~\.ai_media_pipeline.pid")
LOG_FILE = r"C:\Users\19509\.gemini\antigravity-cli\brain\909da7d6-0567-401a-946d-b8da7d08373b\.system_generated\tasks\task-1336.log"

def is_pid_running(pid):
    """Win32 & POSIX Native Robust PID Checker."""
    if pid <= 0:
        return False
    if os.name == 'nt':
        PROCESS_QUERY_INFORMATION = 0x0400
        STILL_ACTIVE = 259
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
        if not handle:
            return False
        exit_code = ctypes.c_ulong()
        kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
        kernel32.CloseHandle(handle)
        return exit_code.value == STILL_ACTIVE
    else:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

def get_running_pid():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            if is_pid_running(pid):
                return pid
        except Exception:
            pass
    return None

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
    subparsers.add_parser("stop", help="Gracefully stop the background processing pipeline")

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

    # Video Command
    video_parser = subparsers.add_parser("video", help="Video 120fps Frame Interpolation & 10-bit HDR Engine")
    video_parser.add_argument("--input", "-i", type=str, required=True, help="Input video file or directory")
    video_parser.add_argument("--output", "-o", type=str, required=True, help="Output video directory")
    video_parser.add_argument("--exe", type=str, required=True, help="Path to rife-ncnn-vulkan.exe")
    video_parser.add_argument("--gpu", type=int, default=0, help="GPU device ID")
    video_parser.add_argument("--fps", type=int, default=120, help="Target FPS (60, 120)")
    video_parser.add_argument("--hdr", action="store_true", help="Enable 10-bit HDR10 color re-encoding")

    args = parser.parse_args()

    if args.command == "status":
        pid = get_running_pid()
        print("=== 📊 ai-media Pipeline Status ===")
        if pid:
            print(f"🟢 Pipeline Status: RUNNING (PID: {pid})")
        else:
            print("⚪ Pipeline Status: STOPPED / IDLE")

        if os.path.exists(LOG_FILE):
            print(f"📄 Log File: {LOG_FILE}")
            with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
                if lines:
                    print("📌 Latest Activity:", lines[-1])

    elif args.command == "stop":
        pid = get_running_pid()
        if not pid:
            print("⚪ No active ai-media pipeline process is currently running.")
            return
        print(f"🛑 Stopping ai-media pipeline (PID: {pid})...")
        try:
            if os.name == 'nt':
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                os.kill(pid, signal.SIGTERM)
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
            print("✅ Pipeline successfully stopped.")
        except Exception as e:
            print("❌ Failed to stop pipeline:", e)

    elif args.command == "continue":
        pid = get_running_pid()
        if pid:
            print(f"🟢 Pipeline is already running (PID: {pid}). Use 'ai-media log' to watch live progress.")
            return
        print("🚀 Resuming ai-media processing pipeline from breakpoint...")
        script_path = r"C:\Users\19509\.gemini\antigravity-cli\brain\909da7d6-0567-401a-946d-b8da7d08373b\scratch\start_video_ai_reconstruction.py"
        if os.path.exists(script_path):
            p = subprocess.Popen([sys.executable, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(PID_FILE, 'w') as f:
                f.write(str(p.pid))
            print(f"✅ Pipeline resumed in background (PID: {p.pid}). Run 'ai-media log' or 'ai-media status'.")
        else:
            print("❌ Pipeline script not found.")

    elif args.command == "restart":
        print("🔄 Restarting ai-media processing pipeline...")
        pid = get_running_pid()
        if pid:
            print(f"🛑 Stopping existing pipeline (PID: {pid})...")
            if os.name == 'nt':
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                os.kill(pid, signal.SIGTERM)
            time.sleep(1)

        script_path = r"C:\Users\19509\.gemini\antigravity-cli\brain\909da7d6-0567-401a-946d-b8da7d08373b\scratch\start_video_ai_reconstruction.py"
        if os.path.exists(script_path):
            p = subprocess.Popen([sys.executable, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(PID_FILE, 'w') as f:
                f.write(str(p.pid))
            print(f"✅ Pipeline restarted in background (PID: {p.pid}). Use 'ai-media log' to watch progress.")

    elif args.command == "log":
        log_path = args.file or LOG_FILE
        if not os.path.exists(log_path):
            print(f"Log file not found: {log_path}")
            return
        print(f"=== 📺 Watching Real-Time Streaming Log: {log_path} (Press Ctrl+C to exit) ===")
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
            print("\n👋 Log watching stopped gracefully.")
            sys.exit(0)

    elif args.command == "photo":
        engine = PhotoUpscaleEngine(exe_path=args.exe, gpu_id=args.gpu, scale=args.scale)
        engine.batch_process(args.input, args.output, deduplicate=not args.no_dedupe)

    elif args.command == "video":
        engine = VideoEnhanceEngine(rife_exe=args.exe, gpu_id=args.gpu, target_fps=args.fps, enable_hdr=args.hdr)
        print(f"Processing video on GPU {args.gpu} (FPS: {args.fps}, HDR: {args.hdr})...")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
