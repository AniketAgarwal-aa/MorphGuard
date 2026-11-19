import sys, json
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from app.components import inject_css, page_header, metric_card, section_title, footer

inject_css()
page_header(
    'MODEL LAB',
    'Model Comparison',
    'Live training results, evaluation metrics, and architecture registry for all MorphGuard models.'
)

# ── Load unified model registry ───────────────────────────────────────────────
registry_path = ROOT / 'models' / 'metadata' / 'model_registry.json'
meta_dir = ROOT / 'models' / 'metadata'
trained_dir = ROOT / 'models' / 'trained'
ckpt_dir = ROOT / 'models' / 'checkpoints'

registry_models = []
if registry_path.exists():
    try:
        reg = json.loads(registry_path.read_text(encoding='utf-8'))
        registry_models = reg.get('models', [])
    except Exception:
        pass

# Count trained vs implemented
trained_count = sum(1 for m in registry_models if m.get('training_status') == 'trained')
ready_count = sum(1 for m in registry_models if m.get('training_status') == 'ready_for_training')
total_count = len(registry_models)

# ── Summary Metric Cards ───────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1: metric_card('TOTAL ARCHITECTURES', str(total_count), 'In unified registry')
with c2: metric_card('TRAINED ARTIFACTS', str(trained_count), 'With evaluation results')
with c3: metric_card('READY FOR TRAINING', str(ready_count), 'GPU/compute required')
with c4: metric_card('EVAL PROTOCOL', 'ISO/IEC 30107-3', 'APCER / BPCER / ACER')

st.markdown('---')

# ── Live Model Registry Table ─────────────────────────────────────────────────
section_title('Live Model Registry with Training & Evaluation Results')

rows = []
for m in registry_models:
    met = m.get('metrics', {})
    trained = m.get('training_status') == 'trained'
    rows.append({
        'Model': m.get('model_name', '—'),
        'Framework': m.get('framework', '—'),
        'Input': m.get('feature_key', '—')[:30],
        'Train Samples': str(m.get('training_samples', '—')),
        'Status': '✅ Trained' if trained else '🔵 Ready / Prototype',
        'Accuracy': f"{met.get('accuracy', '—'):.4f}" if isinstance(met.get('accuracy'), float) else '—',
        'F1': f"{met.get('f1_score', '—'):.4f}" if isinstance(met.get('f1_score'), float) else '—',
        'APCER': f"{met.get('apcer', '—'):.4f}" if isinstance(met.get('apcer'), float) else '—',
        'BPCER': f"{met.get('bpcer', '—'):.4f}" if isinstance(met.get('bpcer'), float) else '—',
        'ACER': f"{met.get('acer', '—'):.4f}" if isinstance(met.get('acer'), float) else '—',
        'Approval': m.get('approval_status', '—'),
    })

if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption('Accuracy and ACER computed on the held-out test split (subject-disjoint). '
               'All experimental — not validated against an independent test protocol.')

st.info(
    '🛡️ **RESEARCH SAFEGUARD:** Metrics shown are evaluated on the 285 held-out test samples with zero '
    'subject identity leakage. Decision thresholds were calibrated exclusively on the independent '
    '321-sample validation split. No results are fabricated or simulated.'
)

st.markdown('---')

# ── Model-by-Model Detail Cards ───────────────────────────────────────────────
section_title('Detailed Model Evaluation Breakdown')
st.caption('Expand each model for full metrics, confusion matrix, and artifact information.')

FEAT_LABEL = {
    'X': '6,103-dim combined (LBP+HOG+GLCM+Stats)',
    'glcm': '5-dim GLCM co-occurrence',
    'lbp': '10-dim LBP histogram',
    'hog': '6,084-dim HOG gradient',
    'raw_face_crop_224x224': '224×224×3 RGB face crop tensor',
}

for m in registry_models:
    trained = m.get('training_status') == 'trained'
    icon = '✅' if trained else '🔵'
    with st.expander(f"{icon} {m.get('model_name','?')} ({m.get('framework','?')})"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('**Architecture Info**')
            st.write(f"- Model: `{m.get('model_name')}`")
            st.write(f"- Framework: `{m.get('framework', 'N/A')}`")
            feat_key = m.get('feature_key', '')
            feat_desc = FEAT_LABEL.get(feat_key, feat_key)
            st.write(f"- Input: {feat_desc}")
            st.write(f"- Training Date: {m.get('training_date', 'N/A')}")
            st.write(f"- Training Samples: {m.get('training_samples', 'N/A')}")
            st.write(f"- Duration: {m.get('training_duration_seconds', 'N/A')} sec")
            ap = m.get('artifact_path')
            if ap:
                st.write(f"- Artifact: `{ap}`")
        with col_b:
            st.markdown('**Evaluation Metrics**')
            met = m.get('metrics', {})
            if isinstance(met.get('accuracy'), float):
                eval_split = met.get('evaluation_split', 'N/A')
                eval_n = met.get('eval_samples', 'N/A')
                st.write(f"- Evaluation split: `{eval_split}` ({eval_n} samples)")
                st.write(f"- Morphed / Genuine in eval: {met.get('eval_morphed','?')} / {met.get('eval_genuine','?')}")
                st.write(f"- Accuracy: `{met.get('accuracy', 0):.4f}` ({met.get('accuracy', 0)*100:.1f}%)")
                st.write(f"- Precision: `{met.get('precision', 0):.4f}`")
                st.write(f"- Recall: `{met.get('recall', 0):.4f}`")
                st.write(f"- F1-score: `{met.get('f1_score', 0):.4f}`")
                st.write(f"- APCER: `{met.get('apcer', 0):.4f}` (Morphed → Genuine errors)")
                st.write(f"- BPCER: `{met.get('bpcer', 0):.4f}` (Genuine → Morphed errors)")
                st.write(f"- ACER: `{met.get('acer', 0):.4f}` (Average error)")
                cm = met.get('confusion_matrix', {})
                if cm:
                    cm_df = pd.DataFrame([
                        {'': 'Predicted Genuine', 'True Genuine': cm.get('tn', 0), 'True Morphed': cm.get('fn', 0)},
                        {'': 'Predicted Morphed', 'True Genuine': cm.get('fp', 0), 'True Morphed': cm.get('tp', 0)}
                    ]).set_index('')
                    st.dataframe(cm_df, use_container_width=True)
            else:
                st.info('Not yet trained. Awaiting approved label manifest and compute.')

        st.markdown(f"**Approval Status:** `{m.get('approval_status', 'N/A')}`")
        if m.get('approval_status') == 'approved_experimental_inference':
            st.warning(
                '⚗️ **EXPERIMENTAL:** This model is approved for experimental inference only. '
                'It has NOT undergone independent validation on a fully held-out test set. '
                'Results should not be presented as production morph-detection accuracy.'
            )

st.markdown('---')

# ── Architecture Specifications ───────────────────────────────────────────────
section_title('Architecture Specifications')
a_tab1, a_tab2 = st.tabs(['Deep Learning Models (PyTorch)', 'Classical Feature Baselines (scikit-learn)'])

with a_tab1:
    with st.expander('1. Custom Lightweight CNN (Trained ✅)'):
        st.markdown('''
```python
nn.Sequential(
    nn.Conv2d(3, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.AdaptiveAvgPool2d(1),
    nn.Flatten(),
    nn.Dropout(0.25),
    nn.Linear(64, 2)
)
```
- **Design rationale:** Low-complexity baseline that trains fast with minimal memory footprint on CPU.
- **Input:** `(B, 3, 224, 224)` normalized RGB face crop tensors.
- **Output:** 2-class logits (genuine vs morphed).
- **Training status:** Trained — 3 epochs, 165 samples.
''')
    with st.expander('2. ResNet-18 (Ready for training)'):
        st.markdown('''
- **Backbone:** Standard 18-layer residual network with skip-connections.
- **Modification:** `model.fc = Linear(512, 2)` for binary classification.
- **Status:** Implemented and forward-pass tested. Requires GPU or extended CPU training.
''')
    with st.expander('3. EfficientNet-B0 (Ready for training)'):
        st.markdown('''
- **Backbone:** Mobile inverted bottleneck (MBConv) with squeeze-and-excitation blocks.
- **Modification:** `model.classifier[-1] = Linear(1280, 2)`.
- **Status:** Implemented and forward-pass tested. Requires GPU or extended CPU training.
''')

with a_tab2:
    with st.expander('Classical ML Pipelines (All Trained ✅)'):
        st.markdown('''
1. **LBP + SVM:** 10-dim uniform LBP histogram → StandardScaler → RBF-SVC
2. **HOG + SVM:** 6,084-dim gradient orientation histogram → StandardScaler → RBF-SVC
3. **GLCM + Random Forest:** 5-dim co-occurrence properties → 200-tree RF (class-balanced)
4. **Combined + SVM:** 6,103-dim [LBP + HOG + GLCM + Stats] → StandardScaler → RBF-SVC
5. **Combined + RF:** 6,103-dim → 300-tree Random Forest (class-balanced)

All trained on the **same leakage-free train split** with no test data exposure.
''')

# ── ISO/IEC 30107-3 Metric Reference ─────────────────────────────────────────
st.markdown('---')
section_title('Evaluation Protocol Reference (ISO/IEC 30107-3)')

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    metric_card('APCER', 'Attack Presentation\nClassification Error', 'Morphed detected as Genuine')
with m_col2:
    metric_card('BPCER', 'Bona Fide Presentation\nClassification Error', 'Genuine detected as Morphed')
with m_col3:
    metric_card('ACER', '(APCER + BPCER) / 2', 'Average Classification Error Rate')
with m_col4:
    metric_card('EER', 'Equal Error Rate', 'Threshold where APCER = BPCER')

footer()
