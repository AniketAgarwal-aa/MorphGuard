# MorphGuard V3.0 — Known Limitations & Research Boundaries

## 1. Morph Generation Confounding
- All 900 approved morphed images in the label manifest originate from MONOT landmark-based Delaunay triangulation mesh blending.
- While models achieve up to **96.49%** test accuracy on held-out MONOT subjects, this performance measures detection of Delaunay triangular mesh interpolation artifacts (smoothing, gradient alignment).
- Models cannot be assumed to generalize to deep learning morphing (e.g. GAN-based style-mixing, diffusion morphing, or commercial face-swapping) without retraining.

## 2. ONOT Corpus Label Asymmetry
- ONOT contains 11,326 digital and 11,326 print-scan bona fide acquisitions.
- The repository does not contain paired morph generation logs for ONOT.
- Attempting to treat ONOT digital as "genuine" and ONOT print-scan as "morphed" would represent a scientifically invalid confounding of capture modality with biometric attack status.

## 3. Hardware & Compute Constraints
- Development and benchmarking were conducted in a CPU-only environment (Windows 11, 8 cores, 7.85 GB RAM).
- Heavier deep architectures (`resnet18`, `resnet50`, `efficientnet_b0`, `densenet121`) are implemented and verified in the codebase, but tagged as `ready_for_training` pending GPU compute cluster resources.
- Real-time client-side inference on 6,103D feature vectors takes ~80–120ms per face on CPU.

## 4. Certification Scope
- MorphGuard is an academic and engineering research testbed.
- It is **not** an operational biometric product certified under ISO/IEC 19794-5 or ISO/IEC 30107-3 compliance frameworks.
