"""Incremental feature extraction to NPZ shards, resumable by existing shard name."""
import argparse,csv
from pathlib import Path
import numpy as np
from PIL import Image
from morphguard.feature_extraction import extract_features
p=argparse.ArgumentParser();p.add_argument("manifest",type=Path);p.add_argument("--output",type=Path,default=Path("data/cache/features"));p.add_argument("--batch-size",type=int,default=32);args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(args.manifest.open(encoding="utf-8")))
for i in range(0,len(rows),args.batch_size):
    target=args.output/f"features_{i:08d}.npz"
    if target.exists(): continue
    feats=[]; lbps=[]; hogs=[]; glmcs=[]; stats=[]; labels=[]; paths=[]
    for row in rows[i:i+args.batch_size]:
        if row["valid"].lower()!="true" or row["label"] not in {"genuine","morphed"}: continue
        try:
            item=extract_features(np.asarray(Image.open(row["path"]).convert("RGB")))
            feats.append(item["combined"]); lbps.append(item["lbp"]); hogs.append(item["hog"]); glmcs.append(item["glcm"]); stats.append(item["stats"])
            labels.append(row["label"]); paths.append(row["path"])
        except Exception: continue
    if feats: np.savez_compressed(target,X=np.asarray(feats),lbp=np.asarray(lbps),hog=np.asarray(hogs),glcm=np.asarray(glmcs),stats=np.asarray(stats),y=np.asarray(labels),paths=np.asarray(paths))
