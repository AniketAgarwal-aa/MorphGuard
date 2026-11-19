# MorphGuard V3.0 — End-to-End Cloud Deployment Guide

This guide details the deployment of **MorphGuard V3.0** across its three core tiers:
1. **GitHub (`AniketAgarwal-aa/MorphGuard`):** Application source code, documentation, configuration, and evaluation metadata.
2. **Hugging Face Hub (`AniketAgarwal-aa/MorphGuard-Models`):** Trained model weights, PyTorch checkpoints, and model cards.
3. **Streamlit Community Cloud (`https://share.streamlit.io`):** Public web application hosting.

---

## 1. Prerequisites & Environment

- **Python Runtime:** 3.12 (Pinned in `.python-version` and tested in `.venv`)
- **Key Dependencies:** `streamlit>=1.40.0`, `opencv-python-headless>=4.10.0`, `huggingface_hub>=0.20.0`, `scikit-learn>=1.3.0`, `torch>=2.0.0`
- **Zero Raw Biometric Data in Version Control:** Ensure `MONOT/`, `ONOT/`, and `data/cache/` are ignored in `.gitignore`.

---

## 2. Model Hosting on Hugging Face Hub

Because trained models (`.joblib`, `.pt`) total ~87 MB, they are excluded from Git and hosted on Hugging Face Hub.

### Step 2.1: Verify Local Staging
```powershell
python scripts/upload_to_huggingface.py --dry-run
```
This stages 15 trained models and metadata into `models/hf_export/`:
- `classical/`: Scikit-Learn models (`combined_svm.joblib`, `logistic_regression.joblib`, `hog_svm.joblib`, etc.)
- `deep_learning/`: PyTorch models (`custom_cnn.pt`)
- `ensembles/`: Stacking and voting ensembles (`stacking_ensemble.joblib`, `voting_ensemble.joblib`)
- `metadata/`: Architecture JSONs and `model_registry.json`
- `README.md`: Biometric model card and metrics

### Step 2.2: Upload to Hugging Face
With your Hugging Face write token:
```powershell
python scripts/upload_to_huggingface.py --token <YOUR_HF_WRITE_TOKEN>
```
Or set `HF_TOKEN` in your environment:
```powershell
$env:HF_TOKEN = "<YOUR_HF_WRITE_TOKEN>"
python scripts/upload_to_huggingface.py
```
*Note:* The default target repository is `AniketAgarwal-aa/MorphGuard-Models`.

---

## 3. Deploy to Streamlit Community Cloud

### Step 3.1: Connect Repository
1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **Create app** -> **I already have an app**.
3. Configure deployment settings:
   - **Repository:** `AniketAgarwal-aa/MorphGuard`
   - **Branch:** `master`
   - **Main file path:** `app/main.py`
   - **App URL:** `morphguard` (or default generated slug)

### Step 3.2: Configure Secrets (Hugging Face Integration)
In **Advanced settings** -> **Secrets**, paste your configuration:
```toml
# Streamlit Secrets for MorphGuard
MORPHGUARD_MODEL_REPO = "AniketAgarwal-aa/MorphGuard-Models"
HF_TOKEN = "hf_your_read_or_write_token_here"
```
*(If the Hugging Face repository is public, `HF_TOKEN` is optional).*

### Step 3.3: Deploy
Click **Deploy!**. Streamlit will install dependencies from `requirements.txt` using Python 3.12, load the theme from `.streamlit/config.toml`, and start the app.

---

## 4. Live Verification & Testing

Once deployed on Streamlit Cloud:
1. Open the app URL.
2. Navigate to **Face Morph Analysis** in the sidebar.
3. Confirm that the model selectbox displays all available models (`combined_svm.joblib`, `logistic_regression.joblib`, `custom_cnn.pt`, etc.).
4. Select a model (e.g. `combined_svm.joblib`).
5. Upload a portrait image (PNG/JPG) or select one of the pre-packaged quick samples.
6. The app lazily downloads the model weights from Hugging Face Hub (verifying SHA-256 hash), runs face detection, multi-scale feature extraction, and computes calibrated morph attack prediction and confidence.
