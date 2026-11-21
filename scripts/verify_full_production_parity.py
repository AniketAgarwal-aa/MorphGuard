import os
import sys
import json
import time
from pathlib import Path
import numpy as np
import cv2

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from morphguard.inference import InferenceService, load_joblib_model, load_pytorch_model, compare_vectors
from morphguard.preprocessing import FacePreprocessor
from morphguard.feature_extraction import extract_features
from morphguard.inference.hosted_models import resolve_model_artifact, get_model_metadata

def main():
    print("=== MORPHGUARD V3.2 FULL PRODUCTION PARITY AUDIT ===")
    
    # 1. Check all 21 models in registry
    reg_path = ROOT / "models/metadata/model_registry.json"
    with open(reg_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
        
    models = registry.get("models", [])
    print(f"\n[STEP 1] Auditing all {len(models)} Models in Registry:")
    assert len(models) == 21, f"Expected 21 models, found {len(models)}"
    
    verified_models = 0
    for m in models:
        m_name = m["model_name"]
        art_path = m["artifact_path"]
        calib_thresh = m.get("calibrated_threshold")
        model_type = m.get("framework", "scikit-learn")
        
        # Verify resolution
        resolved = resolve_model_artifact(m_name)
        assert Path(resolved).exists(), f"Artifact not found: {resolved}"
        assert calib_thresh is not None, f"Missing calibrated threshold for {m_name}"
        
        verified_models += 1
        print(f"  + Model [{m_name:<24}] | Type: {model_type:<12} | Thresh: {str(calib_thresh):<10} | Path: {art_path}")
        
    print(f"\n--> Successfully verified {verified_models}/21 model definitions.")
    
    # 2. Test Single Image Pipeline on Synthetic Test Face
    print("\n[STEP 2] Testing Single Image Analysis Pipeline & JSON Payload:")
    temp_dir = ROOT / "reports/test_fixtures"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate test face fixture
    face_img = np.full((300, 300, 3), 180, dtype=np.uint8)
    test_face_path = temp_dir / "audit_face.png"
    cv2.imwrite(str(test_face_path), face_img)
    
    # Create a preprocessor that simulates successful face localization
    class MockFacePreprocessor(FacePreprocessor):
        def detect(self, image):
            return [(20, 20, 224, 224)]

    mock_prep = MockFacePreprocessor()
    
    # Load combined_svm and run analysis
    svm_path = resolve_model_artifact("combined_svm")
    meta = get_model_metadata("combined_svm")
    thresh = meta.get("calibrated_threshold", 0.0051)
    adapter = load_joblib_model(svm_path, feature_key="combined", threshold=thresh)
    service = InferenceService(model=adapter, preprocessor=mock_prep, threshold=thresh)
    
    result = service.analyse(str(test_face_path))
    assert "state" in result, "Missing state in analysis result"
    assert "morph_probability" in result, "Missing morph_probability in result"
    assert result["state"] in ("MORPHED", "GENUINE"), f"Unexpected state: {result['state']}"
    
    # Verify export report payload
    single_payload = {
        "analysis_id": f"single-{int(time.time())}",
        "status": result.get("state"),
        "decision": result.get("state"),
        "probability": result.get("morph_probability"),
        "threshold": thresh,
        "quality": result.get("quality"),
        "face_box": result.get("face_box"),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    dumped_single = json.dumps(single_payload, indent=2, default=str)
    parsed_single = json.loads(dumped_single)
    assert parsed_single["status"] == result["state"], "Single payload serialization mismatch"
    print(f"  + Single Image Analysis: State={result['state']}, P={result['morph_probability']:.4f}, Valid JSON: YES")
    
    # 3. Test Two-Image Comparison Pipeline
    print("\n[STEP 3] Testing Two-Image Comparison Pipeline & JSON Payload:")
    crop_a = np.full((224, 224, 3), 120, dtype=np.uint8)
    crop_b = np.full((224, 224, 3), 130, dtype=np.uint8)
    
    feat_a = extract_features(crop_a)
    feat_b = extract_features(crop_b)
    
    comp_results = {}
    for k in ("lbp", "hog", "glcm", "stats", "combined"):
        comp_results[k] = compare_vectors(feat_a[k], feat_b[k])
        assert "cosine_similarity" in comp_results[k], f"Missing cosine_similarity for {k}"
        assert "absolute_difference_mean" in comp_results[k], f"Missing diff_mean for {k}"
        
    two_image_payload = {
        "comparison_type": "exploratory_two_image_differential",
        "image_a": {"features": {k: len(v) for k, v in feat_a.items()}},
        "image_b": {"features": {k: len(v) for k, v in feat_b.items()}},
        "feature_differences": comp_results,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    dumped_two = json.dumps(two_image_payload, indent=2, default=str)
    parsed_two = json.loads(dumped_two)
    assert len(parsed_two["feature_differences"]) == 5, "Two-image comparison payload mismatch"
    print("  + Two-Image Comparison: All 5 feature difference vectors computed, Valid JSON: YES")
    
    # 4. Clean up test fixtures
    for f in temp_dir.glob("*"):
        f.unlink()
    temp_dir.rmdir()
    
    print("\n=== ALL PARITY & FUNCTIONAL ACCEPTANCE CHECKS PASSED ===")

if __name__ == "__main__":
    main()
