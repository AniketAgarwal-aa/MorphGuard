# MorphGuard Changelog

All notable changes to the MorphGuard project are documented in this file.

## [3.0.0] - 2026-11-19 (Current Release)

### Added
- **Full Dataset Feature Cache:** 100% processing of all 46,792 biometric images across MONOT (Gate_10, Gate_25, Morphed) and ONOT (digital, print-scan) into 182 compressed NPZ shards (3.39 GB) with 99.02% face detection rate.
- **Hugging Face Hub Integration:** Lazy model resolution via `src/morphguard/inference/hosted_models.py` supporting remote downloads from `AniketAgarwal-aa/MorphGuard-Models` with SHA-256 integrity verification.
- **Automated Staging Script (`scripts/upload_to_huggingface.py`):** Stages 15 trained models into `classical/`, `deep_learning/`, `ensembles/`, and `metadata/` with model cards.
- **Calibration Pipeline (`scripts/recalibrate_and_evaluate_all.py`):** Validation-based ACER minimization yielding 96.49% test accuracy on `combined_svm` and 0.0132 APCER on held-out test data.
- **Model Card & Deployment Guides:** `MODEL_CARD.md`, `DEPLOYMENT.md`, and comprehensive documentation in `docs/`.
- **Python 3.12 Runtime Pinning:** `.python-version` configured for streamlined Streamlit Community Cloud hosting.

### Changed
- **Streamlit Configuration:** Upgraded `.streamlit/config.toml` with native dark mode branding, primary accent `#00dcbe`, and headless execution.
- **Sidebar Model Discovery:** `app/pages/1_Face_Morph_Analysis.py` dynamically resolves models from both local directories and `models/metadata/model_registry.json`.
- **Requirements Update:** `requirements.txt` updated with headless OpenCV (`opencv-python-headless==4.10.0.84`) and `huggingface_hub>=0.20.0`.
- **Memory Footprint Optimization:** `3_Explainability.py` and `5_Research_Experiments.py` optimized to load metadata summaries and bounded samples, preventing RAM exhaustion on 8 GB environments.

---

## [2.0.0] - 2026-11-18

### Added
- Multi-model evaluation architecture supporting 15 scikit-learn and PyTorch models.
- Subject-disjoint train/validation/test split generator using graph connected components to prevent identity leakage.
- Human-in-the-loop annotation audit workbench (`app/pages/annotation_review.py`).
- ISO/IEC 30107-3 biometric metric reporting (APCER, BPCER, ACER).

---

## [1.0.0] - 2026-11-17

### Added
- Initial prototype with OpenCV Haar cascade face detection and basic GLCM texture extraction.
- Single-image morph inspection interface in Streamlit.
