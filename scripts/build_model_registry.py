"""Consolidate all trained and implemented architectures into a unified model registry."""
import sys, json, hashlib
from pathlib import Path

ROOT = Path(__file__).parents[1]
META_DIR = ROOT / 'models' / 'metadata'

def main():
    META_DIR.mkdir(parents=True, exist_ok=True)
    registry = {
        'registry_version': '1.0.0',
        'last_updated': '2026-11-18T19:50:00Z',
        'models': []
    }

    # Load all individual metadata files
    for p in sorted(META_DIR.glob('*.json')):
        if p.name == 'model_registry.json':
            continue
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
            registry['models'].append(data)
        except Exception as e:
            print(f"Error loading {p}: {e}")

    # Add implemented architectures that are ready for training/GPU
    deep_catalog = [
        {
            'model_name': 'resnet18',
            'architecture': 'ResNet-18',
            'framework': 'PyTorch',
            'feature_key': 'raw_face_crop_224x224',
            'input_dimensions': [3, 224, 224],
            'training_status': 'ready_for_training',
            'validation_status': 'pending_training',
            'approval_status': 'experimental_prototype',
            'artifact_path': None,
            'artifact_sha256': None,
            'metrics': {'status': 'Untrained - awaiting compute cluster'}
        },
        {
            'model_name': 'efficientnet_b0',
            'architecture': 'EfficientNet-B0',
            'framework': 'PyTorch',
            'feature_key': 'raw_face_crop_224x224',
            'input_dimensions': [3, 224, 224],
            'training_status': 'ready_for_training',
            'validation_status': 'pending_training',
            'approval_status': 'experimental_prototype',
            'artifact_path': None,
            'artifact_sha256': None,
            'metrics': {'status': 'Untrained - awaiting compute cluster'}
        }
    ]

    existing_names = {m['model_name'] for m in registry['models']}
    for d in deep_catalog:
        if d['model_name'] not in existing_names:
            registry['models'].append(d)

    out_file = META_DIR / 'model_registry.json'
    out_file.write_text(json.dumps(registry, indent=2), encoding='utf-8')
    print(f"Unified model registry created with {len(registry['models'])} models at {out_file.relative_to(ROOT)}")

if __name__ == '__main__':
    main()
