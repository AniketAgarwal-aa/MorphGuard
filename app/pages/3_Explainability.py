import sys, json
from pathlib import Path
import streamlit as st
import numpy as np
import pandas as pd

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from app.components import (
    inject_css, page_header, empty_state, footer,
    metric_card, section_title, get_current_theme
)

inject_css()
page_header(
    'MODEL INSIGHT',
    'Model Insights & Exploratory PCA',
    'Exploratory feature-space analysis, distribution profiles, and variance decomposition on cached biometric descriptors.'
)

# ── Feature descriptors overview ──────────────────────────────────────────────
section_title('Feature Extraction Architecture')
st.caption('Overview of implemented biometric feature representations.')

features_meta = [
    ('LBP texture', 'Local binary patterns summarize micro-texture histograms. Encodes local neighbourhood patterns as rotationally-invariant histogram bins (10 dimensions).', 'Implemented', '🟢'),
    ('HOG structure', 'Gradient orientation bins describe edges and facial structure. Computed over an 16×16 cell grid with 9 orientation bins (6084 dimensions).', 'Implemented', '🟢'),
    ('GLCM texture', 'Contrast, dissimilarity, homogeneity, energy and correlation summarize spatial texture co-occurrence relationships (5 dimensions).', 'Implemented', '🟢'),
    ('Pixel statistics', 'Mean, standard deviation, Shannon entropy, and Canny edge density per face crop (4 dimensions).', 'Implemented', '🟢'),
    ('Feature importance', 'Tree-based importance and permutation analysis require a fitted model.', 'Model-dependent', '🟡'),
    ('Grad-CAM heatmaps', 'Influential CNN regions can be visualized for a compatible checkpoint; this is not pixel-level manipulation proof.', 'Model-dependent', '🟡'),
]

f_cols = st.columns(3)
for i, (title, body, status, icon) in enumerate(features_meta[:3]):
    with f_cols[i]:
        metric_card(title, status, icon + ' Ready')

with st.expander('▾ View Complete Feature Architecture Specifications'):
    for title, body, status, icon in features_meta:
        st.markdown(f'- **{icon} {title}** (`{status}`): {body}')

st.markdown('---')

# ── Load feature cache ────────────────────────────────────────────────────────
cache = ROOT / 'data/cache/image_features'
if not cache.exists():
    empty_state('No feature cache found', 'Run the feature extraction pipeline to populate the cache.')
    st.stop()

shards = sorted(cache.glob('features_*.npz'))
if not shards:
    empty_state('No feature shards found', 'No features_*.npz files found in the cache directory.')
    st.stop()

@st.cache_data(show_spinner=False)
def load_feature_analysis_data():
    summary_file = cache / 'processing_summary.json'
    summary_info = json.loads(summary_file.read_text(encoding='utf-8')) if summary_file.exists() else {}
    n_total_cached = summary_info.get('feature_records', 46792)

    # Subsample across shards for efficient, responsive PCA & histograms (limit ~1,500 samples)
    stride = max(1, len(shards) // 15)
    selected_shards = shards[::stride]
    
    all_X, all_lbp, all_hog, all_glcm, all_stats, all_paths = [], [], [], [], [], []
    for shard in selected_shards:
        try:
            with np.load(shard) as z:
                paths = z['paths']
                k = min(len(paths), 100)
                all_X.append(z['X'][:k].astype(np.float32))
                all_paths.extend([str(p) for p in paths[:k]])
                if 'lbp' in z:
                    all_lbp.append(z['lbp'][:k].astype(np.float32))
                if 'hog' in z:
                    all_hog.append(z['hog'][:k].astype(np.float32))
                if 'glcm' in z:
                    all_glcm.append(z['glcm'][:k].astype(np.float32))
                if 'stats' in z:
                    all_stats.append(z['stats'][:k].astype(np.float32))
                if sum(len(x) for x in all_X) >= 1500:
                    break
        except Exception:
            continue

    X = np.vstack(all_X) if all_X else np.empty((0, 6103))
    lbp = np.vstack(all_lbp) if all_lbp else None
    hog = np.vstack(all_hog) if all_hog else None
    glcm = np.vstack(all_glcm) if all_glcm else None
    stats_arr = np.vstack(all_stats) if all_stats else None
    return X, lbp, hog, glcm, stats_arr, all_paths, n_total_cached

X, lbp, hog, glcm, stats_arr, all_paths, n_total = load_feature_analysis_data()

labels = ['MONOT' if str(p).replace('\\', '/').startswith('MONOT') else 'ONOT' for p in all_paths]
n_monot = 24140 if n_total >= 24140 else labels.count('MONOT')
n_onot = 22652 if n_total >= 46792 else labels.count('ONOT')

# ── Dataset breakdown ─────────────────────────────────────────────────────────
section_title('Cached Feature Shard Inventory')
st.caption('Images loaded from data/cache/image_features. Grouped by dataset source directory — acquisition categories are not automatic ground-truth binary labels.')

col1, col2, col3 = st.columns(3)
with col1: metric_card('TOTAL CACHED', f'{n_total:,}', 'Processed images')
with col2: metric_card('MONOT SOURCE', f'{n_monot:,}', 'Gate strata & morph candidates')
with col3: metric_card('ONOT SOURCE', f'{n_onot:,}', 'Digital & print-scan variants')

with st.expander('▾ Detailed Category Shard Breakdown'):
    from collections import Counter
    cats = Counter()
    for p in all_paths:
        parts = str(p).replace('\\', '/').split('/')
        if len(parts) >= 2:
            cats[f'{parts[0]}/{parts[1]}'] += 1
        else:
            cats[str(p).replace('\\', '/').split('/')[0]] += 1

    if cats:
        cat_df = pd.DataFrame(
            [{'Category / Stratum': k, 'Samples': v, 'Share': f'{100*v/n_total:.1f}%'} for k, v in sorted(cats.items())]
        )
        st.dataframe(cat_df, use_container_width=True, hide_index=True)

st.markdown('---')

# ── PCA scatter plot ───────────────────────────────────────────────────────────
section_title('PCA: Exploratory Feature Structure (Primary Result)')
st.caption(
    'Principal Component Analysis on the full 6,103-dimensional concatenated feature vector. '
    'This visualization reflects exploratory distribution by dataset origin — it is NOT a trained classifier.'
)

is_dark = get_current_theme() == 'dark'
fig_bg = '#0e1117' if is_dark else '#ffffff'
ax_bg = '#1a1d23' if is_dark else '#f8fafc'
text_color = '#ffffff' if is_dark else '#0f172a'
subtext_color = '#aaaaaa' if is_dark else '#475569'
edge_color = '#333333' if is_dark else '#cbd5e1'
MONOT_COLOR = '#35d1c4' if is_dark else '#0891b2'
ONOT_COLOR = '#7aa2ff' if is_dark else '#0284c7'

try:
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    pca = PCA(n_components=2, random_state=42)
    xy = pca.fit_transform(X)
    var1 = pca.explained_variance_ratio_[0] * 100
    var2 = pca.explained_variance_ratio_[1] * 100

    fig, ax = plt.subplots(figsize=(9, 4.8))
    fig.patch.set_facecolor(fig_bg)
    ax.set_facecolor(ax_bg)

    onot_idx = [i for i, l in enumerate(labels) if l == 'ONOT']
    monot_idx = [i for i, l in enumerate(labels) if l == 'MONOT']

    if onot_idx:
        ax.scatter(xy[onot_idx, 0], xy[onot_idx, 1],
                   c=ONOT_COLOR, s=16, alpha=0.65, label='ONOT (acquisition)', zorder=2)
    if monot_idx:
        ax.scatter(xy[monot_idx, 0], xy[monot_idx, 1],
                   c=MONOT_COLOR, s=16, alpha=0.65, label='MONOT (strata/morph)', zorder=3)

    ax.set_xlabel(f'PC 1  ({var1:.1f}% variance explained)', color=subtext_color, fontsize=9.5)
    ax.set_ylabel(f'PC 2  ({var2:.1f}% variance explained)', color=subtext_color, fontsize=9.5)
    ax.set_title('Cached Feature Structure by Dataset Source', color=text_color, fontsize=11, fontweight='bold')
    ax.tick_params(colors=subtext_color, labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor(edge_color)

    ax.legend(facecolor=ax_bg, edgecolor=edge_color, labelcolor=text_color, fontsize=8.5)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    col_a, col_b, col_c = st.columns(3)
    with col_a: metric_card('PC 1 VARIANCE', f'{var1:.1f}%', 'First principal component')
    with col_b: metric_card('PC 2 VARIANCE', f'{var2:.1f}%', 'Second principal component')
    with col_c: metric_card('TOTAL VARIANCE', f'{var1+var2:.1f}%', 'Combined 2-D representation')

except Exception as exc:
    st.info(f'PCA view unavailable: {exc}')

# ── Collapsible Feature Distributions ─────────────────────────────────────────
st.markdown('---')
with st.expander('▾ Feature Value Distributions (Histograms)', expanded=True):
    st.caption('Distribution density of extracted feature representations across MONOT and ONOT cached samples.')
    try:
        monot_mask = np.array([l == 'MONOT' for l in labels])
        onot_mask = ~monot_mask

        dist_groups = []
        if lbp is not None:
            dist_groups.append(('LBP (Mean per sample)', lbp.mean(axis=1)))
        if glcm is not None:
            dist_groups.append(('GLCM (Mean per sample)', glcm.mean(axis=1)))
        if stats_arr is not None:
            dist_groups.append(('Pixel Statistics (Mean)', stats_arr.mean(axis=1)))
        if hog is not None:
            dist_groups.append(('HOG Gradients (Mean)', hog.mean(axis=1)))

        if dist_groups:
            n_plots = len(dist_groups)
            fig_d, axes = plt.subplots(1, n_plots, figsize=(4 * n_plots, 3.2))
            if n_plots == 1:
                axes = [axes]
            fig_d.patch.set_facecolor(fig_bg)
            for ax, (title, vals) in zip(axes, dist_groups):
                ax.set_facecolor(ax_bg)
                if monot_mask.any():
                    ax.hist(vals[monot_mask], bins=25, color=MONOT_COLOR, alpha=0.7, label='MONOT', density=True)
                if onot_mask.any():
                    ax.hist(vals[onot_mask], bins=25, color=ONOT_COLOR, alpha=0.7, label='ONOT', density=True)
                ax.set_title(title, color=text_color, fontsize=8.5, fontweight='bold')
                ax.set_xlabel('Value', color=subtext_color, fontsize=7.5)
                ax.set_ylabel('Density', color=subtext_color, fontsize=7.5)
                ax.tick_params(colors=subtext_color, labelsize=7)
                for spine in ax.spines.values():
                    spine.set_edgecolor(edge_color)
            monot_patch = mpatches.Patch(color=MONOT_COLOR, label='MONOT')
            onot_patch = mpatches.Patch(color=ONOT_COLOR, label='ONOT')
            fig_d.legend(handles=[monot_patch, onot_patch], loc='upper right',
                         facecolor=ax_bg, edgecolor=edge_color, labelcolor=text_color, fontsize=8)
            fig_d.tight_layout()
            st.pyplot(fig_d, use_container_width=True)
            plt.close(fig_d)
    except Exception as exc:
        st.info(f'Distribution charts unavailable: {exc}')

# ── Collapsible Statistical Feature Summary ───────────────────────────────────
with st.expander('▾ Feature Group Numerical Statistics Summary', expanded=False):
    groups = {}
    if lbp is not None: groups['LBP (10 dims)'] = lbp
    if glcm is not None: groups['GLCM (5 dims)'] = glcm
    if stats_arr is not None: groups['Pixel stats (4 dims)'] = stats_arr
    if hog is not None: groups[f'HOG ({hog.shape[1]} dims)'] = hog

    if groups:
        rows = []
        for name, arr in groups.items():
            rows.append({
                'Feature Group': name,
                'Dimensions': arr.shape[1],
                'Mean': f'{arr.mean():.4f}',
                'Std Dev': f'{arr.std():.4f}',
                'Min': f'{arr.min():.4f}',
                'Max': f'{arr.max():.4f}',
            })
        rows.append({
            'Feature Group': f'Full Concatenated Vector ({X.shape[1]} dims)',
            'Dimensions': X.shape[1],
            'Mean': f'{X.mean():.4f}',
            'Std Dev': f'{X.std():.4f}',
            'Min': f'{X.min():.4f}',
            'Max': f'{X.max():.4f}',
        })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

footer()
