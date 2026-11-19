import json
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def main():
    print("=== DATASET & SCIENTIFIC INTEGRITY AUDIT ===")

    # 1. Manifest verification
    manifest_path = ROOT / 'data/manifests/reviewed_label_manifest.csv'
    assert manifest_path.exists(), "Manifest missing!"
    mdf = pd.read_csv(manifest_path)
    print("Total reviewed manifest records:", len(mdf))
    splits = mdf['split'].value_counts().to_dict()
    print("Split counts:", splits)
    assert splits.get('train') == 591, f"Expected 591 train, got {splits.get('train')}"
    assert splits.get('validation') == 321, f"Expected 321 validation, got {splits.get('validation')}"
    assert splits.get('test') == 285, f"Expected 285 test, got {splits.get('test')}"

    # 2. Check subject identity leakage across splits
    train_subjs = set(mdf[mdf['split']=='train']['subject_id'].dropna())
    val_subjs = set(mdf[mdf['split']=='validation']['subject_id'].dropna())
    test_subjs = set(mdf[mdf['split']=='test']['subject_id'].dropna())

    leak_tv = train_subjs.intersection(val_subjs)
    leak_tt = train_subjs.intersection(test_subjs)
    leak_vt = val_subjs.intersection(test_subjs)
    print(f"Identity overlap - Train/Val: {len(leak_tv)}, Train/Test: {len(leak_tt)}, Val/Test: {len(leak_vt)}")
    assert len(leak_tv) == 0 and len(leak_tt) == 0 and len(leak_vt) == 0, "Identity leakage detected!"

    # 3. Check unlabelled reserve
    unlabelled_path = ROOT / 'reports/unlabelled_samples.csv'
    assert unlabelled_path.exists(), "Unlabelled samples report missing!"
    udf = pd.read_csv(unlabelled_path)
    print("Unlabelled reserve count:", len(udf))
    assert len(udf) == 45595, f"Expected 45,595 unlabelled, got {len(udf)}"

    # 4. Check feature cache processing summary
    proc_path = ROOT / 'data/cache/image_features/processing_summary.json'
    assert proc_path.exists(), "Processing summary missing!"
    proc_data = json.loads(proc_path.read_text(encoding='utf-8'))
    print("Processing summary:", proc_data)
    assert proc_data.get('requested') == 46792
    assert proc_data.get('success') == 46792
    assert proc_data.get('failed') == 0

    # 5. Check total dataset sum
    total_images = len(mdf) + len(udf)
    print(f"Total accounted images: {total_images} (Manifest: {len(mdf)} + Unlabelled: {len(udf)})")
    assert total_images == 46792

    print("\n>>> ALL SCIENTIFIC INTEGRITY CHECKS PASSED PERFECTLY! <<<")

if __name__ == '__main__':
    main()
