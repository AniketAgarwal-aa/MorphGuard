from __future__ import annotations
import time
from pathlib import Path
import numpy as np
from ..preprocessing import FacePreprocessor
from ..feature_extraction import extract_features

class FeatureModelAdapter:
    def __init__(self, estimator, feature_key="combined"):
        self.estimator=estimator; self.feature_key=feature_key
    def predict_score(self, rgb):
        features=extract_features(np.asarray(rgb))[self.feature_key].reshape(1,-1)
        if hasattr(self.estimator,"predict_proba"): return float(self.estimator.predict_proba(features)[0][1])
        return float(self.estimator.decision_function(features)[0])

def load_joblib_model(path: Path, feature_key="combined"):
    import joblib
    if not path.exists(): raise FileNotFoundError(f"Model artifact not found: {path}")
    return FeatureModelAdapter(joblib.load(path),feature_key)

class InferenceService:
    def __init__(self, model=None, preprocessor=None, uncertainty=(.40,.60)):
        self.model=model; self.preprocessor=preprocessor or FacePreprocessor(); self.uncertainty=uncertainty
    def analyse(self, source):
        started=time.perf_counter()
        try: image=self.preprocessor.load(source)
        except ValueError as exc: return {"state":"INVALID IMAGE","error":str(exc)}
        faces=self.preprocessor.detect(image)
        if not faces: return {"state":"FACE NOT DETECTED","face_count":0,"processing_seconds":time.perf_counter()-started}
        face=faces[0]; quality=self.preprocessor.quality(image,face).as_dict(); rgb=self.preprocessor.transform(image,face)
        result={"state":"MODEL UNAVAILABLE","face_box":face,"face_count":len(faces),"quality":quality,"image":rgb}
        if self.model is not None:
            score=float(self.model.predict_score(rgb))
            result.update(score=score,state="UNCERTAIN" if self.uncertainty[0]<=score<=self.uncertainty[1] else ("MORPHED / MORPHING ATTACK" if score>.5 else "GENUINE / BONA FIDE"))
        result["processing_seconds"]=time.perf_counter()-started; return result
