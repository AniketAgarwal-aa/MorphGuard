"""Hosted and local model artifact manager.

Supports lazy downloading of trained model artifacts from Hugging Face Hub or
remote object storage with SHA-256 integrity verification and offline local fallback.
"""
from __future__ import annotations
import hashlib, json, os, sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parents[3]
DEFAULT_HF_REPO = "AniketAgarwal-aa/MorphGuard-Models"

SUBFOLDERS = {
    'custom_cnn': 'deep_learning',
    'mobilenet_v3_small': 'deep_learning',
    'resnet18': 'deep_learning',
    'resnet34': 'deep_learning',
    'resnet50': 'deep_learning',
    'efficientnet_b0': 'deep_learning',
    'densenet121': 'deep_learning',
    'stacking_ensemble': 'ensembles',
    'voting_ensemble': 'ensembles',
}

class ModelUnavailableError(FileNotFoundError):
    """Raised when a requested model artifact is neither present locally nor retrievable remotely."""
    pass

def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def get_model_metadata(model_name: str) -> Optional[dict]:
    meta_path = ROOT / 'models/metadata' / f"{model_name}.json"
    if meta_path.exists():
        try:
            return json.loads(meta_path.read_text(encoding='utf-8'))
        except Exception:
            pass
    return None

def resolve_model_artifact(model_name: str, repo_id: Optional[str] = None, token: Optional[str] = None) -> Path:
    """Resolve model artifact path, checking local files first, then remote repositories.
    
    Args:
        model_name: Canonical model identifier (e.g. 'custom_cnn', 'combined_svm', 'stacking_ensemble')
        repo_id: Optional Hugging Face Hub repo id (defaults to 'AniketAgarwal-aa/MorphGuard-Models')
        token: Optional authentication token for private repositories
        
    Returns:
        Path to verified local artifact
    """
    clean_name = Path(model_name).stem
    is_pytorch = (
        SUBFOLDERS.get(clean_name) == 'deep_learning'
        or clean_name.startswith("custom_cnn")
        or model_name.endswith(".pt")
    )
    ext = ".pt" if is_pytorch else ".joblib"
    filename = f"{clean_name}{ext}"

    # 1. Check local standard directories
    local_candidates = [
        ROOT / 'models/trained' / filename,
        ROOT / 'models/checkpoints' / filename,
        ROOT / 'models/cache' / filename,
        ROOT / 'models/hf_export' / filename,
        ROOT / 'models/hf_export' / SUBFOLDERS.get(clean_name, 'classical') / filename,
    ]
    for cand in local_candidates:
        if cand.exists() and cand.stat().st_size > 0:
            return cand

    # Check metadata for expected artifact path
    meta = get_model_metadata(clean_name)
    if meta and meta.get('artifact_path'):
        rel_p = ROOT / meta['artifact_path']
        if rel_p.exists() and rel_p.stat().st_size > 0:
            return rel_p

    # 2. Check remote retrieval via Hugging Face Hub
    hub_repo = repo_id or os.environ.get('MORPHGUARD_MODEL_REPO') or os.environ.get('HF_REPO_ID')
    hf_token = token or os.environ.get('HF_TOKEN') or os.environ.get('HUGGING_FACE_HUB_TOKEN')
    
    # Try importing Streamlit secrets if running inside Streamlit
    if not hub_repo or not hf_token:
        try:
            import streamlit as st
            if not hub_repo:
                hub_repo = st.secrets.get("MORPHGUARD_MODEL_REPO") or st.secrets.get("HF_REPO_ID")
            if not hf_token:
                hf_token = st.secrets.get("HF_TOKEN") or st.secrets.get("HUGGING_FACE_HUB_TOKEN")
        except Exception:
            pass

    # Default to official MorphGuard repo if none specified
    if not hub_repo:
        hub_repo = DEFAULT_HF_REPO

    cache_dir = ROOT / 'models/cache'
    cache_dir.mkdir(parents=True, exist_ok=True)

    try:
        from huggingface_hub import hf_hub_download
        downloaded = None

        # Attempt download from subfolder first, then fallback to root
        subfolder = SUBFOLDERS.get(clean_name, 'classical')
        try:
            downloaded = hf_hub_download(
                repo_id=hub_repo,
                filename=filename,
                subfolder=subfolder,
                token=hf_token,
                local_dir=str(cache_dir)
            )
        except Exception:
            # Fallback to root level in repo
            downloaded = hf_hub_download(
                repo_id=hub_repo,
                filename=filename,
                token=hf_token,
                local_dir=str(cache_dir)
            )

        downloaded_path = Path(downloaded)
        if downloaded_path.exists() and downloaded_path.stat().st_size > 0:
            # Verify SHA-256 checksum if present in metadata
            if meta and meta.get('artifact_sha256'):
                actual_sha = compute_sha256(downloaded_path)
                if actual_sha != meta['artifact_sha256']:
                    downloaded_path.unlink(missing_ok=True)
                    raise ValueError(f"Checksum mismatch for {clean_name}: expected {meta['artifact_sha256']}, got {actual_sha}")
            return downloaded_path
    except Exception as exc:
        status_note = ""
        if meta:
            status_note = f" (Registry status: {meta.get('training_status', 'unknown')})"
        raise ModelUnavailableError(
            f"Model artifact '{filename}' could not be loaded locally or downloaded from Hugging Face repository '{hub_repo}'{status_note}. "
            f"Details: {exc}. If the repository is private, ensure HF_TOKEN is configured in Streamlit Secrets or environment variables."
        ) from exc

    raise ModelUnavailableError(f"Model artifact '{filename}' unavailable.")
