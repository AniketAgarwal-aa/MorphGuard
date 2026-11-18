from __future__ import annotations
import logging, os
from pathlib import Path

def project_root() -> Path:
    return Path(os.getenv("MORPHGUARD_ROOT", Path(__file__).resolve().parents[2]))

def model_dir() -> Path:
    return Path(os.getenv("MORPHGUARD_MODEL_DIR", project_root() / "models" / "trained"))

def configure_logging() -> None:
    logging.basicConfig(level=os.getenv("MORPHGUARD_LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s %(message)s")

def readiness() -> dict:
    root, models = project_root(), model_dir()
    count = len(list(models.glob("*.joblib"))) if models.exists() else 0
    return {"ready": root.exists() and models.exists() and count > 0, "mode": "inference" if count else "research-only (no approved model)", "model_directory": str(models), "model_count": count}
