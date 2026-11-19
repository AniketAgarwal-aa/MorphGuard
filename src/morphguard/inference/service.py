from __future__ import annotations
import time
from pathlib import Path
from typing import Optional
import numpy as np
from ..preprocessing import FacePreprocessor
from ..feature_extraction import extract_features

class FeatureModelAdapter:
    def __init__(self, estimator, feature_key: str = "combined", threshold: float = 0.5):
        self.estimator = estimator
        self.feature_key = feature_key
        self.threshold = threshold

    def predict_score(self, rgb) -> float:
        features = extract_features(np.asarray(rgb))[self.feature_key].reshape(1, -1)
        if hasattr(self.estimator, "predict_proba"):
            return float(self.estimator.predict_proba(features)[0][1])
        return float(self.estimator.decision_function(features)[0])

def load_joblib_model(path: Path, feature_key: str = "combined", threshold: float = 0.5) -> FeatureModelAdapter:
    import joblib
    if not path.exists():
        raise FileNotFoundError(f"Model artifact not found: {path}")
    return FeatureModelAdapter(joblib.load(path), feature_key, threshold=threshold)

class PyTorchModelAdapter:
    def __init__(self, model, threshold: float = 0.5):
        self.model = model
        self.model.eval()
        self.threshold = threshold

    def predict_score(self, rgb) -> float:
        import torch
        arr = np.asarray(rgb, dtype=np.float32) / 255.0
        tensor = torch.from_numpy(arr.transpose(2, 0, 1)).float()
        mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
        tensor = (tensor - mean) / std
        tensor = tensor.unsqueeze(0)
        with torch.no_grad():
            out = self.model(tensor)
            prob = float(torch.softmax(out, dim=1)[0, 1].item())
        return prob

def load_pytorch_model(path: Path, architecture: str = "custom_cnn", threshold: float = 0.5) -> PyTorchModelAdapter:
    import torch
    from ..classification.models import create_model
    if not path.exists():
        raise FileNotFoundError(f"Model artifact not found: {path}")
    model = create_model(architecture)
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    state = checkpoint.get("model", checkpoint) if isinstance(checkpoint, dict) else checkpoint
    model.load_state_dict(state)
    return PyTorchModelAdapter(model, threshold=threshold)

class InferenceService:
    def __init__(self, model=None, preprocessor: Optional[FacePreprocessor] = None, uncertainty: tuple[float, float] = (0.40, 0.60), threshold: Optional[float] = None):
        self.model = model
        self.preprocessor = preprocessor or FacePreprocessor()
        self.uncertainty = uncertainty
        self.threshold = threshold

    def analyse(self, source) -> dict:
        started = time.perf_counter()
        try:
            image = self.preprocessor.load(source)
        except ValueError as exc:
            return {"state": "INVALID IMAGE", "error": str(exc)}
            
        faces = self.preprocessor.detect(image)
        if not faces:
            return {
                "state": "FACE NOT DETECTED",
                "face_count": 0,
                "processing_seconds": time.perf_counter() - started
            }
            
        face = faces[0]
        quality = self.preprocessor.quality(image, face).as_dict()
        rgb = self.preprocessor.transform(image, face)
        
        result = {
            "state": "MODEL UNAVAILABLE",
            "face_box": face,
            "face_count": len(faces),
            "quality": quality,
            "image": rgb
        }
        
        if self.model is not None:
            score = float(self.model.predict_score(rgb))
            active_thresh = self.threshold
            if active_thresh is None and hasattr(self.model, 'threshold'):
                active_thresh = self.model.threshold
            if active_thresh is None:
                active_thresh = 0.5
                
            # Determine state based on score & threshold
            is_morphed = score >= active_thresh
            
            # Uncertainty window around decision threshold
            unc_low = active_thresh - 0.05
            unc_high = active_thresh + 0.05
            if self.uncertainty and active_thresh == 0.5:
                unc_low, unc_high = self.uncertainty
                
            if unc_low <= score <= unc_high and 0.0 < active_thresh < 1.0:
                det_state = "UNCERTAIN"
            elif is_morphed:
                det_state = "MORPHED / MORPHING ATTACK"
            else:
                det_state = "GENUINE / BONA FIDE"
                
            result.update(
                score=score,
                decision_threshold=active_thresh,
                state=det_state,
                predicted_class="morphed" if is_morphed else "genuine"
            )
            
        result["processing_seconds"] = time.perf_counter() - started
        return result
