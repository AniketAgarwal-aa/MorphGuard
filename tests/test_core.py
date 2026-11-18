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
