# MorphGuard V3.2 — Biometric Model Card

## 1. Model Details
- **Model Name:** MorphGuard Facial Morph Attack Detection (MAD) Suite
- **Version:** 3.2.0 (Release: 2026-11)
- **Repository:** [https://github.com/AniketAgarwal-aa/MorphGuard](https://github.com/AniketAgarwal-aa/MorphGuard)
- **Model Storage:** Hugging Face Hub (`AniketAgarwal-aa/MorphGuard-Models`)
- **Evaluation Standard:** ISO/IEC 30107-3 (Biometric Presentation Attack Detection)
- **License:** Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

---

## 2. Intended Use & Boundaries
- **Intended Use:** Academic research, security analysis, and comparative benchmarking of facial morph attack detection algorithms across classical handcrafted texture descriptors (LBP, HOG, GLCM) and deep convolutional architectures.
- **Out of Scope / Prohibited Use:** Production biometric border-control gates, automated criminal justice decisions, or unmonitored commercial access control without secondary human adjudication.
- **Biometric Target:** Single-image (no-reference / differential-free) facial morph detection from standard passport-style portrait captures.

---

## 3. Data & Subject-Disjoint Partitioning
- **Training Corpora:** MONOT (Gate_10 bona fide, Gate_25 semi-controlled, Delaunay morphed) and ONOT (digital ICAO and print-scanned recaptured). Total processed biometric image inventory: **46,792 images** (3.39 GB feature cache).
- **Audit-Approved Ground Truth Manifest (`data/manifests/reviewed_label_manifest.csv`):** 1,197 vetted records.
  - **Train partition:** 591 samples (408 morphed, 183 genuine across 101 subject clusters).
  - **Validation partition:** 321 samples (223 morphed, 98 genuine across 52 subject clusters).
  - **Test partition (Held-out):** 285 samples (228 morphed, 57 genuine across 42 subject clusters).
- **Leakage Prevention:** Graph connected-component partitioning ensures **strictly zero subject identity overlap** between training, validation, and test splits ($0$ train-val, $0$ train-test, $0$ val-test overlap).
- **Unlabelled Reserve Pool:** 45,595 images withheld from training to preserve strict scientific provenance.

---

## 4. Multi-Model Benchmark (Held-out Test Partition: 285 Unseen Samples)

Decision thresholds ($\tau^*$) were calibrated strictly on the independent **validation partition** by minimizing ACER:
$$\text{ACER} = \frac{\text{APCER} + \text{BPCER}}{2}$$

| Model Identifier | Architecture / Family | Input Dimensions | Threshold ($\tau^*$) | Test Accuracy | ACER | APCER | BPCER | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`combined_svm`** | Support Vector Machine (RBF) | 6,103D Texture+Stats | 0.005100 | **96.49%** | **0.0680** | 0.0132 | 0.1228 | **0.9878** | **0.9967** |
| **`hog_svm`** | Linear SVM on HOG | 6,084D Gradient HOG | 0.004000 | **96.14%** | **0.0899** | 0.0044 | 0.1754 | **0.9867** | **0.9964** |
| **`logistic_regression`** | L2 Logistic Regression | 6,103D Texture+Stats | 0.001600 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9769** | **0.9912** |
| **`hist_gradient_boosting`** | Histogram Gradient Boosting | 6,103D Texture+Stats | 0.000600 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9911** | **0.9971** |
| **`extra_trees`** | Extremely Randomized Trees | 6,103D Texture+Stats | 0.252600 | **95.44%** | **0.1140** | 0.0000 | 0.2281 | **0.9950** | **0.9987** |
| **`rf_combined`** | Random Forest Classifier | 6,103D Texture+Stats | 0.267000 | **95.09%** | **0.1228** | 0.0000 | 0.2456 | **0.9879** | **0.9965** |
| **`linear_svm`** | Linear Support Vector Machine | 6,103D Texture+Stats | 0.001000 | **95.09%** | **0.1162** | 0.0044 | 0.2281 | **0.9675** | **0.9854** |
| **`efficientnet_b0`** | EfficientNet-B0 (PyTorch CNN) | $(3 \times 224 \times 224)$ | 0.003194 | **91.58%** | **0.0987** | 0.0746 | 0.1228 | **0.9631** | **0.9884** |
| **`voting_ensemble`** | Soft Probability Fusion | GLCM (5D) | 0.163100 | **89.12%** | **0.1535** | 0.0789 | 0.2281 | 0.8688 | 0.9364 |
| **`stacking_ensemble`** | Stacking Ensemble (Logistic Meta) | GLCM (5D) | 0.443500 | **88.07%** | **0.1338** | 0.1096 | 0.1579 | 0.9044 | 0.9598 |
| **`custom_cnn`** | PyTorch 3-Stage ConvNet | $(3 \times 224 \times 224)$ | 0.500000 | **87.72%** | **0.1096** | 0.1316 | 0.0877 | 0.9601 | — |
| **`lbp_svm`** | SVM on Uniform LBP | LBP (10D) | 0.091700 | **82.46%** | **0.2083** | 0.1535 | 0.2632 | 0.8503 | 0.9218 |
| **`mobilenet_v3_small`** | MobileNetV3-Small (PyTorch) | $(3 \times 224 \times 224)$ | 0.931847 | **80.00%** | **0.5000** | 0.0000 | 1.0000 | 0.1632 | 0.7277 |
| **`lda`** | Linear Discriminant Analysis | GLCM (5D) | 0.558000 | **76.49%** | **0.1996** | 0.2588 | 0.1404 | 0.8690 | 0.9304 |
| **`resnet18`** | ResNet-18 (PyTorch CNN) | $(3 \times 224 \times 224)$ | 0.000007 | **71.23%** | **0.3180** | 0.2675 | 0.3684 | 0.8121 | 0.9414 |
| **`densenet121`** | DenseNet-121 (PyTorch CNN) | $(3 \times 224 \times 224)$ | 0.005979 | **63.86%** | **0.2917** | 0.4079 | 0.1754 | 0.8089 | 0.9461 |
| **`resnet34`** | ResNet-34 (PyTorch CNN) | $(3 \times 224 \times 224)$ | 0.311335 | **62.11%** | **0.2434** | 0.4693 | 0.0175 | 0.8841 | 0.9680 |
| **`gaussian_nb`** | Gaussian Naive Bayes | GLCM (5D) | 0.371200 | **60.35%** | **0.3004** | 0.4605 | 0.1404 | 0.8560 | 0.9068 |
| **`glcm_rf`** | Random Forest on GLCM | GLCM (5D) | 0.419600 | **52.98%** | **0.3202** | 0.5702 | 0.0702 | 0.9058 | 0.9644 |
| **`resnet50`** | ResNet-50 (PyTorch CNN) | $(3 \times 224 \times 224)$ | 0.000703 | **48.77%** | **0.3596** | 0.6140 | 0.1053 | 0.8045 | 0.9378 |
| **`knn`** | K-Nearest Neighbors | GLCM (5D) | 0.592100 | **37.54%** | **0.4167** | 0.7632 | 0.0702 | 0.6682 | 0.8942 |

---

## 5. Artifact Integrity Hashes (SHA-256)
All 21 model checkpoints are verified and checksummed:

| Artifact File | Subfolder | Size (MB) | SHA-256 Checksum |
| :--- | :--- | :---: | :--- |
| `combined_svm.joblib` | `classical/` | 10.95 | `edcdbb4bfe60077521b98bae792372f121d41f7abcbba40ac1d2b84089ea7a84` |
| `custom_cnn.pt` | `deep_learning/` | 0.23 | `f141d2b38e94965fc2327781f9782365ce4613a5968cedf946fc6197f055d565` |
| `densenet121.pt` | `deep_learning/` | 27.10 | `9169572094dcad77ae1a6d71b3e52f55964d4b17e4526dfeb5ec35402ec9ffc9` |
| `efficientnet_b0.pt` | `deep_learning/` | 15.58 | `ef6d7e5a4dfbbd61a0eb79a1fc50a4d94964fe9fe2118d7f41fdac35de9a799e` |
| `extra_trees.joblib` | `classical/` | 1.10 | `6ea40abb5be708170c793ba6f7e44a7f9b88d363b9fca5665890fa2d057193b2` |
| `gaussian_nb.joblib` | `classical/` | 0.01 | `b26ce942d6c11364ff0e28f307d853e3fa52a36aa9d2a2a09c258d4a9cf29fa0` |
| `glcm_rf.joblib` | `classical/` | 0.73 | `9e877b1f8aacefea5d0505b22572a15cbe9395ee13c19ae97815bf5e5c709795` |
| `hist_gradient_boosting.joblib` | `classical/` | 12.29 | `9d7558d62dadc1eb7c452e69cae62fc0b47e3a39e31ff55b7a14e9f3b145803d` |
| `hog_svm.joblib` | `classical/` | 10.96 | `5b1608dc820cd93c22ad64311028712a32eb2479e0a0584b4249a5b3ee0b8523` |
| `knn.joblib` | `classical/` | 0.05 | `27b743888d758dd8b9ddfcfd6b8ef9810bb8e9b62635952d9a6ca2a91e5ee189` |
| `lbp_svm.joblib` | `classical/` | 0.02 | `c03852ef48922c77d9c66a4f216503f192b1da791e809dc390979147fa0e3c03` |
| `lda.joblib` | `classical/` | 0.01 | `dd44eb2d0466a0e1cb3ec1767c9c0dc11e2f75dafa12128b9c475ca24888be62` |
| `linear_svm.joblib` | `classical/` | 5.68 | `7d4718f3f2b7af27670731df40019688bc83f3ba9e685f09459a9bf954ffebbb` |
| `logistic_regression.joblib` | `classical/` | 0.19 | `e3dc99ae4b75e20be4cb89d53c3937cf5da1823eb46b412bf8fa958742ca7b9a` |
| `mobilenet_v3_small.pt` | `deep_learning/` | 5.92 | `30ef3bf8670c0eb245dabfa55dd08aa07a90977349d951c7a5785ad8c97a2a22` |
| `resnet18.pt` | `deep_learning/` | 42.71 | `4887d7e6dbd0826bf16505c685d08f1f88442c5874d65d06863199df45ebb8db` |
| `resnet34.pt` | `deep_learning/` | 81.33 | `fdbc80dc8ee75ac022a105c30fe70bfca752670e30da0fca327db0a02fdb634a` |
| `resnet50.pt` | `deep_learning/` | 89.99 | `f8927bc503efbc0a73da3b4be2ee15eb712ca7e07669d675681ce2658fe84606` |
| `rf_combined.joblib` | `classical/` | 0.49 | `17408ba87482145719ef16eb307d8b584a3aa5837ff449ae22ca8cb6440ecaa7` |
| `stacking_ensemble.joblib` | `ensembles/` | 0.39 | `fc926697ed5cde9a6136d8085df5d5180f98e29a99fc6d289aa81232822a1e7b` |
| `voting_ensemble.joblib` | `ensembles/` | 0.34 | `5ff29f33953d729e24823ce973273e86c757c3d7ea349a51833e21855e9baea9` |

---

## 6. Ethical Considerations & Biometric Limitations
- **Morph Generation Dependency:** Evaluated models were trained primarily on Delaunay mesh morph attacks from MONOT. Performance on modern generative diffusion models (e.g. DiffMorph) or GAN-based morphs must be evaluated empirically before drawing operational conclusions.
- **Biometric Privacy:** No raw biometric images or identity templates are published with this model card.
- **Non-Commercial Research License:** Under CC BY-NC 4.0, these model weights are available solely for non-commercial research, academic replication, and educational demonstration.
