# MorphGuard V3.2 — Final Public Hugging Face 21-Model Verification Report

**Repository ID:** `AniketAgarwal-aa/MorphGuard-Models`  
**Visibility:** **PUBLIC** (Unrestricted Token-Free Download Verified)  
**Remote Commit Revision SHA:** `ca3e7399924818e118b464d145b06b95a9e7e898`  
**Total Remote Files:** 67  
**Preserved Prior Files:** 45 files (Unmodified)  
**New Files Created:** 18 files (6 deep PyTorch models, 6 root aliases, 6 metadata JSONs)  
**Updated Files:** 3 files (`model_registry.json`, `metadata/model_registry.json`, `README.md`)  
**Deletions:** 0 files  

---

## 1. 21-Model Remote Cryptographic Verification

| Architecture | Checkpoint Path | Expected Local SHA-256 | Remote LFS SHA-256 | Status |
| :--- | :--- | :--- | :--- | :---: |
| **combined_svm** | `classical/combined_svm.joblib` | `edcdbb4bfe60...` | `edcdbb4bfe60...` | **VERIFIED** |
| **custom_cnn** | `deep_learning/custom_cnn.pt` | `f141d2b38e94...` | `f141d2b38e94...` | **VERIFIED** |
| **extra_trees** | `classical/extra_trees.joblib` | `6ea40abb5be7...` | `6ea40abb5be7...` | **VERIFIED** |
| **gaussian_nb** | `classical/gaussian_nb.joblib` | `b26ce942d6c1...` | `b26ce942d6c1...` | **VERIFIED** |
| **glcm_rf** | `classical/glcm_rf.joblib` | `9e877b1f8aac...` | `9e877b1f8aac...` | **VERIFIED** |
| **hist_gradient_boosting** | `classical/hist_gradient_boosting.joblib` | `9d7558d62dad...` | `9d7558d62dad...` | **VERIFIED** |
| **hog_svm** | `classical/hog_svm.joblib` | `5b1608dc820c...` | `5b1608dc820c...` | **VERIFIED** |
| **knn** | `classical/knn.joblib` | `27b743888d75...` | `27b743888d75...` | **VERIFIED** |
| **lbp_svm** | `classical/lbp_svm.joblib` | `c03852ef4892...` | `c03852ef4892...` | **VERIFIED** |
| **lda** | `classical/lda.joblib` | `dd44eb2d0466...` | `dd44eb2d0466...` | **VERIFIED** |
| **linear_svm** | `classical/linear_svm.joblib` | `7d4718f3f2b7...` | `7d4718f3f2b7...` | **VERIFIED** |
| **logistic_regression** | `classical/logistic_regression.joblib` | `e3dc99ae4b75...` | `e3dc99ae4b75...` | **VERIFIED** |
| **rf_combined** | `classical/rf_combined.joblib` | `17408ba87482...` | `17408ba87482...` | **VERIFIED** |
| **stacking_ensemble** | `ensembles/stacking_ensemble.joblib` | `fc926697ed5c...` | `fc926697ed5c...` | **VERIFIED** |
| **voting_ensemble** | `ensembles/voting_ensemble.joblib` | `5ff29f33953d...` | `5ff29f33953d...` | **VERIFIED** |
| **resnet18** | `deep_learning/resnet18.pt` | `4887d7e6dbd0...` | `4887d7e6dbd0...` | **VERIFIED** |
| **efficientnet_b0** | `deep_learning/efficientnet_b0.pt` | `ef6d7e5a4dfb...` | `ef6d7e5a4dfb...` | **VERIFIED** |
| **mobilenet_v3_small** | `deep_learning/mobilenet_v3_small.pt` | `30ef3bf8670c...` | `30ef3bf8670c...` | **VERIFIED** |
| **densenet121** | `deep_learning/densenet121.pt` | `9169572094dc...` | `9169572094dc...` | **VERIFIED** |
| **resnet34** | `deep_learning/resnet34.pt` | `fdbc80dc8ee7...` | `fdbc80dc8ee7...` | **VERIFIED** |
| **resnet50** | `deep_learning/resnet50.pt` | `f8927bc503ef...` | `f8927bc503ef...` | **VERIFIED** |

---

## 2. Anonymous Token-Free Download Verification
All downloads executed with `token=None` to simulate anonymous public visitor access.

| Model Name | Remote Path | Download Size | SHA-256 Verification | Status |
| :--- | :--- | :---: | :---: | :---: |
| **combined_svm** | `C:\Users\admin\AppData\Local\Temp\morphguard_anon_test_bzb6a_62\classical\combined_svm.joblib` | Verified | `edcdbb4bfe60...` | **PASS** |
| **hog_svm** | `C:\Users\admin\AppData\Local\Temp\morphguard_anon_test_bzb6a_62\classical\hog_svm.joblib` | Verified | `5b1608dc820c...` | **PASS** |
| **voting_ensemble** | `C:\Users\admin\AppData\Local\Temp\morphguard_anon_test_bzb6a_62\ensembles\voting_ensemble.joblib` | Verified | `5ff29f33953d...` | **PASS** |
| **efficientnet_b0** | `C:\Users\admin\AppData\Local\Temp\morphguard_anon_test_bzb6a_62\deep_learning\efficientnet_b0.pt` | Verified | `ef6d7e5a4dfb...` | **PASS** |
| **resnet18** | `C:\Users\admin\AppData\Local\Temp\morphguard_anon_test_bzb6a_62\deep_learning\resnet18.pt` | Verified | `4887d7e6dbd0...` | **PASS** |
| **resnet50** | `C:\Users\admin\AppData\Local\Temp\morphguard_anon_test_bzb6a_62\deep_learning\resnet50.pt` | Verified | `f8927bc503ef...` | **PASS** |

---

## 3. Real Downloaded Inference Sanity Test

- **Combined SVM (Threshold: 0.0051):** PASS  
- **EfficientNet-B0 (Threshold: 0.0032):** PASS  

### Final Conclusion
The public Hugging Face repository `AniketAgarwal-aa/MorphGuard-Models` is 100% synchronized, cryptographically identical to the local V3.2 export, publicly downloadable without credentials, and fully operational.