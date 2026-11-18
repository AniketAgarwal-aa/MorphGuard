# Human Annotation Review Guide

Review `data/manifests/annotation_inventory.csv` in batches. For each record, inspect the image and available provenance, verify the subject/pair relationship, record an evidence source and reviewer identity, then choose `approved`, `rejected`, `excluded` or `uncertain`. Approval requires an explicit verified class (`genuine` or `morphed`), evidence and notes; `unknown` or missing evidence cannot enter training. Preserve the original proposed interpretation and never convert folder names into labels. Review MONOT and ONOT separately before considering a cross-source protocol.

The inventory is intentionally fully pending. Back up the manifest before edits and validate it with `scripts/validate_label_manifest.py` and the test suite after each batch.
