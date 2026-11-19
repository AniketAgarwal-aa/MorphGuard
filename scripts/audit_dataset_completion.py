"""Comprehensive independent audit of all dataset files, cache shards, manifests, and integrity."""
import hashlib, json, time, sys
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).parents[1]

def main():
    print("=== MORPHGUARD COMPREHENSIVE DATASET & CACHE AUDIT ===")

    # 1. Inspect raw dataset directories
    datasets = {
        'MONOT Gate_10': ROOT / 'MONOT/Gate_10',
        'MONOT Gate_25': ROOT / 'MONOT/Gate_25',
        'MONOT Morphed': ROOT / 'MONOT/Morphed',
        'ONOT digital': ROOT / 'ONOT/digital',
        'ONOT print-scan': ROOT / 'ONOT/print-scan',
    }

    dir_stats = {}
    total_raw = 0
    for name, path in datasets.items():
        if path.exists():
            files = list(path.glob('*.png')) + list(path.glob('*.jpg')) + list(path.glob('*.jpeg'))
            count = len(files)
            dir_stats[name] = count
            total_raw += count
            print(f"  - {name:<18}: {count:>6} images on disk ({path})")
        else:
            dir_stats[name] = 0
            print(f"  - {name:<18}: NOT FOUND ({path})")
    print(f"Total raw biometric images on disk: {total_raw}\n")

    # 2. Inspect Feature Cache Manifest & Shards
    cache_dir = ROOT / 'data/cache/image_features'
    manifest_p = cache_dir / 'processing_manifest.csv'
    summary_p = cache_dir / 'processing_summary.json'

    summary = json.loads(summary_p.read_text(encoding='utf-8'))
    manifest_df = pd.read_csv(manifest_p)
    print(f"=== FEATURE CACHE AUDIT ===")
    print(f"  Cache directory: {cache_dir}")
    print(f"  Total manifest rows: {len(manifest_df)}")
    print(f"  Summary requested: {summary['requested']}")
    print(f"  Summary feature records: {summary['feature_records']}")
    print(f"  Success count: {summary['success_count']}")
    print(f"  Failed count: {summary['failed_count']}")
    print(f"  Face detected: {summary['face_detected_count']} ({summary['face_detected_count']/summary['requested']*100:.2f}%)")

    # Breakdown by stratum in manifest
    print("\nManifest stratum breakdown:")
    for subset, count in manifest_df['subset'].value_counts().items():
        print(f"  - {subset:<18}: {count:>6} records")

    # 3. Label manifests audit
    reviewed_p = ROOT / 'data/manifests/reviewed_label_manifest.csv'
    reviewed_df = pd.read_csv(reviewed_p)
    print(f"\n=== GROUND TRUTH LABEL MANIFEST AUDIT ===")
    print(f"  Total reviewed records: {len(reviewed_df)}")
    print(f"  Labels: {reviewed_df['verified_label'].value_counts().to_dict()}")
    print(f"  Splits: {reviewed_df['split'].value_counts().to_dict()}")
    print(f"  Split x Label matrix:")
    print(pd.crosstab(reviewed_df['split'], reviewed_df['verified_label']))

    # Check subject identity leakage across splits
    def extract_subject(p):
        stem = Path(p).stem
        if 'M_' in stem:
            parts = stem.split('_')
            return parts[1].split('-')[0] + "+" + parts[2].split('-')[0]
        return stem.split('-')[0]

    reviewed_df['subj'] = reviewed_df['image_path'].apply(extract_subject)
    train_subj = set(reviewed_df[reviewed_df['split'] == 'train']['subj'])
    val_subj = set(reviewed_df[reviewed_df['split'] == 'validation']['subj'])
    test_subj = set(reviewed_df[reviewed_df['split'] == 'test']['subj'])

    leak_tv = train_subj.intersection(val_subj)
    leak_tt = train_subj.intersection(test_subj)
    leak_vt = val_subj.intersection(test_subj)

    print(f"\nSubject Separation & Identity Leakage Audit:")
    print(f"  Train subject clusters: {len(train_subj)}")
    print(f"  Validation subject clusters: {len(val_subj)}")
    print(f"  Test subject clusters: {len(test_subj)}")
    print(f"  Train-Val overlap: {len(leak_tv)} subjects")
    print(f"  Train-Test overlap: {len(leak_tt)} subjects")
    print(f"  Val-Test overlap: {len(leak_vt)} subjects")
    assert len(leak_tv) == 0 and len(leak_tt) == 0 and len(leak_vt) == 0, "SUBJECT LEAKAGE DETECTED!"
    print("  ✓ ZERO SUBJECT LEAKAGE: Subject-disjoint integrity 100% verified.")

    # 4. Unlabelled reserve audit
    unlab_p = ROOT / 'reports/unlabelled_samples.csv'
    unlab_df = pd.read_csv(unlab_p)
    print(f"\n=== UNLABELLED RESERVE AUDIT ===")
    print(f"  Total unlabelled samples tracked: {len(unlab_df)}")
    print(f"  Reason summary:\n{unlab_df['reason'].value_counts()}")

if __name__ == '__main__':
    main()
