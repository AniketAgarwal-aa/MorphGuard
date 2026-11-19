# MorphGuard V3.0 — Biometric Dataset Documentation

## 1. Inventory & Composition
MorphGuard utilizes two primary facial biometric corpora:

### 1.1 MONOT (Morphed and Original National Identification Images Dataset)
- **Total Images:** 24,140
- **Strata:**
  - `Gate_10`: 2,550 images. Live operational gate camera capture at 10-meter operational distance.
  - `Gate_25`: 6,350 images. Live operational gate camera capture at 25-meter operational distance.
  - `Morphed`: 15,240 images. Algorithmic facial morphing attack candidates generated via automated landmark-based Delaunay triangulation mesh warping.
- **Characteristics:** Genuine samples have high sharpness (mean blur variance: 370–373); morphed samples exhibit linear interpolation smoothing across triangular meshes (mean blur variance: 140.8).

### 1.2 ONOT (Official National Identity Test Corpus)
- **Total Images:** 22,652
- **Strata:**
  - `digital`: 11,326 images. High-resolution electronic passport photos compliant with ICAO Doc 9303 (mean blur variance: 414.8).
  - `print-scan`: 11,326 images. Analog print-and-scan recapture reproductions simulating printed document acquisition (mean blur variance: 63.2).
- **Provenance Limitation:** ONOT lacks verified paired morph generation records in this repository. Digital and print-scan variants represent acquisition dimensions, not bona fide vs. attack ground truth.

### 1.3 Total Processed Inventory
- **Combined Images:** **46,792 images** (100% processed and cached across 182 compressed NPZ shards).
- **Corrupt / Unreadable Files:** 0.
- **Overall Face Detection Rate:** 99.02% (46,333 / 46,792).

---

## 2. Label Governance & Reviewed Manifest
Supervised learning is strictly restricted to verified ground truth:
- **Approved Manifest (`data/manifests/reviewed_label_manifest.csv`):** 1,197 records.
  - `morphed`: 900 records (all from verified MONOT Delaunay morph pairs `subject_1|subject_2`).
  - `genuine`: 297 records (273 from MONOT `Gate_10` bona fide gate captures, 24 from ONOT verified digital captures).
- **Unlabelled Candidates:** 45,595 records (detailed in `reports/unlabelled_samples.csv`).
  - MONOT `Gate_25` (6,350 samples): Unverified gate threshold operational membership.
  - ONOT `print-scan` & `digital` (22,628 samples): Awaiting paired morph logs.
  - MONOT `Morphed` reserve (14,340 samples): Reserve candidates awaiting independent human reviewer protocol.
