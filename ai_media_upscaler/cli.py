"""
AI Media Upscaler Command Line Interface (CLI)
"""
import os
import sys
import argparse
from .photo_engine import PhotoUpscaleEngine
from .video_engine import VideoEnhanceEngine

def main():
    parser = argparse.ArgumentParser(
        prog="ai-media",
        description="✨ GPU-Accelerated Photo 4K/8K Super-Resolution & Video 120fps HDR Interpolation CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

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

    if args.command == "photo":
        engine = PhotoUpscaleEngine(exe_path=args.exe, gpu_id=args.gpu, scale=args.scale)
        engine.batch_process(args.input, args.output, deduplicate=not args.no_dedupe)
    elif args.command == "video":
        engine = VideoEnhanceEngine(rife_exe=args.exe, gpu_id=args.gpu, target_fps=args.fps, enable_hdr=args.hdr)
        print(f"🚀 Processing video on GPU {args.gpu} (FPS: {args.fps}, HDR: {args.hdr})...")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
