# MorphGuard V3.0 — Feature Engineering Specification

## 1. Feature Representation (Schema `v1.0.0`)
All extracted biometric vectors are standardized into a 6,103-dimensional concatenated representation:

```
[ LBP (10D) | HOG (6,084D) | GLCM (5D) | Pixel Statistics (4D) ] = 6,103 Dimensions
```

### 1.1 Local Binary Patterns (LBP) — 10 Dimensions
- **Algorithm:** Uniform rotation-invariant LBP (`skimage.feature.local_binary_pattern`).
- **Parameters:** `P = 8` points, `R = 1.0` radius, method = `'uniform'`.
- **Dimensionality:** 10-bin histogram normalized to unit sum.
- **Biometric Purpose:** Captures micro-texture alterations and high-frequency edge discontinuities introduced by blending seams.

### 1.2 Histogram of Oriented Gradients (HOG) — 6,084 Dimensions
- **Algorithm:** Dense block-normalized directional gradient histograms (`skimage.feature.hog`).
- **Parameters:**
  - Input: 224x224 grayscale aligned face crop.
  - Orientations: 9 angular bins.
  - Pixels per cell: 8x8 pixels (28x28 grid).
  - Cells per block: 2x2 cells (27x27 blocks).
  - Block normalization: L2-Hys.
- **Dimensionality:** $27 \times 27 \times 4 \times 9 = 6,084$ dimensions.
- **Biometric Purpose:** Captures structural geometry distortions around facial landmarks (eyes, nose, mouth corners) caused by linear mesh triangulation warping.

### 1.3 Gray-Level Co-occurrence Matrix (GLCM) — 5 Dimensions
- **Algorithm:** Spatial gray-level co-occurrence analysis (`skimage.feature.graycomatrix` + `graycoprops`).
- **Parameters:** Distances: `[1]`, Angles: `[0, \pi/4, \pi/2, 3\pi/4]`, 256 gray levels.
- **Computed Descriptors (averaged across 4 angles):**
  1. `contrast`: Measures local gray-level variations ($\sum |i-j|^2 p(i,j)$).
  2. `dissimilarity`: Measures linear differences ($\sum |i-j| p(i,j)$).
  3. `homogeneity`: Measures closeness of element distribution to diagonal.
  4. `energy`: Angular second moment (uniformity of texture).
  5. `correlation`: Joint probability occurrence of pixel pairs.
- **Dimensionality:** 5 scalar metrics.
- **Biometric Purpose:** Quantifies micro-texture smoothness. Linear triangular blending significantly reduces contrast (Genuine mean contrast: 391.1 vs Morphed mean contrast: 199.8).

### 1.4 Statistical Descriptors — 4 Dimensions
- **Computed Properties:**
  1. Mean grayscale intensity.
  2. Standard deviation of intensity (global contrast).
  3. Shannon entropy of intensity histogram.
  4. Canny edge density (ratio of edge pixels to total area).
- **Dimensionality:** 4 scalar metrics.

---

## 2. Integrity and Storage
- **Storage Format:** Compressed NumPy archives (`features_*.npz`) in `data/cache/image_features/`.
- **Arrays per shard:** `X` (6,103D), `lbp` (10D), `hog` (6,084D), `glcm` (5D), `stats` (4D), `paths` (string identifiers).
- **Validation:** 100% of 46,792 samples validated finite, float64/float32, 0 NaNs or Inf values.
