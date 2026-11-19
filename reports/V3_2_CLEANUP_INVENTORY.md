# MorphGuard V3.2 — Project Directory Cleanup Inventory

**Project:** MorphGuard — Facial Morph Attack Detection System  
**Date:** November 19, 2026  
**Status:** Audit & Action Plan  

---

## 1. Cleanup Inventory Table

| File / Folder Path | Current Purpose | Proposed Action | Technical Justification | Risk Level | Rollback Strategy |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `data/manifests/annotation_inventory.csv.bak` | Old backup of annotation inventory | **Move to Quarantine** | 16.8 MB unreferenced backup file. Active manifest is `annotation_inventory.csv`. | Low | Restorable from `quarantine/` |
| `data/cache/image_features/processing_manifest.csv.bak` | Old backup of processing manifest | **Move to Quarantine** | 162 KB backup file. Active file is `processing_manifest.csv`. | Low | Restorable from `quarantine/` |
| `data/cache/image_features/processing_summary.json.bak` | Old backup of processing summary | **Move to Quarantine** | 306 B backup file. Active file is `processing_summary.json`. | Low | Restorable from `quarantine/` |
| `data/metadata/dataset_summary.json.bak` | Old backup of dataset summary | **Move to Quarantine** | 1.4 KB backup file. Active file is `dataset_summary.json`. | Low | Restorable from `quarantine/` |
| `scripts/evaluate_models.py` | 6-line stub raising SystemExit | **Move to Quarantine** | Obsolete stub from v0.1 that refuses to run. Replaced by `verify_model_artifacts.py` & `pytest`. | Low | Restorable from `quarantine/` |
| `scripts/run_chrome_cdp.py` | Ad-hoc debugging script | **Move to Quarantine** | Unused local browser debugging script with hardcoded temp path. | Low | Restorable from `quarantine/` |
| `scripts/run_pipeline.py` | Legacy pipeline coordinator | **Move to Quarantine** | Calls superseded v1 split and baseline scripts. | Low | Restorable from `quarantine/` |
| `scripts/create_splits.py` | Legacy split generator | **Move to Quarantine** | Writes to empty `data/splits/`. Replaced by graph-partitioned `reviewed_label_manifest.csv`. | Low | Restorable from `quarantine/` |
| `scripts/label_review_summary.py` | Short redundant summary script | **Move to Quarantine** | 1KB script whose logic is fully integrated into `app/pages/annotation_review.py`. | Low | Restorable from `quarantine/` |
| `PROJECT_OVERVIEW.md` | Legacy V1.0 text | **Move to Quarantine** | Claims 0 reviewed labels and no validated detector; misleading and obsolete. | Low | Restorable from `quarantine/` |
| `PROJECT_REPORT.md` | Legacy early abstract | **Move to Quarantine** | Superseded by comprehensive reports in `reports/` and `README.md`. | Low | Restorable from `quarantine/` |
| `docs/RESULTS.md` | 126 B placeholder | **Move to Quarantine** | States "No model has been trained or evaluated". Completely inaccurate for V3.2. | Low | Restorable from `quarantine/` |
| `docs/EXPERIMENTS.md` | 255 B placeholder | **Move to Quarantine** | Empty placeholder file. | Low | Restorable from `quarantine/` |
| `docs/MODEL_ARCHITECTURE.md` | 253 B placeholder | **Move to Quarantine** | Empty placeholder file superseded by `MODEL_DOCUMENTATION.md`. | Low | Restorable from `quarantine/` |
| `docs/DATASET_SPLIT_REPORT.md` | 337 B placeholder | **Move to Quarantine** | Empty placeholder file superseded by `reports/split_leakage_audit.md`. | Low | Restorable from `quarantine/` |
| `docs/DATASET_VALIDATION_REPORT.md` | 454 B placeholder | **Move to Quarantine** | Empty placeholder file superseded by `reports/dataset_quality_report.md`. | Low | Restorable from `quarantine/` |
| `docs/CLEANUP_REPORT.md` | 303 B v1 cleanup note | **Move to Quarantine** | Historical note from early repo setup. | Low | Restorable from `quarantine/` |
| `docs/V1_RELEASE_CHECKLIST.md` | Superseded V1 checklist | **Move to Quarantine** | Historical checklist superseded by V3 releases. | Low | Restorable from `quarantine/` |
| `docs/V2_RELEASE_CHECKLIST.md` | Superseded V2 checklist | **Move to Quarantine** | Historical checklist superseded by V3 releases. | Low | Restorable from `quarantine/` |
| `docs/V2_ANNOTATION_PILOT_REPORT.md` | Superseded pilot report | **Move to Quarantine** | Superseded by `docs/ANNOTATION_REVIEW_ACCEPTANCE_REPORT.md`. | Low | Restorable from `quarantine/` |
| `docs/V3_RESEARCH_STATUS.md` | Superseded early V3 note | **Move to Quarantine** | Superseded by final verification reports. | Low | Restorable from `quarantine/` |
| `results/` | Empty directory with empty subdirs | **Remove directory** | Contains empty `metrics/`, `plots/`, `reports/`. All outputs live in `reports/`. | Zero | Can be re-created |
| `logs/` | Empty directory | **Remove directory** | Zero files. | Zero | Can be re-created |
| `data/processed/` | Empty directory | **Remove directory** | Zero files. | Zero | Can be re-created |
| `data/splits/` | Empty directory | **Remove directory** | Zero files. Manifests live in `data/manifests/`. | Zero | Can be re-created |
| `models/hf_export/` (root duplicates) | Duplicate root model copies | **Re-stage cleanly** | 15 `.joblib` & `.pt` files duplicated at root of `hf_export`. Re-stage all 21 models neatly by subfolder. | Low | Local originals remain in `models/trained/` & `models/checkpoints/` |

---

## 2. Protected Files (Never Delete)
The following core assets are strictly preserved:
- `MONOT/` and `ONOT/` raw biometric corpuses (46,792 images).
- `data/cache/image_features/` (182 NPZ shards, 3.39 GB).
- `data/cache/deep_face_crops.pt` (687.8 MB normalized tensor cache).
- `data/manifests/reviewed_label_manifest.csv` (1,197 vetted ground-truth rows).
- `models/trained/*.joblib` (14 trained classical model checkpoints).
- `models/checkpoints/*.pt` (7 trained PyTorch deep checkpoints).
- `models/metadata/*.json` (all 21 architecture metadata files and `model_registry.json`).
- All active application and library source files (`app/`, `src/morphguard/`).
- Test suite (`tests/`).
