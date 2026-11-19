"""Train, calibrate, and evaluate all remaining deep learning models using cached tensors."""
import hashlib, json, os, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from morphguard.classification.models import create_model

class CachedTensorDataset(Dataset):
    def __init__(self, records: list[dict], tensor_dict: dict):
        self.samples = []
        for r in records:
            p = r['image_path']
            if p in tensor_dict:
                tensor = tensor_dict[p]
                label = 1 if r['verified_label'] == 'morphed' else 0
                self.samples.append((tensor, label, p))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

def find_optimal_threshold(y_true, scores):
    candidate_thresholds = np.unique(scores)
    best_thresh = 0.5
    best_acer = float('inf')
    for thresh in candidate_thresholds:
        preds = (scores >= thresh).astype(int)
        tp = np.sum((preds == 1) & (y_true == 1))
        tn = np.sum((preds == 0) & (y_true == 0))
        fp = np.sum((preds == 1) & (y_true == 0))
        fn = np.sum((preds == 0) & (y_true == 1))
        apcer = fn / (tp + fn) if (tp + fn) > 0 else 0.0
        bpcer = fp / (tn + fp) if (tn + fp) > 0 else 0.0
        acer = (apcer + bpcer) / 2.0
        if acer < best_acer:
            best_acer = acer
            best_thresh = float(thresh)
    return best_thresh

def compute_metrics(y_true, scores, thresh):
    preds = (scores >= thresh).astype(int)
    tp = int(np.sum((preds == 1) & (y_true == 1)))
    tn = int(np.sum((preds == 0) & (y_true == 0)))
    fp = int(np.sum((preds == 1) & (y_true == 0)))
    fn = int(np.sum((preds == 0) & (y_true == 1)))
    n = len(y_true)
    acc = (tp + tn) / n if n > 0 else 0.0
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    apcer = fn / (tp + fn) if (tp + fn) > 0 else 0.0
    bpcer = fp / (tn + fp) if (tn + fp) > 0 else 0.0
    acer = (apcer + bpcer) / 2.0
    roc_auc = float(roc_auc_score(y_true, scores)) if len(np.unique(y_true)) > 1 else None
    pr_auc = float(average_precision_score(y_true, scores)) if len(np.unique(y_true)) > 1 else None
    return {
        'threshold': round(float(thresh), 4),
        'accuracy': round(acc, 4),
        'precision': round(prec, 4),
        'recall': round(rec, 4),
        'specificity': round(spec, 4),
        'f1_score': round(f1, 4),
        'apcer': round(apcer, 4),
        'bpcer': round(bpcer, 4),
        'acer': round(acer, 4),
        'confusion_matrix': {'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn},
        'roc_auc': round(roc_auc, 4) if roc_auc is not None else None,
        'pr_auc': round(pr_auc, 4) if pr_auc is not None else None,
    }

def train_and_eval_architecture(model_name: str, tensor_dict: dict, manifest_df: pd.DataFrame, epochs: int = 5, batch_size: int = 32):
    print(f"\n=======================================================")
    print(f"TRAINING DEEP ARCHITECTURE: {model_name}")
    print(f"=======================================================")
    train_recs = manifest_df[manifest_df['split'] == 'train'].to_dict('records')
    val_recs = manifest_df[manifest_df['split'] == 'validation'].to_dict('records')
    test_recs = manifest_df[manifest_df['split'] == 'test'].to_dict('records')

    train_ds = CachedTensorDataset(train_recs, tensor_dict)
    val_ds = CachedTensorDataset(val_recs, tensor_dict)
    test_ds = CachedTensorDataset(test_recs, tensor_dict)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    torch.manual_seed(42)
    np.random.seed(42)

    model = create_model(model_name, pretrained=False)

    # Class weights to handle class imbalance (183 genuine vs 408 morphed)
    class_weights = torch.tensor([591.0 / (2.0 * 183.0), 591.0 / (2.0 * 408.0)]).float()
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4, weight_decay=1e-4)

    t0 = time.time()
    model.train()
    for ep in range(epochs):
        ep_loss = 0.0
        correct = 0
        total = 0
        for imgs, lbls, _ in train_loader:
            optimizer.zero_grad()
            out = model(imgs)
            loss = criterion(out, lbls)
            loss.backward()
            optimizer.step()
            ep_loss += loss.item() * len(lbls)
            preds = out.argmax(dim=1)
            correct += (preds == lbls).sum().item()
            total += len(lbls)
        acc = correct / total if total else 0.0
        print(f"  Epoch {ep+1}/{epochs} | Loss: {ep_loss/total:.4f} | Acc: {acc:.4f}")

    fit_duration = round(time.time() - t0, 3)
    print(f"Training completed in {fit_duration}s.")

    # 1. Validation evaluation & threshold calibration
    model.eval()
    val_scores, val_targets = [], []
    with torch.no_grad():
        for imgs, lbls, _ in val_loader:
            out = model(imgs)
            probs = torch.softmax(out, dim=1)[:, 1]
            val_scores.extend(probs.numpy().tolist())
            val_targets.extend(lbls.numpy().tolist())
    val_scores = np.array(val_scores)
    val_targets = np.array(val_targets)

    opt_thresh = find_optimal_threshold(val_targets, val_scores)
    print(f"Optimal threshold calibrated on Validation set: tau* = {opt_thresh:.4f}")

    # 2. Test evaluation on held-out test split
    test_scores, test_targets, test_paths = [], [], []
    with torch.no_grad():
        for imgs, lbls, paths in test_loader:
            out = model(imgs)
            probs = torch.softmax(out, dim=1)[:, 1]
            test_scores.extend(probs.numpy().tolist())
            test_targets.extend(lbls.numpy().tolist())
            test_paths.extend(paths)
    test_scores = np.array(test_scores)
    test_targets = np.array(test_targets)

    metrics_cal = compute_metrics(test_targets, test_scores, opt_thresh)
    metrics_def = compute_metrics(test_targets, test_scores, 0.5)

    print(f"Test Evaluation Results (285 samples):")
    print(f"  Default (0.50):    Acc = {metrics_def['accuracy']:.4f} | ACER = {metrics_def['acer']:.4f}")
    print(f"  Calibrated ({opt_thresh:.4f}): Acc = {metrics_cal['accuracy']:.4f} | ACER = {metrics_cal['acer']:.4f} | ROC-AUC = {metrics_cal['roc_auc']}")

    # 3. Save model checkpoint
    ckpt_dir = ROOT / 'models/checkpoints'
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    ckpt_path = ckpt_dir / f"{model_name}.pt"
    torch.save({
        'architecture': model_name,
        'state_dict': model.state_dict(),
        'calibrated_threshold': opt_thresh,
        'input_dimensions': [3, 224, 224]
    }, ckpt_path)

    # 4. Save raw prediction CSV
    pred_dir = ROOT / 'reports/predictions'
    pred_dir.mkdir(parents=True, exist_ok=True)
    pred_df = pd.DataFrame({
        'image_path': test_paths,
        'true_label': ['morphed' if y == 1 else 'genuine' for y in test_targets],
        'predicted_label_default': ['morphed' if s >= 0.5 else 'genuine' for s in test_scores],
        'predicted_label_calibrated': ['morphed' if s >= opt_thresh else 'genuine' for s in test_scores],
        'model_score': test_scores,
        'default_threshold': 0.5,
        'calibrated_threshold': opt_thresh,
        'model_version': '3.0.0',
        'split': 'test'
    })
    pred_df.to_csv(pred_dir / f"{model_name}_predictions.csv", index=False)

    # 5. Save metadata
    meta_dir = ROOT / 'models/metadata'
    meta_dir.mkdir(parents=True, exist_ok=True)
    meta = {
        'model_name': model_name,
        'architecture': model_name,
        'framework': 'PyTorch',
        'description': f'Deep convolutional neural network: {model_name}',
        'feature_key': 'raw_face_crop_224x224',
        'input_dimensions': [3, 224, 224],
        'training_samples': len(train_ds),
        'training_morphed': int((manifest_df[manifest_df['split'] == 'train']['verified_label'] == 'morphed').sum()),
        'training_genuine': int((manifest_df[manifest_df['split'] == 'train']['verified_label'] == 'genuine').sum()),
        'training_duration_seconds': fit_duration,
        'artifact_path': f"models/checkpoints/{model_name}.pt",
        'artifact_sha256': hashlib.sha256(ckpt_path.read_bytes()).hexdigest(),
        'training_date': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'training_status': 'trained',
        'validation_status': 'evaluated',
        'approval_status': 'approved_experimental_inference',
        'calibrated_threshold': opt_thresh,
        'default_threshold': 0.5,
        'metrics': metrics_cal,
        'uncalibrated_metrics': metrics_def
    }
    (meta_dir / f"{model_name}.json").write_text(json.dumps(meta, indent=2), encoding='utf-8')
    return meta

def main():
    print("Loading pre-cached tensors from data/cache/deep_face_crops.pt...")
    t0 = time.time()
    tensor_dict = torch.load(ROOT / 'data/cache/deep_face_crops.pt', weights_only=False)
    print(f"Loaded {len(tensor_dict)} tensors in {time.time() - t0:.2f}s.")

    manifest_df = pd.read_csv(ROOT / 'data/manifests/reviewed_label_manifest.csv')

    architectures = [
        'mobilenet_v3_small',
        'resnet18',
        'efficientnet_b0',
        'densenet121',
        'resnet34',
        'resnet50'
    ]

    all_meta = []
    for arch in architectures:
        meta = train_and_eval_architecture(arch, tensor_dict, manifest_df, epochs=5, batch_size=32)
        all_meta.append(meta)

    # Update unified model registry
    reg_path = ROOT / 'models/metadata/model_registry.json'
    registry = json.loads(reg_path.read_text(encoding='utf-8'))
    existing_models = {m['model_name']: m for m in registry.get('models', [])}

    for meta in all_meta:
        existing_models[meta['model_name']] = meta

    registry['models'] = list(existing_models.values())
    registry['last_updated'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    reg_path.write_text(json.dumps(registry, indent=2), encoding='utf-8')
    print("\nUpdated models/metadata/model_registry.json successfully with all trained models!")

if __name__ == '__main__':
    main()
