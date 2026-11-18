# Dataset Annotation Audit

## Scope and method

This audit inspects the existing MONOT and ONOT inventories, filenames, folder structure and accompanying annotation files without modifying or rescanning image pixels. No labels are approved automatically.

## Evidence discovered

- The inventories contain 46,792 records: MONOT 24,140 and ONOT 22,652.
- No image-level CSV, Excel, JSON or XML ground-truth manifest was found in either raw dataset.
- ONOT contains three `threshold=*_cosine_images.txt` files. They are threshold/subset membership lists, not genuine/morphed labels.
- MONOT Morphed filenames encode two source subject-style identifiers and morph parameters; this is generation provenance, not reviewer-approved ground truth.
- MONOT Gate_10 and Gate_25 filenames expose source-style identifiers and acquisition strata; they are not automatically classes.
- ONOT folder and filename conventions expose subject identifiers and digital/print-scan acquisition variants.

The generated inventory is `data/manifests/annotation_inventory.csv`; its summary is `data/metadata/annotation_audit_summary.json`. Every row is `pending_review` and `not_approved`.

## Decision

The evidence supports provenance-aware restricted analyses and a human-review workflow, but not an approved binary detector. A reviewed manifest must supply verified label, evidence source, reviewer, identity/pair grouping and exclusion decisions before training.
