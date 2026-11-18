# MorphGuard project report

## Abstract

MorphGuard is a local, batch-oriented research implementation for facial morphing attack detection. It supports image validation, face localisation, quality assessment, LBP/HOG/GLCM/statistical features, conventional classifiers, PyTorch model definitions, grouped splitting, thresholded inference, and a Streamlit interface.

## Methodology and limitation

All raw MONOT and ONOT records remain untouched. Manifest generation is streaming; feature extraction produces resumable shards. Splits group subject identifiers. MONOT/ONOT source compatibility must be evaluated before any combined classification claim; no fabricated results are reported.
