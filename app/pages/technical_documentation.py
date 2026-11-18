import sys
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from app.components import inject_css, page_header, section_title, metric_card, footer

inject_css()
page_header(
    'DOCUMENTATION',
    'Technical Documentation',
    'Project architecture, execution commands, dependency manifest, and scientific documentation.'
)

# ── Quick Execution Guide ─────────────────────────────────────────────────────
section_title('Running the Application')
st.markdown('''
To launch MorphGuard locally on Windows PowerShell:
```powershell
cd "C:\\Users\\admin\\Downloads\\Code\\MorphGuard"
.venv\\Scripts\\streamlit.exe run app\\main.py --server.port 8501
```
Then navigate to: `http://localhost:8501`
''')

# ── System Architecture Map ───────────────────────────────────────────────────
st.markdown('---')
section_title('Directory Structure & Modules')

st.markdown('''
```text
MorphGuard/
├── app/
│   ├── main.py                     # Entry point & st.navigation router
│   ├── components/                 # Shared UI styles, metric cards, data loaders
│   └── pages/                      # 14 distinct application pages
│       ├── overview.py             # Overview & executive summary
│       ├── about.py                # Problem statement, motivation & scope
│       ├── how_it_works.py         # 7-stage processing workflow
│       ├── datasets.py             # MONOT & ONOT dataset characteristics
│       ├── models_technology.py    # Architecture & stack matrix
│       ├── 1_Face_Morph_Analysis.py# Single & dual-image analysis interface
│       ├── 4_Dataset_Explorer.py   # Corpus distribution & metadata filters
│       ├── annotation_review.py    # Human-in-the-loop review interface
│       ├── 2_Model_Comparison.py   # Model architecture & evaluation registry
│       ├── 3_Explainability.py     # PCA exploratory analysis & feature distributions
│       ├── 5_Research_Experiments.py # Experiment tracking & cache status
│       ├── 6_Methodology.py        # Scientific methodology & processing flow
│       ├── 7_Limitations_And_Info.py # Governance, limitations & privacy
│       └── technical_documentation.py # Technical manual & embedded guides
├── src/morphguard/                 # Core Python package
│   ├── preprocessing/pipeline.py   # FacePreprocessor (Haar, crop, resize, quality)
│   ├── feature_extraction/features.py # LBP, HOG, GLCM, statistical extraction
│   ├── inference/                  # InferenceService, load_joblib_model, compare_vectors
│   ├── classification/models.py    # PyTorch CNN models (custom_cnn, resnet18, efficientnet)
│   ├── dataset/                    # Audit, manifest review, splits, leakage guards
│   └── evaluation/metrics.py       # APCER, BPCER, ACER, EER calculations
├── data/
│   ├── manifests/                  # annotation_inventory.csv, targeted_review_batch.csv
│   ├── metadata/                   # dataset_summary.json, exploratory_analysis.json
│   ├── review_pilot/               # 150-record annotation evidence package
│   └── cache/image_features/       # Resumable NPZ feature cache (500 images)
├── docs/                           # Scientific reports and audit documentation
└── tests/test_core.py              # 21 comprehensive automated test cases
```
''')

# ── Embedded Project Documentation Files ──────────────────────────────────────
st.markdown('---')
section_title('Embedded Technical Guides & Scientific Reports')
st.caption('Click an expander to read the full source markdown documentation from docs/.')

docs = [
    ('Scientific Protocol & Validity', 'docs/SCIENTIFIC_VALIDITY_AND_LABEL_PROTOCOL.md'),
    ('Human Label Review Guide', 'docs/LABEL_REVIEW_GUIDE.md'),
    ('Implementation Review & Architecture', 'docs/FINAL_IMPLEMENTATION_REVIEW.md'),
    ('Deployment Readiness & Handoff', 'docs/FINAL_DEPLOYMENT_HANDOFF.md'),
    ('System Performance & Benchmarks', 'docs/PERFORMANCE.md'),
    ('Installation & Environment Guide', 'docs/INSTALLATION.md'),
    ('Dataset Analysis Report', 'docs/DATASET_ANALYSIS.md'),
    ('Data Leakage Prevention Protocol', 'docs/DATA_LEAKAGE_PREVENTION.md'),
]

for title, relative in docs:
    path = ROOT / relative
    with st.expander(f'📄 {title} ({relative})'):
        if path.exists():
            st.markdown(path.read_text(encoding='utf-8'))
        else:
            st.warning(f'Document file not found: {relative}')

footer()
