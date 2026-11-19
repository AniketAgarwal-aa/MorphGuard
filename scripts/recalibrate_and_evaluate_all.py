"""Scientific Recalibration, Threshold Optimization & Test Prediction Logging.

Optimizes decision thresholds on the independent VALIDATION split (never the test split),
evaluates all models on the held-out TEST split, logs raw prediction artifacts, and
updates model metadata with both default and calibrated ISO/IEC 30107-3 metrics.
"""
from __future__ import annotations
import hashlib, json, os, sys, time
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
import torch

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))

from scripts.train_expanded_models import MODEL_SPECS
from morphguard.classification.models import create_model

PRED_DIR = ROOT / 'reports/predictions'
PRED_DIR.mkdir(parents=True, exist_ok=True)
META_DIR = ROOT / 'models/metadata'
META_DIR.mkdir(parents=True, exist_ok=True)
TRAINED_DIR = ROOT / 'models/trained'
TRAINED_DIR.mkdir(parents=True, exist_ok=True)

def load_feature_splits(feature_dir: Path, path_to_info: dict, feat_key: str):
    shards = sorted(feature_dir.glob('features_*.npz'))
    X_tr, y_tr, p_tr = [], [], []
    X_val, y_val, p_val = [], [], []
    X_te, y_te, p_te = [], [], []

    for s in shards:
        with np.load(s) as z:
            paths = [str(p).replace('\\', '/') for p in z['paths']]
            matched = [(idx, p, path_to_info[p]) for idx, p in enumerate(paths) if p in path_to_info]
            if matched:
                data = z[feat_key]
                for idx, p, info in matched:
                    vec = data[idx].astype(np.float32)
                    lbl = info['label']
                    sp = info['split']
                    if sp == 'train':
                        X_tr.append(vec); y_tr.append(lbl); p_tr.append(p)
                    elif sp == 'validation':
                        X_val.append(vec); y_val.append(lbl); p_val.append(p)
                    elif sp == 'test':
                        X_te.append(vec); y_te.append(lbl); p_te.append(p)

    return (
        np.asarray(X_tr, dtype=np.float32), np.asarray(y_tr, dtype=np.int64), p_tr,
        np.asarray(X_val, dtype=np.float32), np.asarray(y_val, dtype=np.int64), p_val,
        np.asarray(X_te, dtype=np.float32), np.asarray(y_te, dtype=np.int64), p_te,
    )

def compute_metrics_at_threshold(y_true: np.ndarray, y_score: np.ndarray, threshold: float):
    y_pred = (y_score >= threshold).astype(int)
    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    tn = int(np.sum((y_pred == 0) & (y_true == 0)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))
    total = len(y_true)

    acc = (tp + tn) / total if total else 0.0
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    spec = tn / (tn + fp) if (tn + fp) else 0.0
    f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) else 0.0
    apcer = fn / (tp + fn) if (tp + fn) else 0.0  # False Non-Match Rate for Attacks (Missed Morph)
    bpcer = fp / (tn + fp) if (tn + fp) else 0.0  # False Match Rate for Bona Fide (Genuine classified as Morph)
    acer = (apcer + bpcer) / 2.0

    return {
        'threshold': round(float(threshold), 4),
        'accuracy': round(float(acc), 4),
        'precision': round(float(prec), 4),
        'recall': round(float(rec), 4),
        'specificity': round(float(spec), 4),
        'f1_score': round(float(f1), 4),
        'apcer': round(float(apcer), 4),
        'bpcer': round(float(bpcer), 4),
        'acer': round(float(acer), 4),
        'confusion_matrix': {'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}
    }

def find_optimal_threshold(y_val: np.ndarray, val_scores: np.ndarray):
    """Find threshold minimizing ACER on the validation set."""
    candidates = np.percentile(val_scores, np.linspace(1, 99, 199))
    candidates = np.unique(np.concatenate([candidates, [0.5, np.median(val_scores), np.mean(val_scores)]]))
    
    best_thresh = 0.5
    best_acer = 1.0
    best_j = -1.0
    
    for th in candidates:
        m = compute_metrics_at_threshold(y_val, val_scores, th)
        j_stat = m['recall'] + m['specificity'] - 1.0
        if m['acer'] < best_acer or (m['acer'] == best_acer and j_stat > best_j):
            best_acer = m['acer']
            best_j = j_stat
            best_thresh = th

    return float(best_thresh)

def recalibrate_all():
    feature_dir = ROOT / 'data/cache/image_features'
    manifest_path = ROOT / 'data/manifests/reviewed_label_manifest.csv'
    
    rev_df = pd.read_csv(manifest_path)
    path_to_info = {}
    for r in rev_df.to_dict('records'):
        p = r['image_path'].replace('\\', '/')
        path_to_info[p] = {
            'label': 1 if r['verified_label'] == 'morphed' else 0,
            'split': r['split']
        }

    print(f"Loaded {len(path_to_info)} approved manifest entries.")
    
    feature_cache = {}
    comparison_summary = []

    for name, spec in MODEL_SPECS.items():
        feat_key = spec['feature_key']
        if feat_key not in feature_cache:
            print(f"\nLoading '{feat_key}' feature splits...")
            feature_cache[feat_key] = load_feature_splits(feature_dir, path_to_info, feat_key)
            X_tr, y_tr, _, X_val, y_val, _, X_te, y_te, _ = feature_cache[feat_key]
            print(f"  Train: {len(X_tr)} | Val: {len(X_val)} | Test: {len(X_te)}")

        X_tr, y_tr, p_tr, X_val, y_val, p_val, X_te, y_te, p_te = feature_cache[feat_key]

        print(f"\nTraining & Calibrating: {name} ({feat_key})")
        model = spec['pipeline']()
        t0 = time.time()
        model.fit(X_tr, y_tr)
        fit_dur = round(time.time() - t0, 3)

        # Get continuous scores for validation & test
        if hasattr(model, 'predict_proba'):
            val_scores = model.predict_proba(X_val)[:, 1]
            test_scores = model.predict_proba(X_te)[:, 1]
            default_thresh = 0.5
        elif hasattr(model, 'decision_function'):
            val_scores = model.decision_function(X_val)
            test_scores = model.decision_function(X_te)
            default_thresh = 0.0
        else:
            val_scores = model.predict(X_val).astype(float)
            test_scores = model.predict(X_te).astype(float)
            default_thresh = 0.5

        # Calibrate optimal threshold on VALIDATION set ONLY
        opt_thresh = find_optimal_threshold(y_val, val_scores)
        val_metrics_opt = compute_metrics_at_threshold(y_val, val_scores, opt_thresh)

        # Evaluate on unseen TEST set with both default and calibrated thresholds
        test_metrics_default = compute_metrics_at_threshold(y_te, test_scores, default_thresh)
        test_metrics_calibrated = compute_metrics_at_threshold(y_te, test_scores, opt_thresh)

        # Compute ROC-AUC and PR-AUC on test set
        roc_auc = None
        pr_auc = None
        if len(np.unique(y_te)) > 1:
            try:
                roc_auc = round(float(roc_auc_score(y_te, test_scores)), 4)
                p_vals, r_vals, _ = precision_recall_curve(y_te, test_scores)
                pr_auc = round(float(auc(r_vals, p_vals)), 4)
            except Exception:
                pass

        test_metrics_default['roc_auc'] = roc_auc
        test_metrics_default['pr_auc'] = pr_auc
        test_metrics_calibrated['roc_auc'] = roc_auc
        test_metrics_calibrated['pr_auc'] = pr_auc

        # Save raw test prediction logs
        pred_records = []
        for p, y_t, s in zip(p_te, y_te, test_scores):
            pred_records.append({
                'image_path': p,
                'true_label': 'morphed' if y_t == 1 else 'genuine',
                'predicted_label_default': 'morphed' if s >= default_thresh else 'genuine',
                'predicted_label_calibrated': 'morphed' if s >= opt_thresh else 'genuine',
                'model_score': round(float(s), 6),
                'default_threshold': round(float(default_thresh), 4),
                'calibrated_threshold': round(float(opt_thresh), 4),
                'model_version': '3.0.0',
                'split': 'test'
            })
        pred_csv = PRED_DIR / f"{name}_predictions.csv"
        pd.DataFrame(pred_records).to_csv(pred_csv, index=False)

        # Save model artifact
        art_path = TRAINED_DIR / f"{name}.joblib"
        joblib.dump(model, art_path)
        art_sha = hashlib.sha256(art_path.read_bytes()).hexdigest()

        # Update metadata JSON
        meta = {
            'model_name': name,
            'architecture': name,
            'framework': spec['framework'],
            'description': spec['description'],
            'feature_key': feat_key,
            'input_dimensions': X_tr.shape[1],
            'training_samples': len(X_tr),
            'training_morphed': int(np.sum(y_tr == 1)),
            'training_genuine': int(np.sum(y_tr == 0)),
            'training_duration_seconds': fit_dur,
            'artifact_path': str(art_path.relative_to(ROOT)).replace('\\', '/'),
            'artifact_sha256': art_sha,
            'training_date': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'training_status': 'trained',
            'validation_status': 'evaluated',
            'approval_status': 'approved_experimental_inference',
            'calibrated_threshold': round(float(opt_thresh), 4),
            'default_threshold': round(float(default_thresh), 4),
            'metrics': test_metrics_calibrated,
            'uncalibrated_metrics': test_metrics_default,
            'validation_metrics': val_metrics_opt
        }
        (META_DIR / f"{name}.json").write_text(json.dumps(meta, indent=2), encoding='utf-8')

        print(f"  Default Acc: {test_metrics_default['accuracy']:.4f} (ACER: {test_metrics_default['acer']:.4f}, APCER: {test_metrics_default['apcer']:.4f}, BPCER: {test_metrics_default['bpcer']:.4f})")
        print(f"  Calibrated Acc: {test_metrics_calibrated['accuracy']:.4f} (ACER: {test_metrics_calibrated['acer']:.4f}, APCER: {test_metrics_calibrated['apcer']:.4f}, BPCER: {test_metrics_calibrated['bpcer']:.4f}) [Thresh: {opt_thresh:.4f}, AUC: {roc_auc}]")

        comparison_summary.append({
            'model': name,
            'feature': feat_key,
            'calibrated_threshold': opt_thresh,
            'default_accuracy': test_metrics_default['accuracy'],
            'calibrated_accuracy': test_metrics_calibrated['accuracy'],
            'calibrated_acer': test_metrics_calibrated['acer'],
            'calibrated_apcer': test_metrics_calibrated['apcer'],
            'calibrated_bpcer': test_metrics_calibrated['bpcer'],
            'roc_auc': roc_auc,
            'pr_auc': pr_auc
        })

    # Save summary table
    summary_df = pd.DataFrame(comparison_summary).sort_values(by='calibrated_accuracy', ascending=False)
    summary_df.to_csv(PRED_DIR / 'model_benchmark_comparison.csv', index=False)
    print("\n=== MODEL BENCHMARK RECALIBRATION COMPLETE ===")
    print(summary_df.to_string(index=False))

    # Also regenerate models/metadata/model_registry.json
    print("\nUpdating models/metadata/model_registry.json...")
    from scripts.build_model_registry import build_registry
    build_registry()

if __name__ == '__main__':
    recalibrate_all()
