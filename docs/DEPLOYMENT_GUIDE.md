# MorphGuard V3.0 — Deployment & Hosting Guide

## 1. Cloud Architecture Overview
To keep the GitHub repository lightweight (< 50 MB) and protect biometric data, MorphGuard separates code, runtime, and model weights:

- **Source Code:** Hosted on GitHub ([`AniketAgarwal-aa/MorphGuard`](https://github.com/AniketAgarwal-aa/MorphGuard.git)). Contains application, feature extraction pipeline, and metadata.
- **Application Runtime:** Deployed on Streamlit Community Cloud or Docker.
- **Model Storage:** Lightweight models run locally. Heavy checkpoints are hosted on Hugging Face Hub with SHA-256 integrity verification.
- **Biometric Datasets:** Excluded via `.gitignore` and never committed or uploaded publicly.

---

## 2. Hosted Model Loading (`src/morphguard/inference/hosted_models.py`)
MorphGuard implements lazy model resolution:
1. Checks local path in `models/trained/` or `models/checkpoints/`.
2. If missing, retrieves the model from Hugging Face Hub using `hf_hub_download`:
   - Configurable via `MORPHGUARD_MODEL_REPO` or Streamlit Secrets (`st.secrets["HF_REPO_ID"]`).
   - Caches downloads into `models/cache/`.
   - Verifies SHA-256 against expected hash in `models/metadata/{model_name}.json`.
3. If neither local nor remote is accessible, safely transitions to `STATUS: MODEL UNAVAILABLE` without crashing.

---

## 3. Deployment Steps (Streamlit Community Cloud)
1. Fork or push repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Select repository: `AniketAgarwal-aa/MorphGuard`, Branch: `master`, Main file: `app/main.py`.
4. (Optional) In Advanced Settings / Secrets, add:
   ```toml
   HF_REPO_ID = "YourOrg/MorphGuard-Models"
   HF_TOKEN = "<your-huggingface-token-here>"
   ```
5. Deploy.
