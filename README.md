# MorphGuard V2 — Complete Full-Scale Biometric Morph Detection System

**MorphGuard V2** is a local, privacy-preserving research platform for biometric facial morphing attack detection, multi-model ensemble evaluation, and exploratory texture/gradient analysis on the **MONOT and ONOT** biometric corpora. Raw biometric datasets remain protected, local, and read-only.

Authoritative Project Acceptance Report: [FINAL_REPORT.md](FINAL_REPORT.md)  
Demonstration Guide: [DEMONSTRATION_GUIDE.md](DEMONSTRATION_GUIDE.md)  
Architecture Blueprint: [ARCHITECTURE.md](ARCHITECTURE.md)  

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
.\.venv\Scripts\python.exe scripts/verify_model_artifacts.py
.\.venv\Scripts\python.exe scripts/test_all_pages.py
```

---

## 2. Research Problem & Objectives

Facial morphing attacks blend portrait images of two distinct individuals into a single synthetic image capable of matching both contributing subjects in automated biometric face recognition systems (FRSs). Such attacks pose a severe vulnerability to electronic border control gates (ABC gates) and passport issuance infrastructure.

**MorphGuard V2 Objectives:**
1. **Explainable Feature Extraction:** Combine multi-scale texture descriptors (Local Binary Patterns, Gray-Level Co-Occurrence Matrix) and structural gradients (Histogram of Oriented Gradients) into an interpretable 6,103-dimensional vector representation.
2. **Scientific Data Governance:** Enforce strict provenance-based ground truth verification, preventing arbitrary dataset folder names or capture thresholds from being treated as binary class labels.
3. **Leakage-Safe Evaluation:** Prevent identity leakage across training, validation, and test sets using connected-component graph partitioning of contributing subject identities.
4. **Transparent Multi-Model Inference:** Deploy and evaluate classical ML algorithms, voting and stacking ensembles, and deep convolutional neural networks with calibrated decision thresholds and honest `MODEL UNAVAILABLE` safeguards.

---

## 3. Dataset Specifications & Inventory

A complete recursive audit confirmed **46,792 raw biometric images** across five strata:

* **MONOT (24,140 images, ~18.7 GB):**
  * `Gate_10`: 2,550 images (ICAO-compliant biometric acquisition, threshold $T=10$)
  * `Gate_25`: 6,350 images (relaxed threshold $T=25$)
  * `Morphed`: 15,240 images (automated landmark Delaunay facial morphing pairs)
* **ONOT (22,652 images, ~6.7 GB):**
  * `digital`: 11,326 images (uncompressed digital capture)
  * `print-scan`: 11,326 images (physical passport prints recaptured via flatbed scanner)

*Integrity Audit:* 0 corrupted images, 0 zero-byte files, 0 duplicate SHA-256 hashes. Total raw storage footprint: ~25.6 GB.

---

## 4. Scaled Feature Cache (5,000 Images)

* **Active Feature Cache:** 5,000 images processed across 14 NumPy Compressed (`.npz`) shards in `data/cache/image_features/`.
* **Feature Schema (6,103 dimensions total, 100% finite float64):**
  * **LBP:** 10 dimensions ($P=8, R=1$, rotation-invariant uniform histogram capturing micro-texture blending).
  * **HOG:** 6,084 dimensions ($16 \times 16$ cell size, $2 \times 2$ block normalization, 9 gradient bins capturing facial structural geometry).
  * **GLCM:** 5 dimensions (Contrast, Dissimilarity, Homogeneity, Energy, Correlation measuring spatial correlation across horizontal and $45^\circ$ angles).
  * **Statistical Descriptors:** 4 dimensions (Mean intensity, Standard deviation, Shannon entropy, Canny edge density).
* **Strata Distribution:** Gate_10 (1,400), Gate_25 (900), Morphed (900), digital (900), print-scan (900).

---

## 5. Ground Truth Governance & Subject-Disjoint Splits (1,197 Records)

### Provenance-Verified Approved Labels (`data/manifests/reviewed_label_manifest.csv`)
Raw dataset folder names are acquisition conditions, not class labels. Provenance-based ground truth was established by cross-referencing generation logs (confirming dual-subject Delaunay morphing) and ICAO bona fide single-subject captures:

* **Total Approved Records:** **1,197 records**
  * **Morphed:** 900 records (provenance-verified Delaunay morphing)
  * **Genuine:** 297 records (ICAO single-subject bona fide captures)

### Leakage-Safe Partitioning
Contributing subject IDs were grouped using connected-component graph partitioning to ensure **zero identity overlap** across data partitions:

| Split | Total Samples | Morphed | Genuine | Unique Subjects | Subject Overlap with Other Splits |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Train** | 591 | 408 | 183 | 101 | **0 (Zero)** |
| **Validation** | 321 | 264 | 57 | 52 | **0 (Zero)** |
| **Test** | 285 | 228 | 57 | 42 | **0 (Zero)** |

---

## 6. Model Architectures & Evaluation Results (21 Models in Registry)

All trained models were evaluated on the **285 unseen test samples** under ISO/IEC 30107-3 biometric presentation attack detection standards (tracked in `models/metadata/model_registry.json`):

| Model Architecture | Framework | Input Feature / Dimensions | Test Acc | APCER | BPCER | ACER | F1-Score | ROC-AUC | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`custom_cnn`** | PyTorch | Raw Face Crop ($3 \times 224 \times 224$) | **87.72%** | **13.16%** | **8.77%** | **0.1096** | **0.9195** | — | Trained & Evaluated |
| **`lda`** | scikit-learn | GLCM (5 dims) | **80.70%** | **20.18%** | **15.79%** | **0.1798** | **0.8687** | **0.8690** | Trained & Evaluated |
| **`stacking_ensemble`**| scikit-learn | GLCM (Meta-learner) | **80.00%** | **21.93%** | **12.28%** | **0.1711** | **0.8620** | **0.9044** | Trained & Evaluated |
| **`voting_ensemble`** | scikit-learn | GLCM (Soft-voting) | **57.54%** | **50.00%** | **12.28%** | **0.3114** | **0.6533** | **0.8688** | Trained & Evaluated |
| **`rf_combined`** | scikit-learn | Combined (6,103 dims) | **56.49%** | **54.39%** | **0.00%** | **0.2719** | **0.6265** | **0.9879** | Trained & Evaluated |
| **`lbp_svm`** | scikit-learn | LBP (10 dims) | **54.74%** | **53.95%** | **10.53%** | **0.3224** | **0.6195** | **0.8503** | Trained & Evaluated |
| **`gaussian_nb`** | scikit-learn | GLCM (5 dims) | **52.28%** | **56.14%** | **14.04%** | **0.3509** | **0.5952** | **0.8560** | Trained & Evaluated |
| **`extra_trees`** | scikit-learn | Combined (6,103 dims) | **51.93%** | **60.09%** | **0.00%** | **0.3004** | **0.5705** | **0.9950** | Trained & Evaluated |
| **`glcm_rf`** | scikit-learn | GLCM (5 dims) | **51.58%** | **58.77%** | **7.02%** | **0.3289** | **0.5767** | **0.9058** | Trained & Evaluated |
| **`hist_gradient_boosting`**| scikit-learn| Combined (6,103 dims) | **51.58%** | **60.53%** | **0.00%** | **0.3026** | **0.5660** | **0.9911** | Trained & Evaluated |
| **`knn`** | scikit-learn | GLCM (5 dims) | **43.51%** | **67.54%** | **12.28%** | **0.3991** | **0.4790** | **0.6682** | Trained & Evaluated |
| **`linear_svm`** | scikit-learn | Combined (6,103 dims) | **25.96%** | **92.54%** | **0.00%** | **0.4627** | **0.1388** | **0.9675** | Trained & Evaluated |
| **`logistic_regression`**| scikit-learn | Combined (6,103 dims) | **25.26%** | **93.42%** | **0.00%** | **0.4671** | **0.1235** | **0.9769** | Trained & Evaluated |
| **`combined_svm`** | scikit-learn | Combined (6,103 dims) | **23.51%** | **95.61%** | **0.00%** | **0.4781** | **0.0840** | **0.9878** | Trained & Evaluated |
| **`hog_svm`** | scikit-learn | HOG (6,084 dims) | **23.51%** | **95.61%** | **0.00%** | **0.4781** | **0.0840** | **0.9867** | Trained & Evaluated |
| **`resnet18`** | PyTorch | Face Crop ($3 \times 224 \times 224$) | — | — | — | — | — | — | Ready for Training (Compute-gated) |
| **`efficientnet_b0`**| PyTorch | Face Crop ($3 \times 224 \times 224$) | — | — | — | — | — | — | Ready for Training (Compute-gated) |
| **`mobilenet_v3_small`**| PyTorch | Face Crop ($3 \times 224 \times 224$) | — | — | — | — | — | — | Ready for Training (Compute-gated) |
| **`densenet121`** | PyTorch | Face Crop ($3 \times 224 \times 224$) | — | — | — | — | — | — | Ready for Training (Compute-gated) |
| **`resnet34`** | PyTorch | Face Crop ($3 \times 224 \times 224$) | — | — | — | — | — | — | Ready for Training (Compute-gated) |
| **`resnet50`** | PyTorch | Face Crop ($3 \times 224 \times 224$) | — | — | — | — | — | — | Ready for Training (Compute-gated) |

*Metric Definitions (ISO/IEC 30107-3):*
* **APCER (Attack Presentation Classification Error Rate):** False Acceptance Rate of morph attacks.
* **BPCER (Bona Fide Presentation Classification Error Rate):** False Rejection Rate of genuine subjects.
* **ACER (Average Classification Error Rate):** $(\text{APCER} + \text{BPCER}) / 2$.

---

## 7. Application Structure (14 Pages)

The Streamlit interface (`app/main.py`) organizes 14 fully functional pages into two navigation sections:

### MAIN PROJECT
1. **Overview:** Executive summary, interactive pipeline diagram, key performance indicators.
2. **Face Analysis:** Single-image face detection, quality analysis, 6,103D feature breakdown, live experimental model selection across all trained models, and two-image differential comparison with delta metrics and JSON exports.
3. **Dataset Explorer:** Dynamic cache coverage progress bar, category filters, and CSV export.
4. **Annotation Review:** Human-in-the-loop review workspace with provenance audit logs and immutable records.
5. **Model Comparison:** Live model registry displaying real training durations, ISO/IEC 30107-3 metrics, and architecture specifications.
6. **Model Insights:** 2D PCA projection of cached feature space, variance decomposition, and distribution plots.
7. **Experiments:** Comprehensive experiment logs, test metrics, and cache shard statistics.

### ABOUT PROJECT
8. **About MorphGuard:** Problem statement, attack mechanics, project boundaries.
9. **How It Works:** Step-by-step pipeline walkthrough (OpenCV Haar $\to$ Texture extraction $\to$ Model inference).
10. **Datasets:** In-depth breakdown of MONOT and ONOT datasets.
11. **Models & Technology:** Architecture specifications and library dependency matrix.
12. **Methodology:** Identity-leakage prevention protocol and evaluation standards.
13. **Limitations & Privacy:** Honest boundary documentation and privacy protections.
14. **Technical Documentation:** Module hierarchy map and configuration guides.

---

## 8. Critical Scientific Limitations

1. **Source Imbalance & Confounding:**
   * All approved morphed records originate exclusively from MONOT Delaunay morphing.
   * ONOT contributes bona fide acquisition variants (digital and print-scan) but lacks verified morph-generation provenance logs.
   * Consequently, **no claims of cross-dataset generalization to ONOT can be made**. The test results reflect performance on unseen MONOT subjects only.
2. **Prototype Status:**
   * MorphGuard V2 is an academic research platform. Predictions produced by experimental models are not certified biometric decisions under ISO/IEC 30107-3 production standards.

---

## 9. License

Code is distributed under the MIT License. MONOT and ONOT datasets remain subject to their respective institutional research agreements.
