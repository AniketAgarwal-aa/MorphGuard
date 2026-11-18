import sys
from pathlib import Path
import streamlit as st
ROOT = Path(__file__).parents[2]; sys.path.insert(0, str(ROOT))
from app.components import inject_css, page_header, section_title, footer

inject_css()
page_header(
    'GOVERNANCE',
    'Limitations & Project Information',
    'What MorphGuard can claim today, what remains pending, and how to use it responsibly.',
)

# ── Current limitations ───────────────────────────────────────────────────────
section_title('Current limitations')
st.markdown(
    '''
**Detection model**
- No approved, trained morphing-attack detector artifact is currently installed.
  The application will not output a morph/bona-fide classification until a validated
  model is provided and reviewed.

**Dataset confounds**
- MONOT and ONOT images differ in acquisition device, compression pipeline and
  demographic distribution. MONOT/ONOT label comparisons are therefore
  source-confounded unless a carefully controlled experimental protocol accounts
  for identity, session and acquisition variables.
- Dataset statistics displayed in MorphGuard describe the local corpus only; they
  are **not** evidence of real-world deployment accuracy.

**Face detection**
- Haar-cascade face detection is used as a conservative, dependency-free baseline.
  It can miss faces in non-frontal poses, low-lighting conditions, or when faces
  are partially occluded. A more robust MTCNN or RetinaFace detector would reduce
  missed-detection rates but requires additional validated dependencies.

**Image quality**
- Quality thresholds (blur, brightness, contrast) are heuristic. Edge cases—studio
  lighting with deliberate shallow depth-of-field, for example—can be incorrectly
  flagged as unsuitable.

**Containerisation**
- Docker image validation and reproducibility testing remain pending until Docker
  Desktop's Linux engine is confirmed available in the target environment.

**Privacy**
- Uploaded images are processed entirely in-process and are **not** persisted to
  disk beyond the duration of the Streamlit session. No data leaves the local machine.
  However, the application has not been subject to a formal privacy impact assessment
  and **must not** be used to process images of real individuals outside the terms of
  the dataset licence agreements or applicable data-protection law.

**Scalability**
- The application is designed for local, single-user research use. It has not been
  load-tested or hardened for multi-user or internet-facing deployment.
'''
)

# ── Privacy and licensing ─────────────────────────────────────────────────────
section_title('Privacy and licensing')
st.markdown(
    '''
Uploaded images are processed locally and are not persisted by default.

**Dataset licences:**
MONOT and ONOT are distributed under non-commercial research licences.
Do not redistribute the raw image data or use it for commercial model training
without explicit written permission from the dataset custodians.

**Review before hosting:**
Any deployment that processes biometric data beyond a local research workstation
requires a data-protection impact assessment, appropriate legal basis for processing,
and security controls consistent with the sensitivity of the data.
'''
)
st.warning(
    'MorphGuard is a **research prototype**. It is not validated for operational '
    'biometric screening and must not be used as a decision-making system in any '
    'access-control, identity-verification, or law-enforcement context.',
    icon='⚠️',
)

# ── Project documentation ─────────────────────────────────────────────────────
section_title('Project documentation')
st.markdown(
    'The following documents are stored in the `docs/` directory of the project repository. '
    'Open them from the file system or your code editor.'
)
docs = [
    ('INSTALLATION.md',                        'Environment setup and dependency installation'),
    ('SCIENTIFIC_VALIDITY_AND_LABEL_PROTOCOL.md', 'Scientific validity statement and label protocol'),
    ('FINAL_DEPLOYMENT_HANDOFF.md',            'Deployment handoff checklist and requirements'),
    ('LABEL_REVIEW_GUIDE.md',                  'Guide for reviewing and correcting dataset labels'),
]
for filename, description in docs:
    st.markdown(
        f'<div class="panel" style="padding:.7rem 1rem;margin:.3rem 0">'
        f'<code style="color:#6de3d8">{filename}</code>'
        f'<span style="color:#9bb0c2;margin-left:.8rem;font-size:.88rem">{description}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
st.caption('To open: navigate to docs/ in your terminal or file explorer relative to the project root.')

footer()
