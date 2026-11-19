# MorphGuard Installation & Local Setup Guide

**Supported Operating Systems:** Windows 10/11, Ubuntu 20.04+, macOS 12+  
**Required Python Version:** Python 3.10+  

---

## 1. Prerequisites

- Python 3.10.x installed and accessible via system PATH.
- Git installed.
- (Recommended) Dedicated virtual environment (`venv` or `conda`).

---

## 2. Windows Installation (PowerShell)

### Step 1: Clone Repository
```powershell
git clone https://github.com/AniketAgarwal-aa/MorphGuard.git
cd MorphGuard
```

### Step 2: Create and Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Core Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

*Note on PyTorch (CPU-Only):*
If installing PyTorch manually on a CPU machine:
```powershell
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

---

## 3. Linux / macOS Installation (Bash)

```bash
git clone https://github.com/AniketAgarwal-aa/MorphGuard.git
cd MorphGuard
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Verification & Testing

Verify that your local environment is correctly configured by executing the test suite:

```powershell
# Set Python path to include source library
$env:PYTHONPATH = "src"

# 1. Run unit test suite
pytest tests/ -v

# 2. Verify all 14 Streamlit pages render cleanly
python scripts/test_all_pages.py

# 3. Verify dependency tree
pip check
```

---

## 5. Launching the Application

```powershell
$env:PYTHONPATH = "src"
streamlit run app/main.py
```
Open `http://localhost:8501` in your browser.
