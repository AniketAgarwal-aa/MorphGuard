# MorphGuard V3.0 — Biometric Model Card

## 1. Model Details
- **Model Name:** MorphGuard Facial Morph Attack Detection (MAD) Suite
- **Version:** 3.0.0 (Release: 2026-11)
- **Repository:** [https://github.com/AniketAgarwal-aa/MorphGuard](https://github.com/AniketAgarwal-aa/MorphGuard)
- **Model Storage:** Hugging Face Hub (`AniketAgarwal-aa/MorphGuard-Models`)
- **Evaluation Standard:** ISO/IEC 30107-3 (Biometric Presentation Attack Detection)
- **License:** Apache 2.0 (Research and Academic Evaluation)

---

## 2. Intended Use & Boundaries
- **Intended Use:** Academic and research evaluation of facial morphing attack detection across classical texture descriptors (LBP, HOG, GLCM), tree ensembles, and deep neural networks.
- **Out of Scope / Prohibited Use:** Production biometric border-control gates, automated law enforcement surveillance, or high-stakes authentication without secondary human supervisor review.
- **Biometric Target:** Single-image (no-reference / differential-free) facial morph detection from standard passport-style portrait captures.

---

## 3. Data & Subject-Disjoint Partitioning
- **Training Corpora:** MONOT (Gate_10 bona fide, Gate_25 semi-controlled, Delaunay morphed) and ONOT (digital ICAO and print-scanned recaptured). Total processed biometric image inventory: **46,792 images**.
- **Audit-Approved Ground Truth Manifest (`data/manifests/reviewed_label_manifest.csv`):** 1,197 vetted records.
  - **Train partition:** 591 samples (408 morphed, 183 genuine across 101 subject clusters).
  - **Validation partition:** 321 samples (264 morphed, 57 genuine across 52 subject clusters).
  - **Test partition (Held-out):** 285 samples (228 morphed, 57 genuine across 42 subject clusters).
- **Leakage Prevention:** Graph connected-component partitioning ensures **strictly zero subject identity overlap** between training, validation, and test splits.

---

## 4. Multi-Model Benchmark (Held-out Test Partition: 285 Unseen Samples)

Decision thresholds ($\tau^*$) were calibrated strictly on the independent **validation partition** by minimizing ACER:
$$\text{ACER} = \frac{\text{APCER} + \text{BPCER}}{2}$$

| Model Identifier | Architecture | Feature Vector | Calibrated Threshold ($\tau^*$) | Accuracy | ACER | APCER | BPCER | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`combined_svm`** | Support Vector Machine (RBF) | Multi-scale texture + stats (6,103D) | 0.0051 | **96.49%** | **0.0680** | 0.0132 | 0.1228 | **0.9878** | **0.9967** |
| **`logistic_regression`** | L2-Penalized Logistic Regression | Multi-scale texture + stats (6,103D) | 0.0016 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9769** | **0.9912** |
| **`hog_svm`** | Linear SVM on HOG | Histogram of Oriented Gradients (6,084D) | 0.0040 | **96.14%** | **0.0899** | 0.0044 | 0.1754 | **0.9867** | **0.9964** |
| **`hist_gradient_boosting`** | Histogram Gradient Boosting | Multi-scale texture + stats (6,103D) | 0.0006 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9911** | **0.9971** |
| **`extra_trees`** | Extremely Randomized Trees | Multi-scale texture + stats (6,103D) | 0.2526 | **95.44%** | **0.1140** | 0.0000 | 0.2281 | **0.9950** | **0.9987** |
| **`rf_combined`** | Random Forest Classifier | Multi-scale texture + stats (6,103D) | 0.2670 | **95.09%** | **0.1228** | 0.0000 | 0.2456 | **0.9879** | **0.9965** |
| **`linear_svm`** | Linear Support Vector Machine | Multi-scale texture + stats (6,103D) | 0.0010 | **95.09%** | **0.1162** | 0.0044 | 0.2281 | **0.9675** | **0.9854** |
| **`voting_ensemble`** | Soft Voting Ensemble | Multi-model probability fusion | 0.1631 | **89.12%** | **0.1535** | 0.0789 | 0.2281 | 0.8688 | 0.9364 |
| **`stacking_ensemble`** | Stacking Classifier (Logistic Meta) | Multi-model base predictions | 0.4435 | **88.07%** | **0.1338** | 0.1096 | 0.1579 | **0.9044** | **0.9598** |
| **`custom_cnn`** | PyTorch 4-Stage ConvNet | Preprocessed 224×224 RGB Face Crop | 0.5000 | **87.72%** | **0.1096** | 0.1316 | 0.0877 | **0.9601** | — |
| **`lbp_svm`** | SVM on Uniform LBP | Local Binary Patterns (10D) | 0.0917 | **82.46%** | **0.2083** | 0.1535 | 0.2632 | 0.8503 | 0.9218 |
| **`lda`** | Linear Discriminant Analysis | Gray-Level Co-occurrence (5D) | 0.5580 | **76.49%** | **0.1996** | 0.2588 | 0.1404 | 0.8690 | 0.9304 |

---

## 5. Artifact Verification & Integrity Hashes
All published model checkpoints are checksummed using SHA-256:

| Artifact File | Subfolder | Size | SHA-256 Hash |
| :--- | :--- | :---: | :--- |
| `combined_svm.joblib` | `classical/` | 10.95 MB | `edcdbb4bfe60077521b98bae792372f121d41f7abcbba40ac1d2b84089ea7a84` |
| `logistic_regression.joblib` | `classical/` | 192 KB | `04d60232490d16be96d66e77e20ec4e1fce203bca042735749f7ba37a1104eec` |
| `hog_svm.joblib` | `classical/` | 10.96 MB | `ee95a9d8c368dff84b5c77e682057a6270b2ae4c1ef1a1dbcb515d9ccfca5394` |
| `hist_gradient_boosting.joblib` | `classical/` | 12.29 MB | `16cb15f7ebaa563b72350ef91642875b1dc8d7caadad64c92ee0fc3dd3383a4d` |
| `extra_trees.joblib` | `classical/` | 1.10 MB | `9842a2ddc1955d911b3bebb3fa2d515a45b854d9c3ce348a096bb7eb9512d93e` |
| `rf_combined.joblib` | `classical/` | 504 KB | `0ae8a6b16e87fca0dd4ea42c4b0ea4cf422c54cfda51c4a0e980386cfb8e2354` |
| `linear_svm.joblib` | `classical/` | 5.68 MB | `f044bb71d794cb5c8a49aeef8fa03487c67c527e0251787d5a57cb8c0c99a071` |
| `custom_cnn.pt` | `deep_learning/`| 236 KB | `6c10eb3ae8802928373b75fcf54751eaee155b9a896d93eef0be2b2b1eb3e9db` |
| `voting_ensemble.joblib` | `ensembles/` | 348 KB | `829e1604a5525540bf9c4f4a1329c31405b6a7ee7b095cb6ba1b7a2d04a6007e` |
| `stacking_ensemble.joblib` | `ensembles/` | 396 KB | `031a029eebe0fc925f4886aa60fae54fe9738b6d859ec1e9c20a4413158c8ecb` |

---

## 6. Ethical Considerations & Biometric Limitations
- **Morphing Algorithm Dependency:** Evaluated models are sensitive to the specific morphing generator used in MONOT (Delaunay triangulation mesh morphing). Generalization to generative diffusion morphs or GAN-based morphs (StyleGAN, MIPGAN) requires domain-specific fine-tuning.
- **Demographic Distribution:** Training samples originate from the MONOT research dataset, which exhibits demographic skews typical of early biometric benchmark corpora.
- **Non-Certification:** MorphGuard is an academic experimental platform, not an operational biometric component certified under ISO/IEC 19794-5 or ISO/IEC 30107-3.
