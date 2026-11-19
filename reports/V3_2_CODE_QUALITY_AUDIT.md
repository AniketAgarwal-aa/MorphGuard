# MorphGuard V3.2 — Code Quality & Maintainability Audit

**Project:** MorphGuard — Facial Morph Attack Detection System  
**Audit Date:** November 19, 2026  
**Auditor:** MorphGuard Engineering  
**Scope:** `src/morphguard/`, `app/`, `tests/`, `config/`, `scripts/`  

---

## 1. Executive Summary

A comprehensive source code review was conducted across all Python modules to identify dead code, duplicate business logic, circular dependencies, hardcoded paths, unhandled exceptions, and abstraction bloat. The codebase is generally well-decoupled with clean separation of concerns among preprocessing, feature extraction, model definition, and inference orchestration.

Targeted refactorings and improvements were performed:
1. **PyTorch Architecture Auto-Resolution in `hosted_models.py`:** Fixed deep learning extension logic to properly recognize all PyTorch vision backbones (`resnet18`, `resnet34`, `resnet50`, `efficientnet_b0`, `densenet121`, `mobilenet_v3_small`) as `.pt` checkpoints rather than defaulting to `.joblib`.
2. **Quarantine of Obsolete Scripts:** Relocated 5 legacy scripts and 4 unreferenced `.bak` files.
3. **Circular Import Verification:** Validated that zero circular dependencies exist between `morphguard.dataset`, `morphguard.preprocessing`, `morphguard.feature_extraction`, `morphguard.classification`, and `morphguard.inference`.

---

## 2. Granular Module Analysis

### 2.1 Preprocessing (`src/morphguard/preprocessing/pipeline.py`)
- **Responsibilities:** Image decoding, OpenCV Haar face detection, image quality estimation (sharpness variance, brightness mean, contrast standard deviation, minimum face resolution), landmark alignment, and $(224 \times 224)$ normalized RGB cropping.
- **Error Handling:** Robust try/except handling with descriptive `ValueError` on corrupted or non-image data.
- **Hardcoded Paths:** Zero hardcoded paths; OpenCV cascade loaded dynamically from `cv2.data.haarcascades`.
- **Verdict:** **PASS** (Clean, self-contained, 100% test passing).

### 2.2 Feature Extraction (`src/morphguard/feature_extraction/features.py`)
- **Responsibilities:** Multi-scale handcrafted texture and gradient extraction.
  - `lbp`: 10-dimensional uniform Local Binary Patterns (`skimage.feature.local_binary_pattern`).
  - `hog`: 6,084-dimensional Histogram of Oriented Gradients (`skimage.feature.hog`).
  - `glcm`: 5-dimensional Haralick gray-level co-occurrence matrix features (`skimage.feature.graycomatrix`).
  - `stats`: 4 global pixel distribution moments.
  - `combined`: Concatenation yielding exactly 6,103 finite floating-point features.
- **NaN / Inf Safeguards:** Explicit `np.nan_to_num` applied to all descriptors.
- **Verdict:** **PASS**.

### 2.3 Model Architecture Definitions (`src/morphguard/classification/models.py`)
- **Responsibilities:** Model factory `create_model(architecture: str)`.
  - Supports `custom_cnn` (3-layer ConvNet with BatchNorm and Dropout).
  - Supports PyTorch vision backbones with customized binary classification heads:
    - `resnet18`, `resnet34`, `resnet50` (`fc` replaced by Linear(in_features, 2)).
    - `mobilenet_v3_small`, `efficientnet_b0` (`classifier` head adapted to 2 classes).
    - `densenet121` (`classifier` linear adapted to 2 classes).
- **Code Smells:** None. Clean factory design with explicit exception on unknown architecture.
- **Verdict:** **PASS**.

### 2.4 Inference Orchestration (`src/morphguard/inference/service.py`)
- **Responsibilities:** `InferenceService` orchestrates image ingestion $\to$ face detection $\to$ crop extraction $\to$ feature computation $\to$ model prediction $\to$ calibrated threshold decision $\to$ result explanation.
- **Binary Decision Logic:**
  - Strictly maps positive class index (`classes_` containing 1 or `'morphed'`).
  - Strict rule: $P(\text{morphed}) \ge \tau^* \implies \text{MORPHED}$; $P(\text{morphed}) < \tau^* \implies \text{GENUINE}$.
  - No artificial $\pm 0.05$ uncertainty zone.
  - Detailed non-technical explanations generated dynamically with model name and thresholds.
- **Safeguards:** Gracefully emits `INVALID IMAGE`, `FACE NOT DETECTED`, `MODEL UNAVAILABLE`, or `FEATURE EXTRACTION FAILED` with exact error reasons.
- **Verdict:** **PASS**.

### 2.5 Hosted & Local Model Manager (`src/morphguard/inference/hosted_models.py`)
- **Responsibilities:** Multi-tier artifact resolution (local trained models $\to$ local checkpoints $\to$ local cache $\to$ remote Hugging Face Hub download with SHA-256 integrity validation).
- **Refactoring Applied:**
  - Corrected extension resolution for deep vision models:
    ```python
    is_pytorch = (
        SUBFOLDERS.get(clean_name) == 'deep_learning'
        or clean_name.startswith("custom_cnn")
        or model_name.endswith(".pt")
    )
    ext = ".pt" if is_pytorch else ".joblib"
    ```
- **Verdict:** **PASS (Fixed)**.

---

## 3. Code Maintainability Metrics

| Metric | Target | Actual Value | Status |
| :--- | :---: | :---: | :---: |
| **PyTest Pass Rate** | 100% | 23 / 23 (100%) | **PASS** |
| **Package Dependency Conflicts** | 0 | 0 (`pip check` passed) | **PASS** |
| **Circular Imports** | 0 | 0 | **PASS** |
| **Hardcoded Secret Tokens** | 0 | 0 (`scan_secrets.py` passed) | **PASS** |
| **Unreferenced Backup Files** | 0 | 0 (all moved to `quarantine/`) | **PASS** |
| **Total Models Supported** | 21 | 21 fully verified | **PASS** |
