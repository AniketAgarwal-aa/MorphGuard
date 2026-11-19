# MorphGuard Scientific Methodology & Mathematical Foundations

**Version:** 3.2  
**Standard Compliance:** ISO/IEC 30107-3 Biometric Presentation Attack Detection  

---

## 1. Problem Formulation: Facial Morph Attack Detection

A facial morphing attack involves combining facial photographs of two or more distinct subjects (e.g., an accomplice and a malicious applicant) into a single composite synthetic face. When enrolled into an Automated Border Control (ABC) system or Electronic Machine Readable Travel Document (eMRTD), the morphed credential matches the biometrics of both individuals, defeating verification checks.

MorphGuard addresses **Single-Image Morph Attack Detection (No-Reference MAD)**, wherein an algorithm must classify an image $I$ as bona fide (genuine) or morphed without access to a paired reference gallery image:

$$f(I) \rightarrow y \in \{\text{GENUINE}, \text{MORPHED}\}$$

---

## 2. Feature Extraction Pipelines

MorphGuard employs both handcrafted multi-scale texture descriptors and deep convolutional representations to capture high-frequency interpolation artefacts, ghosting contours, and micro-texture inconsistencies.

### 2.1 Handcrafted Texture Descriptors
1. **Histogram of Oriented Gradients (HOG):**
   - Captures local edge gradients and geometric contour transitions.
   - Parameters: $16 \times 16$ pixels per cell, $2 \times 2$ cells per block, 9 orientation bins.
   - Vector Dimensionality: **6,084 dimensions**.
2. **Local Binary Patterns (LBP):**
   - Encodes fine-grained surface roughness and pixel-level texture discontinuities.
   - Circular uniform pattern with radius $R=1$, points $P=8$.
   - Vector Dimensionality: **10 dimensions** (normalized histogram).
3. **Gray-Level Co-occurrence Matrix (GLCM):**
   - Evaluates second-order statistical spatial relationships of pixel intensities.
   - Computed across distances $d \in \{1, 3, 5\}$ and angles $\theta \in \{0, \frac{\pi}{4}, \frac{\pi}{2}, \frac{3\pi}{4}\}$.
   - Scalar features: Contrast, Dissimilarity, Homogeneity, Energy, Correlation.
   - Vector Dimensionality: **5 dimensions** (directionally averaged).
4. **Combined Feature Vector:**
   - Concatenation of HOG, LBP, and GLCM vectors: $6084 + 10 + 5 + 4 \text{ (quality metrics)} = \mathbf{6,103 \text{ dimensions}}$.

### 2.2 Deep Convolutional Architectures
Deep models process face crops normalized to $224 \times 224$ pixels:
1. **Custom CNN:** Lightweight 4-layer convolutional network with BatchNorm and Dropout ($241\text{ KB}$).
2. **Residual Networks (ResNet-18, ResNet-34, ResNet-50):** Skip-connection residual backbones extracting hierarchical semantic features.
3. **MobileNet-V3 Small:** Inverted bottleneck architecture with squeeze-and-excitation blocks optimized for low-latency CPU environments ($6.2\text{ MB}$).
4. **EfficientNet-B0:** Compound-scaled neural architecture balancing depth, width, and resolution ($16.3\text{ MB}$).
5. **DenseNet-121:** Dense connectivity pattern maximizing feature reuse across dense blocks ($28.4\text{ MB}$).

---

## 3. Evaluation Metrics & ISO/IEC 30107-3 Compliance

Biometric MAD performance is evaluated using standardized ISO/IEC 30107-3 presentation attack detection metrics:

1. **Attack Presentation Classification Error Rate (APCER):**
   The proportion of morphed images incorrectly classified as genuine (false acceptance of an attack):
   $$\text{APCER} = \frac{\sum_{i=1}^{N_{\text{morph}}} \mathbb{I}(f(I_i^{\text{morph}}) = \text{GENUINE})}{N_{\text{morph}}}$$

2. **Bona Fide Presentation Classification Error Rate (BPCER):**
   The proportion of genuine images incorrectly classified as morphed (false rejection of a legitimate subject):
   $$\text{BPCER} = \frac{\sum_{j=1}^{N_{\text{bona}}} \mathbb{I}(f(I_j^{\text{bona}}) = \text{MORPHED})}{N_{\text{bona}}}$$

3. **Average Classification Error Rate (ACER):**
   The unweighted arithmetic mean of APCER and BPCER:
   $$\text{ACER} = \frac{\text{APCER} + \text{BPCER}}{2}$$

4. **Area Under the ROC Curve (ROC-AUC):**
   Measures discrimination capability across all possible decision thresholds.

---

## 4. Scientific Protocol: Validation-Only Threshold Tuning

In operational MAD systems, the default threshold $\tau = 0.5$ is frequently sub-optimal due to class imbalance and asymmetric cost functions.

MorphGuard enforces a strict scientific protocol:
1. **Calibration on Validation Set Only:**
   The optimal operational threshold $\tau^*$ is selected by evaluating the validation split and finding the threshold that minimizes ACER:
   $$\tau^* = \arg\min_{\tau \in [0, 1]} \text{ACER}_{\text{val}}(\tau)$$
2. **Strict Test Isolation:**
   The test split (285 samples) is held out completely. Test evaluation occurs once using $\tau^*$. Under no circumstances is $\tau^*$ adjusted on the test set.
