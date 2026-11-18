from pathlib import Path
import json
import sys
import streamlit as st
ROOT = Path(__file__).parents[2]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / 'src'))
from morphguard.runtime import readiness
from app.components import (
    inject_css, page_header, metric_card, status_badge, empty_state,
    section_title, load_audit, load_metrics, audit_status, footer,
    get_accent_color, get_current_theme
)

inject_css()
summary, tables, counts = load_audit()
metrics = load_metrics()
ready = readiness()
audit = audit_status(summary, tables, counts)
total = int(counts['count'].sum()) if not counts.empty else 0
monot = int(counts[counts.dataset == 'MONOT']['count'].sum()) if not counts.empty else 0
onot = int(counts[counts.dataset == 'ONOT']['count'].sum()) if not counts.empty else 0

# ── Load processing summary ──────────────────────────────────────────────────
_proc_path = ROOT / 'data' / 'cache' / 'image_features' / 'processing_summary.json'
_proc = {}
try:
    if _proc_path.exists():
        _proc = json.loads(_proc_path.read_text())
except Exception:
    pass

page_header(
    'MORPHGUARD',
    'Facial Morphing Attack Detection',
    'Analyze facial images, explore biometric datasets and understand the technology behind safer identity verification.',
)

# ── Hero ─────────────────────────────────────────────────────────────────────
hero_left, hero_right = st.columns([1.35, 1])
with hero_left:
    st.markdown('### A clear path from image to insight')
    st.write(
        'MorphGuard brings image validation, face preprocessing, dataset intelligence '
        'and model development into one focused application.'
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button('Open Face Analysis', type='primary', use_container_width=True):
            st.switch_page('pages/1_Face_Morph_Analysis.py')
    with c2:
        if st.button('Explore Datasets', use_container_width=True):
            st.switch_page('pages/datasets.py')

with hero_right:
    st.markdown(
        '<div class="panel">'
        '<div class="eyebrow">CURRENT AVAILABILITY</div>'
        '<h3>Image analysis is ready</h3>'
        '<p>Validation, face detection and quality assessment are available now.</p>'
        '<p style="color:#ffd27b">Morphing classification will be enabled when an approved '
        'detection model is available.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Workflow diagram ──────────────────────────────────────────────────────────
st.markdown('---')
section_title('Processing workflow')
_is_dark = get_current_theme() == 'dark'
_p_bg = 'rgba(53,209,196,.14)' if _is_dark else 'rgba(2,132,199,.12)'
_p_bdr = '#2a7a6e' if _is_dark else '#0284c7'
_p_clr = '#35d1c4' if _is_dark else '#0284c7'
_arrow_clr = '#4a7488' if _is_dark else '#64748b'
_sub_clr = '#91a8ba' if _is_dark else '#64748b'

st.markdown(
    f'''
<div class="progress-card" style="font-family:monospace;text-align:center;padding:1.4rem 1rem">
  <div style="color:{_p_clr};font-size:.72rem;letter-spacing:.18em;margin-bottom:.8rem;font-weight:700">END-TO-END PIPELINE</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:.5rem;flex-wrap:wrap">
    <div style="background:{_p_bg};border:1px solid {_p_bdr};border-radius:10px;padding:.5rem .9rem;color:{_p_clr};font-weight:700">📤 Upload</div>
    <div style="color:{_arrow_clr};font-size:1.3rem">→</div>
    <div style="background:{_p_bg};border:1px solid {_p_bdr};border-radius:10px;padding:.5rem .9rem;color:{_p_clr};font-weight:700">🔍 Detect</div>
    <div style="color:{_arrow_clr};font-size:1.3rem">→</div>
    <div style="background:{_p_bg};border:1px solid {_p_bdr};border-radius:10px;padding:.5rem .9rem;color:{_p_clr};font-weight:700">✅ Assess</div>
    <div style="color:{_arrow_clr};font-size:1.3rem">→</div>
    <div style="background:{_p_bg};border:1px solid {_p_bdr};border-radius:10px;padding:.5rem .9rem;color:{_p_clr};font-weight:700">🧬 Extract</div>
    <div style="color:{_arrow_clr};font-size:1.3rem">→</div>
    <div style="background:{_p_bg};border:1px solid {_p_bdr};border-radius:10px;padding:.5rem .9rem;color:{_p_clr};font-weight:700">📄 Report</div>
  </div>
  <div style="color:{_sub_clr};font-size:.8rem;margin-top:.8rem">
    Image validation · Face crop · Quality scoring · Feature vectors (LBP / HOG / GLCM) · JSON export
  </div>
</div>
''',
    unsafe_allow_html=True,
)

# ── At a glance ──────────────────────────────────────────────────────────────
section_title('At a glance')
cols = st.columns(4)
for col, label, value, hint in zip(
    cols,
    ['AUDITED IMAGES', 'MONOT', 'ONOT', 'CORRUPTED'],
    [f'{total:,}', f'{monot:,}', f'{onot:,}', str(summary.get('corrupted_count', 0))],
    ['Local audit metadata', 'Morphed and gate strata', 'Digital and print-scan', 'Validated image records'],
):
    with col:
        metric_card(label, value, hint)

# ── Processing coverage ───────────────────────────────────────────────────────
if _proc:
    st.markdown('---')
    section_title('Feature extraction coverage', 'From data/cache/image_features/processing_summary.json')
    p1, p2, p3, p4 = st.columns(4)
    with p1: metric_card('REQUESTED', str(_proc.get('requested', '—')), 'Images in manifest')
    with p2: metric_card('PROCESSED', str(_proc.get('success', '—')), 'Successfully extracted', 'ok' if _proc.get('failed', 1) == 0 else 'neutral')
    with p3: metric_card('FAILED', str(_proc.get('failed', '—')), 'Extraction errors', 'ok' if _proc.get('failed', 1) == 0 else 'blocked')
    with p4: metric_card('FEATURE RECORDS', str(_proc.get('feature_records', '—')), f"{_proc.get('duration_seconds', '?')}s total runtime")

# ── What's available today ────────────────────────────────────────────────────
st.markdown('---')
section_title("What's available today")
avail_col, pend_col = st.columns(2)

with avail_col:
    st.markdown(
        '<div class="panel">'
        '<div class="eyebrow" style="color:#35d1c4">✔ Working now</div>'
        '<ul style="color:#c8dce9;margin-top:.6rem;padding-left:1.2rem;line-height:1.8">'
        '<li>Image upload &amp; format validation</li>'
        '<li>Haar-cascade face detection</li>'
        '<li>Quality assessment (blur, brightness, contrast)</li>'
        '<li>LBP / HOG / GLCM feature extraction</li>'
        '<li>Feature vector export (JSON / NPZ)</li>'
        '<li>Dataset audit statistics (MONOT &amp; ONOT)</li>'
        '<li>PCA visualisation of feature space</li>'
        '<li>Research experiment tracking</li>'
        '</ul>'
        '</div>',
        unsafe_allow_html=True,
    )

with pend_col:
    st.markdown(
        '<div class="panel">'
        '<div class="eyebrow" style="color:#ffd27b">⏳ Pending approval / development</div>'
        '<ul style="color:#c8dce9;margin-top:.6rem;padding-left:1.2rem;line-height:1.8">'
        '<li>Trained morphing-attack classifier</li>'
        '<li>Deep-learning feature extractor (CNN)</li>'
        '<li>Morphing confidence score output</li>'
        '<li>Containerised / Docker deployment</li>'
        '<li>REST API for external systems</li>'
        '<li>Formal model validation report</li>'
        '</ul>'
        '</div>',
        unsafe_allow_html=True,
    )

# ── What you can do ───────────────────────────────────────────────────────────
section_title('What you can do')
cards = [
    ('Face Analysis',       'Validate an image, locate faces and assess quality locally.',           ':material/face:'),
    ('Dataset Intelligence','Explore the audited MONOT and ONOT distributions.',                     ':material/database:'),
    ('Model Analysis',      'Compare implemented architectures and real evaluation outputs.',         ':material/compare_arrows:'),
    ('Model Insights',      'Understand texture, gradient and model explanation methods.',           ':material/visibility:'),
    ('Experiments',         'Track configured experiments without inventing results.',               ':material/science:'),
]
grid = st.columns(5)
for col, (title, body, icon) in zip(grid, cards):
    with col:
        st.markdown(
            f'<div class="panel">'
            f'<div style="font-size:1.5rem;color:#55dfd2">{icon}</div>'
            f'<b>{title}</b>'
            f'<p style="color:#9bb0c2;font-size:.85rem">{body}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Technology ────────────────────────────────────────────────────────────────
section_title('Technology')
st.markdown(
    '**OpenCV** for local image processing  ·  '
    '**LBP / HOG / GLCM** for handcrafted analysis  ·  '
    '**PyTorch** for CNN architectures  ·  '
    '**scikit-learn** for baselines  ·  '
    '**Streamlit** for the local product experience'
)
st.caption(f'{audit["label"]}: {audit["message"]} MorphGuard does not present unapproved models as operational detectors.')

footer()
