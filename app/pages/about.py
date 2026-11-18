import sys
from pathlib import Path
import streamlit as st
ROOT = Path(__file__).parents[2]; sys.path.insert(0, str(ROOT))
from app.components import inject_css, page_header, section_title, footer

inject_css()
page_header(
    'PROJECT',
    'About MorphGuard',
    'A practical tool for understanding facial image integrity and developing morphing attack detection methods.',
)

# ── Problem statement ─────────────────────────────────────────────────────────
section_title('Problem statement')
st.markdown(
    '''
A **facial morphing attack** is a deliberate manipulation in which the biometric
characteristics of two or more individuals are blended into a single identity-document
photograph. When this composite image passes automated or human facial verification, it
creates an enrolment that multiple individuals can unlock — a severe identity-fraud
vulnerability.

Morphing attacks are relevant wherever face images are used for high-stakes enrolment:
passport issuance, border crossing, visa applications, and access-card programmes.
Existing detection approaches broadly fall into two families:

| Approach | Description | Limitations |
|---|---|---|
| **Single-image (no-reference)** | Analyses the submitted image in isolation for artefacts | Sensitive to compression and resolution |
| **Differential (reference)** | Compares against a trusted probe image | Requires a live-capture reference |

Neither approach is universally reliable across all acquisition conditions, morphing
algorithms, and compression pipelines. MorphGuard is designed as a research environment
to develop, evaluate, and understand detection methods under controlled conditions.
'''
)

# ── Motivation ────────────────────────────────────────────────────────────────
section_title('Motivation')
st.write(
    'Academic and practitioner literature on morphing-attack detection often lacks reproducible, '
    'self-contained tooling. Researchers need a platform that:'
)
st.markdown(
    '- Applies consistent pre-processing (face detection, alignment, quality filtering) across datasets\n'
    '- Makes feature pipelines explicit and inspectable, not opaque\n'
    '- Records experimental configuration and results without fabricating outcomes\n'
    '- Can be extended incrementally as new models and datasets are validated\n'
    '- Runs locally without sending biometric data to external services'
)
st.info(
    'MorphGuard prioritises correctness and transparency over optimistic accuracy claims. '
    'It will not display a classification result until a validated model artifact is installed.'
)

# ── Scope and objectives ──────────────────────────────────────────────────────
section_title('Scope and objectives')
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        '<div class="panel">'
        '<div class="eyebrow" style="color:#35d1c4">In scope</div>'
        '<ul style="color:#c8dce9;padding-left:1.2rem;line-height:1.8">'
        '<li>Single-image analysis and quality assessment</li>'
        '<li>Handcrafted feature extraction (LBP, HOG, GLCM)</li>'
        '<li>Dataset exploration for MONOT and ONOT corpora</li>'
        '<li>Experiment configuration and result tracking</li>'
        '<li>Foundation for CNN-based detector development</li>'
        '</ul>'
        '</div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        '<div class="panel">'
        '<div class="eyebrow" style="color:#ffd27b">Out of scope</div>'
        '<ul style="color:#c8dce9;padding-left:1.2rem;line-height:1.8">'
        '<li>Operational deployment without ethics / privacy review</li>'
        '<li>Real-time biometric screening at border control</li>'
        '<li>Processing images of real individuals without consent</li>'
        '<li>Morphing attack generation (this is a detection tool)</li>'
        '<li>Commercial use under current research licence</li>'
        '</ul>'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Research approach ─────────────────────────────────────────────────────────
section_title('Research approach')
st.markdown(
    '''
MorphGuard follows a staged, evidence-led development methodology:

1. **Dataset audit** – Catalogue all available images; compute per-class statistics;
   flag corruption, duplication and label ambiguity before any model is trained.

2. **Feature engineering** – Compute hand-crafted descriptors (LBP texture histograms,
   HOG gradient histograms, GLCM co-occurrence statistics) to build an interpretable
   baseline feature space.

3. **Exploratory analysis** – Use PCA and distribution plots to understand class
   separability and identify confounders (acquisition device, compression, resolution).

4. **Controlled experiments** – Define experiment configurations in YAML; record all
   hyperparameters and results; never report numbers that cannot be reproduced from the
   stored configuration.

5. **Model validation** – Evaluate any trained classifier against a held-out set using
   APCER, BPCER, and ACER metrics; subject results to peer review before flagging the
   model as operational.
'''
)

# ── What MorphGuard does ──────────────────────────────────────────────────────
section_title('What MorphGuard does')
st.write(
    'MorphGuard validates facial images, detects faces, assesses image quality, '
    'exposes dataset characteristics and provides a controlled foundation for '
    'traditional and deep-learning detector development.'
)

# ── Intended use ──────────────────────────────────────────────────────────────
section_title('Intended use')
st.markdown(
    '- University and academic biometrics projects\n'
    '- Reproducible image-processing experiments\n'
    '- Local demonstrations of safe inference workflows\n'
    '- Future deployment after model validation and privacy review'
)
st.info('The current release can analyze image suitability, but it does not claim a validated morphing classification model.')

footer()
