"""Train and evaluate deep convolutional neural network architectures for morph detection."""
from __future__ import annotations
import argparse, hashlib, json, time, sys
from pathlib import Path
import cv2
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))

from morphguard.classification.models import create_model
from morphguard.preprocessing import FacePreprocessor
from morphguard.training.engine import train_epoch, save_checkpoint
from morphguard.dataset.labels import approved_rows

class FaceDataset(Dataset):
    def __init__(self, records: list[dict], root: Path):
        self.items = []
        pre = FacePreprocessor(image_size=224)
        for r in records:
            p = root / r['image_path']
            if p.exists():
                bgr = pre.load(str(p))
                if bgr is not None:
                    faces = pre.detect(bgr)
                    crop_rgb = pre.transform(bgr, faces[0] if faces else None)
                    # Convert to PyTorch tensor (C, H, W) normalized to [0, 1]
                    tensor = torch.from_numpy(crop_rgb.transpose(2, 0, 1)).float() / 255.0
                    # Standardize with ImageNet stats
                    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
                    std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
                    tensor = (tensor - mean) / std
                    label = 1 if r['verified_label'] == 'morphed' else 0
                    self.items.append((tensor, label))

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]

def train_deep_model(model_name: str, manifest_path: Path, epochs: int = 5, batch_size: int = 16):
    reviewed = approved_rows(manifest_path, ROOT)
    train_recs = [r for r in reviewed if r['split'] == 'train']
    val_recs = [r for r in reviewed if r['split'] == 'validation']
    test_recs = [r for r in reviewed if r['split'] == 'test']

    print(f"Loading datasets for {model_name}... (Train: {len(train_recs)}, Val: {len(val_recs)}, Test: {len(test_recs)})")
    train_ds = FaceDataset(train_recs, ROOT)
    val_ds = FaceDataset(val_recs, ROOT)
    test_ds = FaceDataset(test_recs, ROOT)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    eval_loader = DataLoader(test_ds if len(test_ds) >= 10 else val_ds, batch_size=batch_size, shuffle=False)

    model = create_model(model_name, pretrained=False)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)

    t0 = time.time()
    history = []
    for epoch in range(epochs):
        ep_res = train_epoch(model, train_loader, optimizer, criterion)
        history.append(ep_res)
        print(f"  Epoch {epoch+1}/{epochs} - Loss: {ep_res['loss']:.4f} - Acc: {ep_res['accuracy']:.4f}")

    fit_duration = round(time.time() - t0, 3)

    # Evaluate on held-out test split
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for imgs, lbls in eval_loader:
            logits = model(imgs)
            preds = logits.argmax(1)
            all_preds.extend(preds.tolist())
            all_labels.extend(lbls.tolist())

    y_eval = np.array(all_labels)
    preds = np.array(all_preds)

    tp = int(np.sum((preds == 1) & (y_eval == 1)))
    tn = int(np.sum((preds == 0) & (y_eval == 0)))
    fp = int(np.sum((preds == 1) & (y_eval == 0)))
    fn = int(np.sum((preds == 0) & (y_eval == 1)))

    total = len(y_eval)
    acc = (tp + tn) / total if total else 0.0
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) else 0.0
    apcer = fn / (tp + fn) if (tp + fn) else 0.0
    bpcer = fp / (tn + fp) if (tn + fp) else 0.0
    acer = (apcer + bpcer) / 2.0

    metrics = {
        'evaluation_split': 'test' if len(test_ds) >= 10 else 'validation',
        'eval_samples': total,
        'eval_morphed': int(np.sum(y_eval == 1)),
        'eval_genuine': int(np.sum(y_eval == 0)),
        'accuracy': round(acc, 4),
        'precision': round(prec, 4),
        'recall': round(rec, 4),
        'f1_score': round(f1, 4),
        'apcer': round(apcer, 4),
        'bpcer': round(bpcer, 4),
        'acer': round(acer, 4),
        'confusion_matrix': {'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}
    }

    ckpt_dir = ROOT / 'models' / 'checkpoints'
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    ckpt_path = ckpt_dir / f"{model_name}.pt"
    save_checkpoint(ckpt_path, model, optimizer, epoch=epochs, history=history)

    meta_dir = ROOT / 'models' / 'metadata'
    meta_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        'model_name': model_name,
        'architecture': model_name,
        'framework': 'PyTorch',
        'feature_key': 'raw_face_crop_224x224',
        'input_dimensions': [3, 224, 224],
        'training_samples': len(train_ds),
        'training_duration_seconds': fit_duration,
        'training_manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        'artifact_path': str(ckpt_path.relative_to(ROOT)).replace('\\', '/'),
        'artifact_sha256': hashlib.sha256(ckpt_path.read_bytes()).hexdigest(),
        'training_date': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'training_status': 'trained',
        'validation_status': 'evaluated',
        'approval_status': 'approved_experimental_inference',
        'metrics': metrics
    }

    meta_file = meta_dir / f"{model_name}.json"
    meta_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print(f"Deep Model saved: {ckpt_path.name} | Acc: {metrics['accuracy']} | ACER: {metrics['acer']}")
    return metadata

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', choices=['custom_cnn', 'resnet18', 'efficientnet_b0', 'all'], default='custom_cnn')
    p.add_argument('--manifest', type=Path, default=ROOT / 'data/manifests/reviewed_label_manifest.csv')
    p.add_argument('--epochs', type=int, default=5)
    args = p.parse_args()

    models = ['custom_cnn', 'resnet18', 'efficientnet_b0'] if args.model == 'all' else [args.model]
    for m in models:
        train_deep_model(m, args.manifest, epochs=args.epochs)

if __name__ == '__main__':
    main()
