"""Train and evaluate expanded classical machine learning models and ensembles.

Adheres strictly to ISO/IEC 30107-3 presentation attack detection standards:
- Train partition only for model fitting and hyperparameter tuning.
- Test partition strictly held-out until final evaluation.
- Metrics: Accuracy, Precision, Recall, Specificity, F1, APCER, BPCER, ACER, ROC-AUC, PR-AUC.
- Ensembles: Voting (Soft), Stacking (Meta-learner).
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time
from pathlib import Path
import numpy as np
import joblib

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier, ExtraTreesClassifier,
    HistGradientBoostingClassifier,
    VotingClassifier, StackingClassifier
)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))

from morphguard.dataset.labels import approved_rows

MODEL_SPECS = {
    # 1. Classical Baselines & Advanced ML
    'glcm_rf': {
        'feature_key': 'glcm',
        'pipeline': lambda: RandomForestClassifier(n_estimators=150, max_depth=10, class_weight='balanced', random_state=42, n_jobs=2),
        'framework': 'scikit-learn',
        'description': 'Random Forest on 5-dimensional GLCM spatial co-occurrence descriptors'
    },
    'rf_combined': {
        'feature_key': 'X',
        'pipeline': lambda: RandomForestClassifier(n_estimators=150, max_depth=12, class_weight='balanced', random_state=42, n_jobs=2),
        'framework': 'scikit-learn',
        'description': 'Random Forest on complete 6,103-dimensional combined feature vectors'
    },
    'extra_trees': {
        'feature_key': 'X',
        'pipeline': lambda: ExtraTreesClassifier(n_estimators=150, max_depth=12, class_weight='balanced', random_state=42, n_jobs=2),
        'framework': 'scikit-learn',
        'description': 'Extremely Randomized Trees on 6,103-dimensional feature space'
    },
    'logistic_regression': {
        'feature_key': 'X',
        'pipeline': lambda: make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=500, class_weight='balanced', random_state=42)),
        'framework': 'scikit-learn',
        'description': 'L2-regularized Logistic Regression with standardized feature inputs'
    },
    'combined_svm': {
        'feature_key': 'X',
        'pipeline': lambda: make_pipeline(StandardScaler(), SVC(C=1.0, kernel='rbf', class_weight='balanced', probability=True, random_state=42)),
        'framework': 'scikit-learn',
        'description': 'Support Vector Classifier with Radial Basis Function kernel'
    },
    'linear_svm': {
        'feature_key': 'X',
        'pipeline': lambda: make_pipeline(StandardScaler(), SVC(C=0.5, kernel='linear', class_weight='balanced', probability=True, random_state=42)),
        'framework': 'scikit-learn',
        'description': 'Linear Support Vector Classifier on scaled combined features'
    },
    'lbp_svm': {
        'feature_key': 'lbp',
        'pipeline': lambda: make_pipeline(StandardScaler(), SVC(C=1.0, kernel='rbf', class_weight='balanced', probability=True, random_state=42)),
        'framework': 'scikit-learn',
        'description': 'RBF Support Vector Machine on 10-dimensional uniform LBP histogram'
    },
    'hog_svm': {
        'feature_key': 'hog',
        'pipeline': lambda: make_pipeline(StandardScaler(), SVC(C=1.0, kernel='rbf', class_weight='balanced', probability=True, random_state=42)),
        'framework': 'scikit-learn',
        'description': 'Support Vector Classifier on 6,084-dimensional HOG structural gradients'
    },
    'hist_gradient_boosting': {
        'feature_key': 'X',
        'pipeline': lambda: HistGradientBoostingClassifier(max_iter=100, max_depth=6, class_weight='balanced', random_state=42),
        'framework': 'scikit-learn',
        'description': 'Histogram-based Gradient Boosting on 6,103-dimensional feature space'
    },
    'knn': {
        'feature_key': 'glcm',
        'pipeline': lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5, weights='distance')),
        'framework': 'scikit-learn',
        'description': 'k-Nearest Neighbors (k=5, distance-weighted) on GLCM texture metrics'
    },
    'lda': {
        'feature_key': 'glcm',
        'pipeline': lambda: LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto'),
        'framework': 'scikit-learn',
        'description': 'Linear Discriminant Analysis with automatic shrinkage covariance estimation'
    },
    'gaussian_nb': {
        'feature_key': 'glcm',
        'pipeline': lambda: GaussianNB(),
        'framework': 'scikit-learn',
        'description': 'Gaussian Naive Bayes classifier on spatial texture descriptors'
    },
    # 2. Ensemble Architecture
    'voting_ensemble': {
        'feature_key': 'glcm',
        'pipeline': lambda: VotingClassifier(
            estimators=[
                ('rf', RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)),
                ('lda', LinearDiscriminantAnalysis()),
                ('nb', GaussianNB())
            ],
            voting='soft'
        ),
        'framework': 'scikit-learn',
        'description': 'Soft-Voting Ensemble combining Random Forest, LDA, and Gaussian Naive Bayes'
    },
    'stacking_ensemble': {
        'feature_key': 'glcm',
        'pipeline': lambda: StackingClassifier(
            estimators=[
                ('rf', RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)),
                ('lda', LinearDiscriminantAnalysis()),
                ('knn', KNeighborsClassifier(n_neighbors=5))
            ],
            final_estimator=LogisticRegression(C=1.0, random_state=42),
            cv=3
        ),
        'framework': 'scikit-learn',
        'description': 'Stacking Ensemble with 3-fold cross-validated meta-learner'
    }
}

def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray | None, split_name: str) -> dict:
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

    apcer = fn / (tp + fn) if (tp + fn) else 0.0
    bpcer = fp / (tn + fp) if (tn + fp) else 0.0
    acer = (apcer + bpcer) / 2.0

    roc_auc = None
    pr_auc = None
    if y_prob is not None and len(np.unique(y_true)) > 1:
        try:
            roc_auc = round(float(roc_auc_score(y_true, y_prob)), 4)
            precision_vals, recall_vals, _ = precision_recall_curve(y_true, y_prob)
            pr_auc = round(float(auc(recall_vals, precision_vals)), 4)
        except Exception:
            pass

    return {
        'evaluation_split': split_name,
        'eval_samples': total,
        'eval_morphed': int(np.sum(y_true == 1)),
        'eval_genuine': int(np.sum(y_true == 0)),
        'accuracy': round(acc, 4),
        'precision': round(prec, 4),
        'recall': round(rec, 4),
        'specificity': round(spec, 4),
        'f1_score': round(f1, 4),
        'apcer': round(apcer, 4),
        'bpcer': round(bpcer, 4),
        'acer': round(acer, 4),
        'roc_auc': roc_auc,
        'pr_auc': pr_auc,
        'confusion_matrix': {'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}
    }

def load_feature_split(feature_dir: Path, path_to_info: dict, feat_key: str):
    """Memory-efficient feature loader: loads one key at a time with float32."""
    shards = sorted(feature_dir.glob('features_*.npz'))
    X_train, y_train = [], []
    X_test, y_test = [], []

    for s in shards:
        with np.load(s) as z:
            paths = [str(p).replace('\\', '/') for p in z['paths']]
            # Match paths in this shard
            match_indices_train = []
            match_indices_test = []
            for idx, p in enumerate(paths):
                if p in path_to_info:
                    split = path_to_info[p]['split']
                    lbl = path_to_info[p]['label']
                    if split == 'train':
                        match_indices_train.append((idx, lbl))
                    elif split == 'test':
                        match_indices_test.append((idx, lbl))

            if match_indices_train or match_indices_test:
                data = z[feat_key]
                for idx, lbl in match_indices_train:
                    X_train.append(data[idx].astype(np.float32))
                    y_train.append(lbl)
                for idx, lbl in match_indices_test:
                    X_test.append(data[idx].astype(np.float32))
                    y_test.append(lbl)

    return (
        np.asarray(X_train, dtype=np.float32),
        np.asarray(y_train, dtype=np.int64),
        np.asarray(X_test, dtype=np.float32),
        np.asarray(y_test, dtype=np.int64)
    )

def train_and_evaluate_all():
    feature_dir = ROOT / 'data/cache/image_features'
    manifest_path = ROOT / 'data/manifests/reviewed_label_manifest.csv'
    output_dir = ROOT / 'models/trained'
    meta_dir = ROOT / 'models/metadata'
    output_dir.mkdir(parents=True, exist_ok=True)
    meta_dir.mkdir(parents=True, exist_ok=True)

    reviewed = approved_rows(manifest_path, ROOT)
    path_to_info = {}
    for r in reviewed:
        norm_p = r['image_path'].replace('\\', '/')
        path_to_info[norm_p] = {
            'label': 1 if r['verified_label'] == 'morphed' else 0,
            'split': r['split']
        }

    print(f"Total Approved Rows to Match in Cache: {len(path_to_info)}")

    # Cache pre-loaded matrices per feature key
    feature_cache_data = {}
    trained_models_summary = []

    for name, spec in MODEL_SPECS.items():
        feat_key = spec['feature_key']
        if feat_key not in feature_cache_data:
            print(f"Loading '{feat_key}' features from shards into memory...")
            X_tr, y_tr, X_te, y_te = load_feature_split(feature_dir, path_to_info, feat_key)
            feature_cache_data[feat_key] = (X_tr, y_tr, X_te, y_te)
            print(f"  Loaded '{feat_key}': Train={len(X_tr)} samples (shape {X_tr.shape}), Test={len(X_te)} samples")

        X_train, y_train, X_test, y_test = feature_cache_data[feat_key]

        model = spec['pipeline']()
        t0 = time.time()
        model.fit(X_train, y_train)
        fit_duration = round(time.time() - t0, 3)

        preds = model.predict(X_test)
        probs = None
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(X_test)[:, 1]
        elif hasattr(model, 'decision_function'):
            probs = model.decision_function(X_test)

        metrics = compute_metrics(y_test, preds, probs, split_name='test')

        # Persist model artifact
        artifact_path = output_dir / f"{name}.joblib"
        joblib.dump(model, artifact_path)

        # Compute SHA-256
        h = hashlib.sha256()
        with artifact_path.open('rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk)
        art_hash = h.hexdigest()

        # Metadata
        meta = {
            'model_name': name,
            'architecture': name,
            'framework': spec['framework'],
            'description': spec['description'],
            'feature_key': feat_key,
            'input_dimensions': X_train.shape[1],
            'training_samples': len(X_train),
            'training_morphed': int(np.sum(y_train == 1)),
            'training_genuine': int(np.sum(y_train == 0)),
            'training_duration_seconds': fit_duration,
            'artifact_path': str(artifact_path.relative_to(ROOT)).replace('\\', '/'),
            'artifact_sha256': art_hash,
            'training_date': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'training_status': 'trained',
            'validation_status': 'evaluated',
            'approval_status': 'approved_experimental_inference',
            'metrics': metrics
        }

        meta_path = meta_dir / f"{name}.json"
        meta_path.write_text(json.dumps(meta, indent=2), encoding='utf-8')

        auc_str = f"AUC: {metrics['roc_auc']:.4f}" if metrics['roc_auc'] is not None else "AUC: N/A"
        print(f"✓ {name:<24} | Acc: {metrics['accuracy']:.4f} | ACER: {metrics['acer']:.4f} | APCER: {metrics['apcer']:.4f} | BPCER: {metrics['bpcer']:.4f} | F1: {metrics['f1_score']:.4f} | {auc_str} ({fit_duration:.2f}s)")
        trained_models_summary.append(meta)

    return trained_models_summary

if __name__ == '__main__':
    train_and_evaluate_all()
