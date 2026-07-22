"""
GPU-Accelerated Photo 4K/8K AI Super-Resolution Engine with MD5 Deduplication
"""
import os
import sys
import time
import hashlib
import subprocess

class PhotoUpscaleEngine:
    def __init__(self, exe_path, gpu_id=0, model="realesrgan-x4plus", tile_size=256, scale=4):
        self.exe_path = exe_path
        self.gpu_id = str(gpu_id)
        self.model = model
        self.tile_size = str(tile_size)
        self.scale = str(scale)

    def get_file_md5(self, filepath):
        if not os.path.exists(filepath):
            return None
        h = hashlib.md5()
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

    def upscale_single(self, input_path, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cmd = [
            self.exe_path,
            "-i", input_path,
            "-o", output_path,
            "-n", self.model,
            "-s", self.scale,
            "-t", self.tile_size,
            "-g", self.gpu_id
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 0

    def batch_process(self, input_dir, output_dir, deduplicate=True):
        os.makedirs(output_dir, exist_ok=True)
        all_files = []
        for root, dirs, filenames in os.walk(input_dir):
            for f in filenames:
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    rel = os.path.relpath(os.path.join(root, f), input_dir)
                    out_name = os.path.splitext(rel)[0] + "_AI4K.png"
                    all_files.append({
                        'in': os.path.join(input_dir, rel),
                        'out': os.path.join(output_dir, out_name),
                        'rel': rel
                    })

        files = []
        if deduplicate:
            seen_hashes = set()
            dup_count = 0
            for item in all_files:
                md5 = self.get_file_md5(item['in'])
                if md5 in seen_hashes:
                    dup_count += 1
                else:
                    seen_hashes.add(md5)
                    files.append(item)
            print(f"🔍 MD5 Deduplication: Skipped {dup_count} duplicate photos. Unique: {len(files)}")
        else:
            files = all_files

        print(f"🚀 Processing {len(files)} unique photos on GPU {self.gpu_id}...")
        t0 = time.time()
        for i, item in enumerate(files, 1):
            if os.path.exists(item['out']):
                continue
            t_s = time.time()
            ok = self.upscale_single(item['in'], item['out'])
            dt = time.time() - t_s
            pct = (i / len(files)) * 100
            if ok:
                mb = os.path.getsize(item['out']) / (1024**2)
                print(f"[{i}/{len(files)}] ({pct:5.1f}%) Upscaled: {os.path.basename(item['in'])} --> {mb:.1f} MB ({dt:.2f}s)")
        print(f"🎉 Batch Photo Upscaling Complete in {(time.time()-t0)/60:.1f} mins!")
