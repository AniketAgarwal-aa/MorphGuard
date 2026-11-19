import json, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))

from morphguard.inference import load_joblib_model, load_pytorch_model, InferenceService

def main():
    reg_path = ROOT / 'models' / 'metadata' / 'model_registry.json'
    reg = json.loads(reg_path.read_text(encoding='utf-8'))

    print("=== MODEL REGISTRY & ARTIFACT VERIFICATION ===")
    print(f"Registry version: {reg.get('registry_version')}")
    print(f"Total models in registry: {len(reg.get('models', []))}\n")

    dummy_img = np.zeros((224, 224, 3), dtype=np.uint8)

    for m in reg.get('models', []):
        name = m.get('model_name')
        status = m.get('training_status')
        art_path = m.get('artifact_path')
        feat_key = m.get('feature_key')
        dims = m.get('input_dimensions')
        mets = m.get('metrics', {})

        framework = m.get('framework', 'unknown')
        print(f"Model: {name:<16} | Status: {status:<18} | Framework: {framework}")
        
        if status == 'trained' and art_path:
            p = ROOT / art_path
            assert p.exists(), f"Artifact not found: {p}"
            sz = p.stat().st_size
            print(f"  Artifact: {p.name} ({sz:,} bytes)")
            
            if p.name.endswith('.joblib'):
                fk = 'combined' if feat_key == 'X' else feat_key
                adapter = load_joblib_model(p, feature_key=fk)
                score = adapter.predict_score(dummy_img)
                print(f"  Inference OK: Score={score:.4f} (feature_key={fk}, dims={dims})")
            elif p.name.endswith('.pt'):
                arch = m.get('architecture')
                adapter = load_pytorch_model(p, architecture=arch)
                score = adapter.predict_score(dummy_img)
                print(f"  Inference OK: Score={score:.4e} (input_dims={dims})")
            
            print(f"  Evaluation (Test): Acc={mets.get('accuracy')}, ACER={mets.get('acer')}, APCER={mets.get('apcer')}, BPCER={mets.get('bpcer')}")
        else:
            print(f"  Note: {mets.get('status', 'Architecture implemented, compute-gated')}")
        print()

    # Verify InferenceService safe handling of missing model and invalid sources
    print("=== INFERENCE SERVICE SAFEGUARD CHECK ===")
    safe_svc = InferenceService(model=None)
    
    # 1. Invalid input type
    res_inv = safe_svc.analyse(12345)
    print(f"Invalid input handling: state={res_inv.get('state')} (error='{res_inv.get('error')}')")
    assert res_inv.get('state') == 'INVALID IMAGE', f"Expected INVALID IMAGE, got {res_inv}"
    
    # 2. Valid image bytes but no face detected
    import cv2
    _, black_buf = cv2.imencode('.png', dummy_img)
    res_noface = safe_svc.analyse(black_buf.tobytes())
    print(f"No face detected handling: state={res_noface.get('state')}")
    assert res_noface.get('state') == 'FACE NOT DETECTED', f"Expected FACE NOT DETECTED, got {res_noface}"

    # 3. Valid sample face from MONOT
    sample_p = ROOT / 'MONOT/Gate_10/S113923411-GF-A35-EEA-T14-S1-LH-C1-I0048-F00-0.png'
    if sample_p.exists():
        res_sample = safe_svc.analyse(sample_p)
        print(f"Model=None on valid face: state={res_sample.get('state')} (face_count={res_sample.get('face_count')})")
        assert res_sample.get('state') == 'MODEL UNAVAILABLE', f"Expected MODEL UNAVAILABLE, got {res_sample}"
    
    print("InferenceService handles all edge cases and missing models safely.\n")

if __name__ == '__main__':
    main()
