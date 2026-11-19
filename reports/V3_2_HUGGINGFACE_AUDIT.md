# MorphGuard V3.2 — Hugging Face Model Repository Audit

**Repository:** `AniketAgarwal-aa/MorphGuard-Models`  
**Repository Type:** Model Hub  
**Audit Date:** November 19, 2026  
**Auditor:** MorphGuard Engineering  

---

## 1. Remote Repository Inspection

- **Remote Status:** Private repository on Hugging Face Hub (`https://huggingface.co/AniketAgarwal-aa/MorphGuard-Models`).
- **Authentication State:** An unauthenticated query returns `401 Client Error: Repository Not Found (Private/Gated)`.
- **Local Staging State (`models/hf_export/`):**
  - **Total Staged Size:** 612.25 MB across 21 models + 22 metadata files.
  - **Directory Structure:**
    - `classical/`: 12 Scikit-Learn baseline and tree classifiers (*.joblib).
    - `deep_learning/`: 7 PyTorch neural network checkpoints (*.pt).
    - `ensembles/`: 2 Decision fusion models (voting and stacking ensembles, *.joblib).
    - `metadata/`: Architecture JSON descriptors and `model_registry.json`.
    - `README.md`: Public-facing Model Card.

---

## 2. Model-by-Model Artifact Verification Matrix

| Model Identifier | Framework | Artifact File | Size (MB) | Local Status | Remote State | SHA-256 Checksum (Truncated) |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **combined_svm** | scikit-learn | `combined_svm.joblib` | 10.95 | Ready / Staged | Pending Auth | `edcdbb4bfe600775...` |
| **custom_cnn** | PyTorch | `custom_cnn.pt` | 0.23 | Ready / Staged | Pending Auth | `f141d2b38e94965f...` |
| **densenet121** | PyTorch | `densenet121.pt` | 27.10 | Ready / Staged | Pending Auth | `9169572094dcad77...` |
| **efficientnet_b0** | PyTorch | `efficientnet_b0.pt` | 15.58 | Ready / Staged | Pending Auth | `ef6d7e5a4dfbbd61...` |
| **extra_trees** | scikit-learn | `extra_trees.joblib` | 1.10 | Ready / Staged | Pending Auth | `6ea40abb5be70817...` |
| **gaussian_nb** | scikit-learn | `gaussian_nb.joblib` | 0.01 | Ready / Staged | Pending Auth | `b26ce942d6c11364...` |
| **glcm_rf** | scikit-learn | `glcm_rf.joblib` | 0.73 | Ready / Staged | Pending Auth | `9e877b1f8aacefea...` |
| **hist_gradient_boosting** | scikit-learn | `hist_gradient_boosting.joblib` | 12.29 | Ready / Staged | Pending Auth | `9d7558d62dadc1eb...` |
| **hog_svm** | scikit-learn | `hog_svm.joblib` | 10.96 | Ready / Staged | Pending Auth | `5b1608dc820cd93c...` |
| **knn** | scikit-learn | `knn.joblib` | 0.05 | Ready / Staged | Pending Auth | `27b743888d758dd8...` |
| **lbp_svm** | scikit-learn | `lbp_svm.joblib` | 0.02 | Ready / Staged | Pending Auth | `c03852ef48922c77...` |
| **lda** | scikit-learn | `lda.joblib` | 0.01 | Ready / Staged | Pending Auth | `dd44eb2d0466a0e1...` |
| **linear_svm** | scikit-learn | `linear_svm.joblib` | 5.68 | Ready / Staged | Pending Auth | `7d4718f3f2b7af27...` |
| **logistic_regression** | scikit-learn | `logistic_regression.joblib` | 0.19 | Ready / Staged | Pending Auth | `e3dc99ae4b75e20b...` |
| **mobilenet_v3_small** | PyTorch | `mobilenet_v3_small.pt` | 5.92 | Ready / Staged | Pending Auth | `30ef3bf8670c0eb2...` |
| **resnet18** | PyTorch | `resnet18.pt` | 42.71 | Ready / Staged | Pending Auth | `4887d7e6dbd0826b...` |
| **resnet34** | PyTorch | `resnet34.pt` | 81.33 | Ready / Staged | Pending Auth | `fdbc80dc8ee75ac0...` |
| **resnet50** | PyTorch | `resnet50.pt` | 89.99 | Ready / Staged | Pending Auth | `f8927bc503efbc0a...` |
| **rf_combined** | scikit-learn | `rf_combined.joblib` | 0.49 | Ready / Staged | Pending Auth | `17408ba874821457...` |
| **stacking_ensemble** | scikit-learn | `stacking_ensemble.joblib` | 0.39 | Ready / Staged | Pending Auth | `fc926697ed5cde9a...` |
| **voting_ensemble** | scikit-learn | `voting_ensemble.joblib` | 0.34 | Ready / Staged | Pending Auth | `5ff29f33953d729e...` |

---

## 3. Privacy & Anti-Leakage Verification

The following sensitive assets are strictly excluded from the staging export and will **never** be uploaded to the Hugging Face repository:
1. **Raw Biometric Images:** Zero images from `MONOT/` or `ONOT/` are included.
2. **Face Crops:** Normalized cropped images and crop tensors are strictly excluded.
3. **Private Manifests:** Unlabelled records (`unlabelled_samples.csv`, 45,595 records) and personal subject IDs are excluded.
4. **Biometric Feature Caches:** Full feature caches (`data/cache/`, 3.39 GB) containing biometric vectors are excluded.
5. **Secrets & Tokens:** Zero environment files, tokens, or private credentials are included.

---

## 4. Loader & Runtime Compatibility

- **Local Loader (`src/morphguard/inference/hosted_models.py`):**
  - Confirmed: When running locally, models load directly from `models/trained/` and `models/checkpoints/` without needing an internet connection.
  - When running in cloud-hosted mode without local weights, `resolve_model_artifact()` retrieves weights via `hf_hub_download` and verifies SHA-256 integrity against `models/metadata/<model>.json`.
  - PyTorch architecture auto-resolution correctly identifies `.pt` models.

---

## 5. Recommendation & Publication Gate

- **Status:** **BLOCKED BY LICENSING REVIEW**
- The repository must remain **Private** until the user reviews and authorizes public distribution under the CC BY-NC 4.0 conditions assessed in `reports/V3_2_PUBLICATION_LICENSING_AUDIT.md`.
