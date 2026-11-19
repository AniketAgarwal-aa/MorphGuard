# MorphGuard — Facial Morph Attack Detection and Biometric Image Analysis System

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31011/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.5+-ee4c2c.svg)](https://pytorch.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.5+-f89939.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-yellow)](https://huggingface.co/AniketAgarwal-aa/MorphGuard-Models)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

**MorphGuard** is a comprehensive biometric research platform and software framework engineered for **Facial Morph Attack Detection (MAD)**. It integrates multi-scale texture extraction, 21 distinct machine learning and deep convolutional architectures, human-in-the-loop annotation auditing, and validation-calibrated decision thresholding complying with **ISO/IEC 30107-3** standards.

---

## Table of Contents
1. [Project Motivation & Problem Statement](#1-project-motivation--problem-statement)
2. [Main Objectives](#2-main-objectives)
3. [Key Features](#3-key-features)
4. [System Architecture](#4-system-architecture)
5. [Technical Stack](#5-technical-stack)
6. [Dataset Overview & Provenance](#6-dataset-overview--provenance)
7. [Data Preprocessing Pipeline](#7-data-preprocessing-pipeline)
8. [Feature Extraction Pipeline](#8-feature-extraction-pipeline)
9. [Model Architectures](#9-model-architectures)
10. [Evaluation Methodology](#10-evaluation-methodology)
11. [Benchmark Results](#11-benchmark-results)
12. [User Interface & Page Hierarchy](#12-user-interface--page-hierarchy)
13. [Installation & Setup](#13-installation--setup)
14. [Local Execution](#14-local-execution)
15. [Repository Structure](#15-repository-structure)
16. [Testing & Verification](#16-testing--verification)
17. [Limitations](#17-limitations)
18. [Ethical & Biometric Privacy Considerations](#18-ethical--biometric-privacy-considerations)
19. [Licensing](#19-licensing)
20. [Citation & Acknowledgments](#20-citation--acknowledgments)
21. [Future Improvements](#21-future-improvements)

---

## 1. Project Motivation & Problem Statement

Facial morphing attacks pose a critical vulnerability to international travel security and automated border control (ABC) gates. By blending the facial images of two or more individuals (such as an accomplice and a criminal applicant), a single photographic credential can match the facial biometrics of multiple subjects. When such an image is enrolled into an Electronic Machine Readable Travel Document (eMRTD), the fraudulent document can be verified against both individuals at automated border verification kiosks.

Detecting single-image facial morphs without an original reference gallery image (**No-Reference MAD**) is an open computer vision challenge. Morphed images often exhibit subtle high-frequency blending boundaries, ghosting around facial landmarks, and micro-texture compression differences. MorphGuard provides a reproducible, scientifically defensible platform to benchmark classical texture-based classifiers alongside deep neural networks against these vulnerabilities.

---

## 2. Main Objectives

1. **Large-Scale Corpus Ingestion:** Preprocess and cache feature vectors for the full available **MONOT and ONOT** biometric datasets (46,792 images total).
2. **Ground-Truth Provenance Isolation:** Establish strict provenance protocols to distinguish rigorously verified labels (1,197 records) from unlabelled research reserves (45,595 records).
3. **Leakage-Safe Partitioning:** Guarantee zero subject identity overlap across training, validation, and test splits using graph connected components.
4. **Comprehensive Model Benchmarking:** Train, calibrate, and compare 21 distinct machine learning and deep learning architectures.
5. **Standardized ISO/IEC 30107-3 Evaluation:** Measure Attack Presentation Classification Error Rate (APCER), Bona Fide Presentation Classification Error Rate (BPCER), and Average Classification Error Rate (ACER).
6. **Defensive, Interactive Serving:** Deliver a 14-page modern Streamlit interface with clear binary classification ($P \ge \tau^* \implies \text{MORPHED}$) and explicit technical error safeguards.

---

## 3. Key Features

- **21 Trained Model Checkpoints:** 14 Scikit-learn models (SVMs, Random Forests, Boosting, Ensembles) and 7 PyTorch deep models (ResNet-18/34/50, EfficientNet-B0, MobileNet-V3 Small, DenseNet-121, Custom CNN).
- **Validation-Calibrated Thresholds:** Operational decision thresholds ($\tau^*$) optimized strictly on independent validation data to minimize ACER.
- **Strict Binary Decision Engine:** Inconclusive predictions eliminated in favor of definitive classification grounded in mathematical thresholding.
- **Defensive Preprocessing:** Automatic Haar face detection, multi-face rejection, and blur/contrast image quality gating.
- **Explainability & Visual Analytics:** Interactive PCA projections, feature importance rankings, and multi-scale texture histograms.
- **Two-Image Comparative Verification:** Cosine similarity and Euclidean distance profiling between image pairs without conflating similarity with morphing attacks.
- **Privacy by Design:** Zero biometric images or cached vectors committed to Git; strict `.gitignore` isolation.

---

## 4. System Architecture

MorphGuard follows a decoupled layered architecture:

```
[ Web Browser ]
      |
      v
[ Streamlit UI (app/) ]
  ├── 6 Navigation Groups
  └── 14 Modular Functional Pages
      |
      v
[ Inference & Serving Engine (src/morphguard/) ]
  ├── Input Quality & Face Detection Gate (OpenCV Haar Cascade)
  ├── Multi-Scale Texture Extractors (HOG 6084D, LBP 10D, GLCM 5D)
  ├── Deep Feature Extractors (PyTorch ImageNet Normalization)
  └── Hosted Model Loader (Local weights -> Hugging Face Hub cache)
      |
      v
[ Model Execution & Decision Engine ]
  ├── 21 Trained Architecture Artifacts
  ├── Synchronized Metadata Registry (models/metadata/model_registry.json)
  └── Threshold Evaluator (P >= tau* -> MORPHED, else GENUINE)
```

Detailed architecture diagrams and design specifications are available in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 5. Technical Stack

- **Programming Language:** Python 3.10.11
- **Machine Learning & Modeling:** Scikit-learn 1.5.2, SciPy 1.13.1, NumPy 1.26.4
- **Deep Learning Framework:** PyTorch 2.5.1+cpu, Torchvision 0.20.1+cpu
- **Computer Vision & Image Processing:** OpenCV (headless) 4.10.0, Scikit-image 0.24.0, Pillow 10.4.0
- **User Interface & Serving:** Streamlit 1.40.2
- **Model Distribution:** Hugging Face Hub Python SDK 0.26.2
- **Testing & Quality Assurance:** Pytest 8.3.5

---

## 6. Dataset Overview & Provenance

MorphGuard processes two major facial biometric research corpora:

| Corpus | Stratum | Description | Total Images | Processing Status |
| :--- | :--- | :--- | :---: | :---: |
| **MONOT** | `Gate_10` | Controlled bona fide ABC border gate captures | 2,550 | 100% Cached |
| **MONOT** | `Gate_25` | Semi-controlled bona fide captures | 6,350 | 100% Cached |
| **MONOT** | `Morphed` | Delaunay-triangulated morph attacks | 15,240 | 100% Cached |
| **ONOT** | `digital` | High-quality ICAO compliant digital passport photos | 11,326 | 100% Cached |
| **ONOT** | `print-scan`| Physical print and flatbed scanned recaptures | 11,326 | 100% Cached |
| **Total** | **All 5 Strata** | Complete research corpus | **46,792** | **100% Cached (3.39 GB)** |

### Distinction Between Processed Corpus & Reviewed Manifest
- **Complete Corpus (46,792 images):** 100% preprocessed and cached into 182 NPZ shards for exploratory and feature analysis.
- **Reviewed Label Manifest (1,197 records):** High-confidence subset with cryptographic, folder-level, or expert ground-truth validation.
- **Unlabelled Research Reserve (45,595 records):** Maintained separately in `reports/unlabelled_samples.csv` to prevent label noise during supervised training.

### Zero Identity Leakage Partitioning
The 1,197 reviewed records are partitioned at the subject-cluster level using graph connected components:
- **Train (591 samples / 101 subject clusters):** Supervised training partition.
- **Validation (321 samples / 52 subject clusters):** Threshold calibration ($\tau^*$) and hyperparameter tuning.
- **Test (285 samples / 42 subject clusters):** Held-out unbiased benchmark evaluation.
- **Identity Leakage:** Strictly **0 subject overlap** across all three partitions.

See [docs/DATASET_DOCUMENTATION.md](docs/DATASET_DOCUMENTATION.md) for full provenance analysis.

---

## 7. Data Preprocessing Pipeline

1. **Format Validation:** Verified RGB 8-bit image array. Non-image or corrupted inputs trigger `INVALID IMAGE`.
2. **Face Detection:** OpenCV Haar Cascade detector identifies primary frontal faces. Multi-face inputs trigger warning; zero-face inputs trigger `FACE NOT DETECTED`.
3. **Face Cropping & Margin Expansion:** Bounding box expanded by 20% margin to include hairline, jaw contours, and ears where morphing artefacts frequently concentrate.
4. **Quality Estimation:**
   - Sharpness: Laplacian variance ($> 50$ threshold).
   - Contrast: Michelson contrast ratio ($> 0.20$ threshold).

---

## 8. Feature Extraction Pipeline

- **Histogram of Oriented Gradients (HOG):** $16 \times 16$ pixel cells, $2 \times 2$ blocks, 9 bins $\rightarrow$ **6,084 dimensions**.
- **Local Binary Patterns (LBP):** Circular uniform pattern ($P=8, R=1$) $\rightarrow$ **10 dimensions**.
- **Gray-Level Co-occurrence Matrix (GLCM):** Multi-distance ($d \in \{1, 3, 5\}$), 4 angles $\rightarrow$ **5 dimensions**.
- **Combined Feature Vector:** Concatenation of HOG, LBP, GLCM, and quality scalars $\rightarrow$ **6,103 dimensions**.

Mathematical formulations are documented in [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

---

## 9. Model Architectures

MorphGuard integrates 21 model architectures across two major paradigms:

1. **Classical Machine Learning (14 Models):**
   - Support Vector Machines (SVM RBF, Linear SVM) on Combined, HOG, and LBP features.
   - Tree & Ensemble Classifiers (Random Forest, Extra Trees, HistGradientBoosting).
   - Linear & Probabilistic Classifiers (Logistic Regression, LDA, Gaussian Naive Bayes, KNN).
   - Meta-Ensembles (Voting Ensemble, Stacking Classifier with Logistic Regression meta-learner).
2. **Deep Convolutional Neural Networks (7 Models):**
   - ResNet-18, ResNet-34, ResNet-50.
   - EfficientNet-B0 (compound scaled).
   - MobileNet-V3 Small (latency optimized).
   - DenseNet-121 (dense feature reuse).
   - Custom CNN (4-layer lightweight baseline).

---

## 10. Evaluation Methodology

1. **Metric Standardization:** Evaluated strictly using ISO/IEC 30107-3 presentation attack detection metrics (APCER, BPCER, ACER), ROC-AUC, and PR-AUC.
2. **Strict Threshold Tuning Protocol:**
   $$\tau^* = \arg\min_{\tau \in [0, 1]} \text{ACER}_{\text{val}}(\tau)$$
   Decision thresholds were chosen purely on validation data and frozen before test evaluation.
3. **Unbiased Held-Out Test Evaluation:** All reported benchmark metrics reflect inference on the unseen 285-sample test set.

---

## 11. Benchmark Results

### Complete 21-Model Performance (Held-Out Test Set: 285 Samples)

| Architecture | Model Family | Feature Key | Calibrated $\tau^*$ | Test Accuracy | ACER | APCER | BPCER | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **combined_svm** | SVM (RBF) | Combined (6,103D) | 0.0051 | **96.49%** | **0.0680** | 0.0132 | 0.1228 | **0.9878** | **0.9967** |
| **hog_svm** | SVM (RBF) | HOG (6,084D) | 0.0040 | **96.14%** | **0.0899** | 0.0044 | 0.1754 | **0.9867** | **0.9964** |
| **logistic_regression** | Linear | Combined (6,103D) | 0.0016 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | 0.9769 | 0.9912 |
| **hist_gradient_boosting**| Boosting | Combined (6,103D) | 0.0006 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9911** | **0.9971** |
| **extra_trees** | Ensemble | Combined (6,103D) | 0.2526 | **95.44%** | **0.1140** | 0.0000 | 0.2281 | **0.9950** | **0.9987** |
| **rf_combined** | Ensemble | Combined (6,103D) | 0.2670 | **95.09%** | **0.1228** | 0.0000 | 0.2456 | 0.9879 | 0.9965 |
| **linear_svm** | Linear SVM | Combined (6,103D) | 0.0010 | **95.09%** | **0.1162** | 0.0044 | 0.2281 | 0.9675 | 0.9854 |
| **efficientnet_b0** | PyTorch Deep | RGB ($224^2$) | 0.0032 | **91.58%** | **0.0987** | 0.0746 | 0.1228 | **0.9631** | **0.9884** |
| **voting_ensemble** | Voting | GLCM (5D) | 0.1631 | **89.12%** | **0.1535** | 0.0789 | 0.2281 | 0.8688 | 0.9364 |
| **stacking_ensemble**| Stacking | GLCM (5D) | 0.4435 | **88.07%** | **0.1338** | 0.1096 | 0.1579 | 0.9044 | 0.9598 |
| **custom_cnn** | PyTorch Deep | RGB ($224^2$) | 0.5000 | **87.72%** | **0.1096** | 0.1316 | 0.0877 | 0.9601 | — |
| **lbp_svm** | SVM (RBF) | LBP (10D) | 0.0917 | **82.46%** | **0.2083** | 0.1535 | 0.2632 | 0.8503 | 0.9218 |
| **mobilenet_v3_small**| PyTorch Deep | RGB ($224^2$) | 0.9318 | **80.00%** | **0.5000** | 0.0000 | 1.0000 | 0.1632 | 0.7277 |
| **lda** | Linear | GLCM (5D) | 0.5580 | **76.49%** | **0.1996** | 0.2588 | 0.1404 | 0.8690 | 0.9304 |
| **resnet18** | PyTorch Deep | RGB ($224^2$) | 0.000007 | **71.23%** | **0.3180** | 0.2675 | 0.3684 | 0.8121 | 0.9414 |
| **densenet121** | PyTorch Deep | RGB ($224^2$) | 0.005979 | **63.86%** | **0.2917** | 0.4079 | 0.1754 | 0.8089 | 0.9461 |
| **resnet34** | PyTorch Deep | RGB ($224^2$) | 0.311335 | **62.11%** | **0.2434** | 0.4693 | 0.0175 | 0.8841 | 0.9680 |
| **gaussian_nb** | Naive Bayes | GLCM (5D) | 0.3712 | **60.35%** | **0.3004** | 0.4605 | 0.1404 | 0.8560 | 0.9068 |
| **glcm_rf** | Random Forest| GLCM (5D) | 0.4196 | **52.98%** | **0.3202** | 0.5702 | 0.0702 | 0.9058 | 0.9644 |
| **resnet50** | PyTorch Deep | RGB ($224^2$) | 0.000703 | **48.77%** | **0.3596** | 0.6140 | 0.1053 | 0.8045 | 0.9378 |
| **knn** | Neighbors | GLCM (5D) | 0.5921 | **37.54%** | **0.4167** | 0.7632 | 0.0702 | 0.6682 | 0.8942 |

*Full evaluation metrics, confusion matrices, and analysis are detailed in [docs/MODEL_EVALUATION.md](docs/MODEL_EVALUATION.md).*

---

## 12. User Interface & Page Hierarchy

The application features 14 modular pages structured into 6 clear functional groups:

```
MorphGuard Navigation
├── 1. Detection & Verification
│   ├── Face Morph Analysis (1_Face_Morph_Analysis.py)
│   └── Executive Dashboard (overview.py)
├── 2. Biometric Data & Provenance
│   ├── Dataset Explorer (4_Dataset_Explorer.py)
│   ├── Annotation Review Workbench (annotation_review.py)
│   └── Dataset Technical Specs (datasets.py)
├── 3. Benchmarking & Evaluation
│   ├── Multi-Model Comparison (2_Model_Comparison.py)
│   ├── Research Experiments (5_Research_Experiments.py)
│   └── Model Architecture Deep-Dive (models_technology.py)
├── 4. Interpretability & Explainability
│   └── Feature Space Explorer (3_Explainability.py)
├── 5. Documentation & Scientific Standards
│   ├── Methodology & Formulas (6_Methodology.py)
│   ├── Technical API Docs (technical_documentation.py)
│   └── How It Works Guide (how_it_works.py)
└── 6. Governance & Limitations
    ├── Limitations & Disclaimers (7_Limitations_And_Info.py)
    └── Research Mission & About (about.py)
```

---

## 13. Installation & Setup

```powershell
# Clone the repository
git clone https://github.com/AniketAgarwal-aa/MorphGuard.git
cd MorphGuard

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

See [docs/INSTALLATION.md](docs/INSTALLATION.md) for Ubuntu and macOS instructions.

---

## 14. Local Execution

```powershell
# Set Python path to source directory
$env:PYTHONPATH = "src"

# Launch Streamlit web interface
streamlit run app/main.py
```
Open `http://localhost:8501` in your browser.

---

## 15. Repository Structure

```text
MorphGuard/
├── app/                      # Streamlit application
│   ├── main.py               # Application entrypoint & 6-group sidebar
│   ├── components/ui.py      # UI primitives, KPI cards, theme CSS
│   └── pages/                # 14 distinct functional page views
├── src/morphguard/           # Core scientific Python package
│   ├── classification/       # Scikit-learn classifier wrappers
│   ├── dataset/              # Dataset loaders & NPZ cache reader
│   ├── evaluation/           # ISO/IEC 30107-3 metric computations
│   ├── feature_extraction/   # HOG, LBP, GLCM mathematical extractors
│   ├── inference/            # InferenceService & hosted_models loader
│   ├── preprocessing/        # Face detection & quality assessment
│   └── training/             # Deep model training loops
├── models/
│   └── metadata/             # model_registry.json & architecture specs
├── docs/                     # Comprehensive technical documentation
├── reports/                  # Evaluation benchmarks, audit reports
├── scripts/                  # Verification, secret scanning, testing
├── tests/                    # 23-test Pytest test suite
├── .gitignore                # Defensive biometric & credential isolation
├── MODEL_CARD.md             # Standardized Biometric Model Card
├── README.md                 # Project README
├── requirements.txt          # Python dependencies
└── pyproject.toml            # Build system & pytest configuration
```

---

## 16. Testing & Verification

MorphGuard maintains a comprehensive automated testing pipeline:

```powershell
$env:PYTHONPATH = "src"

# 1. Run unit test suite (23/23 tests)
pytest tests/ -v

# 2. Verify all 14 Streamlit pages render cleanly
python scripts/test_all_pages.py

# 3. Verify JSON and CSV export schemas
python scripts/verify_exports.py

# 4. Verify all 21 model checkpoints and metadata
python scripts/verify_model_artifacts.py

# 5. Verify zero dataset split identity leakage
python scripts/verify_dataset_integrity.py

# 6. Verify strict binary inference logic
python scripts/test_inference_logic.py

# 7. Scan repository for leaked credentials
python scripts/scan_secrets.py

# 8. Verify dependency tree consistency
pip check
```

---

## 17. Limitations

1. **Closed-World Evaluation:** Benchmark evaluation is currently established on MONOT and ONOT datasets. Cross-dataset performance against commercial morphing tools (e.g., FaceMorpher, OpenCV landmark morphing) requires further validation.
2. **Resolution & Compression Sensitivity:** High-frequency gradient descriptors (HOG) show reduced sensitivity when evaluating heavily compressed JPEG files ($Q < 75$) or scanned documents without recalibration.
3. **No Reference Gallery Pairing:** MorphGuard operates in single-image (no-reference) mode; differential MAD (pairing with trusted eMRTD chip data) is not implemented.
4. **Not Certified for Production:** MorphGuard is an academic research platform and is not certified for operational ABC border deployment under ISO/IEC 19794-5.

---

## 18. Ethical & Biometric Privacy Considerations

- **Zero Biometric Exposure:** Facial images constitute special-category personal data under GDPR Art. 9. Raw datasets (`MONOT/`, `ONOT/`) and feature caches are strictly local and ignored by Git.
- **Defensive Research Intent:** MorphGuard is developed exclusively for defensive presentation attack detection to protect identity credentials.
- **Dual-Use Awareness:** Code or models must not be utilized for unauthorized biometric surveillance or fraudulent morph synthesis.

Full ethical guidelines are available in [docs/PRIVACY_AND_ETHICS.md](docs/PRIVACY_AND_ETHICS.md).

---

## 19. Licensing

- **Source Code:** The software implementation, UI, and scripts are licensed for academic research and educational evaluation.
- **Underlying Datasets (MONOT & ONOT):** Licensed under **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.
- **Model Checkpoints:** Model weights trained directly on representations derived from MONOT and ONOT represent derivative research artifacts and inherit **CC BY-NC 4.0 (Non-Commercial)** redistribution terms. Commercial exploitation is strictly prohibited without explicit authorization from the primary dataset copyright holders.

---

## 20. Citation & Acknowledgments

If you utilize MorphGuard in academic or industrial research, please cite:

```bibtex
@software{agarwal2026morphguard,
  author = {Agarwal, Aniket},
  title = {MorphGuard: Facial Morph Attack Detection and Biometric Image Analysis System},
  year = {2026},
  version = {3.2},
  url = {https://github.com/AniketAgarwal-aa/MorphGuard}
}
```

**Acknowledgments:**
- The creators and maintainers of the **MONOT** and **ONOT** biometric research databases.
- The open-source computer vision and scientific Python community (PyTorch, Scikit-learn, OpenCV, Streamlit).

---

## 21. Future Improvements

1. **Cross-Dataset Validation:** Evaluation on additional public MAD benchmarks (e.g., PMDB, MorGAN, FRLL-Morphs).
2. **Explainable AI (XAI):** Integration of Grad-CAM and Integrated Gradients heatmaps for deep models.
3. **Differential MAD Mode:** Dual-image differential analysis comparing live passport camera captures against eMRTD chip reference images.
4. **Adversarial Robustness:** Data augmentation for print-scan recapture transformations and heavy JPEG compression.
