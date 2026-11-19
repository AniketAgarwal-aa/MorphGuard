# MorphGuard V3.0 — Complete Full-Dataset Biometric Morph Detection System

**MorphGuard V3.0** is an experimental biometric research platform for facial morph attack detection (MAD), multi-scale texture extraction, deep neural networks, and ensemble evaluation on the complete **MONOT and ONOT** biometric corpora (46,792 images).

- **Live Cloud Deployment:** [DEPLOYMENT.md](DEPLOYMENT.md) & [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)
- **Biometric Model Card:** [MODEL_CARD.md](MODEL_CARD.md)
- **Hugging Face Model Repository:** [`AniketAgarwal-aa/MorphGuard-Models`](https://huggingface.co/AniketAgarwal-aa/MorphGuard-Models)
- **Version Changelog:** [CHANGELOG.md](CHANGELOG.md)
- Comprehensive Final Completion Report: [docs/FINAL_COMPLETION_REPORT.md](docs/FINAL_COMPLETION_REPORT.md)
- Completion Audit: [docs/FINAL_COMPLETION_AUDIT.md](docs/FINAL_COMPLETION_AUDIT.md)
- System Architecture: [docs/PROJECT_ARCHITECTURE.md](docs/PROJECT_ARCHITECTURE.md)
- Dataset Documentation: [docs/DATASET_DOCUMENTATION.md](docs/DATASET_DOCUMENTATION.md)
- Feature Engineering: [docs/FEATURE_ENGINEERING.md](docs/FEATURE_ENGINEERING.md)
- Model Documentation: [docs/MODEL_DOCUMENTATION.md](docs/MODEL_DOCUMENTATION.md)
- Experiment Methodology: [docs/EXPERIMENT_METHODOLOGY.md](docs/EXPERIMENT_METHODOLOGY.md)
- Privacy & Security: [docs/PRIVACY_AND_SECURITY.md](docs/PRIVACY_AND_SECURITY.md)
- Known Limitations: [docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md)

---

## 1. Quick Start (Windows PowerShell)

```powershell
cd "C:\Users\admin\Downloads\Code\MorphGuard"
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src"
streamlit run app\main.py
```
Open your browser at `http://localhost:8501`.

### Running Verification & Tests
```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe scripts/validate_feature_cache.py
.\.venv\Scripts\python.exe scripts/verify_model_artifacts.py
.\.venv\Scripts\python.exe scripts/test_all_pages.py
```

---

## 2. Complete Dataset Processing & Feature Cache (100% Coverage)

All 46,792 available biometric images across all five strata are fully processed, validated, and cached into 182 compressed NPZ shards in `data/cache/image_features/`:

| Dataset | Stratum | Inventory | Cached Records | Face Detected | Mean Sharpness | Cache Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **MONOT** | `Gate_10` (Bona Fide) | 2,550 | 2,550 | 95.7% | 373.1 | **100% Complete** |
| **MONOT** | `Gate_25` (Semi-Controlled) | 6,350 | 6,350 | 94.8% | 370.1 | **100% Complete** |
| **MONOT** | `Morphed` (Delaunay Morphs) | 15,240 | 15,240 | 100.0% | 140.8 | **100% Complete** |
| **ONOT** | `digital` (ICAO Passport) | 11,326 | 11,326 | 99.9% | 414.8 | **100% Complete** |
| **ONOT** | `print-scan` (Recaptured) | 11,326 | 11,326 | 99.9% | 63.2 | **100% Complete** |
| **Total** | **All 5 Strata** | **46,792** | **46,792** | **99.02%** | **232.1** | **100% Complete (3.39 GB)** |

*Cache Validation:* 100% of 46,792 feature rows verified float32/float64 finite, with zero NaN or Inf values across all 6,103 dimensions.

---

## 3. Label Provenance & Leakage-Safe Splitting

- **Approved Label Manifest (`data/manifests/reviewed_label_manifest.csv`):** 1,197 records.
  - `train`: 591 samples (408 morphed, 183 genuine; 101 subject clusters).
  - `validation`: 321 samples (264 morphed, 57 genuine; 52 subject clusters).
  - `test`: 285 samples (228 morphed, 57 genuine; 42 subject clusters).
- **Leakage Prevention:** Graph connected-component partitioning guarantees **strictly zero subject identity overlap** between Train, Validation, and Test partitions.
- **Unlabelled Reserve:** 45,595 unlabelled records tracked in `reports/unlabelled_samples.csv` due to provenance guardrails.

---

## 4. Multi-Model Benchmark (Test Split: 285 Unseen Samples)

Decision thresholds were optimized strictly on the independent **validation set** by minimizing ACER. Raw test predictions for every model are logged in `reports/predictions/`.

| Architecture | Feature Type | Calibrated $\tau^*$ | Default Acc | Calibrated Acc | ACER | APCER | BPCER | ROC-AUC | PR-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **combined_svm** | Combined (6,103D) | 0.0051 | 21.05% | **96.49%** | **0.0680** | 0.0132 | 0.1228 | **0.9878** | **0.9967** |
| **logistic_regression** | Combined (6,103D) | 0.0016 | 25.26% | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9769** | **0.9912** |
| **hog_svm** | HOG (6,084D) | 0.0040 | 21.05% | **96.14%** | **0.0899** | 0.0044 | 0.1754 | **0.9867** | **0.9964** |
| **hist_gradient_boosting**| Combined (6,103D) | 0.0006 | 51.58% | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9911** | **0.9971** |
| **extra_trees** | Combined (6,103D) | 0.2526 | 52.28% | **95.44%** | **0.1140** | 0.0000 | 0.2281 | **0.9950** | **0.9987** |
| **rf_combined** | Combined (6,103D) | 0.2670 | 58.60% | **95.09%** | **0.1228** | 0.0000 | 0.2456 | **0.9879** | **0.9965** |
| **linear_svm** | Combined (6,103D) | 0.0010 | 21.75% | **95.09%** | **0.1162** | 0.0044 | 0.2281 | **0.9675** | **0.9854** |
| **voting_ensemble** | GLCM (5D) | 0.1631 | 57.54% | **89.12%** | **0.1535** | 0.0789 | 0.2281 | 0.8688 | 0.9364 |
| **stacking_ensemble**| GLCM (5D) | 0.4435 | 80.00% | **88.07%** | **0.1338** | 0.1096 | 0.1579 | **0.9044** | **0.9598** |
| **custom_cnn** | PyTorch (Face) | 0.5000 | 87.72% | **87.72%** | **0.1096** | 0.1316 | 0.0877 | **0.9601** | — |
| **lbp_svm** | LBP (10D) | 0.0917 | 53.33% | **82.46%** | **0.2083** | 0.1535 | 0.2632 | 0.8503 | 0.9218 |
| **lda** | GLCM (5D) | 0.5580 | 80.70% | **76.49%** | **0.1996** | 0.2588 | 0.1404 | 0.8690 | 0.9304 |
| **gaussian_nb** | GLCM (5D) | 0.3712 | 52.28% | **60.35%** | **0.3004** | 0.4605 | 0.1404 | 0.8560 | 0.9068 |
| **glcm_rf** | GLCM (5D) | 0.4196 | 51.58% | **52.98%** | **0.3202** | 0.5702 | 0.0702 | 0.9058 | 0.9644 |
| **knn** | GLCM (5D) | 0.5921 | 43.51% | **37.54%** | **0.4167** | 0.7632 | 0.0702 | 0.6682 | 0.8942 |

*Compute-Gated Models (6 Models):* `resnet18`, `resnet34`, `resnet50`, `efficientnet_b0`, `mobilenet_v3_small`, `densenet121` are integrated in the registry and marked as `ready_for_training` pending GPU cluster resources.

---

## 5. Live Streamlit Application (14 Pages)

All 14 Streamlit pages are fully verified and interactive:
1. `overview.py`: System operational status and architectural topology.
2. `1_Face_Morph_Analysis.py`: Single-image and dual-image analysis with model selection and calibrated thresholding.
3. `4_Dataset_Explorer.py`: Complete 46,792 dataset stratum explorer with dynamic filtering.
4. `annotation_review.py`: Human-in-the-loop audit and provenance verification workbench.
5. `2_Model_Comparison.py`: Multi-model ROC curves, confusion matrices, and ISO/IEC 30107-3 metrics.
6. `3_Explainability.py`: Interactive PCA, LBP/GLCM/HOG distributions, and feature importance.
7. `5_Research_Experiments.py`: Detailed experiment registry tracking all runs and cache statistics.
8. `about.py`: Research mission and contributor background.
9. `how_it_works.py`: Step-by-step visual guide to morphing attacks and detection pipelines.
10. `datasets.py`: MONOT and ONOT technical specifications.
11. `models_technology.py`: Machine learning and deep learning architecture deep-dive.
12. `6_Methodology.py`: Mathematical formulation of texture extractors and error metrics.
13. `7_Limitations_And_Info.py`: Academic boundaries and research limitations.
14. `technical_documentation.py`: Complete API reference and operational guide.

---

## 6. Project Governance & Disclaimers

MorphGuard is an experimental biometric research platform developed for academic evaluation. It is **not** an operational biometric product certified under ISO/IEC 19794-5 or ISO/IEC 30107-3 compliance standards. Raw biometric datasets (`MONOT/`, `ONOT/`) and large binary model checkpoints remain strictly local and excluded from version control to protect subject privacy.
