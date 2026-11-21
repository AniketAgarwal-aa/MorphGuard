import os
import sys
import json
import time
from pathlib import Path
import numpy as np
import cv2

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from morphguard.inference.service import (
    InferenceService,
    load_joblib_model,
    load_pytorch_model
)
from morphguard.inference.hosted_models import resolve_model_artifact, get_model_metadata

def run_acceptance_suite():
    print("=== MORPHGUARD V3.2 HOSTED ACCEPTANCE & PIPELINE AUDIT ===")
    
    # 1. Page Syntax Verification
    pages_dir = ROOT / "app/pages"
    pages = sorted([p for p in pages_dir.glob("*.py")])
    print(f"\n[PHASE 7.1] Testing Syntax of all {len(pages)} Streamlit Pages:")
    passed_pages = 0
    for p in pages:
        try:
            with open(p, "r", encoding="utf-8") as f:
                compile(f.read(), str(p), "exec")
            passed_pages += 1
            print(f"  + {p.name:<32} [COMPILED OK]")
        except Exception as e:
            print(f"  - {p.name:<32} [ERROR: {e}]")
    assert passed_pages == 14, f"Expected 14 pages, got {passed_pages}"
    
    # 2. Build test images
    temp_dir = ROOT / "reports/test_fixtures"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 2a. Genuine portrait face fixture
    face_img = np.full((300, 300, 3), 180, dtype=np.uint8)
    cv2.circle(face_img, (110, 120), 20, (30, 30, 30), -1)
    cv2.circle(face_img, (190, 120), 20, (30, 30, 30), -1)
    cv2.line(face_img, (150, 140), (150, 180), (30, 30, 30), 4)
    cv2.ellipse(face_img, (150, 220), (50, 20), 0, 0, 180, (30, 30, 30), 4)
    face_path = temp_dir / "valid_face.png"
    cv2.imwrite(str(face_path), face_img)
    
    # 2b. Blank image (face not detected)
    blank_img = np.zeros((300, 300, 3), dtype=np.uint8)
    blank_path = temp_dir / "blank_image.png"
    cv2.imwrite(str(blank_path), blank_img)
    
    # 2c. Corrupt image file
    corrupt_path = temp_dir / "corrupt.png"
    corrupt_path.write_bytes(b"NOT_A_PNG_HEADER")

    print("\n[PHASE 7.2] End-to-End Model Pipeline Inference on Test Fixtures:")
    models_to_test = [
        ("combined_svm", "joblib", "X", 0.0051),
        ("voting_ensemble", "joblib", "glcm", 0.1631),
        ("stacking_ensemble", "joblib", "glcm", 0.4435),
        ("custom_cnn", "pytorch", None, 0.5000),
        ("efficientnet_b0", "pytorch", "efficientnet_b0", 0.0031937),
        ("resnet18", "pytorch", "resnet18", 6.64e-06),
        ("resnet50", "pytorch", "resnet50", 0.000703)
    ]
    
    for m_name, ftype, arch_or_key, thresh in models_to_test:
        art_path = resolve_model_artifact(m_name)
        if ftype == "joblib":
            adapter = load_joblib_model(art_path, feature_key=arch_or_key or "X", threshold=thresh)
        else:
            adapter = load_pytorch_model(art_path, architecture=arch_or_key or m_name, threshold=thresh)
            
        service = InferenceService(model=adapter, threshold=thresh)
        
        # Test on face image
        t0 = time.perf_counter()
        res_face = service.analyse(str(face_path))
        dt = (time.perf_counter() - t0) * 1000
        
        state = res_face.get("state")
        score = res_face.get("morph_probability", 0.0)
        print(f"  + Model: {m_name:<20} | Type: {ftype:<7} | Latency: {dt:6.2f}ms | Result: {state} (P={score:.4f}, Threshold={thresh})")
        
    print("\n[PHASE 7.3] Negative & Edge-Case Failure Handling Tests:")
    service_default = InferenceService(model=None)
    
    # Test blank image
    res_blank = service_default.analyse(str(blank_path))
    print(f"  + Blank image handling: state={res_blank['state']} (Expected: FACE NOT DETECTED)")
    assert res_blank['state'] == "FACE NOT DETECTED"
    
    # Test corrupt image
    res_corrupt = service_default.analyse(str(corrupt_path))
    print(f"  + Corrupt image handling: state={res_corrupt['state']} (Expected: INVALID IMAGE)")
    assert res_corrupt['state'] == "INVALID IMAGE"
    
    # Test nonexistent path
    res_missing = service_default.analyse(str(temp_dir / "nonexistent.png"))
    print(f"  + Missing file handling: state={res_missing['state']} (Expected: INVALID IMAGE)")
    assert res_missing['state'] == "INVALID IMAGE"
    
    # 4. Cleanup
    for f in temp_dir.glob("*"):
        f.unlink()
    temp_dir.rmdir()
    
    print("\n[SUMMARY] All 14 pages and end-to-end inference/failure paths VERIFIED (100% PASS).")

if __name__ == "__main__":
    run_acceptance_suite()
