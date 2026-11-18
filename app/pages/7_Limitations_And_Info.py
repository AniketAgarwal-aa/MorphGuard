import sys
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).parents[2]; sys.path.insert(0,str(ROOT)); from app.components import inject_css,page_header,section_title
inject_css(); page_header('GOVERNANCE','Limitations & Project Information','What MorphGuard can claim today, what remains pending, and how to use it responsibly.')
section_title('Current limitations')
st.markdown('- No approved trained detector artifact is installed.\n- MONOT/ONOT combinations are source-confounded unless a reviewed protocol controls for identity and acquisition.\n- Haar-cascade detection is a conservative baseline and can miss difficult poses.\n- Dataset statistics are not evidence of real-world deployment accuracy.\n- Docker image validation remains pending until Docker Desktop’s Linux engine is available.')
section_title('Privacy and licensing')
st.markdown('Uploaded images are processed locally and are not persisted by default. MONOT and ONOT have their own non-commercial dataset terms; do not redistribute the raw datasets. Review licensing and access controls before any hosted biometric processing.')
section_title('Project links')
st.markdown('[Installation](../docs/INSTALLATION.md) · [Scientific protocol](../docs/SCIENTIFIC_VALIDITY_AND_LABEL_PROTOCOL.md) · [Deployment handoff](../docs/FINAL_DEPLOYMENT_HANDOFF.md) · [Label review guide](../docs/LABEL_REVIEW_GUIDE.md)')
