# MorphGuard Cloud & Server Deployment Guide

**Target Hosting Platform:** Streamlit Community Cloud / Cloud VM (Docker, Ubuntu)  
**Entry Point:** `app/main.py`  
**Configuration Directory:** `.streamlit/config.toml`  

---

## 1. Hosting Architecture Overview

MorphGuard is engineered for stateless, CPU-efficient deployment. In a cloud environment:
- The Streamlit runtime executes `app/main.py`.
- **Model Storage:** Model binaries are not checked into Git. Instead, `src/morphguard/inference/hosted_models.py` dynamically downloads requested model checkpoints from Hugging Face Hub (`AniketAgarwal-aa/MorphGuard-Models`) on-demand and caches them in the local container cache directory.
- **Lazy Loading:** Models are loaded into memory only when selected for inference, conserving container RAM (fits within Streamlit Community Cloud's 1 GB RAM quota).

---

## 2. Streamlit Community Cloud Deployment

### 2.1 Repository Settings
1. Navigate to [share.streamlit.io](https://share.streamlit.io).
2. Connect your GitHub account and select:
   - **Repository:** `AniketAgarwal-aa/MorphGuard`
   - **Branch:** `master`
   - **Main file path:** `app/main.py`

### 2.2 Advanced Settings & Environment Variables
In the Streamlit App Settings -> **Secrets**, define:
```toml
# Hugging Face Hub Token (required if repository is Private)
# HF_TOKEN = "<INSERT_HF_READ_TOKEN>"

# Model Repository Identifier
HF_REPO_ID = "AniketAgarwal-aa/MorphGuard-Models"
```

### 2.3 Dependency Configuration
Streamlit Cloud automatically installs dependencies listed in `requirements.txt`.
Ensure `requirements.txt` specifies headless OpenCV:
```text
opencv-python-headless>=4.8.0
torch>=2.2.0
torchvision>=0.17.0
scikit-learn>=1.4.0
scikit-image>=0.22.0
streamlit>=1.35.0
huggingface_hub>=0.20.0
```

---

## 3. Server Configuration (`.streamlit/config.toml`)

MorphGuard includes a production-ready `.streamlit/config.toml`:

```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 10

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#2563EB"
backgroundColor = "#0F172A"
secondaryBackgroundColor = "#1E293B"
textColor = "#F8FAFC"
font = "sans serif"
```

---

## 4. Verification Post-Deployment

Once deployed, verify:
1. `GET /` returns HTTP 200 OK.
2. Select `combined_svm` on `Face Morph Analysis` page.
3. Upload a sample image and verify that the remote download succeeds and yields a valid prediction without container out-of-memory (OOM) errors.
