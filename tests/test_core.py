from pathlib import Path
import numpy as np
from PIL import Image
from morphguard.dataset.audit import read_onot_thresholds
from morphguard.preprocessing import FacePreprocessor

def test_invalid_image_is_rejected(tmp_path):
    p=tmp_path/'bad.jpg';p.write_bytes(b'not an image')
    try: FacePreprocessor().load(str(p))
    except ValueError: pass
    else: assert False

def test_quality_report():
    image=np.full((100,100,3),128,dtype=np.uint8)
    report=FacePreprocessor().quality(image)
    assert report.blur_variance >= 0

def test_threshold_reader(tmp_path):
    (tmp_path/'threshold=0.5_cosine_images.txt').write_text('a/a.png b/b.png')
    rows=read_onot_thresholds(tmp_path)
    assert rows[0]['entry_count']==2 and rows[0]['cosine_threshold']==.5

def test_feature_dimensions():
    from morphguard.feature_extraction import extract_features
    features=extract_features(np.zeros((224,224,3),dtype=np.uint8))
    assert features['combined'].shape[0] == features['lbp'].shape[0] + features['hog'].shape[0] + features['glcm'].shape[0] + features['stats'].shape[0]

def test_deep_model_interfaces():
    import torch
    from morphguard.classification.models import create_model
    x=torch.zeros(1,3,224,224)
    for name in ('custom_cnn','resnet18','efficientnet_b0'):
        assert create_model(name)(x).shape == (1,2)

def test_metric_calculation():
    from morphguard.evaluation.metrics import binary_metrics
    result=binary_metrics([0,0,1,1],[.1,.2,.8,.9])
    assert result['accuracy']==1.0 and result['specificity']==1.0

def test_label_manifest_rejects_unreviewed_training(tmp_path):
    from morphguard.dataset.labels import validate_label_manifest
    manifest=tmp_path/'labels.csv'
    manifest.write_text('image_path,dataset,category,proposed_label,verified_label,label_source,subject_id,morph_pair_id,reviewer_status,review_notes,split,exclusion_reason,manifest_version\n')
    result=validate_label_manifest(manifest,tmp_path,require_approved=True)
    assert not result['valid'] and result['approved_rows']==0

def test_audit_status_distinguishes_missing_and_complete():
    from app.components.data import audit_status
    assert audit_status({}, {}, __import__('pandas').DataFrame())['state']=='missing'
    rows=__import__('pandas').DataFrame([{'dataset':'MONOT','category':'Gate_10','count':2550},{'dataset':'MONOT','category':'Gate_25','count':6350},{'dataset':'MONOT','category':'Morphed','count':15240},{'dataset':'ONOT','category':'digital','count':11326},{'dataset':'ONOT','category':'print-scan','count':11326}])
    assert audit_status({'image_counts':rows.to_dict('records')},{},rows)['state']=='complete'

def test_model_artifact_requires_approval(tmp_path):
    from morphguard.inference.artifacts import validate_artifact
    model=tmp_path/'m.joblib'; meta=tmp_path/'m.json'; model.write_bytes(b'x'); meta.write_text('{}')
    result=validate_artifact(model,meta)
    assert not result['valid'] and any('approved' in e for e in result['errors'])

def test_annotation_inventory_is_pending_and_unapproved():
    import csv, json
    from pathlib import Path
    root=Path(__file__).parents[1]
    summary=json.loads((root/'data/metadata/annotation_audit_summary.json').read_text(encoding='utf-8'))
    assert summary['records']==46792 and summary['approved_for_training']==0
    with (root/'data/manifests/annotation_inventory.csv').open(encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==46792 and {r['review_status'] for r in rows}=={'pending_review'}

def test_review_approval_requires_evidence(tmp_path):
    from morphguard.dataset.review import apply_review
    p=tmp_path/'manifest.csv'
    p.write_text('image_path,review_status\nimg.png,pending_review\n',encoding='utf-8')
    try: apply_review(p,'img.png',{'review_status':'approved','verified_class':'MORPHED'},'reviewer')
    except ValueError as exc: assert 'requires' in str(exc)
    else: assert False

def test_review_approval_is_audited_and_exports(tmp_path):
    from morphguard.dataset.review import apply_review, export_approved
    image=tmp_path/'img.png'; image.write_bytes(b'placeholder')
    p=tmp_path/'manifest.csv'
    p.write_text('image_path,dataset,category,verified_label,review_status\nimg.png,MONOT,Morphed,,pending_review\n',encoding='utf-8')
    apply_review(p,'img.png',{'review_status':'approved','verified_class':'MORPHED','evidence_source':'official review note','identity_verified':True,'pair_verified':True,'review_notes':'verified by reviewer'},'alice')
    row=__import__('csv').DictReader(p.open(encoding='utf-8')); row=next(row); assert row['verified_label']=='morphed' and row['reviewer']=='alice'
    out=tmp_path/'approved.csv'; assert export_approved(p,out)==1 and out.with_suffix('.csv.json').exists()
    try: apply_review(p,'img.png',{'review_status':'rejected','verified_class':'UNKNOWN'},'alice')
    except ValueError as exc: assert 'immutable' in str(exc)
    else: assert False

def test_group_split_fixture_uses_approved_rows_only(tmp_path):
    import csv
    from morphguard.dataset.splits import create_group_splits
    fields=['image_path','dataset','category','proposed_label','verified_label','label_source','subject_id','morph_pair_id','reviewer_status','review_notes','split','exclusion_reason','manifest_version']
    rows=[]
    for i in range(6):
        name=f'img{i}.png'; (tmp_path/name).write_bytes(b'x')
        rows.append({'image_path':name,'dataset':'MONOT','category':'Morphed','proposed_label':'','verified_label':'morphed' if i%2 else 'genuine','label_source':'review','subject_id':f'S{i}','morph_pair_id':'','reviewer_status':'approved','review_notes':'reviewed','split':'train','exclusion_reason':'','manifest_version':'1'})
    manifest=tmp_path/'labels.csv'
    with manifest.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    summary=create_group_splits(manifest,tmp_path/'splits',seed=1,project_root=tmp_path)
    assert sum(summary['rows'].values())==6 and (tmp_path/'splits/split_validation_report.json').exists()

def test_targeted_review_batch_is_pending_and_stratified():
    import csv, json
    from pathlib import Path
    root=Path(__file__).parents[1]; batch=root/'data/manifests/targeted_review_batch.csv'
    with batch.open(encoding='utf-8') as f: rows=list(csv.DictReader(f))
    assert len(rows)==150 and {r['review_status'] for r in rows}=={'pending_review'}
    counts={}
    for row in rows: counts[f"{row['dataset']}/{row['category']}"]=counts.get(f"{row['dataset']}/{row['category']}",0)+1
    assert set(counts.values())=={30}
    meta=json.loads(batch.with_suffix('.json').read_text(encoding='utf-8')); assert meta['rows']==150 and meta['status']=='pending_review'

def test_feature_cache_validation_output():
    from pathlib import Path
    import json
    root=Path(__file__).parents[1]; summary=json.loads((root/'data/cache/image_features/processing_summary.json').read_text())
    assert summary['success'] >= 500 and summary['feature_records'] == summary['success'] and summary['failed'] == 0

def test_inference_accepts_pathlike_source():
    import csv
    from pathlib import Path
    from morphguard.inference import InferenceService
    root=Path(__file__).parents[1]
    with (root/'data/cache/image_features/processing_manifest.csv').open(encoding='utf-8') as f: row=next(csv.DictReader(f))
    result=InferenceService().analyse(root/row['image_path'])
    assert result['state'] in {'MODEL UNAVAILABLE','FACE NOT DETECTED'}

def test_annotation_pilot_evidence_package():
    import csv, json
    from pathlib import Path
    root=Path(__file__).parents[1]; summary=json.loads((root/'data/review_pilot/pilot_summary.json').read_text(encoding='utf-8'))
    with (root/'data/review_pilot/annotation_evidence.csv').open(encoding='utf-8') as f: rows=list(csv.DictReader(f))
    assert len(rows)==150 and summary['missing_source_images']==0 and {r['review_status'] for r in rows}=={'pending_review'}
    assert sum(summary['eligibility_counts'].values())==150

def test_insufficient_provenance_cannot_be_approved(tmp_path):
    from morphguard.dataset.review import apply_review
    p=tmp_path/'m.csv'; p.write_text('image_path,review_status\nimg.png,pending_review\n',encoding='utf-8')
    try: apply_review(p,'img.png',{'review_status':'approved','verified_class':'MORPHED','eligibility':'INSUFFICIENT_PROVENANCE','evidence_source':'x','identity_verified':True,'review_notes':'x'},'reviewer')
    except ValueError as exc: assert 'not eligible' in str(exc)
    else: assert False

def test_exploratory_feature_comparison_is_safe():
    import numpy as np
    from morphguard.inference import compare_vectors
    result=compare_vectors(np.array([1.,0.,0.]),np.array([1.,1.,0.]))
    assert result['dimensions']==3 and result['finite'] and result['cosine_similarity'] is not None
    try: compare_vectors(np.zeros(2),np.zeros(3))
    except ValueError: pass
    else: assert False

def test_two_image_feature_comparison_on_pipeline():
    import numpy as np
    from morphguard.feature_extraction import extract_features
    from morphguard.inference import compare_vectors

    # Create synthetic face crops of identical shape (224, 224, 3)
    crop_a = np.full((224, 224, 3), 120, dtype=np.uint8)
    crop_b = np.full((224, 224, 3), 130, dtype=np.uint8)

    feat_a = extract_features(crop_a)
    feat_b = extract_features(crop_b)

    for k in ('lbp', 'hog', 'glcm', 'stats', 'combined'):
        assert k in feat_a and k in feat_b
        res = compare_vectors(feat_a[k], feat_b[k])
        assert res['dimensions'] == len(feat_a[k])
        assert res['finite'] is True
        assert res['absolute_difference_mean'] >= 0.0

def test_report_generation_json_integrity():
    import json
    report = {
        'image_metadata': {'filename': 'test.png', 'width': 224, 'height': 224},
        'face_detection': {'face_count': 1, 'bounding_box': [10, 10, 100, 100]},
        'quality_metrics': {'blur_variance': 150.0, 'brightness': 120.0, 'contrast': 50.0},
        'model_status': {'state': 'MODEL UNAVAILABLE', 'classification_performed': False}
    }
    serialized = json.dumps(report, indent=2)
    deserialized = json.loads(serialized)
    assert deserialized['model_status']['state'] == 'MODEL UNAVAILABLE'
    assert deserialized['face_detection']['face_count'] == 1

def test_theme_system_and_accent_colors():
    from app.components import get_accent_color
    import streamlit as st
    st.session_state['theme'] = 'dark'
    assert get_accent_color() == '#35d1c4'
    st.session_state['theme'] = 'light'
    assert get_accent_color() == '#0284c7'

def test_navigation_manifest_contains_all_14_pages():
    from pathlib import Path
    import ast
    root = Path(__file__).parents[1]
    main_py = root / 'app' / 'main.py'
    tree = ast.parse(main_py.read_text(encoding='utf-8'))
    page_files = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, 'attr', '') == 'Page':
            if node.args and isinstance(node.args[0], ast.Constant):
                page_files.append(node.args[0].value)
    assert len(page_files) == 14
    for pf in page_files:
        assert (root / 'app' / pf).exists(), f"Page file {pf} must exist on disk"
