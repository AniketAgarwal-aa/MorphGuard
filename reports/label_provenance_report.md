# MorphGuard V3.0 — Label Provenance Report

**Generated:** 2026-11-19 07:40:26 UTC  
**Approved Label Manifest Records:** 1197  
**Unlabelled Candidate Images:** 45595  

---

## 1. Provenance Grounding Principles

1. **Defensible Ground Truth:**
   - Morphed images are approved only when generated through verified Delaunay triangulation mesh blending pairs (`subject_id_1|subject_id_2`).
   - Genuine images are approved from verified bona fide acquisition streams (`Gate_10` in MONOT and verified `digital` captures in ONOT).
2. **Rejection of Unverified Categories:**
   - `Gate_25` images in MONOT are maintained as unlabelled due to uncalibrated operational gate threshold uncertainty.
   - ONOT `print-scan` samples without paired morphs remain unlabelled for morph classification to prevent spurious cross-domain confounding.
3. **Auditability:**
   - 100% of approved records have reviewer metadata, provenance source logs, and fixed version stamps (`manifest_version: 1.0.0`).
