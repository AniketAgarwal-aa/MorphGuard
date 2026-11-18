import sys
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).parents[2]; sys.path.insert(0,str(ROOT)); from app.components import inject_css,page_header,empty_state
inject_css(); page_header('MODEL INSIGHT','Explainability','Interpretation tools are shown with their evidence boundary; no heatmap is generated without a compatible trained model.')
for title,body,status in [('LBP texture','Local binary patterns summarize micro-texture histograms.','Implemented'),('HOG structure','Gradient orientation bins describe edges and facial structure.','Implemented'),('GLCM texture','Contrast, dissimilarity, homogeneity, energy and correlation summarize spatial texture.','Implemented'),('Feature importance','Tree-based importance and permutation analysis require a fitted model.','Model-dependent'),('Grad-CAM','Influential CNN regions can be visualized for a compatible checkpoint; this is not pixel-level manipulation proof.','Model-dependent')]: st.markdown(f'#### {title}  ·  `{status}`\n{body}')
empty_state('No visual explanation available','Install an approved trained artifact and its metadata to enable image-specific feature importance or Grad-CAM.')
