# Contributing to MorphGuard

Thank you for your interest in contributing to **MorphGuard**! We welcome academic research contributions, bug fixes, algorithmic improvements, and documentation enhancements.

---

## 1. Development Principles

1. **Scientific Integrity First:** All reported metrics must be strictly reproducible on the designated validation and test splits. Never alter empirical numbers or tune decision thresholds on the test partition.
2. **Zero Biometric Data Exposure:** Never commit raw facial images, biometric crops, `.npz` feature caches, or private subject manifests to Git. Always verify `.gitignore` before submitting changes.
3. **No Unauthenticated Secret Uploads:** Never commit `.env` files, API keys, or personal access tokens.

---

## 2. Setting Up Development Environment

```powershell
git clone https://github.com/AniketAgarwal-aa/MorphGuard.git
cd MorphGuard
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pytest
```

---

## 3. Pull Request Guidelines

Before submitting a Pull Request (PR):
1. **Run Unit Tests:**
   ```powershell
   $env:PYTHONPATH = "src"
   pytest tests/ -v
   ```
2. **Verify Streamlit Pages:**
   ```powershell
   python scripts/test_all_pages.py
   ```
3. **Verify Dependencies:**
   ```powershell
   pip check
   ```
4. **Scan for Credentials:**
   ```powershell
   python scripts/scan_secrets.py
   ```

---

## 4. Code Style & Standards

- Follow PEP 8 style guidelines.
- Include docstrings on all public functions, classes, and methods.
- Ensure all model changes update the central registry in `models/metadata/model_registry.json`.
