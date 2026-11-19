# MorphGuard V3.2 — Publication Rights & Licensing Audit

**Project:** MorphGuard — Facial Morph Attack Detection System  
**Audit Date:** November 19, 2026  
**Auditor:** MorphGuard Compliance & Engineering  
**Primary Dataset Terms:** Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)  

---

## 1. Executive Summary

This audit establishes the legal, ethical, and licensing boundaries governing the publication of MorphGuard artifacts across GitHub, Hugging Face Hub, and Streamlit Community Cloud. 

Because the underlying training corpora (**MONOT** and **ONOT**) are licensed under **CC BY-NC 4.0** and involve sensitive biometric facial representations of human subjects, strict partition-of-rights rules apply. Trained model parameters, feature caches, and raw images cannot be treated identically to the original application source code.

---

## 2. Granular 10-Category Publication Rights Matrix

| Category | Description | Primary Governing License / Law | Publication Permitted? | Required Conditions & Safeguards |
| :--- | :--- | :--- | :---: | :--- |
| **1. Original Source Code** | `src/morphguard/`, `app/`, `scripts/`, `tests/` | MIT License (Authorship) | **YES** | Publishable on GitHub under MIT. Retain copyright notice. |
| **2. Project Documentation** | Markdown reports, guides, methodology docs | MIT / CC BY 4.0 | **YES** | Publishable on GitHub and Hugging Face. Attribution required. |
| **3. Classical Model Weights** | Scikit-Learn `.joblib` files (SVM, RF, Ensembles) | CC BY-NC 4.0 (Derivative) | **CONDITIONAL** | Can only be published under **Non-Commercial** terms (CC BY-NC 4.0 or OpenRAIL). No commercial exploitation. |
| **4. Deep Learning Checkpoints** | PyTorch `.pt` files (`custom_cnn`, `resnet`, etc.) | CC BY-NC 4.0 (Derivative) | **CONDITIONAL** | Must inherit CC BY-NC 4.0 non-commercial restrictions. |
| **5. Pretrained Weights** | Torchvision initial backbones (ImageNet weights) | BSD 3-Clause (PyTorch) | **YES** | Covered by standard PyTorch/torchvision redistribution terms with non-commercial fine-tuning overlay. |
| **6. Original Dataset Images** | `MONOT/` and `ONOT/` raw image files | Biometric Data Privacy (GDPR/BIPA) + CC BY-NC | **STRICTLY NO** | **FORBIDDEN TO UPLOAD.** Biometric raw data must remain strictly on local authorized storage. |
| **7. Biometric Face Crops** | $(224 \times 224)$ normalized face crops | Biometric Privacy Regulations | **STRICTLY NO** | **FORBIDDEN TO UPLOAD.** Face crops reveal biometric identity templates. |
| **8. Extracted Feature Caches** | 6,103D NPZ shards (`data/cache/`) | Biometric Embeddings (GDPR Art. 9) | **STRICTLY NO** | **FORBIDDEN TO UPLOAD.** Feature vectors allow reconstruction or biometric matching. |
| **9. Evaluation Metadata** | `model_registry.json`, benchmark CSVs, ROC curves | Open Data Commons (ODC-By) | **YES** | Aggregated, non-identifying statistical performance metrics are fully publishable. |
| **10. Dependency Notices** | OpenCV, Scikit-learn, PyTorch, Streamlit licenses | Various (Apache 2.0, BSD, MIT) | **YES** | Bundled dependency notices in `docs/` and repository headers. |

---

## 3. Hugging Face Repository Legal Classification

### 3.1 License Incompatibility Finding
In early drafts, `scripts/upload_to_huggingface.py` applied an `apache-2.0` license tag to the Hugging Face repository metadata. This audit identifies a **license conflict**:
- Apache 2.0 permits unrestricted commercial exploitation.
- The training data (MONOT/ONOT) explicitly forbids commercial exploitation under **CC BY-NC 4.0**.
- **Action Required:** Change the Hugging Face Model Card license tag from `apache-2.0` to `cc-by-nc-4.0`.

### 3.2 Publication Authorization Recommendation
- **Current Status:** **BLOCKED BY LICENSING REVIEW**
- The repository `AniketAgarwal-aa/MorphGuard-Models` should remain **Private** during development.
- It may be set to **Public** only after:
  1. License tag is confirmed as `cc-by-nc-4.0`.
  2. The Hugging Face Model Card explicitly carries the Non-Commercial Research-Only disclaimer.
  3. User provides explicit authorization to publish the model weights under non-commercial research terms.

---

## 4. Biometric Privacy & Ethical Guardrails

1. **Informed Consent & Subject Anonymity:** MONOT and ONOT datasets contain human facial captures. No subject names or external identity mappings exist in the repository; subject tokens are randomized opaque identifiers (e.g. `S113923411`).
2. **Reverse Reconstruction Defense:** Classical SVM hyperplanes and convolutional filter weights in the staged model artifacts represent generalized decision boundaries and cannot be readily inverted to reconstruct recognizable subject faces.
3. **Dual-Use Warning:** MorphGuard is an attack **detection** tool, not an attack generation tool. Zero code for morph creation, face warping, or synthetic identity spoofing is distributed in this repository.
