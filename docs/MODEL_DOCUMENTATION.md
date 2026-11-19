# MorphGuard V3.0 — Model Documentation & Registry

## 1. Registry Architecture
MorphGuard tracks 21 total model architectures across classical Scikit-Learn, ensemble, and PyTorch deep neural networks.

### 1.1 Trained Artifacts (15 Models)
All 15 trained models are serialized in `models/trained/` (`.joblib`) and `models/checkpoints/` (`.pt`), with full metadata in `models/metadata/`.

| Model Name | Framework | Input Feature | Calibrated $\tau^*$ | Test Acc | ACER | APCER | BPCER | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **combined_svm** | Scikit-Learn | Combined (6,103D) | 0.0051 | **96.49%** | **0.0680** | 0.0132 | 0.1228 | **0.9878** | **0.9967** |
| **logistic_regression** | Scikit-Learn | Combined (6,103D) | 0.0016 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9769** | **0.9912** |
| **hog_svm** | Scikit-Learn | HOG (6,084D) | 0.0040 | **96.14%** | **0.0899** | 0.0044 | 0.1754 | **0.9867** | **0.9964** |
| **hist_gradient_boosting** | Scikit-Learn | Combined (6,103D) | 0.0006 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9911** | **0.9971** |
| **extra_trees** | Scikit-Learn | Combined (6,103D) | 0.2526 | **95.44%** | **0.1140** | 0.0000 | 0.2281 | **0.9950** | **0.9987** |
| **rf_combined** | Scikit-Learn | Combined (6,103D) | 0.2670 | **95.09%** | **0.1228** | 0.0000 | 0.2456 | **0.9879** | **0.9965** |
| **linear_svm** | Scikit-Learn | Combined (6,103D) | 0.0010 | **95.09%** | **0.1162** | 0.0044 | 0.2281 | **0.9675** | **0.9854** |
| **voting_ensemble** | Scikit-Learn | GLCM (5D) | 0.1631 | **89.12%** | **0.1535** | 0.0789 | 0.2281 | 0.8688 | 0.9364 |
| **stacking_ensemble** | Scikit-Learn | GLCM (5D) | 0.4435 | **88.07%** | **0.1338** | 0.1096 | 0.1579 | **0.9044** | **0.9598** |
| **custom_cnn** | PyTorch | Raw Face Crop | 0.5000 | **87.72%** | **0.1096** | 0.1316 | 0.0877 | **0.9601** | — |
| **lbp_svm** | Scikit-Learn | LBP (10D) | 0.0917 | **82.46%** | **0.2083** | 0.1535 | 0.2632 | 0.8503 | 0.9218 |
| **lda** | Scikit-Learn | GLCM (5D) | 0.5580 | **76.49%** | **0.1996** | 0.2588 | 0.1404 | 0.8690 | 0.9304 |
| **gaussian_nb** | Scikit-Learn | GLCM (5D) | 0.3712 | 60.35% | 0.3004 | 0.4605 | 0.1404 | 0.8560 | 0.9068 |
| **glcm_rf** | Scikit-Learn | GLCM (5D) | 0.4196 | 52.98% | 0.3202 | 0.5702 | 0.0702 | 0.9058 | 0.9644 |
| **knn** | Scikit-Learn | GLCM (5D) | 0.5921 | 37.54% | 0.4167 | 0.7632 | 0.0702 | 0.6682 | 0.8942 |

### 1.2 Compute-Gated Deep Backbones (6 Models)
Marked in registry as `ready_for_training`. Requires external GPU cluster:
1. `resnet18`: PyTorch 18-layer Residual Network.
2. `resnet34`: PyTorch 34-layer Residual Network.
3. `resnet50`: PyTorch 50-layer Residual Network with bottleneck blocks.
4. `efficientnet_b0`: Compound scaling depth/width convolutional architecture.
5. `mobilenet_v3_small`: Mobile inverted bottleneck depthwise-separable network.
6. `densenet121`: Densely Connected Convolutional Network.

---

## 2. Threshold Calibration Investigation
### 2.1 The V2 Anomaly
In V2.0, Linear SVM, Logistic Regression, HOG SVM, and Combined SVM exhibited accuracy of ~21–25% despite ROC-AUC > 0.96.
- **Root Cause:** Standard Scikit-Learn `predict()` applies a hardcoded decision threshold of 0.50. Under test imbalance (228 morphed vs 57 genuine) and Platt scaling probability compression, almost all morphed sample scores clustered in $[0.01, 0.40]$, causing `predict()` to classify nearly all morphed samples as genuine.
- **Resolution:** Calibrating decision thresholds on the independent **validation set** by minimizing ACER ($\tau^* = \arg\min (\text{APCER} + \text{BPCER})/2$) raised `combined_svm` accuracy from **21.05%** to **96.49%** (ACER: 0.0680) and `hog_svm` to **96.14%** (ACER: 0.0899).
