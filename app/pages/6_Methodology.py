import sys
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from app.components import inject_css, page_header, section_title, metric_card, footer

inject_css()
page_header(
    'METHODOLOGY',
    'Methodology',
    'Rigorous experimental design and processing pipeline: moving from raw biometric corpora to verified inference.'
)

# ── Processing Architecture Flow ──────────────────────────────────────────────
section_title('End-to-End Processing Architecture')
st.markdown('''
```text
┌─────────────────────────────────────────────────────────────┐
│                 MONOT / ONOT AUDITED CORPORA                │
│    24,140 MONOT records (Gate & Morph) + 22,652 ONOT records│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 IMAGE PREPROCESSING STAGE                   │
│  Format validation → Haar face detection → Quality metrics  │
│          → 15% padded crop → 224×224 RGB resizing           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                FEATURE EXTRACTION PIPELINE                  │
│   • LBP Uniform 10-bin histogram (skin micro-texture)       │
│   • HOG 9-orientation, 16×16 cell gradient vector (6084-dim)│
│   • GLCM spatial co-occurrence properties (5 metrics)       │
│   • Pixel statistical moments (4 metrics)                   │
│   ═══════════════════════════════════════════════════════   │
│   Combined Feature Vector: 6,103 dimensions                 │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              HUMAN-IN-THE-LOOP ANNOTATION AUDIT             │
│    Provenance verification → Evidence check → Review notes  │
│     → Immutable approval records with SHA-256 audit logs    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               LEAKAGE-SAFE MODEL DEVELOPMENT                │
│    Subject-isolated & morph-pair-isolated cross-validation  │
│    Zero train/test leakage → ISO/IEC 30107-3 metrics (APCER)│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               SAFE LOCAL INFERENCE DEPLOYMENT               │
│   Strict state management: MODEL UNAVAILABLE when untrained │
│        JSON audit exports with provenance verification       │
└─────────────────────────────────────────────────────────────┘
```
''')

st.markdown('---')

# ── Scientific Guardrails ─────────────────────────────────────────────────────
section_title('Core Scientific Principles & Guardrails')

g_col1, g_col2 = st.columns(2)

with g_col1:
    st.markdown('''
#### 1. Zero Identity Leakage
- Face recognition models and morph detectors easily overfit to subject identities rather than morphing artifacts.
- MorphGuard enforces strict subject-level splitting: no subject ID or constituent morph-pair contributor can appear in both training and test partitions.

#### 2. Protocol Neutrality & Confound Isolation
- MONOT and ONOT datasets differ in resolution, compression, and acquisition hardware.
- Naive classification between MONOT and ONOT measures dataset origin rather than biometric manipulation.
- MorphGuard models must be evaluated within consistent acquisition strata.
''')

with g_col2:
    st.markdown('''
#### 3. Threshold File Semantics
- ONOT threshold text files (`threshold=0.413...`, etc.) denote algorithmic cosine similarity subset inclusion.
- They are **not** binary ground-truth labels and are never used as training targets without external evidence.

#### 4. Uncalibrated Score Honesty
- Classifier decision values are raw distance or logit scores, not true Bayesian posterior probabilities.
- MorphGuard strictly refrains from presenting uncalibrated model scores as "percentage confidence" of a morph attack.
''')

st.markdown('---')

# ── Quality Evaluation Methodology ───────────────────────────────────────────
section_title('Biometric Image Quality Metrics')

q_col1, q_col2, q_col3 = st.columns(3)
with q_col1:
    metric_card('SHARPNESS', 'Laplacian Var', 'Blur threshold: Var ≥ 50.0')
with q_col2:
    metric_card('BRIGHTNESS', 'Mean Luminance', 'Acceptable range: 45–220')
with q_col3:
    metric_card('CONTRAST', 'Luminance Std', 'Minimum standard dev: ≥ 20.0')

st.markdown('''
- **Laplacian Blur Variance:** Convolves the grayscale image with a $3 \\times 3$ Laplacian kernel. Morphed images that have undergone aggressive spatial interpolation, feathering, or re-sampling exhibit reduced high-frequency energy, resulting in significantly lower Laplacian variance.
- **Luminance & Contrast Bounds:** Ensures images captured under severe underexposure, backlighting, or saturation are flagged before extracting texture descriptors.
''')

# ── Privacy and Local Execution ───────────────────────────────────────────────
st.markdown('---')
section_title('Privacy, Security & Ethics')
st.markdown('''
- **Local In-Process Processing:** Image uploads exist exclusively in temporary memory buffers during active Streamlit request cycles.
- **No Third-Party Transmission:** No biometric features, crops, or embeddings are transmitted to remote cloud APIs.
- **Auditability:** Every report download includes input parameters, timestamps, algorithm identifiers, and exact feature dimensions for academic reproducibility.
''')

footer()
