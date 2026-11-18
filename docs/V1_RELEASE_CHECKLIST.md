# MorphGuard V1.0 Release Checklist

## Verified

- [x] Streamlit application starts and health endpoint returns HTTP 200.
- [x] Grouped navigation renders under `MAIN PROJECT` and `ABOUT PROJECT`.
- [x] 16 automated tests pass.
- [x] Python compilation and `pip check` pass.
- [x] 500-record image feature cache validates successfully.
- [x] LBP/HOG/GLCM dimensions are stable and finite.
- [x] Face Analysis supports upload, face detection, quality analysis, feature extraction and JSON report download.
- [x] Annotation Review preserves pending status, evidence requirements, backups and audit history.
- [x] Raw MONOT/ONOT directories and `data/cache` are ignored by Git.
- [x] README and demonstration commands describe the current research-only state.

## Before demonstration

1. Activate `.venv` and set `PYTHONPATH=src`.
2. Run the test and cache-validation commands below.
3. Start Streamlit and follow `DEMONSTRATION_GUIDE.md`.
4. Use only approved demonstration images and do not present quality values as morph probabilities.

## Known limitations

- No approved labels, trained detector or independent metrics exist.
- Docker engine validation is environment-dependent and was not required for the local presentation release.
- The image cache covers 500 records; it is intentionally not the full dataset.

## Verification commands

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\validate_feature_cache.py
.\.venv\Scripts\python.exe -m pip check
streamlit run app\main.py
```
