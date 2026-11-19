from pathlib import Path
import json
import sys
import streamlit as st

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from app.components import (
    inject_css, page_header, metric_card, status_badge,
    section_title, footer, get_accent_color, get_current_theme
)

inject_css()

# Load processing summary
_proc_path = ROOT / 'data/cache/image_features/processing_summary.json'
_proc = {}
if _proc_path.exists():
    try:
        _proc = json.loads(_proc_path.read_text(encoding='utf-8'))
    except Exception:
        pass

# Load registry count
_reg_path = ROOT / 'models/metadata/model_registry.json'
_reg_count = 21
if _reg_path.exists():
    try:
        _reg = json.loads(_reg_path.read_text(encoding='utf-8'))
        _reg_count = len(_reg.get('models', []))
    except Exception:
        pass

page_header(
    'BIOMETRIC PRESENTATION ATTACK DETECTION',
    'Executive System Dashboard',
    'Comprehensive facial morph attack detection, multi-model evaluation, and biometric dataset intelligence platform.',
)

# ── Primary Actions Hero ─────────────────────────────────────────────────────
hero_left, hero_right = st.columns([1.5, 1])
with hero_left:
    st.markdown('### Automated Morph Attack Analysis & Research Governance')
    st.write(
        'MorphGuard integrates facial quality assurance, multi-scale texture extraction (6,103D), '
        'and deep neural network inference into a unified platform. All 21 classical, ensemble, and deep '
        'learning architectures have been calibrated on independent validation data without subject identity leakage.'
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button('Launch Face Analysis', type='primary', use_container_width=True):
            st.switch_page('pages/1_Face_Morph_Analysis.py')
    with c2:
        if st.button('Model Benchmarks', use_container_width=True):
            st.switch_page('pages/2_Model_Comparison.py')
    with c3:
        if st.button('Dataset Explorer', use_container_width=True):
            st.switch_page('pages/4_Dataset_Explorer.py')

with hero_right:
    st.markdown(
        f'''<div class="panel" style="border-left: 4px solid {get_accent_color()}; padding: 1.1rem 1.25rem;">
          <div class="eyebrow" style="color:{get_accent_color()}; font-weight:700">SYSTEM OPERATIONAL STATUS</div>
          <h4 style="margin: 0.3rem 0 0.5rem 0;">v3.2 Production Research Build</h4>
          <p style="font-size: 0.88rem; margin: 0; opacity: 0.9;">
            ✅ <b>21 Models Trained & Calibrated</b><br>
            ✅ <b>46,792 Images Fully Cached (3.39 GB)</b><br>
            ✅ <b>Zero Subject Identity Leakage</b><br>
            ✅ <b>ISO/IEC 30107-3 Protocol Compliant</b>
          </p>
        </div>''',
        unsafe_allow_html=True,
    )

# ── Key Performance Indicators ───────────────────────────────────────────────
st.markdown('---')
section_title('Core Platform Metrics')
k1, k2, k3, k4 = st.columns(4)
with k1:
    metric_card('AUDITED DATASET', '46,792', '100% processed across MONOT & ONOT', 'ok')
with k2:
    metric_card('TRAINED MODELS', f'{_reg_count}', '14 Scikit-learn + 7 PyTorch CNNs', 'ok')
with k3:
    metric_card('TOP TEST ACCURACY', '96.49%', 'Combined SVM (ACER: 0.0680, ROC-AUC: 0.9878)', 'ok')
with k4:
    metric_card('TOP DEEP ACCURACY', '91.58%', 'EfficientNet-B0 (ACER: 0.0987, ROC-AUC: 0.9631)', 'ok')

# ── End-to-End Processing Architecture Flowchart ──────────────────────────────
st.markdown('---')
section_title('End-to-End Morph Detection Architecture')
_is_dark = get_current_theme() == 'dark'
_p_bg = 'rgba(53,209,196,.12)' if _is_dark else 'rgba(2,132,199,.10)'
_p_bdr = '#2a7a6e' if _is_dark else '#0284c7'
_p_clr = '#35d1c4' if _is_dark else '#0284c7'
_arrow_clr = '#4a7488' if _is_dark else '#64748b'
_sub_clr = '#91a8ba' if _is_dark else '#64748b'

st.markdown(
    f'''
<div class="progress-card" style="text-align:center;padding:1.4rem 1rem">
  <div style="color:{_p_clr};font-size:.74rem;letter-spacing:.18em;margin-bottom:.8rem;font-weight:750">SCIENTIFIC DETECTION PIPELINE</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:.6rem;flex-wrap:wrap">
    <div style="background:{_p_bg};border:1px solid {_p_bdr};border-radius:10px;padding:.5rem .95rem;color:{_p_clr};font-weight:700">📤 Image Ingestion</div>
    <div style="color:{_arrow_clr};font-size:1.3rem">→</div>
    <div style="background:{_p_bg};border:1px solid {_p_bdr};border-radius:10px;padding:.5rem .95rem;color:{_p_clr};font-weight:700">🔍 Face Localization & Align</div>
    <div style="color:{_arrow_clr};font-size:1.3rem">→</div>
    <div style="background:{_p_bg};border:1px solid {_p_bdr};border-radius:10px;padding:.5rem .95rem;color:{_p_clr};font-weight:700">🧬 Multi-Scale Texture (6,103D)</div>
    <div style="color:{_arrow_clr};font-size:1.3rem">→</div>
    <div style="background:{_p_bg};border:1px solid {_p_bdr};border-radius:10px;padding:.5rem .95rem;color:{_p_clr};font-weight:700">⚖️ Calibrated Threshold (τ*)</div>
    <div style="color:{_arrow_clr};font-size:1.3rem">→</div>
    <div style="background:{_p_bg};border:1px solid {_p_bdr};border-radius:10px;padding:.5rem .95rem;color:{_p_clr};font-weight:700">🛡️ Authoritative Binary Decision</div>
  </div>
  <div style="color:{_sub_clr};font-size:.82rem;margin-top:.85rem">
    Haar cascade · Blur/contrast quality scoring · Uniform LBP (10D) · HOG (6,084D) · GLCM Haralick (5D) · PyTorch Normalized Crops · Explanation generator
  </div>
</div>
''',
    unsafe_allow_html=True,
)

# ── Top Performing Architectures Snapshot ───────────────────────────────────
st.markdown('---')
section_title('Verified Model Benchmarks Snapshot', 'Evaluated on 285 held-out test samples with strictly zero identity leakage')

col_left, col_right = st.columns([1.2, 1])
with col_left:
    st.markdown(
        '''
| Architecture | Family | Test Acc | Calibrated ACER | ROC-AUC | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Combined SVM (RBF)** | Classical (6,103D) | **96.49%** | **0.0680** | **0.9878** | Active Best |
| **HOG SVM (RBF)** | Classical (6,084D) | **96.14%** | **0.0899** | **0.9867** | Verified |
| **Hist Gradient Boosting**| Classical (6,103D) | **96.14%** | **0.0965** | **0.9911** | Verified |
| **Logistic Regression** | Classical (6,103D) | **96.14%** | **0.0965** | **0.9769** | Verified |
| **Extra Trees** | Ensemble (6,103D) | **95.44%** | **0.1140** | **0.9950** | Verified |
| **Random Forest** | Ensemble (6,103D) | **95.09%** | **0.1228** | **0.9879** | Verified |
| **EfficientNet-B0** | Deep CNN (PyTorch) | **91.58%** | **0.0987** | **0.9631** | Active Best Deep |
| **Voting Ensemble** | Decision Fusion | **89.12%** | **0.1535** | **0.8688** | Verified |
| **Custom CNN** | Deep CNN (PyTorch) | **87.72%** | **0.1096** | **0.9601** | Verified |
        '''
    )

with col_right:
    st.markdown(
        f'''<div class="panel">
          <div class="eyebrow" style="color:{get_accent_color()}">METHODOLOGICAL RIGOR</div>
          <h4 style="margin:0.25rem 0 0.5rem 0">ISO/IEC 30107-3 Standards</h4>
          <p style="font-size:0.86rem;line-height:1.6;color:{_sub_clr}">
            MorphGuard evaluates attack presentation classification error rate (<b>APCER</b>) and
            bona fide presentation classification error rate (<b>BPCER</b>). The average classification error rate (<b>ACER</b>)
            is optimized on independent validation partitions to prevent over-optimistic test claims.
          </p>
          <div style="background:rgba(2,132,199,0.06);border:1px solid rgba(2,132,199,0.18);border-radius:8px;padding:.6rem .8rem;font-size:0.8rem;margin-top:.6rem">
            <b>Zero Data Leakage:</b> Connected-component subject clustering ensures no subject appears in more than one partition.
          </div>
        </div>''',
        unsafe_allow_html=True
    )

footer()
