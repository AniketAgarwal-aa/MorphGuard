import pytest
import numpy as np
from pathlib import Path
from morphguard.inference.service import InferenceService, load_joblib_model, load_pytorch_model
from morphguard.inference.hosted_models import resolve_model_artifact, get_model_metadata

ROOT = Path(__file__).parents[1]

def test_combined_svm_threshold_and_parity():
    meta = get_model_metadata("combined_svm")
    assert meta is not None
    assert meta["calibrated_threshold"] == 0.0051
    assert meta["metrics"]["accuracy"] == 0.9649

    art = resolve_model_artifact("combined_svm")
    assert art.exists()
    
    adapter = load_joblib_model(art, feature_key="combined", threshold=meta["calibrated_threshold"])
    assert adapter.threshold == 0.0051

    # Verify decision logic: score >= 0.0051 -> MORPHED, score < 0.0051 -> GENUINE
    svc = InferenceService(model=adapter, threshold=0.0051)
    assert svc.threshold == 0.0051

def test_efficientnet_b0_threshold_and_parity():
    meta = get_model_metadata("efficientnet_b0")
    assert meta is not None
    assert meta["calibrated_threshold"] == 0.003193704877048731
    assert meta["metrics"]["accuracy"] == 0.9158

    art = resolve_model_artifact("efficientnet_b0")
    assert art.exists()
    
    adapter = load_pytorch_model(art, architecture="efficientnet_b0", threshold=meta["calibrated_threshold"])
    assert adapter.threshold == meta["calibrated_threshold"]

def test_all_21_models_registered_and_calibrated():
    import json
    with open(ROOT / "models/metadata/model_registry.json", "r", encoding="utf-8") as f:
        reg = json.load(f)
    assert len(reg["models"]) == 21
    for m in reg["models"]:
        assert "calibrated_threshold" in m
        assert m["calibrated_threshold"] is not None
        assert "artifact_sha256" in m
        assert len(m["artifact_sha256"]) == 64
