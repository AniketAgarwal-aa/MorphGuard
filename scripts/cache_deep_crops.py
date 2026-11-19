"""Pre-extract and cache normalized face crop tensors for deep model training and evaluation."""
import sys, time
from pathlib import Path
import pandas as pd
import torch
import numpy as np

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from morphguard.preprocessing import FacePreprocessor

def main():
    cache_path = ROOT / 'data/cache/deep_face_crops.pt'
    if cache_path.exists():
        print(f"Deep crop cache already exists: {cache_path} ({cache_path.stat().st_size / (1024*1024):.1f} MB)")
        return

    manifest_path = ROOT / 'data/manifests/reviewed_label_manifest.csv'
    df = pd.read_csv(manifest_path)
    print(f"Caching face crops for {len(df)} reviewed records...")

    pre = FacePreprocessor(image_size=224)
    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)

    t0 = time.time()
    tensors = {}
    for idx, row in df.iterrows():
        p = ROOT / row['image_path']
        bgr = pre.load(str(p))
        if bgr is not None and bgr.size > 0:
            faces = pre.detect(bgr)
            crop_rgb = pre.transform(bgr, faces[0] if faces else None)
            t = torch.from_numpy(crop_rgb.transpose(2, 0, 1)).float() / 255.0
            t = (t - mean) / std
            tensors[row['image_path']] = t
        else:
            # Fallback zero tensor
            tensors[row['image_path']] = torch.zeros((3, 224, 224), dtype=torch.float32)

        if (idx + 1) % 200 == 0 or (idx + 1) == len(df):
            print(f"  Processed {idx + 1}/{len(df)} images ({time.time() - t0:.1f}s)...")

    torch.save(tensors, cache_path)
    print(f"Successfully cached {len(tensors)} tensors to {cache_path} ({cache_path.stat().st_size / (1024*1024):.1f} MB in {time.time() - t0:.1f}s)")

if __name__ == '__main__':
    main()
