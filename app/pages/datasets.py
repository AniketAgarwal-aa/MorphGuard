import sys
from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from app.components import (
    inject_css, page_header, load_audit, load_annotation_summary,
    metric_card, section_title, audit_status, footer
)

inject_css()
page_header(
    'DATASETS',
    'Datasets & Biometric Corpora',
    'Audited distributions and scientific characterization of the MONOT and ONOT datasets.'
)

summary, tables, counts = load_audit()
audit = audit_status(summary, tables, counts)

total = int(counts['count'].sum()) if not counts.empty else 0
monot = int(counts[counts.dataset == 'MONOT']['count'].sum()) if not counts.empty else 0
onot = int(counts[counts.dataset == 'ONOT']['count'].sum()) if not counts.empty else 0

# ── Summary metrics ───────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1: metric_card('TOTAL IMAGES', f'{total:,}', 'Audited local corpus')
with c2: metric_card('MONOT CORPUS', f'{monot:,}', 'Gate strata & morphed attacks')
with c3: metric_card('ONOT CORPUS', f'{onot:,}', 'Digital & print-scan variants')

st.markdown('---')

# ── Category distribution ─────────────────────────────────────────────────────
section_title('Corpus Inventory Breakdown')
if not counts.empty:
    chart_series = counts.assign(series=counts.dataset + ' / ' + counts.category).set_index('series')['count']
    st.bar_chart(chart_series, color='#35d1c4')
    st.dataframe(counts, use_container_width=True, hide_index=True)

# ── Dataset Descriptions ──────────────────────────────────────────────────────
st.markdown('---')
section_title('Dataset Specifications')

col_m, col_o = st.columns(2)

with col_m:
    st.markdown('''
#### MONOT Dataset (24,140 Images)
- **Gate_10 (2,550 images):** Live automated border control gate capture at 10-meter operational distance.
- **Gate_25 (6,350 images):** Live automated border control gate capture at 25-meter operational distance.
- **Morphed (15,240 images):** Algorithmic morph attacks generated from verified source subject pairs.
- **Key Observation:** Gate_10 and Gate_25 represent operational acquisition strata, not attack classes.
''')

with col_o:
    st.markdown('''
#### ONOT Dataset (22,652 Images)
- **digital (11,326 images):** High-quality direct digital passport photographs compliant with ICAO Doc 9303.
- **print-scan (11,326 images):** Digitally reprinted and scanned versions exhibiting analog halftoning and scanner noise.
- **Threshold membership:** Contains three cosine similarity threshold subset lists (0.413, 0.493, 0.597).
- **Key Observation:** Digital vs print-scan represents medium variations, not bona-fide vs attack ground-truth.
''')

# ── Scientific Limitations & Confounders ──────────────────────────────────────
st.markdown('---')
section_title('Data Limitations & Confounders')
st.markdown('''
1. **Source Confounding:** MONOT and ONOT originate from different camera pipelines, compression histories, and demographic cohorts. Comparing MONOT against ONOT directly causes cross-dataset confounding rather than pure morph detection.
2. **Stratum vs Label:** Category names such as `Gate_10` or `print-scan` indicate acquisition circumstances, not binary morph ground-truth.
3. **Leakage Prevention:** Training splits must strictly isolate subject IDs and morph-pair IDs across training, validation, and testing sets to prevent identity leakage.
''')

st.caption(f"Audit verification: **{audit['label']}** — {audit['message']}")

# ── Annotation Readiness ──────────────────────────────────────────────────────
annotations = load_annotation_summary()
with st.expander('Ground-Truth Annotation Readiness Status', expanded=True):
    if annotations.get('state') == 'available':
        st.write(
            f"**{annotations.get('records', 0):,}** records inventoried. "
            f"**{annotations.get('approved_for_training', 0):,}** records approved for supervised training."
        )
        st.info(
            'All records currently require human-in-the-loop review. Proposed interpretations from '
            'filenames are provenance evidence only, not confirmed ground-truth labels.'
        )
    else:
        st.warning(annotations.get('message', 'Annotation status unavailable.'))

footer()
