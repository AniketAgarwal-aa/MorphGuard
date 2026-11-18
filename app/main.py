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
    page_title='MorphGuard',
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

# ── 14 Pages organized into the two requested sections ───────────────────────
main_project = [
    st.Page('pages/overview.py', title='Overview', icon=':material/home:'),
    st.Page('pages/1_Face_Morph_Analysis.py', title='Face Analysis', icon=':material/face:'),
    st.Page('pages/4_Dataset_Explorer.py', title='Dataset Explorer', icon=':material/table_view:'),
    st.Page('pages/annotation_review.py', title='Annotation Review', icon=':material/rate_review:'),
    st.Page('pages/2_Model_Comparison.py', title='Model Comparison', icon=':material/compare_arrows:'),
    st.Page('pages/3_Explainability.py', title='Model Insights', icon=':material/visibility:'),
    st.Page('pages/5_Research_Experiments.py', title='Experiments', icon=':material/science:'),
]

about_project = [
    st.Page('pages/about.py', title='About MorphGuard', icon=':material/info:'),
    st.Page('pages/how_it_works.py', title='How It Works', icon=':material/account_tree:'),
    st.Page('pages/datasets.py', title='Datasets', icon=':material/database:'),
    st.Page('pages/models_technology.py', title='Models & Technology', icon=':material/psychology:'),
    st.Page('pages/6_Methodology.py', title='Methodology', icon=':material/schema:'),
    st.Page('pages/7_Limitations_And_Info.py', title='Limitations & Privacy', icon=':material/lock:'),
    st.Page('pages/technical_documentation.py', title='Technical Documentation', icon=':material/description:'),
]

navigation = st.navigation(
    {
        'MAIN PROJECT': main_project,
        'ABOUT PROJECT': about_project,
    },
    position='sidebar',
    expanded=True
)

navigation.run()
