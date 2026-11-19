# MorphGuard V3.0 — System Architecture

## 1. System Overview
MorphGuard is an experimental biometric research platform designed to investigate facial morph attack detection (MAD), multi-scale texture extraction, and deep neural architectures under strict leakage prevention protocols.

```mermaid
flowchart TD
    subgraph Data["1. Biometric Data Layer"]
        A1["MONOT (24,140 imgs)<br>Gate_10, Gate_25, Morphed"]
        A2["ONOT (22,652 imgs)<br>Digital, Print-Scan"]
        A3["Feature Cache<br>182 Shards (46,792 samples)"]
    end

    subgraph Governance["2. Scientific Governance Layer"]
        B1["Provenance Audit<br>reviewed_label_manifest.csv (1,197)"]
        B2["Connected-Component Partitioning<br>Train (591) / Val (321) / Test (285)"]
        B3["Zero Identity Overlap Guarantee"]
    end

    subgraph Features["3. Feature Engineering Layer"]
        C1["Face Preprocessor<br>Haar Detection + Alignment 224x224"]
        C2["Multi-Scale Feature Extraction<br>LBP (10D) + HOG (6,084D) + GLCM (5D) + Stats (4D)"]
        C3["Unified 6,103D Combined Vector"]
    end

    subgraph Models["4. Model & Inference Layer"]
        D1["Scikit-Learn Baselines<br>Combined SVM, Logistic, HOG SVM, Extra Trees, RF, LDA"]
        D2["Ensembles<br>Stacking & Voting Ensembles"]
        D3["PyTorch Deep Models<br>Custom CNN (Trained) + 6 Compute-Gated Backbones"]
        D4["InferenceService<br>Polymorphic Routing + Threshold Calibration"]
    end

    subgraph Application["5. Presentation & Delivery"]
        E1["Streamlit Application (14 Pages)<br>http://localhost:8501"]
        E2["Hosted Artifact Retrieval<br>Lazy Hugging Face Hub / Local Cache"]
        E3["Explainability Engine<br>PCA, Histograms, Feature Inspection"]
    end

    Data --> Governance
    Data --> Features
    Governance --> Models
    Features --> Models
    Models --> Application
```

## 2. Directory Hierarchy
- `app/`: Multi-page Streamlit application (14 interactive research pages).
  - `pages/`: 14 pages including Face Morph Analysis, Model Comparison, Dataset Explorer, Model Insights, Research Experiments.
  - `components/`: UI components, theme manager, data loaders.
- `src/morphguard/`: Production-grade core Python library.
  - `preprocessing/`: Haar cascade detection, blur variance (sharpness), contrast, and alignment.
  - `feature_extraction/`: Extractors for LBP, HOG, GLCM, and statistical descriptors.
  - `classification/`: Model factories and PyTorch / Scikit-learn definitions.
  - `inference/`: `InferenceService`, polymorphic adapters (`FeatureModelAdapter`, `PyTorchModelAdapter`), and hosted model resolution.
  - `dataset/`: Manifest schemas, label validation, and connected-component grouping.
- `data/`:
  - `cache/image_features/`: 182 compressed `.npz` shards storing 46,792 feature records.
  - `manifests/`: `annotation_inventory.csv` (46,792 records) and `reviewed_label_manifest.csv` (1,197 records).
- `models/`:
  - `trained/`: Trained `.joblib` model artifacts.
  - `checkpoints/`: Trained PyTorch checkpoints (`custom_cnn.pt`).
  - `metadata/`: Individual architecture JSON specs and `model_registry.json` tracking 21 architectures.
- `reports/`:
  - `dataset_inventory.csv`, `label_distribution.csv`, `unlabelled_samples.csv`, `duplicate_audit.csv`, `split_assignments.csv`.
  - `split_leakage_audit.md`, `dataset_quality_report.md`, `label_provenance_report.md`.
  - `predictions/`: Raw test predictions for all 15 trained models.
- `scripts/`: Modular automation tools for processing, training, calibration, validation, and testing.
