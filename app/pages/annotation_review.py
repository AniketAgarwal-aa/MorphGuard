import sys, csv, json
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from app.components import inject_css, page_header, metric_card, section_title, footer
from morphguard.dataset.review import read_manifest, review_summary, apply_review

inject_css()
page_header(
    'HUMAN-IN-THE-LOOP',
    'Annotation Review',
    'Evidence-backed review workspace with strict approval safeguards, immutable history, and atomic backups.'
)

manifest = ROOT / 'data/manifests/annotation_inventory.csv'
if not manifest.exists():
    st.error('Annotation inventory manifest is unavailable.')
    st.stop()

# ── Review Scope Selection ────────────────────────────────────────────────────
scope = st.radio(
    'Review Scope',
    ['150-record evidence pilot (Recommended)', 'Full inventory (46,792 records)'],
    horizontal=True,
    help='The 150-record pilot includes pre-extracted image features and provenance assessments for fast targeted review.'
)

# Load data based on scope
pilot_path = ROOT / 'data/review_pilot/annotation_evidence.csv'
processing_path = ROOT / 'data/cache/image_features/processing_manifest.csv'

if scope.startswith('150') and pilot_path.exists():
    with pilot_path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    summary = {
        'records': len(rows),
        'statuses': {'pending_review': sum(1 for r in rows if r.get('review_status') == 'pending_review')},
        'approved_for_training': sum(1 for r in rows if r.get('review_status') == 'approved' and r.get('verified_class') in {'BONA_FIDE', 'MORPHED'})
    }
else:
    rows, fields = read_manifest(manifest)
    summary = review_summary(manifest)

processing = {}
if processing_path.exists():
    with processing_path.open(newline='', encoding='utf-8') as f:
        processing = {r['image_path']: r for r in csv.DictReader(f)}

# ── Summary Metrics ───────────────────────────────────────────────────────────
total_recs = summary['records']
pending_recs = summary['statuses'].get('pending_review', 0)
reviewed_recs = total_recs - pending_recs
approved_recs = summary.get('approved_for_training', 0)

cols = st.columns(4)
with cols[0]: metric_card('TOTAL RECORDS', f'{total_recs:,}', 'Manifest inventory')
with cols[1]: metric_card('PENDING REVIEW', f'{pending_recs:,}', 'Awaiting decision')
with cols[2]: metric_card('REVIEWED', f'{reviewed_recs:,}', 'Completed inspections')
with cols[3]: metric_card('APPROVED FOR TRAINING', f'{approved_recs:,}', 'Eligible ground-truth')

st.progress(reviewed_recs / max(total_recs, 1))
st.caption('Decisions are written atomically with `.bak` backups and logged to `data/manifests/review_history.jsonl`.')

# ── Filters ───────────────────────────────────────────────────────────────────
st.markdown('---')
f1, f2, f3 = st.columns([1, 1, 2])
with f1:
    status_filter = st.selectbox('Filter by Status', ['all', 'pending_review', 'approved', 'rejected', 'insufficient_evidence'])
with f2:
    dataset_filter = st.selectbox('Filter by Dataset', ['all', 'MONOT', 'ONOT'])
with f3:
    query = st.text_input('Search image path, subject ID, or morph pair ID')

filtered = [
    r for r in rows
    if (status_filter == 'all' or r.get('review_status') == status_filter)
    and (dataset_filter == 'all' or r.get('dataset') == dataset_filter)
    and (not query or query.lower() in (' '.join(str(r.get(k, '')) for k in ('image_path', 'subject_id', 'morph_pair_id'))).lower())
]

st.write(f'Showing **{len(filtered):,}** matching records')
if not filtered:
    st.info('No records match these criteria.')
    st.stop()

# ── Record Inspection ─────────────────────────────────────────────────────────
rec_idx = st.number_input('Select Record Number', min_value=1, max_value=len(filtered), value=1) - 1
row = filtered[int(rec_idx)]

section_title(f"Record: {row.get('record_id', row.get('image_path'))}")

# Table of record metadata
rec_meta = [
    {'Field': 'Image Path', 'Value': row.get('image_path', '')},
    {'Field': 'Dataset / Category', 'Value': f"{row.get('dataset', '')} / {row.get('category', '')}"},
    {'Field': 'Subject ID', 'Value': row.get('subject_id', 'None')},
    {'Field': 'Morph Pair ID', 'Value': row.get('morph_pair_id', 'None')},
    {'Field': 'Proposed Interpretation', 'Value': row.get('proposed_interpretation', 'None')},
    {'Field': 'Provenance Reference', 'Value': row.get('provenance_reference', row.get('label_provenance', 'N/A'))},
    {'Field': 'Current Review Status', 'Value': row.get('review_status', 'pending_review')},
    {'Field': 'Eligibility Assessment', 'Value': row.get('eligibility', 'Awaiting assessment')},
]
import pandas as pd
st.dataframe(pd.DataFrame(rec_meta), use_container_width=True, hide_index=True)

# Image preview if file exists
img_file_path = ROOT / row['image_path']
col_img, col_proc = st.columns([1, 1.2])

with col_img:
    if img_file_path.exists():
        st.image(str(img_file_path), caption=f"Preview: {row['image_path']}", use_container_width=True)
    else:
        st.warning('Image binary not mounted in local path. Metadata review remains active.')

with col_proc:
    proc = processing.get(row['image_path'])
    if proc:
        st.markdown('**Existing Preprocessing Metrics (Exploratory Evidence):**')
        st.json({
            'dimensions': f"{proc.get('width')}×{proc.get('height')}",
            'face_detected': proc.get('face_detected'),
            'face_count': proc.get('face_count'),
            'sharpness_blur_var': proc.get('sharpness'),
            'brightness': proc.get('brightness'),
            'contrast': proc.get('contrast'),
            'feature_shard': proc.get('feature_shard')
        })

    if row.get('eligibility') == 'INSUFFICIENT_PROVENANCE':
        st.warning(
            '⚠️ **INSUFFICIENT PROVENANCE:** This image has acquisition and stratum metadata, but lacks '
            'external biometric ground-truth proof. The safeguard policy prevents binary approval.'
        )

# ── Review Decision Form ──────────────────────────────────────────────────────
st.markdown('---')
section_title('Human-in-the-Loop Decision Recording')

with st.form('review_decision_form'):
    reviewer = st.text_input('Reviewer Identity (Required)', value=row.get('reviewer', ''))

    decision_opts = ['pending_review', 'approved', 'rejected', 'insufficient_evidence']
    curr_dec = row.get('review_status', 'pending_review')
    decision = st.selectbox(
        'Review Decision',
        decision_opts,
        index=decision_opts.index(curr_dec) if curr_dec in decision_opts else 0,
        help='Approved requires verified identity, evidence source, and complete notes.'
    )

    class_opts = ['UNKNOWN', 'BONA_FIDE', 'MORPHED']
    curr_class = row.get('verified_class', 'UNKNOWN')
    verified_class = st.selectbox(
        'Verified Ground-Truth Class',
        class_opts,
        index=class_opts.index(curr_class) if curr_class in class_opts else 0
    )

    evidence_source = st.text_input(
        'Evidence Source Document',
        value=row.get('evidence_source', row.get('provenance_reference', ''))
    )

    c_chk1, c_chk2 = st.columns(2)
    with c_chk1:
        id_verified = st.checkbox('Identity verified independently', value=str(row.get('identity_verified', '')).lower() == 'true')
    with c_chk2:
        pair_verified = st.checkbox('Morph pair verified independently', value=str(row.get('pair_verified', '')).lower() == 'true')

    review_notes = st.text_area(
        'Review Notes / Justification',
        value=row.get('review_notes', ''),
        help='State the reasoning behind this decision for audit tracking.'
    )

    submitted = st.form_submit_button('💾 Save Decision to Manifest', type='primary')
    if submitted:
        decision_dict = {
            'review_status': decision,
            'verified_class': verified_class,
            'evidence_source': evidence_source,
            'eligibility': row.get('eligibility', ''),
            'identity_verified': id_verified,
            'pair_verified': pair_verified,
            'review_notes': review_notes
        }
        try:
            target_manifest = manifest
            apply_review(target_manifest, row['image_path'], decision_dict, reviewer)
            st.success(f"✓ Decision recorded successfully for {row['image_path']}. History appended.")
            st.rerun()
        except ValueError as val_err:
            st.error(f'❌ Safeguard Blocked Action: {val_err}')

footer()
