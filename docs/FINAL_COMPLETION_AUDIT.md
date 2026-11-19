# MorphGuard V3.0 — Comprehensive Completion Audit

**Date:** November 19, 2026  
**Operating Environment:** Windows 11, Python 3.10.11, CPU-only (8 logical cores, 7.85 GB RAM, 32.13 GB free disk)  
**Target Repository:** `https://github.com/AniketAgarwal-aa/MorphGuard`  
**Current Branch:** `master`  
**Latest Baseline Commit:** `3bd66e4805c15d58105dfcb4a207bd64c70a123b`  

---

## 1. Executive Summary

This audit establishes the empirical baseline of MorphGuard prior to the V3.0 finalisation phase. MorphGuard is an experimental facial morph detection research platform designed to evaluate classical feature engineering (LBP, HOG, GLCM, statistical properties), deep neural networks, and ensemble architectures on facial biometric datasets.

The system is strictly research-oriented: it does **not** claim ISO/IEC 30107-3 compliance or operational biometric certification. All claims are grounded in verifiable, reproducible local artifacts.

---

## 2. Inventory & Current State Audit

### 2.1 Raw Biometric Datasets
- **MONOT (`MONOT/`):** Total 24,140 biometric images.
  - `Gate_10`: 2,550 images (Controlled bona fide acquisition).
  - `Gate_25`: 6,350 images (Semi-controlled bona fide acquisition).
  - `Morphed`: 15,240 images (Delaunay triangular mesh landmark morphs).
- **ONOT (`ONOT/`):** Total 22,652 biometric images.
  - `digital`: 11,326 images (High-resolution digital bona fide capture).
  - `print-scan`: 11,326 images (Print-and-scan recapture variants).
- **Combined Raw Inventory:** **46,792 images** (Footprint: ~25.37 GB on disk).

### 2.2 Feature Cache (`data/cache/image_features/`)
- **Currently Cached:** 5,200 valid records across 15 compressed `.npz` shards.
- **Cache Size:** 382.9 MB.
- **Pending Candidates:** 41,592 images.
- **Schema:** 6,103 dimensions (LBP: 10D, HOG: 6,084D, GLCM: 5D, Stats: 4D) all float64 finite.
- **Status:** Resumable, idempotent shard streaming with SHA-256 file integrity verification.

### 2.3 Label Manifests & Reviewer Provenance
- **Reviewed Manifest (`data/manifests/reviewed_label_manifest.csv`):** 1,197 records.
  - `train`: 591 records (408 morphed, 183 genuine; 101 subject clusters).
  - `validation`: 321 records (264 morphed, 57 genuine; 52 subject clusters).
  - `test`: 285 records (228 morphed, 57 genuine; 42 subject clusters).
  - `reviewer_status`: 100% `approved`.
- **Identity Isolation:** Connected-component subject clustering guarantees **zero identity overlap** across Train, Validation, and Test splits.

### 2.4 Model Registry & Artifacts (`models/`)
- **Total Tracked Architectures:** 21 models in `models/metadata/model_registry.json`.
- **Trained Artifacts Present (15 models):**
  1. `custom_cnn` (`models/checkpoints/custom_cnn.pt`): Test Acc = 87.72%, ACER = 0.1096.
  2. `lda` (`models/trained/lda.joblib`): Test Acc = 80.70%, ACER = 0.1798.
  3. `stacking_ensemble` (`models/trained/stacking_ensemble.joblib`): Test Acc = 80.00%, ACER = 0.1711.
  4. `voting_ensemble` (`models/trained/voting_ensemble.joblib`): Test Acc = 57.54%, ACER = 0.3114.
  5. `rf_combined` (`models/trained/rf_combined.joblib`): Test Acc = 56.49%, ROC-AUC = 0.9879.
  6. `lbp_svm` (`models/trained/lbp_svm.joblib`): Test Acc = 54.74%, ACER = 0.3224.
  7. `gaussian_nb` (`models/trained/gaussian_nb.joblib`): Test Acc = 52.28%, ACER = 0.3509.
  8. `extra_trees` (`models/trained/extra_trees.joblib`): Test Acc = 51.93%, ROC-AUC = 0.9950.
  9. `glcm_rf` (`models/trained/glcm_rf.joblib`): Test Acc = 51.58%, ROC-AUC = 0.9058.
  10. `hist_gradient_boosting` (`models/trained/hist_gradient_boosting.joblib`): Test Acc = 51.58%, ROC-AUC = 0.9911.
  11. `knn` (`models/trained/knn.joblib`): Test Acc = 43.51%, ACER = 0.3991.
  12. `linear_svm` (`models/trained/linear_svm.joblib`): Test Acc = 25.96%, ROC-AUC = 0.9675.
  13. `logistic_regression` (`models/trained/logistic_regression.joblib`): Test Acc = 25.26%, ROC-AUC = 0.9769.
  14. `combined_svm` (`models/trained/combined_svm.joblib`): Test Acc = 23.51%, ROC-AUC = 0.9878.
  15. `hog_svm` (`models/trained/hog_svm.joblib`): Test Acc = 23.51%, ROC-AUC = 0.9867.
- **Compute-Gated Models (6 models):** `resnet18`, `resnet34`, `resnet50`, `efficientnet_b0`, `mobilenet_v3_small`, `densenet121` marked as `ready_for_training`.

---

## 3. What Already Works
1. **Automated Testing:** 23/23 tests passing (`pytest tests/ -v`).
2. **Dependency Tree:** `pip check` reports zero broken requirements.
3. **Application Navigation:** All 14 Streamlit pages load and render without unhandled exceptions.
4. **Live Application:** Streamlit daemon running on port 8501 responding with HTTP 200.
5. **Preprocessing & Feature Extraction:** Robust Haar face detection, image quality metrics (blur, brightness, contrast), and 6,103D feature extraction.
6. **Inference Pipeline:** Multi-model polymorphism supporting Scikit-learn `.joblib` and PyTorch `.pt` models with safety states (`INVALID IMAGE`, `FACE NOT DETECTED`, `MODEL UNAVAILABLE`).
7. **Git & Release Sanitation:** Sensitive biometric images, checkpoints, large NPZ shards, and private manifests are properly ignored by `.gitignore`.

---

## 4. What Is Partially Implemented or Missing
1. **Full Dataset Cache Coverage:** 5,200 of 46,792 images cached. The remaining 41,592 candidate images must be incrementally processed into shards.
2. **Formal Reports:** Missing dedicated report directory (`reports/`) containing:
   - `reports/dataset_inventory.csv`
   - `reports/label_distribution.csv`
   - `reports/dataset_quality_report.md`
   - `reports/label_provenance_report.md`
   - `reports/duplicate_audit.csv`
   - `reports/unlabelled_samples.csv`
   - `reports/split_leakage_audit.md`
   - `reports/split_assignments.csv`
   - Model test prediction logs in `reports/predictions/`
3. **High ROC-AUC / Low Accuracy Discrepancy:**
   - Linear models (Linear SVM, Logistic Regression, HOG SVM, Combined SVM) exhibited test accuracy of 23.5%–25.9% despite ROC-AUC > 0.96.
   - **Root Cause Identified:** Default decision threshold (0.5 on uncalibrated decision function or inverted probability index) under severe test imbalance (228 morphed vs 57 genuine). With proper validation-tuned decision thresholds, these models' high discrimination capability will yield appropriate accuracy and balanced APCER/BPCER.
4. **Deployment Hosted Model Fallback:**
   - To support cloud deployment (Streamlit Community Cloud) without committing 100+ MB model binaries to Git, a lazy download mechanism (`hf_hub_download` or hosted object storage) with SHA-256 verification and local offline fallback must be integrated.

---

## 5. Resource and Storage Feasibility
- **Available RAM:** 1.14 GB free (7.85 GB total). Concurrency must not exceed 4–6 worker threads to avoid memory paging.
- **Available Disk:** 32.13 GB free.
- **Projected Cache Footprint:** 46,792 images @ ~75 KB/compressed shard record = ~3.5 GB total storage. This is well within the 32.13 GB available limit.
- **Compute:** Local execution is CPU-only. Heavy 50-layer deep networks are compute-gated and require cloud GPU clusters; lightweight CNNs and Scikit-learn models execute cleanly locally.

---

## 6. Execution Plan

| Phase | Milestone | Actions |
| :--- | :--- | :--- |
| **Phase 1** | Full Dataset Utilization | Run inventory SHA-256 duplicate audit; process remaining 41,592 images in resumable batches of 500 records per shard using 4–6 workers. |
| **Phase 2 & 3** | Provenance & Leakage Audit | Generate all required reports (`reports/dataset_inventory.csv`, `reports/split_leakage_audit.md`, etc.); verify zero identity overlap. |
| **Phase 4 & 7** | Metric Calibration & Evaluation | Tune decision thresholds on the validation set using Youden's J statistic; re-evaluate test performance; export raw predictions to `reports/predictions/`. |
| **Phase 5 & 6** | Deep Learning & Ensembles | Evaluate CNN vs texture ensembles; ensure all compute-gated models are accurately tagged in registry. |
| **Phase 8 & 10** | App Polish & Inference | Verify all 14 pages; ensure explainability renders live for all models; verify single and dual-image inference. |
| **Phase 11** | Hosted Deployment Module | Implement `src/morphguard/inference/hosted_models.py` for authenticated/public lazy artifact retrieval with local caching. |
| **Phase 12–15** | Acceptance & Handover | Complete pytest (23+ tests), pip check, browser acceptance pass, update documentation, and push V3.0 release to GitHub. |
