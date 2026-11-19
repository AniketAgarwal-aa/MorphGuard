# MorphGuard Biometric Dataset & Provenance Documentation

**Corpus Scope:** MONOT and ONOT Biometric Datasets  
**Total Processed Images:** 46,792  
**Reviewed Manifest Records:** 1,197  
**Unlabelled Reserve:** 45,595  

---

## 1. Biometric Corpora Overview

MorphGuard operates on two recognized biometric research datasets:

| Corpus | Stratum / Category | Acquisition Mode | Total Images | Processing Status |
| :--- | :--- | :--- | :---: | :---: |
| **MONOT** | `Gate_10` (Bona Fide) | Controlled ABC border gate | 2,550 | 100% Cached (2,550) |
| **MONOT** | `Gate_25` (Semi-Controlled) | Variable lighting/pose | 6,350 | 100% Cached (6,350) |
| **MONOT** | `Morphed` | Delaunay triangulated morphs | 15,240 | 100% Cached (15,240) |
| **ONOT** | `digital` | ICAO compliant digital passport | 11,326 | 100% Cached (11,326) |
| **ONOT** | `print-scan` | Physical print and recapture | 11,326 | 100% Cached (11,326) |
| **Total** | **All 5 Strata** | — | **46,792** | **100% Cached (3.39 GB)** |

---

## 2. Feature Cache Architecture

All 46,792 images have been fully preprocessed, face-cropped, and transformed into 6,103-dimensional feature vectors stored in 182 compressed NPZ shards under `data/cache/image_features/`.
- Every feature record contains verified float32/float64 finite numeric values (zero NaN or Inf occurrences).
- Mean face detection rate across the complete corpus: **99.02%**.

---

## 3. Label Provenance & Human-in-the-Loop Audit

Due to inconsistent or missing ground-truth metadata in raw archives, MorphGuard established a strict **Ground-Truth Provenance Policy**:
1. Only samples with cryptographic cross-reference, folder-level evidence, or manual expert audit approval were admitted to the reviewed training manifest.
2. An audit of 1,197 records yielded:
   - Genuine: 297 samples
   - Morphed: 900 samples
3. The remaining **45,595 images** are maintained in an **Unlabelled Research Reserve** (`reports/unlabelled_samples.csv`). They are fully cached and available for exploratory unsupervised analysis, but strictly excluded from supervised model training to avoid label noise.

---

## 4. Subject-Disjoint Partitioning (Zero Identity Leakage)

To prevent data leakage caused by subject identity overlap across splits, MorphGuard employs **Graph-Connected Component Partitioning**:
- All images originating from the same physical subject (or morph pairs involving that subject) are clustered into an exclusive subject group.
- Partitions are allocated at the cluster level:

| Partition | Total Samples | Morphed | Genuine | Subject Clusters | Usage |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Train** | 591 | 408 | 183 | 101 | Supervised classifier training |
| **Validation** | 321 | 264 | 57 | 52 | Hyperparameter tuning & threshold calibration ($\tau^*$) |
| **Test** | 285 | 228 | 57 | 42 | Unbiased final benchmark evaluation |

**Empirical Leakage Verification:**
- Train $\cap$ Validation Identity Overlap: **0**
- Train $\cap$ Test Identity Overlap: **0**
- Validation $\cap$ Test Identity Overlap: **0**
