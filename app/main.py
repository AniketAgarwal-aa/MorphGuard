from pathlib import Path
import sys
import streamlit as st

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))

from morphguard.runtime import configure_logging
from app.components import inject_css, render_sidebar_controls

configure_logging()
st.set_page_config(
    page_title='MorphGuard — Biometric Facial Morph Attack Detection',
    page_icon=':shield:',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Initialize theme state if not present
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

inject_css()

# Render persistent sidebar controls (Branding, Version, Theme Toggle, Status)
render_sidebar_controls()

# ── 14 Pages structured into 6 intuitive, logical functional groups ─────────
overview_group = [
    st.Page('pages/overview.py', title='Executive Dashboard', icon=':material/dashboard:'),
    st.Page('pages/about.py', title='About MorphGuard', icon=':material/info:'),
]

analysis_group = [
    st.Page('pages/1_Face_Morph_Analysis.py', title='Face Morph Analysis', icon=':material/biometrics:'),
]

models_eval_group = [
    st.Page('pages/2_Model_Comparison.py', title='Model Benchmark', icon=':material/leaderboard:'),
    st.Page('pages/3_Explainability.py', title='Model Insights', icon=':material/visibility:'),
    st.Page('pages/5_Research_Experiments.py', title='Research Experiments', icon=':material/science:'),
]

data_method_group = [
    st.Page('pages/4_Dataset_Explorer.py', title='Dataset Explorer', icon=':material/dataset:'),
    st.Page('pages/6_Methodology.py', title='Detection Methodology', icon=':material/schema:'),
    st.Page('pages/how_it_works.py', title='System Architecture', icon=':material/account_tree:'),
]

documentation_group = [
    st.Page('pages/models_technology.py', title='Technology Deep Dive', icon=':material/memory:'),
    st.Page('pages/technical_documentation.py', title='Technical Documentation', icon=':material/menu_book:'),
    st.Page('pages/7_Limitations_And_Info.py', title='Limitations & Privacy', icon=':material/policy:'),
]

admin_review_group = [
    st.Page('pages/annotation_review.py', title='Annotation Review', icon=':material/verified_user:'),
    st.Page('pages/datasets.py', title='Dataset Governance', icon=':material/shield:'),
]

navigation = st.navigation(
    {
        'OVERVIEW': overview_group,
        'ANALYSIS': analysis_group,
        'MODELS & BENCHMARKS': models_eval_group,
        'DATA & METHODOLOGY': data_method_group,
        'DOCUMENTATION': documentation_group,
        'GOVERNANCE & REVIEW': admin_review_group,
    },
    position='sidebar',
    expanded=True
)

navigation.run()
