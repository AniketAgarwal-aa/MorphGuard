import sys, os
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).parents[2]; sys.path.insert(0,str(ROOT/'src')); sys.path.insert(0,str(ROOT))
from morphguard.inference import InferenceService, load_joblib_model
from morphguard.preprocessing import FacePreprocessor
from app.components import inject_css, page_header, section_title, empty_state
inject_css(); page_header('LIVE ANALYSIS','Face Morph Analysis','Validate a single image locally. No upload is stored, and no binary prediction is shown without an approved model.')
with st.sidebar:
    st.markdown('### Analysis controls'); st.caption('Supported: JPG, JPEG, PNG · local processing only')
uploaded=st.file_uploader('Drop a facial image here',type=['jpg','jpeg','png'])
model_files=sorted((ROOT/'models'/'trained').glob('*.joblib')); selected=st.selectbox('Detection model', ['No approved model available']+[p.name for p in model_files])
if uploaded:
    limit=int(float(os.getenv('MORPHGUARD_MAX_UPLOAD_MB','10'))*1024*1024)
    if uploaded.size>limit: st.error(f'Upload exceeds the configured {limit/1024/1024:.0f} MB limit.'); st.stop()
    col1,col2=st.columns([1.1,1]);
    with col1:
        st.image(uploaded,caption=f'{uploaded.name} · {uploaded.size/1024:.1f} KB',use_container_width=True)
    model=None
    if selected != 'No approved model available':
        try: model=load_joblib_model(ROOT/'models'/'trained'/selected)
        except Exception as exc: st.error(f'Model could not be loaded safely: {exc}')
    result=InferenceService(model=model).analyse(uploaded)
    with col2:
        state=result.get('state','UNKNOWN'); st.markdown(f'## {state}')
        if state=='MODEL UNAVAILABLE': st.info('Research-only mode: image validation, face detection and quality assessment are available, but a validated detector is not installed.')
        if 'quality' in result:
            q=result['quality']; st.metric('Blur variance',f"{q['blur_variance']:.1f}"); st.metric('Brightness',f"{q['brightness']:.1f}"); st.metric('Contrast',f"{q['contrast']:.1f}")
            if q['warnings']: st.warning(' · '.join(q['warnings']))
        if 'face_count' in result: st.caption(f"Faces detected: {result['face_count']} · Processing: {result.get('processing_seconds',0):.3f}s")
    if 'image' in result:
        section_title('Detected face crop'); st.image(result['image'],width=280)
else:
    empty_state('Ready for a local image','Upload a JPG, JPEG or PNG to run validation, face detection and quality checks. The detector remains intentionally unavailable until an approved artifact exists.')
