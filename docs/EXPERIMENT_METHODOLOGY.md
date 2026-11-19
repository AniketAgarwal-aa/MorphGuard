# MorphGuard V3.0 — Experiment Methodology & Leakage Prevention

## 1. Grouped Partitioning Protocol
Face morph attack detection models are vulnerable to **identity leakage**: if images of the same subject appear in both training and test sets, the model learns facial recognition features rather than morphing artifacts.

### 1.1 Connected-Component Graph Partitioning
1. Build an undirected graph $G = (V, E)$ where vertices $V$ represent subject IDs.
2. For every morphed image created from subject pair $(s_1, s_2)$, add an edge $(s_1, s_2)$.
3. Compute connected components of $G$. Each component forms an indivisible subject cluster.
4. Distribute components into **Train (50%)**, **Validation (25%)**, and **Test (25%)** splits.

### 1.2 Leakage Verification Results
Audited in `reports/split_leakage_audit.md`:
- **Train vs. Validation Subject Overlap:** `0` (Zero shared identities).
- **Train vs. Test Subject Overlap:** `0` (Zero shared identities).
- **Validation vs. Test Subject Overlap:** `0` (Zero shared identities).
- **Morph Pair Overlap Across Partitions:** `0`.
- **Exact Hash (SHA-256) Duplicates Across Splits:** `0`.

---

## 2. Evaluation Protocol (ISO/IEC 30107-3 Standards)
All models are evaluated on the 285-sample unseen test set (228 morphed, 57 genuine) using standard biometric presentation attack metrics:

$$\text{APCER} = \frac{\text{FN}}{\text{TP} + \text{FN}} \quad (\text{Attack Presentation Classification Error Rate / Missed Morphs})$$
$$\text{BPCER} = \frac{\text{FP}}{\text{TN} + \text{FP}} \quad (\text{Bona Fide Presentation Classification Error Rate / False Alarms})$$
$$\text{ACER} = \frac{\text{APCER} + \text{BPCER}}{2} \quad (\text{Average Classification Error Rate})$$

Thresholds $\tau^*$ are optimized strictly on the **Validation split** and never on the Test split.
