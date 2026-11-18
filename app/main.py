from pathlib import Path
import sys
import streamlit as st

ROOT=Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/'src')); sys.path.insert(0,str(ROOT))
from morphguard.runtime import configure_logging, readiness
from app.components import inject_css, page_header, metric_card, status_badge, empty_state, section_title, load_audit, load_metrics, audit_status

configure_logging()
st.set_page_config(page_title='MorphGuard',page_icon='🛡️',layout='wide',initial_sidebar_state='expanded')
inject_css()
summary,tables,counts=load_audit(); metrics=load_metrics(); ready=readiness(); audit=audit_status(summary,tables,counts)
with st.sidebar:
    st.markdown('<div class="eyebrow">BIOMETRIC SECURITY LAB</div><div class="brand">MORPH<span>GUARD</span></div>',unsafe_allow_html=True)
    st.caption('Facial morphing attack detection research workspace')
    st.divider(); st.markdown('**System mode**')
    st.markdown(status_badge('INFERENCE READY' if ready['ready'] else 'RESEARCH ONLY','ok' if ready['ready'] else 'pending'),unsafe_allow_html=True)
page_header('AI SECURITY RESEARCH / LOCAL','Facial Morphing Attack Detection','A controlled research workspace for auditing, analyzing and preparing biometric morphing detection systems.')
if not ready['ready']:
    st.info('Research-only mode is active. Audited datasets and analysis tools are available; no supervised detector is presented until an approved model artifact exists.')
total=int(counts['count'].sum()) if not counts.empty and 'count' in counts else 0
monot=int(counts.loc[counts.dataset.eq('MONOT'),'count'].sum()) if not counts.empty else 0
onot=int(counts.loc[counts.dataset.eq('ONOT'),'count'].sum()) if not counts.empty else 0
cols=st.columns(4)
for col,label,value,hint in zip(cols,['AUDITED IMAGES','MONOT RECORDS','ONOT RECORDS','MODEL ARTIFACTS'],[f'{total:,}',f'{monot:,}',f'{onot:,}',str(ready['model_count'])],['Full local inventory','Attack/gate source strata','Synthetic mugshot source','Approved artifacts found']):
    with col: metric_card(label,value,hint)
section_title('Dataset intelligence','Loaded from the completed audit under data/metadata; raw folders are not rescanned by the dashboard.')
left,right=st.columns([1.2,1])
with left:
    if not counts.empty:
        chart=counts.assign(series=counts.dataset+' / '+counts.category).set_index('series')['count']
        st.bar_chart(chart,color='#35d1c4',height=300)
    else: empty_state('Audit metadata unavailable',audit['message'])
with right:
    st.markdown('<div class="panel"><h3>Audit status</h3>',unsafe_allow_html=True)
    st.markdown(status_badge(audit['label'],audit['tone']),unsafe_allow_html=True)
    st.write(audit['message'])
    st.write('Cached summaries and inventories are used; a full audit never runs during startup.')
    st.markdown('</div>',unsafe_allow_html=True)
section_title('Research capability map')
capabilities=[('Face preprocessing','TESTED','ok'),('LBP / HOG / GLCM','TESTED','ok'),('Traditional ML interfaces','READY','ok'),('CNN / ResNet18 / EfficientNet','FORWARD PASS TESTED','ok'),('Supervised detector','AWAITING APPROVED LABELS','pending'),('Explainability outputs','MODEL-DEPENDENT','neutral')]
grid=st.columns(3)
for i,(name,state,tone) in enumerate(capabilities):
    with grid[i%3]: st.markdown(f'<div class="panel"><b>{name}</b><br>{status_badge(state,tone)}</div>',unsafe_allow_html=True)
section_title('End-to-end workflow')
st.markdown(' **1. Dataset audit**  →  **2. Preprocessing**  →  **3. Feature extraction**  →  **4. Model development**  →  **5. Evaluation**  →  **6. Inference** ')
section_title('Research status')
if metrics.empty: empty_state('No evaluation results published','No approved supervised label manifest and validated detector are present. This intentional empty state avoids invented metrics.')
else: st.dataframe(metrics,use_container_width=True,hide_index=True)
st.caption('MorphGuard is a local research prototype. Model scores are not calibrated probabilities and outputs are not forensic proof.')
