# Cross-Dataset Compatibility

MONOT and ONOT differ in generation and acquisition design. Combining MONOT Morphed with all ONOT images as a binary task would confound attack status with dataset source, camera/print-scan process, filename conventions and subject composition. Gate strata and ONOT threshold subsets are not class labels.

Scientifically defensible work now includes metadata/quality analysis, threshold-stratum analysis, provenance review and preprocessing/feature smoke tests. A validated cross-source detector requires reviewed image-level labels, subject and morph-pair grouping, duplicate checks and a pre-registered leakage-safe split. Until then, no binary metrics or detector claims are permitted.
