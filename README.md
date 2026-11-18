# MorphGuard

Local, research-oriented facial morphing attack detection using **only MONOT and ONOT**. Raw datasets are protected: all generated material is written outside `MONOT/` and `ONOT/`.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
$env:PYTHONPATH = "src"
python scripts/audit_datasets.py
python scripts/run_pipeline.py splits
streamlit run app/main.py
```

The app starts in explicit research-only mode until a reviewed manifest and approved model artifact exist. Validate a reviewed manifest with `python scripts/validate_label_manifest.py data/manifests/label_manifest.csv`; training commands require that manifest.

Run feature extraction and model training only after establishing a defensible labelled protocol. `MONOT/Morphed` is provisionally marked `morphed`; gate folders and ONOT categories are retained as metadata, not guessed labels.

## Important scientific limitation

MONOT’s official page states that bona fide images are provided by ONOT. Combining sources can therefore create dataset-source confounding (acquisition, compression, resolution, or generation differences). This repository prevents a silent assumption that folder names are classes, groups identities during splits, and does not claim cross-dataset generalization.

## Commands

- `python scripts/audit_datasets.py` — streaming inventory; add `--hash-duplicates` only when disk reads are acceptable.
- `python scripts/create_splits.py data/metadata/monot_inventory.csv` — creates leakage-aware splits from labels present in the input manifest.
- `python scripts/extract_features.py data/splits/train.csv` — creates resumable NPZ feature shards.
- `python scripts/validate_label_manifest.py data/manifests/label_manifest.csv` — rejects unreviewed labels, missing files, and split leakage.
- `streamlit run app/main.py` — local dashboard.

For deployment handoff, see `docs/FINAL_DEPLOYMENT_HANDOFF.md`. Docker does not include raw datasets.

The Streamlit interface includes a dark research-dashboard theme, cached audit cards/charts, Dataset Explorer, Model Comparison, Explainability, Research Experiments, Methodology, Limitations, and a safe Face Morph Analysis workflow. The app starts in research-only mode when no approved model artifact is present.

License: code is MIT; MONOT has its own CC BY-NC 4.0 terms and ONOT retains its source terms. Do not publish either dataset with this repository.
