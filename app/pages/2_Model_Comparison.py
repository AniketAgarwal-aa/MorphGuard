import sys
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).parents[2]; sys.path.insert(0,str(ROOT)); from app.components import inject_css,page_header,load_metrics,empty_state
inject_css(); page_header('MODEL LAB','Model Comparison','A transparent registry of implemented architectures and evaluation artifacts. Metrics appear only when saved results exist.')
registry=[('Custom CNN','Deep learning','224×224 RGB','Forward pass tested','Ready'),('ResNet18','Deep learning','224×224 RGB','Forward pass tested','Ready'),('EfficientNet-B0','Deep learning','224×224 RGB','Forward pass tested','Ready'),('LBP + SVM','Traditional ML','LBP histogram','Pipeline ready','Awaiting labels'),('HOG + SVM','Traditional ML','HOG vector','Pipeline ready','Awaiting labels'),('GLCM + RF','Traditional ML','GLCM statistics','Pipeline ready','Awaiting labels'),('Combined + SVM','Traditional ML','Combined features','Pipeline ready','Awaiting labels')]
st.dataframe([{'Model':a,'Family':b,'Representation':c,'Implementation':d,'Status':e} for a,b,c,d,e in registry],use_container_width=True,hide_index=True)
metrics=load_metrics()
if metrics.empty: empty_state('No evaluation artifacts found','The results/metrics directory contains no JSON evaluation outputs. This intentional empty state avoids invented metrics.')
else: st.dataframe(metrics,use_container_width=True,hide_index=True)
