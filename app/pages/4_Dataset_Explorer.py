import sys, json
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from app.components import (
    inject_css, page_header, load_audit, load_annotation_summary,
    load_processing_summary, metric_card, section_title, audit_status, footer
)

inject_css()
page_header(
    'DATA INTELLIGENCE',
    'Dataset Explorer',
    'Audited distributions and metadata for MONOT and ONOT facial biometric corpora. Manifest-driven.'
)

# ── Load audited manifests and summary ─────────────────────────────────────────
summary, tables, counts = load_audit()
total_images = int(counts['count'].sum()) if not counts.empty else 0
monot_count = int(counts[counts.dataset == 'MONOT']['count'].sum()) if not counts.empty else 0
onot_count = int(counts[counts.dataset == 'ONOT']['count'].sum()) if not counts.empty else 0
corrupted_count = int(summary.get('corrupted_count', 0))
duplicate_count = int(summary.get('duplicate_count', 0))
audit_info = audit_status(summary, tables, counts)

# ── Metric Cards ──────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1: metric_card('TOTAL IMAGES', f'{total_images:,}', 'Verified across 2 datasets')
with c2: metric_card('MONOT DATASET', f'{monot_count:,}', 'Gate & morph strata')
with c3: metric_card('ONOT DATASET', f'{onot_count:,}', 'Digital & print-scan variants')
with c4: metric_card('CORRUPTED / DUPES', f'{corrupted_count} / {duplicate_count}', 'Data integrity check')

st.markdown(f"**Audit Status:** `{audit_info['label']}` — {audit_info['message']}")
st.markdown('---')

# ── Category Distribution & Filter ────────────────────────────────────────────
section_title('Corpus Inventory Breakdown')
st.caption('Category counts loaded from data/metadata/dataset_summary.json. Categories represent acquisition strata and generation parameters, not ground-truth binary labels.')

if not counts.empty:
    chart_df = counts.assign(category_label=counts.dataset + ' / ' + counts.category).set_index('category_label')
    st.bar_chart(chart_df['count'], color='#35d1c4')

    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f1:
        dataset_filter = st.selectbox('Filter by Dataset', ['All'] + sorted(counts.dataset.unique().tolist()))
    with col_f2:
        cat_choices = sorted(counts[counts.dataset == dataset_filter].category.unique().tolist()) if dataset_filter != 'All' else sorted(counts.category.unique().tolist())
        category_filter = st.selectbox('Filter by Category', ['All'] + cat_choices)
    with col_f3:
        search_query = st.text_input('Search Category / Strata', placeholder='e.g. Gate, Morphed, digital')

    visible_counts = counts.copy()
    if dataset_filter != 'All':
        visible_counts = visible_counts[visible_counts.dataset == dataset_filter]
    if category_filter != 'All':
        visible_counts = visible_counts[visible_counts.category == category_filter]
    if search_query:
        sq = search_query.lower()
        visible_counts = visible_counts[
            visible_counts['category'].str.lower().str.contains(sq) |
            visible_counts['dataset'].str.lower().str.contains(sq)
        ]

    st.dataframe(visible_counts, use_container_width=True, hide_index=True)

    csv_data = visible_counts.to_csv(index=False)
    st.download_button(
        '📥 Download Category Breakdown (CSV)',
        csv_data,
        file_name='morphguard_dataset_categories.csv',
        mime='text/csv'
    )

# ── Detailed Inventory Verification ───────────────────────────────────────────
st.markdown('---')
section_title('Dataset Characteristics')

tab_monot, tab_onot, tab_tech = st.tabs(['MONOT Specification', 'ONOT Specification', 'Exploratory Image Metadata'])

with tab_monot:
    st.markdown('''
**MONOT (Morphed and Original National Identification Images Dataset):**
- **Gate_10:** 2,550 images · Live gate camera capture at 10-meter operational distance.
- **Gate_25:** 6,350 images · Live gate camera capture at 25-meter operational distance.
- **Morphed:** 15,240 images · Algorithmic facial morphing attack candidates.
- **Total:** **24,140 images**
- **Morphing algorithms:** Automated landmark-based Delaunay triangulation morphing across designated subject pairs.
- **Filename convention:** Exposes source pair IDs, blending coefficients (B30, B50), warping parameters (W30, W50), and alignment flags.
''')

with tab_onot:
    st.markdown('''
**ONOT (Official National Identity Test Corpus):**
- **digital:** 11,326 images · High-resolution digital passport photo captures compliant with ICAO Doc 9303.
- **print-scan:** 11,326 images · Analog print-and-scan reproductions simulating printed physical travel documents.
- **Total:** **22,652 images**
- **Threshold membership files:** 3 cosine similarity threshold indexing lists (`0.413`, `0.493`, `0.597`) describing subset membership.
- **Scientific guardrail:** Print-scan vs digital variants represent an acquisition dimension, not bona-fide vs attack ground-truth.
''')

with tab_tech:
    ea_path = ROOT / 'data/metadata/exploratory_analysis.json'
    if ea_path.exists():
        try:
            ea = json.loads(ea_path.read_text(encoding='utf-8'))
            dim_col, subj_col = st.columns(2)
            with dim_col:
                st.markdown('**Image Resolution Statistics:**')
                w_info = ea.get('dimensions', {})
                h_info = ea.get('heights', {})
                st.write(f"- Width: Min = {w_info.get('min')}, Median = {w_info.get('median')}, Max = {w_info.get('max')} px")
                st.write(f"- Height: Min = {h_info.get('min')}, Median = {h_info.get('median')}, Max = {h_info.get('max')} px")
            with subj_col:
                st.markdown('**Subject & Pair Clusters:**')
                sg = ea.get('subject_group_sizes', {})
                pg = ea.get('candidate_pair_group_sizes', {})
                st.write(f"- Unique Subject Groups: {sg.get('groups')} (max size: {sg.get('max')})")
                st.write(f"- Candidate Pair Groups: {pg.get('groups')} (max size: {pg.get('max')})")
        except Exception:
            st.caption('Exploratory metadata file parsing unavailable.')

# ── Processing Coverage & Feature Cache Status ────────────────────────────────
st.markdown('---')
section_title('Feature Extraction Cache & Image Processing Coverage')

proc_summary = load_processing_summary()
if proc_summary.get('state') == 'available':
    cached_cnt = int(proc_summary.get('success', 0))
    failed_cnt = int(proc_summary.get('failed', 0))
    pending_cnt = max(0, total_images - cached_cnt)
    cov_pct = (cached_cnt / total_images * 100) if total_images > 0 else 0.0

    p1, p2, p3, p4 = st.columns(4)
    with p1: metric_card('PROCESSED IN CACHE', f'{cached_cnt:,}', 'In data/cache/image_features')
    with p2: metric_card('PENDING IMAGES', f'{pending_cnt:,}', 'Awaiting pipeline execution')
    with p3: metric_card('EXTRACTION ERRORS', str(failed_cnt), 'Corrupted or unreadable')
    with p4: metric_card('FEATURE DIMS', '6,103 dims', 'LBP (10) + HOG (6084) + GLCM (5) + Stats (4)')

    st.progress(min(1.0, cov_pct / 100.0), text=f"Feature cache coverage: {cached_cnt:,} / {total_images:,} images ({cov_pct:.1f}%)")
    st.caption(f'The {cached_cnt:,}-image cached feature shard is immediately accessible for PCA, statistical distribution profiling, and baseline model verification.')

    # Cached strata distribution
    cache_dir = ROOT / 'data/cache/image_features'
    cache_manifest = cache_dir / 'processing_manifest.csv'
    if cache_manifest.exists():
        try:
            m_df = pd.read_csv(cache_manifest)
            if not m_df.empty and 'dataset' in m_df.columns and 'category' in m_df.columns:
                with st.expander('▾ View Cached Feature Strata Distribution'):
                    grp = m_df.groupby(['dataset', 'category']).size().reset_index(name='Cached Count')
                    grp['Share of Cache'] = (grp['Cached Count'] / len(m_df) * 100).map('{:.1f}%'.format)
                    st.dataframe(grp, use_container_width=True, hide_index=True)
        except Exception:
            pass
else:
    st.info('Feature cache summary not yet created. Run scripts/process_images.py to populate.')

# ── Inventory Table Samples ───────────────────────────────────────────────────
st.markdown('---')
section_title('Audited Image Sample Previews')

for name in ('monot_inventory', 'onot_inventory'):
    df = tables.get(name)
    if df is not None and not df.empty:
        with st.expander(f'View {name.replace("_", " ").title()} (first 50 records)'):
            st.dataframe(df.head(50), use_container_width=True, hide_index=True)

footer()
