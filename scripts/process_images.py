"""Resumable, scalable image-level quality assessment and feature extraction.

Reads from data/manifests/annotation_inventory.csv and writes compressed NPZ feature
shards and processing manifests into data/cache/image_features.
Fully idempotent, supports interruption, shard streaming, and multi-threaded processing.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os, sys, threading, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from morphguard.feature_extraction import extract_features
from morphguard.preprocessing import FacePreprocessor

_tls = threading.local()

def get_preprocessor(image_size: int = 224) -> FacePreprocessor:
    if not hasattr(_tls, 'pre'):
        _tls.pre = FacePreprocessor(image_size=image_size)
    return _tls.pre

def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def process_single_image(row: dict, root: Path, fields: list[str]) -> tuple[dict, tuple[str, dict] | None]:
    rel = row['image_path']
    path = root / rel
    out = {k: '' for k in fields}
    out.update({k: row.get(k, '') for k in ('image_path', 'dataset', 'category', 'subject_id', 'morph_pair_id')})
    out['processed_at'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    
    if not path.exists():
        out['status'] = 'failed'
        out['error'] = 'FileNotFoundError: File does not exist'
        return out, None

    try:
        digest = compute_sha256(path)
        pre = get_preprocessor(image_size=224)
        bgr = pre.load(str(path))
        if bgr is None or bgr.size == 0:
            raise ValueError("Empty or unreadable image")
        h, w = bgr.shape[:2]
        faces = pre.detect(bgr)
        primary_face = faces[0] if faces else None
        q = pre.quality(bgr, primary_face)
        rgb = pre.transform(bgr, primary_face)
        feat = extract_features(rgb)
        
        out.update({
            'source_sha256': digest,
            'width': w,
            'height': h,
            'aspect_ratio': round(w / h, 4) if h else 1.0,
            'brightness': round(float(q.brightness), 4),
            'contrast': round(float(q.contrast), 4),
            'sharpness': round(float(q.blur_variance), 4),
            'face_detected': bool(faces),
            'face_count': len(faces),
            'status': 'success',
            'error': ''
        })
        if faces:
            out.update(dict(zip(('face_x', 'face_y', 'face_w', 'face_h'), faces[0])))
        return out, (rel, feat)
    except Exception as exc:
        out['status'] = 'failed'
        out['error'] = f'{type(exc).__name__}: {exc}'
        return out, None

def save_shard(output_dir: Path, shard_name: str, features: list[tuple[str, dict]], results: list[dict]):
    if not features:
        return
    shard_path = output_dir / shard_name
    np.savez_compressed(
        shard_path,
        paths=np.asarray([p for p, _ in features]),
        X=np.asarray([f['combined'] for _, f in features], dtype=np.float64),
        lbp=np.asarray([f['lbp'] for _, f in features], dtype=np.float64),
        hog=np.asarray([f['hog'] for _, f in features], dtype=np.float64),
        glcm=np.asarray([f['glcm'] for _, f in features], dtype=np.float64),
        stats=np.asarray([f['stats'] for _, f in features], dtype=np.float64)
    )
    rel_shard = shard_path.relative_to(ROOT).as_posix()
    shard_paths = {p for p, _ in features}
    for r in results:
        if r['image_path'] in shard_paths:
            r['feature_shard'] = rel_shard

def update_manifest_and_summary(output_dir: Path, results: list[dict], fields: list[str],
                                source_manifest_path: Path, started_time: float):
    manifest_path = output_dir / 'processing_manifest.csv'
    with manifest_path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)

    cached_records = 0
    for npz in sorted(output_dir.glob('features_*.npz')):
        try:
            with np.load(npz) as z:
                cached_records += len(z['paths'])
        except Exception:
            pass

    summary = {
        'requested': len(results),
        'success': sum(1 for r in results if r.get('status') == 'success'),
        'failed': sum(1 for r in results if r.get('status') == 'failed'),
        'feature_records': cached_records,
        'new_feature_records': sum(1 for r in results if r.get('feature_shard')),
        'duration_seconds': round(time.time() - started_time, 2),
        'source_manifest_sha256': compute_sha256(source_manifest_path),
        'cache': str(output_dir.relative_to(ROOT)),
        'resumable': True
    }
    (output_dir / 'processing_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return summary

def main():
    p = argparse.ArgumentParser(description="Process dataset images and generate feature shards")
    p.add_argument('--limit', type=int, default=None, help="Maximum number of new images to process")
    p.add_argument('--shard-size', type=int, default=250, help="Number of records per NPZ shard")
    p.add_argument('--workers', type=int, default=4, help="Number of concurrent worker threads")
    p.add_argument('--stratified', action='store_true', help="Interleave categories evenly across all strata")
    p.add_argument('--dataset', choices=['MONOT', 'ONOT'], help="Filter to specific dataset")
    p.add_argument('--category', type=str, help="Filter to specific category (e.g. Gate_25, Morphed, digital, print-scan)")
    p.add_argument('--output', type=Path, default=ROOT / 'data/cache/image_features', help="Output directory")
    args = p.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'data/manifests/annotation_inventory.csv'
    fields = [
        'image_path', 'dataset', 'category', 'subject_id', 'morph_pair_id',
        'source_sha256', 'width', 'height', 'aspect_ratio', 'brightness',
        'contrast', 'sharpness', 'face_detected', 'face_count',
        'face_x', 'face_y', 'face_w', 'face_h', 'status', 'error',
        'processed_at', 'feature_shard'
    ]

    with source.open(newline='', encoding='utf-8') as f:
        all_inventory = list(csv.DictReader(f))

    # Read existing manifest
    manifest_path = args.output / 'processing_manifest.csv'
    done = {}
    if manifest_path.exists():
        with manifest_path.open(newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                done[r['image_path']] = r

    # Determine existing valid records
    results_order = []
    processed_paths = set()
    for row in all_inventory:
        rel = row['image_path']
        if rel in done and done[rel].get('status') == 'success':
            # Check if shard still exists
            shard_rel = done[rel].get('feature_shard', '')
            if shard_rel and (ROOT / shard_rel).exists():
                results_order.append(done[rel])
                processed_paths.add(rel)

    print(f"Existing valid cached records: {len(processed_paths)} / {len(all_inventory)}")

    # Candidate images to process
    pending = []
    for r in all_inventory:
        if r['image_path'] not in processed_paths:
            if args.dataset and r['dataset'] != args.dataset:
                continue
            if args.category and r['category'] != args.category:
                continue
            pending.append(r)

    print(f"Pending candidate images: {len(pending)}")

    if args.stratified and pending:
        # Group by (dataset, category) and interleave round-robin
        by_cat = defaultdict(list)
        for r in pending:
            by_cat[(r['dataset'], r['category'])].append(r)
        interleaved = []
        max_len = max(len(v) for v in by_cat.values())
        for i in range(max_len):
            for cat_key in sorted(by_cat.keys()):
                if i < len(by_cat[cat_key]):
                    interleaved.append(by_cat[cat_key][i])
        pending = interleaved

    if args.limit is not None and args.limit > 0:
        pending = pending[:args.limit]

    print(f"Images to process in this run: {len(pending)}")

    if not pending:
        # Just update summary if no new items
        summary = update_manifest_and_summary(args.output, results_order, fields, source, time.time())
        print(json.dumps(summary, indent=2))
        return

    started = time.time()
    current_shard_features = []
    current_shard_results = []
    total_processed_in_run = 0

    def flush_shard(shard_num: int):
        nonlocal current_shard_features, current_shard_results
        if not current_shard_features:
            return
        shard_name = f"features_shard_{shard_num}_{int(time.time())}.npz"
        save_shard(args.output, shard_name, current_shard_features, current_shard_results)
        results_order.extend(current_shard_results)
        update_manifest_and_summary(args.output, results_order, fields, source, started)
        print(f"  --> Saved shard {shard_name} ({len(current_shard_features)} records). Total cached: {len(results_order)}")
        current_shard_features = []
        current_shard_results = []

    shard_counter = len(list(args.output.glob('features_*.npz'))) + 1

    # Process in batches using ThreadPoolExecutor
    batch_size = args.shard_size
    for batch_idx in range(0, len(pending), batch_size):
        batch = pending[batch_idx : batch_idx + batch_size]
        t_batch = time.time()
        print(f"\nProcessing batch {batch_idx // batch_size + 1}/{(len(pending) + batch_size - 1) // batch_size} ({len(batch)} images)...")
        
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_row = {executor.submit(process_single_image, row, ROOT, fields): row for row in batch}
            for fut in as_completed(future_to_row):
                out_rec, feat_tuple = fut.result()
                current_shard_results.append(out_rec)
                if feat_tuple is not None:
                    current_shard_features.append(feat_tuple)
                total_processed_in_run += 1
                if total_processed_in_run % 50 == 0 or total_processed_in_run == len(pending):
                    elapsed = time.time() - started
                    rate = total_processed_in_run / elapsed if elapsed > 0 else 0
                    print(f"  Processed {total_processed_in_run}/{len(pending)} ({rate:.1f} img/s)...")

        flush_shard(shard_counter)
        shard_counter += 1

    final_summary = update_manifest_and_summary(args.output, results_order, fields, source, started)
    print("\nProcessing Complete!")
    print(json.dumps(final_summary, indent=2))

if __name__ == '__main__':
    main()
