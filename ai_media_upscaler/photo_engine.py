"""
GPU-Accelerated & CPU-Fallback Photo AI Super-Resolution Engine with Triple Hardware Safety Net
"""
import os
import sys
import time
import hashlib
import subprocess
from PIL import Image

class PhotoUpscaleEngine:
    def __init__(self, exe_path="realesrgan-ncnn-vulkan", gpu_id=0, scale=4, tile_size=256, model="realesrgan-x4plus"):
        self.exe_path = exe_path
        self.gpu_id = str(gpu_id)
        self.scale = str(scale)
        self.tile_size = str(tile_size)
        self.model = model

    def get_file_md5(self, filepath):
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    def batch_process(self, input_dir, output_dir, deduplicate=True):
        os.makedirs(output_dir, exist_ok=True)
        files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp'))]
        print(f"=== 🖼️ Starting Photo AI Super-Resolution ({len(files)} files) ===", flush=True)

        processed_hashes = {}
        items = []

        for f in files:
            inp = os.path.join(input_dir, f)
            out = os.path.join(output_dir, f"{os.path.splitext(f)[0]}.png")
            items.append({'in': inp, 'out': out, 'name': f})

        success = 0
        skipped = 0

        for i, item in enumerate(items, 1):
            if os.path.exists(item['out']) and os.path.getsize(item['out']) > 0:
                print(f"[{i}/{len(items)}] ⏩ Skipping (already processed): {item['name']}", flush=True)
                skipped += 1
                continue

            if deduplicate:
                md5_val = self.get_file_md5(item['in'])
                if md5_val in processed_hashes:
                    print(f"[{i}/{len(items)}] ⏩ Skipping duplicate content: {item['name']}", flush=True)
                    skipped += 1
                    continue
                processed_hashes[md5_val] = item['out']

            t0 = time.time()
            
            # 🛡️ Level 1: Try GPU Vulkan Acceleration (-g 0)
            cmd = [
                self.exe_path,
                "-i", item['in'],
                "-o", item['out'],
                "-s", self.scale,
                "-t", self.tile_size,
                "-m", "models",
                "-n", self.model,
                "-g", self.gpu_id
            ]
            exe_dir = os.path.dirname(self.exe_path)
            res = subprocess.run(cmd, cwd=exe_dir if os.path.exists(exe_dir) else None, capture_output=True, text=True)

            # 🛡️ Level 2: CPU Fallback (-g -1) if GPU Vulkan is unavailable
            if not (os.path.exists(item['out']) and os.path.getsize(item['out']) > 0):
                print(f"  ⚠️ GPU Vulkan unavailable/failed on {item['name']}. Fallback to CPU Multi-Threading mode (-g -1)...", flush=True)
                cmd[cmd.index("-g") + 1] = "-1"  # CPU Mode
                res = subprocess.run(cmd, cwd=exe_dir if os.path.exists(exe_dir) else None, capture_output=True, text=True)

            if os.path.exists(item['out']) and os.path.getsize(item['out']) > 0:
                dt = time.time() - t0
                mb = os.path.getsize(item['out']) / (1024**2)
                print(f"[{i}/{len(items)}] ✅ AI Upscaled: {item['name']} --> {mb:.1f} MB (Done in {dt:.2f}s)", flush=True)
                success += 1
            else:
                print(f"[{i}/{len(items)}] ❌ Super-resolution failed on {item['name']}", flush=True)

        print(f"\n🎉 Photo AI Super-Resolution Completed: {success} processed, {skipped} skipped.", flush=True)
