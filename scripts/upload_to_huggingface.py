"""Prepare and upload MorphGuard trained model artifacts to Hugging Face Hub.

Target Repository: AniketAgarwal-aa/MorphGuard-Models
Artifacts:
  - classical/: Scikit-Learn baseline and tree models (*.joblib)
  - deep_learning/: PyTorch neural network checkpoints (*.pt)
  - ensembles/: Stacking and voting ensemble models (*.joblib)
  - metadata/: Model registry and architecture metadata (*.json)
  - README.md: Repository documentation and model cards
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, sys
from pathlib import Path

ROOT = Path(__file__).parents[1]

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

def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def prepare_export_directory(export_dir: Path) -> dict[str, Path]:
    """Assemble verified trained model artifacts and metadata into export tree."""
    export_dir.mkdir(parents=True, exist_ok=True)
    (export_dir / 'classical').mkdir(exist_ok=True)
    (export_dir / 'deep_learning').mkdir(exist_ok=True)
    (export_dir / 'ensembles').mkdir(exist_ok=True)
    (export_dir / 'metadata').mkdir(exist_ok=True)

    staged_artifacts = {}
    trained_dir = ROOT / 'models/trained'
    checkpoints_dir = ROOT / 'models/checkpoints'
    meta_dir = ROOT / 'models/metadata'

    # 1. Classical & Ensemble Models
    for joblib_path in sorted(trained_dir.glob('*.joblib')):
        name = joblib_path.stem
        sub = SUBFOLDERS.get(name, 'classical')
        dest = export_dir / sub / joblib_path.name
        shutil.copy2(joblib_path, dest)
        staged_artifacts[name] = dest
        # Also copy to root of export_dir for maximum download compatibility
        shutil.copy2(joblib_path, export_dir / joblib_path.name)

    # 2. Deep Learning Checkpoints
    for pt_path in sorted(checkpoints_dir.glob('*.pt')):
        name = pt_path.stem
        sub = 'deep_learning'
        dest = export_dir / sub / pt_path.name
        shutil.copy2(pt_path, dest)
        staged_artifacts[name] = dest
        shutil.copy2(pt_path, export_dir / pt_path.name)

    # 3. Metadata
    for json_path in sorted(meta_dir.glob('*.json')):
        shutil.copy2(json_path, export_dir / 'metadata' / json_path.name)
        if json_path.name == 'model_registry.json':
            shutil.copy2(json_path, export_dir / json_path.name)

    # 4. Model Card README
    readme_content = f"""---
license: apache-2.0
tags:
- biometrics
- facial-morphing-detection
- computer-vision
- pytorch
- scikit-learn
datasets:
- MONOT
- ONOT
metrics:
- accuracy
- acer
- apcer
- bpcer
- roc_auc
---

# MorphGuard-Models: Facial Morph Attack Detection Artifacts

Trained model artifacts, ensembles, and evaluation metadata for the **MorphGuard V3.0** research platform.

- **Source Code Repository:** [https://github.com/AniketAgarwal-aa/MorphGuard](https://github.com/AniketAgarwal-aa/MorphGuard)
- **Live Application:** Streamlit Community Cloud
- **Standard Protocol:** ISO/IEC 30107-3 Biometric Presentation Attack Detection

## Structure
- `classical/`: Scikit-Learn classifiers trained on 6,103D multi-scale texture features (LBP, HOG, GLCM, pixel statistics).
  - Top model: `combined_svm.joblib` (96.49% Test Accuracy, 0.0680 ACER, 0.9878 ROC-AUC).
  - Linear models: `logistic_regression.joblib`, `linear_svm.joblib`, `hog_svm.joblib`.
  - Tree ensembles: `extra_trees.joblib`, `rf_combined.joblib`, `hist_gradient_boosting.joblib`.
- `deep_learning/`: PyTorch deep neural networks.
  - `custom_cnn.pt`: Convolutional neural network trained on 224x224 face crops (87.72% Test Accuracy, 0.1096 ACER).
- `ensembles/`: Multi-model decision fusion.
  - `voting_ensemble.joblib` (89.12% Test Accuracy).
  - `stacking_ensemble.joblib` (88.07% Test Accuracy).
- `metadata/`: Architecture JSON descriptors and `model_registry.json`.

## Evaluation Summary (Held-Out Test Split: 285 Unseen Samples, Zero Identity Leakage)
All decision thresholds are optimized on an independent validation split by minimizing ACER.

| Architecture | Artifact | Test Accuracy | ACER | APCER | BPCER | ROC-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Combined SVM (RBF)** | `combined_svm.joblib` | **96.49%** | **0.0680** | 0.0132 | 0.1228 | **0.9878** |
| **Logistic Regression** | `logistic_regression.joblib` | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9769** |
| **HOG SVM** | `hog_svm.joblib` | **96.14%** | **0.0899** | 0.0044 | 0.1754 | **0.9867** |
| **Hist Gradient Boosting** | `hist_gradient_boosting.joblib` | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9911** |
| **Extra Trees** | `extra_trees.joblib` | **95.44%** | **0.1140** | 0.0000 | 0.2281 | **0.9950** |
| **Random Forest Combined** | `rf_combined.joblib` | **95.09%** | **0.1228** | 0.0000 | 0.2456 | **0.9879** |
| **Voting Ensemble** | `voting_ensemble.joblib` | **89.12%** | **0.1535** | 0.0789 | 0.2281 | 0.8688 |
| **Stacking Ensemble** | `stacking_ensemble.joblib` | **88.07%** | **0.1338** | 0.1096 | 0.1579 | **0.9044** |
| **Custom CNN** | `custom_cnn.pt` | **87.72%** | **0.1096** | 0.1316 | 0.0877 | **0.9601** |

*Disclaimer:* MorphGuard models are experimental research artifacts developed on MONOT Delaunay mesh morphs and do not constitute certified operational biometric security products.
"""
    (export_dir / 'README.md').write_text(readme_content, encoding='utf-8')
    return staged_artifacts

def main():
    p = argparse.ArgumentParser(description="Upload MorphGuard models to Hugging Face Hub")
    p.add_argument('--repo-id', default="AniketAgarwal-aa/MorphGuard-Models", help="Hugging Face repo id")
    p.add_argument('--token', default=None, help="Hugging Face access token (write access)")
    p.add_argument('--export-dir', type=Path, default=ROOT / 'models/hf_export', help="Local export staging directory")
    p.add_argument('--dry-run', action='store_true', help="Stage files locally without uploading")
    args = p.parse_args()

    token = args.token or os.environ.get('HF_TOKEN') or os.environ.get('HUGGING_FACE_HUB_TOKEN')
    
    print(f"Staging artifacts in {args.export_dir}...")
    staged = prepare_export_directory(args.export_dir)
    print(f"Successfully staged {len(staged)} model artifacts and metadata files.")
    
    # Print staged files and sizes
    total_size = sum(f.stat().st_size for f in args.export_dir.rglob('*') if f.is_file())
    print(f"Total staged size: {total_size / (1024*1024):.2f} MB")
    for name, dest in sorted(staged.items()):
        print(f"  - {name:<24} -> {dest.relative_to(args.export_dir)} ({dest.stat().st_size / 1024:.1f} KB)")

    if args.dry_run or not token:
        print("\n[NOTE] No write token provided or --dry-run requested.")
        print(f"Artifacts are ready in local staging directory: {args.export_dir}")
        print("\nTo upload to Hugging Face Hub, run:")
        print(f"  .\\.venv\\Scripts\\python.exe scripts/upload_to_huggingface.py --token <YOUR_HF_WRITE_TOKEN>")
        print("Or using the Hugging Face CLI:")
        print(f"  huggingface-cli upload {args.repo_id} models/hf_export .")
        return

    print(f"\nUploading to Hugging Face Hub: {args.repo_id}...")
    try:
        from huggingface_hub import HfApi
        api = HfApi(token=token)
        api.upload_folder(
            folder_path=str(args.export_dir),
            repo_id=args.repo_id,
            repo_type="model",
            commit_message="MorphGuard V3.0 — Upload calibrated model artifacts and metadata"
        )
        print(f"Successfully uploaded all model artifacts to https://huggingface.co/{args.repo_id}!")
    except Exception as exc:
        print(f"Upload failed: {exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
