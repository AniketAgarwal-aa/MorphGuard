# MorphGuard V3.2 — Live Streamlit Hosted Acceptance & Parity Report

**Application URL:** [https://morphguard.streamlit.app/](https://morphguard.streamlit.app/)  
**Entrypoint:** `app/main.py`  
**GitHub Branch / Tag:** `master` / `v3.2` (`c17561db41dae9d5f154c4c8093bfcf2b64f6b16`)  
**Model Hub Integration:** [AniketAgarwal-aa/MorphGuard-Models](https://huggingface.co/AniketAgarwal-aa/MorphGuard-Models) (PUBLIC)  
**Standard Compliance:** ISO/IEC 30107-3 Presentation Attack Detection  

---

## 1. 14-Page Navigation & Rendering Verification

All 14 modular pages were verified for clean syntax, import resolution, and responsive rendering across the 6 sidebar navigation categories:

| Page Category | Page Identifier | Streamlit Script Path | Status |
| :--- | :--- | :--- | :---: |
| **1. Detection & Verification** | Face Morph Analysis | `app/pages/1_Face_Morph_Analysis.py` | **PASS** |
| | Executive Dashboard | `app/pages/overview.py` | **PASS** |
| **2. Biometric Data & Provenance**| Dataset Explorer | `app/pages/4_Dataset_Explorer.py` | **PASS** |
| | Annotation Review Workbench | `app/pages/annotation_review.py` | **PASS** |
| | Dataset Technical Specs | `app/pages/datasets.py` | **PASS** |
| **3. Benchmarking & Evaluation** | Multi-Model Comparison | `app/pages/2_Model_Comparison.py` | **PASS** |
| | Research Experiments | `app/pages/5_Research_Experiments.py` | **PASS** |
| | Architecture Deep-Dive | `app/pages/models_technology.py` | **PASS** |
| **4. Interpretability** | Feature Space Explorer | `app/pages/3_Explainability.py` | **PASS** |
| **5. Documentation & Standards** | Methodology & Formulas | `app/pages/6_Methodology.py` | **PASS** |
| | Technical API Docs | `app/pages/technical_documentation.py` | **PASS** |
| | How It Works Guide | `app/pages/how_it_works.py` | **PASS** |
| **6. Governance & Limitations** | Limitations & Disclaimers | `app/pages/7_Limitations_And_Info.py` | **PASS** |
| | Research Mission & About | `app/pages/about.py` | **PASS** |

---

## 2. Model Selection & Inference Verification (Representative Architectures)

| Model Name | Framework | Download Source | Optimal Threshold $\tau^*$ | Inference Output State | Parity Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Combined SVM (RBF)** | scikit-learn | Public Hub Cache | **0.0051** | `GENUINE` / `MORPHED` | **VERIFIED (Parity)** |
| **HOG SVM (RBF)** | scikit-learn | Public Hub Cache | **0.0040** | `GENUINE` / `MORPHED` | **VERIFIED (Parity)** |
| **Voting Ensemble** | scikit-learn | Public Hub Cache | **0.1631** | `GENUINE` / `MORPHED` | **VERIFIED (Parity)** |
| **EfficientNet-B0** | PyTorch | Public Hub Cache | **0.0032** | `GENUINE` / `MORPHED` | **VERIFIED (Parity)** |
| **ResNet-18** | PyTorch | Public Hub Cache | **0.00000664** | `GENUINE` / `MORPHED` | **VERIFIED (Parity)** |
| **ResNet-50** | PyTorch | Public Hub Cache | **0.000703** | `GENUINE` / `MORPHED` | **VERIFIED (Parity)** |

---

## 3. Local versus Cloud Prediction Parity Analysis

A critical objective was preventing the previously observed discrepancy where local MorphGuard returned `AUTHENTIC` while the cloud application returned `MORPHED` for the identical input image.

### Root Cause of Prior Discrepancy
1. **Uncalibrated vs. Calibrated Threshold Mismatch:** The previous cloud build utilized a hardcoded fallback threshold of `0.5000` or an inverted probability score $1 - P$, whereas local inference used decision function margins.
2. **Standardized Fix in V3.2:**
   - Both local and hosted runtimes strictly utilize `src/morphguard/inference/hosted_models.py` and `src/morphguard/inference/service.py`.
   - The decision rule is strictly unified:
     $$\text{Decision} = \begin{cases} \text{MORPHED}, & \text{if } P(\text{Morphed}) \ge \tau^* \\ \text{GENUINE}, & \text{if } P(\text{Morphed}) < \tau^* \end{cases}$$
   - For `combined_svm`, $\tau^* = 0.0051$ is applied uniformly across both local and hosted environments.
   - Result: **Zero prediction discrepancy between local and cloud runtimes.**

---

## 4. Edge-Case & Error Handling Acceptance

- **Missing Face in Input:** When an image without a detectable human face is uploaded, the Haar cascade safely routes to `state = "FACE NOT DETECTED"`, issuing an informative warning rather than crashing.
- **Corrupted / Non-Image File:** Defensive format validation intercepts non-image files, displaying a user-friendly error message.
- **Export Validation:** Both JSON and CSV prediction reports generate valid RFC 4180 / JSON RFC 8259 structured output files upon user download.
