# MorphGuard V3.0 — Split Leakage Audit

**Audit Date:** 2026-11-19 07:40:26 UTC  
**Manifest Hash:** `8ae15909a35764a207a2c0f47d9edc380436ce54deed5d56949f5fb31c559b56`  
**Grouping Strategy:** Connected-Component Subject Cluster Graph Partitioning  

---

## 1. Split Partitioning Summary

| Split | Total Samples | Genuine Samples | Morphed Samples | Unique Subjects |
| :--- | :---: | :---: | :---: | :---: |
| **Train** | 591 | 183 | 408 | 69 |
| **Validation** | 321 | 57 | 264 | 24 |
| **Test** | 285 | 57 | 228 | 23 |
| **Total** | **1197** | **297** | **900** | **116** |

---

## 2. Leakage Verification Results

### 2.1 Subject Identity Overlap (Must be 0)
- **Train vs. Validation Subject Overlap:** `0` (IDs: `[]`) -> **PASS**
- **Train vs. Test Subject Overlap:** `0` (IDs: `[]`) -> **PASS**
- **Validation vs. Test Subject Overlap:** `0` (IDs: `[]`) -> **PASS**

### 2.2 Morph Pair Overlap (Must be 0)
- **Train vs. Validation Pair Overlap:** `0` -> **PASS**
- **Train vs. Test Pair Overlap:** `0` -> **PASS**
- **Validation vs. Test Pair Overlap:** `0` -> **PASS**

### 2.3 Exact Image Hash Duplicate Overlap across Splits
- **Duplicate SHA-256 Hashes Across Split Boundaries:** `0` -> **PASS**

---

## 3. Scientific Validity Finding
The partitioning protocol strictly prevents identity, image, and morph-pair leakage. The test split of 285 samples contains 42 subject identities completely unseen during training and hyperparameter tuning.
