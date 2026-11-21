# MorphGuard V3.2 — Final Production Release & Handover Report

**Document Version:** 3.2.0-Final  
**Author:** Aniket Agarwal  
**Release Tag:** `v3.2`  
**Git Release Commit:** `c17561db41dae9d5f154c4c8093bfcf2b64f6b16`  
**Target Repository:** [https://github.com/AniketAgarwal-aa/MorphGuard](https://github.com/AniketAgarwal-aa/MorphGuard)  
**Model Hub Repository:** [https://huggingface.co/AniketAgarwal-aa/MorphGuard-Models](https://huggingface.co/AniketAgarwal-aa/MorphGuard-Models) (PUBLIC)  
**Live Application URL:** [https://morphguard.streamlit.app/](https://morphguard.streamlit.app/)  

---

## 1. Executive Summary & Verification Matrix

MorphGuard V3.2 is an end-to-end biometric research platform for **Facial Morph Attack Detection (MAD)** adhering to the **ISO/IEC 30107-3** evaluation framework. The platform provides:
- **21 Trained Model Artifacts:** 14 classical baseline/ensemble models and 7 deep neural networks.
- **Strict Validation Calibration:** Decision thresholds ($\tau^*$) mathematically optimized on independent validation splits to minimize Average Classification Error Rate (ACER).
- **Zero Identity Leakage:** Graph connected-component partitioning guaranteeing zero subject overlap between splits.
- **Public Model Hub Distribution:** Free, token-independent public model downloading hosted on Hugging Face Hub under non-commercial research terms (`license: other`).
- **Defensive Interactive Deployment:** 14-page responsive Streamlit application operating live on Streamlit Community Cloud.

### Verification Status Table

| Area | Component | Target Standard / URL | Status |
| :--- | :--- | :--- | :---: |
| **Source Code** | GitHub Master & Tag | `v3.2` (`c17561db41dae9d5f154c4c8093bfcf2b64f6b16`) | **PUBLISHED** |
| **Model Hosting** | Hugging Face Model Hub | `AniketAgarwal-aa/MorphGuard-Models` | **PUBLIC & SYNCED** |
| **Live App** | Streamlit Community Cloud | `https://morphguard.streamlit.app/` | **DEPLOYED & VERIFIED** |
| **Model Count** | 21 Serialized Artifacts | 14 Classical / 7 Deep PyTorch Models | **VERIFIED (21/21)** |
| **Calibration** | Top Performer Threshold | Combined SVM $\tau^* = 0.0051$ (96.49% Acc, 0.0680 ACER) | **CANONICAL** |
| **Test Suite** | PyTest Core Unit Tests | 23/23 Tests Passing (`tests/test_core.py`) | **VERIFIED** |
| **UI Tests** | Streamlit App Compilation | 14/14 Pages Compiling with Zero Errors | **VERIFIED** |
| **Parity** | Local vs Hosted Inference | Uniform mathematical decision rule applied | **VERIFIED** |
| **Biometric Privacy**| GDPR Article 9 Governance | Zero raw facial images or private identities stored | **VERIFIED** |

---

## 2. Authoritative 21-Model Benchmark Benchmark (Held-Out Test Set: 285 Samples)

All metrics reflect evaluation on **285 unseen test samples** (228 morphed attacks, 57 genuine bona fide).
Decision thresholds ($\tau^*$) were frozen on an independent validation set (321 samples).

| # | Architecture | Family | Artifact Path | Optimal $\tau^*$ | Test Accuracy | ACER | APCER | BPCER | ROC-AUC |
| :-: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Combined SVM (RBF)** | SVM (RBF) | `classical/combined_svm.joblib` | **0.0051** | **96.49%** | **0.0680** | 0.0132 | 0.1228 | **0.9878** |
| 2 | **HOG SVM (RBF)** | SVM (RBF) | `classical/hog_svm.joblib` | 0.0040 | **96.14%** | **0.0899** | 0.0044 | 0.1754 | **0.9867** |
| 3 | **Logistic Regression** | Linear | `classical/logistic_regression.joblib`| 0.0016 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | 0.9769 |
| 4 | **Hist Gradient Boosting**| Boosting | `classical/hist_gradient_boosting.joblib`| 0.0006 | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9911** |
| 5 | **Extra Trees** | Ensemble | `classical/extra_trees.joblib` | 0.2526 | **95.44%** | **0.1140** | 0.0000 | 0.2281 | **0.9950** |
| 6 | **Random Forest** | Ensemble | `classical/rf_combined.joblib` | 0.2670 | **95.09%** | **0.1228** | 0.0000 | 0.2456 | 0.9879 |
| 7 | **Linear SVM** | Linear SVM | `classical/linear_svm.joblib` | 0.0010 | **95.09%** | **0.1162** | 0.0044 | 0.2281 | 0.9675 |
| 8 | **EfficientNet-B0** | Deep CNN | `deep_learning/efficientnet_b0.pt` | 0.0032 | **91.58%** | **0.0987** | 0.0746 | 0.1228 | **0.9631** |
| 9 | **Voting Ensemble** | Voting | `ensembles/voting_ensemble.joblib` | 0.1631 | **89.12%** | **0.1535** | 0.0789 | 0.2281 | 0.8688 |
| 10 | **Stacking Ensemble** | Stacking | `ensembles/stacking_ensemble.joblib` | 0.4435 | **88.07%** | **0.1338** | 0.1096 | 0.1579 | 0.9044 |
| 11 | **Custom CNN** | Deep CNN | `deep_learning/custom_cnn.pt` | 0.5000 | **87.72%** | **0.1096** | 0.1316 | 0.0877 | 0.9601 |
| 12 | **LBP SVM (RBF)** | SVM (RBF) | `classical/lbp_svm.joblib` | 0.0917 | **82.46%** | **0.2083** | 0.1535 | 0.2632 | 0.8503 |
| 13 | **MobileNetV3-Small** | Deep CNN | `deep_learning/mobilenet_v3_small.pt`| 0.9318 | **80.00%** | **0.5000** | 0.0000 | 1.0000 | 0.1632 |
| 14 | **LDA** | Linear | `classical/lda.joblib` | 0.5580 | **76.49%** | **0.1996** | 0.2588 | 0.1404 | 0.8690 |
| 15 | **ResNet-18** | Deep CNN | `deep_learning/resnet18.pt` | 0.000007 | **71.23%** | **0.3180** | 0.2675 | 0.3684 | 0.8121 |
| 16 | **DenseNet-121** | Deep CNN | `deep_learning/densenet121.pt` | 0.0060 | **63.86%** | **0.2917** | 0.4079 | 0.1754 | 0.8089 |
| 17 | **ResNet-34** | Deep CNN | `deep_learning/resnet34.pt` | 0.3113 | **62.11%** | **0.2434** | 0.4693 | 0.0175 | 0.8841 |
| 18 | **Gaussian Naive Bayes**| Bayesian | `classical/gaussian_nb.joblib` | 0.3712 | **60.35%** | **0.3004** | 0.4605 | 0.1404 | 0.8560 |
| 19 | **GLCM Random Forest** | Random Forest| `classical/glcm_rf.joblib` | 0.4196 | **52.98%** | **0.3202** | 0.5702 | 0.0702 | 0.9058 |
| 20 | **ResNet-50** | Deep CNN | `deep_learning/resnet50.pt` | 0.000703 | **48.77%** | **0.3596** | 0.6140 | 0.1053 | 0.8045 |
| 21 | **KNN** | Neighbors | `classical/knn.joblib` | 0.5921 | **37.54%** | **0.4167** | 0.7632 | 0.0702 | 0.6682 |

---

## 3. Reproduction & Execution Instructions

```powershell
# Clone the verified repository
git clone https://github.com/AniketAgarwal-aa/MorphGuard.git
cd MorphGuard

# Create and activate environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run the full test suite
pytest tests/test_core.py -v

# Launch the Streamlit dashboard locally
streamlit run app/main.py
```
