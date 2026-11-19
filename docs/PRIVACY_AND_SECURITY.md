# MorphGuard V3.0 — Privacy, Security & Biometric Governance

## 1. Biometric Data Protection Principles
MorphGuard enforces strict data safety controls:
1. **Zero Raw Biometric Data in Version Control:**
   - `MONOT/` and `ONOT/` corpora are excluded via `.gitignore`.
   - Feature caches (`data/cache/`) and reviewer SQLite databases are excluded.
   - Scripts refuse to stage or commit raw facial images.
2. **In-Memory Volatile Processing:**
   - User-uploaded images in the live analysis page are processed in memory and discarded upon session completion. No biometric images are permanently stored on the host filesystem during web inference.
3. **Traceability Without Exposure:**
   - Reviewer annotations and audit trails use pseudonymous identifiers.
   - Public logs strip sensitive local paths and participant personally identifiable information.

---

## 2. Model Governance Safeguards
- **Clear Research Status:** Displays `EXPERIMENTAL RESEARCH PROTOTYPE` badges in all UI headers.
- **Fail-Safe Inference:** When face detection fails or no model is selected, outputs explicit diagnostic states (`FACE NOT DETECTED`, `MODEL UNAVAILABLE`) instead of fabricated scores.
- **No Overclaiming:** Explicitly documents that models trained on MONOT Delaunay mesh morphs cannot claim cross-dataset generalization to unseen morph algorithms without compatible validation data.
