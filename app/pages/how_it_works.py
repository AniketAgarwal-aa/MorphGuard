import sys
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from app.components import inject_css, page_header, section_title, footer

inject_css()
page_header(
    'ARCHITECTURE',
    'How It Works',
    'The 7-stage MorphGuard processing pipeline, separating reliable image processing from supervised classification.'
)

steps = [
    (
        '01',
        'Image Input & File Validation',
        'The submitted file is verified against allowed formats (PNG, JPG, JPEG) and size limits (10 MB). '
        'The raw bytes are decoded in-memory using OpenCV. Corrupted or unreadable payloads are rejected immediately '
        'without crashing the runtime.'
    ),
    (
        '02',
        'Face Detection & Localization',
        'An OpenCV Haar-cascade frontal face detector locates candidate faces within the image. '
        'Multiple-face occurrences are tracked and reported; the primary bounding box is ranked by area and '
        'isolated with contextual margin padding for downstream processing.'
    ),
    (
        '03',
        'Image Quality Assessment',
        'Before feature extraction or classification, the image undergoes objective biometric quality analysis: '
        'Laplacian blur variance (sharpness), mean pixel luminance (brightness), and standard deviation (contrast). '
        'Images that fall outside operational thresholds receive clear warnings.'
    ),
    (
        '04',
        'Face Alignment & Preprocessing',
        'The detected primary face region is cropped with a 15% bounding box margin and standardized to a fixed '
        '224×224 pixel resolution using area-based interpolation (`INTER_AREA`). Color spaces are aligned to RGB '
        'for cross-pipeline compatibility.'
    ),
    (
        '05',
        'Multi-Scale Feature Extraction',
        'The 224×224 normalized face crop is transformed into a rich 6,103-dimensional descriptor: '
        '10-bin Uniform Local Binary Patterns (LBP) for skin micro-texture, '
        '6,084-dimensional Histogram of Oriented Gradients (HOG) for facial edge contours, '
        '5-property Gray-Level Co-occurrence Matrix (GLCM) for spatial texture statistics, '
        'and 4 global statistical moments.'
    ),
    (
        '06',
        'Model Evaluation & Inference Stage',
        'If an approved model artifact is loaded, feature vectors or RGB tensors feed into the classifier. '
        'When no validated artifact is present, MorphGuard enforces a strict `MODEL UNAVAILABLE` state, '
        'preventing the generation of synthetic or speculative prediction scores.'
    ),
    (
        '07',
        'Result Presentation & Auditable Reports',
        'All results—detection coordinates, quality scores, feature dimensions, and processing latency—are presented '
        'in clean visual tables and download-ready structured JSON reports. Full provenance and disclaimer metadata '
        'are embedded in every export.'
    ),
]

for number, title, body in steps:
    st.markdown(
        f'<div class="progress-card" style="margin:.7rem 0">'
        f'<span class="eyebrow" style="color:#35d1c4;font-size:.85rem;font-weight:800">STAGE {number}</span>'
        f'<h3 style="margin:.3rem 0 .5rem 0">{title}</h3>'
        f'<p style="color:#c8dce9;font-size:.92rem;line-height:1.6;margin:0">{body}</p>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown('---')
section_title('Technical & Scientific Guarantees')
st.markdown('''
- **Reproducibility:** Preprocessing and feature extraction steps produce deterministic numeric vectors given the same input image.
- **Privacy First:** Uploaded images exist exclusively in working memory during the request lifecycle. No uploads are written to disk.
- **Safe Fallbacks:** Every math routine safely handles zero norms, infinite values, and missing faces without uncaught exceptions.
''')

footer()
