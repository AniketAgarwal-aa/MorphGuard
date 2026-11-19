# MorphGuard V3.2 — Initial Comprehensive Project Audit

**Project:** MorphGuard — Facial Morph Attack Detection and Biometric Image Analysis System  
**Repository (GitHub):** `https://github.com/AniketAgarwal-aa/MorphGuard`  
**Model Repository (Hugging Face):** `https://huggingface.co/AniketAgarwal-aa/MorphGuard-Models`  
**Audit Timestamp:** 2026-11-19T21:20:00+05:30  
**Environment:** Windows 11, Python 3.10.11 (`.venv`), PyTorch 2.5.1+cpu, Scikit-learn 1.5.2, Streamlit 1.40.2  
**Audit Scope:** Full repository scan (Codebase, Models, Data Manifests, Caches, Scripts, Tests, Documentation, Security, UI/UX).

---

## 1. Executive Status Matrix

| Audit Domain | Status | Key Observation |
| :--- | :---: | :--- |
| **Code Architecture & Modules** | **PASS** | Modular package under `src/morphguard/` with clean boundaries (data, features, inference, preprocessing, models). |
| **Biometric Image Processing** | **PASS** | 46,792 biometric images across MONOT & ONOT audited and cached into 182 NPZ shards (6,103D schema). |
| **Model Inventory & Checkpoints** | **PASS** | All 21 models trained, calibrated, and evaluated; all checkpoints present in `models/trained/` & `models/checkpoints/`. |
| **Threshold Calibration Integrity** | **PASS** | Calibrated exclusively on the independent validation split ($\tau^*$ minimizing ACER); held-out test split (285 samples) strictly unobserved during tuning. |
| **Core Test Suite** | **PASS** | `pytest tests/ -q` passes 23/23 tests in 23.89s; all Streamlit pages render in AppTest harness. |
| **Inference Consistency & Class Mapping** | **PASS** | Confirmed strict binary classification ($P(\text{morphed}) \ge \tau^* \implies \text{MORPHED}$) with zero inverted index bugs. |
| **Directory Cleanliness & Redundancy** | **FAIL** | Multiple backup files (`.bak`), 56 documentation files (many outdated/v1 stubs), duplicate exports in `models/hf_export/`. |
| **UI/UX & Sidebar Hierarchy** | **WARNING** | Current sidebar lumps 14 pages into two generic sections (`MAIN PROJECT` & `ABOUT PROJECT`) without functional grouping; outdated v1 footer version. |
| **Remote Hugging Face State** | **WARNING** | Remote repository `AniketAgarwal-aa/MorphGuard-Models` is private/unauthenticated (HTTP 401 without token); only 15 models staged previously. |
| **Licensing & Redistribution Rights** | **BLOCKED BY REVIEW** | MONOT & ONOT datasets are licensed CC BY-NC 4.0. Model weight redistribution rights must be clearly assessed before making repo public. |
| **Security & Secrets Exposure** | **PASS** | Zero secrets in working directory or full Git history (`scan_secrets.py` reports 0 matches). |
| **Deployment Gate** | **BLOCKED** | Phase 8 & 14 strictly prohibit premature GitHub push or Streamlit Cloud deployment until explicit user authorization. |

---

## 2. Granular Architectural Audit

### 2.1 Existing Architecture
- **Core Package (`src/morphguard/`):**
  - `preprocessing/`: FacePreprocessor with OpenCV Haar cascade detection, quality scoring (sharpness, brightness, contrast, size), landmark alignment, and normalized face cropping $(224 \times 224)$.
  - `feature_extraction/`: Extract uniform LBP (10D), HOG (6,084D), GLCM Haralick descriptors (5D), and statistical moments (4D) $\to$ 6,103D feature vector.
  - `classification/`: Definitions for PyTorch custom CNN and torchvision backbones (ResNet-18, ResNet-34, ResNet-50, EfficientNet-B0, MobileNetV3-Small, DenseNet-121).
  - `inference/`: `InferenceService`, `ModelAdapter`, `HostedModelManager` (`hosted_models.py`).
  - `dataset/`: `audit.py`, `labels.py`, `review.py`, `splits.py` (graph connected-component partitioning for zero identity leakage).
- **Application (`app/`):**
  - `main.py`: Streamlit entrypoint with theme toggle and page navigation.
  - `components/ui.py` & `data.py`: Reusable CSS styles, metrics, headers, and audit loaders.
  - `pages/`: 14 pages covering Face Analysis, Model Comparison, Explainability, Dataset Explorer, Research Experiments, Methodology, Documentation, etc.

### 2.2 Working Modules (PASS)
- `morphguard.preprocessing.pipeline`: PASS. Full unit test coverage, handles corrupted inputs cleanly.
- `morphguard.feature_extraction.features`: PASS. Generates deterministic 6,103D vectors.
- `morphguard.inference.service`: PASS. Strict binary classification with calibrated thresholding, no artificial uncertainty zones.
- `morphguard.dataset.splits`: PASS. Strictly prevents cross-partition subject identity leakage.
- `scripts/verify_model_artifacts.py`: PASS. All 21 models load and infer dummy tensors cleanly.

### 2.3 Broken or Defective Logic (FAIL / WARNING)
1. **`hosted_models.py` Architecture Extension Check (WARNING):**
   - Line 58: `is_pytorch = clean_name.startswith("custom_cnn") or model_name.endswith(".pt")`.
   - If a caller asks for `'resnet18'` without `.pt`, it defaults `ext = ".joblib"`, failing to find the PyTorch `.pt` checkpoint. Needs to check `SUBFOLDERS.get(clean_name) == 'deep_learning'`.
2. **Obsolete / Broken Scripts (FAIL):**
   - `scripts/evaluate_models.py`: Obsolete 6-line stub that raises `SystemExit('Evaluation is blocked...')`.
   - `scripts/run_chrome_cdp.py`: Ad-hoc headless Chrome debugging script not part of the reproducible test harness.
   - `scripts/create_splits.py` & `scripts/run_pipeline.py`: Legacy v1 pipeline scripts writing to obsolete `data/splits/`.

### 2.4 Duplicate Implementations & Clutter (FAIL)
1. **Model Checkpoint Duplication:**
   - `models/hf_export/`: Duplicates 15 model files both in their subfolders (`classical/`, `deep_learning/`, `ensembles/`) and directly in the `hf_export/` root, consuming ~50+ MB redundantly.
2. **Backup Files (`*.bak`):**
   - `data/manifests/annotation_inventory.csv.bak` (16.8 MB)
   - `data/cache/image_features/processing_manifest.csv.bak` (162 KB)
   - `data/cache/image_features/processing_summary.json.bak` (306 B)
   - `data/metadata/dataset_summary.json.bak` (1.4 KB)
3. **Outdated Root Markdown Files:**
   - `PROJECT_OVERVIEW.md`: Claims "V1.0 ... no validated morph detector is claimed because reviewed label count is zero" (completely obsolete).
   - `docs/RESULTS.md` (126 B) & `docs/EXPERIMENTS.md` (255 B): Empty templates claiming "No model has been trained or evaluated".
   - `docs/V1_RELEASE_CHECKLIST.md`, `docs/V2_RELEASE_CHECKLIST.md`, `docs/V2_ANNOTATION_PILOT_REPORT.md`: Superseded historical checklist files.

### 2.5 Dependencies & Requirements (WARNING)
- `requirements.txt`: Pins `streamlit==1.40.2` and `scikit-learn==1.5.2`, matching `.venv`.
- `requirements-dev.txt`: Has `-r requirements.txt`.
- `requirements-inference.txt`: Stripped down inference dependencies for lightweight deployment.
- No broken requirements found via `pip check`.

### 2.6 Security Concerns (PASS)
- `scan_secrets.py`: 0 secret matches.
- Git commit history scan: 0 exposed GitHub, Hugging Face, or AWS tokens.
- Biometric corpuses (`MONOT/`, `ONOT/`) and large caches (`data/cache/`) are properly ignored by `.gitignore`.

### 2.7 UI/UX Weaknesses (WARNING)
1. **Sidebar Navigation Structure:** Currently grouped into only 2 large menus (`MAIN PROJECT` & `ABOUT PROJECT`). The user requested a logical 6-group hierarchy:
   - OVERVIEW (Dashboard, About)
   - ANALYSIS (Face Analysis)
   - MODELS & EVALUATION (Model Comparison, Explainability, Research Experiments)
   - DATA & METHODOLOGY (Dataset Explorer, Methodology, How It Works)
   - DOCUMENTATION (Models & Technology, Technical Documentation, Limitations & Privacy)
   - ADMINISTRATION / REVIEW (Annotation Review, Datasets)
2. **Version Inconsistencies:** Sidebar footer displays "v1.0.0 Research Edition", whereas the system is now MorphGuard V3.2.
3. **CSS / Design Uniformity:** Several page headings, tables, and metric cards have slightly different inline styles that should use unified components from `app/components/ui.py`.

---

## 3. Recommended Remediation Plan

1. **Phase 2 (Cleanup):**
   - Inventory all redundant files into `reports/V3_2_CLEANUP_INVENTORY.md`.
   - Remove `.bak` files, obsolete stubs (`evaluate_models.py`, `run_chrome_cdp.py`), and empty directories (`results/`, `logs/`).
   - Clean up and modernize `docs/` and root documentation.
2. **Phase 3 (Code Quality):**
   - Fix `hosted_models.py` extension logic for deep learning architectures.
   - Refactor reusable components and clean up unused imports.
3. **Phase 7 (UI/UX Redesign):**
   - Implement the 6-group structured sidebar in `app/main.py`.
   - Modernize `overview.py` (Dashboard), `1_Face_Morph_Analysis.py` (Analysis), and comparison tools.
4. **Phase 8, 9, 10 (Hugging Face & Licensing):**
   - Prepare clean staging for all 21 models.
   - Document CC BY-NC 4.0 data constraints and publication status in `reports/V3_2_PUBLICATION_LICENSING_AUDIT.md`.
5. **Phase 13, 14, 15 (Verification & Release Readiness):**
   - Verify full test harness, freeze git working tree, and generate final V3.2 completion report.
