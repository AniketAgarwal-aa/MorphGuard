# MorphGuard Model Evaluation & Empirical Benchmark

**Benchmark Dataset:** Held-Out Test Split (285 Samples: 228 Morphed, 57 Genuine)  
**Tuning Rule:** Validation Split Only ($\tau^* = \arg\min \text{ACER}_{\text{val}}$)  
**Evaluation Standard:** ISO/IEC 30107-3  

---

## 1. Complete 21-Model Benchmark Table

Every model was evaluated on the held-out test split using its validation-calibrated threshold $\tau^*$. Raw predictions and ground truth are logged in `reports/predictions/`.

| Architecture | Model Family | Feature Key / Input | Calibrated $\tau^*$ | Test Accuracy | ACER | APCER | BPCER | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **combined_svm** | SVM (RBF) | Combined (6,103D) | 0.0051 | **96.49%** | **0.0680** | 0.0132 | 0.1228 | **0.9878** | **0.9967** |
| **hog_svm** | SVM (RBF) | HOG (6,084D) | 0.0040 | **96.14%** | **0.0899** | 0.0044 | 0.1754 | **0.9867** | **0.9964** |
| **logistic_regression** | Linear | Combined (6,103D) | 0.0016 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | 0.9769 | 0.9912 |
| **hist_gradient_boosting**| Boosting | Combined (6,103D) | 0.0006 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9911** | **0.9971** |
| **extra_trees** | Ensemble | Combined (6,103D) | 0.2526 | **95.44%** | **0.1140** | 0.0000 | 0.2281 | **0.9950** | **0.9987** |
| **rf_combined** | Ensemble | Combined (6,103D) | 0.2670 | **95.09%** | **0.1228** | 0.0000 | 0.2456 | 0.9879 | 0.9965 |
| **linear_svm** | Linear SVM | Combined (6,103D) | 0.0010 | **95.09%** | **0.1162** | 0.0044 | 0.2281 | 0.9675 | 0.9854 |
| **efficientnet_b0** | PyTorch Deep | RGB Crop ($224^2$) | 0.0032 | **91.58%** | **0.0987** | 0.0746 | 0.1228 | **0.9631** | **0.9884** |
| **voting_ensemble** | Voting | GLCM (5D) | 0.1631 | **89.12%** | **0.1535** | 0.0789 | 0.2281 | 0.8688 | 0.9364 |
| **stacking_ensemble**| Stacking | GLCM (5D) | 0.4435 | **88.07%** | **0.1338** | 0.1096 | 0.1579 | 0.9044 | 0.9598 |
| **custom_cnn** | PyTorch Deep | RGB Crop ($224^2$) | 0.5000 | **87.72%** | **0.1096** | 0.1316 | 0.0877 | 0.9601 | — |
| **lbp_svm** | SVM (RBF) | LBP (10D) | 0.0917 | **82.46%** | **0.2083** | 0.1535 | 0.2632 | 0.8503 | 0.9218 |
| **mobilenet_v3_small**| PyTorch Deep | RGB Crop ($224^2$) | 0.9318 | **80.00%** | **0.5000** | 0.0000 | 1.0000 | 0.1632 | 0.7277 |
| **lda** | Linear | GLCM (5D) | 0.5580 | **76.49%** | **0.1996** | 0.2588 | 0.1404 | 0.8690 | 0.9304 |
| **resnet18** | PyTorch Deep | RGB Crop ($224^2$) | 0.000007 | **71.23%** | **0.3180** | 0.2675 | 0.3684 | 0.8121 | 0.9414 |
| **densenet121** | PyTorch Deep | RGB Crop ($224^2$) | 0.005979 | **63.86%** | **0.2917** | 0.4079 | 0.1754 | 0.8089 | 0.9461 |
| **resnet34** | PyTorch Deep | RGB Crop ($224^2$) | 0.311335 | **62.11%** | **0.2434** | 0.4693 | 0.0175 | 0.8841 | 0.9680 |
| **gaussian_nb** | Naive Bayes | GLCM (5D) | 0.3712 | **60.35%** | **0.3004** | 0.4605 | 0.1404 | 0.8560 | 0.9068 |
| **glcm_rf** | Random Forest| GLCM (5D) | 0.4196 | **52.98%** | **0.3202** | 0.5702 | 0.0702 | 0.9058 | 0.9644 |
| **resnet50** | PyTorch Deep | RGB Crop ($224^2$) | 0.000703 | **48.77%** | **0.3596** | 0.6140 | 0.1053 | 0.8045 | 0.9378 |
| **knn** | Neighbors | GLCM (5D) | 0.5921 | **37.54%** | **0.4167** | 0.7632 | 0.0702 | 0.6682 | 0.8942 |

---

## 2. Key Findings & Insights

1. **High-Dimensional Gradient Features Dominate Handcrafted MAD:**
   The `combined_svm` (6,103D) and `hog_svm` (6,084D) achieved the highest overall detection accuracy (96.49% and 96.14% respectively) and lowest error rates (ACER 0.0680 and 0.0899). HOG effectively captures the high-frequency blending boundaries created during morphing triangulation.
2. **Deep Architecture Trade-Offs:**
   Among deep models, `efficientnet_b0` demonstrated the strongest performance (**91.58% accuracy, 0.0987 ACER, 0.9631 ROC-AUC**), outperforming deeper ResNet variants on this CPU-trained regime.
3. **Threshold Calibration is Essential:**
   Default thresholds ($\tau = 0.5$) severely underperformed on uncalibrated models due to prior probability shifts; tuning $\tau^*$ on validation data restored true operational sensitivity.
