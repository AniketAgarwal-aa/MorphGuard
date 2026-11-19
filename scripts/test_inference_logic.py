import sys
from pathlib import Path
import json, numpy as np, cv2

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from morphguard.inference.service import load_joblib_model, InferenceService

def main():
    print("=== TESTING INFERENCE SERVICE LOGIC ===")
    meta = json.loads((ROOT / 'models/metadata/combined_svm.json').read_text(encoding='utf-8'))
    thresh = float(meta['calibrated_threshold'])
    print(f"Model: combined_svm, Threshold: {thresh}")

    model = load_joblib_model(ROOT / 'models/trained/combined_svm.joblib', feature_key='combined', threshold=thresh)
    service = InferenceService(model=model, threshold=thresh)

    # 1. Genuine test sample
    p_gen = ROOT / 'MONOT/Gate_10/S457681878-GF-A95-EEA-T14-S1-LH-C1-I0017-F00-0.png'
    assert p_gen.exists(), f"File {p_gen} does not exist"
    res_gen = service.analyse(p_gen)
    print("\n1. Genuine Test Sample:")
    print(f"   State: {res_gen.get('state')}")
    print(f"   Score: {res_gen.get('score'):.6f}")
    print(f"   Threshold: {res_gen.get('decision_threshold'):.6f}")
    print(f"   Status: {res_gen.get('status')}")
    print(f"   Explanation: {res_gen.get('explanation')}")
    assert res_gen.get('state') == 'GENUINE', f"Expected GENUINE, got {res_gen.get('state')}"
    assert res_gen.get('status') == 'SUCCESS'
    assert res_gen.get('score') < thresh

    # 2. Morphed test sample
    p_morph = ROOT / 'MONOT/Morphed/M_S115293589-GF-A67-EME-T01-S1-LH-C1-I0030-F00_S368730932-GF-A97-EME-T14-S1-LH-C1-I0020-F00_C01_B30_W30_PA01_PM00_F00.png'
    assert p_morph.exists(), f"File {p_morph} does not exist"
    res_morph = service.analyse(p_morph)
    print("\n2. Morphed Test Sample:")
    print(f"   State: {res_morph.get('state')}")
    print(f"   Score: {res_morph.get('score'):.6f}")
    print(f"   Threshold: {res_morph.get('decision_threshold'):.6f}")
    print(f"   Status: {res_morph.get('status')}")
    print(f"   Explanation: {res_morph.get('explanation')}")
    assert res_morph.get('state') == 'MORPHED', f"Expected MORPHED, got {res_morph.get('state')}"
    assert res_morph.get('status') == 'SUCCESS'
    assert res_morph.get('score') >= thresh

    # 3. Technical Safeguard Tests
    print("\n3. Technical Safeguards:")
    # A. Model None
    res_nomodel = InferenceService(model=None).analyse(p_gen)
    print(f"   No model state: {res_nomodel.get('state')} (status={res_nomodel.get('status')})")
    assert res_nomodel.get('state') == 'MODEL UNAVAILABLE'

    # B. Invalid input
    res_inv = service.analyse('non_existent_file.xyz')
    print(f"   Invalid file state: {res_inv.get('state')} (status={res_inv.get('status')})")
    assert res_inv.get('state') == 'INVALID IMAGE'

    # C. No face detected
    black_img = np.zeros((300, 300, 3), dtype=np.uint8)
    _, black_bytes = cv2.imencode('.png', black_img)
    res_noface = service.analyse(black_bytes.tobytes())
    print(f"   No face detected state: {res_noface.get('state')} (status={res_noface.get('status')})")
    assert res_noface.get('state') == 'FACE NOT DETECTED'

    print("\nALL VERIFICATIONS PASSED PERFECTLY!")

if __name__ == '__main__':
    main()
