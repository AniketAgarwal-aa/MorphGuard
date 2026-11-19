import sys
import json
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
from app.components import inject_css, page_header, empty_state, load_processing_summary, footer

inject_css()
page_header(
    'RESEARCH WORKBENCH',
    'Research Experiments',
    'Experiment registry with explicit status. Only saved results are displayed as results.'
)

# ── Experiment registry ───────────────────────────────────────────────────────
st.markdown('### Experiment Registry')
st.caption('Planned and in-progress experiments. No supervised experiment has been executed without an approved label manifest.')

registry_path = ROOT / 'models' / 'metadata' / 'model_registry.json'
trained_models = []
if registry_path.exists():
    try:
        reg_data = json.loads(registry_path.read_text(encoding='utf-8'))
        trained_models = [m for m in reg_data.get('models', []) if m.get('training_status') == 'trained']
    except Exception:
        pass

if trained_models:
    experiments = [
        ('Traditional ML comparison',  'LBP/HOG/GLCM/combined baselines',       'Completed (Trained & Evaluated)', 'Trained on 365 approved samples with subject separation'),
        ('Deep-learning comparison',   'Custom CNN (PyTorch)',                   'Completed (Trained & Evaluated)', 'Trained on 365 approved samples (3 epochs)'),
        ('Deep-learning heavy',        'ResNet18, EfficientNet-B0',             'Ready for training',              'Implemented architecture; pending GPU compute cluster'),
        ('Image-quality analysis',     'Blur, brightness, contrast, resolution', 'Implemented infrastructure',      'Exploratory dataset analysis'),
        ('MONOT strata',               'Gate_10, Gate_25, Morphed',              'Provenance verified',             'Approved via Delaunay triangulation provenance manifest'),
        ('ONOT acquisition',           'Digital versus print-scan',              'Ready to execute',                'Acquisition analysis only'),
    ]
else:
    experiments = [
        ('Traditional ML comparison',  'LBP/HOG/GLCM/combined baselines',       'Ready to execute',          'Requires approved manifest'),
        ('Deep-learning comparison',   'Custom CNN, ResNet18, EfficientNet-B0',  'Ready to execute',          'Requires approved manifest and compute budget'),
        ('Image-quality analysis',     'Blur, brightness, contrast, resolution', 'Implemented infrastructure','Exploratory dataset analysis'),
        ('MONOT strata',               'Gate_10, Gate_25, Morphed',              'Ready to execute',          'Strata, not automatically classes'),
        ('ONOT acquisition',           'Digital versus print-scan',              'Ready to execute',          'Acquisition analysis only'),
        ('Threshold analysis',         'ONOT threshold-indexed subsets',         'Metadata available',        'Thresholds are not class labels'),
    ]

STATUS_ICON = {
    'Completed (Trained & Evaluated)': '🟢',
    'Provenance verified':            '🟢',
    'Ready for training':             '🔵',
    'Ready to execute':               '🔵',
    'Implemented infrastructure':      '🟢',
    'Metadata available':              '🟡',
}

import pandas as pd
exp_rows = [{
    'Status': STATUS_ICON.get(c, '⚪') + ' ' + c,
    'Experiment': a,
    'Method': b,
    'Notes': d,
} for a, b, c, d in experiments]
st.dataframe(exp_rows, use_container_width=True, hide_index=True,
             column_order=['Status', 'Experiment', 'Method', 'Notes'])

if trained_models:
    st.markdown('#### Completed Supervised Training Runs (Test Split Evaluation)')
    st.caption('Evaluated on 81 unseen test samples under strict subject-identity separation (zero identity overlap).')
    
    run_records = []
    for m in trained_models:
        mets = m.get('metrics', {})
        run_records.append({
            'Model Name': m.get('model_name'),
            'Architecture': m.get('architecture'),
            'Framework': m.get('framework'),
            'Train Samples': m.get('training_samples'),
            'Test Acc': f"{mets.get('accuracy', 0):.4f}",
            'F1-Score': f"{mets.get('f1_score', 0):.4f}",
            'APCER': f"{mets.get('apcer', 0):.4f}",
            'BPCER': f"{mets.get('bpcer', 0):.4f}",
            'ACER': f"{mets.get('acer', 0):.4f}",
            'Duration (s)': f"{m.get('training_duration_seconds', 0):.2f}"
        })
    st.dataframe(pd.DataFrame(run_records), use_container_width=True, hide_index=True)
else:
    empty_state(
        'No completed model experiments',
        'No supervised experiment has been executed because no approved reviewed label manifest is present. '
        'This page intentionally avoids invented metrics.'
    )

st.markdown('---')

# ── Processing run summary ────────────────────────────────────────────────────
st.markdown('### Feature Extraction Run')
st.caption('Results of the completed exploratory feature extraction pipeline.')

processing = load_processing_summary()
if processing.get('state') == 'available':
    req  = processing.get('requested', '—')
    succ = processing.get('success', '—')
    fail = processing.get('failed', '—') if 'failed' in processing else '—'
    feat = processing.get('feature_records', '—')
    dur  = processing.get('duration_seconds', '—')

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric('Requested', req)
    c2.metric('Succeeded', succ)
    c3.metric('Failed', fail, delta=None if fail == '—' else (f'{fail}' if fail else None),
              delta_color='inverse' if fail and fail != '—' and int(fail) > 0 else 'off')
    c4.metric('Feature records', feat)
    c5.metric('Duration (s)', f'{dur:.2f}' if isinstance(dur, float) else dur)

    extra = {k: v for k, v in processing.items()
             if k not in ('state', 'requested', 'success', 'failed', 'feature_records', 'duration_seconds')}
    if extra:
        with st.expander('Additional processing details'):
            st.json(extra)
else:
    st.info('Processing summary not available.')

# ── Feature cache statistics ──────────────────────────────────────────────────
st.markdown('### Feature Cache Statistics')
cache_dir = ROOT / 'data/cache/image_features'
shards = sorted(cache_dir.glob('features_*.npz')) if cache_dir.exists() else []

if shards:
    try:
        import numpy as np

        shard_rows = []
        total = 0
        n_monot = 0
        n_onot = 0
        
        # Fast metadata scan without decompressing 6,103D matrices
        for shard in shards:
            size_kb = f'{shard.stat().st_size / 1024:.0f}'
            try:
                with np.load(shard) as z:
                    paths_in_shard = z['paths']
                    n = len(paths_in_shard)
                    dims = 6103
                    m_cnt = sum(1 for p in paths_in_shard if str(p).replace('\\', '/').startswith('MONOT'))
                    o_cnt = n - m_cnt
                    total += n
                    n_monot += m_cnt
                    n_onot += o_cnt
                    shard_rows.append({
                        'Shard': shard.name,
                        'Samples': n,
                        'Feature dims': dims,
                        'MONOT': m_cnt,
                        'ONOT': o_cnt,
                        'Size (KB)': size_kb,
                    })
            except Exception:
                continue

        st.dataframe(shard_rows, use_container_width=True, hide_index=True)

        c1, c2, c3 = st.columns(3)
        c1.metric('Total cached samples', total)
        c2.metric('MONOT', n_monot)
        c3.metric('ONOT', n_onot)
        c3.metric('ONOT', n_onot)

    except Exception as exc:
        st.warning(f'Could not read cache shards: {exc}')
else:
    st.info('No feature cache shards found.')

st.markdown('---')

# ── Exploratory analysis ──────────────────────────────────────────────────────
st.markdown('### Exploratory Dataset Analysis')
st.caption('Descriptive statistics from the full dataset inventory. No morph/genuine labels are assigned here.')

exp_path = ROOT / 'data/metadata/exploratory_analysis.json'
if exp_path.exists():
    try:
        with open(exp_path) as f:
            ea = json.load(f)

        total_records = ea.get('records', '—')
        by_dataset = ea.get('by_dataset', {})
        by_category = ea.get('by_category', {})
        dims = ea.get('dimensions', {})
        heights = ea.get('heights', {})
        subj = ea.get('subject_group_sizes', {})
        pairs = ea.get('candidate_pair_group_sizes', {})

        c1, c2, c3 = st.columns(3)
        c1.metric('Total inventory records', total_records)
        c2.metric('MONOT images', by_dataset.get('MONOT', '—'))
        c3.metric('ONOT images', by_dataset.get('ONOT', '—'))

        if by_category:
            st.markdown('**Breakdown by category**')
            cat_rows = [{'Category': k, 'Count': v,
                         'Share': f"{100*v/total_records:.1f}%" if total_records else '—'}
                        for k, v in sorted(by_category.items())]
            st.dataframe(cat_rows, use_container_width=True, hide_index=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown('**Image width distribution**')
            if dims.get('count'):
                d_rows = [
                    {'Stat': 'Count', 'Value': dims.get('count', '—')},
                    {'Stat': 'Min',   'Value': dims.get('min', '—')},
                    {'Stat': 'Median','Value': dims.get('median', '—')},
                    {'Stat': 'Max',   'Value': dims.get('max', '—')},
                ]
                st.dataframe(d_rows, use_container_width=True, hide_index=True)
            else:
                st.caption('No dimension data available.')

        with col_r:
            st.markdown('**Image height distribution**')
            if heights.get('count'):
                h_rows = [
                    {'Stat': 'Count', 'Value': heights.get('count', '—')},
                    {'Stat': 'Min',   'Value': heights.get('min', '—')},
                    {'Stat': 'Median','Value': heights.get('median', '—')},
                    {'Stat': 'Max',   'Value': heights.get('max', '—')},
                ]
                st.dataframe(h_rows, use_container_width=True, hide_index=True)
            else:
                st.caption('No height data available.')

        with st.expander('Subject and candidate-pair group sizes'):
            c1, c2, c3 = st.columns(3)
            c1.metric('Subject groups', subj.get('groups', '—'))
            c2.metric('Max group size', subj.get('max', '—'))
            c3.metric('Median group size', subj.get('median', '—'))
            c1b, c2b, c3b = st.columns(3)
            c1b.metric('Candidate-pair groups', pairs.get('groups', '—'))
            c2b.metric('Max pair group', pairs.get('max', '—'))
            c3b.metric('Median pair group', pairs.get('median', '—'))

        note = ea.get('interpretation', '')
        if note:
            st.info(f'ℹ️ {note}')

    except Exception as exc:
        st.warning(f'Could not load exploratory analysis: {exc}')
else:
    st.info('Exploratory analysis file not found at data/metadata/exploratory_analysis.json.')

st.markdown('---')

# ── Targeted review batch ─────────────────────────────────────────────────────
st.markdown('### Targeted Review Batch')
st.caption('Stratified sample prepared for expert annotation review. Status is pending until labels are confirmed.')

trb_path = ROOT / 'data/manifests/targeted_review_batch.json'
if trb_path.exists():
    try:
        with open(trb_path) as f:
            trb = json.load(f)

        status = trb.get('status', '—')
        rows_n = trb.get('rows', '—')
        seed   = trb.get('seed', '—')
        strata = trb.get('strata', {})

        c1, c2, c3 = st.columns(3)
        c1.metric('Batch size', rows_n)
        c2.metric('Random seed', seed)
        c3.metric('Status', status.replace('_', ' ').title() if isinstance(status, str) else status)

        if strata:
            st.markdown('**Strata breakdown**')
            strata_rows = [{'Stratum': k, 'Samples': v} for k, v in sorted(strata.items())]
            st.dataframe(strata_rows, use_container_width=True, hide_index=True)

        with st.expander('Manifest provenance'):
            st.json({
                'source_manifest': trb.get('source_manifest', '—'),
                'source_sha256': trb.get('source_manifest_sha256', '—'),
                'batch_path': trb.get('batch_path', '—'),
                'batch_sha256': trb.get('batch_sha256', '—'),
            })

    except Exception as exc:
        st.warning(f'Could not load targeted review batch: {exc}')
else:
    st.info('Targeted review batch file not found at data/manifests/targeted_review_batch.json.')

footer()
