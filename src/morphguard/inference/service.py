from __future__ import annotations
import time
from pathlib import Path
from typing import Optional
import numpy as np
from ..preprocessing import FacePreprocessor
from ..feature_extraction import extract_features

class FeatureModelAdapter:
    def __init__(self, estimator, feature_key: str = "combined", threshold: float = 0.5, model_name: str = "feature_model"):
        self.estimator = estimator
        self.feature_key = feature_key
        self.threshold = threshold
        self.model_name = model_name

    def predict_score(self, rgb) -> float:
        feat_dict = extract_features(np.asarray(rgb))
        if not feat_dict or self.feature_key not in feat_dict:
            raise ValueError(f"Feature key '{self.feature_key}' could not be extracted from input image.")
        features = feat_dict[self.feature_key].reshape(1, -1)
        
        # Determine morph probability from estimator
        if hasattr(self.estimator, "predict_proba"):
            probs = self.estimator.predict_proba(features)
            # Find class index corresponding to morph attack (class 1 or 'morphed')
            classes = getattr(self.estimator, "classes_", None)
            morph_idx = 1
            if classes is not None and len(classes) == 2:
                if 1 in classes:
                    morph_idx = int(np.where(classes == 1)[0][0])
                elif 'morphed' in classes:
                    morph_idx = int(np.where(classes == 'morphed')[0][0])
            if probs.ndim == 2 and probs.shape[1] > morph_idx:
                return float(probs[0, morph_idx])
            return float(probs[0, -1])
            
        elif hasattr(self.estimator, "decision_function"):
            return float(self.estimator.decision_function(features)[0])
        elif hasattr(self.estimator, "predict"):
            return float(self.estimator.predict(features)[0])
            
        raise ValueError(f"Estimator {type(self.estimator)} has no predict_proba, decision_function, or predict method.")

def load_joblib_model(path: Path, feature_key: str = "combined", threshold: float = 0.5) -> FeatureModelAdapter:
    import joblib
    if not path.exists():
        raise FileNotFoundError(f"Model artifact not found: {path}")
    return FeatureModelAdapter(joblib.load(path), feature_key, threshold=threshold, model_name=path.name)

class PyTorchModelAdapter:
    def __init__(self, model, threshold: float = 0.5, model_name: str = "custom_cnn.pt"):
        self.model = model
        self.model.eval()
        self.threshold = threshold
        self.model_name = model_name

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

def load_pytorch_model(path: Path, architecture: Optional[str] = None, threshold: Optional[float] = None) -> PyTorchModelAdapter:
    import torch
    from ..classification.models import create_model
    if not path.exists():
        raise FileNotFoundError(f"Model artifact not found: {path}")
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)

    arch = architecture
    if not arch and isinstance(checkpoint, dict):
        arch = checkpoint.get("architecture")
    if not arch:
        arch = path.stem
    if not arch:
        arch = "custom_cnn"

    model = create_model(arch)
    if isinstance(checkpoint, dict):
        if "state_dict" in checkpoint:
            state = checkpoint["state_dict"]
        elif "model" in checkpoint:
            state = checkpoint["model"]
        else:
            state = checkpoint
    else:
        state = checkpoint

    model.load_state_dict(state)

    thresh = threshold
    if thresh is None and isinstance(checkpoint, dict):
        thresh = checkpoint.get("calibrated_threshold")
    if thresh is None:
        thresh = 0.5

    return PyTorchModelAdapter(model, threshold=thresh, model_name=path.name)

class InferenceService:
    def __init__(self, model=None, preprocessor: Optional[FacePreprocessor] = None, uncertainty: Optional[tuple[float, float]] = None, threshold: Optional[float] = None):
        self.model = model
        self.preprocessor = preprocessor or FacePreprocessor()
        self.uncertainty = uncertainty
        self.threshold = threshold

    def analyse(self, source) -> dict:
        started = time.perf_counter()
        
        # 1. Load and decode image
        try:
            image = self.preprocessor.load(source)
        except ValueError as exc:
            return {
                "state": "INVALID IMAGE",
                "error": str(exc),
                "status": "FAILED",
                "processing_seconds": time.perf_counter() - started
            }
        except Exception as exc:
            return {
                "state": "INVALID IMAGE",
                "error": f"Image load failed: {exc}",
                "status": "FAILED",
                "processing_seconds": time.perf_counter() - started
            }
            
        if image is None or image.size == 0:
            return {
                "state": "INVALID IMAGE",
                "error": "Image is empty or unreadable.",
                "status": "FAILED",
                "processing_seconds": time.perf_counter() - started
            }

        # 2. Detect face
        try:
            faces = self.preprocessor.detect(image)
        except Exception as exc:
            return {
                "state": "INFERENCE ERROR",
                "error": f"Face detection failure: {exc}",
                "status": "FAILED",
                "processing_seconds": time.perf_counter() - started
            }
            
        if not faces:
            return {
                "state": "FACE NOT DETECTED",
                "face_count": 0,
                "error": "No face detected in the input image. Ensure a clear, upright portrait capture.",
                "status": "FAILED",
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
            "image": rgb,
            "status": "NO_MODEL"
        }
        
        if self.model is None:
            result["processing_seconds"] = time.perf_counter() - started
            return result

        # 3. Model Inference & Decision
        try:
            score = float(self.model.predict_score(rgb))
            if np.isnan(score) or np.isinf(score):
                raise ValueError("Model output is NaN or Inf")
        except ValueError as exc:
            if "Feature key" in str(exc):
                result.update(
                    state="FEATURE EXTRACTION FAILED",
                    error=str(exc),
                    status="FAILED",
                    processing_seconds=time.perf_counter() - started
                )
            else:
                result.update(
                    state="INFERENCE ERROR",
                    error=f"Model prediction failed: {exc}",
                    status="FAILED",
                    processing_seconds=time.perf_counter() - started
                )
            return result
        except Exception as exc:
            result.update(
                state="INFERENCE ERROR",
                error=f"Model prediction failed: {exc}",
                status="FAILED",
                processing_seconds=time.perf_counter() - started
            )
            return result

        active_thresh = self.threshold
        if active_thresh is None and hasattr(self.model, 'threshold'):
            active_thresh = self.model.threshold
        if active_thresh is None:
            active_thresh = 0.5

        # Strict binary classification based on verified decision threshold
        # Morph probability >= threshold -> MORPHED
        # Morph probability < threshold -> GENUINE
        is_morphed = score >= active_thresh
        det_state = "MORPHED" if is_morphed else "GENUINE"
        predicted_class = "morphed" if is_morphed else "genuine"
        model_name = getattr(self.model, 'model_name', 'active_model')

        explanation = (
            f"Model '{model_name}' produced a morph probability of {score:.4f}, "
            f"which {'meets or exceeds' if is_morphed else 'is below'} the verified decision threshold "
            f"of {active_thresh:.4f}. Classified as {det_state}."
        )

        result.update(
            score=score,
            morph_probability=score,
            decision_threshold=active_thresh,
            state=det_state,
            predicted_class=predicted_class,
            explanation=explanation,
            model_name=model_name,
            status="SUCCESS",
            processing_seconds=time.perf_counter() - started
        )
        return result
