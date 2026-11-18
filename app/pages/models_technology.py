import sys
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from app.components import inject_css, page_header, empty_state, load_annotation_summary, metric_card, section_title, footer

inject_css()
page_header(
    'TECHNOLOGY',
    'Models & Technology Stack',
    'Technical foundation: OpenCV preprocessing, handcrafted texture extraction, PyTorch CNNs, and scientific safeguards.'
)

# ── Architecture & Technology Matrix ──────────────────────────────────────────
section_title('Implemented Model Architectures')
st.caption('All architectures below are implemented in src/morphguard/ and tested. None are falsely reported as trained without verified artifacts.')

items = [
    {
        'Component': 'Custom CNN',
        'Technology': 'PyTorch (2-stage Conv2D + AdaptiveAvgPool + Dropout)',
        'Input Representation': '224×224×3 RGB Face Crop',
        'Implementation State': '✓ Implemented & Forward Tested',
        'Operational Status': 'No trained artifact (awaiting labels)'
    },
    {
        'Component': 'ResNet18',
        'Technology': 'PyTorch (Residual Network with modified classification head)',
        'Input Representation': '224×224×3 RGB Face Crop',
        'Implementation State': '✓ Implemented & Forward Tested',
        'Operational Status': 'No trained artifact (awaiting labels)'
    },
    {
        'Component': 'EfficientNet-B0',
        'Technology': 'PyTorch (Compound scaled inverted bottleneck architecture)',
        'Input Representation': '224×224×3 RGB Face Crop',
        'Implementation State': '✓ Implemented & Forward Tested',
        'Operational Status': 'No trained artifact (awaiting labels)'
    },
    {
        'Component': 'LBP + SVM',
        'Technology': 'scikit-image + scikit-learn (Uniform LBP histogram)',
        'Input Representation': '10-dim texture histogram',
        'Implementation State': '✓ Pipeline Ready',
        'Operational Status': 'Awaiting reviewed labels'
    },
    {
        'Component': 'HOG + SVM',
        'Technology': 'scikit-image + scikit-learn (Oriented gradient histogram)',
        'Input Representation': '6,084-dim structural gradient vector',
        'Implementation State': '✓ Pipeline Ready',
        'Operational Status': 'Awaiting reviewed labels'
    },
    {
        'Component': 'GLCM + Random Forest',
        'Technology': 'scikit-image + scikit-learn (Co-occurrence statistics)',
        'Input Representation': '5-dim texture statistics',
        'Implementation State': '✓ Pipeline Ready',
        'Operational Status': 'Awaiting reviewed labels'
    },
    {
        'Component': 'Combined Features + SVM',
        'Technology': 'Multi-scale fusion: LBP + HOG + GLCM + Statistical moments',
        'Input Representation': '6,103-dim combined representation',
        'Implementation State': '✓ Pipeline Ready',
        'Operational Status': 'Awaiting reviewed labels'
    },
]

st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)

# ── Feature Extraction Techniques ─────────────────────────────────────────────
st.markdown('---')
section_title('Feature Extraction Techniques')

f1, f2, f3, f4 = st.columns(4)
with f1:
    metric_card('LBP', '10 dims', 'Micro-texture histogram')
with f2:
    metric_card('HOG', '6,084 dims', 'Structural gradient orientations')
with f3:
    metric_card('GLCM', '5 dims', 'Spatial co-occurrence matrix')
with f4:
    metric_card('COMBINED', '6,103 dims', 'Complete fused vector')

st.markdown('''
- **Local Binary Patterns (LBP):** Computes rotationally-invariant uniform binary patterns with radius $R=1$ and $P=8$ neighbors. Quantizes local texture transitions into 10 histogram bins that capture skin smoothness and blending seams.
- **Histogram of Oriented Gradients (HOG):** Uses 9 orientation bins with $16 \\times 16$ pixel cells and $2 \\times 2$ block normalization. Identifies structural facial edge anomalies and artificial contour distortions caused by morphing algorithms.
- **Gray-Level Co-occurrence Matrix (GLCM):** Computes second-order spatial statistics (contrast, dissimilarity, homogeneity, energy, correlation) at distances $[1, 2]$ and angles $[0, \\pi/4]$. Sensitive to pixel interpolation artifacts in morphed facial regions.
- **Statistical Descriptors:** Mean intensity, standard deviation, Shannon entropy, and Canny edge density across the face crop.
''')

# ── Core Technology Stack ─────────────────────────────────────────────────────
st.markdown('---')
section_title('Software Stack & Environment')

tech_col1, tech_col2 = st.columns(2)
with tech_col1:
    st.markdown('''
- **Computer Vision:** `OpenCV (cv2)` for image loading, Haar-cascade face detection, and CLAHE pre-processing.
- **Image Features:** `scikit-image` for LBP, HOG, and GLCM extraction.
- **Deep Learning:** `PyTorch` & `torchvision` for CNN models, forward-pass inference, and checkpoint validation.
''')
with tech_col2:
    st.markdown('''
- **Machine Learning:** `scikit-learn` for PCA decomposition, baseline classifiers, and metric calculation.
- **Application Interface:** `Streamlit` with custom navy/cyan theme and native component architecture.
- **Testing & Quality:** `pytest` suite ensuring all pipelines, guards, and math operations pass.
''')

empty_state(
    'No Approved Detector Artifact Installed',
    'A model file alone is not enough: a deployment-ready artifact must include approval status, '
    'preprocessing metadata, label-manifest reference, data split hash, and independent evaluation evidence.'
)

annotations = load_annotation_summary()
with st.expander('Training Readiness Status'):
    approved = annotations.get('approved_for_training', 0)
    st.write(f'Approved reviewed records: **{approved:,}**')
    if approved == 0:
        st.warning(
            'Supervised model training is blocked by design until human-reviewed labels '
            'and a leakage-safe identity-isolated split are approved.'
        )

footer()
