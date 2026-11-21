# MorphGuard V3.2 — Canonical 21-Model Scientific Benchmark & Calibration Manifest

**Authoritative Benchmark Standard:** ISO/IEC 30107-3 Biometric Presentation Attack Detection  
**Evaluation Dataset:** Held-out Test Split of **285 samples** (228 morphed attacks, 57 genuine bona fide) with zero subject/identity leakage.  
**Threshold Calibration:** Strictly optimized on an independent **Validation Split (321 samples)** by minimizing ACER. **Zero calibration on the test set.**  
**Class Convention:** Class 1 = `morphed` (Attack / Positive), Class 0 = `genuine` (Bona Fide / Negative).  

---

## 1. Authoritative 21-Model Scientific Manifest Table

| # | Model Identifier | Framework | Artifact SHA-256 Checksum | Calibrated $\tau^*$ | Test Acc | APCER | BPCER | ACER | ROC-AUC | Primary Evidence File |
| :-: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | **combined_svm** | scikit-learn | `edcdbb4bfe...` | **0.0051** | **96.49%** | 0.0132 | 0.1228 | **0.0680** | **0.9878** | [combined_svm_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/combined_svm_predictions.csv) |
| 2 | **hog_svm** | scikit-learn | `5b1608dc82...` | **0.0040** | **96.14%** | 0.0044 | 0.1754 | **0.0899** | **0.9867** | [hog_svm_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/hog_svm_predictions.csv) |
| 3 | **hist_gradient_boosting** | scikit-learn | `9d7558d62d...` | **0.0006** | **96.14%** | 0.0000 | 0.1930 | **0.0965** | **0.9911** | [hist_gradient_boosting_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/hist_gradient_boosting_predictions.csv) |
| 4 | **logistic_regression** | scikit-learn | `e3dc99ae4b...` | **0.0016** | **96.14%** | 0.0000 | 0.1930 | **0.0965** | **0.9769** | [logistic_regression_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/logistic_regression_predictions.csv) |
| 5 | **efficientnet_b0** | PyTorch | `ef6d7e5a4d...` | **0.0032** | **91.58%** | 0.0746 | 0.1228 | **0.0987** | **0.9631** | [efficientnet_b0_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/efficientnet_b0_predictions.csv) |
| 6 | **custom_cnn** | PyTorch | `f141d2b38e...` | **0.5000** | **87.72%** | 0.1316 | 0.0877 | **0.1096** | **0.9601** | [custom_cnn_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/custom_cnn_predictions.csv) |
| 7 | **extra_trees** | scikit-learn | `6ea40abb5b...` | **0.2526** | **95.44%** | 0.0000 | 0.2281 | **0.1140** | **0.9950** | [extra_trees_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/extra_trees_predictions.csv) |
| 8 | **linear_svm** | scikit-learn | `7d4718f3f2...` | **0.0010** | **95.09%** | 0.0044 | 0.2281 | **0.1162** | **0.9675** | [linear_svm_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/linear_svm_predictions.csv) |
| 9 | **rf_combined** | scikit-learn | `17408ba874...` | **0.2670** | **95.09%** | 0.0000 | 0.2456 | **0.1228** | **0.9879** | [rf_combined_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/rf_combined_predictions.csv) |
| 10 | **stacking_ensemble** | scikit-learn | `fc926697ed...` | **0.4435** | **88.07%** | 0.1096 | 0.1579 | **0.1338** | **0.9044** | [stacking_ensemble_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/stacking_ensemble_predictions.csv) |
| 11 | **voting_ensemble** | scikit-learn | `5ff29f3395...` | **0.1631** | **89.12%** | 0.0789 | 0.2281 | **0.1535** | **0.8688** | [voting_ensemble_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/voting_ensemble_predictions.csv) |
| 12 | **lda** | scikit-learn | `dd44eb2d04...` | **0.5580** | **76.49%** | 0.2588 | 0.1404 | **0.1996** | **0.8690** | [lda_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/lda_predictions.csv) |
| 13 | **lbp_svm** | scikit-learn | `c03852ef48...` | **0.0917** | **82.46%** | 0.1535 | 0.2632 | **0.2083** | **0.8503** | [lbp_svm_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/lbp_svm_predictions.csv) |
| 14 | **resnet34** | PyTorch | `fdbc80dc8e...` | **0.3113** | **62.11%** | 0.4693 | 0.0175 | **0.2434** | **0.8841** | [resnet34_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/resnet34_predictions.csv) |
| 15 | **densenet121** | PyTorch | `9169572094...` | **0.0060** | **63.86%** | 0.4079 | 0.1754 | **0.2917** | **0.8089** | [densenet121_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/densenet121_predictions.csv) |
| 16 | **gaussian_nb** | scikit-learn | `b26ce942d6...` | **0.3712** | **60.35%** | 0.4605 | 0.1404 | **0.3004** | **0.8560** | [gaussian_nb_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/gaussian_nb_predictions.csv) |
| 17 | **resnet18** | PyTorch | `4887d7e6db...` | **0.00000664** | **71.23%** | 0.2675 | 0.3684 | **0.3180** | **0.8121** | [resnet18_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/resnet18_predictions.csv) |
| 18 | **glcm_rf** | scikit-learn | `9e877b1f8a...` | **0.4196** | **52.98%** | 0.5702 | 0.0702 | **0.3202** | **0.9058** | [glcm_rf_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/glcm_rf_predictions.csv) |
| 19 | **resnet50** | PyTorch | `f8927bc503...` | **0.0007** | **48.77%** | 0.6140 | 0.1053 | **0.3596** | **0.8045** | [resnet50_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/resnet50_predictions.csv) |
| 20 | **knn** | scikit-learn | `27b743888d...` | **0.5921** | **37.54%** | 0.7632 | 0.0702 | **0.4167** | **0.6682** | [knn_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/knn_predictions.csv) |
| 21 | **mobilenet_v3_small** | PyTorch | `30ef3bf867...` | **0.9318** | **80.00%** | 0.0000 | 1.0000 | **0.5000** | **0.1632** | [mobilenet_v3_small_predictions.csv](file:///C:/Users/admin/Downloads/Code/MorphGuard/reports/predictions/mobilenet_v3_small_predictions.csv) |

---

## 2. Threshold Discrepancy Resolution & Root-Cause Explanation

### 2.1 The Two Competing Threshold Sets Identified
1. **Set A — Authoritative Validation-Calibrated Thresholds (Preserved in Manifest & Code):**
   - Generated by `scripts/recalibrate_and_evaluate_all.py` on the 321-sample validation split.
   - Serialized in `models/metadata/<model_name>.json`, `models/metadata/model_registry.json`, and `reports/predictions/<model_name>_predictions.csv`.
   - These exact values produce the verified test metrics (e.g. `combined_svm` $\tau^* = 0.0051$ -> 96.49% accuracy; `efficientnet_b0` $\tau^* = 0.0032$ -> 91.58% accuracy).

2. **Set B — Arbitrary Rounded Estimates (Erroneously Written in Some Markdown Drafts):**
   - In earlier markdown reports (e.g., `reports/PHASE_5_1_MEMORY_MEASUREMENT_RECONCILIATION.md`), an earlier assistant had manually drafted summary tables using rounded placeholders (`0.3800`, `0.3500`, `0.2500`, `0.0050` across classical models).
   - **Resolution:** These rounded estimates were never produced by calibration scripts, do not appear in serialized JSON metadata, and were not used to compute test metrics. They have been fully purged and replaced with the authoritative Validation-Calibrated Thresholds in Set A.

---

## 3. Cryptographic Checksum & Identity Verification
All 21 model files across `models/trained/`, `models/checkpoints/`, and `models/hf_export/` have been verified byte-for-byte against the serialized SHA-256 hashes.
No models were retrained. Zero checkpoint substitution occurred.

```json
{
  "combined_svm": {
    "sha256": "edcdbb4bfe60077521b98bae792372f121d41f7abcbba40ac1d2b84089ea7a84",
    "threshold": 0.0051,
    "accuracy": 0.9649,
    "acer": 0.068
  },
  "custom_cnn": {
    "sha256": "f141d2b38e94965fc2327781f9782365ce4613a5968cedf946fc6197f055d565",
    "threshold": 0.5,
    "accuracy": 0.8772,
    "acer": 0.1096
  },
  "densenet121": {
    "sha256": "9169572094dcad770c6ea36e2857f5b5da4e73a3d53cee738f60c99885c4fd83",
    "threshold": 0.0059793405234813,
    "accuracy": 0.6386,
    "acer": 0.2917
  },
  "efficientnet_b0": {
    "sha256": "ef6d7e5a4dfbbd61a0eb79a1fc50a4d94964fe9fe2118d7f41fdac35de9a799e",
    "threshold": 0.0031937048770487,
    "accuracy": 0.9158,
    "acer": 0.0987
  },
  "extra_trees": {
    "sha256": "6ea40abb5be70817a22fbe968506aba09ba9e5511b499e53885736bd062cf485",
    "threshold": 0.2526,
    "accuracy": 0.9544,
    "acer": 0.114
  },
  "gaussian_nb": {
    "sha256": "b26ce942d6c1136442eaa5edc0789f82a971798ebac0c85065e09f79a2de180a",
    "threshold": 0.3712,
    "accuracy": 0.6035,
    "acer": 0.3004
  },
  "glcm_rf": {
    "sha256": "9e877b1f8aacefea7b95ece896c660cf0a9f366f862508ba38b32fb54fbb7659",
    "threshold": 0.4196,
    "accuracy": 0.5298,
    "acer": 0.3202
  },
  "hist_gradient_boosting": {
    "sha256": "9d7558d62dadc1ebd24251f5cee1e253a7f62650389b8d7223ac427aece631fd",
    "threshold": 0.0006,
    "accuracy": 0.9614,
    "acer": 0.0965
  },
  "hog_svm": {
    "sha256": "5b1608dc820cd93ca78c3eda06a8a9294721df34e7b6e2ba346ca5c00a14ad4e",
    "threshold": 0.004,
    "accuracy": 0.9614,
    "acer": 0.0899
  },
  "knn": {
    "sha256": "27b743888d758dd8b38b49fd35ec469f71ff223f0b8036e3567e8826a2d43bf3",
    "threshold": 0.5921,
    "accuracy": 0.3754,
    "acer": 0.4167
  },
  "lbp_svm": {
    "sha256": "c03852ef48922c77da42d44041cbef17b2249e85f5d67d6ae134806aed898926",
    "threshold": 0.0917,
    "accuracy": 0.8246,
    "acer": 0.2083
  },
  "lda": {
    "sha256": "dd44eb2d0466a0e167538d82994faaa7e264a0548f28b9d4a417cc6d2fd0cbd0",
    "threshold": 0.558,
    "accuracy": 0.7649,
    "acer": 0.1996
  },
  "linear_svm": {
    "sha256": "7d4718f3f2b7af27fef4549b5b725895d8a9a0386482c930517917c3d435ce7d",
    "threshold": 0.001,
    "accuracy": 0.9509,
    "acer": 0.1162
  },
  "logistic_regression": {
    "sha256": "e3dc99ae4b75e20b68dc91bb59e63437c8330b0d11fec98eb1da9426c8865a03",
    "threshold": 0.0016,
    "accuracy": 0.9614,
    "acer": 0.0965
  },
  "mobilenet_v3_small": {
    "sha256": "30ef3bf8670c0eb245dabfa55dd08aa07a90977349d951c7a5785ad8c97a2a22",
    "threshold": 0.931846797466278,
    "accuracy": 0.8,
    "acer": 0.5
  },
  "resnet18": {
    "sha256": "4887d7e6dbd0826bf16505c685d08f1f88442c5874d65d06863199df45ebb8db",
    "threshold": 6.644662335020257e-06,
    "accuracy": 0.7123,
    "acer": 0.318
  },
  "resnet34": {
    "sha256": "fdbc80dc8ee75ac021ed805f5847a02697aee1fd6f1081edc04dcb151bd271e7",
    "threshold": 0.3113348484039306,
    "accuracy": 0.6211,
    "acer": 0.2434
  },
  "resnet50": {
    "sha256": "f8927bc503efbc0ac5cc2a9eda2348263873d32eeb16da06a613ff17a29caaa1",
    "threshold": 0.0007034130976535,
    "accuracy": 0.4877,
    "acer": 0.3596
  },
  "rf_combined": {
    "sha256": "17408ba874821457c7a849dae1e4b4a8dac98f81be0010721a26b6d644ff3695",
    "threshold": 0.267,
    "accuracy": 0.9509,
    "acer": 0.1228
  },
  "stacking_ensemble": {
    "sha256": "fc926697ed5cde9af89b529ec00c5d47360c0407ed747dbcdaafc9c49c109b1a",
    "threshold": 0.4435,
    "accuracy": 0.8807,
    "acer": 0.1338
  },
  "voting_ensemble": {
    "sha256": "5ff29f33953d729eef2c61743fa004904561a5df42b879e2ccb514398dae0234",
    "threshold": 0.1631,
    "accuracy": 0.8912,
    "acer": 0.1535
  }
}
```