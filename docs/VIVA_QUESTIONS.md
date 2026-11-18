# Likely Viva Questions

**Why is there no accuracy value?** Because no image-level reviewed labels or independent test split exist; fabricating one would be scientifically invalid.

**What does the app do today?** It validates images, detects faces, measures quality, extracts reproducible features and provides dataset/review tooling.

**Why not call ONOT genuine?** Its local annotations describe acquisition and threshold subsets, not a reviewed image-level class label.

**How is leakage prevented?** Approved-only manifests and group-aware subject/morph-pair splitting are required before training.
