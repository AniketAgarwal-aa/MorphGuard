# MorphGuard Architecture & System Design

**Version:** 3.2  
**Date:** November 2026  
**Status:** Release-Ready  

---

## 1. High-Level Architectural Overview

MorphGuard is designed as a decoupled, multi-tier biometric software system specializing in facial morph attack detection (MAD). The system cleanly separates the scientific detection core from the presentation and serving layers:

```
+-------------------------------------------------------------------------------+
|                       Streamlit User Interface (app/)                         |
|  - 6 Functional Navigation Groups                                             |
|  - 14 Modular Pages (Analysis, Comparison, Explorer, Explainability, etc.)    |
|  - Modern Dark / Light UI with Material 3 Design Tokens                       |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                      Inference & Serving Layer (src/)                         |
|  - InferenceService (Single-image & Dual-image pipeline)                      |
|  - Multi-Tier Hosted Model Loader (Local disk -> Hugging Face Hub cache)      |
|  - Strict Binary Decision Engine (P >= tau* => MORPHED)                       |
|  - Defensive Error Handling (No silent fallback, explicit status codes)       |
+-------------------------------------------------------------------------------+
        |                                                   |
        v                                                   v
+-------------------------------+   +-------------------------------------------+
| Preprocessing & Features      |   | Model Execution Layer                     |
|  - Haar Cascade Face Detector |   |  - 14 Scikit-learn Classifiers            |
|  - Landmark Alignment & Crop  |   |  - 7 PyTorch Deep Neural Networks         |
|  - Blur / Contrast Quality    |   |  - Synchronized Model Registry            |
|  - HOG (6084D) / LBP (10D)    |   |  - Validation-Calibrated Decision Thresh. |
|  - GLCM (5D) / Combined 6103D |   +-------------------------------------------+
+-------------------------------+
        |
        v
+-------------------------------------------------------------------------------+
|                      Biometric Corpora & Storage Layer                        |
|  - MONOT (24,140 images) & ONOT (22,652 images) -> Total 46,792 cached        |
|  - Approved Manifest (1,197 records, 0 identity leakage between splits)       |
|  - Unlabelled Research Reserve (45,595 cached records)                        |
|  - Defended by .gitignore (Zero biometric assets in version control)          |
+-------------------------------------------------------------------------------+
```

---

## 2. Component Structure

### 2.1 Presentation Layer (`app/`)
- `app/main.py`: Entrypoint and sidebar controller organizing the 14 views into 6 ergonomic groups:
  1. **Detection & Verification:** Single-Image Analysis (`1_Face_Morph_Analysis.py`), Overview Dashboard (`overview.py`).
  2. **Biometric Data & Provenance:** Dataset Explorer (`4_Dataset_Explorer.py`), Annotation Review Workbench (`annotation_review.py`), Dataset Specs (`datasets.py`).
  3. **Benchmarking & Evaluation:** Model Comparison (`2_Model_Comparison.py`), Research Experiments (`5_Research_Experiments.py`), Model Architecture Deep-Dive (`models_technology.py`).
  4. **Interpretability & Explainability:** Feature Space Explorer (`3_Explainability.py`).
  5. **Documentation & Scientific Standards:** Methodology (`6_Methodology.py`), Technical Documentation (`technical_documentation.py`), How It Works (`how_it_works.py`).
  6. **Governance & Limitations:** Limitations & Disclaimers (`7_Limitations_And_Info.py`), About (`about.py`).
- `app/components/ui.py`: Centralized UI primitives, responsive metric cards, badges, and synchronized theme CSS.

### 2.2 Core Scientific Library (`src/morphguard/`)
- `morphguard/preprocessing/`: Image validation, color-space conversion, face detection via Haar Cascade, bounding box expansion, and facial quality evaluation (Laplacian variance, Michelson contrast).
- `morphguard/feature_extraction/`: Deterministic mathematical extractors:
  - Histogram of Oriented Gradients (HOG): 6,084 dimensions.
  - Local Binary Patterns (LBP): 10 dimensions (uniform pattern histogram).
  - Gray-Level Co-occurrence Matrix (GLCM): 5 dimensions (contrast, dissimilarity, homogeneity, energy, correlation).
  - Combined Feature Vector: 6,103 dimensions.
- `morphguard/inference/service.py`: `InferenceService` managing end-to-end execution, image validation, face detection, feature extraction, score generation, threshold comparison, and structured response packaging.
- `morphguard/inference/hosted_models.py`: Robust model loader supporting local filesystem weights, Hugging Face Hub authenticated/public download caching, and dynamic framework routing (Scikit-learn vs. PyTorch).
- `morphguard/evaluation/metrics.py`: Implementation of ISO/IEC 30107-3 compliant metrics (APCER, BPCER, ACER), ROC curves, and PR curves.

### 2.3 Model Registry & Metadata (`models/metadata/`)
- `model_registry.json`: Authoritative catalog mapping all 21 models to their feature requirements, framework, calibrated thresholds ($\tau^*$), training status, and evaluation metrics.
- Individual JSON manifests for deep learning models detailing input dimensions, normalization constants, and architecture parameters.

---

## 3. Data Flow & Security Boundaries

1. **Input Ingestion:** User uploads image via web UI or API path. Image is read in-memory as a byte stream or decoded via OpenCV.
2. **Quality & Face Gate:** Image is evaluated for minimum dimensions and single face presence. If no face or invalid data is detected, pipeline terminates with an explicit technical error code (`FACE NOT DETECTED` or `INVALID IMAGE`).
3. **Feature Generation / Tensor Transformation:**
   - Classical Models: Crop is extracted, resized to standard dimension, and transformed into HOG, LBP, or GLCM vectors.
   - Deep Models: Crop is resized to $224 \times 224$, normalized via ImageNet statistics ($\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$), and passed through PyTorch inference.
4. **Decision Boundary:** Posterior probability $P(\text{morphed})$ is compared against the model's validation-tuned threshold $\tau^*$:
   $$\text{Decision} = \begin{cases} \text{MORPHED}, & \text{if } P \ge \tau^* \\ \text{GENUINE}, & \text{if } P < \tau^* \end{cases}$$
5. **Zero Data Retention:** Uploaded images and intermediate feature vectors are discarded immediately following request completion; no biometric image is written to persistent disk storage during inference.
