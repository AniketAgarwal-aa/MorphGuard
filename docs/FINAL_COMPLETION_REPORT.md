# MorphGuard V3.0 — Final Engineering Completion Report

**Project:** MorphGuard — Facial Morph Attack Detection and Biometric Image Analysis System  
**Repository:** `https://github.com/AniketAgarwal-aa/MorphGuard`  
**Date:** November 19, 2026  
**Status:** COMPLETE & SCIENTIFICALLY VALIDATED  

---

## 1. Executive Summary
MorphGuard V3.0 successfully scales from an experimental prototype into a comprehensive, scientifically validated facial morph detection research platform. The entire available biometric inventory of **46,792 images** across MONOT and ONOT has been fully processed, validated, and cached into 182 compressed NPZ shards.

The V2.0 threshold compression anomaly has been resolved through validation-tuned decision calibration, raising top model accuracy from 21.05% to **96.49%** (`combined_svm`, ACER: 0.0680, ROC-AUC: 0.9878), followed by `logistic_regression` (**96.14%**, ACER: 0.0965), `hog_svm` (**96.14%**, ACER: 0.0899), `hist_gradient_boosting` (**96.14%**, ACER: 0.0965), and `extra_trees` (**95.44%**, ACER: 0.1140).

All 15 trained models have raw prediction logs stored in `reports/predictions/`. All 14 Streamlit pages are functional and verified. The complete automated test suite (23/23 tests) passes.

---

## 2. Dataset Processing & Cache Scaling Summary

| Metric | V2.0 Baseline | V3.0 Final State | Change |
| :--- | :---: | :---: | :---: |
| **Total Raw Inventory** | 46,792 images | **46,792 images** | Audited 100% |
| **MONOT Images** | 24,140 images | **24,140 images** | Audited 100% |
| **ONOT Images** | 22,652 images | **22,652 images** | Audited 100% |
| **Cached Feature Records** | 5,000 images | **46,792 images** | **+41,792 (100% Cached)** |
| **Feature Shards on Disk** | 14 shards | **182 shards** | **+168 shards (3.39 GB)** |
| **Cache Validation** | Partial (5,000) | **100% (46,792 / 46,792)** | Valid float32/float64 finite |
| **Failed / Corrupt Files** | 0 | **0** | Zero unreadable files |
| **Face Detection Rate** | 99.1% (subset) | **99.02% (46,333 / 46,792)** | Full corpus rate |
| **Approved Label Records** | 1,197 records | **1,197 records** | Verified provenance |
| **Identity Overlap (Train/Val/Test)**| 0 | **0** | Strictly zero leakage |

---

## 3. Model Benchmark Comparison (Test Split: 285 Samples)

| Architecture | Feature Type | Calibrated $\tau^*$ | Default Acc | Calibrated Acc | ACER | APCER | BPCER | ROC-AUC | PR-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **combined_svm** | Combined (6,103D) | 0.0051 | 21.05% | **96.49%** | **0.0680** | 0.0132 | 0.1228 | **0.9878** | **0.9967** |
| **logistic_regression** | Combined (6,103D) | 0.0016 | 25.26% | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9769** | **0.9912** |
| **hog_svm** | HOG (6,084D) | 0.0040 | 21.05% | **96.14%** | **0.0899** | 0.0044 | 0.1754 | **0.9867** | **0.9964** |
| **hist_gradient_boosting**| Combined (6,103D) | 0.0006 | 51.58% | **96.14%** | **0.0965** | 0.0000 | 0.1930 | **0.9911** | **0.9971** |
| **extra_trees** | Combined (6,103D) | 0.2526 | 52.28% | **95.44%** | **0.1140** | 0.0000 | 0.2281 | **0.9950** | **0.9987** |
| **rf_combined** | Combined (6,103D) | 0.2670 | 58.60% | **95.09%** | **0.1228** | 0.0000 | 0.2456 | **0.9879** | **0.9965** |
| **linear_svm** | Combined (6,103D) | 0.0010 | 21.75% | **95.09%** | **0.1162** | 0.0044 | 0.2281 | **0.9675** | **0.9854** |
| **voting_ensemble** | GLCM (5D) | 0.1631 | 57.54% | **89.12%** | **0.1535** | 0.0789 | 0.2281 | 0.8688 | 0.9364 |
| **stacking_ensemble**| GLCM (5D) | 0.4435 | 80.00% | **88.07%** | **0.1338** | 0.1096 | 0.1579 | **0.9044** | **0.9598** |
| **custom_cnn** | PyTorch (Face) | 0.5000 | 87.72% | **87.72%** | **0.1096** | 0.1316 | 0.0877 | **0.9601** | — |
| **lbp_svm** | LBP (10D) | 0.0917 | 53.33% | **82.46%** | **0.2083** | 0.1535 | 0.2632 | 0.8503 | 0.9218 |
| **lda** | GLCM (5D) | 0.5580 | 80.70% | **76.49%** | **0.1996** | 0.2588 | 0.1404 | 0.8690 | 0.9304 |
| **gaussian_nb** | GLCM (5D) | 0.3712 | 52.28% | **60.35%** | **0.3004** | 0.4605 | 0.1404 | 0.8560 | 0.9068 |
| **glcm_rf** | GLCM (5D) | 0.4196 | 51.58% | **52.98%** | **0.3202** | 0.5702 | 0.0702 | 0.9058 | 0.9644 |
| **knn** | GLCM (5D) | 0.5921 | 43.51% | **37.54%** | **0.4167** | 0.7632 | 0.0702 | 0.6682 | 0.8942 |

---

## 4. Verification & Acceptance
- **Automated Tests:** 23/23 tests passing (`pytest tests/ -v`).
- **Dependencies:** `pip check` confirmed zero broken requirements.
- **Streamlit Pages:** 14/14 pages passing (`scripts/test_all_pages.py`).
- **Inference Service:** Verified multi-model polymorphic routing, threshold handling, and safety states.
- **Reports:** All 8 requested dataset and provenance reports generated under `reports/`.
- **Predictions:** 15 model prediction logs generated under `reports/predictions/`.
