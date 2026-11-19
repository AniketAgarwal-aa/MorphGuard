# MorphGuard Biometric Privacy, Security & Research Ethics

**Applicable Guidelines:** GDPR Article 9 (Special Category Biometric Data), CC BY-NC 4.0 Research Governance  

---

## 1. Biometric Data Governance & Isolation

Biometric facial images constitute sensitive personal data under global data protection frameworks (such as GDPR Art. 9). MorphGuard strictly enforces a **Zero-Biometric-Leakage Architecture**:

1. **Strict Version Control Defenses:**
   The repository `.gitignore` explicitly isolates all raw biometric archives (`MONOT/`, `ONOT/`), intermediate face crops (`data/cache/`), and precomputed tensor representations.
2. **No Repository Embedding:**
   Neither the public GitHub repository nor any public commit history contains subject face photographs or biometric templates.
3. **Stateless Processing:**
   When an image is processed via the web interface or API, it is decoded in transient memory, evaluated, and immediately released. No uploaded user images are logged to persistent disk or transmitted to third parties.

---

## 2. Licensing & Redistribution Rights

1. **Source Code:**
   The MorphGuard application and pipeline code are provided for academic research and educational evaluation.
2. **Underlying Datasets (MONOT & ONOT):**
   The primary biometric corpora utilized in this research are licensed under **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.
3. **Model Weights:**
   Trained model checkpoints represent mathematical derivatives trained directly on biometric representations derived from MONOT and ONOT. In strict adherence to CC BY-NC 4.0 Section 3, these trained model weights **cannot be commercialized** and must retain non-commercial research licensing.

---

## 3. Ethical Considerations in Automated Border Control

1. **Impact of Asymmetric Errors:**
   - **False Acceptance (High APCER):** Allows a morphed identity to pass border inspection, creating a national security vulnerability.
   - **False Rejection (High BPCER):** Rejects a legitimate traveler, causing inconvenience, secondary screening, and potential traveler distress.
2. **Demographic Equity:**
   Facial recognition and morph detection models can exhibit disparate accuracy across demographic groups (age, gender, ethnicity) if datasets lack diversity. MorphGuard is explicitly documented as an academic research platform and is **not certified for autonomous real-world border deployment**.
3. **Dual-Use Safeguards:**
   This research is intended solely for defensive biometric presentation attack detection and research reproducibility.
