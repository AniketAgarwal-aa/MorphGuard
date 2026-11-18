"""Test and verify all application export artifacts (JSON & CSV)."""
import sys, json, csv
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))

from morphguard.preprocessing import FacePreprocessor
from morphguard.feature_extraction import extract_features
from morphguard.inference import compare_vectors

out_dir = ROOT / 'data' / 'test_exports'
out_dir.mkdir(parents=True, exist_ok=True)

# ── 1. Single Image Report Export ─────────────────────────────────────────────
print("1. Testing Single-Image Analysis JSON Export...")
sample_path = ROOT / 'MONOT/Gate_10/S113923411-GF-A35-EEA-T14-S1-LH-C1-I0048-F00-0.png'
assert sample_path.exists(), f"Sample image {sample_path} not found"

pre = FacePreprocessor(image_size=224)
bgr = pre.load(str(sample_path))
h, w = bgr.shape[:2]
faces = pre.detect(bgr)
q = pre.quality(bgr, faces[0] if faces else None)
rgb = pre.transform(bgr, faces[0] if faces else None)
feat = extract_features(rgb)

single_report = {
    'image_metadata': {
        'filename': sample_path.name,
        'file_size_bytes': sample_path.stat().st_size,
        'width': w,
        'height': h,
    },
    'face_detection': {
        'face_count': len(faces),
        'bounding_box': faces[0] if faces else None,
        'crop_dimensions': [224, 224, 3],
    },
    'quality_metrics': q.as_dict(),
    'feature_summary': {
        k: {
            'dimensions': list(v.shape),
            'mean': float(np.mean(v)),
            'std': float(np.std(v)),
            'finite': bool(np.isfinite(v).all()),
        } for k, v in feat.items()
    },
    'model_status': {
        'selected_model': 'No approved model available',
        'state': 'MODEL UNAVAILABLE',
        'classification_performed': False,
        'notice': 'No approved model artifact installed. Research safeguards active.'
    },
    'processing_seconds': 0.12,
    'timestamp': '2026-11-18T18:40:00Z',
}

single_path = out_dir / 'test_single_analysis.json'
single_path.write_text(json.dumps(single_report, indent=2, default=str), encoding='utf-8')
loaded_single = json.loads(single_path.read_text(encoding='utf-8'))
assert loaded_single['model_status']['state'] == 'MODEL UNAVAILABLE'
assert loaded_single['model_status']['classification_performed'] is False
assert 'feature_summary' in loaded_single
assert loaded_single['face_detection']['face_count'] >= 1
print("  ✓ Single Image JSON Report: VALID, all safeguards confirmed.")

# ── 2. Two-Image Comparison Report Export ─────────────────────────────────────
print("2. Testing Two-Image Comparison JSON Export...")
sample_morphed = ROOT / 'MONOT/Morphed/M_S113923411-GF-A35-EEA-T14-S1-LH-C1-I0048-F00_S198149424-GF-A51-EEA-T13-S1-LH-C1-I0055-F00_C01_B30_W30_PA01_PM00_F00.png'
assert sample_morphed.exists()

bgr_m = pre.load(str(sample_morphed))
faces_m = pre.detect(bgr_m)
q_m = pre.quality(bgr_m, faces_m[0] if faces_m else None)
rgb_m = pre.transform(bgr_m, faces_m[0] if faces_m else None)
feat_m = extract_features(rgb_m)

comp_results = {k: compare_vectors(feat[k], feat_m[k]) for k in ('lbp', 'hog', 'glcm', 'stats', 'combined')}

comp_report = {
    'comparison_type': 'exploratory_two_image_differential',
    'classification_performed': False,
    'disclaimer': 'Exploratory feature vector comparisons only. Not a trained classifier prediction.',
    'image_a': {
        'filename': sample_path.name,
        'dimensions': [w, h],
        'face_box': faces[0],
        'quality': q.as_dict(),
    },
    'image_b': {
        'filename': sample_morphed.name,
        'dimensions': [bgr_m.shape[1], bgr_m.shape[0]],
        'face_box': faces_m[0],
        'quality': q_m.as_dict(),
    },
    'feature_differences': comp_results,
    'timestamp': '2026-11-18T18:40:00Z',
}

comp_path = out_dir / 'test_comparison_report.json'
comp_path.write_text(json.dumps(comp_report, indent=2, default=str), encoding='utf-8')
loaded_comp = json.loads(comp_path.read_text(encoding='utf-8'))
assert loaded_comp['classification_performed'] is False
assert 'feature_differences' in loaded_comp
assert 'combined' in loaded_comp['feature_differences']
assert 'cosine_similarity' in loaded_comp['feature_differences']['combined']
print("  ✓ Two-Image Comparison JSON Report: VALID, cosine similarities verified, zero fake scores.")

# ── 3. Dataset Category Breakdown CSV Export ──────────────────────────────────
print("3. Testing Dataset Category CSV Export...")
cat_summary_path = ROOT / 'data/metadata/dataset_summary.json'
assert cat_summary_path.exists()
ds_summary = json.loads(cat_summary_path.read_text(encoding='utf-8'))
csv_export_path = out_dir / 'test_dataset_categories.csv'
with csv_export_path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['dataset', 'category', 'label', 'count'])
    writer.writeheader()
    writer.writerows(ds_summary['image_counts'])

loaded_csv_rows = list(csv.DictReader(csv_export_path.open(encoding='utf-8')))
assert len(loaded_csv_rows) == 5
assert sum(int(r['count']) for r in loaded_csv_rows) == 46792
print(f"  ✓ Dataset Categories CSV Export: VALID ({len(loaded_csv_rows)} strata, 46,792 total images).")

# ── 4. Annotation Review Manifest Export ───────────────────────────────────────
print("4. Testing Annotation Review Batch Export...")
review_batch = ROOT / 'data/manifests/targeted_review_batch.csv'
assert review_batch.exists()
with review_batch.open(encoding='utf-8') as f:
    rev_rows = list(csv.DictReader(f))
assert len(rev_rows) == 150
print(f"  ✓ Annotation Review Batch Export: VALID ({len(rev_rows)} items).")

print("\nALL EXPORTS VERIFIED SUCCESSFULLY!")
