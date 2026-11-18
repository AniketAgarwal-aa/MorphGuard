import sys
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).parents[2]; sys.path.insert(0,str(ROOT)); from app.components import inject_css,page_header,empty_state
inject_css(); page_header('RESEARCH WORKBENCH','Research Experiments','Experiment registry with explicit status. Only saved results are displayed as results.')
experiments=[('Traditional ML comparison','LBP/HOG/GLCM/combined baselines','Ready to execute','Requires approved manifest'),('Deep-learning comparison','Custom CNN, ResNet18, EfficientNet-B0','Ready to execute','Requires approved manifest and compute budget'),('Image-quality analysis','Blur, brightness, contrast, resolution','Implemented infrastructure','Exploratory dataset analysis'),('MONOT strata','Gate_10, Gate_25, Morphed','Ready to execute','Strata, not automatically classes'),('ONOT acquisition','Digital versus print-scan','Ready to execute','Acquisition analysis only'),('Threshold analysis','ONOT threshold-indexed subsets','Metadata available','Thresholds are not class labels')]
st.dataframe([{'Experiment':a,'Method':b,'Status':c,'Notes':d} for a,b,c,d in experiments],use_container_width=True,hide_index=True)
empty_state('No completed model experiments','No supervised experiment has been executed because no approved reviewed label manifest is present. This page intentionally avoids invented metrics.')
