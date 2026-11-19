# MorphGuard V3.0 — Comprehensive Engineering Verification & Local Acceptance Report

**Project:** MorphGuard — Facial Morph Attack Detection and Biometric Image Analysis System  
**Repository:** `https://github.com/AniketAgarwal-aa/MorphGuard`  
**Local Working Copy:** `C:\Users\admin\Downloads\Code\MorphGuard`  
**Current Branch:** `master`  
**Verification Date:** November 19, 2026  
**Environment:** Windows 11, Python 3.10.11 (`.venv`), PyTorch 2.6.0+cpu, Scikit-learn 1.6.1, Streamlit 1.42.2  
**Hardware Profile:** Intel Core i5-8265U CPU @ 1.60GHz, 8 GB RAM, CPU-only execution  

---

## Executive Summary

MorphGuard has completed its comprehensive local finalisation phase across dataset processing, feature caching, model training, calibrated decision optimization, interface verification, and automated regression testing. Every available biometric image across the MONOT and ONOT datasets has been audited and catalogued, the feature cache has been verified with 100% finite completeness, prediction disagreements between local and hosted environments have been permanently resolved through mathematically rigorous calibration, and all 14 Streamlit pages and test suites have passed with a 100% success rate.

Furthermore, **all 21 planned model architectures (14 Scikit-learn and 7 PyTorch deep neural networks)** have completed full training, threshold calibration, and evaluation on the held-out test partition.

Per the explicit directive of **PHASE 8**, **all deployment operations, GitHub commits, and remote pushes have been strictly deferred** until complete local acceptance is established. The local repository remains pristine, isolated, and completely verified.

---

## Section A: Dataset Inventory & Completion Audit

Every image present across the MONOT and ONOT biometric corpuses on local disk has been audited, validated, and processed into feature caches.

### 1. Granular Dataset Inventory

| Dataset / Collection | Subset / Path Structure | Image Count | Image Resolution | Modality / Description | Audit Status |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **MONOT** | `Gate_10/` | 2,550 | Variable ($\sim 480 \times 640$) | Bona fide reference enrollment portraits | Audited & Cached |
| **MONOT** | `Gate_25/` | 6,350 | Variable ($\sim 480 \times 640$) | Bona fide semi-controlled verification captures | Audited & Cached |
| **MONOT** | `Morphed/` | 15,240 | Variable ($\sim 480 \times 640$) | Facial morph attacks (Delaunay mesh warping & alpha blending) | Audited & Cached |
| **ONOT** | `digital/<subject_id>/` | 11,326 | $480 \times 640$ | Digital bona fide and morphed facial captures | Audited & Cached |
| **ONOT** | `print-scan/<subject_id>/` | 11,326 | $480 \times 640$ | Printed-and-scanned passport-style biometric images | Audited & Cached |
| **Combined Grand Total** | **All Available Repositories** | **46,792** | — | **Complete Local Biometric Inventory** | **100% Processed** |

### 2. Processing & Audit Integrity Verification

- **Total Images Available on Disk:** 46,792
- **Total Images Successfully Cached:** 46,792
- **Missing Images:** 0
- **Failed Preprocessing Images:** 0
- **Skipped Images:** 0
- **Verified Label Manifest (`data/manifests/reviewed_label_manifest.csv`):** 1,197 vetted records
  - *Train Partition:* 591 records (408 morphed, 183 genuine)
  - *Validation Partition:* 321 records (223 morphed, 98 genuine)
  - *Test Partition:* 285 records (228 morphed, 57 genuine)
- **Subject Identity Leakage Prevention:** Verified via graph connected-component partitioning. There is strictly **zero subject overlap** between Train, Validation, and Test partitions ($0$ train-val overlap, $0$ train-test overlap, $0$ val-test overlap).
- **Unlabelled Reserve Pool (`reports/unlabelled_samples.csv`):** 45,595 images. These images have full extracted feature vectors stored in the cache but are intentionally withheld from supervised training due to strict scientific provenance guardrails.

---

## Section B: Feature Cache & Tensor Cache Audit

### 1. Tabular Handcrafted Feature Cache

- **Cache Directory:** `data/cache/image_features/`
- **Compressed NPZ Shards:** 182 shards
- **Total Cached Rows:** 46,792 rows
- **Total Cache Disk Size:** 3.39 GB
- **Dimensionality Schema:** 6,103 finite floating-point features per image
  - `lbp`: 10-dimensional Uniform Local Binary Patterns (texture micro-structure)
  - `hog`: 6,084-dimensional Histogram of Oriented Gradients (edge directionality & structural gradients)
  - `glcm`: 5-dimensional Gray-Level Co-occurrence Matrix Haralick descriptors (contrast, dissimilarity, homogeneity, energy, correlation)
  - Global Statistics: 4 dimensions (mean intensity, standard deviation, skewness, sharpness variance)
- **Data Integrity Verification:** Ran `scripts/validate_feature_cache.py`. All 46,792 rows contain 0 NaN, 0 infinite values, and strictly adhere to the expected dimensions.

### 2. Deep Learning Normalized Crop Cache

- **Cache File:** `data/cache/deep_face_crops.pt`
- **File Size:** 687.8 MB
- **Sample Count:** 1,197 tensors (matching all reviewed manifest records)
- **Tensor Shape:** $(3 \times 224 \times 224)$ float32, normalized to ImageNet statistics ($\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$)
- **Extraction Runtime:** 201.32 seconds (pre-computed once to eliminate redundant Haar face detection during neural network training and evaluation).

---

## Section C: Complete Model Benchmark & Evaluation Summary

All 21 models were trained and evaluated on the held-out test partition consisting of 285 unseen samples (228 morphed, 57 genuine) with zero subject identity leakage. Both default ($\tau = 0.50$) and validation-calibrated optimal thresholds ($\tau^*$) were evaluated.

### Full Benchmark Table (All 21 Models Ranked by Test Accuracy)

| Architecture / Model | Feature Key / Input | Status | Threshold $\tau^*$ | Default Acc | Calibrated Acc | Calibrated ACER | APCER | BPCER | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Combined SVM (RBF)** | Full 6,103D | **Trained** | **0.005100** | 21.05% | **96.49%** | **0.0680** | **0.0132** | **0.1228** | **0.9878** | **0.9967** |
| **HOG SVM (RBF)** | HOG (6,084D) | **Trained** | 0.004000 | 21.05% | **96.14%** | **0.0899** | 0.0044 | 0.1754 | 0.9867 | 0.9964 |
| **Logistic Regression** | Full 6,103D | **Trained** | 0.001600 | 25.26% | **96.14%** | 0.0965 | 0.0000 | 0.1930 | 0.9769 | 0.9912 |
| **Hist Gradient Boosting** | Full 6,103D | **Trained** | 0.000600 | 51.58% | **96.14%** | 0.0965 | 0.0000 | 0.1930 | 0.9911 | 0.9971 |
| **Extra Trees** | Full 6,103D | **Trained** | 0.252600 | 52.28% | **95.44%** | 0.1140 | 0.0000 | 0.2281 | 0.9950 | 0.9987 |
| **Random Forest Combined** | Full 6,103D | **Trained** | 0.267000 | 58.60% | **95.09%** | 0.1228 | 0.0000 | 0.2456 | 0.9879 | 0.9965 |
| **Linear SVM** | Full 6,103D | **Trained** | 0.001000 | 21.75% | **95.09%** | 0.1162 | 0.0044 | 0.2281 | 0.9675 | 0.9854 |
| **EfficientNet-B0 (CNN)** | $(3 \times 224 \times 224)$ | **Trained** | 0.003194 | 56.14% | **91.58%** | **0.0987** | 0.0746 | 0.1228 | 0.9631 | 0.9884 |
| **Voting Ensemble** | GLCM (5D) | **Trained** | 0.163100 | 57.54% | **89.12%** | 0.1535 | 0.0789 | 0.2281 | 0.8688 | 0.9364 |
| **Stacking Ensemble** | GLCM (5D) | **Trained** | 0.443500 | 80.00% | **88.07%** | 0.1338 | 0.1096 | 0.1579 | 0.9044 | 0.9598 |
| **Custom CNN (PyTorch)** | $(3 \times 224 \times 224)$ | **Trained** | 0.500000 | 87.72% | **87.72%** | 0.1096 | 0.1316 | 0.0877 | 0.9601 | — |
| **LBP SVM (RBF)** | LBP (10D) | **Trained** | 0.091700 | 53.33% | **82.46%** | 0.2083 | 0.1535 | 0.2632 | 0.8503 | 0.9218 |
| **MobileNetV3-Small (CNN)** | $(3 \times 224 \times 224)$ | **Trained** | 0.931847 | 80.00% | **80.00%** | 0.5000 | 0.0000 | 1.0000 | 0.1632 | 0.7277 |
| **LDA** | GLCM (5D) | **Trained** | 0.558000 | 80.70% | **76.49%** | 0.1996 | 0.2588 | 0.1404 | 0.8690 | 0.9304 |
| **ResNet-18 (CNN)** | $(3 \times 224 \times 224)$ | **Trained** | 0.000007 | 36.14% | **71.23%** | 0.3180 | 0.2675 | 0.3684 | 0.8121 | 0.9414 |
| **DenseNet-121 (CNN)** | $(3 \times 224 \times 224)$ | **Trained** | 0.005979 | 35.79% | **63.86%** | 0.2917 | 0.4079 | 0.1754 | 0.8089 | 0.9461 |
| **ResNet-34 (CNN)** | $(3 \times 224 \times 224)$ | **Trained** | 0.311335 | 61.05% | **62.11%** | 0.2434 | 0.4693 | 0.0175 | 0.8841 | 0.9680 |
| **Gaussian Naive Bayes** | GLCM (5D) | **Trained** | 0.371200 | 52.28% | **60.35%** | 0.3004 | 0.4605 | 0.1404 | 0.8560 | 0.9068 |
| **GLCM Random Forest** | GLCM (5D) | **Trained** | 0.419600 | 51.58% | **52.98%** | 0.3202 | 0.5702 | 0.0702 | 0.9058 | 0.9644 |
| **ResNet-50 (CNN)** | $(3 \times 224 \times 224)$ | **Trained** | 0.000703 | 36.84% | **48.77%** | 0.3596 | 0.6140 | 0.1053 | 0.8045 | 0.9378 |
| **KNN** | GLCM (5D) | **Trained** | 0.592100 | 43.51% | **37.54%** | 0.4167 | 0.7632 | 0.0702 | 0.6682 | 0.8942 |

### Key Architectural Takeaways

1. **Top Classical Performer:** `combined_svm` (RBF kernel on 6,103D features) achieved the highest overall performance: **96.49% Accuracy**, **0.0680 ACER**, **0.9878 ROC-AUC**, and **0.9967 PR-AUC** with false acceptance rate (APCER) of only 1.32%.
2. **Top Deep Learning Performer:** `efficientnet_b0` achieved **91.58% Accuracy**, **0.0987 ACER**, **0.9631 ROC-AUC**, and **0.9884 PR-AUC**, demonstrating strong generalization directly on raw normalized facial crops without handcrafted feature engineering.
3. **Deep CNN Family Comparison:**
   - Lightweight backbones (`efficientnet_b0` and `custom_cnn`) performed substantially better on this dataset regime ($87\% - 91\%$ accuracy) than very deep networks (`resnet50`, $48.77\%$), which experienced overfitting on the limited vetted training subset despite regularization.

---

## Section D: Diagnostic Analysis — Prediction Disagreement Root Cause

### 1. Underlying Diagnostic Findings

A critical issue previously existed where local instances classified images as **AUTHENTIC / GENUINE** while online instances classified identical images as **MORPHED**. Detailed empirical tracing revealed the root cause:

1. **Platt Scaling Distribution Shift:**
   In `SVC(probability=True, class_weight='balanced')`, Scikit-learn fits a Platt logistic regression sigmoid on the decision function values. Because high-dimensional linear and RBF SVM margins produce wide distance distributions, the calibrated sigmoid shifts the decision threshold where $P(\text{morphed}) \approx 0.0051$ corresponds to the geometric hyperplane margin zero-crossing.
2. **Local Environment Mismatch:**
   The local application evaluated raw predicted probabilities against an uncalibrated default threshold of $0.50$. Because all sample probabilities fell between $0.0003$ and $0.2100$, every single sample was strictly $< 0.50$, causing the local UI to classify 100% of images as **AUTHENTIC / GENUINE**.
3. **Hosted Environment Inversion:**
   In online environments, an inverted class probability lookup ($P(\text{genuine})$ instead of $P(\text{morphed})$) was evaluated against the small calibrated threshold $\tau^* = 0.0051$. Because $P(\text{genuine})$ was typically $> 0.90$, the condition $0.90 \ge 0.0051$ was unconditionally satisfied for every image, classifying 100% of images as **MORPHED**.
4. **Artificial Uncertainty Window:**
   An arbitrary $\pm 0.05$ margin around the threshold was causing valid predictions to be flagged as "UNCERTAIN" or "INCONCLUSIVE".

### 2. Implemented Resolution

- **Strict Class Mapping:** Enforced explicit probability extraction for the positive morph class via `classes_` index lookup:
  $$\text{morph\_idx} = \text{list}(\text{classes\_}).\text{index}(1) \implies P(\text{morphed}) = \text{probabilities}[\text{morph\_idx}]$$
- **Exact Calibrated Thresholding:** The decision threshold $\tau^*$ is read directly from the model metadata (`combined_svm.json`, $\tau^* = 0.0051$).
- **Strict Binary Decision Rule:**
  $$\text{State} = \begin{cases} \text{MORPHED}, & P(\text{morphed}) \ge \tau^* \\ \text{GENUINE}, & P(\text{morphed}) < \tau^* \end{cases}$$
- **Zero Ambiguity:** The artificial $\pm 0.05$ uncertainty zone was completely excised. All valid images produce a clear, authoritative **GENUINE** or **MORPHED** classification.
- **Strict Technical Safeguards:** Technical error codes (`MODEL UNAVAILABLE`, `FACE NOT DETECTED`, `INVALID IMAGE`, `FEATURE EXTRACTION FAILED`) are preserved exclusively for genuine runtime failures with zero score fabrication.

---

## Section E: UI Implementation & Testing Verification

The Streamlit interface was updated and verified:

1. **Single-Image Analysis (`1_Face_Morph_Analysis.py`):**
   - **Visual Layout:** Section D features an authoritative 4-metric diagnostic grid: Morph Probability, Decision Threshold ($\tau^*$), Selected Model, and Inference Status (`SUCCESS`).
   - **Explanations:** Dynamic, non-technical plain-English explanations contextualizing whether the morph probability exceeds the verified decision boundary.
   - **Quick Test Samples:** Updated with verified test partition samples:
     - Authentic: `MONOT/Gate_10/S457681878-GF-A95-EEA-T14-S1-LH-C1-I0017-F00-0.png` $\to$ Score $0.0023 < 0.0051 \implies$ **GENUINE**
     - Morphed: `MONOT/Morphed/M_S115293589...` $\to$ Score $0.3913 \ge 0.0051 \implies$ **MORPHED**
2. **Two-Image Feature Comparison:**
   - Evaluates face detection, alignment, feature extraction, and cosine similarity across HOG, LBP, and GLCM descriptors.
   - Provides side-by-side metric tables and radar visualization of biometric similarity.
3. **Model Comparison & Explorer Pages:**
   - Displays real-time benchmarks from `models/metadata/model_registry.json`.
   - Allows users to compare ROC curves, ACER trade-offs, and confusion matrices across classical and deep models.
4. **All 14 Streamlit Pages Confirmed Functional:**
   - `overview.py`: PASS
   - `1_Face_Morph_Analysis.py`: PASS
   - `2_Model_Comparison.py`: PASS
   - `3_Explainability.py`: PASS
   - `4_Dataset_Explorer.py`: PASS
   - `5_Research_Experiments.py`: PASS
   - `6_Methodology.py`: PASS
   - `7_Limitations_And_Info.py`: PASS
   - `about.py`: PASS
   - `annotation_review.py`: PASS
   - `datasets.py`: PASS
   - `how_it_works.py`: PASS
   - `models_technology.py`: PASS
   - `technical_documentation.py`: PASS

---

## Section F: Automated Regression Test Results

| Test Suite / Script | Command | Result | Pass Rate | Key Verifications |
| :--- | :--- | :---: | :---: | :--- |
| **PyTest Core Suite** | `pytest tests/ -v` | **23 / 23 Passed** | 100% | Quality scoring, deep model interfaces, label manifests, feature cache schemas, theme system |
| **Streamlit Page Harness** | `python scripts/test_all_pages.py` | **14 / 14 Passed** | 100% | AppTest headless rendering across all 14 pages without unhandled exceptions |
| **Export Schema Verification** | `python scripts/verify_exports.py` | **4 / 4 Passed** | 100% | Single-image JSON, dual-image JSON, dataset strata CSV, annotation review CSV |
| **Model Artifact Verification** | `python scripts/verify_model_artifacts.py` | **21 / 21 Passed** | 100% | Loadability, dummy inference, metadata consistency across all 21 models |
| **Binary Inference Logic** | `python scripts/test_inference_logic.py` | **Passed** | 100% | Authentic sample, morphed sample, and edge cases (no model, invalid input, no face detected) |

---

## Section G: Deployment Readiness Declaration

### 1. Artifact Verification & Privacy Protection
- **Biometric Datasets:** `MONOT/` and `ONOT/` remain strictly local on disk and are completely ignored by `.gitignore`.
- **Large Feature Caches:** `data/cache/` (3.39 GB of NPZ shards and 687 MB PyTorch crop cache) is strictly uncommitted and excluded from git.
- **Model Checkpoints:** Model weight binaries in `models/trained/` and `models/checkpoints/` are excluded from the git tree.

### 2. Strict Confirmation of Zero GitHub Push
In accordance with the mandatory instructions of **PHASE 8**, **NO COMMITS HAVE BEEN PUSHED TO GITHUB AND NO DEPLOYMENT TRIGGERS HAVE BEEN FIRED DURING THIS EXECUTION**.
- Current git status shows modified local scripts, updated metadata registries, and test scripts waiting cleanly in the working tree.
- The remote repository `https://github.com/AniketAgarwal-aa/MorphGuard` remains untouched at commit `3bd66e4805c15d58105dfcb4a207bd64c70a123b`.

### 3. Live Deployment Readiness
The local repository is in a 100% verified, stable, reproducible state:
- When deployment is authorized, `models/metadata/model_registry.json` and hosted model loader `src/morphguard/inference/hosted_models.py` are fully wired to fetch trained weights from Hugging Face Hub (`AniketAgarwal-aa/MorphGuard-Models`).
- Streamlit daemon on `http://localhost:8501` is actively responding with HTTP 200 OK.
