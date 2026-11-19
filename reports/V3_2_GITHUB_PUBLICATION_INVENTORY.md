# MorphGuard V3.2 — GitHub Publication Inventory & Safety Audit

**Project:** MorphGuard — Facial Morph Attack Detection and Biometric Image Analysis System  
**Date:** November 19, 2026  
**Status:** Prepared for Review & User Authorization (Phase 2 Checkpoint)  

---

## 1. Publication Inventory: Intended Tracked Files

The following files represent the clean, reproducible source repository intended for public release on GitHub:

### Core Application & UI (`app/`)
- `app/main.py`: Entry point and 6-group sidebar navigation.
- `app/components/ui.py`: Centralized UI components, theme styling, and KPI primitives.
- `app/pages/*.py`: 14 modular Streamlit pages (`overview.py`, `1_Face_Morph_Analysis.py`, `2_Model_Comparison.py`, `3_Explainability.py`, `4_Dataset_Explorer.py`, `5_Research_Experiments.py`, `6_Methodology.py`, `7_Limitations_And_Info.py`, `about.py`, `annotation_review.py`, `datasets.py`, `how_it_works.py`, `models_technology.py`, `technical_documentation.py`).

### Scientific Package (`src/morphguard/`)
- `src/morphguard/preprocessing/`: Image loading, Haar face detection, bounding box expansion, and sharpness/contrast quality estimation.
- `src/morphguard/feature_extraction/`: Deterministic HOG (6084D), LBP (10D), and GLCM (5D) extractors.
- `src/morphguard/classification/`: Classifier implementations and meta-ensembles.
- `src/morphguard/inference/`: `InferenceService` and `hosted_models.py` multi-tier model loader.
- `src/morphguard/evaluation/`: ISO/IEC 30107-3 biometric presentation attack metrics (APCER, BPCER, ACER).
- `src/morphguard/dataset/`: Manifest readers and split loaders.

### Model Metadata (`models/metadata/`)
- `model_registry.json`: Authoritative 21-model catalog with feature keys, calibrated thresholds ($\tau^*$), and validation metrics.
- Deep architecture metadata manifests (`resnet18.json`, `resnet34.json`, `resnet50.json`, `efficientnet_b0.json`, `mobilenet_v3_small.json`, `densenet121.json`).

### Standardized Documentation (`docs/` & Root)
- Root `README.md`: Modernized 21-section technical overview.
- `MODEL_CARD.md`: Standardized Biometric Model Card complying with AI governance guidelines.
- `docs/ARCHITECTURE.md`: Detailed component topology and data flow.
- `docs/METHODOLOGY.md`: Mathematical formulations of texture descriptors and ISO/IEC 30107-3 metrics.
- `docs/DATASET_DOCUMENTATION.md`: MONOT & ONOT dataset provenance, stratum details, and split protocols.
- `docs/MODEL_EVALUATION.md`: 21-model empirical benchmark on the 285-sample test split.
- `docs/INSTALLATION.md`: Environment and setup instructions across platforms.
- `docs/DEPLOYMENT.md`: Hosting architecture and Streamlit Community Cloud guidance.
- `docs/PRIVACY_AND_ETHICS.md`: Biometric privacy governance and non-commercial usage terms.
- `docs/CONTRIBUTING.md`: Development principles and PR verification checklist.

### Verification Scripts & Tests (`scripts/` & `tests/`)
- `tests/test_core.py`: 23 comprehensive pytest test cases.
- `scripts/test_all_pages.py`: Automated 14-page headless rendering test.
- `scripts/verify_exports.py`: Verification of JSON and CSV report schemas.
- `scripts/verify_model_artifacts.py`: Verification of model loading and synthetic inference.
- `scripts/verify_dataset_integrity.py`: Split identity leakage and image accounting verification.
- `scripts/test_inference_logic.py`: Verification of strict binary decision thresholds.
- `scripts/scan_secrets.py`: Credential and token scanning utility.

### Configuration & Dependencies
- `requirements.txt`: Python package specifications.
- `pyproject.toml`: Pytest configuration.
- `.gitignore`: Defensive boundary rules.
- `.streamlit/config.toml`: Production server configuration.

---

## 2. Excluded Categories (Strictly Kept Out of Git)

The following items are isolated by `.gitignore` and are strictly excluded from GitHub tracking:

1. **Raw Biometric Images:** All face images from `MONOT/` and `ONOT/` directories.
2. **Processed Image Caches:** All face crops in `data/processed/` and `data/cache/`.
3. **Feature Tensors:** All 182 `.npz` feature cache shards (`data/cache/image_features/`).
4. **Private Manifests:** Raw database manifests (`reviewed_label_manifest.csv`, `annotation_inventory.csv`, SQLite files).
5. **Model Checkpoints & Weights:** Large binary weights (`*.joblib`, `*.pt` in `models/trained/`, `models/checkpoints/`, `models/hf_export/`).
6. **Environment Files & Secrets:** `.venv/`, `.env`, and temporary token files.
7. **Quarantine Archive:** Archived obsolete files and backups in `quarantine/`.
8. **Runtime Cache:** `__pycache__/`, `.pytest_cache/`, and log files.

---

## 3. Git History Audit Summary

- Git log history was scanned across all branches and commits.
- **Zero raw image files (`.png`, `.jpg`, `.jpeg`) have ever been committed.**
- **Zero binary model checkpoints (`.joblib`, `.pt`) have ever been committed.**
- **Zero secrets or API keys have ever been committed.**
- Repository history is completely clean and free of biometric data.

---

## 4. Licensing Segregation Summary

- **Application Source Code:** Original framework code is provided for research and academic evaluation.
- **Biometric Corpora (MONOT/ONOT):** Creative Commons Attribution-NonCommercial 4.0 International (**CC BY-NC 4.0**).
- **Trained Model Weights:** As mathematical derivatives of MONOT and ONOT representations, trained weights inherit **CC BY-NC 4.0** non-commercial restrictions.
