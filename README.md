# MorphGuard — Facial Morphing Attack Detection & Biometric Analysis System

**MorphGuard** is a local, privacy-preserving research application designed for biometric facial morphing attack detection and exploratory image quality/texture analysis on the **MONOT and ONOT** biometric corpora. Raw datasets remain protected, local, and read-only.

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

Facial morphing attacks combine facial images of two distinct individuals into a single synthetic image capable of matching both contributing subjects in automated biometric face recognition systems (FRSs). Such attacks pose a severe vulnerability to electronic border gates (ABC gates) and passport issuance systems.

**MorphGuard's Objectives:**
1. **Explainable Feature Extraction:** Combine multi-scale texture descriptors (Local Binary Patterns, Gray-Level Co-Occurrence Matrix) and structural gradients (Histogram of Oriented Gradients) into an interpretable 6,103-dimensional vector representation.
2. **Scientific Data Governance:** Enforce strict provenance-based ground truth verification, preventing arbitrary dataset folder names or capture thresholds from being treated as binary class labels.
3. **Leakage-Safe Evaluation:** Prevent identity leakage across training, validation, and test sets using connected-component graph partitioning of contributing subject identities.
4. **Transparent Inference:** Distinguish experimental prototype predictions from certified forensic decisions, strictly returning `STATUS: MODEL UNAVAILABLE` when no validated model is loaded.

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

## 4. Feature Extraction & Scaled Cache

* **Active Feature Cache:** 2,400 images processed across 8 NumPy Compressed (`.npz`) shards in `data/cache/image_features/`.
* **Feature Schema (6,103 dimensions total, 100% finite float64):**
  * **LBP:** 10 dimensions ($P=8, R=1$, rotation-invariant uniform histogram capturing micro-texture blending).
  * **HOG:** 6,084 dimensions ($16 \times 16$ cell size, $2 \times 2$ block normalization, 9 gradient bins capturing facial structural geometry).
  * **GLCM:** 5 dimensions (Contrast, Dissimilarity, Homogeneity, Energy, Correlation measuring spatial correlation across horizontal and $45^\circ$ angles).
  * **Statistical Descriptors:** 4 dimensions (Mean intensity, Standard deviation, Shannon entropy, Canny edge density).
* **Processing Throughput:** Multithreaded execution (`ThreadPoolExecutor` with thread-local `FacePreprocessor`) achieving ~8.5 images/second on local CPU without system unresponsiveness.

---

## 5. Ground Truth Governance & Subject-Disjoint Splits

### Provenance-Verified Approved Labels (`data/manifests/reviewed_label_manifest.csv`)
Raw dataset folder names (e.g. `Gate_10`, `digital`) are acquisition conditions, not class labels. Provenance-based ground truth was established by cross-referencing generation logs (confirming dual-subject Delaunay morphing) and ICAO bona fide single-subject captures:

* **Total Approved Records:** **611 records**
  * **Morphed:** 380 records (all from MONOT Morphed)
  * **Genuine:** 231 records (225 from MONOT Gate_10/25, 6 from ONOT)

### Leakage-Safe Partitioning
Contributing subject IDs were grouped using connected-component graph partitioning to ensure **zero identity overlap** across data partitions:

| Split | Total Samples | Morphed | Genuine | Unique Subjects | Subject Overlap with Other Splits |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Train** | 365 | 224 | 141 | 76 | **0 (Zero)** |
| **Validation** | 165 | 120 | 45 | 25 | **0 (Zero)** |
| **Test** | 81 | 36 | 45 | 21 | **0 (Zero)** |

---

## 6. Model Architectures & Evaluation Results

All trained models were evaluated on the **81 unseen test samples** under ISO/IEC 30107-3 biometric presentation attack detection standards (tracked in `models/metadata/model_registry.json`):

| Model Name | Framework | Input Feature / Dimensions | Train Samples | Test Acc | APCER | BPCER | ACER | F1-Score | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`glcm_rf`** | scikit-learn | GLCM (5 dims) | 365 | **98.77%** | **0.00%** | **2.22%** | **0.0111** | **0.9863** | Trained & Evaluated |
| **`rf_combined`** | scikit-learn | Combined (6,103 dims) | 365 | **83.95%** | **36.11%** | **0.00%** | **0.1806** | **0.7797** | Trained & Evaluated |
| **`lbp_svm`** | scikit-learn | LBP (10 dims) | 365 | **75.31%** | **50.00%** | **4.44%** | **0.2722** | **0.6429** | Trained & Evaluated |
| **`combined_svm`** | scikit-learn | Combined (6,103 dims) | 365 | **58.02%** | **94.44%** | **0.00%** | **0.4722** | **0.1053** | Trained & Evaluated |
| **`hog_svm`** | scikit-learn | HOG (6,084 dims) | 365 | **58.02%** | **94.44%** | **0.00%** | **0.4722** | **0.1053** | Trained & Evaluated |
| **`custom_cnn`** | PyTorch | Raw Face Crop ($3 \times 224 \times 224$) | 365 | **56.79%** | **91.67%** | **4.44%** | **0.4806** | **0.1463** | Trained & Evaluated |
| **`resnet18`** | PyTorch | ResNet-18 ($3 \times 224 \times 224$) | — | — | — | — | — | — | Architecture Ready (Compute-gated) |
| **`efficientnet_b0`**| PyTorch | EfficientNet-B0 ($3 \times 224 \times 224$) | — | — | — | — | — | — | Architecture Ready (Compute-gated) |

*Metric Definitions (ISO/IEC 30107-3):*
* **APCER (Attack Presentation Classification Error Rate):** False Acceptance Rate of morph attacks.
* **BPCER (Bona Fide Presentation Classification Error Rate):** False Rejection Rate of genuine subjects.
* **ACER (Average Classification Error Rate):** $(\text{APCER} + \text{BPCER}) / 2$.

---

## 7. Application Structure (14 Pages)

The Streamlit interface (`app/main.py`) organizes 14 fully functional pages into two navigation sections:

### MAIN PROJECT
1. **Overview:** Executive summary, interactive pipeline diagram, key performance indicators.
2. **Face Analysis:** Single-image face detection, quality analysis, 6,103D feature breakdown, live experimental model selection, and two-image differential comparison with delta metrics and JSON exports.
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
   * All 380 approved morphed records originate exclusively from MONOT.
   * ONOT contributes only 6 approved genuine records and 0 morphed records.
   * Furthermore, all 6 ONOT genuine records reside in the training split; **0 ONOT records exist in the test split**.
   * Consequently, **no claims of cross-dataset generalization to ONOT can be made**. The test results reflect performance on unseen MONOT subjects only.
2. **Prototype Status:**
   * MorphGuard is an academic research prototype. Predictions produced by experimental models are not certified biometric decisions under ISO/IEC 30107-3 production standards.
3. **Cache Coverage:**
   * 2,400 images are cached and validated; 44,392 images remain in the raw image backlog to preserve local CPU stability.

---

## 9. License

Code is distributed under the MIT License. MONOT and ONOT datasets remain subject to their respective institutional research agreements.
