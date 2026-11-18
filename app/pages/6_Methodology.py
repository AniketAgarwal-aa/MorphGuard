import sys
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).parents[2]; sys.path.insert(0,str(ROOT)); from app.components import inject_css,page_header,section_title
inject_css(); page_header('METHOD / GOVERNANCE','Methodology & Limitations','A compact view of how MorphGuard moves from audited data to safe local inference.')
section_title('Processing architecture')
st.markdown('''```text
MONOT / ONOT audit outputs
          ↓
validation → face detection → quality assessment → crop/resize
          ↓
LBP / HOG / GLCM / statistics or CNN input
          ↓
reviewed-label training → validation → held-out evaluation
          ↓
portable inference service → explicit result state
```''')
st.markdown('### Scientific guardrails')
st.markdown('- Only MONOT and ONOT are in scope.\n- ONOT threshold files describe subset membership, not class labels.\n- Identity and morph-pair leakage must be blocked before supervised training.\n- Source-confounded MONOT-vs-ONOT experiments cannot be presented as real-world generalization.\n- A model score is not a calibrated probability unless calibration is independently validated.')
st.markdown('### Privacy and deployment')
st.markdown('Uploads are processed locally and are not persisted by default. The Docker runtime excludes raw datasets and runs with inference-only dependencies. Public hosting requires HTTPS, authentication, licensing and biometric privacy review.')
