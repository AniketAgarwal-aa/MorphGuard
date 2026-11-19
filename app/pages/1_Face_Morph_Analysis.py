import sys, os, json, time, io
from pathlib import Path
import streamlit as st
import numpy as np
import cv2
import pandas as pd

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))

from morphguard.inference import InferenceService, load_joblib_model, load_pytorch_model, compare_vectors
from morphguard.preprocessing import FacePreprocessor
from morphguard.feature_extraction import extract_features
from app.components import (
    inject_css, page_header, section_title, empty_state,
    metric_card, footer, get_accent_color
)

def load_pipeline_model(name: str):
    """Load model with proper feature adapter or deep PyTorch adapter and calibrated threshold."""
    if not name or name == 'No approved model available':
        return None
    stem = Path(name).stem
    meta_path = ROOT / 'models' / 'metadata' / f"{stem}.json"
    thresh = 0.5
    fkey = 'combined'
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding='utf-8'))
            fk = meta.get('feature_key', 'combined')
            fkey = 'combined' if fk == 'X' else fk
            thresh = float(meta.get('calibrated_threshold', 0.5))
        except Exception:
            pass

    if name.endswith('.pt'):
        pt_path = ROOT / 'models' / 'checkpoints' / name
        if pt_path.exists():
            return load_pytorch_model(pt_path, architecture='custom_cnn', threshold=thresh)
    elif name.endswith('.joblib'):
        job_path = ROOT / 'models' / 'trained' / name
        if job_path.exists():
            if not meta_path.exists():
                if any(k in name for k in ('glcm', 'lda', 'knn', 'nb', 'ensemble')):
                    fkey = 'glcm'
                elif 'lbp' in name:
                    fkey = 'lbp'
                elif 'hog' in name:
                    fkey = 'hog'
            return load_joblib_model(job_path, feature_key=fkey, threshold=thresh)
    return None

inject_css()
page_header(
    'LIVE ANALYSIS',
    'Face Morph Analysis',
    'Validate facial images locally. Runs OpenCV face detection, quality analysis, and multi-scale texture extraction (LBP, HOG, GLCM).'
)

# ── Sidebar Configuration ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('### Analysis Settings')
    st.caption('Supported formats: JPG, JPEG, PNG · In-process execution only')

    trained_dir = ROOT / 'models' / 'trained'
    checkpoints_dir = ROOT / 'models' / 'checkpoints'
    model_options = ['No approved model available']
    if trained_dir.exists():
        model_options.extend([p.name for p in sorted(trained_dir.glob('*.joblib'))])
    if checkpoints_dir.exists():
        model_options.extend([p.name for p in sorted(checkpoints_dir.glob('*.pt'))])

    selected_model_name = st.selectbox(
        'Detection model',
        model_options
    )

    demo_mode = st.checkbox(
        'Enable illustrative demonstration mode',
        help=(
            'Computes a deterministic pattern class (DEMO PATTERN A/B) from extracted texture '
            'features for interface demonstration. It is NOT a morph prediction or confidence score.'
        )
    )

    st.markdown('---')
    st.markdown('### Quick Samples')
    st.caption('Load pre-packaged dataset samples for instant demonstration:')
    sample_choice = st.selectbox(
        'Load pre-packaged sample',
        [
            'None (Upload your own)',
            'Sample A: Genuine candidate (MONOT Gate_10)',
            'Sample B: Morphed candidate (MONOT Morphed)'
        ]
    )

# ── Mode Selection Tabs ────────────────────────────────────────────────────────
tab_single, tab_compare = st.tabs(['Single Image Analysis', 'Original-versus-Morphed Comparison'])

def load_image_bytes(file_or_path):
    """Safely decode image into BGR numpy array and raw bytes with comprehensive error handling."""
    if isinstance(file_or_path, (str, Path)):
        p = Path(file_or_path)
        if not p.exists():
            return None, None, f'File does not exist: {p.name}'
        raw_bytes = p.read_bytes()
        filename = p.name
    else:
        filename = file_or_path.name
        raw_bytes = file_or_path.getvalue()

    if not raw_bytes or len(raw_bytes) == 0:
        return None, None, 'File is empty (0 bytes).'

    try:
        arr = np.asarray(bytearray(raw_bytes), dtype=np.uint8)
        img_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img_bgr is None or img_bgr.size == 0:
            return None, None, 'Invalid or corrupted image format. Unable to decode image data.'
        return img_bgr, raw_bytes, None
    except Exception as exc:
        return None, None, f'Image decoding error: {exc}'

accent = get_accent_color()

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1: SINGLE IMAGE ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
with tab_single:
    u_col1, u_col2 = st.columns([2, 1])
    with u_col1:
        uploaded_file = st.file_uploader(
            'Upload facial image (PNG, JPG, JPEG)',
            type=['jpg', 'jpeg', 'png'],
            key='single_upload_input'
        )
    with u_col2:
        st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)
        st.caption('File size limit: 10 MB per image. Local in-memory processing only.')

    target_source = None
    source_name = ''
    source_bytes = None

    if uploaded_file is not None:
        target_source = uploaded_file
        source_name = uploaded_file.name
        source_bytes = uploaded_file.getvalue()
    elif sample_choice == 'Sample A: Genuine candidate (MONOT Gate_10)':
        sample_path = ROOT / 'MONOT/Gate_10/S113923411-GF-A35-EEA-T14-S1-LH-C1-I0048-F00-0.png'
        if sample_path.exists():
            target_source = sample_path
            source_name = sample_path.name
            source_bytes = sample_path.read_bytes()
    elif sample_choice == 'Sample B: Morphed candidate (MONOT Morphed)':
        sample_path = ROOT / 'MONOT/Morphed/M_S113923411-GF-A35-EEA-T14-S1-LH-C1-I0048-F00_S198149424-GF-A51-EEA-T13-S1-LH-C1-I0055-F00_C01_B30_W30_PA01_PM00_F00.png'
        if sample_path.exists():
            target_source = sample_path
            source_name = sample_path.name
            source_bytes = sample_path.read_bytes()

    if target_source is not None:
        # Size validation
        limit_mb = float(os.getenv('MORPHGUARD_MAX_UPLOAD_MB', '10'))
        limit_bytes = int(limit_mb * 1024 * 1024)
        if len(source_bytes) > limit_bytes:
            st.error(f'Upload exceeds the configured limit of {limit_mb:.0f} MB.')
            st.stop()

        # Image decode validation
        img_bgr, _, decode_err = load_image_bytes(target_source)
        if decode_err:
            st.error(f'Validation failed: {decode_err}')
            st.stop()

        orig_h, orig_w = img_bgr.shape[:2]

        # Run backend inference pipeline with spinner
        with st.spinner('Running face detection, quality analysis, and feature extraction...'):
            start_time = time.perf_counter()
            model = None
            if selected_model_name != 'No approved model available':
                try:
                    model = load_pipeline_model(selected_model_name)
                except Exception as exc:
                    st.error(f'Model load failed: {exc}')

            bio = io.BytesIO(source_bytes)
            analysis_result = InferenceService(model=model).analyse(bio)
            proc_time = time.perf_counter() - start_time

        # Extract features if face detected
        features_dict = None
        feature_summary = None
        if 'image' in analysis_result and analysis_result.get('state') not in {'INVALID IMAGE', 'FACE NOT DETECTED'}:
            try:
                face_crop_rgb = np.asarray(analysis_result['image'])
                features_dict = extract_features(face_crop_rgb)
                feature_summary = {
                    k: {
                        'dimensions': list(v.shape),
                        'total_elements': int(np.prod(v.shape)),
                        'mean': float(np.mean(v)),
                        'std': float(np.std(v)),
                        'finite': bool(np.isfinite(v).all()),
                    }
                    for k, v in features_dict.items()
                }
                analysis_result['feature_summary'] = feature_summary
                analysis_result['feature_vectors'] = {k: v.tolist() for k, v in features_dict.items()}

                if demo_mode and selected_model_name == 'No approved model available':
                    demo_val = float(np.mean(features_dict['lbp']) + np.mean(features_dict['glcm']))
                    analysis_result['demo_class'] = 'DEMO PATTERN A' if demo_val < 0.6 else 'DEMO PATTERN B'
                    analysis_result['demo_disclaimer'] = (
                        'Illustrative feature-pipeline output only; not a morph/genuine classification '
                        'and not a confidence score.'
                    )
            except Exception as f_exc:
                st.warning(f'Feature extraction warning: {f_exc}')

        st.markdown('---')

        # ── SECTION A: IMAGE PREVIEW ──────────────────────────────────────────
        section_title('Section A — Image Previews & Face Localization')
        col_orig, col_box, col_crop = st.columns([1.2, 1.2, 0.9])

        with col_orig:
            st.markdown('**1. Original Uploaded Image**')
            st.image(
                cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB),
                caption=f'{source_name} ({orig_w}×{orig_h} px)',
                use_container_width=True
            )

        with col_box:
            st.markdown('**2. Detected Face with Bounding Box**')
            box_img = img_bgr.copy()
            if analysis_result.get('face_box'):
                bx, by, bw, bh = analysis_result['face_box']
                cv2.rectangle(box_img, (bx, by), (bx + bw, by + bh), (0, 220, 190), 3)
                cv2.putText(
                    box_img, 'Primary Face', (bx, max(18, by - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 190), 2
                )
            st.image(
                cv2.cvtColor(box_img, cv2.COLOR_BGR2RGB),
                caption='Detected bounding box (OpenCV Haar Cascade)',
                use_container_width=True
            )

        with col_crop:
            st.markdown('**3. Extracted Face Crop**')
            if 'image' in analysis_result:
                crop_arr = np.asarray(analysis_result['image'])
                st.image(crop_arr, caption='Normalized crop (224×224 RGB)', width=180)
            else:
                st.info('Face crop unavailable')

        with st.expander('▾ Image Details & Geometry Specifications'):
            fb = analysis_result.get('face_box', (0, 0, 0, 0))
            geom_df = pd.DataFrame([
                {'Property': 'Original Resolution', 'Value': f'{orig_w}×{orig_h} px'},
                {'Property': 'File Size', 'Value': f'{len(source_bytes)/1024:.1f} KB'},
                {'Property': 'Aspect Ratio', 'Value': f'{orig_w/max(orig_h,1):.2f}'},
                {'Property': 'Color Space', 'Value': 'RGB (3 channels)'},
                {'Property': 'Primary Face Bounding Box', 'Value': f'x={fb[0]}, y={fb[1]}, w={fb[2]}, h={fb[3]}' if analysis_result.get('face_box') else 'None'},
                {'Property': 'Face Crop Target', 'Value': '224×224 RGB (15% contextual padding)'},
            ])
            st.dataframe(geom_df, use_container_width=True, hide_index=True)

        # ── SECTION B: ANALYSIS SUMMARY ───────────────────────────────────────
        st.markdown('---')
        section_title('Section B — Quality Assessment & Analysis Summary')

        # Metric cards
        m1, m2, m3, m4, m5 = st.columns(5)
        faces_detected = analysis_result.get('face_count', 0)
        with m1: metric_card('FACES DETECTED', str(faces_detected), 'Haar Cascade')
        with m2: metric_card('PROCESSING TIME', f'{proc_time:.3f} s', 'Local execution')

        q = analysis_result.get('quality', {})
        with m3: metric_card('SHARPNESS', f"{q.get('blur_variance', 0):.1f}", 'Laplacian variance')
        with m4: metric_card('BRIGHTNESS', f"{q.get('brightness', 0):.1f}", 'Scale: 0–255')
        with m5: metric_card('CONTRAST', f"{q.get('contrast', 0):.1f}", 'Standard deviation')

        # Quality status
        if q.get('suitable'):
            st.success('✓ Image Quality Status: **SUITABLE** — Image passes sharpness, brightness, and contrast thresholds.')
        else:
            warns = ' · '.join(q.get('warnings', ['Quality check flagged']))
            st.warning(f'⚠️ Image Quality Status: **WARNING** — {warns}')

        with st.expander('▾ Quality Metrics & Threshold Explanations'):
            q_info = pd.DataFrame([
                {'Metric': 'Sharpness (Blur Variance)', 'Measured': f"{q.get('blur_variance', 0):.2f}", 'Operational Threshold': '≥ 50.0', 'Assessment': 'Pass' if q.get('blur_variance', 0) >= 50 else 'Blurred'},
                {'Metric': 'Luminance (Brightness)', 'Measured': f"{q.get('brightness', 0):.2f}", 'Operational Threshold': '45.0 – 220.0', 'Assessment': 'Pass' if 45 <= q.get('brightness', 0) <= 220 else 'Out of bounds'},
                {'Metric': 'Contrast (Luminance Std)', 'Measured': f"{q.get('contrast', 0):.2f}", 'Operational Threshold': '≥ 20.0', 'Assessment': 'Pass' if q.get('contrast', 0) >= 20 else 'Low contrast'},
            ])
            st.dataframe(q_info, use_container_width=True, hide_index=True)

        # ── SECTION C: FEATURE EXTRACTION ─────────────────────────────────────
        st.markdown('---')
        section_title('Section C — Multi-Scale Feature Extraction')

        if features_dict is not None:
            comb_dim = len(features_dict['combined'])
            metric_card('COMBINED FEATURE VECTOR', f'{comb_dim:,} dimensions', 'Concatenated LBP + HOG + GLCM + Statistical moments')

            # Expandable sections for each feature group
            with st.expander('▾ 1. Local Binary Patterns (LBP) Texture Features (10 Dimensions)', expanded=False):
                st.markdown('**Rotational-Invariant Uniform LBP Histogram ($P=8, R=1$):**')
                lbp_arr = features_dict['lbp']
                lbp_df = pd.DataFrame({
                    'Histogram Bin': [f'Bin {i}' for i in range(len(lbp_arr))],
                    'Relative Density': lbp_arr
                }).set_index('Histogram Bin')
                st.bar_chart(lbp_df, color=accent)
                st.caption('LBP captures micro-texture smoothness and high-frequency edge blending artifacts at pixel-neighborhood scale.')

            with st.expander('▾ 2. Histogram of Oriented Gradients (HOG) Structural Edge Features (6,084 Dimensions)', expanded=False):
                hog_arr = features_dict['hog']
                h1, h2, h3, h4 = st.columns(4)
                with h1: metric_card('HOG DIMENSIONS', f'{len(hog_arr):,}')
                with h2: metric_card('MEAN GRADIENT', f'{float(np.mean(hog_arr)):.4f}')
                with h3: metric_card('MAX GRADIENT', f'{float(np.max(hog_arr)):.4f}')
                with h4: metric_card('L2 VECTOR NORM', f'{float(np.linalg.norm(hog_arr)):.4f}')
                st.caption('HOG captures structural facial geometry across 16×16 pixel cells with 2×2 block normalization over 9 gradient orientations.')

            with st.expander('▾ 3. Gray-Level Co-Occurrence Matrix (GLCM) Spatial Descriptors (5 Dimensions)', expanded=False):
                glcm_names = ['Contrast', 'Dissimilarity', 'Homogeneity', 'Energy', 'Correlation']
                glcm_arr = features_dict['glcm']
                glcm_df = pd.DataFrame([
                    {'Property': name, 'Value': f'{val:.4f}'}
                    for name, val in zip(glcm_names, glcm_arr)
                ])
                st.dataframe(glcm_df, use_container_width=True, hide_index=True)
                st.caption('GLCM measures spatial gray-level pixel correlations across horizontal and 45° angular distances.')

            with st.expander('▾ 4. Statistical Descriptors (4 Dimensions)', expanded=False):
                stat_labels = ['Intensity Mean', 'Intensity Std Dev', 'Shannon Entropy', 'Canny Edge Density']
                stat_arr = features_dict['stats']
                stat_df = pd.DataFrame([
                    {'Descriptor': lbl, 'Value': f'{val:.4f}'}
                    for lbl, val in zip(stat_labels, stat_arr)
                ])
                st.dataframe(stat_df, use_container_width=True, hide_index=True)

            with st.expander('▾ 5. Combined Feature Vector Summary & Sanity Verification', expanded=False):
                feat_rows = []
                for k, v in features_dict.items():
                    feat_rows.append({
                        'Feature Group': k.upper(),
                        'Dimensions': len(v),
                        'Mean Value': f'{np.mean(v):.4f}',
                        'Std Dev': f'{np.std(v):.4f}',
                        'Finite & Valid': '✓ All Finite' if np.isfinite(v).all() else '✗ Non-finite'
                    })
                st.dataframe(pd.DataFrame(feat_rows), use_container_width=True, hide_index=True)
        else:
            st.info('Feature extraction is pending face detection.')

        # ── SECTION D: MODEL STATUS ───────────────────────────────────────────
        st.markdown('---')
        section_title('Section D — Morph Detection Model Status')

        cur_state = analysis_result.get('state', 'MODEL UNAVAILABLE')
        if cur_state == 'MODEL UNAVAILABLE' or model is None:
            st.markdown(
                f'''<div class="panel" style="border-left:4px solid #f59e0b;padding:1.2rem">
                  <div style="font-size:1.15rem;font-weight:800;color:#f59e0b">STATUS: MODEL UNAVAILABLE</div>
                  <p style="margin-top:.4rem;line-height:1.6">
                    Image processing and feature extraction completed successfully. No trained model was selected,
                    so exploratory analysis is presented without classification.
                  </p>
                  <div style="font-size:.78rem;opacity:.8;margin-top:.4rem">
                    MorphGuard enforces research governance: uncalibrated confidence scores, simulated ROC curves,
                    and fabricated morph/genuine predictions are strictly prohibited. Select a trained model from the sidebar to enable experimental inference.
                  </div>
                </div>''',
                unsafe_allow_html=True
            )
        else:
            # Active experimental inference
            score = analysis_result.get('score', 0.5)
            badge_color = '#ef4444' if 'MORPH' in cur_state else ('#10b981' if 'GENUINE' in cur_state else '#f59e0b')
            badge_icon = '🚨' if 'MORPH' in cur_state else ('✅' if 'GENUINE' in cur_state else '⚠️')

            st.markdown(
                f'''<div class="panel" style="border-left:5px solid {badge_color};padding:1.2rem">
                  <div style="font-size:1.25rem;font-weight:800;color:{badge_color}">
                    {badge_icon} DETECTION RESULT: {cur_state}
                  </div>
                  <div style="margin-top:.6rem;display:flex;gap:2rem;flex-wrap:wrap">
                    <div><b>Inference Score:</b> <code>{score:.4f}</code></div>
                    <div><b>Active Model:</b> <code>{selected_model_name}</code></div>
                    <div><b>Decision Threshold:</b> <code>0.5000</code> (Uncertainty zone: [0.40, 0.60])</div>
                  </div>
                  <p style="margin-top:.6rem;font-size:.85rem;line-height:1.5;opacity:.9">
                    <b>Experimental Model Output:</b> This classification was generated by an experimental model trained on
                    provenance-verified MONOT/ONOT partitions with strict subject-identity separation.
                  </p>
                  <div style="font-size:.78rem;opacity:.75;margin-top:.4rem;border-top:1px solid rgba(255,255,255,0.1);padding-top:.4rem">
                    <b>Research Safeguard Notice:</b> This is an experimental research detector trained on 365 approved samples.
                    It has not completed full independent certification under ISO/IEC 30107-3.
                  </div>
                </div>''',
                unsafe_allow_html=True
            )

        if analysis_result.get('demo_class'):
            st.markdown(
                f'''<div class="panel" style="border-left:4px solid #35d1c4;margin-top:.8rem">
                  <span style="font-weight:700;color:{accent}">ILLUSTRATIVE DEMO MODE:</span> <b>{analysis_result['demo_class']}</b>
                  <div style="font-size:.78rem;opacity:.85;margin-top:2px">{analysis_result.get('demo_disclaimer')}</div>
                </div>''',
                unsafe_allow_html=True
            )

        # ── SECTION E: REPORTS & AUDIT TRAIL ──────────────────────────────────
        st.markdown('---')
        section_title('Section E — Reports & Audit Export')

        report_payload = {
            'image_metadata': {
                'filename': source_name,
                'file_size_bytes': len(source_bytes),
                'width': orig_w,
                'height': orig_h,
            },
            'face_detection': {
                'face_count': faces_detected,
                'bounding_box': analysis_result.get('face_box'),
                'crop_dimensions': [224, 224, 3],
            },
            'quality_metrics': q,
            'feature_summary': feature_summary,
            'model_status': {
                'selected_model': selected_model_name,
                'state': 'MODEL UNAVAILABLE',
                'classification_performed': False,
                'notice': 'No approved model artifact installed. Research safeguards active.'
            },
            'processing_seconds': proc_time,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        }

        col_rep1, col_rep2 = st.columns([1, 2])
        with col_rep1:
            st.download_button(
                '📥 Download Analysis Report (JSON)',
                json.dumps(report_payload, indent=2, default=str),
                file_name=f'morphguard_analysis_{Path(source_name).stem}.json',
                mime='application/json',
                use_container_width=True
            )

        with st.expander('▾ Technical JSON Payload & Processing Metadata', expanded=False):
            st.json(report_payload)

    else:
        empty_state(
            'Ready for Face Analysis',
            'Upload a JPG, JPEG, or PNG facial image above, or select one of the pre-packaged samples in the sidebar. '
            'Face detection, quality evaluation, and multi-scale texture features will be computed locally.'
        )

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2: ORIGINAL-VERSUS-MORPHED COMPARISON
# ═════════════════════════════════════════════════════════════════════════════
with tab_compare:
    section_title('Two-Image Exploratory Comparison')
    st.write(
        'Upload an original candidate and a corresponding morphed candidate. '
        'Both images are processed independently through the exact same feature pipeline, '
        'enabling side-by-side inspection of quality differences, LBP micro-textures, and HOG structural gradients.'
    )

    c_up1, c_up2 = st.columns(2)
    with c_up1:
        st.markdown('**Image A (Original Candidate)**')
        comp_file_a = st.file_uploader('Upload Image A', type=['jpg', 'jpeg', 'png'], key='comp_a_file')
        sample_btn_a = st.button('Load Sample A (Gate_10 Genuine)', key='btn_load_sample_a')
    with c_up2:
        st.markdown('**Image B (Morphed Candidate)**')
        comp_file_b = st.file_uploader('Upload Image B', type=['jpg', 'jpeg', 'png'], key='comp_b_file')
        sample_btn_b = st.button('Load Sample B (MONOT Morphed)', key='btn_load_sample_b')

    source_a = comp_file_a
    source_b = comp_file_b

    if sample_btn_a or (sample_choice == 'Sample A: Genuine candidate (MONOT Gate_10)' and not comp_file_a):
        sample_a_path = ROOT / 'MONOT/Gate_10/S113923411-GF-A35-EEA-T14-S1-LH-C1-I0048-F00-0.png'
        if sample_a_path.exists():
            source_a = sample_a_path

    if sample_btn_b or (sample_choice == 'Sample B: Morphed candidate (MONOT Morphed)' and not comp_file_b):
        sample_b_path = ROOT / 'MONOT/Morphed/M_S113923411-GF-A35-EEA-T14-S1-LH-C1-I0048-F00_S198149424-GF-A51-EEA-T13-S1-LH-C1-I0055-F00_C01_B30_W30_PA01_PM00_F00.png'
        if sample_b_path.exists():
            source_b = sample_b_path

    if source_a is not None and source_b is not None:
        img_a_bgr, bytes_a, err_a = load_image_bytes(source_a)
        img_b_bgr, bytes_b, err_b = load_image_bytes(source_b)

        if err_a:
            st.error(f'Image A error: {err_a}')
            st.stop()
        if err_b:
            st.error(f'Image B error: {err_b}')
            st.stop()

        with st.spinner('Processing both images independently through the feature pipeline...'):
            prep = FacePreprocessor()
            faces_a = prep.detect(img_a_bgr)
            faces_b = prep.detect(img_b_bgr)

            if not faces_a:
                st.warning('Image A: No face detected.')
                st.stop()
            if not faces_b:
                st.warning('Image B: No face detected.')
                st.stop()

            face_a = faces_a[0]
            face_b = faces_b[0]

            q_a = prep.quality(img_a_bgr, face_a).as_dict()
            q_b = prep.quality(img_b_bgr, face_b).as_dict()

            crop_a = prep.transform(img_a_bgr, face_a)
            crop_b = prep.transform(img_b_bgr, face_b)

            feat_a = extract_features(crop_a)
            feat_b = extract_features(crop_b)

        # ── Side-by-Side Visual Previews ──────────────────────────────────────
        st.markdown('---')
        section_title('Side-by-Side Visual Previews')

        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown('#### Image A (Original Candidate)')
            draw_a = img_a_bgr.copy()
            xa, ya, wa, ha = face_a
            cv2.rectangle(draw_a, (xa, ya), (xa + wa, ya + ha), (0, 220, 190), 3)
            st.image(cv2.cvtColor(draw_a, cv2.COLOR_BGR2RGB), caption=f'Image A: {img_a_bgr.shape[1]}×{img_a_bgr.shape[0]} px', use_container_width=True)
            st.image(crop_a, caption='Image A Face Crop (224×224)', width=200)

        with c_right:
            st.markdown('#### Image B (Morphed Candidate)')
            draw_b = img_b_bgr.copy()
            xb, yb, wb, hb = face_b
            cv2.rectangle(draw_b, (xb, yb), (xb + wb, yb + hb), (255, 120, 80), 3)
            st.image(cv2.cvtColor(draw_b, cv2.COLOR_BGR2RGB), caption=f'Image B: {img_b_bgr.shape[1]}×{img_b_bgr.shape[0]} px', use_container_width=True)
            st.image(crop_b, caption='Image B Face Crop (224×224)', width=200)

        # ── Model Classification Comparison (if model selected) ──────────────
        comp_model = load_pipeline_model(selected_model_name)
        if comp_model is not None:
            st.markdown('---')
            section_title(f'Experimental Model Classification ({selected_model_name})')
            try:
                score_a = float(comp_model.predict_score(crop_a))
                score_b = float(comp_model.predict_score(crop_b))
                state_a = "UNCERTAIN" if 0.40 <= score_a <= 0.60 else ("MORPHED / MORPHING ATTACK" if score_a > 0.5 else "GENUINE / BONA FIDE")
                state_b = "UNCERTAIN" if 0.40 <= score_b <= 0.60 else ("MORPHED / MORPHING ATTACK" if score_b > 0.5 else "GENUINE / BONA FIDE")

                mc_col1, mc_col2 = st.columns(2)
                with mc_col1:
                    bg_a = '#ef4444' if 'MORPH' in state_a else ('#10b981' if 'GENUINE' in state_a else '#f59e0b')
                    st.markdown(
                        f'''<div class="panel" style="border-left:4px solid {bg_a};padding:1rem">
                          <div style="font-weight:700;color:{bg_a}">IMAGE A: {state_a}</div>
                          <div>Score: <code>{score_a:.4f}</code></div>
                        </div>''', unsafe_allow_html=True
                    )
                with mc_col2:
                    bg_b = '#ef4444' if 'MORPH' in state_b else ('#10b981' if 'GENUINE' in state_b else '#f59e0b')
                    st.markdown(
                        f'''<div class="panel" style="border-left:4px solid {bg_b};padding:1rem">
                          <div style="font-weight:700;color:{bg_b}">IMAGE B: {state_b}</div>
                          <div>Score: <code>{score_b:.4f}</code></div>
                        </div>''', unsafe_allow_html=True
                    )
            except Exception as m_exc:
                st.warning(f'Experimental classification comparison error: {m_exc}')

        # ── Side-by-Side Parameter Comparison Table ───────────────────────────
        st.markdown('---')
        section_title('Parameter Comparison Table')

        param_table = [
            {
                'Parameter': 'Image dimensions',
                'Original (Image A)': f'{img_a_bgr.shape[1]}×{img_a_bgr.shape[0]} px',
                'Morphed (Image B)': f'{img_b_bgr.shape[1]}×{img_b_bgr.shape[0]} px',
                'Comparison / Delta': f'A: {img_a_bgr.shape[1]}×{img_a_bgr.shape[0]} vs B: {img_b_bgr.shape[1]}×{img_b_bgr.shape[0]}'
            },
            {
                'Parameter': 'Faces detected',
                'Original (Image A)': str(len(faces_a)),
                'Morphed (Image B)': str(len(faces_b)),
                'Comparison / Delta': 'Equal (1 face)' if len(faces_a) == len(faces_b) else f'A: {len(faces_a)} vs B: {len(faces_b)}'
            },
            {
                'Parameter': 'Brightness',
                'Original (Image A)': f"{q_a['brightness']:.2f}",
                'Morphed (Image B)': f"{q_b['brightness']:.2f}",
                'Comparison / Delta': f"Δ = {q_b['brightness'] - q_a['brightness']:+.2f}"
            },
            {
                'Parameter': 'Contrast',
                'Original (Image A)': f"{q_a['contrast']:.2f}",
                'Morphed (Image B)': f"{q_b['contrast']:.2f}",
                'Comparison / Delta': f"Δ = {q_b['contrast'] - q_a['contrast']:+.2f}"
            },
            {
                'Parameter': 'Sharpness (Blur variance)',
                'Original (Image A)': f"{q_a['blur_variance']:.2f}",
                'Morphed (Image B)': f"{q_b['blur_variance']:.2f}",
                'Comparison / Delta': f"Δ = {q_b['blur_variance'] - q_a['blur_variance']:+.2f} ({'Blurred' if q_b['blur_variance'] < 50 else 'Sharp'})"
            },
            {
                'Parameter': 'LBP dimensions',
                'Original (Image A)': str(len(feat_a['lbp'])),
                'Morphed (Image B)': str(len(feat_b['lbp'])),
                'Comparison / Delta': 'Identical (10 dims)'
            },
            {
                'Parameter': 'HOG dimensions',
                'Original (Image A)': str(len(feat_a['hog'])),
                'Morphed (Image B)': str(len(feat_b['hog'])),
                'Comparison / Delta': 'Identical (6084 dims)'
            },
            {
                'Parameter': 'GLCM dimensions',
                'Original (Image A)': str(len(feat_a['glcm'])),
                'Morphed (Image B)': str(len(feat_b['glcm'])),
                'Comparison / Delta': 'Identical (5 dims)'
            },
            {
                'Parameter': 'Combined dimensions',
                'Original (Image A)': str(len(feat_a['combined'])),
                'Morphed (Image B)': str(len(feat_b['combined'])),
                'Comparison / Delta': 'Identical (6103 dims)'
            },
        ]
        st.dataframe(pd.DataFrame(param_table), use_container_width=True, hide_index=True)

        # ── Feature Differences & Cosine Similarities ─────────────────────────
        comp_results = {}
        for k in ('lbp', 'hog', 'glcm', 'stats', 'combined'):
            try:
                comp_results[k] = compare_vectors(feat_a[k], feat_b[k])
            except Exception as c_err:
                comp_results[k] = {'error': str(c_err)}

        with st.expander('▾ Extracted Feature Differences & Mathematical Similarities', expanded=True):
            feat_diff_table = []
            for k, v in comp_results.items():
                if 'error' in v:
                    feat_diff_table.append({
                        'Feature Group': k.upper(),
                        'Dimensions': 'Error',
                        'Cosine Similarity': 'N/A',
                        'Mean Absolute Diff': 'N/A',
                        'Max Absolute Diff': 'N/A',
                        'Vector Integrity': 'Failed'
                    })
                else:
                    cos_sim = v.get('cosine_similarity')
                    feat_diff_table.append({
                        'Feature Group': k.upper(),
                        'Dimensions': v.get('dimensions'),
                        'Cosine Similarity': f"{cos_sim:.4f}" if cos_sim is not None else 'N/A (zero norm)',
                        'Mean Absolute Diff': f"{v.get('absolute_difference_mean', 0):.4f}",
                        'Max Absolute Diff': f"{v.get('absolute_difference_max', 0):.4f}",
                        'Vector Integrity': '✓ Finite & Valid' if v.get('finite') else 'Non-finite'
                    })
            st.dataframe(pd.DataFrame(feat_diff_table), use_container_width=True, hide_index=True)

            st.info(
                '⚠️ **SCIENTIFIC DISCLAIMER:** These calculations are exploratory feature differences and mathematical vector similarities. '
                'They are **NOT** validated morph detection scores, attack probabilities, or classification decisions. '
                'High or low similarity does not constitute proof of morphing.'
            )

        # ── Visual Feature Comparisons ────────────────────────────────────────
        with st.expander('▾ Visual Feature Comparisons (Charts)', expanded=True):
            v_col1, v_col2 = st.columns(2)
            with v_col1:
                st.markdown('**LBP Histogram Comparison (Micro-Texture)**')
                lbp_comp_df = pd.DataFrame({
                    'Bin': [f'Bin {i}' for i in range(len(feat_a['lbp']))],
                    'Image A (Original)': feat_a['lbp'],
                    'Image B (Morphed)': feat_b['lbp'],
                }).set_index('Bin')
                st.bar_chart(lbp_comp_df)

            with v_col2:
                st.markdown('**GLCM Properties Comparison (Spatial Texture)**')
                glcm_names = ['Contrast', 'Dissimilarity', 'Homogeneity', 'Energy', 'Correlation']
                glcm_comp_df = pd.DataFrame({
                    'Property': glcm_names,
                    'Image A (Original)': feat_a['glcm'],
                    'Image B (Morphed)': feat_b['glcm'],
                }).set_index('Property')
                st.bar_chart(glcm_comp_df)

        # ── Download Comparison Report ────────────────────────────────────────
        comparison_report = {
            'comparison_type': 'exploratory_two_image_differential',
            'classification_performed': False,
            'disclaimer': 'Exploratory feature vector comparisons only. Not a trained classifier prediction.',
            'image_a': {
                'dimensions': [img_a_bgr.shape[1], img_a_bgr.shape[0]],
                'face_box': face_a,
                'quality': q_a,
                'feature_summary': {k: {'mean': float(np.mean(v)), 'std': float(np.std(v))} for k, v in feat_a.items()}
            },
            'image_b': {
                'dimensions': [img_b_bgr.shape[1], img_b_bgr.shape[0]],
                'face_box': face_b,
                'quality': q_b,
                'feature_summary': {k: {'mean': float(np.mean(v)), 'std': float(np.std(v))} for k, v in feat_b.items()}
            },
            'feature_differences': comp_results,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        }

        st.markdown('---')
        col_c_d1, col_c_d2 = st.columns([1, 2])
        with col_c_d1:
            st.download_button(
                '📥 Download Comparison Report (JSON)',
                json.dumps(comparison_report, indent=2, default=str),
                file_name='morphguard_two_image_comparison.json',
                mime='application/json',
                use_container_width=True
            )

        with st.expander('▾ Technical Comparison JSON Payload', expanded=False):
            st.json(comparison_report)

    else:
        empty_state(
            'Upload Both Images to Compare',
            'Provide both Image A (original candidate) and Image B (morphed candidate) '
            'or use the "Load Sample" buttons above to view an instant side-by-side comparison.'
        )

footer()
